p = 'prob2.py'
s = open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in s else '\n'
s = s.replace('\r\n', '\n')
i = s.index('class CanetaIntro(Write):')
j = s.index('def troca_anim(')
novo = '''CANETA_TRACO_PREVIEW, CANETA_PONTA_PREVIEW = 2.3, 0.032      # ≈ 1,5 px e ponta de 4 px a 960×540 (v5 §3.1b)
CANETA_TRACO_FINAL, CANETA_PONTA_FINAL = 0.75, 0.011         # ≈ 1 px e ponta de 3 px a 1080p (finíssimo da tabela §3.4b)


class CanetaAnim(Animation):
    """Caneta (regra permanente 2026-11-08): cada glifo é traçado pelo contorno finíssimo, um depois do outro (esquerda → direita), com uma
    ponta branca na ponta do traço; ao fechar o contorno o glifo preenche na cor do token SEM contorno por cima. Antes da sua vez o glifo
    não tem tinta nenhuma (nem fill nem stroke)."""
    introducer = True

    def __init__(self, mob, run_time=0.6, **kw):
        kw.pop("shift", None)
        kw.pop("stroke_width", None)
        kw.pop("lag_ratio", None)
        super().__init__(mob, run_time=run_time, **kw)
        pre = config.pixel_height < 1080
        self._w = CANETA_TRACO_PREVIEW if pre else CANETA_TRACO_FINAL
        self._rp = CANETA_PONTA_PREVIEW if pre else CANETA_PONTA_FINAL
        gl = [g for g in mob.family_members_with_points() if isinstance(g, VMobject)]
        gl.sort(key=lambda g: g.get_left()[0])
        self._gl = gl
        self._ori = [(g, g.copy(), float(g.get_fill_opacity()), g.get_fill_color(), float(g.get_stroke_opacity())) for g in gl]
        self._tip = None
        self._cena = None

    def _setup_scene(self, scene):
        super()._setup_scene(scene)
        self._cena = scene

    def begin(self):
        super().begin()
        self._tip = VGroup(Dot(radius=self._rp * 1.9, color="#050B18"), Dot(radius=self._rp, color="#FFFFFF")).set_z_index(40)
        self._tip.set_opacity(0)
        if self._cena is not None:
            self._cena.add(self._tip)

    def interpolate_mobject(self, alpha):
        n = max(1, len(self._ori))
        dur = min(1.0, 0.6 / max(self.run_time, 1e-6)) if n == 1 else min(1.0, 0.6 / max(self.run_time, 1e-6))
        dur = max(dur, 1.0 / n) if n > 1 else 1.0
        passo = 0.0 if n == 1 else (1.0 - dur) / (n - 1)
        ponta = None
        for k, (g, o, fo, fc, so) in enumerate(self._ori):
            a = (alpha - k * passo) / dur
            if a <= 0:
                g.set_fill(opacity=0, family=False)
                g.set_stroke(opacity=0, family=False)
            elif a >= 1:
                g.pointwise_become_partial(o, 0, 1)
                g.set_fill(fc, opacity=fo, family=False)
                g.set_stroke(width=0, opacity=0, family=False)
            else:
                tr = min(1.0, a / 0.7)
                g.pointwise_become_partial(o, 0, max(1e-3, tr))
                g.set_stroke(color=fc, width=self._w, opacity=1.0, family=False)
                g.set_fill(fc, opacity=fo * max(0.0, (a - 0.7) / 0.3), family=False)
                if a < 0.95:
                    ponta = o.point_from_proportion(tr)
        if self._tip is not None:
            if ponta is None:
                self._tip.set_opacity(0)
            else:
                self._tip.move_to(ponta).set_opacity(1)

    def clean_up_from_scene(self, scene):
        if self._tip is not None:
            scene.remove(self._tip)
            self._tip = None
        super().clean_up_from_scene(scene)


def CanetaIntro(mob, **kw):
    """Introdutor do glyph map (`default_introducer`): o termo NOVO do passo é escrito pela caneta em vez de aparecer por FadeIn."""
    return CanetaAnim(mob, **kw)


def Caneta(g, rt=None):
    n = len([x for x in g.family_members_with_points() if isinstance(x, VMobject)])
    return CanetaAnim(g, run_time=rt if rt is not None else 0.3 * max(0, n - 1) + 0.6)


'''
s = s[:i] + novo + s[j:]
# voa: o termo fixo usa a duração da própria caneta
s = s.replace('f_ = Caneta(g_, 0.4)', 'f_ = Caneta(g_)')
s = s.replace('starts.append(L - (d if tp == "voo" else 0.4))', 'starts.append(L - (d if tp == "voo" else float(an_.run_time)))')
s = s.replace('dur = d if tp == "voo" else 0.4', 'dur = d if tp == "voo" else float(an_.run_time)')
s = s.replace('pous_ = [(t[0], t[1], s0_ + sh + (d if t[2] == "voo" else 0.4)) for t, s0_ in zip(itens, starts)]', 'pous_ = [(t[0], t[1], s0_ + sh + (d if t[2] == "voo" else float(t[3].run_time))) for t, s0_ in zip(itens, starts)]')
open(p, 'w', encoding='utf-8', newline='').write(s.replace('\n', nl))
print('ok')
