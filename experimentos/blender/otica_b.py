"""Óptica e física moderna, fila B (7.2 a 7.6, 7.11) — estudo 25 (sandbox).

Espelho esférico, dioptro plano (Snell e reflexão interna total), filme fino, interferômetro de Michelson, rede de difração,
polarizadores (lei de Malus), relógio de luz e átomo de Bohr. Raios de luz = branco fino (neutro); campo E = ciano; objetos
transparentes = vidro azul-claro; construções = violeta tracejado. fase 0 a 1 = um ciclo (loop) ou, nos de ciclo único, do começo
ao fim. Valores, fórmulas e rótulos (n1, n2, θ, λ, ...) são do Manim.
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
import revolucao as rv  # noqa: E402
import vetores3d as v3  # noqa: E402

OT = co.ST["materiais"]["otica"]


def _mat_raio():
    return v3.material_cor("RaioLuz", "texto_neutro", 2.0)


def _mat_raio_fraco():
    return v3.material_cor("RaioFraco", "texto_neutro", 0.8)


def _mat_dash():
    return co._material("TracoOB", {"cor": "gaussiana", "emissao": 1.8, "rugosidade": 0.4})


def _mat_eixo():
    return v3.material_cor("EixoOB", "texto_neutro", 0.8)


def _caixa(escala, local):
    o = osc._caixa("ProxyEnquadramento", escala, local)
    o.hide_render = True
    return o


def _movel(nome, escala, local):
    """Caixa cuja posição é `location` (sem deslocamento gravado nos vértices): serve para peças que atualizar() move."""
    o = osc._caixa(nome, escala, (0, 0, 0))
    o.location = local
    return o


def _vidro(o, base=None):
    cm.material_vidro(o, cor=OT["vidro_cor"], base=OT["vidro_base"] if base is None else base, ganho=OT["vidro_ganho"], brilho_borda=OT["vidro_brilho"])


def _raio(nome, mat, esp=0.022):
    obj, sp = osc.curva_viva(nome, 2, mat, esp)
    return sp


def _def_raio(sp, a, b):
    osc.pontos_curva(sp, [a, b])


# ── espelho esférico ─────────────────────────────────────────────────────────
def espelho_esferico(tipo="concavo", raio_curvatura=3.0, diametro=2.6, marcas=1, eixo=1):
    """Calota esférica (espelho côncavo ou convexo) de revolução em torno do eixo X, com a face refletora voltada para +X.
    Marcas neutras: vértice V, foco F = R/2 e centro de curvatura C = R (para o convexo, atrás do espelho: virtuais). Eixo
    óptico tracejado."""
    R, h = raio_curvatura, diametro / 2
    s = 1.0 if tipo == "concavo" else -1.0
    sag = lambda r: R - math.sqrt(R * R - r * r)
    NP = 60
    rs = [h * i / NP for i in range(NP + 1)]
    frente = [(s * sag(r), r) for r in rs]
    tras = [(s * sag(r) - 0.14, r) for r in reversed(rs)]
    corpo = rv.malha_revolucao("Espelho", frente + tras, "X")
    cm.material_vidro(corpo, cor=OT["vidro_cor"], base=0.55, ganho=0.6, brilho_borda=2.2)
    if eixo:
        ga.criar_curva("EixoOptico", v3.tracejado([(-1.2 - R, 0, 0), (R + 1.4, 0, 0)], False, 0.24, 0.6), _mat_eixo(), 0.011)
    if marcas:
        mat = v3.material_cor("MarcaEsp", "texto_neutro", 2.2)
        for x in (0.0, s * R / 2, s * R):
            v3.esfera_pt((x, 0, 0), 0.07, mat, "Marca")
    proxy = _caixa((2 * R + 2.0, diametro + 0.8, diametro + 0.8), (s * R / 2, 0, 0))
    return proxy


# ── dioptro plano: Snell e reflexão interna total ────────────────────────────
def dioptro_plano(n1=1.0, n2=1.5, angulo_graus=40.0, sentido="ar_vidro", movimento=0, fase=0.0, comprimento_raio=2.3):
    """Interface plana entre dois meios (o vidro é a placa de vidro azul-claro) com a normal tracejada e três raios brancos:
    incidente, refletido (mais fraco) e refratado (Snell: n1 sen θ1 = n2 sen θ2); se sen θ2 > 1 só há o refletido (reflexão
    interna total). `sentido`: ar_vidro (o raio vem do ar) ou vidro_ar (vem do vidro). Com movimento θ1 varre de 5° a 85° e volta."""
    if sentido == "vidro_ar":
        n1, n2 = max(n1, n2), min(n1, n2)
    else:
        n1, n2 = min(n1, n2), max(n1, n2)
    L = comprimento_raio
    esp = 2.4
    zs = (-esp, 0.0) if sentido == "ar_vidro" else (0.0, esp)
    placa = osc._caixa("Vidro", (4.2, 2.6, esp), (0, 0, (zs[0] + zs[1]) / 2))
    _vidro(placa, base=0.12)
    ga.criar_curva("Normal", v3.tracejado([(0, 0, -L - 0.2), (0, 0, L + 0.2)], False, 0.2, 0.6), _mat_eixo(), 0.011)
    inc, ref, rfr = _raio("Incidente", _mat_raio()), _raio("Refletido", _mat_raio_fraco(), 0.016), _raio("Refratado", _mat_raio())
    sinal_inc = 1.0                                                  # o meio de incidência fica sempre em z > 0 (o vidro vai para z > 0 em vidro_ar)
    def montar(th):
        s = math.sin(th)
        d = sinal_inc
        _def_raio(inc, (-L * s, 0, d * L * math.cos(th)), (0, 0, 0))
        _def_raio(ref, (0, 0, 0), (L * s, 0, d * L * math.cos(th)))
        st = n1 * s / n2
        if st < 1.0:
            tt = math.asin(st)
            _def_raio(rfr, (0, 0, 0), (L * math.sin(tt), 0, -d * L * math.cos(tt)))
        else:
            _def_raio(rfr, (0, 0, -90), (0, 0, -90.001))

    def atualizar(fase):
        montar(math.radians(45 + 40 * math.sin(2 * math.pi * fase)) if movimento else math.radians(angulo_graus))

    atualizar(fase)
    proxy = _caixa((4.4, 3.0, 2 * L + 0.8), (0, 0, 0))
    return proxy, atualizar


# ── filme fino ───────────────────────────────────────────────────────────────
def filme_fino(n_filme=1.4, espessura=0.55, angulo_graus=28.0, movimento=0, fase=0.0, amplitude=0.45):
    """Película de vidro (n > 1) sobre um substrato: um raio incidente se divide num refletido na face de cima e noutro que
    atravessa o filme, reflete na de baixo e sai (dois raios finos). A esfera no alto indica o brilho da interferência
    cos²(2π · 2 n t cos θ₂ / λ): com movimento a espessura varia e o brilho vai e volta (construtiva/destrutiva)."""
    th = math.radians(angulo_graus)
    tt = math.asin(math.sin(th) / n_filme)
    sub = _movel("Substrato", (5.0, 2.6, 0.5), (0, 0, -0.25 - 0.8))
    cm.material_vidro(sub, base=0.25, ganho=0.5, brilho_borda=1.4)
    filme = _movel("Filme", (5.0, 2.6, 1.0), (0, 0, -0.5))
    _vidro(filme, base=0.18)
    inc, r1, r2, interno1, interno2 = (_raio(n, _mat_raio(), 0.02) for n in ("Incidente", "Refl1", "Refl2", "Interno1", "Interno2"))
    mat_b = v3.material_degrade("Brilho", "texto_neutro", "fonte_contorno", 0.0001, 0.6)
    brilho = v3.esfera_pt((2.0, 0, 1.9), 0.2, mat_b, "Brilho")
    nodo = mat_b.node_tree.nodes["Principled BSDF"]
    L = 1.7

    def atualizar(fase):
        t = espessura * (1.0 + (amplitude * math.sin(2 * math.pi * fase) if movimento else 0.0))
        filme.scale = (1, 1, t)
        filme.location = (0, 0, -t / 2)
        sub.location = (0, 0, -t - 0.25)
        dx = 2 * t * math.tan(tt)                                # deslocamento horizontal entre os dois pontos de reflexão
        _def_raio(inc, (-L * math.sin(th), 0, L * math.cos(th)), (0, 0, 0))
        _def_raio(r1, (0, 0, 0), (L * math.sin(th), 0, L * math.cos(th)))
        _def_raio(interno1, (0, 0, 0), (dx / 2, 0, -t))
        _def_raio(interno2, (dx / 2, 0, -t), (dx, 0, 0))
        _def_raio(r2, (dx, 0, 0), (dx + L * math.sin(th), 0, L * math.cos(th)))
        fase_opt = 2 * math.pi * 2 * n_filme * t * math.cos(tt) / 0.62                 # λ = 0,62 (unidades do sólido)
        intens = 0.5 + 0.5 * math.cos(fase_opt)                                           # 1 = construtiva, 0 = destrutiva
        nodo.inputs["Emission Strength"].default_value = 0.05 + 3.4 * intens
        brilho.location = (dx + L * math.sin(th) + 0.7, 0, L * math.cos(th) + 0.3)

    atualizar(fase)
    proxy = _caixa((5.2, 3.0, 3.8), (0.4, 0, 0.6))
    return proxy, atualizar


# ── Michelson ────────────────────────────────────────────────────────────────
def interferometro_michelson(braco=2.4, lambda_=0.32, amplitude=0.34, movimento=0, fase=0.0):
    """Fonte (esfera branca à esquerda), divisor de feixe (placa de vidro a 45°), espelhos 1 (acima) e 2 (à direita, móvel) e
    um detector (disco embaixo) cujo brilho segue cos²(2π · 2 Δ / λ), com Δ = diferença dos braços. Feixes brancos. Com movimento o
    espelho 2 vai e volta e o detector pisca (franjas)."""
    L = braco
    src = v3.esfera_pt((-2.2, 0, 0), 0.16, v3.material_cor("Fonte", "texto_neutro", 2.4), "Fonte")
    bs = osc._caixa("Divisor", (0.08, 1.1, 1.1), (0, 0, 0))
    bs.rotation_euler = (0, 0, math.radians(45))
    cm.material_vidro(bs, cor=OT["vidro_cor"], base=0.3, ganho=0.6, brilho_borda=2.0)
    m1 = osc._caixa("Espelho1", (1.0, 0.1, 1.0), (0, L, 0))
    cm.material_vidro(m1, cor="fonte_fisica", base=0.6, ganho=0.6, brilho_borda=2.0)
    m2 = _movel("Espelho2", (0.1, 1.0, 1.0), (L, 0, 0))
    cm.material_vidro(m2, cor="fonte_fisica", base=0.6, ganho=0.6, brilho_borda=2.0)
    mat_b = v3.material_degrade("Detector", "texto_neutro", "fonte_contorno", 0.0001, 0.6)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.38, depth=0.08, vertices=48, location=(0, -L, 0))
    det = bpy.context.active_object
    det.name = "Detector"
    det.rotation_euler = (math.radians(90), 0, 0)
    det.data.materials.append(mat_b)
    nodo = mat_b.node_tree.nodes["Principled BSDF"]
    feixes = {k: _raio(k, _mat_raio(), 0.02) for k in ("Entrada", "ParaM1", "DeM1", "ParaM2", "DeM2", "ParaDet")}
    _def_raio(feixes["Entrada"], (-2.2, 0, 0), (0, 0, 0))
    _def_raio(feixes["ParaM1"], (0, 0, 0), (0, L, 0))
    _def_raio(feixes["DeM1"], (0, L, 0.03), (0, 0, 0.03))
    _def_raio(feixes["ParaDet"], (0, 0, 0.03), (0, -L, 0.03))

    def atualizar(fase):
        x2 = L + (amplitude * math.sin(2 * math.pi * fase) if movimento else 0.0)
        m2.location = (x2, 0, 0)
        _def_raio(feixes["ParaM2"], (0, 0, 0), (x2, 0, 0))
        _def_raio(feixes["DeM2"], (x2, 0, -0.03), (0, 0, -0.03))
        delta = x2 - L
        intens = 0.5 + 0.5 * math.cos(2 * math.pi * 2 * delta / lambda_)
        nodo.inputs["Emission Strength"].default_value = 0.05 + 3.4 * intens

    atualizar(fase)
    proxy = _caixa((L + 3.4, 2 * L + 1.2, 1.4), (L / 2 - 0.6, 0, 0))
    return proxy, atualizar


# ── rede de difração ─────────────────────────────────────────────────────────
def rede_de_difracao(n_fendas=5, largura=4.0, altura=3.0, espessura=0.12, fenda=0.16, separacao=0.5):
    """Anteparo opaco azul com `n_fendas` fendas verticais de largura `fenda` e período `separacao`; as bordas das fendas em
    azul-claro. É a generalização do anteparo_fenda_dupla para N fendas (rede de difração). O padrão de difração é do Manim."""
    mat = co._material("Rede", {"cor": "fonte_fisica", "emissao": OT["anteparo_emissao"], "rugosidade": 0.4, "metalico": 0.2})
    mat_r = v3.material_cor("BordaRede", "fonte_contorno", 1.0)
    n = int(n_fendas)
    centros = [(k - (n - 1) / 2) * separacao for k in range(n)]
    bordas = [-largura / 2]
    for c in centros:
        bordas += [c - fenda / 2, c + fenda / 2]
    bordas.append(largura / 2)
    for i in range(0, len(bordas), 2):
        y0, y1 = bordas[i], bordas[i + 1]
        o = osc._caixa("Anteparo", (espessura, y1 - y0, altura), (0, (y0 + y1) / 2, 0))
        o.data.materials.append(mat)
    for y in bordas[1:-1]:
        for x in (-espessura / 2, espessura / 2):
            ga.criar_curva("Borda", [([(x, y, -altura / 2), (x, y, altura / 2)], False)], mat_r, OT["aresta_espessura"])
    proxy = _caixa((espessura * 4, largura, altura), (0, 0, 0))
    return proxy


# ── polarizadores e lei de Malus ─────────────────────────────────────────────
def polarizador_malus(raio=1.15, separacao=2.6, angulo_graus=40.0, movimento=0, fase=0.0):
    """Luz que atravessa dois polarizadores (discos de vidro com o eixo de transmissão em linhas brancas): o primeiro polariza na
    vertical, o segundo (analisador) gira de θ; o campo E (setas ciano) depois do analisador tem amplitude E0 |cos θ| ao longo do eixo
    dele, e a intensidade ∝ cos² θ (Malus). Antes do primeiro, setas em várias direções (luz não polarizada). Com movimento θ dá
    uma volta."""
    x1, x2 = -separacao / 2, separacao / 2
    mat_E, mat_l = v3.material_cor("CampoE", "campo_eletrico", 1.6), v3.material_cor("EixoPol", "texto_neutro", 1.4)
    for x in (x1, x2):
        bpy.ops.mesh.primitive_cylinder_add(radius=raio, depth=0.07, vertices=64, location=(x, 0, 0))
        d = bpy.context.active_object
        d.name = "Polarizador"
        d.rotation_euler = (0, math.radians(90), 0)
        bpy.context.view_layer.objects.active = d
        d.select_set(True)
        bpy.ops.object.transform_apply(rotation=True)
        _vidro(d, base=0.18)
    ga.criar_curva("Feixe", v3.tracejado([(x1 - 2.0, 0, 0), (x2 + 2.2, 0, 0)], False, 0.22, 0.6), _mat_eixo(), 0.011)
    dinam1 = []
    for k in range(6):                                                    # luz não polarizada (várias direções)
        a = math.pi * k / 6
        v3.seta((x1 - 1.6, -0.5 * math.cos(a), -0.5 * math.sin(a)), (0, math.cos(a), math.sin(a)), mat_E, 1.0)
    v3.seta((x1 + 0.9, -0.0, -0.5), (0, 0, 1.0), mat_E, 1.0)             # depois do 1.º: vertical (E0 = 1)
    eixo1, eixo2 = _raio("Eixo1", mat_l, 0.02), _raio("Eixo2", mat_l, 0.02)
    _def_raio(eixo1, (x1 + 0.05, 0, -raio * 0.9), (x1 + 0.05, 0, raio * 0.9))
    sa = v3.seta((x2 + 0.9, 0, 0), (0, 0, 1), mat_E, 1.0)

    def atualizar(fase):
        th = 2 * math.pi * fase if movimento else math.radians(angulo_graus)
        u = (0.0, math.sin(th), math.cos(th))                                     # eixo do analisador (th = 0: vertical)
        _def_raio(eixo2, (x2 + 0.05, -raio * 0.9 * u[1], -raio * 0.9 * u[2]), (x2 + 0.05, raio * 0.9 * u[1], raio * 0.9 * u[2]))
        A = math.cos(th)
        v3.ajustar_seta(sa, (x2 + 0.9, -0.5 * A * u[1], -0.5 * A * u[2]), (0, A * u[1], A * u[2]), max(abs(A), 1e-4))

    atualizar(fase)
    proxy = _caixa((separacao + 5.2, 2 * raio + 0.8, 2 * raio + 0.8), (0.3, 0, 0))
    return proxy, atualizar


# ── relógio de luz ───────────────────────────────────────────────────────────
def relogio_de_luz(altura=2.0, velocidade=0.65, movimento=0, fase=0.0):
    """Relógio de luz: dois espelhos (barras de vidro) separados de L e um fóton (esfera) que vai de um ao outro. Visto de um
    referencial em que o relógio se move com velocidade v (seta branca), o fóton percorre a diagonal: (c Δt)² = L² + (v Δt)² (triângulo
    em violeta tracejado). Ciclo único: o relógio vai de x = 0 a x = v Δt enquanto o fóton sobe de um espelho ao outro."""
    L = altura
    c = 1.0
    gam = 1.0 / math.sqrt(1 - velocidade ** 2)
    dt = L / c * gam                                              # tempo da subida no referencial em que o relógio se move
    X = velocidade * dt
    mat_f = v3.material_degrade("Foton", "texto_neutro", "fonte_contorno", 2.0, 0.7)
    foton = v3.esfera_pt((0, 0, 0), 0.13, mat_f, "Foton")
    base = _movel("EspelhoBaixo", (1.4, 1.0, 0.16), (0, 0, -0.08))
    topo = _movel("EspelhoCima", (1.4, 1.0, 0.16), (0, 0, L + 0.08))
    for o in (base, topo):
        cm.material_vidro(o, cor="fonte_fisica", base=0.5, ganho=0.6, brilho_borda=2.0)
    mat_d = _mat_dash()
    ga.criar_curva("Diagonal", v3.tracejado([(0, 0, 0), (X, 0, L)], False, 0.22, 0.6), mat_d, 0.016)
    ga.criar_curva("Vertical", v3.tracejado([(X, 0, 0), (X, 0, L)], False, 0.2, 0.6), mat_d, 0.016)
    ga.criar_curva("Horizontal", v3.tracejado([(0, 0, 0), (X, 0, 0)], False, 0.2, 0.6), mat_d, 0.016)
    mat_vf = v3.material_cor("VetorFisico", "vetor_fisico", co.ST["materiais"]["vetor_fisico"]["emissao"])
    fantasma = _movel("MarcaFinal", (1.4, 1.0, 0.04), (X, 0, 0.02))
    cm.material_vidro(fantasma, base=0.05, ganho=0.3, brilho_borda=1.0)
    ga.criar_curva("PosicaoFinal", v3.tracejado([(X - 0.7, -0.5, L + 0.1), (X + 0.7, -0.5, L + 0.1), (X + 0.7, 0.5, L + 0.1), (X - 0.7, 0.5, L + 0.1)], True, 0.2, 0.6), mat_d, 0.012)
    dinam = []

    def atualizar(fase):
        f = min(max(fase, 0.0), 1.0) if movimento else 0.0
        x = X * f
        base.location = (x, 0, -0.08)
        topo.location = (x, 0, L + 0.08)
        foton.location = (x, 0, L * f)
        v3.remover(dinam)
        dinam.append(v3.seta((x - 1.9, 0, L / 2), (1.0, 0, 0), mat_vf, 1.0))

    atualizar(fase)
    proxy = _caixa((X + 3.6, 1.6, L + 1.6), (X / 2, 0, L / 2))
    return proxy, atualizar


# ── átomo de Bohr ────────────────────────────────────────────────────────────
def atomo_bohr(n_inicial=3, n_final=2, escala=0.55, instante=0.5, voltas=2, fase=0.0):
    """Átomo de Bohr: núcleo (esfera branca), órbitas tracejadas (violeta) de raio ∝ n² e um elétron. No instante `instante` o
    elétron salta de n_inicial para n_final e emite um fóton (esfera que se afasta). Ciclo único."""
    ni, nf = int(n_inicial), int(n_final)
    rn = lambda n: escala * n * n
    mat_d = _mat_dash()
    v3.esfera_pt((0, 0, 0), 0.22, v3.material_degrade("Nucleo", "texto_neutro", "fonte_fisica", 1.4, 0.6), "Nucleo")
    for n in range(1, max(ni, nf) + 1):
        c = [(rn(n) * math.cos(2 * math.pi * k / 120), rn(n) * math.sin(2 * math.pi * k / 120), 0) for k in range(120)]
        ga.criar_curva("Orbita", v3.tracejado(c, True, 0.24, 0.6), mat_d, 0.012)
    el = v3.esfera_pt((rn(ni), 0, 0), 0.11, v3.material_degrade("Eletron", "fonte_contorno", "fonte_fisica", 1.8, 0.7), "Eletron")
    fot = v3.esfera_pt((0, 0, 0), 0.11, v3.material_cor("Foton", "texto_neutro", 3.0), "Foton")
    onda_obj, sp_on = osc.curva_viva("OndaFoton", 40, v3.material_cor("OndaFoton", "texto_neutro", 1.6), 0.014)
    ang_salto = 2 * math.pi * voltas * instante

    def atualizar(fase):
        f = min(max(fase, 0.0), 1.0)
        a = 2 * math.pi * voltas * f
        if f < instante:
            r = rn(ni)
        elif f < instante + 0.08:
            s = (f - instante) / 0.08
            s = s * s * (3 - 2 * s)
            r = rn(ni) + (rn(nf) - rn(ni)) * s
        else:
            r = rn(nf)
        el.location = (r * math.cos(a), r * math.sin(a), 0)
        if f > instante:
            dire = Vector((math.cos(ang_salto), math.sin(ang_salto), 0))
            d = (f - instante) * 9.0 * rn(ni) / 3
            fot.location = tuple(dire * (rn(ni) + d) + Vector((0, 0, 0)))
            fot.scale = (1, 1, 1)
            perp = Vector((-dire.y, dire.x, 0))
            pts = [tuple(dire * (rn(ni) + d - 1.4 * kk / 39) + perp * 0.14 * math.sin(2 * math.pi * 3.5 * kk / 39)) for kk in range(40)]
            osc.pontos_curva(sp_on, pts)
        else:
            fot.location = (0, 0, -90)
            osc.pontos_curva(sp_on, [(0, 0, -90 - 0.001 * kk) for kk in range(40)])

    atualizar(fase)
    proxy = _caixa((2 * rn(max(ni, nf)) + 2.4, 2 * rn(max(ni, nf)) + 2.4, 1.0), (0, 0, 0))
    return proxy, atualizar


def cena_preview():
    co.limpar_cena()
    proxy, _ = dioptro_plano(movimento=0)
    co.mundo()
    co.luzes()
    co.camera_enquadrada(co.cantos([proxy]), azimute=-90, elevacao=6, margem=0.08)
    co.render(co.OUT / "otica_b_v1.png")


if __name__ == "__main__":
    cena_preview()
