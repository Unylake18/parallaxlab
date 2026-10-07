"""Onda numa corda e ondas na superfície com duas fontes (Física II 5.3 e 5.4) — estudo 17 (sandbox).

Rodar: blender.exe -b -P experimentos/blender/ondas.py   (gera out/ondas_v1.png)

Corda: curva azul-claro y(x, t) com contas neutras que só sobem e descem (a partícula não anda com a onda); estacionária:
nós = marcas violeta, envelope = pontilhado violeta. Superfície: vidro azul com malha azul-claro, duas fontes neutras.
fase de 0 a 1 = UM período (fase=1 repete a fase 0). Frentes de onda, λ, v e as fórmulas são do Manim.
"""

import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import gaussiana as ga  # noqa: E402
import oscilacoes as osc  # noqa: E402
import vetores3d as v3  # noqa: E402

ON = co.ST["materiais"]["ondas"]


def _esfera(nome, raio, mat, pos=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=raio, segments=32, ring_count=16, location=pos)
    o = bpy.context.active_object
    o.name = nome
    bpy.ops.object.shade_smooth()
    o.data.materials.append(mat)
    return o


def criar_corda(tipo="progressiva", comprimento=8.0, n_ondas=2, amplitude=0.9, n_contas=9, fase=0.0, nos=1):
    """Corda ao longo de X (de −L/2 a L/2). 'progressiva': y = A sen(kx − 2π fase) (para +X); 'estacionaria':
    y = A sen(kx) cos(2π fase), extremos fixos (n_ondas deve ser inteiro). Devolve (proxy, atualizar(fase))."""
    L, A = comprimento, amplitude
    k = 2 * math.pi * n_ondas / L
    x0 = -L / 2
    mat_c = v3.material_cor("Corda", ON["corda_cor"], ON["corda_emissao"])
    NP = 220
    _, sp = osc.curva_viva("Corda", NP, mat_c, ON["corda_espessura"])
    mat_b = v3.material_cor("Conta", ON["conta_cor"], ON["conta_emissao"])
    contas = [_esfera("Conta", ON["conta_raio"], mat_b) for _ in range(int(n_contas))]
    mat_t = co._material("TracoOnda", {"cor": "gaussiana", "emissao": 1.8, "rugosidade": 0.4})
    ga.criar_curva("Repouso", v3.tracejado([(x0, 0, 0), (-x0, 0, 0)], False, 0.22, 0.6), mat_t, 0.01)
    estac = tipo == "estacionaria"
    if estac:
        env_s = [(x0 + L * i / 160, 0, A * math.sin(k * (L * i / 160))) for i in range(161)]
        ga.criar_curva("EnvoltoriaSup", v3.tracejado(env_s, False, 0.2, 0.6), mat_t, 0.01)
        ga.criar_curva("EnvoltoriaInf", v3.tracejado([(x, 0, -z) for x, _, z in env_s], False, 0.2, 0.6), mat_t, 0.01)
        if nos:
            mat_n = co._material("No", {"cor": "gaussiana", "emissao": 2.2, "rugosidade": 0.4})
            for j in range(2 * int(n_ondas) + 1):
                _esfera("No", ON["no_raio"], mat_n, (x0 + j * L / (2 * n_ondas), 0, 0))
    proxy = osc._caixa("ProxyEnquadramento", (L + 0.8, 0.5, 2 * A + 0.9), (0, 0, 0))
    proxy.hide_render = True

    def y(x, f):
        if estac:
            return A * math.sin(k * (x - x0)) * math.cos(2 * math.pi * f)
        return A * math.sin(k * (x - x0) - 2 * math.pi * f)

    def atualizar(fase):
        osc.pontos_curva(sp, [(x0 + L * i / (NP - 1), 0.0, y(x0 + L * i / (NP - 1), fase)) for i in range(NP)])
        for j, c in enumerate(contas):
            x = x0 + L * (j + 0.5) / len(contas)
            c.location = (x, 0.0, y(x, fase))

    atualizar(fase)
    return proxy, atualizar


def criar_ondas_superficie(extensao=5.0, separacao=3.0, comprimento_onda=1.8, amplitude=0.42, resolucao=64, fase=0.0):
    """Superfície de água com duas fontes coerentes em (±separacao/2, 0): z = A Σ sen(k r_i − 2π fase)/√(1 + 0.5 r_i).
    fase de 0 a 1 = um período. Devolve (corpo, atualizar(fase))."""
    E, N = extensao, resolucao
    k = 2 * math.pi / comprimento_onda
    verts = [(-E + 2 * E * i / N, -E + 2 * E * j / N, 0.0) for i in range(N + 1) for j in range(N + 1)]
    faces = [(i * (N + 1) + j, (i + 1) * (N + 1) + j, (i + 1) * (N + 1) + j + 1, i * (N + 1) + j + 1)
             for i in range(N) for j in range(N)]
    me = bpy.data.meshes.new("Agua")
    me.from_pydata(verts, [], faces)
    me.update()
    corpo = bpy.data.objects.new("Agua", me)
    bpy.context.collection.objects.link(corpo)
    bpy.context.view_layer.objects.active = corpo
    corpo.select_set(True)
    sol = corpo.modifiers.new("Espessura", "SOLIDIFY")
    sol.thickness = 0.04
    bpy.ops.object.shade_smooth()
    cm.material_vidro(corpo)
    grade = bpy.data.objects.new("MalhaAgua", me)                     # mesmos dados: acompanha a deformação
    bpy.context.collection.objects.link(grade)
    wf = grade.modifiers.new("Malha", "WIREFRAME")
    wf.thickness = ON["malha_espessura"]
    wf.use_replace = True
    grade.data.materials.append(v3.material_cor("MalhaAgua", ON["malha_cor"], ON["malha_emissao"]))
    mat_f = v3.material_cor("Fonte", ON["conta_cor"], ON["conta_emissao"])
    fontes = [(-separacao / 2, 0.0), (separacao / 2, 0.0)]
    for fx, fy in fontes:
        _esfera("Fonte", ON["fonte_raio"], mat_f, (fx, fy, 0.0))
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    buf = [0.0] * (3 * len(verts))

    def atualizar(fase):
        a = 2 * math.pi * fase
        for idx, (x, y_) in enumerate(zip(xs, ys)):
            z = 0.0
            for fx, fy in fontes:
                r = math.hypot(x - fx, y_ - fy)
                z += math.sin(k * r - a) / math.sqrt(1.0 + 0.5 * r)
            d = min(max((1.0 - math.hypot(x, y_) / E) / 0.3, 0.0), 1.0)          # amortece até zero na borda
            buf[3 * idx], buf[3 * idx + 1], buf[3 * idx + 2] = x, y_, amplitude * z * d * d * (3 - 2 * d)
        me.vertices.foreach_set("co", buf)
        me.update()

    atualizar(fase)
    return corpo, atualizar


def cena_preview():
    co.limpar_cena()
    proxy, _ = criar_corda("estacionaria", n_ondas=2, fase=0.1)
    co.mundo()
    co.luzes()
    co.camera_enquadrada(co.cantos([proxy]), azimute=-20, elevacao=14, margem=0.08)
    co.render(co.OUT / "ondas_v1.png")


if __name__ == "__main__":
    cena_preview()
