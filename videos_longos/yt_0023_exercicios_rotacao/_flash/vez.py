"""vez(): agenda uma animação para daqui a `s0` s SEM deixar o destino na cena antes da hora (corrige o flash do TransformFromCopy dentro de
AnimationGroup/Succession: o Scene.begin_animations adiciona o mobject em estado final no instante 0)."""
from manim import *


def _dests(an_, saida):
    for b in getattr(an_, "animations", None) or []:
        _dests(b, saida)
    m = getattr(an_, "mobject", None)
    if m is not None and (an_.is_introducer() or isinstance(an_, TransformFromCopy)) and not isinstance(m, ValueTracker):
        saida.append(m)
    return saida


class Vez(Succession):
    def __init__(self, s0, an_, **kw):
        super().__init__(Wait(s0), an_, **kw)
        self._salvo = []
        vistos = set()
        for m in _dests(an_, []):
            for x in m.family_members_with_points():
                if id(x) in vistos or not isinstance(x, VMobject):
                    continue
                vistos.add(id(x))
                self._salvo.append((x, float(x.get_fill_opacity()), float(x.get_stroke_opacity())))
        self.oculta()

    def oculta(self):
        for x, fo, so in self._salvo:
            x.set_fill(opacity=0, family=False)
            x.set_stroke(opacity=0, family=False)

    def restaura(self):
        for x, fo, so in self._salvo:
            x.set_fill(opacity=fo, family=False)
            x.set_stroke(opacity=so, family=False)

    def update_active_animation(self, index):
        if index == 1:
            self.restaura()
        super().update_active_animation(index)
