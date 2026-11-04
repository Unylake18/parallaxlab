"""vid_0031 — Por que o anel do Sol tem 22°? Camada Manim (transparente) sobre o 3D (cena3d/, render3d.js). v7.

O 3D dá o fundo (céu escurecido), o céu com o halo, o poste, o chão, os cristais, o cristal 2.5D e o FEIXE (uma malha só).
Esta cena desenha só o que é de leitura: a pessoa e o Sol do vid_0025 (arte_vid0025.py), a cena de lado, a comparação com o
arco-íris, o globo, o minimapa, ângulos, normais, rótulos, equações, gráficos, cone e textos. Tempos, layout e o estado do cristal por quadro vêm de roteiro.py (o mesmo que gera o timeline.json do 3D);
toda a física vem de fisica.py. Zonas: cabeçalho +8..+7 · A +6,8..+1,4 · B +1,2..−0,6 · C −0,8..−4,5; legenda (−4,67..−6) vazia.
Render (na raiz do repositório; --disable_caching é obrigatório):
    uv run python -m manim -t --disable_caching -r 540,960 --fps 15 videos/vid_0031_halo_22/cena.py HaloSol031
Modo seco (tempos + QA em segundos, sem desenhar): SECO=1 ... --dry_run --progress_bar none
Stills: STILLS=q1,q2,... SECO=1 ... -r 1080,1920 --dry_run → media_*/stills/q.png (só esses quadros são desenhados).
"""
from pathlib import Path
import json
import os
import sys

import numpy as np
from manim import *
from MF_Tools import TransformByGlyphMap

ROOT = Path(__file__).resolve().parents[2]
UNIT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(UNIT))
from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text
import fisica as F
import roteiro as RT
import arte_vid0025 as A

config.media_dir = str(UNIT / os.environ.get('MIDIA', 'media_preview'))
config.background_color = BACKGROUND_COLOR
TL = json.loads((UNIT / 'timeline.json').read_text(encoding='utf-8'))
E, CEU = RT.E, TL['ceu']
FPS = RT.FPS
SYNC_J = json.loads((UNIT / 'sync.json').read_text(encoding='utf-8')) if (UNIT / 'sync.json').exists() and not os.environ.get('SEM_SYNC') else None
SYNC_INV = {k: n for n, k in SYNC_J['mapa'].items()} if SYNC_J else {}

CYAN, VIOLET, MAG, ICE, DIM = PRIMARY_COLOR, SECONDARY_COLOR, '#EA63FF', '#9CC7FF', '#8FA3C4'
CLARO, RED, AZUL_GOTA, QUENTE = '#A8EEFF', '#FF5A4A', '#267BFF', '#FFB08A'
SOLC = A.WARM                                    # luz do Sol (§B.3): #FFC857, como no vid_0025
SOL = np.array([*CEU['sol_manim'], 0.])
BORDA = np.array([*CEU['borda_manim'], 0.])
CURVA22 = np.array([[x, y, 0.] for x, y in CEU['curva_22']])
TOPO_ANEL = max(y for _, y in CEU['curva_24'])
PERFIL = np.array(TL['perfil_anel']['rgb'])
P_A0, P_DA = TL['perfil_anel']['a0_deg'], TL['perfil_anel']['passo_deg']
DMIN, IMIN = float(F.d_min()), float(F.i1_min())
EL = RT.EL_SOL
FOLGA, FOLGA_T, MARGEM = .14, .25, .35            # traço · entre rótulos · borda da tela (§B.6)
Y_MAIN, Y_MEMO = 0.0, .9                                                  # C07: equação principal e memória (zona B)


def P3(p):
    return np.array([p[0], p[1], 0.])


FUNDO_TXT = '#050816'


def legivel(m):
    """Texto sem caixa (§B.2 v6): contorno fino na cor do fundo (2 px, 80 %) e uma sombra larga e fraca (cópia em traço grosso)."""
    sombra = m.copy().set_fill(opacity=0).set_stroke(FUNDO_TXT, 8, .3)
    m.set_stroke(FUNDO_TXT, 2.2, .8, background=True)
    g = VGroup(sombra, m)
    g._qa = 'texto'
    g.text = getattr(m, 'text', None)
    return g.set_z_index(40)


def T(s, size=24, color=TEXT_COLOR, maius=True, piso=26):
    size = max(size, piso)                                  # v7 §B.5: rótulos ≥ 14 px a 540 px (maiúsculas: tamanho ≥ 26)
    m = screen_text(s.upper() if maius else s, size, color=color, oversample=4 if len(s) < 30 else 2)
    if m.width > 8.2:
        m.scale_to_fit_width(8.2)
    m.text = s
    return legivel(m)


def M(tex, size=48, color=TEXT_COLOR):
    m = MathTex(tex, font_size=size, color=color).set_z_index(40)
    m.set_stroke(FUNDO_TXT, 2.2, .8, background=True)
    m._qa = 'texto'
    return m


def pinta(eq, cores):
    for cor, idx in cores.items():
        for i in idx:
            eq[0][i].set_color(cor)
    return eq


def contorno(m, w=6):
    return m.set_stroke(BACKGROUND_COLOR, w, .85, background=True)


def linha(pts, cor=TEXT_COLOR, w=3., op=1., qa=True):
    m = VMobject().set_points_as_corners([P3(p) for p in pts]).set_stroke(cor, w, op)
    if qa:
        m._qa = 'traco'
    return m


def oculta(pts):
    """Traço invisível só para o QA/posicionador (feixe e arestas desenhados pelo 3D)."""
    m = VMobject().set_points_as_corners([P3(p) for p in pts]).set_stroke(BLACK, 0, 1)
    m._qa = 'traco'
    return m


def tracejada(a, b, cor=TEXT_COLOR, w=2., op=.5, dash=.09, qa=False):
    a, b = P3(a), P3(b)
    if np.linalg.norm(b - a) < 1e-3:
        return VGroup()
    m = DashedLine(a, b, dash_length=dash, dashed_ratio=.55).set_stroke(cor, w, op)
    if qa:
        m._qa = 'traco'
    return m


def arco(P, v1, v2, r, cor, w=5., op=1.):
    """Arco do ângulo entre os vetores reais v1 → v2 (menor ângulo), centro P (o ponto exato da interseção)."""
    a1, a2 = np.arctan2(v1[1], v1[0]), np.arctan2(v2[1], v2[0])
    da = (a2 - a1 + PI) % TAU - PI
    m = Arc(radius=r, start_angle=a1, angle=da, arc_center=P3(P)).set_stroke(cor, w, op)
    m._qa = 'traco'                                    # o posicionador e o QA não deixam rótulo encostar no arco
    return m


def bissetriz(v1, v2):
    b = np.asarray(v1, float)[:2] / np.linalg.norm(v1[:2]) + np.asarray(v2, float)[:2] / np.linalg.norm(v2[:2])
    return b / np.linalg.norm(b)


def meio_arco(P, v1, v2, r):
    return np.asarray(P, float)[:2] + r * bissetriz(v1, v2)


def cruza(p1, d1, p2, d2):
    a, _ = np.linalg.solve(np.array([d1, -d2]).T, p2 - p1)
    return p1 + a * d1


def luz(pts, cor=SOLC, w=4.5, op=1.):
    """Feixe de luz no Manim (cenas de lado): UMA polilinha de núcleo + UMA de halo, desenhadas juntas."""
    pts = [P3(p) for p in pts]
    halo = VMobject().set_points_as_corners(pts).set_stroke(cor, w * 3.4, .16 * op)
    nucleo = VMobject().set_points_as_corners(pts).set_stroke(cor, w, op)
    nucleo._qa = 'traco'
    return VGroup(halo, nucleo)


def sol_icone(c, r=.3, op=1.):
    """O Sol do vid_0025 (make_sun), com opacidade."""
    g = A.make_sun(c, r)
    if op < 1:
        for f in g.get_family():
            if f.has_points():
                f.set_fill(opacity=f.get_fill_opacity() * op).set_stroke(opacity=f.get_stroke_opacity() * op)
    g[0]._borda_ok = True                              # halo translúcido (op ≤ 0,2) pode passar da margem; núcleo e raios não
    g[1]._qa = 'traco'                                 # raios do Sol: o posicionador não deixa rótulo encostar
    return g


def perfil_cor(ang, ganho=1.):
    k = np.clip((ang - P_A0) / P_DA, 0, len(PERFIL) - 1)
    c = np.array([np.interp(k, np.arange(len(PERFIL)), PERFIL[:, j]) for j in range(3)])
    b = c.max()
    return (rgb_to_color(c / b) if b > 1e-6 else WHITE), float(np.clip(ganho * b, 0, 1))


def anel_suave(centro, k, ang0=21.3, ang1=30., passo=.05, ganho=1.5, op=1.):
    """Anel a partir do perfil suavizado (passo fino: sem degraus)."""
    g = VGroup()
    for a in np.arange(ang0, ang1, passo):
        cor, b = perfil_cor(a + passo / 2, ganho)
        if b * op > .01:
            g.add(AnnularSector(inner_radius=a * k, outer_radius=(a + passo) * k + .002, angle=TAU, arc_center=P3(centro))
                  .set_fill(cor, b * op).set_stroke(width=0))
    return g


class VoaDe(ReplacementTransform):
    """Entrada de glyph map: os glifos de B nascem de uma cópia de 'origem' que voa até eles (cópia deliberada).
    ReplacementTransform de uma cópia (o TransformFromCopy interpola em 1 − α e inverteria o atraso do §B.8)."""
    def __init__(self, mobject, origem=None, **kw):
        super().__init__(origem.copy(), mobject, **kw)


def gm(A, B, *mapa, anda=(.2, .8), **kw):
    """Glyph map com tempos do §B.8: peças sem par saem em 0–35 %, entram em 65–100 %; termos andam em 'anda' (atraso, duração)."""
    an = TransformByGlyphMap(A, B, *mapa, auto_fade=True,
                             default_remover_kwargs={'run_time': .35},
                             default_introducer_kwargs={'delay': .65, 'run_time': .35},
                             default_transformer_kwargs={'delay': anda[0], 'run_time': anda[1]}, **kw)
    assert not an.show_indices, 'glyph map inválido (mostraria índices na tela)'
    return an


def redesenha(f):
    """Como always_redraw, mas troca os submobjects a cada quadro (become() não preserva as marcas de QA)."""
    g = VGroup(f())
    g.add_updater(lambda m, dt: setattr(m, 'submobjects', [f()]))     # dt: conta como "móvel" (sem cópia no fundo cacheado)
    return g


GELO, GELO_LUZ = '#CFE8FF', '#CFF6FF'               # gelo (§B.5): contorno/corpo e núcleo do raio dentro do gelo


GELO_TOPO = '#F2F9FF'


def sombra_ceu(m, cor='#0B1A33', n=10):
    """Sobre o céu claro: escurece o céu atrás do texto com um gradiente largo e suave (elipses fracas, sem borda; não é caixa)."""
    g = VGroup()
    for k in range(n):
        f = 1 + .12 * k
        g.add(Ellipse(width=m.width * f + .4, height=m.height * (1.3 + .25 * k) + .2).move_to(m).set_fill(cor, .018).set_stroke(width=0))
    g._qa_isento = True
    return g.set_z_index(38)


def veu_grafico(m, cor='#0B1A33', n=9):
    """Véu escuro e suave atrás de um gráfico sobre o céu claro (camadas largas e fracas, sem borda; abaixo do gráfico)."""
    g = VGroup()
    for k in range(n):
        g.add(RoundedRectangle(width=m.width + .3 + .22 * k, height=m.height + .3 + .22 * k, corner_radius=.5 + .1 * k)
              .move_to(m).set_fill(cor, .06).set_stroke(width=0))
    g._qa_isento = True
    return g.set_z_index(3)


def recorta(p, d, V):
    """Segmento da reta p + s·d dentro do polígono convexo V (Cyrus–Beck); None se não cruza."""
    s0, s1 = -1e9, 1e9
    c = V.mean(axis=0)
    for k in range(len(V)):
        a, b = V[k], V[(k + 1) % len(V)]
        n = np.array([b[1] - a[1], a[0] - b[0]])
        if n @ (c - a) < 0:
            n = -n
        num, den = n @ (p - a), n @ d
        if abs(den) < 1e-12:
            if num < 0:
                return None
            continue
        t = -num / den
        if den > 0:
            s0 = max(s0, t)
        else:
            s1 = min(s1, t)
    return None if s0 >= s1 else (p + s0 * d, p + s1 * d)


def estrela(p, r, op=1., cor=WHITE):
    """Brilho de gelo: estrela de 4 pontas."""
    p = np.asarray(p, float)[:2]
    pts = [P3(p + (r if k % 2 == 0 else .22 * r) * np.array([np.cos(k * PI / 4), np.sin(k * PI / 4)])) for k in range(8)]
    m = Polygon(*pts).set_fill(cor, op).set_stroke(cor, 1, op)
    m._desenho = True
    return m


def sol_redondo(c, R, op=1.):
    """O Sol do vid_0025 (make_sun) escalado para disco R: halo em quatro círculos e 12 raios curtos, tudo inteiro na tela."""
    c = P3(c)
    halo = VGroup(*[Circle(radius=R * k).move_to(c).set_fill(A.WARM, o * op).set_stroke(width=0)
                    for k, o in ((1.33, .045), (1.24, .075), (1.15, .12), (1.07, .2))])
    raios = VGroup(*[Line(c + R * 1.1 * np.array([np.cos(q), np.sin(q), 0]), c + R * (1.21 if k % 2 == 0 else 1.16) * np.array([np.cos(q), np.sin(q), 0]))
                     .set_stroke(A.WARM, 5, op) for k, q in enumerate(np.linspace(0, TAU, 12, endpoint=False))])
    nucleo = Circle(radius=R).move_to(c).set_fill(A.SUN_CORE, op).set_stroke(width=0)
    brilho = VGroup(*[Circle(radius=R * k).move_to(c + R * (1 - k) * .35 * np.array([-1, 1, 0]) / np.sqrt(2))
                      .set_fill('#FFF6D8', .16 * op).set_stroke(width=0) for k in (.82, .62, .42)])      # brilho interno: não chapado
    g = VGroup(halo, raios, nucleo, brilho)
    halo._borda_ok = True
    raios._qa = 'traco'
    g._sol = {'c': c[:2].copy(), 'R': R}
    return g


_ang22 = np.arctan2(CURVA22[:, 1] - SOL[1], CURVA22[:, 0] - SOL[0])
_r22 = np.hypot(CURVA22[:, 1] - SOL[1], CURVA22[:, 0] - SOL[0])
_o22 = np.argsort(_ang22)


def RAIO22(tt):
    """Vetor do centro do Sol à borda de 22° do céu do C01 (escala 1), no rumo tt da tela."""
    tt = (tt + PI) % TAU - PI
    r = np.interp(tt, _ang22[_o22], _r22[_o22], period=TAU)
    return r * np.array([np.cos(tt), np.sin(tt)])


def F_dentro(V, p):
    """p dentro do hexágono convexo V."""
    s = [(V[(k + 1) % 6][0] - V[k][0]) * (p[1] - V[k][1]) - (V[(k + 1) % 6][1] - V[k][1]) * (p[0] - V[k][0]) for k in range(6)]
    return all(x > -1e-9 for x in s) or all(x < 1e-9 for x in s)


def seta_chevron(p, d, cor, op, s=.11):
    """Chevron de sentido no meio de um segmento tracejado."""
    d = np.asarray(d, float)[:2] / np.linalg.norm(np.asarray(d, float)[:2])
    n = np.array([-d[1], d[0]])
    p = np.asarray(p, float)[:2]
    return linha([p - s * d + s * n, p, p - s * d - s * n], cor, 3, op, qa=False)



CORTES_R = ('c02', 'c03', 'c04', 'prisma', 'equacao', 'girar', 'conta', 'amontoado', 'lado9', 'ceu_volta', 'cores', 'sintese', 'cta')


def dist_caixa_pl(c, pl):
    """Menor distância de uma caixa [x0, y0, x1, y1] a uma polilinha (amostrada a cada 0,03)."""
    d = 1e9
    for p, q in zip(pl[:-1], pl[1:]):
        L = np.linalg.norm(q - p)
        for t_ in np.linspace(0, 1, max(2, int(L / .03) + 1)):
            x, y = p + t_ * (q - p)
            dx = max(c[0] - x, 0, x - c[2])
            dy = max(c[1] - y, 0, y - c[3])
            d = min(d, float(np.hypot(dx, dy)))
    return d


class HaloSol031(Scene):
    # ---------- tempo exato em quadros; modos seco e stills ----------
    def setup(self):
        self.nq, self.atrasos, self.capt, self.glifos_transicao, self.objetos_giro = 0, [], {}, [], []
        self.parados, self.glifos_parados, self.cone_qa, self.cone_pessoa, self.cone_info = {}, [], [], None, {}
        self.corte_r = []
        orig_add, orig_uf, orig_gf = self.renderer.add_frame, self.renderer.update_frame, self.renderer.get_frame
        # Sem o "fundo estático" do Cairo: ele grava numa imagem os objetos que julga parados no início de cada play/wait e
        # desenha por cima só os móveis; com os submobjects trocados a cada quadro (redesenha) isso deixava cópias velhas
        # (o rastro do giro). Aqui cada quadro redesenha a cena inteira.
        rend = self.renderer

        def sem_estatico(scene, static_mobjects):
            rend.static_image = None

        def desenha_tudo(scene, time, moving_mobjects=None):
            if rend.skip_animations:                       # faixa pulada (-n): só conta o quadro
                rend.add_frame(None)
                return
            rend.update_frame(scene)
            rend.add_frame(rend.get_frame())
        rend.save_static_frame_data, rend.render = sem_estatico, desenha_tudo
        seco = bool(os.environ.get('SECO'))
        stills = {int(q) for q in os.environ.get('STILLS', '').split(',') if q}
        if seco:
            def uf(*a, **k):
                if self.nq in stills:
                    return orig_uf(*a, **k)

            def gf():
                if self.nq in stills:
                    arr = orig_gf()
                    pasta = Path(config.media_dir) / 'stills'
                    pasta.mkdir(exist_ok=True)
                    from PIL import Image
                    Image.fromarray(arr).save(pasta / f'{self.nq}.png')
                    return arr
            self.renderer.update_frame, self.renderer.get_frame = uf, gf

        def conta(frame, num_frames=1):
            t = self.nq / FPS
            if E['giro_ini'] <= t < E['giro_fim'] - .1:       # só objetos desenháveis (cada wait deixa um Mobject vazio)
                self.objetos_giro.append(sum(1 for m in self.mobjects for f in m.get_family() if f.has_points()))
            if self.nq in self.capt:
                self.glifos_transicao.append({**self.capt[self.nq], 'cruzamentos': self.cruzamentos(self.capt[self.nq]['y'])})
            self.vigia_parados()
            if any(abs(t - E[k]) <= .5 for k in CORTES_R):
                self.corte_r.extend(self.meio_tom())
            cp = self.cone_pessoa                            # (p) a pessoa e o vértice em todos os quadros do cone
            if cp is not None and t < E['ceu_volta']:
                pes = [f for f in cp.get_family() if getattr(f, '_cone_pessoa', False)]
                vis = bool(pes) and max(g.get_fill_opacity() for f in pes for g in f.get_family() if g.has_points()) > .5
                self.cone_qa.append({'quadro': self.nq, 'pessoa': bool(vis and cp in self.mobjects)})
            self.nq += num_frames
            if not seco:
                return orig_add(frame, num_frames)
        self.renderer.add_frame = conta

    def meio_tom(self):
        """(r) glifo com opacidade entre 0,05 e 0,95 sobre outro glifo cheio ou sobre um traço visível (quadros perto dos cortes)."""
        parc, cheios, tracos = [], [], []
        for m in self.mobjects:
            if getattr(m, '_qa_isento', False):
                continue
            for f in m.get_family():
                if not f.has_points():
                    continue
                if isinstance(f, VMobjectFromSVGPath):
                    op = f.get_fill_opacity()
                    if .05 < op < .95:
                        parc.append(self.caixa(f))
                    elif op >= .95:
                        cheios.append(self.caixa(f))
                elif getattr(f, '_qa', None) == 'traco' and f.get_stroke_opacity() > .5:
                    a = np.asarray(f.get_anchors())[:, :2]
                    if len(a) > 1:
                        tracos.append(a)
        out = []
        for b in parc:
            hit = any(c[0] < b[2] and c[2] > b[0] and c[1] < b[3] and c[3] > b[1] and
                      not (abs(c[0] - b[0]) < 1e-6 and abs(c[1] - b[1]) < 1e-6) for c in cheios)
            if not hit:
                for pl in tracos:
                    if dist_caixa_pl(b, pl) < .02:
                        hit = True
                        break
            if hit:
                out.append({'quadro': self.nq, 'segundos': round(self.nq / FPS, 2), 'caixa': [round(x, 2) for x in b]})
        return out

    def vigia_parados(self):
        """(g) glifo em opacidade intermediária (0,05–0,95) parado (mesma opacidade e lugar) por mais de 0,3 s."""
        vistos = {}
        for m in self.mobjects:
            if getattr(m, '_qa_isento', False):
                continue
            for f in m.get_family():
                if isinstance(f, VMobjectFromSVGPath) and f.has_points():
                    op = f.get_fill_opacity()
                    if .05 < op < .95:
                        chave = (round(op, 3), *np.round(f.get_center()[:2], 3))
                        n = self.parados.get(id(f), (None, 0))
                        vistos[id(f)] = (chave, n[1] + 1 if n[0] == chave else 1)
                        if vistos[id(f)][1] == 6:
                            self.glifos_parados.append({'quadro': self.nq, 'segundos': round(self.nq / FPS, 2),
                                                        'opacidade': round(op, 2), 'centro': list(np.round(f.get_center()[:2], 2))})
        self.parados = vistos

    @property
    def tq(self):
        return self.nq / FPS

    _raw = False

    def get_time_progression(self, run_time, *a, **k):
        # com `-n` (render em faixas) o Manim pula as animações anteriores em UM passo, o que quebra os objetos que se refazem a
        # cada quadro e o contador de quadros: aqui o tempo das puladas percorre todos os quadros (atualiza, mas não desenha)
        k['override_skip_animations'] = True
        return super().get_time_progression(run_time, *a, **k)

    def escala_em(self, t):
        for a, b, s_ in RT.ESCALA:
            if a <= t < b:
                return s_
        return 1.

    def escala(self):
        return self.escala_em(self.tq + .5 / FPS)

    def untilr(self, chave, c):
        """until(E[chave] + c) com o deslocamento c na escala do trecho (as animações do trecho são reescaladas pelo mesmo fator)."""
        t0 = E[chave]
        self.until(t0 + c * self.escala_em(t0 - 1e-6 if c < 0 else t0 + 1e-6))

    def playr(self, *args, **kwargs):
        """play sem reescala (duração calculada para preencher o tempo que falta)."""
        self._raw = True
        try:
            return self.play(*args, **kwargs)
        finally:
            self._raw = False

    def play(self, *args, run_time=None, **kwargs):
        if os.environ.get('PLAYLOG'):
            open(os.environ['PLAYLOG'], 'a').write(f'{self.renderer.num_plays} {self.nq}\n')
        if self._raw or not RT.ESCALA:
            return super().play(*args, **kwargs) if run_time is None else super().play(*args, run_time=run_time, **kwargs)
        return super().play(*args, run_time=max(2 / FPS, (1. if run_time is None else run_time) * self.escala()), **kwargs)

    def wait(self, *args, **kwargs):
        self._raw = True
        try:
            return super().wait(*args, **kwargs)
        finally:
            self._raw = False

    def until(self, t):
        n = round(t * FPS) - self.nq
        if n < -1:
            self.atrasos.append(f'{t:.2f}s: bloco anterior terminou em {self.tq:.3f}s')
        if n > 0:
            self.wait((n - .5) / FPS)

    def at(self, nome):
        self.until(E[nome])
        if SYNC_J and nome in SYNC_INV:                        # atraso da imagem em relação à palavra da voz (âncora)
            a_ = SYNC_INV[nome]
            self.chegada[a_] = round(self.tq - SYNC_J['ancoras'][a_], 3)

    def mark(self, nome, qa=True):
        ev = {'estado': nome, 'segundos': round(self.tq, 3), 'quadro': self.nq}
        self.events.append(ev)
        if qa:
            self.geometria.append({**ev, **self.geom()})

    # ---------- estado do cristal (o mesmo do 3D) ----------
    def est(self, t=None):
        q = self.nq if t is None else round(t * FPS)
        if q not in self._est:
            self._est[q] = RT.estado_cristal(q / FPS)
        return self._est[q]

    # ---------- geometria (QA e posicionador) ----------
    def visiveis(self, tipo):
        out = []
        for m in self.mobjects:
            for s in m.get_family():
                if getattr(s, '_qa', None) != tipo:
                    continue
                fam = [f for f in s.get_family() if f.has_points()]
                if not fam:
                    continue
                op = max(max(f.get_fill_opacity(), f.get_stroke_opacity() if tipo == 'traco' else 0) for f in fam)
                if op > .2:
                    out.append(s)
        return out

    def caixa(self, m):
        pts = np.concatenate([f.points for f in m.get_family() if f.has_points()])
        return [float(pts[:, 0].min()), float(pts[:, 1].min()), float(pts[:, 0].max()), float(pts[:, 1].max())]

    def polilinha(self, m):
        out = []
        for f in m.get_family():
            if f.has_points() and f.get_stroke_opacity() > .2:
                a = np.asarray(f.get_anchors())
                if len(a) > 1:
                    out.append(a[:, :2])
        return out

    def geom(self):
        textos = [{'tex': getattr(m, 'tex_string', None) or getattr(m, 'text', None) or type(m).__name__,
                   'caixa': self.caixa(m)} for m in self.visiveis('texto')]
        tracos = [p.tolist() for m in self.visiveis('traco') for p in self.polilinha(m)]
        ymin = []
        for m in self.mobjects:
            for f in m.get_family():
                if isinstance(f, VMobject) and f.has_points() and (f.get_fill_opacity() > .05 or (f.get_stroke_width() > 0 and f.get_stroke_opacity() > .05)):
                    y = float(f.points[:, 1].min())
                    if y < -4.5:
                        ymin.append({'obj': type(f).__name__, 'y_min': round(y, 3)})
        fora = []

        def visita(m):
            if getattr(m, '_borda_ok', False) or getattr(m, '_qa_isento', False):
                return
            if isinstance(m, VMobject) and m.has_points() and (m.get_fill_opacity() > .05 or
                                                               (m.get_stroke_width() > 0 and m.get_stroke_opacity() > .05)):
                p = m.points
                x0, x1, y1 = p[:, 0].min(), p[:, 0].max(), p[:, 1].max()
                if x0 < -4.5 + MARGEM - 1e-3 or x1 > 4.5 - MARGEM + 1e-3 or y1 > 7.0 + 1e-3:
                    fora.append({'obj': type(m).__name__, 'caixa': [round(float(x0), 2), round(float(x1), 2), round(float(y1), 2)]})
            for sm in m.submobjects:
                visita(sm)
        for m in self.mobjects:
            visita(m)
        raios = []                                           # (i) todo raio nasce no disco do Sol, paralelo à reta olho → Sol
        for m in self.mobjects:
            for f in m.get_family():
                r = getattr(f, '_raio', None)
                if r is None or not f.has_points() or f.get_stroke_opacity() < .05:
                    continue
                a = np.asarray(f.get_anchors())[:, :2]
                k = next(j for j in range(1, len(a)) if np.linalg.norm(a[j] - a[0]) > 1e-3)
                v, d = a[k] - a[0], np.asarray(r['dir'], float)
                ang = float(np.degrees(np.arccos(np.clip(v @ d / np.linalg.norm(v) / np.linalg.norm(d), -1, 1))))
                raios.append({'dist_ini_sol': round(float(np.linalg.norm(a[0] - np.asarray(r['sol'], float)[:2])), 4),
                              'R': float(r['R']), 'ang_deg': round(ang, 4)})
        sois, caixas = [], []                            # (n) Sol inteiro na tela · (m) caixa atrás de texto
        for m in self.mobjects:
            for f in m.get_family():
                so = getattr(f, '_sol', None)
                if so:
                    c, R = np.asarray(so['c'], float), so['R']
                    ok = c[0] - R >= -4.5 + MARGEM - 1e-3 and c[0] + R <= 4.5 - MARGEM + 1e-3 and c[1] + R <= 7 + 1e-3 and c[1] - R >= -4.5
                    sois.append({'c': [round(float(c[0]), 2), round(float(c[1]), 2)], 'R': R, 'inteiro': bool(ok)})
                if (isinstance(f, (Rectangle, Polygon)) and f.has_points() and f.get_fill_opacity() > .05
                        and not getattr(f, '_desenho', False) and not getattr(f, '_moldura', False)):
                    b = self.caixa(f)
                    for t in textos:
                        a = t['caixa']
                        if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
                            caixas.append({'forma': type(f).__name__, 'texto': t['tex']})
        return {'textos': textos, 'tracos': tracos, 'abaixo_de_-4,5': ymin, 'fora_da_margem': fora, 'raios': raios,
                'sois': sois, 'caixas_texto': caixas}

    def cruzamentos(self, y):
        """Glifos (MathTex/Text) visíveis (opacidade > 0,4) na faixa da equação cujas caixas se sobrepõem (IoU > 0,12)."""
        gl = []
        for m in self.mobjects:
            for f in m.get_family():
                if isinstance(f, VMobjectFromSVGPath) and f.has_points() and f.get_fill_opacity() > .4:
                    b = self.caixa(f)
                    if abs((b[1] + b[3]) / 2 - y) < .9 and (b[3] - b[1]) < 1.:
                        gl.append(b)
        gl = list({tuple(np.round(b, 4)) for b in gl})
        n = 0
        for i in range(len(gl)):
            for j in range(i + 1, len(gl)):
                a, b = gl[i], gl[j]
                ix = max(0, min(a[2], b[2]) - max(a[0], b[0])); iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
                inter = ix * iy
                uni = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
                if uni > 0 and inter / uni > .12:
                    n += 1
        return n

    def livre(self, cx, cy, w, h, extra=()):
        x0, y0, x1, y1 = cx - w / 2 - FOLGA, cy - h / 2 - FOLGA, cx + w / 2 + FOLGA, cy + h / 2 + FOLGA
        if x0 < -4.5 + MARGEM or x1 > 4.5 - MARGEM or y0 < -4.45 or y1 > 6.95:
            return False
        d = FOLGA_T - FOLGA
        for m in self.visiveis('texto') + list(extra):
            a = self.caixa(m)
            if a[0] < x1 + d and a[2] > x0 - d and a[1] < y1 + d and a[3] > y0 - d:
                return False
        for m in self.visiveis('traco'):
            for pl in self.polilinha(m):
                for p, q in zip(pl[:-1], pl[1:]):
                    L = np.linalg.norm(q - p)
                    for s in np.linspace(0, 1, max(2, int(L / .03) + 1)):
                        x, y = p + s * (q - p)
                        if x0 <= x <= x1 and y0 <= y <= y1:
                            return False
        return True

    def coloca(self, m, ancora, pref, r0=.42, extra=(), guia_cor=DIM):
        """Rótulo perto da âncora, sem tocar traços nem textos (folga ≥ 0,14); VGroup(m) ou VGroup(m, seta-guia)."""
        a = np.asarray(ancora, float)[:2]
        pref = np.degrees(np.arctan2(pref[1], pref[0]))
        w, h = m.width, m.height
        for r in np.arange(r0, 2.4, .08):
            for dang in (0, 15, -15, 30, -30, 45, -45, 60, -60, 90, -90, 120, -120, 150, -150, 180):
                ang = np.radians(pref + dang)
                c = a + np.array([np.cos(ang) * (r + w / 2 * abs(np.cos(ang))), np.sin(ang) * (r + h / 2 * abs(np.sin(ang)))])
                if self.livre(c[0], c[1], w, h, extra):
                    m.move_to(P3(c))
                    if r > .8:
                        borda = c - np.array([np.cos(ang) * w / 2 * abs(np.cos(ang)), np.sin(ang) * h / 2 * abs(np.sin(ang))])
                        u = (borda - a) / np.linalg.norm(borda - a)
                        return VGroup(m, Line(P3(borda - .06 * u), P3(a + .05 * u)).set_stroke(guia_cor, 2, .85))
                    return VGroup(m)
        print('AVISO coloca: sem posição livre para', getattr(m, 'tex_string', None) or getattr(m, 'text', '?'))
        m.move_to(P3(a + r0 * np.array([np.cos(np.radians(pref)), np.sin(np.radians(pref))])))
        return VGroup(m)

    # ---------- transições de equação (QA do §B.8) ----------
    def toca(self, final, *anims, rt=1., y=None, nome=None):
        antes = set(self.mobjects)
        if nome is not None:
            n = int(np.ceil(rt * FPS))
            for p in (.3, .5, .7):
                self.capt[self.nq + int(round(p * n))] = {'transicao': nome, 'p': p, 'quadro': self.nq + int(round(p * n)), 'y': y}
            self.transicoes.append({'nome': nome, 'quadro0': self.nq, 'quadros': n, 'y': y})
        self.playr(*anims, run_time=max(rt * min(1., self.escala() * 1.25), .5))      # as transições de equação não acompanham a compressão inteira (legibilidade)
        for m in list(self.mobjects):
            if m not in antes:
                self.remove(m)
        self.add(final)

    def troca(self, A, B, anim, rt=1., nome=None):
        self.toca(B, anim, rt=rt, y=float(B.get_y()), nome=nome)
        self.remove(A)
        self.add(B)

    # ---------- minimapa do céu (C03 → C08) ----------
    def minimapa(self, D, rotulo=None):
        olho = np.array([3.62, 5.15])
        sol = olho + 1.7 * RT.dir_lado(EL)
        caixa = RoundedRectangle(width=2.45, height=2.1, corner_radius=.14).move_to([2.85, 5.9, 0])
        caixa.set_fill(BACKGROUND_COLOR, .88).set_stroke(DIM, 1.5, .7)
        caixa._moldura = True                             # desenho (moldura do minimapa), não caixa de texto (§B.2)
        g = VGroup(caixa, Line(P3(olho + [-1.0, -.12]), P3(olho + [.4, -.12])).set_stroke(DIM, 2),
                   Dot(P3(olho), .055, color=TEXT_COLOR), sol_icone(sol, .1),
                   tracejada(olho, sol - .2 * RT.dir_lado(EL), SOLC, 2, .7, .07))
        g[3]._sol = None
        if D is not None:
            C = olho + 1.45 * RT.dir_lado(EL + D)
            din = -RT.dir_lado(EL)
            g.add(Line(P3(C - .42 * din), P3(C)).set_stroke(SOLC, 2.5), Line(P3(C), P3(olho)).set_stroke(SOLC, 2.5),
                  RegularPolygon(6, radius=.07).move_to(P3(C)).set_stroke(CLARO, 2).set_fill(ICE, .3),
                  arco(olho, RT.dir_lado(EL), C - olho, .42, CYAN, 3.5))
        if rotulo:                                        # o número fica embaixo do quadro, nunca sobre o desenho
            g.add(T(rotulo, 22, CYAN).next_to(caixa, DOWN, .12))
        return g.set_z_index(46)

    def d_minimapa(self):
        if self.tq < E['prisma'] + .4:
            return 22.
        st = self.est()
        return None if st is None else st['D']

    # ---------- cristal de gelo em vetor (§B.5 v6): contorno firme + corpo, bisel, reflexos e brilhos ----------
    realce_extra = 0.

    def corpo_gelo(self, V, a, reflexos=True, brilhos=True, t=None):
        t = self.tq if t is None else t
        c = V.mean(axis=0)
        g = VGroup()
        corpo = Polygon(*[P3(v) for v in V]).set_stroke(width=0)
        corpo.set_fill([GELO_TOPO, GELO], .18 * a).set_sheen_direction(DOWN)     # gradiente vertical: mais claro em cima
        corpo._desenho = True
        R = float(np.linalg.norm(V[0] - c))
        k = max(R - .12 / np.cos(np.radians(30)), .05) / R
        Vi = c + k * (V - c)
        bisel = VGroup(Polygon(*[P3(v) for v in Vi]).set_stroke(GELO, 1.6, .35 * a).set_fill(opacity=0),
                       *[Line(P3(V[j]), P3(Vi[j])).set_stroke(GELO, 1.6, .35 * a) for j in range(6)])
        g.add(corpo, bisel)
        if reflexos:                                      # três faixas finas e diagonais que deslizam devagar
            ang = np.arctan2(*(V[0] - c)[::-1]) + np.radians(35)
            d = np.array([np.cos(ang), np.sin(ang)])
            nrm = np.array([-d[1], d[0]])
            for j, o in enumerate((-.42, .06, .38)):
                p0 = c + (o + .12 * np.sin(.45 * t + j)) * R * nrm
                seg = recorta(p0, d, Vi)
                if seg is None:
                    seg, o_ = (c, c + .01 * d), 0.
                else:
                    o_ = .10 * a
                g.add(Line(P3(seg[0]), P3(seg[1])).set_stroke(WHITE, 5 if j != 1 else 3, o_))
        if brilhos:                                       # um ponto de luz por vez nos vértices (loop de 3 s)
            j = int(t // 1.0) % 3
            f = (t % 1.0)
            al = np.sin(np.pi * f) ** 2 * a
            g.add(estrela(V[(2 * j + 1) % 6], .16 * (.6 + .4 * np.sin(np.pi * f)) + .01, al))
        return g

    def cristal_vetor(self, realce=None, ponta=False, rotulo_olho=False):
        st = self.est()
        g = VGroup()
        if st is None or st['alpha'] < .02 or st.get('caso') == 'lupa':
            return g
        a = st['alpha']
        V = F.hexagono(st['c'], st['R'], st['th'])
        g.add(self.corpo_gelo(V, a))
        cont = Polygon(*[P3(v) for v in V]).set_stroke(GELO, 4.5, .95 * a).set_fill(opacity=0)
        cont._qa = 'traco'
        g.add(cont)
        faces = realce if realce is not None else {'oposta': (2, 5), 'vizinha': (2, 3), 'alternada': (2, 4), 'gira': ()}.get(st['caso'], ())
        k = self.realce_extra * (.5 + .5 * np.cos(2 * PI * self.tq / .8)) if self.realce_extra else 0
        for f in faces:
            g.add(linha([V[f], V[(f + 1) % 6]], (CYAN if realce is None else WHITE) if k < .5 else CYAN, 6 + 6 * k, (.9 + .1 * k) * a, qa=False))
        fx = st['feixe']
        if fx is not None and fx['prog'] > 1e-3 and fx['alpha'] * a > .02:
            pts = np.array(fx['pts'])
            seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
            resta, corte = fx['prog'] * seg.sum(), [pts[0]]
            for i, l in enumerate(seg):
                if resta <= 0:
                    break
                fr = min(1., resta / l)
                corte.append(pts[i] + fr * (pts[i + 1] - pts[i]))
                resta -= l
            op = fx['alpha'] * a
            for i in range(len(corte) - 1):
                p, q = corte[i], corte[i + 1]
                dentro = F_dentro(V, (p + q) / 2)
                cor, w = (GELO_LUZ, 3.5) if dentro else (SOLC, 4.)
                o = op * (1 - .85 * i / max(1, len(corte) - 2) if (fx['fade_fim'] and i == len(corte) - 2) else 1)
                g.add(Line(P3(p), P3(q)).set_stroke(cor, 10, .18 * o))
                nuc = Line(P3(p), P3(q)).set_stroke(cor, w, o)
                nuc._qa = 'traco'
                if i == 0:
                    nuc._raio = {'ini': p, 'dir': RT.D_SOL, 'sol': st['sol'], 'R': RT.SOL_CR_R}
                g.add(nuc)
            if ponta and fx['prog'] > .99 and st['caso'] == 'alternada':
                d = (pts[-1] - pts[-2]) / np.linalg.norm(pts[-1] - pts[-2])
                g.add(Arrow(P3(pts[-1] - .45 * d), P3(pts[-1] + .1 * d), buff=0, stroke_width=4, color=SOLC,
                            max_tip_length_to_length_ratio=.45).set_opacity(op))
                if rotulo_olho:
                    nl = np.array([d[1], -d[0]])
                    g.add(VGroup(T('para o', 26, SOLC), T('seu olho', 26, SOLC)).arrange(DOWN, buff=.04).move_to([3.1, -2.3, 0]))
        if st.get('sol') is not None and (fx is not None or st['caso'] in ('gira', 'oposta')):
            s_ = sol_icone(st['sol'], RT.SOL_CR_R, a)
            s_._sol = {'c': np.asarray(st['sol'], float)[:2], 'R': RT.SOL_CR_R}
            g.add(s_)
            g.add(oculta([np.asarray(st['sol'], float)[:2] + 1.25 * RT.SOL_CR_R * np.array([np.cos(q), np.sin(q)]) for q in np.linspace(0, TAU, 25)]))
        fg = st['fantasma']
        if fg is not None and fg['alpha'] > .02:
            P = fg['pts']
            for p, q in zip(P[:-1], P[1:]):
                g.add(tracejada(p, q, CLARO, 3, fg['alpha'] * a, .1, qa=True))
                g.add(seta_chevron((p + q) / 2, q - p, CLARO, fg['alpha'] * a))
        return g.set_z_index(10)

    def cristal_peq(self, c, r, ang, a=1.):
        """Cristal pequeno do hook (o mesmo gelo do C05, sem reflexos)."""
        V = F.hexagono(c, r, ang)
        g = VGroup(self.corpo_gelo(V, a, reflexos=False, brilhos=False),
                   Polygon(*[P3(v) for v in V]).set_stroke(GELO, 2.6, .95 * a).set_fill(opacity=0))
        return g

    # ---------- gráfico desvio × ângulo de incidência ----------
    def grafico(self, origem=(-2.6, -3.5), xl=5.6, yl=2.55, marcas_y=(30, 40), legendas=True, numeros_x=True, x_ticks=(20, 40, 60, 80)):
        ax = Axes(x_range=[10, 90, 10], y_range=[20, 45, 5], x_length=xl, y_length=yl, tips=False,
                  axis_config={'stroke_color': DIM, 'stroke_width': 2.5, 'include_ticks': False})
        ax.shift(P3(origem) - ax.c2p(10, 20))
        marcas = VGroup()
        self.marcas_x = {}
        for x in x_ticks:
            p = ax.c2p(x, 20)
            marcas.add(Line(p, p + DOWN * .08).set_stroke(DIM, 1.5, .6))
            if numeros_x:
                self.marcas_x[x] = T(f'{x}°', 34, '#6E7F9E', piso=34).next_to(p, DOWN, .25)       # item 9.2: números afastados do eixo
                marcas.add(self.marcas_x[x])
        for y in marcas_y:
            p = ax.c2p(10, y)
            ty = T(f'{y}°', 34, TEXT_COLOR, piso=34).next_to(p, LEFT, .2)
            if y == 20:
                ty.shift(DOWN * .08)
            marcas.add(Line(p, p + LEFT * .1).set_stroke(DIM, 2), ty)
        g = VGroup(ax, marcas)
        if legendas:
            g.add(T('ângulo de incidência', 34, DIM, piso=34).next_to(ax.c2p(50, 20), DOWN, .8 if numeros_x else .16))
        g.add(T('desvio', 34, CYAN, piso=34).next_to(ax.c2p(10, 45), RIGHT, .15).shift(UP * .05))      # ao lado da ponta do eixo: em cima ele encostaria na equação do C08
        self.ax = ax
        ax.x_axis._qa = 'traco'
        return g.set_z_index(5)

    def curva(self, a, b, cor=CYAN, w=4.5):
        if b - a < .05:
            return VGroup()
        c = self.ax.plot(lambda x: float(F.desvio(x)), x_range=[a, b, .2]).set_stroke(cor, w).set_z_index(6)
        c._qa = 'traco'
        return c

    def ponto(self, x, cor=CYAN, op=1., r=.09):
        return Dot(self.ax.c2p(x, float(F.desvio(x))), r, color=cor).set_opacity(op).set_z_index(8)

    def leitura_min(self, x_min=IMIN, y=DMIN, rotulo='21,8°', cor=CYAN, dy=.07):
        p, e = self.ax.c2p(x_min, y), self.ax.c2p(self.ax.x_range[0], y)
        linha_h = DashedLine(p, e, dash_length=.08).set_stroke(cor, 2.5, .9).set_z_index(7)
        rot = T(rotulo, 30, cor, piso=30).next_to(e, LEFT, .14).shift(UP * dy)
        return VGroup(linha_h, rot)

    # ---------- equações: tempo parado (QA j/q) e caderno (§B.3 C06/C08) ----------
    def eq_entra(self, eq, nome):
        self.eq_vivas[id(eq)] = (nome, self.tq, eq)

    def eq_sai(self, eq):
        if id(eq) in self.eq_vivas:
            nome, t0, m = self.eq_vivas.pop(id(eq))
            self.eq_tempos.append({'equacao': nome, 'entra': round(t0, 2), 'sai': round(self.tq, 2), 'parada_s': round(self.tq - t0, 2),
                                   'posicao': [round(float(m.get_x()), 2), round(float(m.get_y()), 2)]})

    def troca_eq(self, A, B, anim, rt, nome, nome_b):
        self.eq_sai(A)
        self.troca(A, B, anim, rt=rt, nome=nome)
        self.eq_entra(B, nome_b)

    def para_caderno(self, eq, y, esc=.72, x0=-3.35, num=None):
        """Anima a equação encolhendo para a coluna do caderno (alinhada à esquerda em x0); devolve as animações."""
        w = eq.width * esc
        alvo = np.array([x0 + w / 2, y, 0])
        anims = [eq.animate.scale(esc).move_to(alvo)]
        if num is not None:
            n_ = T(str(num), 22, '#AEB9CC').move_to([-3.85, y, 0])
            self.numeros.append(n_)
            anims.append(FadeIn(n_))
        self.caderno.append({'eq': eq, 'y': y})
        return anims

    # ---------- cena de lado (C02, C03, C09): Sol redondo e inteiro; todo raio nasce no disco (§B.4) ----------
    def raio_do_sol(self, p_fim, op=.85, w=2.6, seta=True, sol=None, R=None, d=None):
        sol = RT.SOL_L if sol is None else np.asarray(sol, float)
        R = RT.SOL_LR if R is None else R
        d = RT.D_LUZ if d is None else np.asarray(d, float)
        ini = RT.ini_no_disco(p_fim, sol, R, d)
        r = Arrow(P3(ini), P3(p_fim), buff=0, stroke_width=w, color=SOLC, max_tip_length_to_length_ratio=.05,
                  max_stroke_width_to_length_ratio=10) if seta else Line(P3(ini), P3(p_fim)).set_stroke(SOLC, w)
        r.set_opacity(op)
        r._raio = {'ini': ini, 'dir': d, 'sol': sol, 'R': R}
        return r

    def cena_lado(self, phis=(DMIN,), n=26, seed=31):
        chao = VGroup(A.make_ground(RT.CHAO_Y, RT.CHAO_Y + 4.5, A.BLUE, 7, .09, 9.4),
                      Line([-4.7, RT.CHAO_Y, 0], [4.7, RT.CHAO_Y, 0], color=A.GEO, stroke_width=2.2, stroke_opacity=.9))
        chao._borda_ok = True
        for f in chao.get_family():
            f._desenho = True
        pessoa = A.make_person_espelhada([RT.OLHO_M[0], RT.CHAO_Y], 1.5).set_z_index(20)
        assert np.linalg.norm(pessoa.eye_point[:2] - RT.OLHO_M) < 1e-9
        sol = sol_redondo(RT.SOL_L, RT.SOL_LR).set_z_index(9)
        sol_l = VGroup(T('Sol', 41, SOLC), T('muito longe:', 33, SOLC), T('raios paralelos', 33, SOLC))
        sol_l.arrange(DOWN, buff=.1, aligned_edge=LEFT).move_to([0, 5.45, 0]).align_to([.45, 0, 0], LEFT)
        if sol_l.width > 4.15 - .45:
            sol_l.scale((4.15 - .45) / sol_l.width).align_to([.45, 0, 0], LEFT)
        voce = T('você', 22).move_to([RT.OLHO_M[0] + .75, RT.CHAO_Y + .28, 0])
        nuvem = self.nuvem_lado(n, seed, phis_fora=phis)
        nuvem[0]._borda_ok = True
        crs = {p: self.cristal_lado(p) for p in phis}
        return dict(chao=chao, pessoa=pessoa, sol=sol, sol_l=sol_l, voce=voce, nuvem=nuvem, crs=crs)

    def nuvem_lado(self, n=26, seed=31, phis_fora=()):
        rng = np.random.default_rng(seed)
        y0 = RT.NUVEM_Y
        faixa = RoundedRectangle(width=9.4, height=.8, corner_radius=.4).move_to([0, y0, 0])
        faixa.set_fill(WHITE, .06).set_stroke(WHITE, 0)
        faixa._desenho = True
        hexs = VGroup()
        for k in range(n):
            x = -3.95 + 7.9 * (k + rng.uniform(.15, .85)) / n
            if any(abs(x - RT.cristal_lado(p)[0]) < .2 for p in phis_fora):
                continue
            hexs.add(RegularPolygon(6, radius=.065, start_angle=rng.uniform(0, PI)).move_to([x, y0 + rng.uniform(-.25, .25), 0])
                     .set_stroke(ICE, 1.5, .55).set_fill(ICE, .08))
        return VGroup(faixa, hexs).set_z_index(3)

    def cristal_lado(self, phi, r=.15, cor=CLARO):
        return RegularPolygon(6, radius=r, start_angle=PI / 6).move_to(P3(RT.cristal_lado(phi))).set_stroke(cor, 3).set_fill(ICE, .25).set_z_index(8)

    def raio_lado(self, phi, D=None, op=1., ate_chao=False, w=4.5):
        """Raio que nasce no disco do Sol, chega ao cristal a phi do Sol e sai desviado de D (rumo ao lado do olho)."""
        C = RT.cristal_lado(phi)
        assert abs(F.angulo_no_olho(RT.dir_lado(RT.EL_LADO), RT.OLHO_M, C) - phi) < 1e-6
        din = RT.D_LUZ
        ini = RT.ini_no_disco(C)
        D = phi if D is None else D
        e = RT.OLHO_M - C
        s = np.sign(din[0] * e[1] - din[1] * e[0])
        a = np.radians(s * D)
        dout = np.array([din[0] * np.cos(a) - din[1] * np.sin(a), din[0] * np.sin(a) + din[1] * np.cos(a)])
        if abs(D - phi) < 1e-9:
            assert np.degrees(np.arccos(np.clip(dout @ e / np.linalg.norm(e), -1, 1))) < 1e-6
        fim = C + (C[1] - RT.CHAO_Y) / -dout[1] * dout if ate_chao else RT.OLHO_M.copy()
        g = luz([ini, C, fim], SOLC, w, op)
        g[1]._raio = {'ini': ini, 'dir': din, 'sol': RT.SOL_L, 'R': RT.SOL_LR}
        seta = Arrow(P3(fim - .4 * dout), P3(fim), buff=0, stroke_width=w, color=SOLC, max_tip_length_to_length_ratio=.4).set_opacity(op)
        g.add(seta)
        return g, C, din, dout

    def tracejada_sol(self, olho=None):
        olho = RT.OLHO_M if olho is None else olho
        m = tracejada(olho, RT.SOL_L, SOLC, 2.5, .8, qa=True)
        return m

    def dial(self):
        st = self.est()
        t = self.tq
        if st is None or not (E['giro_ini'] - .3 <= t <= E['giro_fim']):
            return VGroup()
        c, R = st['c'], st['R']
        th = np.radians(st['th'])
        a = Arc(radius=R + .35, start_angle=th + PI / 3, angle=PI / 2.6, arc_center=P3(c)).set_stroke(DIM, 4)
        a.add_tip(tip_length=.2)
        a.set_fill(opacity=0, family=False)
        a.tip.set_fill(DIM, 1).set_stroke(DIM, 1)
        txt = T('girando o cristal', 22, DIM).move_to([-2.3, 6.35, 0])
        return VGroup(a, txt).set_z_index(30)

    # ---------- o cone saindo da pessoa (C09, §B.2 v7; modelo: c10 do vid_0025, com o eixo no Sol) ----------
    N_CONE, H_CONE, L_CONE = 48, 2.55, 3.8                  # linhas de visão (≥ 36) · altura do olho (pessoa ≈ 17 % da tela) · comprimento do cone

    def cone_s(self, t):
        return float(RT.suave((t - E['cone_frente']) / (E['ceu_volta'] - E['cone_frente'])))

    def cone_desenho(self):
        t = self.tq
        s = self.cone_s(t)
        sai = 1 - float(RT.suave((t - E['ceu_volta'] - .1) / .5))               # cruza com o céu do 3D (corte casado)
        dcone = E['cone_frente'] - E['cone']
        cresce = float(RT.suave((t - E['cone']) / (.25 * dcone)))
        H = (1 - s) * (1.5 + (self.H_CONE - 1.5) * cresce) + s * 1.1
        pe = (1 - s) * np.array([RT.OLHO_M[0], RT.CHAO_Y]) + s * np.array([0., -4.35])
        E_ = pe + np.array([0., H])                                               # o olho: vértice do cone
        olho0 = np.array([RT.OLHO_M[0], RT.CHAO_Y + self.H_CONE])
        a = (RT.SOL_L - olho0) / np.linalg.norm(RT.SOL_L - olho0)                # eixo: olho → centro do Sol
        nrm = np.array([-a[1], a[0]])
        rho = self.L_CONE * np.tan(np.radians(DMIN))
        Cs = olho0 + self.L_CONE * a
        sol_c = (1 - s) * RT.SOL_L + s * np.asarray(SOL[:2])
        sol_R = (1 - s) * RT.SOL_LR + s * .32

        def anel(tt):
            lado = Cs + rho * np.cos(tt) * nrm + .24 * rho * np.sin(tt) * a
            frente = np.asarray(SOL[:2]) + RAIO22(tt)
            return (1 - s) * lado + s * frente
        varre = float(np.clip((t - E['cone'] - .25 * dcone) / (.6 * dcone), 0, 1)) * TAU
        g = VGroup()
        g.add(sol_redondo(sol_c, sol_R, op=1.))
        n_lin = 0
        if varre > 1e-3:
            M_ = 96
            op_f = .09 * (1 - .7 * s) * sai
            for k in range(M_):                                                   # superfície entre as linhas: ciano translúcido (18 % onde cobre duas vezes)
                t0, t1 = TAU * k / M_, TAU * (k + 1) / M_
                if t1 <= varre:
                    tri_ = Polygon(P3(E_), P3(anel(t0)), P3(anel(t1))).set_fill(CYAN, op_f).set_stroke(width=0)
                    tri_._desenho = True
                    g.add(tri_)
            tts = np.linspace(0, varre, max(2, int(varre / TAU * 160)))
            borda = VMobject().set_points_as_corners([P3(anel(x)) for x in tts]).set_stroke(CYAN, 2.6, .95 * sai)
            borda._qa = 'traco'
            g.add(borda)
            for k in range(self.N_CONE):
                tk = TAU * k / self.N_CONE
                if tk <= varre + 1e-9:
                    p = anel(tk)
                    g.add(Line(P3(E_), P3(p)).set_stroke(CYAN, 1.8, .7 * sai * (1 - .3 * s)))
                    cr_ = RegularPolygon(6, radius=.11, start_angle=PI / 6).move_to(P3(p)).set_stroke(GELO, 2, .95 * sai).set_fill(ICE, .35 * sai)
                    cr_._desenho = True
                    g.add(cr_)
                    n_lin += 1
        eixo = DashedLine(P3(E_), P3(sol_c - sol_R * (sol_c - E_) / np.linalg.norm(sol_c - E_)), dash_length=.12)
        eixo.set_stroke(SOLC, 2.6, .9 * sai * cresce)
        g.add(eixo)
        pessoa = A.make_person_espelhada(list(pe), H).set_opacity(sai)
        pessoa._cone_pessoa = True
        g.add(pessoa)
        halo_o = Circle(radius=.17 + .03 * np.sin(8 * t), arc_center=P3(E_)).set_stroke(CYAN, 2.2, .7 * sai).set_fill(opacity=0)
        halo_o._desenho = True
        g.add(halo_o, Dot(P3(E_), .075, color=CYAN).set_opacity(sai))
        self.cone_info[self.nq] = {'quadro': self.nq, 'linhas': n_lin, 'olho': E_.round(4).tolist(), 's': round(s, 4),
                                   'sol': np.asarray(sol_c).round(4).tolist(), 'H': round(float(H), 3)}
        return g.set_z_index(25)

    def construct(self):
        self.events, self.geometria, self.transicoes, self._est = [], [], [], {}
        self.eq_vivas, self.eq_tempos, self.caderno, self.numeros, self.chegada = {}, [], [], [], {}
        self.add(Mobject().add_updater(lambda m, dt: None))   # garante quadros novos nos waits

        tag = screen_text('DA EQUAÇÃO AO FENÔMENO · EP. 09', 20, oversample=2).set_opacity(.75)
        tag.to_corner(UP + LEFT, buff=.4).set_z_index(60)
        logo = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(.35).to_corner(UP + RIGHT, buff=.28)
        tag._qa_isento = True
        self.add(tag, logo)

        # ══ C01 — hook: o halo solar, a pergunta e os cristais ═══════════════════════════════════════════════════
        t1 = T('halo solar de 22°', 50, WHITE)
        t2 = T('como ele se forma?', 33, WHITE)
        titulo = VGroup(t1, t2).arrange(DOWN, buff=.3).move_to([0, 6.2, 0]).align_to([0, 6.95, 0], UP)
        sombra_t = sombra_ceu(titulo)
        self.at('titulo')
        self.play(FadeIn(sombra_t), FadeIn(titulo, shift=DOWN * .1), run_time=.4)
        self.mark('C01_halo')

        def hook():
            t = self.tq
            esc, tr = RT.cam_hook(t)
            g = VGroup()
            for k, ang in enumerate(RT.ANG_HOOK):
                t0 = E['brilhos'] + min(.8, (E['aviso'] - E['brilhos'] - .6) / 5) * k
                if t < t0:
                    continue
                p = tr + esc * RT.manim_de_dir(RT._no_cone(RT.SOL_DIR, DMIN + .25, ang))
                u_st = float(np.clip((t - t0) / .35, 0, 1))
                u_cr = float(np.clip((t - t0 - .3) / .4, 0, 1))
                if u_cr < 1:
                    g.add(estrela(p, .28 * np.sin(np.pi * min(u_st, 1) * .5 + np.pi * .5 * u_cr) + .02, 1 - u_cr))
                if u_cr > 0:
                    g.add(self.cristal_peq(p, .24 * esc, 20 * k + 9 * t, u_cr))
            if t >= E['raio_hook']:                                      # raio dourado: Sol → cristal → desviado
                p = tr + esc * RT.manim_de_dir(RT._no_cone(RT.SOL_DIR, DMIN + .25, RT.ANG_HOOK[0]))
                s0 = tr + esc * np.asarray(SOL[:2])
                d = (p - s0) / np.linalg.norm(p - s0)
                u1 = float(np.clip((t - E['raio_hook']) / .6, 0, 1))
                u2 = float(np.clip((t - E['raio_hook'] - .6) / .7, 0, 1))
                ini = s0 + .3 * esc * d
                g.add(luz([ini, ini + u1 * (p - ini)], SOLC, 4, 1))
                if u2 > 0:
                    a = np.radians(-DMIN)
                    dout = np.array([d[0] * np.cos(a) - d[1] * np.sin(a), d[0] * np.sin(a) + d[1] * np.cos(a)])
                    fim = p + u2 * 2.2 * dout
                    g.add(luz([p, fim], SOLC, 4, 1))
                    if u2 > .2:
                        g.add(Arrow(P3(fim - .35 * dout), P3(fim + .05 * dout), buff=0, stroke_width=4, color=SOLC,
                                    max_tip_length_to_length_ratio=.45))
            return g.set_z_index(30)
        hk = redesenha(hook)
        self.add(hk)
        self.untilr('brilhos', +4.0)
        self.mark('C01_cristais')
        aviso = VGroup(T('nunca olhe direto', 46, WHITE), T('para o Sol', 46, WHITE)).arrange(DOWN, buff=.05).move_to([0, -3.55, 0])
        self.at('aviso')
        self.play(FadeIn(aviso, shift=UP * .1), run_time=.4)
        self.untilr('raio_hook', +1.5)
        self.mark('C01_raio')
        self.untilr('mergulho', -.5)                             # item 2.7: o título sai com o aviso, antes do corte para o C02
        self.play(FadeOut(VGroup(aviso, titulo, sombra_t)), run_time=.3)
        self.at('mergulho')

        # ══ C02 — a cena de lado: o raio já entrando no cristal; a pessoa entra por último ════════════════════════════
        L = self.cena_lado()
        C22 = RT.cristal_lado(DMIN)
        raio22, _, din22, dout22 = self.raio_lado(DMIN)
        raio22.set_z_index(10)
        ini22 = RT.ini_no_disco(C22)
        entra = luz([ini22, C22], SOLC, 4.5, 1)
        entra[1]._raio = {'ini': ini22, 'dir': din22, 'sol': RT.SOL_L, 'R': RT.SOL_LR}
        self.untilr('c02', -.25)
        self.play(FadeOut(hk), FadeIn(L['sol']), FadeIn(L['sol_l']), FadeIn(L['nuvem']), FadeIn(L['crs'][DMIN], scale=1.6),
                  FadeIn(entra), run_time=.5)
        hk.clear_updaters()
        self.remove(hk)
        sai22 = luz([C22, RT.OLHO_M], SOLC, 4.5, 1).set_z_index(10)
        self.play(Create(sai22), run_time=1.0, rate_func=linear)
        self.mark('C02_raio_no_cristal')
        st = self.est(E['lupa'] + .6)
        lupa = Circle(radius=1.12, arc_center=P3(st['c'])).set_stroke(CLARO, 2.5, .9).set_z_index(2)
        lig = DashedLine(P3(C22), P3(st['c']) + 1.12 * normalize(P3(C22) - P3(st['c'])), dash_length=.08).set_stroke(CLARO, 2, .8)
        l_cr = T('cristal de gelo', 22, CLARO).next_to(lupa, DOWN, .16)
        self.at('lupa')
        self.play(FadeIn(lupa), Create(lig), FadeIn(l_cr), run_time=.5)
        self.untilr('lupa', +1.6)
        self.mark('C02_lupa')
        self.at('lupa_sai')
        self.play(FadeOut(VGroup(lupa, lig, l_cr)), run_time=.4)
        seta_olho = Arrow(P3(RT.OLHO_M - .4 * dout22), P3(RT.OLHO_M), buff=0, stroke_width=4.5, color=SOLC,
                          max_tip_length_to_length_ratio=.4).set_z_index(11)
        self.at('pessoa')
        self.play(FadeIn(L['chao']), FadeIn(L['pessoa'], shift=UP * .15), FadeIn(L['voce']), FadeIn(seta_olho), run_time=.8)
        self.mark('C02_pessoa')
        t_c = float((C22 - RT.SOL_L) @ RT.N_LUZ)
        paral = VGroup()
        for t in (-1.3, -.65, .55, 1.25):
            if abs(t - t_c) < .3:
                continue
            p0 = RT.SOL_L + t * RT.N_LUZ
            fim = p0 + (RT.NUVEM_Y + .45 - p0[1]) / RT.D_LUZ[1] * RT.D_LUZ
            paral.add(self.raio_do_sol(fim, op=.8))
        paral.set_z_index(7)
        self.at('paralelas')
        self.play(LaggedStart(*[GrowArrow(r) for r in paral], lag_ratio=.15), run_time=1.0)
        self.mark('C02_paralelas')
        l_os = self.tracejada_sol()

        def marcas_par(p, d):
            q = np.array([-d[1], d[0]]) * .13
            return VGroup(*[Line(P3(p + s * .09 * d - q), P3(p + s * .09 * d + q)) for s in (-1, 1)]).set_stroke(SOLC, 3)
        mpar = VGroup(marcas_par(RT.OLHO_M + 2.2 * RT.dir_lado(RT.EL_LADO), din22), marcas_par(C22 - 1.1 * din22, din22)).set_z_index(12)
        cont = tracejada(C22, C22 + 1.0 * din22, SOLC, 2.5, .8)
        aD = arco(C22, din22, dout22, .62, CYAN, 5)
        aO = arco(RT.OLHO_M, RT.dir_lado(RT.EL_LADO), C22 - RT.OLHO_M, 1.0, CYAN, 5)
        self.at('lado_arcos')
        self.play(Create(l_os), FadeIn(mpar), Create(cont), Create(aD), Create(aO), run_time=.8)
        lD = self.coloca(M('D', 52, CYAN), meio_arco(C22, din22, dout22, .62), bissetriz(din22, dout22), r0=.12)
        self.play(FadeIn(lD), Indicate(aO, color=CYAN, scale_factor=1.06), Indicate(aD, color=CYAN, scale_factor=1.06), run_time=.8)
        self.mark('C02_arcos')
        frase = VGroup(T('ângulo no olho', 24, CYAN), T('= desvio no cristal', 24, CYAN)).arrange(DOWN, buff=.14).move_to([2.3, -.9, 0])
        self.at('igual')
        self.play(FadeIn(frase, shift=UP * .1), Indicate(aO, color=CYAN, scale_factor=1.06), Indicate(aD, color=CYAN, scale_factor=1.06),
                  run_time=.9)
        self.mark('C02_igual')
        l22 = self.coloca(T('22°', 32, CYAN), meio_arco(RT.OLHO_M, RT.dir_lado(RT.EL_LADO), C22 - RT.OLHO_M, 1.0),
                          bissetriz(RT.dir_lado(RT.EL_LADO), C22 - RT.OLHO_M), r0=.15)
        self.at('n22')
        self.play(FadeIn(l22, scale=.8), Indicate(aO, color=CYAN, scale_factor=1.08), L['crs'][DMIN].animate.set_stroke(SOLC, 3.5).set_fill(SOLC, .5),
                  run_time=.8)
        self.mark('C02_22')

        # ══ C03 — comparação com o arco-íris: a mesma pessoa vira ═════════════════════════════════════════════
        halo_els = VGroup(L['sol_l'], L['nuvem'], L['crs'][DMIN], paral, entra, sai22, seta_olho, l_os, mpar, cont, aD, aO, lD, l22, frase)
        E_ = np.array([*RT.OLHO_M, 0.])
        h_ai = np.radians(34.)
        a_ = np.array([np.cos(h_ai), -np.sin(h_ai), 0.])
        R_AI = 1.3
        sol_ai_c = E_ - 3.4 * a_
        L_ = (RT.OLHO_M[1] - RT.CHAO_Y) / np.sin(h_ai)
        A_ = E_ + L_ * a_                                    # sombra da cabeça no chão
        u_ = np.array([np.sin(h_ai), np.cos(h_ai), 0.])
        Tlong = A_ + L_ * np.tan(np.radians(42.078107)) * u_
        T_ = E_ + 2.9 * normalize(Tlong - E_)
        assert abs(np.degrees(np.arccos(np.dot(normalize(A_ - E_), normalize(T_ - E_)))) - 42.078107) < 1e-6
        p_ai = A.make_person([RT.OLHO_M[0], RT.CHAO_Y], 1.5).set_z_index(20)
        sol_ai = sol_redondo(sol_ai_c[:2], R_AI).set_z_index(9)
        d_ai = a_[:2]
        raios_ai = VGroup(*[self.raio_do_sol(sol_ai_c[:2] + o * np.array([-d_ai[1], d_ai[0]]) + 2.4 * d_ai, sol=sol_ai_c[:2], R=R_AI, d=d_ai)
                            for o in (.75, -.7)])
        ini_cab = RT.ini_no_disco(A_[:2], sol_ai_c[:2], R_AI, d_ai)
        raio_cab = Line(P3(ini_cab), A_).set_stroke(SOLC, 3, .9)
        raio_cab._raio = {'ini': ini_cab, 'dir': d_ai, 'sol': sol_ai_c[:2], 'R': R_AI}
        sombra = Circle(radius=.12, color=TEXT_COLOR, stroke_width=2, fill_color=TEXT_COLOR, fill_opacity=.3).move_to(A_)
        eixo_as = DashedLine(E_, A_, dash_length=.1).set_stroke(TEXT_COLOR, 2.5, .8)
        eixo_as._qa = 'traco'
        l_sombra = T('sua sombra', 20)
        a42 = arco(E_, A_ - E_, T_ - E_, 1.2, CYAN, 5.5)
        visada = Line(E_, T_, color=CYAN, stroke_width=2.6)
        visada._qa = 'traco'
        nT = normalize(np.array([-(T_ - E_)[1], (T_ - E_)[0], 0.]))
        arco_iris = VGroup(*[Line(T_ - .75 * nT + (k - 2.5) * .085 * normalize(T_ - E_), T_ + .75 * nT + (k - 2.5) * .085 * normalize(T_ - E_))
                             .set_stroke(col, 6.5) for k, col in enumerate(["#9B5CFF", "#3CA4FF", "#4BE07D", "#FFE24B", "#FFA03C", "#FF4B4B"])])
        gota = A.make_drop(T_ + 1.0 * nT, .13, A.BLUE_L, .95)
        lbl_a = T('arco-íris: Sol nas costas · gota de água', 22, A.BLUE_L).move_to([0, 4.9, 0])
        self.at('c03')
        self.play(FadeOut(halo_els), Transform(L['pessoa'], p_ai), Transform(L['sol'], sol_ai), run_time=.5)     # item 2.6: a C02 sai antes do rótulo do C03
        self.play(FadeIn(lbl_a), run_time=.3)
        self.remove(L['pessoa'], L['sol'])
        self.add(p_ai, sol_ai)
        self.play(*[GrowArrow(r) for r in raios_ai], Create(raio_cab), run_time=.5)
        self.at('ai_sombra')
        self.play(FadeIn(sombra, scale=.5), Create(eixo_as), run_time=.5)
        futuros3 = VGroup(oculta([E_[:2], T_[:2]]), oculta(np.asarray(a42.get_anchors())[:, :2]))
        self.add(futuros3)
        l_sombra.become(self.coloca(T('sua sombra', 20), A_[:2], np.array([-1., .7]), r0=.3)[0])
        self.remove(futuros3)
        self.play(FadeIn(l_sombra), run_time=.3)
        self.at('ai_42')
        self.play(Create(visada), Create(a42), FadeIn(arco_iris), FadeIn(gota), run_time=.7)
        l42 = self.coloca(T('42°', 36, CYAN), meio_arco(E_, A_ - E_, T_ - E_, 1.2), bissetriz(A_ - E_, T_ - E_), r0=.12)
        self.play(FadeIn(l42), run_time=.3)
        self.mark('C03_arco_iris')
        p_h = A.make_person_espelhada([RT.OLHO_M[0], RT.CHAO_Y], 1.5).set_z_index(20)
        sol_h = sol_redondo(RT.SOL_L, RT.SOL_LR).set_z_index(9)
        ai_els = VGroup(lbl_a, raios_ai, raio_cab, sombra, eixo_as, l_sombra, a42, visada, arco_iris, gota, l42)
        volta = VGroup(L['nuvem'], L['crs'][DMIN], entra, sai22, seta_olho, l_os, mpar, aO, aD)
        self.at('vira')
        self.play(FadeOut(ai_els), run_time=.3)
        self.play(Transform(p_ai, p_h), Transform(sol_ai, sol_h), run_time=.7)
        self.remove(p_ai, sol_ai)
        self.add(p_h, sol_h)
        self.mark('C03_vira')
        self.play(FadeIn(volta), run_time=.8)
        lbl_h = VGroup(T('halo:', 26, CYAN), T('olhando', 26, CYAN), T('para o Sol', 26, CYAN), T('cristal', 26, CYAN), T('de gelo', 26, CYAN)).arrange(DOWN, buff=.08, aligned_edge=LEFT)
        lbl_h.move_to([2.9, .3, 0])
        self.at('halo_lbl')
        self.play(FadeIn(lbl_h, shift=UP * .1), run_time=.5)
        self.mark('C03_halo')

        # ══ C04 — onde ver: calor no chão, gelo no alto (textos sem caixa) ═══════════════════════════════════════
        self.at('c04')                                          # corte direto: tudo sai enquanto o céu do 3D entra; o Sol encolhe (a cor não muda)
        self.play(FadeOut(VGroup(L['chao'], L['voce'], p_h, volta, lbl_h)), sol_h.animate.scale(.05), run_time=.35)
        self.remove(sol_h)

        def termometro():
            u = float(np.clip((self.tq - E['c04'] - .4) / 3.2, 0, 1))
            cor = interpolate_color(ManimColor('#FF6A3D'), ManimColor('#7FD0FF'), u)
            tubo = RoundedRectangle(width=.42, height=5.2, corner_radius=.21).move_to([-3.75, .5, 0]).set_stroke(TEXT_COLOR, 2.5, .8)
            tubo._desenho = True
            nivel = RoundedRectangle(width=.24, height=.4 + 4.3 * (1 - u), corner_radius=.12).set_fill(cor, .95).set_stroke(width=0)
            nivel.align_to(tubo, DOWN).shift(UP * .09).set_x(-3.75)
            nivel._desenho = True
            bulbo = Circle(radius=.36, arc_center=[-3.75, -2.25, 0]).set_fill(cor, .95).set_stroke(TEXT_COLOR, 2.5, .8)
            return VGroup(tubo, nivel, bulbo).set_z_index(40)
        termo = redesenha(termometro)
        selo_v = T('aqui: verão', 28, '#FFC08A').move_to([.4, -3.5, 0])
        selo_f = T('lá em cima: abaixo de zero', 28, WHITE).move_to([.4, .15, 0])      # item 2.4: abaixo da faixa dos cristais (y < 0,5)
        self.add(termo)
        self.at('selo_verao')
        self.play(FadeIn(selo_v), run_time=.5)
        self.at('verao_sai')                                   # sai antes de a câmera passar do horizonte e de o anel aparecer
        self.play(FadeOut(selo_v), run_time=.3)
        self.at('selo_frio')
        self.play(FadeIn(selo_f), run_time=.5)
        self.untilr('globo', -1.1)
        self.mark('C04_frio')
        self.untilr('globo', -.5)
        termo.clear_updaters()
        self.play(FadeOut(VGroup(termo, selo_f)), run_time=.4)
        GC, GR, lat0 = np.array([0., .6, 0]), 3.5, np.radians(-12.)
        AS = [(-77, 8), (-72, 12), (-63, 11), (-60, 8), (-52, 5), (-50, 0), (-44, -2), (-35, -5), (-35, -9), (-39, -14), (-39, -18),
              (-41, -22), (-48, -26), (-53, -33), (-57, -36), (-62, -39), (-65, -42), (-66, -47), (-68, -51), (-70, -54), (-74, -52),
              (-74, -46), (-73, -40), (-71, -30), (-70, -20), (-75, -15), (-80, -7), (-81, -3), (-80, 1), (-78, 4)]
        ICONES = [(-47, -15), (-70, -35), (-30, 10), (-90, 15), (-60, -55), (-50, 62), (-90, 55), (-40, -68), (-110, 30), (-20, -30)]

        def ortho(lon, lat, lon0):
            lon, lat = np.radians(lon), np.radians(lat)
            x = np.cos(lat) * np.sin(lon - lon0)
            y = np.cos(lat0) * np.sin(lat) - np.sin(lat0) * np.cos(lat) * np.cos(lon - lon0)
            vis = np.sin(lat0) * np.sin(lat) + np.cos(lat0) * np.cos(lat) * np.cos(lon - lon0)
            return GC + GR * np.array([x, y, 0.]), vis

        def globo():
            u = float(np.clip((self.tq - E['globo']) / 1.8, 0, 1))
            lon0 = np.radians(-140 + 85 * (u * u * (3 - 2 * u)))
            g = VGroup(Circle(radius=GR, arc_center=GC).set_fill('#0E2A52', .97).set_stroke(CLARO, 2.5, .85))
            for lat in range(-60, 61, 30):
                seg = [p for p, v in (ortho(lo, lat, lon0) for lo in range(-180, 181, 4)) if v > 0]
                if len(seg) > 1:
                    g.add(VMobject().set_points_as_corners(seg).set_stroke(CLARO, 1.2, .3))
            for lo in range(-180, 180, 30):
                seg = [p for p, v in (ortho(lo, la, lon0) for la in range(-90, 91, 4)) if v > 0]
                if len(seg) > 1:
                    g.add(VMobject().set_points_as_corners(seg).set_stroke(CLARO, 1.2, .3))
            pts = [ortho(lo, la, lon0) for lo, la in AS]
            if all(v > 0 for _, v in pts):
                g.add(Polygon(*[p for p, _ in pts]).set_fill('#3E9B7A', .8).set_stroke('#7FD6B0', 2, .9))
            ki = float(np.clip((self.tq - E['icones']) / .8, 0, 1))
            kb = float(np.clip((self.tq - E['brasil']) / .5, 0, 1))
            for j, (lo, la) in enumerate(ICONES):
                p, v = ortho(lo, la, lon0)
                if v > .05 and ki > 0:
                    r = .09 * (1 + .9 * kb * (.75 + .25 * np.sin(6 * self.tq))) if j == 0 else .085
                    g.add(Circle(radius=r, arc_center=p).set_stroke('#FFF1C9', 2.4, ki * v ** .5),
                          Dot(p, .025, color='#FFF1C9').set_opacity(ki * v ** .5))
            for m in g:
                m._desenho = True
            return g.set_z_index(30)
        glb = redesenha(globo)
        self.at('globo')
        self.add(glb)
        l_br = T('Brasil', 22, '#FFF1C9')
        self.at('icones')
        self.until(E['brasil'])
        p_br, _ = ortho(-47, -15, np.radians(-55))
        l_br.next_to(P3(p_br), RIGHT, .25).set_z_index(41)
        self.play(FadeIn(l_br), run_time=.6)
        self.untilr('brasil', +1.2)
        self.mark('C04_globo')
        self.untilr('prisma', -.5)
        glb.clear_updaters()
        self.play(FadeOut(VGroup(glb, l_br)), run_time=.45)

        # ══ C05 — o prisma escondido: hexágono grande; o feixe entra pelo meio de uma face; a lista fica embaixo ════════
        cristal = redesenha(lambda: self.cristal_vetor(ponta=True, rotulo_olho=E['olho'] <= self.tq < E['equacao'] - .5))
        minimapa = redesenha(lambda: self.minimapa(self.d_minimapa()))
        self.add(cristal, minimapa)
        self.mark('C05_inicio')
        self.at('feixe_op')
        self.untilr('feixe_op', +1.0)
        st = self.est()
        pts = st['feixe']['pts']
        l_op = VGroup(T('passa', 26), T('reto', 26)).arrange(DOWN, buff=.04)
        l_op.move_to([3.1, -2.3, 0])                                                            # fora do gelo, embaixo da face de saída
        l_op = VGroup(l_op, Line(P3([3.4, -1.85]), P3(pts[2]) + .08 * DOWN).set_stroke(DIM, 2, .85))
        self.play(FadeIn(l_op), run_time=.3)
        self.mark('C05_oposta')
        self.untilr('rot_vz', -.45)
        self.play(FadeOut(l_op), run_time=.35)
        self.at('rot_vz')
        self.untilr('feixe_vz', +.75)
        st = self.est(E['feixe_vz'] + 1.5)
        pts = st['feixe']['pts']
        self.play(Flash(P3(pts[2]), color=WHITE, line_length=.3, flash_radius=.3), run_time=.6)
        self.untilr('feixe_vz', +1.45)
        l_vz = T('reflexão total', 26)
        l_vz.move_to([1.0, -2.3, 0])                                                         # fora do gelo, embaixo, com seta-guia até a face
        guia = Line(P3(l_vz.get_right() + RIGHT * .08 + UP * .1), P3(pts[2]) + .08 * DOWN).set_stroke(DIM, 2, .85)
        l_vz = VGroup(l_vz, guia)
        self.play(FadeIn(l_vz), run_time=.3)
        self.mark('C05_vizinha')
        self.untilr('rot_al', -.45)
        self.play(FadeOut(l_vz), run_time=.35)
        self.at('rot_al')
        self.untilr('olho', +.4)
        self.mark('C05_alternada_olho')
        st = self.est(E['prolonga'] + .5)
        V = F.hexagono(st['c'], st['R'], st['th'])
        apice = cruza(V[2], V[3] - V[2], V[5], V[4] - V[5])
        ext = VGroup(tracejada(V[3], apice, CLARO, 3.5, .95, .1), tracejada(V[4], apice, CLARO, 3.5, .95, .1)).set_z_index(12)
        self.at('prolonga')
        self.play(Create(ext), run_time=.7)
        a60 = arco(apice, V[3] - apice, V[4] - apice, .75, CYAN, 6).set_z_index(12)
        l60 = T('60°', 34, CYAN).move_to(P3((apice + V[3] + V[4]) / 3))
        self.at('arco60')
        self.play(Create(a60), FadeIn(l60), run_time=.6)
        self.mark('C05_60')
        tri = Polygon(P3(apice), P3(V[2]), P3(V[5])).set_stroke(CYAN, 3, .9).set_fill(CYAN, .0).set_z_index(9)
        tri._desenho = True
        self.at('pulso')
        self.mark('C05_prisma')
        self.play(tri.animate.set_fill(CYAN, .18), run_time=.3)
        self.play(tri.animate.set_fill(CYAN, 0).set_stroke(opacity=0), run_time=.3)
        self.untilr('pulso', +.7)
        self.play(FadeOut(VGroup(ext, a60, l60, tri)), run_time=.3)

        # ══ C06 — a equação nasce, com o caderno na metade de baixo ═════════════════════════════════════════════
        st = self.est(E['b1_i1'])
        tr = st['tr']
        V, (_, P1, P2), d_in, d_out = tr['V'], tr['pontos'], tr['d_in'], tr['d_final']
        N2, N4 = F.normal_face(2, tr['theta']), F.normal_face(4, tr['theta'])
        w = (P2 - P1) / np.linalg.norm(P2 - P1)
        RA = .85
        nrm1 = tracejada(P1 - 1.4 * N2, P1 + 1.4 * N2, TEXT_COLOR, 2.6, .7, qa=True).set_z_index(11)
        nrm2 = tracejada(P2 - 1.4 * N4, P2 + 1.4 * N4, TEXT_COLOR, 2.6, .7, qa=True).set_z_index(11)
        ai1, ar1 = arco(P1, N2, -d_in, RA, VIOLET, 5.5), arco(P1, -N2, w, RA, MAG, 5.5)
        ai2, ar2 = arco(P2, N4, d_out, RA, VIOLET, 5.5), arco(P2, -N4, -w, RA, MAG, 5.5)
        YA, YB, YC = -1.75, -2.95, -3.2                       # linhas grandes do caderno (atual)
        SL = [.45, -.15, -.75, -1.35]                        # linhas arquivadas (62 %): 4 = payoff no topo
        self.at('b1_i1')
        self.play(Create(nrm1), Create(ai1), run_time=.35)
        li1 = self.coloca(M('i_1', 44, VIOLET), meio_arco(P1, N2, -d_in, RA), bissetriz(N2, -d_in), r0=.12)
        self.play(FadeIn(li1), run_time=.15)
        self.at('b1_r1')
        self.play(Create(ar1), run_time=.3)
        lr1 = self.coloca(M('r_1', 44, MAG), meio_arco(P1, -N2, w, RA), bissetriz(-N2, w), r0=.12, extra=[li1])
        self.play(FadeIn(lr1), run_time=.15)
        S1 = pinta(M(r'\operatorname{sen} i_1 = n\,\operatorname{sen} r_1', 68), {VIOLET: [3, 4], MAG: [10, 11]}).move_to([.2, YA, 0])
        S2 = pinta(M(r'\operatorname{sen} i_2 = n\,\operatorname{sen} r_2', 68), {VIOLET: [3, 4], MAG: [10, 11]}).move_to([.2, YB, 0])
        self.at('b1_eq1')
        self.play(FadeIn(S1, shift=UP * .08), Indicate(ai1, color=VIOLET, scale_factor=1.12), Indicate(ar1, color=MAG, scale_factor=1.12),
                  run_time=.5)
        self.eq_entra(S1, '1 · sen i1 = n sen r1')
        self.mark('C06_b1_snell1')
        self.at('b1_i2')
        self.play(Create(nrm2), Create(ai2), Create(ar2), run_time=.35)
        li2 = self.coloca(M('i_2', 44, VIOLET), meio_arco(P2, N4, d_out, RA), bissetriz(N4, d_out), r0=.12, extra=[li1, lr1])
        lr2 = self.coloca(M('r_2', 44, MAG), meio_arco(P2, -N4, -w, RA), bissetriz(-N4, -w), r0=.12, extra=[li1, lr1, li2])
        self.play(FadeIn(VGroup(li2, lr2)), run_time=.25)
        copia = S1.copy()
        self.at('b1_eq2')
        self.add(copia)
        self.toca(S2, gm(copia, S2, ([0, 1, 2, 3], [0, 1, 2, 3]), ([4], [4]), ([5, 6, 7, 8, 9, 10], [5, 6, 7, 8, 9, 10]), ([11], [11])),
                  Indicate(ai2, color=VIOLET, scale_factor=1.12), Indicate(ar2, color=MAG, scale_factor=1.12),
                  rt=.9, y=YB, nome='C06 MF1: sen i2 = n sen r2 construída da linha 1')
        self.remove(copia)
        self.eq_entra(S2, '2 · sen i2 = n sen r2')
        self.mark('C06_b1_snell2')
        self.at('b1_arq')
        self.eq_sai(S1); self.eq_sai(S2)
        self.play(*self.para_caderno(S1, SL[1], num=1), *self.para_caderno(S2, SL[2], num=2), run_time=.6)
        # batida 2: o triângulo das normais (preenchido), 120°, r1 + r2 = 60°
        X = cruza(P1, -N2, P2, -N4)
        tri_n = Polygon(P3(P1), P3(P2), P3(X)).set_stroke(CYAN, 2, .9).set_fill(CYAN, 0).set_z_index(8)
        tri_n._desenho = True
        cresce = VGroup(Line(P3(P1), P3(X)).set_stroke(CLARO, 3.5), Line(P3(P2), P3(X)).set_stroke(CLARO, 3.5)).set_z_index(11)
        for c_ in cresce:
            c_._qa = 'traco'
        a120 = arco(X, P1 - X, P2 - X, .5, CYAN, 5.5)
        self.at('b2')
        self.play(FadeOut(VGroup(ai1, ai2, li1, li2)), Create(cresce), run_time=.5)
        self.play(tri_n.animate.set_fill(CYAN, .22), Create(a120), run_time=.45)
        self.remove(lr1, lr2)
        alvo_r1 = self.coloca(lr1[0].copy(), meio_arco(P1, -N2, w, RA), bissetriz(-N2, w), r0=.12)
        alvo_r2 = self.coloca(lr2[0].copy(), meio_arco(P2, -N4, -w, RA), bissetriz(-N4, -w), r0=.12, extra=[alvo_r1])
        self.add(lr1, lr2)
        l120 = self.coloca(T('120°', 30, CYAN), meio_arco(X, P1 - X, P2 - X, .5), bissetriz(P1 - X, P2 - X), r0=.1,
                           extra=[alvo_r1, alvo_r2])
        self.play(FadeIn(l120), lr1.animate.move_to(alvo_r1[0]), lr2.animate.move_to(alvo_r2[0]), run_time=.3)
        self.mark('C06_b2_triangulo')
        T1 = pinta(M(r'120^\circ + r_1 + r_2 = 180^\circ', 64), {MAG: [5, 6, 8, 9], CYAN: [0, 1, 2, 3]}).move_to([.2, YC, 0])
        T3 = pinta(M(r'r_1 + r_2 = 60^\circ', 64), {MAG: [0, 1, 3, 4]}).move_to([.2, YC, 0])
        self.at('b2_eq')
        self.play(FadeIn(T1, shift=UP * .08), Indicate(ar1, color=MAG, scale_factor=1.15), Indicate(ar2, color=MAG, scale_factor=1.15), run_time=.5)
        self.eq_entra(T1, '120° + r1 + r2 = 180°')
        self.mark('C06_b2_eq')
        self.at('b2_mf')
        self.troca_eq(T1, T3, gm(T1, T3, ([5, 6, 7, 8, 9], [0, 1, 2, 3, 4]), ([10], [5]), ([4], []),
                                 ([0, 1, 2, 3, 11, 12, 13, 14], [6, 7, 8], {'path_arc': -PI / 2})),
                      rt=.9, nome='C06 MF2: o 120° atravessa o = e junta com o 180°', nome_b='3 · r1 + r2 = 60°')
        self.mark('C06_b2_r60')
        self.at('b2_arq')
        self.eq_sai(T3)
        self.play(*self.para_caderno(T3, SL[3], num=3), run_time=.6)
        # batida 3: o desvio em cada face (i − r), com a "dobra" percorrendo o raio
        cont1 = tracejada(P1, P1 + 1.4 * d_in, TEXT_COLOR, 2.6, .7, qa=True).set_z_index(9)
        cont2 = tracejada(P2, P2 + 1.4 * w, TEXT_COLOR, 2.6, .7, qa=True).set_z_index(9)
        av1, av2 = arco(P1, d_in, w, 1.15, CYAN, 5.5), arco(P2, w, d_out, 1.15, CYAN, 5.5)
        self.at('b3')
        self.play(FadeOut(VGroup(cresce, tri_n, a120, l120, lr1, lr2, ar1, ar2, nrm1, nrm2)), Create(cont1), Create(av1), run_time=.4)
        lv1 = self.coloca(M('i_1 - r_1', 56, CYAN), meio_arco(P1, d_in, w, 1.15), bissetriz(d_in, w), r0=.12)
        self.play(FadeIn(lv1), Create(cont2), Create(av2), run_time=.3)
        lv2 = self.coloca(M('i_2 - r_2', 56, CYAN), meio_arco(P2, w, d_out, 1.15), bissetriz(w, d_out), r0=.12, extra=[lv1])
        self.play(FadeIn(lv2), run_time=.2)
        dobra1 = luz([P1 - 1.0 * d_in, P1, P1 + 1.0 * w], CYAN, 6, 1)[1].copy()
        dobra2 = luz([P2 - 1.0 * w, P2, P2 + 1.0 * d_out], CYAN, 6, 1)[1].copy()
        self.play(ShowPassingFlash(dobra1, time_width=.6), Indicate(av1, color=CYAN, scale_factor=1.1), run_time=.75)
        self.play(ShowPassingFlash(dobra2, time_width=.6), Indicate(av2, color=CYAN, scale_factor=1.1), run_time=.75)
        self.mark('C06_b3_viradas')
        # batida 4: a soma; o 60° voa da linha 3 do caderno
        D1 = pinta(M(r'D = (i_1 - r_1) + (i_2 - r_2)', 64), {CYAN: list(range(17))}).move_to([.2, YC, 0])
        D2 = pinta(M(r'D = i_1 + i_2 - (r_1 + r_2)', 64), {CYAN: [0], VIOLET: [2, 3, 5, 6], MAG: [8, 9, 10, 11, 12, 13, 14]}).move_to([.2, YC, 0])
        D3 = pinta(M(r'D = i_1 + i_2 - 60^\circ', 72), {CYAN: list(range(11))}).move_to([.2, YC, 0])
        self.at('b3_eq')
        self.play(FadeIn(D1, shift=UP * .08), Indicate(av1, color=CYAN, scale_factor=1.1), Indicate(av2, color=CYAN, scale_factor=1.1), run_time=.5)
        self.eq_entra(D1, 'D = (i1 − r1) + (i2 − r2)')
        self.mark('C06_b4_D1')
        self.at('soma')                                          # "somando as duas faces": os dois parênteses brilham juntos
        self.play(Indicate(D1, color=WHITE, scale_factor=1.05), run_time=.6)
        self.at('b4_mf1')
        self.troca_eq(D1, D2, gm(D1, D2, ([0, 1], [0, 1]), ([3, 4], [2, 3], {'path_arc': 1.5}), ([9], [4], {'path_arc': 1.5}),
                                 ([11, 12], [5, 6], {'path_arc': 1.5}), ([5], [7], {'path_arc': 1.5}), ([6, 7], [9, 10], {'path_arc': 1.5}),
                                 ([14, 15], [12, 13], {'path_arc': 1.5}), ([16], [14]), ([2, 8, 10, 13], []), ([], [8, 11])),
                      rt=.7, nome='C06 MF3: os −r entram no parêntese', nome_b='D = i1 + i2 − (r1 + r2)')
        self.mark('C06_b4_D2')
        self.at('d2b')                                           # "menos a soma das refrações": (r1 + r2) destacado
        self.play(Indicate(VGroup(*[D2[0][i] for i in (8, 9, 10, 11, 12, 13, 14)]), color=WHITE, scale_factor=1.12), run_time=.6)
        self.untilr('b4_mf2', -.45)
        self.play(Indicate(T3, color=CYAN, scale_factor=1.06), run_time=.4)           # a linha 3 pisca: o 60° vem dela
        self.at('b4_mf2')
        self.troca_eq(D2, D3, gm(D2, D3, ([0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 2, 3, 4, 5, 6, 7]), ([8, 9, 10, 11, 12, 13, 14], []),
                                 (VoaDe, [8, 9, 10], {'origem': VGroup(*T3[0][6:9]), 'delay': .15, 'run_time': .4}), anda=(.05, .4)),
                      rt=.7, nome='C06 MF4: o 60° voa da linha 3', nome_b='4 · D = i1 + i2 − 60° (payoff)')
        n4 = T('4', 22, '#AEB9CC').move_to([-3.85, YC, 0])
        self.numeros.append(n4)
        self.add(n4)
        self.mark('C06_payoff')

        # ══ C07 — girar o cristal; o caderno encolhe (D = i1 + i2 − 60° no topo) ══════════════════════════════════
        ref = pinta(M(r'D = i_1 + i_2 - 60^\circ', 62), {CYAN: [0], VIOLET: [2, 3, 5, 6]}).move_to([0, 1.2, 0])
        self.until(E['girar'])
        self.eq_sai(D3)
        graf = self.grafico(origem=(-3.1, -3.55), xl=6.4, yl=1.7)
        for c_ in self.caderno:
            self.eq_tempos.append({'equacao': f"caderno: {c_['eq'].tex_string}", 'entra': None, 'sai': None, 'parada_s': None,
                                   'posicao': [round(float(c_['eq'].get_x()), 2), round(float(c_['eq'].get_y()), 2)]})
        # 1) o caderno e o resto do C06 saem; 2) D sobe sozinha ao topo; 3) só então o gráfico entra por baixo
        self.play(FadeOut(VGroup(cont1, cont2, av1, av2, lv1, lv2, *self.numeros, *[c_['eq'] for c_ in self.caderno]), shift=UP * .25), run_time=.35)
        self.play(ReplacementTransform(D3, ref), run_time=.55)
        self.eq_entra(ref, 'D = i1 + i2 − 60° (topo do caderno)')
        pt = redesenha(lambda: self.ponto(self.est()['i1']))
        self.traco_max = 14.

        def tracado():
            t = self.tq
            if E['giro_ini'] <= t:
                self.traco_max = max(self.traco_max, min(self.est()['i1'], 88.) if t <= E['giro_fim'] + .1 else 88.)
            return self.curva(14., max(self.traco_max, 14.1)) if t >= E['giro_ini'] else VGroup()
        trac = redesenha(tracado)
        dial = redesenha(lambda: self.dial())
        self.untilr('giro_ini', -.6)                           # item 2.1: o gráfico e o ponto só entram com "girando, ele cai"
        self.play(FadeIn(graf, shift=UP * .2), run_time=.45)
        self.add(trac, pt)
        self.untilr('giro_ini', -.05)
        self.add(dial)
        self.mark('C07_grafico')
        self.until((E['giro_ini'] + E['giro_fim']) / 2)
        self.mark('C07_meio_do_giro')
        self.at('giro_fim')
        self.mark('C07_curva')
        self.remove(dial)
        ia, ib = F.faixa_fundo()
        ax = self.ax
        fx = Rectangle(width=ax.c2p(ib, 20)[0] - ax.c2p(ia, 20)[0], height=ax.c2p(10, 45)[1] - ax.c2p(10, 20)[1])
        fx.move_to((ax.c2p(ia, 20) + ax.c2p(ib, 45)) / 2).set_fill(CYAN, .08).set_stroke(CYAN, 1.5, .45).set_z_index(4)
        fy = Rectangle(width=ax.c2p(90, 20)[0] - ax.c2p(10, 20)[0], height=ax.c2p(10, DMIN + 1)[1] - ax.c2p(10, DMIN)[1])
        fy.move_to((ax.c2p(10, DMIN) + ax.c2p(90, DMIN + 1)) / 2).set_fill(CYAN, .22).set_stroke(CYAN, 1.5, .6).set_z_index(4)
        fx._desenho = fy._desenho = True
        fundo = self.curva(ia, ib, TEXT_COLOR, 6.5)
        lmin7 = self.leitura_min()
        self.at('faixas')
        self.play(FadeIn(fx), FadeIn(fy), Create(fundo), run_time=.8)
        bx = Brace(Line(ax.c2p(ia, 30), ax.c2p(ib, 30)), UP, buff=.04, color=CYAN)
        lx = T('> 20°', 26, CYAN).next_to(bx, UP, .06)
        by = Brace(Line(ax.c2p(90, DMIN), ax.c2p(90, DMIN + 1)), RIGHT, buff=.08, color=CYAN, sharpness=1.2)
        ly = T('< 1°', 24, CYAN).next_to(by, RIGHT, .08)
        chs = VGroup(bx, lx, by, ly).set_z_index(9)
        self.at('chaves')
        self.play(FadeIn(chs), Create(lmin7[0]), FadeIn(lmin7[1]), run_time=.6)
        self.mark('C07_faixas_chaves')
        self.untilr('conta', -.5)
        self.play(FadeOut(VGroup(fx, fy, chs, fundo)), run_time=.45)

        # ══ C08 — a conta: ida e volta, com o caderno ═════════════════════════════════════════════════════════
        self.untilr('fantasma', +.35)
        st = self.est(E['fantasma'] + 1.2)
        tr, g = st['tr'], st['fantasma']['pts']
        fut8 = oculta(g)
        self.add(fut8)
        l_ida = self.coloca(T('ida', 26, SOLC), tr['pontos'][1] - .8 * tr['d_in'], np.array([.2, 1.]), r0=.2)
        l_volta = self.coloca(T('volta', 26, CLARO), g[0] + .45 * (g[1] - g[0]), g[0] - g[1], r0=.2, extra=[l_ida])
        self.remove(fut8)
        self.play(FadeIn(l_ida), FadeIn(l_volta), run_time=.3)
        self.mark('C08_ida_volta_cristal')

        def par_x():
            return float(F.par_invertido(self.est()['i1']))

        def k_rot():
            dx = abs(self.ax.c2p(par_x(), 20)[0] - self.ax.c2p(self.est()['i1'], 20)[0])
            return float(np.clip((dx - 1.3) / .4, 0, 1))
        par = redesenha(lambda: self.ponto(par_x(), CLARO))
        pt_ida = redesenha(lambda: self.ponto(self.est()['i1'], SOLC))
        fs = ValueTracker(0)                       # fade do segmento e dos rótulos: FadeIn/FadeOut em grupo que se refaz a cada quadro quebra (zip de famílias)

        def com_fade(m):
            for f in m.get_family():
                if f.has_points():
                    f.set_stroke(opacity=f.get_stroke_opacity() * fs.get_value())
                    f.set_fill(opacity=f.get_fill_opacity() * fs.get_value())
            return m
        seg = redesenha(lambda: com_fade(tracejada(self.ax.c2p(self.est()['i1'], float(F.desvio(self.est()['i1']))),
                                                   self.ax.c2p(par_x(), float(F.desvio(self.est()['i1']))), TEXT_COLOR, 2.5, .75).set_z_index(7)))

        def rotulos_pts():
            k = k_rot()
            y = float(F.desvio(self.est()['i1']))
            a, b = self.ax.c2p(self.est()['i1'], y), self.ax.c2p(par_x(), y)
            g = VGroup(T('ida', 20, SOLC).move_to(a + UP * .3 + RIGHT * .3).set_opacity(k),
                       T('volta', 20, CLARO).move_to(b + UP * .3 + LEFT * .42).set_opacity(k))
            for m in g:
                m._qa_isento = True
            return com_fade(g)
        rots = redesenha(rotulos_pts)
        rots._qa_isento = True
        curva8 = self.curva(14., 88.)
        self.remove(trac)
        self.add(curva8)
        self.at('pontos_par')
        self.play(FadeOut(pt), FadeIn(pt_ida), FadeIn(par, scale=.5), run_time=.35)
        self.at('segmento')
        self.add(seg, rots)
        self.play(fs.animate.set_value(1), run_time=.3)
        self.mark('C08_par_30_53')
        self.untilr('giro2_ini', -.35)
        self.play(FadeOut(VGroup(l_ida, l_volta)), run_time=.3)
        self.at('coincide')
        self.play(Flash(self.ax.c2p(IMIN, DMIN), color=CYAN, flash_radius=.28, line_length=.22), fs.animate.set_value(0), run_time=.5)
        self.remove(seg, rots)
        self.mark('C08_coincide')
        st = self.est(E['paralelo'])
        tr = st['tr']
        V, (_, P1, P2) = tr['V'], tr['pontos']
        wv = (P2 - P1) / np.linalg.norm(P2 - P1)

        def marca(p):
            q = np.array([-wv[1], wv[0]])
            return VGroup(*[linha([p + s * .1 * wv - .1 * wv + .1 * q, p + s * .1 * wv, p + s * .1 * wv - .1 * wv - .1 * q], CYAN, 3.5, qa=False)
                            for s in (-.5, .5)])
        face3 = linha([V[3], V[4]], CYAN, 8, qa=False).set_z_index(12)
        marcas = VGroup(marca((P1 + P2) / 2 + .25 * wv), marca((V[3] + V[4]) / 2)).set_z_index(13)
        self.at('paralelo')
        self.play(FadeIn(face3), FadeIn(marcas), run_time=.5)
        self.play(face3.animate.set_stroke(width=5, opacity=.6), run_time=.3)
        self.mark('C08_paralelo')
        # caderno do C08: linha 0 (topo) = D; linha 1 = r; linha 2 = Snell arquivada; a linha atual (grande) embaixo
        X0, Y0, Y1, Y2, YA8 = -3.35, 1.45, .8, .15, -.8

        def esq(m, y, x0=X0):
            return m.move_to([x0 + m.width / 2, y, 0])
        DD1 = esq(pinta(M(r'D = 2i - 60^\circ', 48), {CYAN: [0], VIOLET: [2, 3]}), Y0)
        R1 = esq(pinta(M(r'r_1 + r_2 = 60^\circ', 48), {MAG: [0, 1, 3, 4]}), Y1)
        R2 = esq(pinta(M(r'2r = 60^\circ', 48), {MAG: [0, 1]}), Y1)
        R3 = esq(pinta(M(r'r = 30^\circ', 48), {MAG: [0, 2, 3, 4]}), Y1)
        tro = dict(run_time=.4)
        tri_ = dict(delay=.4, run_time=.4)
        self.at('eq_par')
        n8 = [T('1', 22, '#AEB9CC').move_to([-3.85, Y0, 0]), T('2', 22, '#AEB9CC').move_to([-3.85, Y1, 0])]
        self.troca_eq(ref, DD1, gm(ref, DD1, ([0, 1], [0, 1]), ([2, 3, 4, 5, 6], [], tro), ([], [2, 3], tri_), ([7, 8, 9, 10], [4, 5, 6, 7]), anda=(.15, .6)),
                      rt=.8, nome='C08 MF5: simetria D = 2i − 60°', nome_b='D = 2i − 60°')
        self.add(n8[0])
        self.play(FadeIn(R1, shift=UP * .08), FadeIn(n8[1]), run_time=.4)
        self.eq_entra(R1, 'r1 + r2 = 60°')
        self.mark('C08_simetria')
        self.at('r30a')
        self.troca_eq(R1, R2, gm(R1, R2, ([0], [1]), ([1, 2, 4], [], tro), ([3], [], tro), ([], [0], tri_), ([5], [2]), ([6, 7, 8], [3, 4, 5])),
                      rt=.7, nome='C08 MF5: r1 + r2 = 60° → 2r = 60°', nome_b='2r = 60°')
        C1 = pinta(M(r'\operatorname{sen} i = n\,\operatorname{sen} r', 64), {VIOLET: [3], MAG: [9]}).move_to([.1, YA8, 0])
        self.play(FadeIn(C1, shift=UP * .08), run_time=.5)
        self.eq_entra(C1, 'sen i = n sen r')
        self.mark('C08_snell_1')
        self.at('r30b')
        self.troca_eq(R2, R3, gm(R2, R3, ([0], [], tro), ([1], [0]), ([2], [1]), ([3], [], tro), ([], [2], tri_), ([4, 5], [3, 4])),
                      rt=.7, nome='C08 MF5: 2r = 60° → r = 30°', nome_b='r = 30°')
        N2, N4 = F.normal_face(2, tr['theta']), F.normal_face(4, tr['theta'])
        n30 = VGroup(tracejada(P1, P1 - 1.0 * N2, TEXT_COLOR, 2.6, .7), tracejada(P2, P2 - 1.0 * N4, TEXT_COLOR, 2.6, .7)).set_z_index(11)
        a30 = VGroup(arco(P1, -N2, wv, .7, MAG, 5.5), arco(P2, -N4, -wv, .7, MAG, 5.5)).set_z_index(12)
        self.play(Create(n30), Create(a30), run_time=.4)
        l30a = self.coloca(T('30°', 28, MAG), meio_arco(P1, -N2, wv, .7), bissetriz(-N2, wv), r0=.1)
        l30b = self.coloca(T('30°', 28, MAG), meio_arco(P2, -N4, -wv, .7), bissetriz(-N4, -wv), r0=.1, extra=[l30a])
        self.play(FadeIn(l30a), FadeIn(l30b), run_time=.3)
        self.mark('C08_r30')
        C2 = pinta(M(r'\operatorname{sen} i = 1{,}31 \cdot \operatorname{sen} 30^\circ', 64), {VIOLET: [3], MAG: [13, 14, 15]}).move_to([.1, YA8, 0])
        C3 = pinta(M(r'\operatorname{sen} i = 1{,}31 \cdot 0{,}5', 64), {VIOLET: [3]}).move_to([.1, YA8, 0])
        C4 = pinta(M(r'\operatorname{sen} i = 0{,}655', 64), {VIOLET: [3]}).move_to([.1, YA8, 0])
        C5 = pinta(M(r'i = \arcsin(0{,}655) \approx 40{,}9^\circ', 70), {VIOLET: [0, 16, 17, 18, 19, 20]}).move_to([.1, YA8, 0])
        self.at('snell2')
        self.troca_eq(C1, C2, gm(C1, C2, ([0, 1, 2, 3, 4], [0, 1, 2, 3, 4]), ([5], [], tro), ([], [5, 6, 7, 8, 9], tri_),
                                 ([6, 7, 8], [10, 11, 12]), ([9], [], tro),
                                 (VoaDe, [13, 14, 15], {'origem': VGroup(*R3[0][2:5]), 'delay': .4, 'run_time': .5})),
                      rt=.75, nome='C08 MF6: n = 1,31 e r = 30°', nome_b='sen i = 1,31 · sen 30°')
        self.mark('C08_snell_2')
        self.at('snell4')                                          # "a incidência dá uns quarenta e um graus": 1,31 · sen 30° → arcsen(0,655) ≈ 40,9° em um passo
        self.troca_eq(C2, C5, gm(C2, C5, ([3], [0]), ([4], [1]), ([0, 1, 2], [], tro), (list(range(5, 16)), [], tro),
                                 ([], [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], tri_), ([], [14, 15, 16, 17, 18, 19, 20], tri_), anda=(.05, .45)),
                      rt=.8, nome='C08: 1,31 · sen 30° → i = arcsen(0,655) ≈ 40,9°', nome_b='i = arcsen(0,655) ≈ 40,9°')
        self.mark('C08_snell_4')
        DD2 = pinta(M(r'D = 2 \cdot 40{,}9^\circ - 60^\circ', 64), {CYAN: [0], VIOLET: [4, 5, 6, 7, 8]})
        PAY = M(r'D = 2 \cdot 40{,}9^\circ - 60^\circ \approx 21{,}8^\circ', 62, CYAN)
        self.at('mf4')
        self.eq_sai(C5)
        self.play(*self.para_caderno(C5, Y2, esc=.78, num=3), run_time=.4)
        DD2.move_to([0, YA8, 0])
        PAY.move_to([0, YA8, 0])
        self.troca_eq(DD1, DD2, AnimationGroup(gm(DD1, DD2, ([0, 1, 2], [0, 1, 2]), ([3], [], tro), ([], [3], tri_),
                                   (VoaDe, [4, 5, 6, 7, 8], {'origem': VGroup(*C5[0][16:21]), 'delay': .5, 'run_time': .45}),
                                   ([4, 5, 6, 7], [9, 10, 11, 12]), anda=(.05, .45)), FadeOut(n8[0])), rt=.9, nome='C08: o 40,9° voa para D = 2i − 60°',
                      nome_b='D = 2 · 40,9° − 60°')
        self.mark('C08_mf4')
        pmin = self.ax.c2p(IMIN, DMIN)
        self.at('payoff')
        self.troca_eq(DD2, PAY, gm(DD2, PAY, (list(range(13)), list(range(13))), ([], [13, 14, 15, 16, 17, 18], {'delay': .35, 'run_time': .45})),
                      rt=.8, nome='C08: ≈ 21,8°', nome_b='D = 2 · 40,9° − 60° ≈ 21,8° (payoff)')
        self.remove(minimapa)
        minimapa = redesenha(lambda: self.minimapa(self.d_minimapa(), '21,8°' if self.tq < E['amontoado'] - .5 else None))
        self.add(minimapa)
        self.play(Flash(pmin, color=CYAN, flash_radius=.3), run_time=.6)
        self.mark('C08_payoff')
        self.until(E['amontoado'])
        for k_ in list(self.eq_vivas.values()):
            self.eq_sai(k_[2])
        for m in (pt_ida, par, cristal, minimapa):
            m.clear_updaters()
        self.play(FadeOut(VGroup(pt_ida, par, face3, marcas, n30, a30, l30a, l30b, PAY, graf, curva8, cristal, minimapa, lmin7, R3, C5,
                                 *n8, self.numeros[-1])), run_time=.25)

        # ══ C09 — o amontoado, a cena de lado e o cone saindo da pessoa ══════════════════════════════════════════
        graf9 = self.grafico(origem=(-2.8, -3.4), xl=3.7, yl=5.4, x_ticks=(20, 60))
        curva9 = self.curva(14., 89.)
        x_h = 1.05
        eixo_h = VGroup(Line([x_h, self.ax.c2p(10, 20)[1], 0], [x_h, self.ax.c2p(10, 45)[1], 0]).set_stroke(DIM, 2.5),
                        T('orientações', 18, DIM).move_to([x_h + 1.15, self.ax.c2p(10, 45)[1] + .3, 0])).set_z_index(5)
        self.play(FadeIn(graf9), Create(curva9), FadeIn(eixo_h), run_time=.25)
        self.mark('C09_inicio')
        ip, Dp = F.projecao_orientacoes()
        pontos = VGroup(*[Dot(self.ax.c2p(x, y), .055, color=CYAN).set_z_index(8) for x, y in zip(ip, Dp)])
        txt_pt = T('cada ponto: uma orientação', 28).move_to([0, 4.4, 0])
        self.at('pontos_ini')
        self.playr(FadeIn(txt_pt), LaggedStart(*[FadeIn(p, scale=.4) for p in pontos], lag_ratio=.8), run_time=E['pontos_fim'] - self.tq - .05)
        self.mark('C09_pontos')
        bins = np.floor((Dp - DMIN) / .5 + 1e-9).astype(int)
        ocup, alvos = {}, []
        for kk in range(len(Dp)):
            j = bins[kk]
            n = ocup.get(j, 0); ocup[j] = n + 1
            alvos.append(np.array([x_h + .14 + n * .14, self.ax.c2p(10, DMIN + .5 * (j + .5))[1], 0]))
        self.at('projeta_ini')
        anims = [Succession(p.animate(run_time=.6).move_to([alvos[k][0], p.get_y(), 0]), p.animate(run_time=.25).move_to(alvos[k]))
                 for k, p in enumerate(pontos)]
        self.playr(LaggedStart(*anims, lag_ratio=.12), run_time=E['projeta_fim'] - self.tq - .05)
        self.mark('C09_projecao')
        y_dmin = self.ax.c2p(10, DMIN)[1]
        vazio = Rectangle(width=2.0, height=y_dmin - self.ax.c2p(10, 20)[1]).next_to([x_h, y_dmin, 0], RIGHT, .02, aligned_edge=UP)
        vazio.set_fill(CYAN, 0).set_stroke(CYAN, 2.5, .9).set_z_index(7)
        vazio._desenho = True
        base = Line([x_h, y_dmin, 0], [x_h + 2.0, y_dmin, 0]).set_stroke(CYAN, 3).set_z_index(7)
        lmin9 = self.leitura_min()
        self.at('vazio')
        self.play(FadeOut(txt_pt), FadeIn(vazio), run_time=.25)
        for _ in range(2):
            self.play(vazio.animate.set_fill(CYAN, .25), run_time=.2)
            self.play(vazio.animate.set_fill(CYAN, 0), run_time=.2)
        self.play(FadeOut(vazio), Create(base), Create(lmin9[0]), FadeIn(lmin9[1]), run_time=.35)
        self.mark('C09_parede')
        self.untilr('lado9', -.3)                                # item 2.5: sem vão entre o histograma e a cena de lado
        self.play(FadeOut(VGroup(graf9, curva9, eixo_h, pontos, base, lmin9)), run_time=.3)
        PHP, PHL = (9., 14.), (30.,)
        L9 = self.cena_lado(phis=(DMIN,) + PHP + PHL, n=30, seed=8)
        D_perto = float(F.desvio(30.))
        i_longe = float(F.faixa_fundo(30. - DMIN)[1])
        assert abs(F.desvio(i_longe) - 30.) < 1e-6 and D_perto >= DMIN
        l_os9 = self.tracejada_sol()
        self.at('lado9')
        self.play(FadeIn(VGroup(L9['chao'], L9['pessoa'], L9['sol'], L9['voce'], L9['nuvem'], l_os9, *L9['crs'].values())),
                  run_time=.5)
        self.mark('C09_lado')
        r22s = self.raio_lado(DMIN, w=5.5)[0].set_z_index(10)
        rp = VGroup(*[self.raio_lado(p, D=D_perto, op=.75, ate_chao=True)[0] for p in PHP]).set_z_index(10)
        rl = self.raio_lado(30., D=float(F.desvio(i_longe)), op=.45)[0].set_z_index(10)
        futuros = VGroup(*[oculta([q[:2] for q in r[1].get_anchors()]) for r in list(rp) + [rl]])
        self.add(futuros)
        self.at('acende9')
        self.play(L9['crs'][DMIN].animate.set_stroke(SOLC, 3.5).set_fill(SOLC, .5), Create(r22s), run_time=.55)
        lm = self.coloca(T('muita luz', 34, SOLC, piso=34), RT.cristal_lado(DMIN) + np.array([0, -.45]), np.array([-1., -.6]), r0=.2)
        self.play(FadeIn(lm), run_time=.2)
        self.mark('C09_muita_luz')
        self.at('perto')
        self.play(Create(rp), run_time=.55)
        lp = self.coloca(T('nada', 34, piso=34), (RT.cristal_lado(9.) + RT.cristal_lado(14.)) / 2, np.array([.6, -1.]), r0=.5, extra=[lm])
        self.play(FadeIn(lp), run_time=.2)
        self.mark('C09_perto')
        self.at('longe')
        self.play(Create(rl), run_time=.45)
        self.remove(futuros)
        ll = self.coloca(T('pouca', 34, DIM, piso=34), RT.cristal_lado(30.), np.array([-1., -.4]), r0=.3, extra=[lm, lp])
        self.play(FadeIn(ll), run_time=.2)
        self.mark('C09_longe')
        # o cone: a pessoa cresce, as linhas de visão varrem o cone, a vista gira em 2.5D em torno do eixo olho → Sol e a borda vira o anel do C01
        self.at('cone')
        cone = redesenha(lambda: self.cone_desenho())
        self.cone_pessoa = cone
        self.add(cone)
        self.remove(L9['pessoa'], L9['sol'])                  # a pessoa e o Sol agora são os do cone (o mesmo desenho, no mesmo lugar)
        self.play(FadeOut(VGroup(L9['nuvem'], *L9['crs'].values(), r22s, rp, rl, lm, lp, ll, l_os9, L9['voce'])), run_time=.4)
        l_cone = VGroup(T('ao redor', 26, CYAN), T('de você:', 26, CYAN), T('um cone', 34, CYAN)).arrange(DOWN, buff=.06, aligned_edge=LEFT).move_to([2.75, -2.7, 0])
        self.play(FadeIn(l_cone), run_time=.3)
        self.until(E['cone_frente'] - .2)
        self.mark('C09_cone_varre')
        self.at('cone_frente')
        self.play(FadeOut(VGroup(L9['chao'], l_cone)), run_time=.6)
        self.until((E['cone_frente'] + E['ceu_volta']) / 2)
        self.mark('C09_cone_girando')
        self.at('ceu_volta')
        self.mark('C09_cone_frente')
        self.untilr('ceu_volta', +.7)
        cone.clear_updaters()
        self.remove(cone)
        self.cone_pessoa = None
        self.mark('C09_ceu')
        self.untilr('cores', -.25)

        # ══ C10 — as cores: índice de refração (Warren & Brandt 2008) ═════════════════════════════════════════════
        axz = Axes(x_range=[30, 52, 2], y_range=[21, 23, .5], x_length=6.2, y_length=7.3, tips=False,
                   axis_config={'stroke_color': DIM, 'stroke_width': 2.5, 'include_ticks': False})
        axz.shift(P3((-2.55, -3.5)) - axz.c2p(30, 21))
        self.ax = axz
        mz = VGroup()
        for y in (21, 22, 23):
            p = axz.c2p(30, y)
            mz.add(Line(p, p + LEFT * .1).set_stroke(DIM, 2))
            if y != 22:
                mz.add(T(f'{y}°', 34, TEXT_COLOR, piso=34).next_to(p, LEFT, .25).shift(UP * (.2 if y == 21 else 0)))
        for x in (30, 40, 50):
            p = axz.c2p(x, 21)
            mz.add(Line(p, p + DOWN * .08).set_stroke(DIM, 1.5, .6), T(f'{x}°', 34, '#6E7F9E', piso=34).next_to(p, DOWN, .3))
        tz = T('zoom no fundo do vale', 34, piso=34)
        tz.move_to([axz.c2p(30, 21)[0] + .25 + tz.width / 2, axz.c2p(30, 21)[1] + .55, 0])      # acima do eixo, à esquerda; nenhuma curva passa aqui
        tit = VGroup(T('desvio', 34, CYAN, piso=34).next_to(axz.c2p(30, 23), UP, .5).align_to(axz.c2p(30, 23) + LEFT * .5, LEFT),
                     T('ângulo de incidência', 34, DIM, piso=34).next_to(axz.c2p(41, 21), DOWN, .8))
        axz.x_axis._qa = 'traco'
        gz = VGroup(axz, mz, tit).set_z_index(5)
        nV, nVi = F.N_GELO_VERMELHO, F.N_GELO_VIOLETA
        def janela(n_):
            xs = np.arange(30, 52.0001, .05)
            ok = [x for x in xs if float(F.desvio(x, n_)) <= 22.97]
            return [float(ok[0]), float(ok[-1]), .05]
        cv = axz.plot(lambda x: float(F.desvio(x, nV)), x_range=janela(nV)).set_stroke('#FF5A4A', 5).set_z_index(6)
        cvi = axz.plot(lambda x: float(F.desvio(x, nVi)), x_range=janela(nVi)).set_stroke('#9B7BFF', 5).set_z_index(6)
        cv._qa = cvi._qa = 'traco'
        iv, ivi = float(F.i1_min(nV)), float(F.i1_min(nVi))
        dv, dvi = float(F.d_min(nV)), float(F.d_min(nVi))
        lv_ = self.leitura_min(iv, dv, f'{dv:.1f}°'.replace('.', ','), '#FF5A4A', dy=-.04)
        lvi_ = self.leitura_min(ivi, dvi, f'{dvi:.1f}°'.replace('.', ','), '#9B7BFF', dy=.02)
        nv = T(f'n DO VERMELHO = {nV:.4f}'.replace('.', ','), 26, '#FF8A7A', maius=False)
        nvi = T(f'n DO VIOLETA = {nVi:.4f}'.replace('.', ','), 26, '#B9A3FF', maius=False)
        selos = VGroup(nv, nvi).arrange(DOWN, buff=.18, aligned_edge=LEFT).move_to([0, 5.3, 0])
        veu10 = veu_grafico(VGroup(gz, selos))
        self.play(FadeIn(gz), FadeIn(veu10), run_time=.25)                       # item 2.5: o gráfico entra um instante antes da fala
        self.at('cores')
        self.at('curva_v')
        self.play(Create(cv), FadeIn(nv), run_time=.7)
        self.at('min_v')                                         # "vinte e um vírgula sete"
        self.play(Create(lv_[0]), FadeIn(lv_[1]), Flash(axz.c2p(iv, dv), color='#FF5A4A', flash_radius=.25), run_time=.6)
        self.at('curva_vi')
        self.play(Create(cvi), FadeIn(nvi), run_time=.7)
        self.at('min_vi')                                        # "vinte e dois vírgula cinco"
        self.play(Create(lvi_[0]), FadeIn(lvi_[1]), Flash(axz.c2p(ivi, dvi), color='#9B7BFF', flash_radius=.25), run_time=.6)
        self.at('zoom_txt')                                     # o texto do zoom entra com o gráfico já pleno e sai antes de ele sumir
        self.play(FadeIn(tz), run_time=.3)
        self.mark('C10_zoom_curvas')
        self.untilr('ceu_cores', -.8)
        self.play(FadeOut(tz), run_time=.3)
        self.untilr('ceu_cores', -.4)
        self.play(FadeOut(VGroup(gz, cv, cvi, lv_, lvi_, selos, veu10)), run_time=.4)
        esc, tr_ = RT.ZOOM

        def tela(ang):
            return RT.vista_para_tela(RT.manim_de_dir(RT._no_cone(RT.SOL_DIR, ang, -38.)), esc, tr_)
        p_in, p_out = tela(21.0), tela(23.6)
        rad = normalize(np.array([*(p_out - p_in), 0.]))
        nrm = np.array([-rad[1], rad[0], 0.])
        barra = VGroup()
        cores_b = [(21.0, '#FF5A4A'), (21.7, '#FF7A5E'), (22.0, '#FFE7D2'), (22.5, '#C9B8FF'), (23.0, '#9B7BFF'), (23.6, '#7FA8FF')]
        for (a0, c0), (a1, c1) in zip(cores_b, cores_b[1:]):
            q0, q1 = P3(tela(a0)) - .5 * nrm, P3(tela(a1)) - .5 * nrm
            barra.add(Line(q0, q1).set_stroke(width=16).set_color([c0, c1]))
        barra.set_z_index(20)
        self.at('barra')
        self.play(Create(barra), run_time=.6)
        self.at('seta_verm')
        self.at('seta_vio')                                      # os rótulos "vermelho por dentro / violeta por fora" agora entram com o cristal do C11
        self.mark('C10_cores_ceu')
        self.untilr('sintese', -.9)
        self.play(FadeOut(barra), run_time=.4)

        # ══ C11 — síntese em três andares (céu · cristal · gráfico) e CTA ═════════════════════════════════════════
        graf11 = self.grafico(origem=(-2.75, -4.38), xl=5.2, yl=1.5, marcas_y=(), numeros_x=False, legendas=False)
        curva11 = self.curva(14., 89.)
        pb = self.ax.c2p(IMIN, DMIN)
        dot11 = Dot(pb, .09, color=CYAN).set_z_index(9)
        lmin11 = self.leitura_min()
        andar_vale = VGroup(graf11, curva11, dot11, lmin11)
        cristal11 = redesenha(lambda: self.cristal_vetor(realce=(2, 4), ponta=True))
        self.at('sintese')
        self.add(cristal11)
        self.play(FadeIn(andar_vale), run_time=.7)
        self.mark('C11_sintese')
        pts11 = np.array(self.est(E['sintese'] + 1)['feixe']['pts'])           # o raio que sai do cristal: vermelho desvia menos (por dentro), violeta mais (por fora)
        d_in, d_out = normalize(pts11[1] - pts11[0]), normalize(pts11[-1] - pts11[-2])
        sgn = 1. if d_in[0] * d_out[1] - d_in[1] * d_out[0] > 0 else -1.
        gira = lambda v, a: np.array([v[0] * np.cos(a) - v[1] * np.sin(a), v[0] * np.sin(a) + v[1] * np.cos(a)])
        pe = pts11[-2]
        r_verm = Line(P3(pe), P3(pe + 2.4 * gira(d_out, -sgn * np.radians(6)))).set_stroke('#FF5A4A', 5)
        r_viol = Line(P3(pe), P3(pe + 2.4 * gira(d_out, sgn * np.radians(6)))).set_stroke('#9B7BFF', 5)
        r_verm.set_z_index(11), r_viol.set_z_index(11)
        l_viol = VGroup(T('violeta', 28, '#B9A3FF', piso=28), T('por fora', 28, '#B9A3FF', piso=28)).arrange(DOWN, buff=.05).move_to([3.35, -1.0, 0])
        l_verm = VGroup(T('vermelho', 28, '#FF8A7A', piso=28), T('por dentro', 28, '#FF8A7A', piso=28)).arrange(DOWN, buff=.05).move_to([3.35, -3.0, 0])
        leque = VGroup(r_verm, r_viol, l_viol, l_verm)
        self.play(Create(r_verm), Create(r_viol), FadeIn(l_viol), FadeIn(l_verm), run_time=.6)
        self.at('pulso_faces')
        self.realce_extra = 1.
        self.untilr('pulso_faces', +1.7)
        self.realce_extra = 0.
        self.mark('C11_duas_faces')
        self.untilr('fios', -.5)
        self.play(FadeOut(leque), run_time=.3)
        st = self.est(E['fios'] + 1)
        tr11 = st['tr']
        borda_s = RT.vista_para_tela(RT.manim_de_dir(RT._no_cone(RT.SOL_DIR, DMIN, -60.)), *RT.FAIXA)
        fio1 = DashedLine(P3(st['feixe']['pts'][-1]), P3(borda_s), dash_length=.08).set_stroke(SOLC, 2, .8).set_z_index(9)
        fio2 = DashedLine(pb + UP * .12, P3(tr11['pontos'][2] + .25 * tr11['d_final']), dash_length=.08).set_stroke(CYAN, 2, .8).set_z_index(9)
        fio1._qa = fio2._qa = 'traco'
        self.at('fios')
        self.play(Create(fio1), Create(fio2), run_time=.8)
        self.mark('C11_fios')
        self.at('halo11')                                        # "aparece o halo": o anel acende no céu da faixa (3D) e o Sol pulsa
        self.play(Flash(P3(RT.FAIXA[1] + RT.FAIXA[0] * np.array(RT.SOL_MANIM)), color=SOLC, flash_radius=.55, line_length=.3), run_time=.6)
        self.mark('C11_halo')
        self.at('cta')
        cristal11.clear_updaters()
        siga = legivel(screen_text('Siga o Parallax Lab', 40, oversample=2)).move_to([0, .45, 0]).set_z_index(40)
        handle = screen_text('@labparallax', 48, oversample=2).next_to(siga, DOWN, .35).set_z_index(40)
        handle.set_color_by_gradient(PRIMARY_COLOR, SECONDARY_COLOR, MAG)
        handle = legivel(handle)
        siga._qa = handle._qa = 'texto'
        self.play(FadeOut(VGroup(andar_vale, fio1, fio2, cristal11, tag)), FadeOut(logo),      # item 2.8: o cartão entra junto com a fala
                  FadeIn(siga, shift=UP * .1), FadeIn(handle, scale=.96), run_time=.6)
        self.mark('C11_cta')
        self.until(RT.DURACAO)
        self.mark('fim', qa=False)
        print('ATRASOS:', len(self.atrasos), *self.atrasos, sep='\n  ')
        assert self.nq == round(RT.DURACAO * FPS), (self.nq, RT.DURACAO * FPS)
        pasta = Path(config.media_dir)
        (pasta / 'estados.json').write_text(json.dumps({'eventos': self.events}, ensure_ascii=False, indent=2), encoding='utf-8')
        (pasta / 'qa_geometria.json').write_text(json.dumps({
            'topo_anel_22_24': TOPO_ANEL, 'estados': self.geometria, 'transicoes': self.transicoes,
            'glifos_transicao': self.glifos_transicao, 'glifos_parados': self.glifos_parados, 'equacoes': self.eq_tempos,
            'chegada': self.chegada, 'cortes_r': self.corte_r, 'cone': self.cone_qa, 'cone_info': list(self.cone_info.values()),
            'objetos_giro': {'serie': self.objetos_giro, 'quadros': len(self.objetos_giro), 'min': min(self.objetos_giro, default=0),
                             'max': max(self.objetos_giro, default=0)},
            'linhas_mistas': []}, ensure_ascii=False), encoding='utf-8')
