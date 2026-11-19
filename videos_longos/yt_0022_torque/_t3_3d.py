"""Aplica o mapeamento 3D (Three.js 'disco') ao sec_t3.py: toda geometria no plano do disco passa por MP() (projeção exata da câmera)."""
from pathlib import Path

p = Path(__file__).resolve().parent / "sec_t3.py"
s = p.read_text(encoding="utf-8")


def sub(a, b):
    global s
    if a not in s:
        print("NÃO ACHEI:", a[:80])
        return
    s = s.replace(a, b, 1)


sub("        PARK = 0.35\n", '''        PARK = 0.35

        # Three.js 'disco': câmera oblíqua (el 52°) sobre o disco de raio 1; MP leva um ponto do plano 2D do disco à tela (mesma câmera do b3d.js)
        cam3 = cam_obl(az=-90.0, el=52.0, alvo=(0.0, 0.0, 0.0), K=R_D3, xc=float(C_D3[0]), yc=float(C_D3[1]), fov=14)

        def MP(p):
            q = projeta3d(cam3, ((p[0] - C_D3[0]) / R_D3, (p[1] - C_D3[1]) / R_D3, 0.0))
            return P3(float(q[0]), float(q[1]), 0.0)

        def est3(t):
            return r4({"th": round(float(fi()), 5), "cam": cam3})

        f3 = Fundo3D(self, "disco", est3)
        self.add(f3)
        self.f3 = f3
''')
sub("            g = DiscoPedacos(C_D3, R_D3, NR3, NT3)\n            g.rotate(fi(), about_point=C_D3)\n", "            g = DiscoPedacos(C_D3, R_D3, NR3, NT3)\n            g.rotate(fi(), about_point=C_D3)\n            g.remove(g.corpo)                      # o corpo (espessura, aro, sombra) é o Three.js\n")
sub("            vp = varre_pares.get_value()\n", "            g.apply_function(MP)\n            vp = varre_pares.get_value()\n")
sub("                        pa, pb = pos(ka), pos(kb)\n", "                        pa, pb = MP(pos(ka)), MP(pos(kb))\n")
sub("        a_alp = seta_curva(C_D3, R_D3 + 0.36, 1.85, 0.85, ACC, 6)\n", "        a_alp = seta_curva(C_D3, R_D3 + 0.36, 1.85, 0.85, ACC, 6).apply_function(MP)\n")
sub(".next_to(C_D3 + (R_D3 + 0.36) * np.array([math.cos(2.3), math.sin(2.3), 0.0]), UL, buff=0.26)", ".next_to(MP(C_D3 + (R_D3 + 0.36) * np.array([math.cos(2.3), math.sin(2.3), 0.0])), UL, buff=0.26)")
sub("lin_ri = DashedLine(C_D3, p_i, dash_length=0.08)", "lin_ri = DashedLine(C_D3, MP(p_i), dash_length=0.08)")
sub("l_mi = T(\"m_i\", 40, MAS).move_to(p_i + u_rad * 0.56 + DOWN * 0.24)", "l_mi = T(\"m_i\", 40, MAS).move_to(MP(p_i + u_rad * 0.9))")
sub("l_ri = T(\"r_i\", 40, GEO).move_to((C_D3 + p_i) / 2 + u_tan * 0.36)", "l_ri = T(\"r_i\", 40, GEO).move_to(MP((C_D3 + p_i) / 2 + u_tan * 0.45))")
sub("s_at = seta(p_i, p_i + u_tan * 1.15, ACC, 5, tip=0.18)", "s_at = seta(MP(p_i), MP(p_i + u_tan * 1.15), ACC, 5, tip=0.18)")
sub("l_at = T(\"a_{t,i}\", 38, ACC).next_to(p_i + u_tan * 1.15, UP, buff=0.14)", "l_at = T(\"a_{t,i}\", 38, ACC).next_to(MP(p_i + u_tan * 1.15), UP, buff=0.14)")
sub("s_fr = seta(p_i, p_i - u_rad * 0.85, GEO, 4, tip=0.16, op=0.65)", "s_fr = seta(MP(p_i), MP(p_i - u_rad * 0.85), GEO, 4, tip=0.16, op=0.65)")
sub("l_fr = T(\"F_{r,i}\", 40, GEO).next_to(s_fr, DOWN, buff=0.08)", "l_fr = T(\"F_{r,i}\", 40, GEO).next_to(s_fr, DOWN, buff=0.3)")
sub("s_ft = seta(p_i, p_i + u_tan * 1.35, FC, 6, tip=0.20)", "s_ft = seta(MP(p_i), MP(p_i + u_tan * 1.35), FC, 6, tip=0.20)")
sub("l_ft = T(\"F_{t,i}\", 40, FC).next_to(p_i + u_tan * 1.35, UR, buff=0.08)", "l_ft = T(\"F_{t,i}\", 40, FC).next_to(MP(p_i + u_tan * 1.35), UR, buff=0.2)")
sub("lin_ab = DashedLine(pa - u_ab * 0.9, pb + u_ab * 0.9, dash_length=0.08)", "lin_ab = DashedLine(MP(pa - u_ab * 0.9), MP(pb + u_ab * 0.9), dash_length=0.08)")
sub("seg_rp = Line(C_D3, p_proj)", "seg_rp = Line(C_D3, MP(p_proj))")
sub("l_rp = T(r\"r_\\perp\", 36, GEO).move_to((C_D3 + p_proj) / 2 + P3(-0.32, -0.22))", "l_rp = T(r\"r_\\perp\", 40, GEO).move_to(MP((C_D3 + p_proj) / 2) + P3(-0.45, -0.3))")
sub("s_fab = seta(pa, pa + u_ab * 0.78, FC, 5.5, tip=0.18, z=16)", "s_fab = seta(MP(pa), MP(pa + u_ab * 0.78), FC, 5.5, tip=0.18, z=16)")
sub("s_fba = seta(pb, pb - u_ab * 0.78, FC, 5.5, tip=0.18, z=16)", "s_fba = seta(MP(pb), MP(pb - u_ab * 0.78), FC, 5.5, tip=0.18, z=16)")
sub("l_fab = T(r\"\\vec F_{AB}\", 40, FC).next_to(pa, UL, buff=0.08)", "l_fab = T(r\"\\vec F_{AB}\", 40, FC).next_to(MP(pa), UL, buff=0.3)")
sub("l_fba = T(r\"\\vec F_{BA}\", 40, FC).next_to(pb, UR, buff=0.08)", "l_fba = T(r\"\\vec F_{BA}\", 40, FC).next_to(MP(pb), UR, buff=0.3)")
sub("        self.play(\n            FadeOut(VGroup(dv, a_alp, l_alp, Eb, cab, *[lt for lt, _ in linhas_tab])),\n            run_time=0.45,\n        )", "        self.play(\n            f3.op.animate.set_value(0.0),\n            FadeOut(VGroup(dv, a_alp, l_alp, Eb, cab, *[lt for lt, _ in linhas_tab])),\n            run_time=0.45,\n        )")
p.write_text(s, encoding="utf-8")
