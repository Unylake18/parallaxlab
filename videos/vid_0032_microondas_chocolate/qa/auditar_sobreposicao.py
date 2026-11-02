"""Portão de sobreposição do vid_0032 v2 (handoff v2 §9.2, adaptado do Anexo B).

Roda a cena a 270×480 / 5 fps e testa, quadro a quadro, a caixa de cada Text/MathTex visível (opacidade > 0,15, caixa
encolhida 0,02) contra: outro rótulo (caixa × caixa), objeto preenchido (caixa × caixa), traço (algum ponto da curva
dentro da caixa) e, quando o 3D aparece, as caixas projetadas de barra, prato, gotas e relevo (timeline.json → projecao_3d).
Exceções (G1): retângulo de fundo de tela inteira; painel do próprio rótulo (preenchido que contém o rótulo inteiro);
glifos que saem por cópia do próprio rótulo enquanto a cópia anda (registrados pela cena em self.isentos).
Uso (na raiz do repositório): uv run python videos/vid_0032_microondas_chocolate/qa/auditar_sobreposicao.py
Saída: qa/sobreposicao.json (eventos) e, no terminal, os intervalos por par (rótulo × objeto). Zero = aprovado.
"""
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

UNIT = Path(__file__).resolve().parents[1]
sys.argv = ['manim']
os.environ['MIDIA'] = 'media_audit'
sys.path.insert(0, str(UNIT))
from manim import *  # noqa: E402
from manim.renderer.cairo_renderer import CairoRenderer  # noqa: E402

config.pixel_width, config.pixel_height, config.frame_rate = 270, 480, 5
config.disable_caching = True
config.write_to_movie = False
import cena  # noqa: E402

EVENTOS = []
ROTULO = (Text, SingleStringMathTex)


def nome(m):
    if isinstance(m, Text):
        return 'T:' + m.text[:28]
    return 'M:' + getattr(m, 'tex_string', '')[:28]


def bbox(m, enc=0.):
    p = m.get_all_points()
    if len(p) == 0:
        return None
    lo, hi = p.min(0)[:2], p.max(0)[:2]
    return np.r_[lo + enc, hi - enc]


def inter(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def area(a):
    return (a[2] - a[0]) * (a[3] - a[1])


def contem(a, b):
    return a[0] <= b[0] and a[1] <= b[1] and a[2] >= b[2] and a[3] >= b[3]


def opac(s):
    return max(s.get_fill_opacity(), s.get_stroke_opacity())


def rotulos(scene):
    out = []
    for top in scene.mobjects:
        fam = top.get_family()
        for m in fam:
            if isinstance(m, ROTULO) and not any(isinstance(pp, ROTULO) and pp is not m and m in pp.get_family() for pp in fam):
                if any(opac(s) > .15 for s in m.family_members_with_points()):
                    out.append(m)
    return out


def auditar(scene, t):
    labs = rotulos(scene)
    ids_rot = {id(x) for m in labs for x in m.get_family()}
    isentos = [f for a, b, f in scene.isentos if a <= t <= b]
    fundo = getattr(scene, 'fundo', None)
    ve_3d = fundo is None or fundo not in scene.mobjects or fundo.get_fill_opacity() < .5
    cx3 = (cena.pj(t) or {}).get('caixas', {}) if ve_3d else {}
    for m in labs:
        b = bbox(m, .02)
        if b is None:
            continue
        famL = {id(x) for x in m.get_family()}
        fontes = [f for f in isentos if m in f.get_family()]
        for nome3, c in cx3.items():
            if inter(b, c):
                EVENTOS.append((round(t, 2), nome(m), '3D:' + nome3))
        for top in scene.mobjects:
            if isinstance(top, ImageMobject):
                bb = np.r_[top.get_corner(DL)[:2], top.get_corner(UR)[:2]]
                if inter(b, bb) and top.get_opacity() > .15 and top is not scene.cab[1]:
                    EVENTOS.append((round(t, 2), nome(m), 'imagem'))
                continue
            for s in top.family_members_with_points():
                if id(s) in famL or not isinstance(s, VMobject) or opac(s) < .15:
                    continue
                if s.width > 9 and s.height > 15:                       # fundo de tela inteira
                    continue
                if fontes and id(s) not in ids_rot:                      # cópia saindo do próprio rótulo
                    continue
                if id(s) in ids_rot:
                    bb = bbox(s, .02)
                    if bb is not None and inter(b, bb):
                        dono = next(x for x in labs if s in x.get_family())
                        if not any(dono in f.get_family() for f in isentos if m in f.get_family()):
                            EVENTOS.append((round(t, 2), nome(m), 'rótulo ' + nome(dono)))
                    continue
                pts = s.points[:, :2]
                if s.get_fill_opacity() > .15 and len(pts) > 3:
                    bb = bbox(s)
                    if contem(bb, b) and (getattr(s, 'es_painel', False) or area(bb) < 5 * area(b)):          # painel do próprio rótulo (painel() ou caixa justa); caixa de resultado × outro rótulo é testada
                        continue
                    if inter(b, bb):
                        EVENTOS.append((round(t, 2), nome(m), 'preenchido:' + type(s).__name__))
                        continue
                if s.get_stroke_opacity() > .15 and s.get_stroke_width() > .5:
                    dentro = (pts[:, 0] > b[0]) & (pts[:, 0] < b[2]) & (pts[:, 1] > b[1]) & (pts[:, 1] < b[3])
                    if dentro.any():
                        EVENTOS.append((round(t, 2), nome(m), 'traço:' + type(s).__name__))


orig = CairoRenderer.render


def render(self, scene, time, moving):
    auditar(scene, self.time)
    return orig(self, scene, time, moving)


CairoRenderer.render = render
sc = cena.Microondas032()
try:
    sc.render()
except Exception as e:
    print('ERRO', repr(e))
    raise
EVENTOS = sorted(set(EVENTOS))
(UNIT / 'qa' / 'sobreposicao.json').write_text(json.dumps(EVENTOS, ensure_ascii=False, indent=0), encoding='utf-8')
g = defaultdict(list)
for t, a, b in EVENTOS:
    g[(a, b)].append(t)
for (a, b), ts in sorted(g.items(), key=lambda kv: min(kv[1])):
    ts = sorted(set(ts))
    segs = [[ts[0], ts[0]]]
    for x in ts[1:]:
        if x - segs[-1][1] <= .45:
            segs[-1][1] = x
        else:
            segs.append([x, x])
    print(f'{a:34s} x {b:34s} {[(s, e) for s, e in segs][:6]}')
print(f'TOTAL: {len(g)} pares, {len(EVENTOS)} eventos (quadros a 5 fps)')
