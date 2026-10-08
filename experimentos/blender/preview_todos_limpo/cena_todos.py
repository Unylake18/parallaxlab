"""Os casos de Gauss no padrão do coaxial limpo: 3D do Blender permanente + Manim só com título, região, Q_env e E(r) (sandbox, fora do yt_0002).

Uma classe por caso (Scene). A trajetória p(k) vem de traj_gen.py (a mesma do Blender): o quadro k (30 fps) mostra a imagem renderizada para p(k) e o texto da
região usa o MESMO p(k). Sem dissolução entre imagens.

    uv run python -m manim -r 960,540 --fps 30 --media_dir media/preview_todos_limpo/<caso> experimentos/blender/preview_todos_limpo/cena_todos.py LinhaLimpo
Classes: LinhaLimpo CascaCilLimpo MacicoCilLimpo FolhaLimpo PlacaLimpo DuasLimpo FaceLimpo CascaEsfLimpo MacicoEsfLimpo CapEsfLimpo
"""

import sys
from collections import OrderedDict
from pathlib import Path

import numpy as np
from manim import DOWN, LEFT, RIGHT, FadeIn, FadeOut, ImageMobject, Scene, VGroup, config
from PIL import Image

HERE = Path(__file__).resolve().parent
RAIZ = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "teste_gauss_coaxial"))
from cena_manim import BACKGROUND_COLOR, BLUE_L, CYAN, VIOLET, WHITE, P, eq, text  # noqa: E402  (helpers da v1 do coaxial; ela não é alterada)
from traj_gen import CASOS, FPS, Traj  # noqa: E402

MAG = "#EA63FF"
PASTA = RAIZ / "renders" / "preview_todos_limpo"
RL, XMAX = 1.9, 6.95
Q = r"Q_{\mathrm{env}}"
EXPR = {"lin": r"\frac{\lambda}{2\pi\varepsilon_0 r}"}
t_ = lambda s: ("t", s)                  # noqa: E731
m_ = lambda s, cor=WHITE: ("m", s, cor)  # noqa: E731
sempre = lambda p: True                  # noqa: E731
menor = lambda x: (lambda p: p < x - 1e-3)             # noqa: E731
maior = lambda x: (lambda p: p >= x - 1e-3)            # noqa: E731
entre = lambda a, b: (lambda p: a - 1e-3 <= p <= b + 1e-3)    # noqa: E731
fora = lambda x: (lambda p: p > x + 1e-3)              # noqa: E731
LAM, SIG = m_(r"+\lambda", BLUE_L), m_(r"+\sigma", BLUE_L)

# regs: (condição em p, domínio, Q_env, E (tex do segundo membro; None = "=0"), nota, símbolo de E opcional)
UI = {
    "linha": dict(
        titulo=[t_("LINHA INFINITA ·"), LAM],
        regs=[(sempre, r"r>0", Q + r"=\lambda L", EXPR["lin"], "a área cresce; a carga não muda")],
        leg=[m_("r", VIOLET), t_("raio da gaussiana")]),
    "casca_cil": dict(
        titulo=[t_("CASCA CILÍNDRICA ·"), LAM],
        regs=[(menor(1.0), r"r<R", Q + "=0", None, "por dentro: nada envolvido"),
              (maior(1.0), r"r>R", Q + r"=\lambda L", EXPR["lin"], "por fora: igual à linha")],
        leg=[m_("R", BLUE_L), t_("raio da casca ·"), m_("r", VIOLET), t_("raio da gaussiana")]),
    "macico_cil": dict(
        titulo=[t_("CILINDRO MACIÇO ·"), m_(r"\rho", BLUE_L), t_("constante")],
        regs=[(menor(1.0), r"r<R", Q + r"=\rho\pi r^{2}L", r"\frac{\rho r}{2\varepsilon_0}", "a carga envolvida cresce com r²"),
              (maior(1.0), r"r>R", Q + r"=\rho\pi R^{2}L", r"\frac{\rho R^{2}}{2\varepsilon_0 r}", "fora do corpo: carga envolvida fixa")],
        leg=[m_("R", BLUE_L), t_("raio do cilindro ·"), m_("r", VIOLET), t_("raio da gaussiana")]),
    "folha": dict(
        titulo=[t_("FOLHA INFINITA ·"), SIG],
        regs=[(sempre, r"x>0", Q + r"=\sigma A", r"\frac{\sigma}{2\varepsilon_0}", "as tampas se afastam: E não muda")],
        leg=[m_("x", VIOLET), t_("posição das tampas ·"), m_("A", VIOLET), t_("área de cada tampa")]),
    "placa": dict(
        titulo=[t_("PLACA COM ESPESSURA ·"), m_(r"\rho", BLUE_L), t_("constante")],
        regs=[(menor(0.7), r"0<x<a", Q + r"=2\rho xA", r"\frac{\rho x}{\varepsilon_0}", "a carga envolvida cresce com x", "E_x"),
              (maior(0.7), r"x>a", Q + r"=2\rho aA", r"\frac{\rho a}{\varepsilon_0}", "fora da placa: campo constante", "E_x")],
        leg=[m_("a", BLUE_L), t_("meia-espessura ·"), m_("x", VIOLET), t_("posição das tampas")]),
    "duas": dict(
        titulo=[t_("DUAS FOLHAS ·"), SIG, t_("e"), m_(r"-\sigma", MAG)],
        regs=[(menor(-1.1), r"x<-d", Q + "=0", None, "fora: os campos se cancelam"),
              (entre(-1.1, 1.1), r"-d<x<d", Q + r"=\sigma A", r"\frac{\sigma}{\varepsilon_0}", "entre as folhas: os campos somam"),
              (fora(1.1), r"x>d", Q + r"=(\sigma-\sigma)A=0", None, "fora: os campos se cancelam")],
        leg=[m_("d", BLUE_L), t_("meia-distância ·"), m_("x", VIOLET), t_("tampa direita")]),
    "face": dict(
        titulo=[t_("FACE DE CONDUTOR ·"), m_(r"\sigma_{\mathrm{face}}", BLUE_L)],
        regs=[(sempre, r"x>0", Q + r"=\sigma_{\mathrm{face}}A", r"\frac{\sigma_{\mathrm{face}}}{\varepsilon_0}", "só a tampa de fora contribui", r"E_{\mathrm{fora}}")],
        leg=[m_("x", VIOLET), t_("tampa de fora ·"), t_("dentro do metal, E = 0")]),
    "casca_esf": dict(
        titulo=[t_("CASCA ESFÉRICA ·"), m_(r"+Q", BLUE_L)],
        regs=[(menor(1.0), r"r<R", Q + "=0", None, "por dentro: nada envolvido"),
              (maior(1.0), r"r>R", Q + "=Q", r"\frac{Q}{4\pi\varepsilon_0 r^{2}}", "por fora: como carga pontual")],
        leg=[m_("R", BLUE_L), t_("raio da casca ·"), m_("r", VIOLET), t_("raio da gaussiana")]),
    "macico_esf": dict(
        titulo=[t_("ESFERA MACIÇA ·"), m_(r"\rho", BLUE_L), t_("constante")],
        regs=[(menor(1.0), r"r<R", Q + r"=\frac{4}{3}\pi\rho r^{3}", r"\frac{\rho r}{3\varepsilon_0}", "a carga envolvida cresce com r³"),
              (maior(1.0), r"r>R", Q + r"=\frac{4}{3}\pi\rho R^{3}", r"\frac{\rho R^{3}}{3\varepsilon_0 r^{2}}", "fora do corpo: carga envolvida fixa")],
        leg=[m_("R", BLUE_L), t_("raio da esfera ·"), m_("r", VIOLET), t_("raio da gaussiana")]),
    "cap_esf": dict(
        titulo=[t_("CAPACITOR ESFÉRICO ·"), m_(r"+Q", BLUE_L), t_("e"), m_(r"-Q", MAG)],
        regs=[(menor(0.8), r"r<a", Q + "=0", None, "dentro do metal: nada envolvido"),
              (entre(0.8, 1.6), r"a<r<b", Q + "=Q", r"\frac{Q}{4\pi\varepsilon_0 r^{2}}", "o campo radial existe só no vão"),
              (fora(1.6), r"r>b", Q + "=Q-Q=0", None, "fora, no modelo ideal: E = 0")],
        leg=[m_("a", BLUE_L), t_("esfera interna ·"), m_("b", BLUE_L), t_("casca externa ideal")]),
}


def peca(q, size=24, op=0.92):
    return text(q[1], size, WHITE, op) if q[0] == "t" else eq(q[1], size=size + 4, color=q[2])


def linha(pedacos, size=24, op=0.92):
    return VGroup(*[peca(q, size, op) for q in pedacos]).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)


def encaixa(m, x_esq):
    """Alinha a borda esquerda em x_esq e, se passar da margem direita, reduz só o necessário."""
    m.move_to(P(0, m.get_center()[1])).align_to(P(x_esq, 0), LEFT)
    if m.get_right()[0] > XMAX:
        m.scale((XMAX - x_esq) / m.width, about_point=P(x_esq, m.get_center()[1]))
    return m


class CasoBase(Scene):
    CID = None

    def construct(self):
        assert config.frame_rate == FPS, f"use --fps {FPS}: a trajetória foi renderizada para {FPS} fps"
        cid = self.CID
        ui, T = UI[cid], Traj(CASOS[cid]["wps"])
        pasta = PASTA / cid / "1120x784"
        self.camera.background_color = BACKGROUND_COLOR
        cache = OrderedDict()

        def quadro(k):
            nome = pasta / f"q_{T.chave(k)}.png"
            if nome not in cache:
                cache[nome] = np.array(Image.open(nome).convert("RGBA"))
                while len(cache) > 24:
                    cache.popitem(last=False)
            return cache[nome]

        img = ImageMobject(quadro(0)).set_width(9.0).move_to(P(-3.0, -0.15))
        img.set_opacity(0.0)
        estado = {"k": 0, "t0": 0.0}

        regs = []
        for reg in ui["regs"]:
            cond, dom, q, e, nota = reg[:5]
            esq = reg[5] if len(reg) > 5 else "E"
            d = eq(dom, size=34, color=VIOLET).move_to(P(0, 1.55)).align_to(P(RL, 0), LEFT)
            qq = eq(q, size=40).move_to(P(0, 1.55)).align_to(P(max(RL + 1.85, d.get_right()[0] + 0.4), 0), LEFT)      # nunca encosta no domínio
            linha1 = VGroup(d, qq)
            if linha1.get_right()[0] > XMAX:
                linha1.scale((XMAX - RL) / (linha1.get_right()[0] - RL), about_point=P(RL, 1.55))
            ee = eq(esq, "=0", size=50, colors={0: CYAN}) if e is None else eq(esq, "=", e, size=50, colors={0: CYAN})
            nt = text(nota, 22, WHITE, 0.92)
            regs.append((cond, VGroup(linha1, encaixa(ee.move_to(P(0, 0.4)), RL), encaixa(nt.move_to(P(0, -0.55)), RL))))
        titulo = encaixa(linha(ui["titulo"]).move_to(P(0, 2.9)), RL)
        leg = encaixa(linha(ui["leg"], size=20, op=0.7).move_to(P(0, -3.55)), RL)

        def atualiza(m, dt=0):
            """Escolhe a imagem do quadro atual e o texto da região, a partir do tempo da cena (não de dt acumulado)."""
            k = min(max(int(round((self.time - estado["t0"]) * FPS)), 0), T.total - 1)
            if k != estado["k"] or m.stroke_opacity < 1:
                estado["k"] = k
                arr = quadro(k)
                m.pixel_array = arr.copy()
                m.orig_alpha_pixel_array = arr[:, :, 3]
                if m.stroke_opacity < 1:                      # preserva o FadeIn em andamento
                    m.pixel_array[:, :, 3] = (arr[:, :, 3] * m.stroke_opacity).astype(m.pixel_array.dtype)
            p = T.p_em_quadro(k)
            for cond, g in regs:
                g.set_opacity(0.0 if p is None else (1.0 if cond(p) else 0.0))

        img.add_updater(atualiza)
        for _, g in regs:
            g.set_opacity(0.0)
        self.add(img, *[g for _, g in regs])
        self.play(img.animate.set_opacity(1.0), FadeIn(titulo), FadeIn(leg), run_time=0.8)
        estado["t0"] = self.time
        self.wait(T.total / FPS)                              # a trajetória completa: intro, pausas e as passagens pelas fronteiras
        img.remove_updater(atualiza)
        self.play(FadeOut(VGroup(titulo, leg, *[g for _, g in regs])), img.animate.set_opacity(0.0), run_time=0.6)


class LinhaLimpo(CasoBase):
    CID = "linha"


class CascaCilLimpo(CasoBase):
    CID = "casca_cil"


class MacicoCilLimpo(CasoBase):
    CID = "macico_cil"


class FolhaLimpo(CasoBase):
    CID = "folha"


class PlacaLimpo(CasoBase):
    CID = "placa"


class DuasLimpo(CasoBase):
    CID = "duas"


class FaceLimpo(CasoBase):
    CID = "face"


class CascaEsfLimpo(CasoBase):
    CID = "casca_esf"


class MacicoEsfLimpo(CasoBase):
    CID = "macico_esf"


class CapEsfLimpo(CasoBase):
    CID = "cap_esf"
