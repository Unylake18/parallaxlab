"""Sólidos de revolução (Cálculo): método dos discos, das arruelas e das cascas — estudo 10 (sandbox).

Rodar (sem abrir a interface), a partir da raiz do repositório:
    blender.exe -b -P experimentos/blender/revolucao.py

Gera out/revolucao_v1.png (disco, arruela e cascas lado a lado). O corpo é vidro azul (a "física" da gramática); a
FATIA ELEMENTAR (disco, arruela ou casca, de espessura dx) é construção matemática em violeta, com arestas
tracejadas; a curva geratriz é azul-claro. Com movimento, a fatia varre o sólido em vaivém suave (fase de 0 a 1;
fase=1 reproduz a fase 0).

Eixos: discos e arruelas giram em torno de X (horizontal); cascas, em torno de Z (vertical).
"""

import math
import sys
from pathlib import Path

import bmesh
import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import gaussiana as ga  # noqa: E402

RV = co.ST["materiais"]["revolucao"]
EIXO = co.ST["materiais"]["eixo"]

# perfis normalizados: t em [0, 1] -> raio relativo em [0, 1]
PERFIS = {
    "raiz": lambda t: math.sqrt(t),                                   # y = √x: paraboloide
    "parabola": lambda t: t * t,                                      # y = x²: "trompete"
    "cone": lambda t: t,                                              # y = x: cone
    "elipsoide": lambda t: math.sqrt(max(0.0, 1 - (2 * t - 1) ** 2)),  # semi-elipse: elipsoide (esfera se L = 2 R)
}


def _suave(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(35))


def malha_revolucao(nome, perfil, eixo="X", n=96):
    """Revolve o laço fechado `perfil` [(s, r), ...] em torno do eixo (X ou Z). Vértices sobre o eixo são fundidos."""
    bm = bmesh.new()
    aneis = []
    for s, r in perfil:
        anel = []
        for j in range(n):
            a = 2 * math.pi * j / n
            anel.append(bm.verts.new((s, r * math.cos(a), r * math.sin(a)) if eixo == "X"
                                     else (r * math.cos(a), r * math.sin(a), s)))
        aneis.append(anel)
    m = len(perfil)
    for i in range(m):
        A, B = aneis[i], aneis[(i + 1) % m]
        for j in range(n):
            try:
                bm.faces.new((A[j], A[(j + 1) % n], B[(j + 1) % n], B[j]))
            except ValueError:
                pass
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(nome)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(nome, me)
    bpy.context.collection.objects.link(obj)
    _suave(obj)
    return obj


def _curva_perfil(nome, pts, mat):
    return ga.criar_curva(nome, [(pts, False)], mat, RV["perfil_espessura"])


def _mat_perfil():
    return co._material("Geratriz", {"cor": RV["perfil_cor"], "emissao": RV["perfil_emissao"], "rugosidade": 0.4})


def _linha_eixo(p0, p1):
    mat = co._material("EixoRevolucao", {"cor": EIXO["cor"], "emissao": RV["eixo_emissao"], "rugosidade": 0.5})
    return ga.criar_curva("Eixo", ga.linha(p0, p1, False), mat, EIXO["espessura"])


class Fatia:
    """Fatia elementar violeta: reconstruída a cada atualização (a geometria depende da posição)."""

    def __init__(self, construir):
        self.construir = construir          # callable(t) -> (perfil_do_laço, eixo, [(centro, u, v, raio), ...])
        self.objs = []
        self.mat_vidro = None
        self.mat_traco = ga.material_traco()

    def _limpar(self):
        for o in self.objs:
            dado = o.data
            bpy.data.objects.remove(o, do_unlink=True)
            if dado is not None and dado.users == 0:
                (bpy.data.meshes if isinstance(dado, bpy.types.Mesh) else bpy.data.curves).remove(dado)
        self.objs = []

    def definir(self, t):
        self._limpar()
        perfil, eixo, circulos = self.construir(t)
        corpo = malha_revolucao("Fatia", perfil, eixo)
        if self.mat_vidro is None:
            cm.material_vidro(corpo, cor=RV["fatia_cor"], base=RV["fatia_vidro_base"], ganho=RV["fatia_vidro_ganho"],
                              brilho_borda=RV["fatia_vidro_brilho"])
            self.mat_vidro = corpo.data.materials[0]
        else:
            corpo.data.materials.append(self.mat_vidro)
        self.objs.append(corpo)
        for c, u, v, r in circulos:                                  # arestas tracejadas violeta
            self.objs.append(ga.criar_curva("FatiaAresta", ga.circulo(c, u, v, r, False), self.mat_traco))


def _loop_retangulo(s0, s1, r0, r1):
    """Laço do retângulo [s0, s1] x [r0, r1] no semiplano (s, r)."""
    return [(s0, r0), (s0, r1), (s1, r1), (s1, r0)]


def _vaivem(fase):
    """0 -> 1 -> 0 suave ao longo de uma fase completa: fase=0 e fase=1 coincidem (loop perfeito)."""
    return 0.5 - 0.5 * math.cos(2 * math.pi * fase)


def criar_revolucao(metodo="disco", perfil="raiz", comprimento=4.0, raio_max=1.6, raio_base=2.0, altura=3.0,
                    fatia=1, posicao_fatia=0.5, espessura_fatia=0.14, perfil_visivel=1, eixo=1, movimento=0, fase=0.0):
    """Sólido de revolução. metodo: 'disco', 'arruela' (região entre `raiz` e `parabola`) ou 'casca'.
    Devolve (corpo, atualizar(fase)); `atualizar` move a fatia em vaivém (use com `movimento`)."""
    NP = 80
    mat_g = _mat_perfil()
    f_ext = PERFIS[perfil if metodo == "disco" else "raiz"]
    f_int = PERFIS["parabola"]
    dx = espessura_fatia

    if metodo in ("disco", "arruela"):
        L, R = comprimento, raio_max
        xs = [L * i / NP for i in range(NP + 1)]
        if metodo == "disco":
            laco = [(0.0, 0.0)] + [(x, R * f_ext(x / L)) for x in xs] + [(L, 0.0)]
        else:  # arruela: curva externa de 0 a L e interna de volta (se tocam em 0 e em L)
            laco = [(x, R * f_ext(x / L)) for x in xs] + [(x, R * f_int(x / L)) for x in reversed(xs)]
        corpo = malha_revolucao("Corpo", laco, "X")
        cm.material_vidro(corpo)
        if perfil_visivel:
            _curva_perfil("Geratriz", [(x, R * f_ext(x / L), 0.0) for x in xs], mat_g)
            if metodo == "arruela":
                _curva_perfil("GeratrizInterna", [(x, R * f_int(x / L), 0.0) for x in xs], mat_g)
        if eixo:
            _linha_eixo((-0.5, 0, 0), (L + 0.5, 0, 0))

        def construir(t):
            x = L * (0.04 + 0.92 * t)
            ro = R * f_ext(x / L)
            ri = 0.0 if metodo == "disco" else R * f_int(x / L)
            circ = [((x + s * dx / 2, 0, 0), (0, 1, 0), (0, 0, 1), r) for s in (-1, 1) for r in ({ro, ri} - {0.0})]
            return _loop_retangulo(x - dx / 2, x + dx / 2, ri, ro), "X", circ
    elif metodo == "casca":
        a, H = raio_base, altura
        rs = [a * i / NP for i in range(NP + 1)]
        f = lambda r: H * (1 - (r / a) ** 2)                     # y = H (1 - (x/a)²), revolução em torno de Z
        # laço (s = z, r): fundo (z = 0) do eixo até a borda r = a, depois a curva de volta ao eixo, no topo z = H
        laco = [(0.0, 0.0), (0.0, a)] + [(f(r), r) for r in reversed(rs)][1:]
        corpo = malha_revolucao("Corpo", laco, "Z")
        cm.material_vidro(corpo)
        if perfil_visivel:
            _curva_perfil("Geratriz", [(r, 0.0, f(r)) for r in rs], mat_g)
        if eixo:
            _linha_eixo((0, 0, -0.4), (0, 0, H + 0.5))

        def construir(t):
            r = a * (0.1 + 0.8 * t)
            h = f(r)
            circ = [((0, 0, h), (1, 0, 0), (0, 1, 0), r + s * dx / 2) for s in (-1, 1)]
            circ += [((0, 0, 0), (1, 0, 0), (0, 1, 0), r + s * dx / 2) for s in (-1, 1)]
            return _loop_retangulo(0.0, h, r - dx / 2, r + dx / 2), "Z", circ
    else:
        raise ValueError(f"metodo desconhecido: {metodo}")

    sl = Fatia(construir) if fatia else None

    def atualizar(fase):
        if sl is not None:
            sl.definir(_vaivem(fase) if movimento else posicao_fatia)

    atualizar(fase)
    return corpo, atualizar


def cena_trio():
    co.limpar_cena()
    corpos = []
    for k, (metodo, kw) in enumerate((("disco", {}), ("arruela", {}), ("casca", {}))):
        antes = set(bpy.data.objects)
        corpo, _ = criar_revolucao(metodo, **kw)
        novos = [o for o in bpy.data.objects if o not in antes and o.parent is None]
        off = (k - 1) * 5.0
        for o in novos:
            o.location = (o.location[0], o.location[1] + off, o.location[2])
        corpos.append(corpo)
    co.mundo()
    co.luzes()
    co.camera_enquadrada(co.cantos(corpos), azimute=-35, elevacao=22, margem=0.07)
    co.render(co.OUT / "revolucao_v1.png")


if __name__ == "__main__":
    cena_trio()
