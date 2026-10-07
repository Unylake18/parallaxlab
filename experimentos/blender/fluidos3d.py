"""Fluidos em 3D (5.6 e 5.7), fila B — estudo 23 (sandbox).

Hidrostática com empuxo, prensa hidráulica (Pascal) e jato de Torricelli. O líquido é vidro azul translúcido (com a superfície
livre em violeta tracejado); forças e velocidades = setas brancas; partículas marcadoras = neutras (degradê). fase 0 a 1 = um
ciclo. Valores, fórmulas e nomes dos vetores são do Manim.
"""

import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import gaussiana as ga  # noqa: E402
import oscilacoes as osc  # noqa: E402
import vetores3d as v3  # noqa: E402

VF = co.ST["materiais"]["vetor_fisico"]


def _mat_vf():
    return v3.material_cor("VetorFisico", VF["cor"], VF["emissao"])


def _mat_dash():
    return co._material("TracoFlu", {"cor": "gaussiana", "emissao": 1.8, "rugosidade": 0.4})


def _caixa(escala, local, nome="ProxyEnquadramento", oculto=True):
    o = osc._caixa(nome, escala, local)
    o.hide_render = oculto
    return o


def _arestas(x0, x1, y0, y1, z0, z1, mat, esp=0.014):
    for (a, b) in ((x0, y0), (x0, y1), (x1, y0), (x1, y1)):
        ga.criar_curva("Aresta", [([(a, b, z0), (a, b, z1)], False)], mat, esp)
    for z in (z0, z1):
        for (p, q) in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
            ga.criar_curva("Aresta", [([(p[0], p[1], z), (q[0], q[1], z)], False)], mat, esp)


def _liquido(escala, local, base=0.2):
    o = osc._caixa("Liquido", escala, local)
    cm.material_vidro(o, base=base, ganho=0.5, brilho_borda=1.4)
    return o


# ── tanque com empuxo ────────────────────────────────────────────────────────
def tanque_hidrostatico(largura=3.2, profundidade=2.2, altura_tanque=2.8, nivel=1.9, densidade_bloco=0.6, lado=0.95, setas=1,
                        movimento=0, fase=0.0):
    """Tanque de vidro com líquido até `nivel`, a superfície livre (violeta tracejado), um bloco flutuante (fração submersa =
    densidade do bloco / densidade do líquido) e as forças peso e empuxo (brancas). As setas horizontais na parede mostram a
    pressão aumentando com a profundidade. Com movimento o bloco oscila em torno do equilíbrio e o empuxo acompanha o volume
    submerso (Arquimedes)."""
    W, D, H = largura, profundidade, altura_tanque
    mat_vf, mat_d = _mat_vf(), _mat_dash()
    casco = osc._caixa("Tanque", (W, D, H), (0, 0, H / 2))
    cm.material_vidro(casco, base=0.04, ganho=0.15, brilho_borda=0.7)
    _arestas(-W / 2, W / 2, -D / 2, D / 2, 0.0, H, v3.material_cor("ArestaTanque", "fonte_contorno", 1.0))
    _liquido((W - 0.1, D - 0.1, nivel), (0, 0, nivel / 2))
    sup = [(-W / 2 + 0.05, -D / 2 + 0.05, nivel), (W / 2 - 0.05, -D / 2 + 0.05, nivel), (W / 2 - 0.05, D / 2 - 0.05, nivel), (-W / 2 + 0.05, D / 2 - 0.05, nivel)]
    ga.criar_curva("SuperficieLivre", v3.tracejado(sup, True, 0.22, 0.6), mat_d, 0.016)
    frac = min(max(densidade_bloco, 0.05), 0.95)
    bloco = osc._caixa("Bloco", (lado, lado, lado), (0, 0, 0))
    cm.material_vidro(bloco, cor="fonte_contorno", base=0.5, ganho=0.6, brilho_borda=2.0)
    arrows = []
    if setas:
        wall_x = -W / 2 + 0.08
        for d in (0.35 * nivel, 0.65 * nivel, 0.92 * nivel):
            z = nivel - d
            comp = 0.25 + 0.95 * d / nivel
            v3.seta((wall_x + comp, -D / 4, z), (-comp, 0, 0), mat_vf, comp)
    dinam = []

    def atualizar(fase):
        calado0 = frac * lado
        calado = calado0 + (0.16 * math.cos(2 * math.pi * fase) if movimento else 0.0)
        zc = nivel + lado / 2 - calado
        bloco.location = (0, 0, zc)
        v3.remover(dinam)
        if setas:
            P = 1.7
            E = P * calado / calado0
            dinam.append(v3.seta((0.0, 0.0, zc), (0, 0, -P), mat_vf, P))
            dinam.append(v3.seta((0.0, 0.0, zc), (0, 0, E), mat_vf, E))

    atualizar(fase)
    proxy = _caixa((W + 0.8, D + 0.8, H + 1.6), (0, 0, H / 2 + 0.4))
    return proxy, atualizar


# ── prensa hidráulica ────────────────────────────────────────────────────────
def prensa_hidraulica(raio1=0.45, raio2=1.1, altura=2.0, curso=0.55, escala_forca=0.32, movimento=0, fase=0.0):
    """Dois cilindros de vidro ligados por baixo, cheios de líquido, com êmbolos de áreas A1 = π r1² e A2 = π r2². Empurrar o êmbolo
    pequeno com F1 desce d1 e levanta o grande d2 = d1 A1/A2; F2 = F1 A2/A1 (setas brancas, a do êmbolo grande desenhada na
    escala `escala_forca`). fase 0 a 1 = um ciclo (desce e sobe)."""
    x1, x2 = -(raio2 + 0.6), (raio1 + 0.6)
    z0, h0 = 0.35, altura
    mat_vf = _mat_vf()
    bpy.ops.mesh.primitive_cylinder_add(radius=raio1 + 0.05, depth=1.0, vertices=48, location=(x1, 0, 0.5))
    c1 = bpy.context.active_object
    c1.name = "Casco1"
    cm.material_vidro(c1, base=0.05, ganho=0.2, brilho_borda=0.9)
    c1.scale = (1, 1, z0 + h0 + 0.4)
    c1.location = (x1, 0, (z0 + h0 + 0.4) / 2)
    bpy.ops.mesh.primitive_cylinder_add(radius=raio2 + 0.05, depth=1.0, vertices=64, location=(x2, 0, 0.5))
    c2 = bpy.context.active_object
    c2.name = "Casco2"
    cm.material_vidro(c2, base=0.05, ganho=0.2, brilho_borda=0.9)
    c2.scale = (1, 1, z0 + h0 + 0.4)
    c2.location = (x2, 0, (z0 + h0 + 0.4) / 2)
    liga = osc._caixa("Ligacao", (x2 - x1, 0.7, 0.45), ((x1 + x2) / 2, 0, 0.22))
    cm.material_vidro(liga, base=0.18, ganho=0.5, brilho_borda=1.4)
    fl = []
    for (x, r) in ((x1, raio1), (x2, raio2)):
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=1.0, vertices=48, location=(x, 0, 0.5))
        f = bpy.context.active_object
        f.name = "Fluido"
        cm.material_vidro(f, base=0.22, ganho=0.5, brilho_borda=1.4)
        fl.append(f)
    pist = []
    mat_p = co._material("Embolo", {"cor": "fonte_contorno", "emissao": 1.0, "rugosidade": 0.3})
    for (x, r) in ((x1, raio1), (x2, raio2)):
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=0.14, vertices=48)
        pp = bpy.context.active_object
        pp.name = "Embolo"
        pp.data.materials.append(mat_p)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.7, vertices=16)
        hh = bpy.context.active_object
        hh.name = "Haste"
        hh.data.materials.append(mat_p)
        pist.append((pp, hh))
    d_ratio = (raio1 / raio2) ** 2
    dinam = []

    def atualizar(fase):
        s = 0.5 - 0.5 * math.cos(2 * math.pi * fase) if movimento else 0.0
        d1 = curso * s
        d2 = d1 * d_ratio
        n1, n2 = h0 - d1, h0 + d2
        for f, (x, n) in zip(fl, ((x1, n1), (x2, n2))):
            f.scale = (1, 1, z0 + n)
            f.location = (x, 0, (z0 + n) / 2)
        for (pp, hh), (x, n) in zip(pist, ((x1, n1), (x2, n2))):
            pp.location = (x, 0, z0 + n + 0.07)
            hh.location = (x, 0, z0 + n + 0.07 + 0.42)
        v3.remover(dinam)
        F1 = 1.0
        F2 = F1 / d_ratio * escala_forca
        dinam.append(v3.seta((x1, 0, z0 + n1 + 0.95 + F1), (0, 0, -F1), mat_vf, F1))
        dinam.append(v3.seta((x2, 0, z0 + n2 + 0.95), (0, 0, F2), mat_vf, F2))

    atualizar(fase)
    proxy = _caixa((x2 - x1 + 2 * raio2 + 1.0, 2 * raio2 + 0.8, z0 + h0 + 3.2), ((x1 + x2) / 2, 0, (z0 + h0 + 2.2) / 2))
    return proxy, atualizar


# ── jato de Torricelli ───────────────────────────────────────────────────────
def tanque_torricelli(largura=2.4, nivel=2.2, altura_furo=0.7, n_particulas=26, setas=1, movimento=0, fase=0.0,
                      varrer_furo=0, enquadramento_fixo=0, faixa_min=0.1, faixa_max=0.9):
    """Tanque com líquido até `nivel` (H) e um furo a `altura_furo` (y) do fundo: o jato sai com v = √(2 g h), h = H − y
    (g = 1 nas unidades do sólido) e descreve uma parábola (violeta tracejado) até o chão; o alcance a partir da parede é
    2√(y (H − y)), máximo em y = H/2. Partículas marcadoras percorrem o jato continuamente. fase 0 a 1 = um ciclo de emissão.

    Opt-in (o padrão é o comportamento original):
    - `varrer_furo=1` (com movimento=1): y varia em loop suave de `faixa_min`·H a `faixa_max`·H e volta (y = H(c − a cos 2π fase)); o
      furo, a seta, a cota de altura e a parábola são recalculados a cada quadro; o quadro inicial e o final coincidem.
    - `enquadramento_fixo=1`: enquadra pelo alcance máximo teórico (x_max = H, em y = H/2), então a escala da câmera e o chão não
      mudam com `altura_furo`. A varredura liga isto automaticamente (senão a câmera, feita uma vez, cortaria o jato)."""
    W, D, H = largura, 1.4, nivel + 0.6
    fixo = bool(enquadramento_fixo or (varrer_furo and movimento))
    ref = nivel if fixo else math.sqrt(2 * (nivel - altura_furo)) * math.sqrt(2 * altura_furo)   # alcance que dimensiona chão e câmera
    mat_vf, mat_d = _mat_vf(), _mat_dash()
    casco = osc._caixa("Tanque", (W, D, H), (0, 0, H / 2))
    cm.material_vidro(casco, base=0.04, ganho=0.15, brilho_borda=0.7)
    _arestas(-W / 2, W / 2, -D / 2, D / 2, 0.0, H, v3.material_cor("ArestaTanque", "fonte_contorno", 1.0))
    _liquido((W - 0.1, D - 0.1, nivel), (0, 0, nivel / 2))
    chao = osc._caixa("Chao", (W + ref + 1.6, D + 0.6, 0.05), ((ref + 1.0) / 2 - 0.0, 0, -0.025))
    cm.material_vidro(chao, base=0.06, ganho=0.2, brilho_borda=0.6)
    sup = [(-W / 2, -D / 2, nivel), (W / 2, -D / 2, nivel), (W / 2, D / 2, nivel), (-W / 2, D / 2, nivel)]
    ga.criar_curva("SuperficieLivre", v3.tracejado(sup, True, 0.22, 0.6), mat_d, 0.016)
    xf = W / 2
    mat_b = v3.material_degrade("Particula", "texto_neutro", "fonte_contorno", 1.0, 0.7)
    part = [v3.esfera_pt((xf, 0, altura_furo), 0.075, mat_b, "Particula") for _ in range(int(n_particulas))]
    mat_furo = v3.material_cor("Furo", "texto_neutro", 1.6)
    dinam = []
    estado = {}

    def montar(y):
        """Tudo o que depende de y: parábola, furo, cota de altura e seta da velocidade."""
        v3.remover(dinam)
        h = nivel - y
        v, T = math.sqrt(2 * h), math.sqrt(2 * y)
        estado.update(y=y, v=v, T=T)
        traj = [(xf + v * (T * k / 60), 0.0, y - 0.5 * (T * k / 60) ** 2) for k in range(61)]
        dinam.append(ga.criar_curva("Parabola", v3.tracejado(traj, False, 0.18, 0.6), mat_d, 0.014))
        dinam.append(ga.criar_curva("Furo", ga.circulo((xf, 0, y), (0, 1, 0), (0, 0, 1), 0.06, True), mat_furo, 0.02))
        dinam.append(ga.criar_curva("Altura", v3.tracejado([(xf + 0.25, 0, nivel), (xf + 0.25, 0, y)], False, 0.14, 0.6), mat_d, 0.012))
        if setas:
            dinam.append(v3.seta((xf + 0.02, 0, y), (0.4 * v + 0.2, 0, 0), mat_vf, 0.4 * v + 0.2))

    def altura_em(fase):
        c, a = nivel * (faixa_max + faixa_min) / 2, nivel * (faixa_max - faixa_min) / 2
        return c - a * math.cos(2 * math.pi * fase)

    def atualizar(fase):
        if varrer_furo and movimento:
            montar(altura_em(fase))
        v, T, y = estado["v"], estado["T"], estado["y"]
        for k, o in enumerate(part):
            tau = (((k / len(part)) + fase) % 1.0) * T
            o.location = (xf + v * tau, 0.0, y - 0.5 * tau * tau)

    montar(altura_em(fase) if (varrer_furo and movimento) else altura_furo)
    atualizar(fase)
    proxy = _caixa((W + ref + 1.6, D + 0.8, H + 0.8), ((ref) / 2, 0, H / 2 - 0.1))
    return proxy, atualizar


def cena_preview():
    co.limpar_cena()
    proxy, _ = tanque_hidrostatico()
    co.mundo()
    co.luzes()
    co.camera_enquadrada(co.cantos([proxy]), azimute=-65, elevacao=16, margem=0.08)
    co.render(co.OUT / "fluidos3d_v1.png")


if __name__ == "__main__":
    cena_preview()
