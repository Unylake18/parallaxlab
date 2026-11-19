def patch(p, pares):
    s = open(p, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (p, a[:60], s.count(a))
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s)


# ── k39: câmeras, pontos e as duas funções do B3 ─────────────────────────────────────────────────────────────────────────
patch('k39.py', [
    ('''def pontos39(cena, e):
    sm_ =''', '''def pontos39(cena, e):
    if cena == "massa":
        return {"ex": (1.12, 0, 0), "ey": (0, .78, 0)} if e.get("forma", "elipse") == "elipse" else {"ex": (2.4, 0, 0), "ey": (0, 2.45, 0)}
    sm_ ='''),
    ('''def tira_presos(sc, rt=0.3):''', '''def cam_incl(tgt, d, el=32, az=-35, cx=960, cy=560, fov=22):
    e, a = math.radians(el), math.radians(az)
    pos = [tgt[0] + d * math.cos(e) * math.sin(a), tgt[1] - d * math.cos(e) * math.cos(a), tgt[2] + d * math.sin(e)]
    return cam_dict(pos, tgt, (0, 0, 1), cx, cy, fov)


CAM_M43 = cam_incl((0, .25, .3), 6.6, cx=560, cy=620)           # B3: meia elipse ρ = k y (aprovado nos stills)
CAM_M54 = cam_incl((0, .9, .35), 13.5, cx=540, cy=620)          # B3: meia arruela ρ = k r


def massa_entra(sc, forma, cam, k1, cx1, cy1, esconde, lx2, ly2, H=None, rt=1.5):
    """B3 (massa como volume): no mesmo quadro o 2D sai e entra a cena 3D `massa` vista de cima ortográfica (alt = 0, idêntica ao 2D);
    em `rt` s a câmera inclina e a chapa ganha a altura ρ. Os rótulos x e y ficam presos às pontas dos eixos 3D."""
    ini = {"forma": forma, "alt": 0.0}
    if H:
        ini["H"] = float(H)
    pal = Palco37(sc, "massa", cam, **ini)
    pal.fundo.set_z_index(-5)
    pal.sobe(k1, cx1, cy1)
    pal.tr["s"].set_value(1.0)
    sc.add(pal.fundo)
    qx, qy = pal.pt("ex"), pal.pt("ey")
    lx3 = pal.prende(TC(r"\\X", 0, 0, 32, "c"), "ex", pxof(lx2.get_center())[0] - qx[0], pxof(lx2.get_center())[1] - qx[1])
    ly3 = pal.prende(TC(r"\\Y", 0, 0, 32, "c"), "ey", pxof(ly2.get_center())[0] - qy[0], pxof(ly2.get_center())[1] - qy[1])
    pronto(lx3, ly3)
    sc.remove(*[m for m in esconde if m in sc.mobjects], lx2, ly2)
    sc.add(lx3, ly3)
    print(f"[pouso3d] {sc.lote} {sc._aid} massa/{forma} entrada quadro {sc.nq} (2D → 3D, vista de cima)")
    sc.play(*pal.anim(rt, s=0.0), *pal.anim(rt, alt=1.0), run_time=rt)
    return pal, lx3, ly3


def massa_volta(sc, pal, entram, lx3, ly3, lx2, ly2, rt=2.0):
    """B3: a câmera volta à vista de cima ortográfica e a chapa desce a alt = 0; no último quadro o PNG 3D sai e o 2D entra por cima."""
    sc.play(*pal.anim(rt, s=1.0), *pal.anim(rt, alt=0.0), run_time=rt)
    print(f"[pouso3d] {sc.lote} {sc._aid} massa pouso quadro {sc.nq} (3D → 2D, vista de cima)")
    for m in (lx3, ly3):
        m.clear_updaters()
    sc.remove(lx3, ly3)
    troca_para_2d(sc, pal, list(entram) + [lx2, ly2])


def tira_presos(sc, rt=0.3):'''),
])

# ── E4-3 ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────
s = open('sec_e4.py', encoding='utf-8').read()
a0 = s.index('        # v2 B2 · a cunha que varre')
a1 = s.index('        self.gat("seno ao quadrado a gente não integra")')
s = s[:a0] + s[a1:]
open('sec_e4.py', 'w', encoding='utf-8').write(s)
patch('sec_e4.py', [
    ('        self.gat("o momento em relação ao eixo")\n',
     '''        self.gat("o momento em relação ao eixo")
        hide43 = [mp, bd, sx, sy] + [x for t in tks for x in t] + list(t5)
        pal43, lx43, ly43 = massa_entra(self, "elipse", CAM_M43, 470, 545, 900, hide43, lx, ly, H=.8)
'''),
    ('        self.gat("é momento sobre massa")\n',
     '''        self.gat("é momento sobre massa")
        massa_volta(self, pal43, [mp, bd, sx, sy] + [x for t in tks for x in t] + list(t5), lx43, ly43, lx, ly)
'''),
])

# ── E5-4 ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────
s = open('sec_e5.py', encoding='utf-8').read()
a0 = s.index('        mp = meia_lua_mapa(v, 1, 2, lambda r: r, 2.0, z=2)\n        self.play(FadeIn(mp), run_time=1.0)\n        lr = rot_m(v, r"\\rr=\\kk\\,r"')
a1 = s.index('        M3 = linha(self, [("m", r"\\mm")')
novo = '''        mp = meia_lua_mapa(v, 1, 2, lambda r: r, 2.0, z=2)
        h54 = [ar, fora, dentro, base, P["sx"], P["sy"]] + [x for t in P["tk"] for x in t]
        pal54, lx54, ly54 = massa_entra(self, "arruela", CAM_M54, 210, 520, 860, h54, P["lx"], P["ly"])
        lr = rot_m(v, r"\\rr=\\kk\\,r", (-2.2, 2.62), 0, 0, 30, "l")
        lp = leg("MAIS PESADA LONGE DO CENTRO", *v.px(-2.2, 2.38), CI, "left", 26)
        self.pena(lr, lp, lag=0.1)
        self.gat("Pensa numa roda de bicicleta")
'''
s = s[:a0] + novo + s[a1:]
open('sec_e5.py', 'w', encoding='utf-8').write(s)
patch('sec_e5.py', [
    ('        tira_chips(self)\n        limpa_col(self)\n        h1 = leg("HOMOGÊNEA"',
     '        massa_volta(self, pal54, [mp, ar, fora, dentro, base, P["sx"], P["sy"]] + [x for t in P["tk"] for x in t], lx54, ly54, P["lx"], P["ly"])\n        tira_chips(self)\n        limpa_col(self)\n        h1 = leg("HOMOGÊNEA"'),
])
print('ok')
