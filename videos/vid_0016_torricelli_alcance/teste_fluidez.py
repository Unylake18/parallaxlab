"""Teste de fluidez (15 fps × 30 fps): trecho de ~10 s da varredura S1 com barras, cotas e marcador do gráfico.

  uv run python -m manim -r 540,960 --fps 30 --media_dir videos/vid_0016_torricelli_alcance/media_teste videos/vid_0016_torricelli_alcance/teste_fluidez.py Teste30
  uv run python -m manim -r 540,960 --fps 15 --media_dir videos/vid_0016_torricelli_alcance/media_teste videos/vid_0016_torricelli_alcance/teste_fluidez.py Teste30
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cena import *          # noqa: F401,F403
from cena import _Vid0016


class Teste30(_Vid0016):
    DUR = 10.0
    INTERP = False

    def u_sched(self, t):
        return float(u1(F248 + t / TC1))

    def construct(self):
        self.preparar()
        U = self.U
        self.img = self.seq_img(self.s1, lambda t: clip(F248 + t / TC1, F248, 1 + F248))
        self.add(self.img)
        self.vivas = self.cotas_vivas()
        self.add(self.vivas)
        b_v, l_v, n_v = self.barra("v", V_COL, -4.4, lambda u: 5.6 * np.sqrt(1 - u), "velocidade de saída")
        b_t, l_t, n_t = self.barra("t", T_COL, -5.3, lambda u: 5.6 * np.sqrt(u), "tempo de voo")
        self.add(b_v, l_v, n_v, b_t, l_t, n_t)
        axes = Axes(x_range=[0, 1, 0.5], y_range=[0, 1, 1], x_length=6.2, y_length=2.6, tips=False,
                    axis_config={"stroke_width": 2.5, "color": MUTED, "include_ticks": True, "tick_size": 0.07}).move_to([0.3, -2.7, 0])
        self.add(axes)
        f = lambda: 2 * np.sqrt(U.get_value() * (1 - U.get_value()))
        self.add(always_redraw(lambda: Dot(axes.c2p(U.get_value(), f()), radius=0.12, color=WHITE).set_z_index(8)))
        self.umin, self.umax = ValueTracker(0.65), ValueTracker(0.65)

        def acompanhar(m, dt):
            u = U.get_value()
            self.umin.set_value(min(self.umin.get_value(), u))
            self.umax.set_value(max(self.umax.get_value(), u))

        self.add(Mobject().add_updater(acompanhar))
        th = lambda u: float(np.arcsin(np.sqrt(clip(u, 0.0, 1.0))))

        def traco():
            a, b = th(self.umin.get_value()), th(self.umax.get_value())
            if b - a < 0.02:
                return VMobject()
            return ParametricFunction(lambda x: axes.c2p(np.sin(x) ** 2, np.sin(2 * x), 0), t_range=[a, b, 0.01], color=CYAN, stroke_width=4.5).set_z_index(4)

        self.add(always_redraw(traco))
        self.wait(self.DUR)

