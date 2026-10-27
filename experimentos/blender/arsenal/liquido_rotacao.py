"""Líquido em rotação rígida: superfície livre plano -> paraboloide (candidato do arsenal, sandbox) — rodada 3 (setor angular).

Recipiente cilíndrico de vidro (raio interno R) com líquido. A superfície livre vem de UMA fórmula, usada de verdade na malha
(inalterada desde a rodada 1):

    z(r, λ) = h0 - λ α R² / 2 + λ α r²,        α = ω² / (2 g),      Δh = α R²,      0 ≤ λ ≤ 1

λ = 0: plano em z = h0. λ = 1: paraboloide final, centro em h0 - Δh/2 e borda em h0 + Δh/2. A conservação do volume NÃO é
corrigida à mão: ∫0^R z r dr = h0 R²/2 - λ α R⁴/4 + λ α R⁴/4 = h0 R²/2 para todo λ (os termos em λ se cancelam).

NÃO é dinâmica de fluidos: sem ondas, splash, viscosidade ou oscilação. λ é parâmetro geométrico (homotopia), não tempo físico.

Duas coordenadas independentes (função `estado` do controle):
  • λ            -> SÓ a forma da superfície e do setor angular que a acompanha;
  • fase_rotacao -> SÓ o azimute do setor: φ = φ_inicial + 2π · voltas · fase_rotacao.
Tracers pontuais permanecem apenas como opção do modo QA, com r/z constantes.

Estados visuais (`estado_visual`; flags grade/meridiana/referencia/setor: -1 = "conforme o estado", 0/1 forçam;
marcadores só é aceito em qa):
  fenomeno   líquido limpo + um setor translúcido, sem tracers                 (padrão)
  geometria  grade discreta + UMA seção meridiana destacada, sem setor/tracers por padrão
  qa         grade, meridiana, setor, tracers opcionais e referência z = h0

Volume fechado: corpo (lateral + fundo + topo, normais para fora) + "interior" (lateral e fundo com normais para dentro, que
mostram a parede e o chão do fundo por dentro) + lâmina fina da superfície livre. Roda só dentro do Blender (importa bpy).
"""

import math
import sys
from pathlib import Path
from types import SimpleNamespace

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import gaussiana as ga  # noqa: E402
import vetores3d as v3  # noqa: E402

N_THETA = 128         # segmentos azimutais; smooth shading, sem subdivisão extra
N_RAIOS = 32          # anéis radiais da superfície livre
N_CURVA = 256         # pontos dos anéis desenhados como curva
FOLGA_VIDRO = 0.06    # espessura visual da parede de vidro (fora do raio interno R)
ELEVA_SUPERFICIE = 0.006   # a lâmina da superfície sobe um fio, contra z-fighting com o corpo do líquido
ELEVA_SETOR = ELEVA_SUPERFICIE + 0.003  # separação mínima da interface; não altera o volume físico
TAM_TRACER = 0.028    # raio do octaedro-tracer (todos iguais; sem aparência de bolha)
MARGEM_FOLGA = 0.08   # folga mínima do centro ao fundo e da borda ao topo no estado final
ESTADOS = {           # (marcadores, grade, meridiana, referencia, setor)
    "fenomeno": (0, 0, 0, 0, 1),
    "geometria": (0, 1, 1, 0, 0),
    "qa": (1, 1, 1, 1, 1),
}
_SEM = object()


# ── física (Python puro) ─────────────────────────────────────────────────────
def altura_superficie(r, lam, R, h0, alpha):
    """z(r, λ) = h0 - λ α R²/2 + λ α r². É a única fonte de altura da superfície."""
    return h0 - lam * alpha * R ** 2 / 2 + lam * alpha * r ** 2


def altura_tracer(r, R, h0, alpha, profundidade):
    """z constante de um anel de tracers: abaixo da superfície para QUALQUER λ ∈ [0,1]. z(r,λ) é linear em λ, então o menor valor
    está em λ=0 (h0) ou λ=1 (z(r,1))."""
    return min(h0, altura_superficie(r, 1.0, R, h0, alpha)) - profundidade


def suave(t):
    """Smoothstep: easing monotônico, derivada zero nos extremos."""
    t = min(max(float(t), 0.0), 1.0)
    return t * t * (3 - 2 * t)


def estado_editorial(tipo, fase):
    """Roteiros de preview; fase normalizada é tempo editorial, não transiente físico.
    Retorna apenas controles pertinentes: morph não altera fase_rotacao; rotação não altera λ.
    """
    if tipo == "morph":
        return {"lam": suave((fase - 0.15) / 0.60)}
    if tipo == "rotacao":
        return {"fase_rotacao": float(fase)}
    if tipo == "payoff":
        revela = suave((fase - 0.18) / 0.62)
        return {"lam": 1.0, "revela": revela, "revela_grade": revela}
    raise ValueError(f"Tipo editorial desconhecido: {tipo}")


# ── malhas ───────────────────────────────────────────────────────────────────
def _objeto(nome, vertices, faces):
    me = bpy.data.meshes.new(nome)
    me.from_pydata(vertices, [], faces)
    me.update()
    o = bpy.data.objects.new(nome, me)
    bpy.context.collection.objects.link(o)
    return o


def _topologia_superficie():
    """Índices: 0 = centro; anel i (1..N_RAIOS), segmento j -> 1 + (i-1) N_THETA + j. Faces com normal para +z."""
    idx = lambda i, j: 1 + (i - 1) * N_THETA + (j % N_THETA)   # noqa: E731
    faces = [(0, idx(1, j), idx(1, j + 1)) for j in range(N_THETA)]
    for i in range(1, N_RAIOS):
        for j in range(N_THETA):
            faces.append((idx(i, j), idx(i + 1, j), idx(i + 1, j + 1), idx(i, j + 1)))
    return idx, faces


def _verts_superficie(zs, R, lift=0.0):
    """Vértices da superfície (centro + anéis) com z(r) por anel; `zs[i]` = altura do anel i (0 = centro)."""
    v = [(0.0, 0.0, zs[0] + lift)]
    for i in range(1, N_RAIOS + 1):
        r = R * i / N_RAIOS
        for j in range(N_THETA):
            a = 2 * math.pi * j / N_THETA
            v.append((r * math.cos(a), r * math.sin(a), zs[i] + lift))
    return v


def _zs(lam, R, h0, alpha):
    return [altura_superficie(R * i / N_RAIOS, lam, R, h0, alpha) for i in range(N_RAIOS + 1)]


def _criar_corpo_liquido(R, h0, alpha, lam, interior=False):
    """Volume fechado do líquido: fundo plano em z=0, parede lateral em r=R e topo = superfície livre z(r, λ).
    `interior=True`: só lateral e fundo, com as normais invertidas (para dentro): com backface culling, mostram a parede e o chão
    do lado de trás através do líquido (o topo e os vértices de superfície ficam na malha só para atualizar z do mesmo jeito)."""
    idx, faces_topo = _topologia_superficie()
    v = _verts_superficie(_zs(lam, R, h0, alpha), R)
    base = len(v)                   # anel do fundo (r = R, z = 0)
    for j in range(N_THETA):
        a = 2 * math.pi * j / N_THETA
        v.append((R * math.cos(a), R * math.sin(a), 0.0))
    centro_fundo = len(v)
    v.append((0.0, 0.0, 0.0))
    faces = [] if interior else list(faces_topo)
    for j in range(N_THETA):
        topo_a, topo_b = idx(N_RAIOS, j), idx(N_RAIOS, j + 1)
        fun_a, fun_b = base + j, base + (j + 1) % N_THETA
        parede, fundo = (topo_a, fun_a, fun_b, topo_b), (centro_fundo, fun_b, fun_a)      # normais para fora
        if interior:
            parede, fundo = parede[::-1], fundo[::-1]
        faces.append(parede)
        faces.append(fundo)
    return _objeto("LiquidoInterior" if interior else "LiquidoCorpo", v, faces)


def _criar_lamina_superficie(R, h0, alpha, lam):
    """Só o topo (a superfície livre): lâmina fina por cima do corpo, para a forma ficar legível."""
    _, faces = _topologia_superficie()
    o = _objeto("SuperficieLivre", _verts_superficie(_zs(lam, R, h0, alpha), R, ELEVA_SUPERFICIE), faces)
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def _criar_setor(R, h0, alpha, lam, angulo):
    """Uma região angular da própria superfície; sem bordas desenhadas ou espessura sólida.
    λ deforma as alturas em coordenadas locais; fase_rotacao aplica rotação rígida ao objeto.
    """
    if not 0 < angulo <= 90:
        raise ValueError('angulo_setor deve estar entre 0 e 90 graus (exclusive 0)')
    abertura = math.radians(angulo)
    n = max(4, math.ceil(N_THETA * angulo / 360))
    idx = lambda i, j: 1 + (i - 1) * (n + 1) + j
    verts = [(0, 0, altura_superficie(0, lam, R, h0, alpha) + ELEVA_SETOR)]
    for i in range(1, N_RAIOS + 1):
        r = R * i / N_RAIOS
        z = altura_superficie(r, lam, R, h0, alpha) + ELEVA_SETOR
        for j in range(n + 1):
            a = abertura * (j / n - 0.5)
            verts.append((r * math.cos(a), r * math.sin(a), z))
    faces = [(0, idx(1, j), idx(1, j + 1)) for j in range(n)]
    faces += [(idx(i,j), idx(i+1,j), idx(i+1,j+1), idx(i,j+1))
              for i in range(1, N_RAIOS) for j in range(n)]
    obj = _objeto('SetorRotacao', verts, faces)
    for p in obj.data.polygons:
        p.use_smooth = True
    return obj


def _atualizar_setor(obj, lam, R, h0, alpha):
    for v in obj.data.vertices:
        r = math.hypot(v.co.x, v.co.y)
        v.co.z = altura_superficie(r, lam, R, h0, alpha) + ELEVA_SETOR
    obj.data.update()


def _criar_recipiente(R, H):
    """Copo de vidro: parede cilíndrica (raio R + folga) e fundo; aberto em cima (a superfície livre é livre)."""
    Rg = R + FOLGA_VIDRO
    v, faces = [], []
    for z in (0.0, H):
        for j in range(N_THETA):
            a = 2 * math.pi * j / N_THETA
            v.append((Rg * math.cos(a), Rg * math.sin(a), z))
    for j in range(N_THETA):
        k = (j + 1) % N_THETA
        faces.append((j, N_THETA + j, N_THETA + k, k))      # parede, normal para fora
    centro = len(v)
    v.append((0.0, 0.0, 0.0))
    for j in range(N_THETA):
        faces.append((centro, (j + 1) % N_THETA, j))        # fundo, normal para baixo
    o = _objeto("Recipiente", v, faces)
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def _suavizar_com_quinas(obj):
    """Smooth shading por ângulo, calculado com λ=0 (quina de 90° entre topo, parede e fundo fica viva; o resto é liso)."""
    for o in bpy.context.selected_objects:
        o.select_set(False)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(40))
    obj.select_set(False)


def _atualizar_z(obj, zs, lift=0.0):
    """Reescreve só o z dos vértices da superfície (centro + anéis); os extras (parede/fundo) ficam como estão."""
    me = obj.data
    co_ = [0.0] * (3 * len(me.vertices))
    me.vertices.foreach_get("co", co_)
    co_[2] = zs[0] + lift
    for i in range(1, N_RAIOS + 1):
        for j in range(N_THETA):
            co_[3 * (1 + (i - 1) * N_THETA + j) + 2] = zs[i] + lift
    me.vertices.foreach_set("co", co_)
    me.update()


def _circulo_sobre_superficie(r, lam, R, h0, alpha, dz=0.0, n=N_CURVA):
    z = altura_superficie(r, lam, R, h0, alpha) + dz
    return [(r * math.cos(2 * math.pi * k / n), r * math.sin(2 * math.pi * k / n), z) for k in range(n)]


def _diametro(a, lam, R, h0, alpha, dz=0.0, n=120):
    """Seção da superfície pelo plano vertical de azimute `a` que contém o eixo: de -R a +R, é a PARÁBOLA z(s) = h0 - λαR²/2 + λαs²
    (uma meridiana em a e a oposta em a+π). Girá-la em torno do eixo gera o paraboloide."""
    return [(s * math.cos(a), s * math.sin(a), altura_superficie(abs(s), lam, R, h0, alpha) + dz)
            for s in (R * (2 * k / n - 1) for k in range(n + 1))]


def _meridiano(a, lam, R, h0, alpha, dz=0.0, n=40):
    return [(R * k / n * math.cos(a), R * k / n * math.sin(a), altura_superficie(R * k / n, lam, R, h0, alpha) + dz) for k in range(n + 1)]


def _revelavel(obj, slot=0):
    """Insere num material translúcido do arsenal um fator `Revela` (0-1) que multiplica opacidade e emissão. Devolve o nó Value."""
    nt = obj.data.materials[slot].node_tree
    bsdf = nt.nodes["Principled BSDF"]
    val = nt.nodes.new("ShaderNodeValue")
    val.name = "Revela"
    val.outputs[0].default_value = 1.0
    for entrada in ("Alpha", "Emission Strength"):
        sock = bsdf.inputs[entrada]
        origem = sock.links[0].from_socket
        mult = nt.nodes.new("ShaderNodeMath")
        mult.operation = "MULTIPLY"
        nt.links.new(origem, mult.inputs[0])
        nt.links.new(val.outputs[0], mult.inputs[1])
        nt.links.new(mult.outputs[0], sock)
    return val


def _atenuar_fundo(obj):
    """Fundo continua fechado, mas recebe material menos luminoso que a superfície livre."""
    mat = obj.data.materials[0].copy()
    mat.name = 'FundoLiquidoDiscreto'
    nt = mat.node_tree
    bsdf = nt.nodes['Principled BSDF']
    alfa = bsdf.inputs['Alpha'].links[0].from_node
    alfa.inputs[1].default_value = 0.12
    alfa.inputs[2].default_value = 0.12
    brilho = bsdf.inputs['Emission Strength'].links[0].from_node
    brilho.inputs[1].default_value = 0.2
    obj.data.materials.append(mat)
    for p in obj.data.polygons:
        if all(abs(obj.data.vertices[i].co.z) < 1e-8 for i in p.vertices):
            p.material_index = 1


def _revelavel_curva(mat):
    """Fade editorial de linhas, mantendo emissão proporcional à opacidade."""
    mat.surface_render_method = "BLENDED"
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    val = nt.nodes.new("ShaderNodeValue")
    val.outputs[0].default_value = 1.0
    mult = nt.nodes.new("ShaderNodeMath")
    mult.operation = "MULTIPLY"
    mult.inputs[1].default_value = bsdf.inputs["Emission Strength"].default_value
    nt.links.new(val.outputs[0], mult.inputs[0])
    nt.links.new(mult.outputs[0], bsdf.inputs["Emission Strength"])
    nt.links.new(val.outputs[0], bsdf.inputs["Alpha"])
    return val


# ── sólido ───────────────────────────────────────────────────────────────────
def liquido_rotacao(raio=1.2, altura_recipiente=2.35, nivel=1.35, delta_h=1.0, lam=1.0, estado_visual="fenomeno", marcadores=-1,
                    n_marc_interno=8, n_marc_externo=10, voltas=1, prof_marcador=0.08, grade=-1, meridiana=-1, fi_meridiana=30.0,
                    referencia=-1, movimento=0, fase=0.0, fase_rotacao=0.0, varrer_lambda=0,
                    setor=-1, angulo_setor=24.0, fi_setor=-35.0):
    """Líquido em rotação rígida num copo cilíndrico. `lam` ∈ [0, 1] deforma o plano (λ=0) até o paraboloide (λ=1) pela fórmula
    z = h0 - λ α R²/2 + λ α r², α = Δh/R² (g=1 nas unidades do sólido: ω² = 2 α g). `fase_rotacao` gira o setor (e tracers no QA),
    sem deformar o líquido; `lam` deforma a superfície e o setor, sem mudar o azimute. Tracers são bloqueados fora de `qa`.
    `estado_visual`: fenomeno | geometria | qa; marcadores/grade/meridiana/referencia/setor
    valem -1 (conforme o estado) ou 0/1. `fi_meridiana`: azimute (graus) da seção destacada; o padrão (30°) é perpendicular à
    câmera da ficha. `fase` + `varrer_lambda` só servem à animação-loop de QA (animar.py): a rotação segue `fase` e, com
    varrer_lambda=1, λ faz 0 → 1 → 0 em cosseno.

    Devolve (proxy, atualizar, apos_camera, controle). `controle.estado(lam, fase_rotacao, fi_meridiana, giro, revela, circulos)`
    atualiza só o que for passado (animações editoriais)."""
    R, H, h0 = float(raio), float(altura_recipiente), float(nivel)
    alpha = float(delta_h) / R ** 2
    if h0 - delta_h / 2 < MARGEM_FOLGA or h0 + delta_h / 2 > H - MARGEM_FOLGA:
        raise ValueError(f"nivel={h0}, delta_h={delta_h}, altura_recipiente={H}: no estado final o centro ({h0 - delta_h / 2:.3f}) "
                         f"expõe o fundo ou a borda ({h0 + delta_h / 2:.3f}) transborda; folga mínima {MARGEM_FOLGA}")
    if estado_visual not in ESTADOS:
        raise ValueError(f"estado_visual='{estado_visual}': use {', '.join(ESTADOS)}")
    pre = ESTADOS[estado_visual]
    marcadores, grade, meridiana, referencia, setor = (p if f < 0 else int(f) for p, f in
                                                      zip(pre, (marcadores, grade, meridiana, referencia, setor)))
    marcadores = marcadores if estado_visual == 'qa' else 0
    lam = min(max(float(lam), 0.0), 1.0)
    Rg = R + FOLGA_VIDRO

    # recipiente: vidro discreto; só o aro de cima (o fundo do copo quase some: o foco é a superfície livre)
    rec = _criar_recipiente(R, H)
    cm.material_vidro(rec, base=0.012, ganho=0.06, brilho_borda=0.2)
    mat_aro = v3.material_cor("AroRecipiente", "fonte_contorno", 0.12)
    ga.criar_curva("AroRecipiente", [([(Rg * math.cos(2 * math.pi * k / N_CURVA), Rg * math.sin(2 * math.pi * k / N_CURVA), H)
                                       for k in range(N_CURVA)], True)], mat_aro, 0.007)

    # líquido: volume fechado, mais saturado que o vidro (fonte_fisica)
    corpo = _criar_corpo_liquido(R, h0, alpha, 0.0)
    interior = _criar_corpo_liquido(R, h0, alpha, 0.0, interior=True)
    lamina = _criar_lamina_superficie(R, h0, alpha, 0.0)
    for o in (corpo, interior):
        _suavizar_com_quinas(o)
    cm.material_vidro(corpo, base=0.34, ganho=0.42, brilho_borda=1.1)
    cm.material_vidro(interior, base=0.26, ganho=0.30, brilho_borda=0.5)
    cm.material_vidro(lamina, cor="fonte_contorno", base=0.15, ganho=0.40, brilho_borda=0.4, rugosidade=0.38)
    for o in (corpo, interior):
        _atenuar_fundo(o)
    revela_nos = [_revelavel(o, slot) for o in (corpo, interior, lamina) for slot in range(len(o.data.materials))]
    setor_obj = None
    if setor:
        setor_obj = _criar_setor(R, h0, alpha, lam, float(angulo_setor))
        # Camada única, visível dos dois lados através do líquido: culling apagaria o setor na metade frontal do paraboloide.
        cm.material_vidro(setor_obj, cor='texto_neutro', modo='sem_sobreposicao', base=0.18,
                          ganho=0.0, brilho_borda=0.12, rugosidade=0.55)
        setor_obj.data.materials[0].node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value = 0.05
        revela_nos.append(_revelavel(setor_obj))
    mat_fundo = v3.material_cor("BaseLiquido", "fonte_fisica", 0.08)
    revela_fundo = _revelavel_curva(mat_fundo)
    ga.criar_curva("BaseLiquido", [([(R * math.cos(2 * math.pi * k / N_CURVA), R * math.sin(2 * math.pi * k / N_CURVA), 0.0)
                                     for k in range(N_CURVA)], True)], mat_fundo, 0.007)

    if referencia:      # elemento de QA: nível h0 (violeta tracejado, construção) sobre o vidro
        mat_ref = co._material("RefNivel", {"cor": "apoio_magenta", "emissao": 0.7, "rugosidade": 0.4})
        pts = [(Rg * math.cos(2 * math.pi * k / N_CURVA), Rg * math.sin(2 * math.pi * k / N_CURVA), h0) for k in range(N_CURVA)]
        ga.criar_curva("NivelReferencia", v3.tracejado(pts, True, 0.22, 0.6), mat_ref, 0.012)

    mat_grade = v3.material_cor("GradeSuperficie", "fonte_contorno", 0.3)
    revela_grade_no = _revelavel_curva(mat_grade)
    mat_contato = v3.material_cor("LinhaContato", "texto_neutro", 0.35)
    revela_contato = _revelavel_curva(mat_contato)
    mat_merid = v3.material_cor("SecaoMeridiana", "texto_neutro", 1.0)
    mat_tracer = v3.material_cor("Tracer", "texto_neutro", 0.25)
    dinam = []

    # tracers: poucos, mesmo tamanho, r e z constantes; só o ângulo muda
    tracers = []        # (objeto, φ0)
    if marcadores:
        for fr, n, desl in ((0.50, int(n_marc_interno), 0.0), (0.85, int(n_marc_externo), 0.5)):
            r = fr * R
            z = altura_tracer(r, R, h0, alpha, float(prof_marcador))
            for k in range(n):
                phi0 = 2 * math.pi * (k + desl) / n
                bpy.ops.mesh.primitive_uv_sphere_add(radius=TAM_TRACER, segments=4, ring_count=2, location=(r * math.cos(phi0), r * math.sin(phi0), z))
                o = bpy.context.active_object
                o.name = "Tracer"
                o.data.materials.append(mat_tracer)
                tracers.append((o, phi0, r, z))

    est = {"lam": lam, "fase_rot": float(fase_rotacao), "fi": math.radians(float(fi_meridiana)), "giro": None,
           "circulos": bool(grade), "revela": 1.0}

    def _curvas():
        v3.remover(dinam)
        L, fi = est["lam"], est["fi"]
        dinam.append(ga.criar_curva("LinhaContato", [(_circulo_sobre_superficie(R, L, R, h0, alpha, ELEVA_SUPERFICIE), True)], mat_contato, 0.005))
        grade_ = []
        if est["circulos"]:
            grade_ += [(_circulo_sobre_superficie(f * R, L, R, h0, alpha, 0.01), True) for f in (0.25, 0.5, 0.75)]
        if est["giro"] is None:
            if grade:                    # grade estática: 4 diâmetros (8 meridianos), alinhados à seção destacada
                grade_ += [(_diametro(fi + k * math.pi / 4, L, R, h0, alpha, 0.01), False) for k in range(4)]
        else:                            # varredura: deixa para trás os diâmetros já "gerados" (a cada 45°)
            grade_ += [(_diametro(fi + k * math.pi / 4, L, R, h0, alpha, 0.01), False)
                       for k in range(4) if k * math.pi / 4 <= est["giro"] + 1e-6 and est["giro"] > 1e-6]
        if grade_:
            dinam.append(ga.criar_curva("GradeSuperficie", grade_, mat_grade, 0.004))
        if meridiana or est["giro"] is not None:
            a = fi + (est["giro"] or 0.0)
            dinam.append(ga.criar_curva("SecaoMeridiana", [(_diametro(a, L, R, h0, alpha, 0.014), False)], mat_merid, 0.014))

    def _forma():
        zs = _zs(est["lam"], R, h0, alpha)
        _atualizar_z(corpo, zs)
        _atualizar_z(interior, zs)
        _atualizar_z(lamina, zs, ELEVA_SUPERFICIE)
        if setor_obj is not None:
            _atualizar_setor(setor_obj, est['lam'], R, h0, alpha)
        _curvas()

    def _rotacao():
        if setor_obj is not None:
            setor_obj.rotation_euler.z = math.radians(fi_setor) + 2 * math.pi * voltas * est['fase_rot']
        for (o, phi0, r, z) in tracers:
            phi = phi0 + 2 * math.pi * voltas * est["fase_rot"]       # φ(t) = φ0 + ω t ; r e z não mudam
            o.location = (r * math.cos(phi), r * math.sin(phi), z)
            o.rotation_euler = (0.0, 0.0, phi)

    def estado(lam=None, fase_rotacao=None, fi_meridiana=None, giro=_SEM, revela=None, circulos=None, revela_grade=None):
        """λ deforma superfície/setor; fase_rotacao só gira setor e tracers de QA. Controles independentes.
        `giro` (rad): varredura da seção meridiana. `revela` 0-1: opacidade do líquido e setor."""
        mudou_forma = False
        if lam is not None:
            est["lam"], mudou_forma = min(max(float(lam), 0.0), 1.0), True
        if fi_meridiana is not None:
            est["fi"], mudou_forma = math.radians(float(fi_meridiana)), True
        if giro is not _SEM:
            est["giro"], mudou_forma = giro, True
        if circulos is not None:
            est["circulos"], mudou_forma = bool(circulos), True
        if mudou_forma:
            _forma()
        if fase_rotacao is not None:
            est["fase_rot"] = float(fase_rotacao)
            _rotacao()
        if revela is not None:
            est["revela"] = min(max(float(revela), 0.0), 1.0)
            for no in [*revela_nos, revela_fundo, revela_contato]:
                no.outputs[0].default_value = est["revela"]
        if revela_grade is not None:
            revela_grade_no.outputs[0].default_value = min(max(float(revela_grade), 0.0), 1.0)

    def atualizar(fase_):
        """Loop de QA (animar.py): a rotação segue `fase_` (voltas inteiras: fecha sem emenda); com varrer_lambda, λ = 0 → 1 → 0."""
        L = 0.5 - 0.5 * math.cos(2 * math.pi * fase_) if (varrer_lambda and movimento) else lam
        estado(lam=L, fase_rotacao=float(fase_rotacao) + fase_)

    _forma()
    _rotacao()
    estado(revela=1.0)

    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, H / 2 + 0.15))
    proxy = bpy.context.active_object
    proxy.name = "ProxyEnquadramento"
    proxy.scale = (2 * Rg + 0.5, 2 * Rg + 0.5, H + 0.5)
    bpy.ops.object.transform_apply(scale=True)
    proxy.hide_render = True

    # O enquadramento padrão usa os 8 cantos de uma caixa; o copo é redondo e a caixa quadrada visa a diagonal (largura ~40%
    # maior): o copo ficava pequeno no 9:16. Depois da câmera, refaz o enquadramento (mesma direção) com pontos do próprio copo.
    pontos = [(Rg * math.cos(2 * math.pi * k / 48), Rg * math.sin(2 * math.pi * k / 48), z) for z in (0.0, H) for k in range(48)]

    def apos_camera(cam):
        _reenquadrar(cam, pontos, margem=0.035)

    controle = SimpleNamespace(estado=estado, R=R, H=H, h0=h0, alpha=alpha)
    return proxy, atualizar, apos_camera, controle


def _reenquadrar(cam, pontos, margem):
    """Ajusta distância e centragem da câmera (orientação fixa) até `pontos` ocuparem o quadro com `margem` em volta."""
    sc = bpy.context.scene
    largura, altura = sc.render.resolution_x, sc.render.resolution_y
    q = cam.rotation_euler.to_quaternion()
    frente, direita, cima = q @ Vector((0, 0, -1)), q @ Vector((1, 0, 0)), q @ Vector((0, 1, 0))
    centro = sum((Vector(p) for p in pontos), Vector()) / len(pontos)
    dist = (cam.location - centro).length
    alvo = cam.location + frente * dist
    for _ in range(20):
        cam.location = alvo - frente * dist
        bpy.context.view_layer.update()
        ndc = [world_to_camera_view(sc, cam, Vector(p)) for p in pontos]
        xs, ys = [n.x for n in ndc], [n.y for n in ndc]
        cx, cy = (min(xs) + max(xs)) / 2 - 0.5, (min(ys) + max(ys)) / 2 - 0.5
        ocupa = max(max(xs) - min(xs), max(ys) - min(ys))
        dist *= ocupa / (1 - 2 * margem)
        lado = dist * cam.data.sensor_width / cam.data.lens          # a dimensão maior do quadro vê `lado` à distância dist
        wv, hv = (lado, lado * altura / largura) if largura >= altura else (lado * largura / altura, lado)
        alvo += direita * cx * wv + cima * cy * hv
    cam.location = alvo - frente * dist
