"""vid_0030 — Anel de guardanapo: camadas Manim do pipeline Three.js + Manim (+ Remotion experimental).

Duas cenas com fundo TRANSPARENTE (-t), ambas presas ao mesmo timeline.json (nenhum tempo solto aqui):
  CenaMat — matemática exata: rótulos sobre o 3D, triângulo, área da coroa, R sumindo, Cavalieri, volume, integral,
            casos-limite. Entra no compor.py (preview oficial) e no Remotion (experimento).
  CenaUI  — interface: cabeçalho, títulos do gancho, réguas "6 cm", rótulos R = …, contadores, textos de cena e end card.
            Entra só no preview oficial; no experimento Remotion esta camada é refeita em React.
Rótulos que acompanham o 3D leem ancoras_<fps>fps.json (gerado por ancoras.js a partir do cena3d.js).

Cores (paleta Parallax Lab): h = ciano (protagonista), R = magenta (some da conta), a = violeta (furo), z e
construção = GEO, texto/equações = branco, painel #0E2A52 com borda #7FB2FF.

Render (raiz do repositório, bash):
  MEDIA_DIR=videos/vid_0030_anel_guardanapo/media_preview uv run --no-sync python -m manim -t -r 540,960 --fps 15 \
      --disable_caching videos/vid_0030_anel_guardanapo/cena.py CenaMat CenaUI
"""
import json
import os
import sys
from pathlib import Path

from manim import *
from MF_Tools import TransformByGlyphMap

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
sys.path.insert(0, str(ROOT))
from template.config import TEXT_COLOR, PRIMARY_COLOR, WATERMARK_PATH  # noqa: E402  (frame 9 × 16 e CRF do canal)
from template.fonts import screen_text  # noqa: E402

config.media_dir = os.environ.get("MEDIA_DIR", str(UNIT / "media_preview"))
TL = json.loads((UNIT / "timeline.json").read_text(encoding="utf-8"))
G, E, CH = TL["geometria"], TL["eventos"], TL["chaves"]
PISO = TL["legenda"]["conteudo_acima_de"]           # nada da cena abaixo disto (faixa da legenda)

# v4.2 (Kaio): h SEMPRE magenta, em todo o vídeo; R branco; ciano só como destaque (setas, ✓, cancelamentos)
H_C, R_C, A_C = "#EA63FF", "#F2F6FF", "#9C8CFF"     # h, R, a
CIANO = "#35D9FF"
R_TXT = "#F28DFF"                                    # v4: magenta clareado para rótulo pequeno (contraste ≥ 4,5:1)
GEO, DIM, PANEL, BLUE_L = "#B8C4DA", "#8FA3C4", "#0E2A52", "#7FB2FF"
CYAN, PINK = PRIMARY_COLOR, "#EA63FF"                # só no degradê do @labparallax do cartão final
TRIO_C = ["#5C93FF", "#3D7BFF", "#2C68EA"]           # três anéis do gancho: mesma família azul do 3D (v2)
HFRAC = r"\left(\tfrac{h}{2}\right)"
HF, HD = HFRAC, r"\left(\dfrac{h}{2}\right)"
BRANCO, ESF, RECUO = "#F2F6FF", "#F7B8FF", 0.85     # equação ativa em branco pleno; usada recua a 85 % (v3: ≥ 75 % medidos)

# cores das partes das equações (string exata da parte → cor)
CORES = {
    "R": R_C, "R^2": R_C, "a": A_C, "a^2": A_C, "h": H_C, "z": GEO, "z^2": GEO,
    HFRAC + "^2": H_C, HFRAC + "^3": H_C, r"\tfrac{h}{2}": H_C, r"\tfrac{h^3}{8}": H_C,
    r"r_{\text{ext}}^2": TEXT_COLOR, r"r_{\text{int}}^2": TEXT_COLOR,
}


def fim_chave(nome):
    return CH[nome][-1]["t"]


def eq(*partes, size=48, y=None, x=0.0):
    m = MathTex(*partes, font_size=size, color=TEXT_COLOR)
    for i, p in enumerate(partes):
        if p in CORES:
            m[i].set_color(CORES[p])
    if y is not None:
        m.move_to([x, y, 0])
    return m


def pinta(m, mapa):
    """Cor por índice de glifo (MathTex de string única): {cor: [índices]}."""
    for cor, idx in mapa.items():
        for i in idx:
            m[0][i].set_color(cor)
    return m


def words(content, y=0, size=28, color=TEXT_COLOR, x=0, **kw):
    pw, ph = config.pixel_width, config.pixel_height
    try:
        config.pixel_width = config.pixel_height = 4000
        mob = screen_text(content, size, color=color, oversample=2, **kw)
    finally:
        config.pixel_width, config.pixel_height = pw, ph
    if mob.width > 8.2:
        mob.scale_to_fit_width(8.2)
    return mob.move_to([x, y, 0])


def troca(a, b, pares):
    """Transformação parte a parte entre MathTex com partes: [([índices em a], [índices em b]), ...]."""
    return [ReplacementTransform(VGroup(*[a[i] for i in ia]), VGroup(*[b[j] for j in ib])) for ia, ib in pares]


def chip(mob, buff=0.18):
    caixa = RoundedRectangle(corner_radius=0.12, width=mob.width + 2 * buff, height=mob.height + 2 * buff,
                             fill_color=PANEL, fill_opacity=0.85, stroke_color=BLUE_L, stroke_width=2)
    return VGroup(caixa.move_to(mob), mob)


def caixa(mob, buff=0.16):
    return SurroundingRectangle(mob, color=BLUE_L, buff=buff, corner_radius=0.08, stroke_width=3)


class Base(Scene):
    """Relógio do timeline, âncoras do 3D e verificação da faixa de legenda."""

    def setup(self):
        fps = round(config.frame_rate)
        dados = json.loads((UNIT / f"ancoras_{fps}fps.json").read_text(encoding="utf-8"))
        assert dados["fps"] == fps
        self._idx = {n: i for i, n in enumerate(dados["nomes"])}
        self._vidx = {n: i for i, n in enumerate(dados["valores_nomes"])}
        self._q, self._v, self._fps = dados["quadros"], dados["valores"], fps
        self._cx = dados.get("caixas", [])
        self.atrasos, self.fora = [], []
        # v3 · QA: caixas de cada glifo visível por quadro, com o nome do grupo (linha de álgebra, rótulo, memo...).
        # Atualizador da cena: roda depois dos atualizadores dos objetos, uma vez por quadro (e torna as esperas não
        # estáticas). O qa/sobreposicao.py cruza estas caixas com as do Remotion e com a máscara do 3D.
        self._log, self.transito = {}, "transito"
        self.add_updater(lambda dt: self._registra())

    def agora(self):
        return self.renderer.time

    def _quadro(self):
        return min(len(self._q) - 1, max(0, round(self.agora() * self._fps)))

    def anc(self, nome):
        x, y = self._q[self._quadro()][self._idx[nome]]
        return np.array([x, y, 0.0])

    def val(self, nome):
        return self._v[self._quadro()][self._vidx[nome]]

    def ate(self, alvo):
        nome = alvo
        if isinstance(alvo, str):
            alvo = E[alvo]
        n = round((alvo - self.agora()) * self._fps)
        if n > 0:
            self.wait(n / self._fps - 1e-6)
        elif n < -1:
            self.atrasos.append({"evento": nome, "alvo": alvo, "chegou": round(self.agora(), 3)})
            print(f"ATRASO {nome}: alvo {alvo:.2f}s, cena em {self.agora():.2f}s")

    def segue(self, m, nome, off=ORIGIN, lado=None):
        """Prende m a uma âncora do 3D. lado='esq' encosta a borda esquerda; 'dir' a direita."""
        off = np.array(off, dtype=float)

        def upd(mob):
            p = self.anc(nome) + off
            if lado == "esq":
                p = p + RIGHT * mob.width / 2
            elif lado == "dir":
                p = p + LEFT * mob.width / 2
            mob.move_to(p)
        upd(m)
        m.add_updater(upd)
        return m

    def acima(self, *mobs):
        for m in mobs:
            assert m.get_bottom()[1] > PISO, f"invadiu a faixa da legenda: {m}"

    def cx(self, nome):
        """Caixa projetada da silhueta de um sólido no quadro atual, em unidades do Manim: (x0, y0, x1, y1), y para cima."""
        b = self._cx[self._quadro()].get(nome) if self._cx else None
        return None if b is None else (b[0] / 60 - 4.5, 8 - b[3] / 60, b[2] / 60 - 4.5, 8 - b[1] / 60)

    def zona(self, *mobs, grupo=None):
        """Confere a zona de álgebra do trecho atual (timeline 'zonas') e a margem lateral de 24 px; registra o desvio."""
        t = self.agora()
        tr = next(z for z in TL["zonas"]["trechos"] if z["de"] - 1e-6 <= t < z["ate"] + 1e-6)
        topo, base = 8 - tr["zona_algebra"][0] / 60, 8 - tr["zona_algebra"][1] / 60
        for m in mobs:
            erro = []
            if m.get_top()[1] > topo + 1e-3 or m.get_bottom()[1] < base - 1e-3:
                erro.append(f"y {m.get_bottom()[1]:.2f}..{m.get_top()[1]:.2f} fora de {base:.2f}..{topo:.2f}")
            if m.get_left()[0] < -4.1 or m.get_right()[0] > 4.1:
                erro.append(f"x {m.get_left()[0]:.2f}..{m.get_right()[0]:.2f} fora de ±4,1")
            if erro:
                self.fora.append({"t": round(t, 2), "grupo": grupo or getattr(m, "grupo", "?"), "erro": erro})
                print("FORA DA ZONA", round(t, 2), grupo or getattr(m, "grupo", "?"), erro)
        return mobs[0]

    def nomeia(self, nome, *mobs):
        for m in mobs:
            m.grupo = nome
        return mobs[0]

    def _registra(self):
        # um glifo pode estar na cena duas vezes (a equação e o próprio glifo solto, deixado por Indicate/Replacement):
        # conta uma vez só, com o nome do grupo quando houver
        caixas, vistos = [], {}
        antes, agora = getattr(self, "_pos", {}), {}
        for m in self.mobjects:
            g = getattr(m, "grupo", None) or self.transito
            for leaf in m.family_members_with_points():
                if id(leaf) in vistos:
                    if getattr(m, "grupo", None):
                        vistos[id(leaf)][0] = g
                    continue
                if not isinstance(leaf, VMobject):
                    continue
                fo = leaf.get_fill_opacity()
                so = leaf.get_stroke_opacity() if leaf.get_stroke_width() > 0 else 0.0
                op = max(fo, so)
                if op < 0.02:
                    continue
                pad = 0.0 if fo >= so else 1.5
                x0, x1 = (leaf.get_left()[0] + 4.5) * 60 - pad, (leaf.get_right()[0] + 4.5) * 60 + pad
                y0, y1 = (8 - leaf.get_top()[1]) * 60 - pad, (8 - leaf.get_bottom()[1]) * 60 + pad
                # v5: deslocamento do glifo desde o quadro anterior (px) — o QA de transições compara movimentos relativos
                c = ((x0 + x1) / 2, (y0 + y1) / 2)
                agora[id(leaf)] = c
                d = antes.get(id(leaf), c)
                vistos[id(leaf)] = [g, round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1), round(op, 3),
                                    round(c[0] - d[0], 2), round(c[1] - d[1], 2)]
        self._pos = agora
        self._log[self._quadro()] = list(vistos.values())

    def tira(self, *mobs):
        """v5: remove os objetos E os pedaços soltos deles. Indicate/.animate num pedaço de equação (m[0][3:5]) põem esse
        pedaço na cena como objeto próprio; ao trocar a equação ele ficava desenhado (glifo fantasma)."""
        folhas = {id(l) for m in mobs for l in m.family_members_with_points()}
        soltos = [m for m in self.mobjects if m not in mobs and m.family_members_with_points()
                  and all(id(l) in folhas for l in m.family_members_with_points())]
        self.remove(*mobs, *soltos)

    def sai(self, *mobs, rt=0.6):
        mobs = [m for m in mobs if m is not None]
        for m in mobs:
            m.clear_updaters()
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=rt)
            self.tira(*mobs)

    def fecha(self, classe):
        # mesmo nº de quadros do 3D (wait estático do Manim arredonda para baixo: completa de 1 em 1)
        while round(self.agora() * self._fps) < round(TL["duracao_s"] * self._fps):
            self.wait(1 / self._fps)
        out = Path(config.media_dir) / f"estados_{classe}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"atrasos": self.atrasos, "fora_da_zona": self.fora, "duracao": round(self.agora(), 3),
                                   "quadros": round(self.agora() * self._fps)}, ensure_ascii=False, indent=1),
                       encoding="utf-8")
        (out.parent / f"caixas_{classe}.json").write_text(json.dumps({"fps": self._fps, "quadros": self._log}),
                                                           encoding="utf-8")
        print("ATRASOS:", self.atrasos)
        print("FORA DA ZONA:", len(self.fora))


def vem_de(origem):
    """Introdutor do TransformByGlyphMap: o glifo novo nasce de uma CÓPIA de `origem` (outra equação na tela)."""
    class _Vem(ReplacementTransform):
        def __init__(self, mob, **kw):
            super().__init__(origem.copy(), mob, **kw)
    return _Vem


def move_de(origem):
    """Introdutor do TransformByGlyphMap (v5): o glifo novo é a PRÓPRIA peça `origem` viajando (sem cópia + fade, que
    deixava um "duplo" por 2–3 quadros)."""
    class _Move(ReplacementTransform):
        def __init__(self, mob, **kw):
            super().__init__(origem, mob, **kw)
    return _Move


def vai_para(destino):
    """Removedor do TransformByGlyphMap: os glifos viajam inteiros (sem apagar) até `destino` (outra equação na tela)."""
    class _Vai(ReplacementTransform):
        def __init__(self, mob, **kw):
            super().__init__(mob, destino, **kw)
    return _Vai


def tx(tex, size, cores=None, y=None, x=0.0):
    """MathTex de string única (base dos glyph maps), branco pleno, cor por índice de glifo {cor: [índices]}."""
    m = MathTex(tex, font_size=size, color=BRANCO)
    pinta(m, cores or {})
    if m.width > 8.5:
        m.scale_to_fit_width(8.5)
    if y is not None:
        m.move_to([x, y, 0])
    return m


def fundo(mob, buff=0.17):
    """Caixa da fórmula-chave: fundo #0E2A52 e borda #7FB2FF, atrás da fórmula."""
    return RoundedRectangle(corner_radius=0.1, width=mob.width + 2 * buff, height=mob.height + 2 * buff,
                            fill_color=PANEL, fill_opacity=0.9, stroke_color=BLUE_L, stroke_width=3).move_to(mob).set_z_index(-1)


FUNDO = "#050816"


def rot3d(tex, cor, size=48):
    """Rótulo sobre o 3D: texto sólido e opaco na cor da grandeza (v4.1, pedido do Kaio: sem chip nem contorno preto)."""
    return MathTex(tex, font_size=size, color=cor)


def halo(m, largura=12):
    """v4.1: sem contorno escuro (mantida para não mexer nas chamadas)."""
    return m


def nota(glifo, txt, lado, size=40, cor=CIANO):
    """Número escrito à mão sobre/sob um algarismo riscado (v5: folga ≥ 6 px do riscado)."""
    return MathTex(txt, font_size=size, color=cor).next_to(glifo, lado, buff=0.12)


def risco(glifo, cor=CIANO):
    """Traço diagonal de cancelamento sobre um glifo."""
    return Line(glifo.get_corner(DL) + DL * 0.04, glifo.get_corner(UR) + UR * 0.04, color=cor, stroke_width=5)


class CenaMat(Base):
    # v3 · layout por zonas (timeline "zonas"): a álgebra mora na zona de álgebra do trecho, em linhas (slots) que não
    # se tocam; linha nova só entra em slot livre; linha velha sai (FadeOut) antes; termos que viajam usam slots vazios.
    def gm(self, a, b, *mapa, rt=1.4, extras=(), **kw):
        """Glyph map + limpeza: no fim só b fica na cena (sem glifo 'pela metade' de a)."""
        b.grupo = getattr(b, "grupo", None) or getattr(a, "grupo", None)
        self.transito = f"{b.grupo}*"
        self.play(TransformByGlyphMap(a, b, *mapa, **kw), *extras, run_time=rt)
        self.transito = "transito"
        self.tira(a)
        self.add(b)

    def recua(self, *mobs, rt=0.5):
        """Equação já usada: recua para RECUO (nunca abaixo de 75 % efetivos)."""
        self.play(*[m.animate.set_opacity(RECUO) for m in mobs], run_time=rt)

    def entra(self, *mobs, rt=0.4, extras=()):
        """Linha nova: FadeIn inteiro e curto (v4: ≤ 0,4 s, a fórmula já nasce legível)."""
        self.play(*[FadeIn(m, shift=UP * 0.12) for m in mobs], *extras, run_time=min(rt, 0.4))

    def construct(self):
        S = 1.25                                          # escala da álgebra do v2 em relação ao v1
        # ── C02 · anatomia: rótulos do triângulo e relação R² − a² = (h/2)² ─────────────────────────────────
        self.ate("rotulos_tri")
        # v5 (L2): rótulos ≥ 20 px, afastados 6–8 px da linha; sem chip nem contorno (decisão do Kaio)
        lR = self.segue(rot3d("R", BRANCO, 58), "meio_R", off=[-0.4, 0.46, 0])
        la = self.segue(rot3d("a", A_C, 58), "meio_a", off=[0, -0.46, 0])
        lh2 = self.segue(rot3d(r"\tfrac{h}{2}", H_C, size=54), "meio_h2", off=[-0.6, 0, 0])
        lh = rot3d("h", H_C, 58).move_to((self.anc("parede_e_baixo") + self.anc("parede_e_cima")) / 2 + RIGHT * 0.5)
        self.nomeia("rot_aux", lR, la, lh2, lh)
        self.play(FadeIn(lR, scale=0.8), run_time=0.4)
        self.ate(fim_chave("tri_a") - 0.3)
        self.play(FadeIn(la, scale=0.8), run_time=0.4)
        self.ate(fim_chave("tri_h") - 0.3)
        self.play(FadeIn(lh2, scale=0.8), run_time=0.4)
        self.ate(fim_chave("tri_hcheia") - 0.3)
        self.play(FadeIn(lh, scale=0.8), run_time=0.4)

        self.ate("eq_pitagoras")
        cP = {R_C: [0, 1], A_C: [3, 4], H_C: range(6, 12)}
        P1 = self.nomeia("C02_pit", tx(r"R^2=a^2+" + HF + "^2", 58 * S, cP, y=-1.45))
        self.zona(P1)
        self.entra(P1)
        self.play(Indicate(lR, color=WHITE), Indicate(P1[0][0:2], color=WHITE), run_time=0.6)
        self.play(Indicate(la, color=WHITE), Indicate(P1[0][3:5], color=WHITE), run_time=0.6)
        self.play(Indicate(lh2, color=WHITE), Indicate(P1[0][6:12], color=WHITE), run_time=0.6)
        self.ate("eq_relacao")
        # S1 (v5): em tempos separados — o "+" some; o a² SOBE (fica acima da linha); o "=" anda para a direita por
        # baixo dele; o a² desce do outro lado e o "−" nasce. Nada cruza nada.
        P2 = self.nomeia("C02_pit", tx(r"R^2-a^2=" + HF + "^2", 58 * S, cP).move_to(P1))
        self.transito = "C02_pit*"
        self.play(FadeOut(P1[0][5], scale=0.6), run_time=0.25)
        self.play(P1[0][3:5].animate.shift(UP * 0.48), run_time=0.35)
        self.play(P1[0][2].animate.move_to(P2[0][5]), P1[0][0:2].animate.move_to(P2[0][0:2]),
                  P1[0][6:12].animate.move_to(P2[0][6:12]), run_time=0.45)
        self.play(P1[0][3:5].animate.move_to(P2[0][3:5]), FadeIn(P2[0][2], scale=0.6), run_time=0.4)
        self.transito = "transito"
        self.tira(P1)
        self.remove(P2[0][2])
        self.add(P2)
        cx2 = self.nomeia("C02_pit", fundo(P2))
        self.play(FadeIn(cx2), run_time=0.4)

        self.ate("memo")
        # a própria equação vira o lembrete (sem cópia: nunca duas versões na tela). Encolhe no lugar, no topo da zona,
        # com o bloco R² − a² exatamente acima do bloco (R² − a²) da linha A(z) do C03.
        A3_ref = tx(r"A(z)=\pi\big[(R^2-a^2)-z^2\big]", 52 * S)
        memo = VGroup(cx2, P2)
        self.nomeia("memo", P2, cx2)
        alvo = memo.copy().scale(0.62)
        alvo.shift(UP * (-0.72 - alvo.get_top()[1]))
        alvo.shift(RIGHT * (A3_ref[0][8:13].get_x() - alvo[1][0][0:5].get_x()))
        self.play(Transform(memo, alvo), run_time=1.0)
        self.tira(memo)
        memo_box, memo_tex = alvo[0], alvo[1]
        self.nomeia("memo", memo_box, memo_tex)
        self.add(memo_box, memo_tex)
        self.zona(VGroup(memo_box, memo_tex), grupo="memo")
        self.ate("corte_sai")
        self.sai(lR, la, lh2, lh, rt=0.4)

        # ── C03 · a fatia: coroa, área e o R saindo da conta ────────────────────────────────────────────────
        self.ate("rotulos_fatia")
        fz = self.segue(rot3d("z", GEO, 52), "fat_zmeio", off=[-0.4, 0, 0])
        fext = self.segue(rot3d(r"r_{\text{ext}}", BRANCO, 52), "fat_ext_meio", off=[0, 0.42, 0])
        fint = self.segue(rot3d(r"r_{\text{int}}", A_C, 52), "fat_int_meio", off=[0, 0.42, 0])
        fR = self.segue(rot3d("R", BRANCO, 52), "fat_R_meio", off=[0.32, -0.36, 0])
        self.nomeia("rot_aux", fz, fext, fint, fR)
        self.play(*[FadeIn(m) for m in (fz, fext, fint, fR)], run_time=0.6)

        self.ate("eq_rext")
        # v5: a linha A(z) desce para −3,6 e abre um corredor entre ela e X|I (as cópias nascem nele, S2)
        Y_XI, Y_A, SA = -2.3, -3.6, 52 * S
        X = self.nomeia("C03_X", tx(r"r_{\text{ext}}^2=R^2-z^2", 46 * S, {R_C: [6, 7], GEO: [9, 10]}))
        I = self.nomeia("C03_I", tx(r"r_{\text{int}}^2=a^2", 46 * S, {A_C: [6, 7]}))
        VGroup(X, I).arrange(RIGHT, buff=0.75).move_to([0, Y_XI, 0])
        I.align_to(X, DOWN).shift(UP * (X[0][5].get_y() - I[0][5].get_y()))
        self.zona(X, I)
        self.entra(X, extras=[Indicate(fext, color=WHITE), Indicate(fR, color=WHITE)])
        self.ate("eq_rint")
        self.entra(I, extras=[Indicate(fint, color=WHITE)])

        def no_corredor(glifos, destinos):
            """S2: a cópia nasce no meio do corredor entre X|I e a linha A(z), já alinhada com a vaga (desce na vertical,
            sem cobrir a origem nem cruzar o colchete), enquanto a origem pisca."""
            meio = (VGroup(X, I).get_bottom()[1] + (Y_A + 0.42)) / 2
            cs = [g.copy().move_to([d.get_x(), meio, 0]) for g, d in zip(glifos, destinos)]
            self.play(*[Indicate(g, color=WHITE, scale_factor=1.06) for g in glifos], *[FadeIn(c) for c in cs], run_time=0.4)
            return cs

        self.ate("eq_area")
        A1 = self.nomeia("C03_A", tx(r"A(z)=\pi\big(r_{\text{ext}}^2-r_{\text{int}}^2\big)", SA, {GEO: [2]}, y=Y_A))
        self.zona(A1)
        esq = VGroup(*[A1[0][i] for i in (0, 1, 2, 3, 4, 5, 6, 12, 18)])
        bx, bi = A1[0][7:12], A1[0][13:18]
        self.transito = "C03_A*"
        cX, cI = no_corredor([X[0][0:5], I[0][0:5]], [bx, bi])
        self.play(Transform(cX, bx.copy()), Transform(cI, bi.copy()), run_time=0.7)
        self.nomeia("C03_A", esq)
        self.play(FadeIn(esq, shift=UP * 0.1), run_time=0.4)
        self.transito = "transito"
        self.tira(esq, cX, cI)
        self.add(A1)

        self.ate("eq_area_subst")
        cA2 = {R_C: [8, 9], GEO: [2, 11, 12], A_C: [15, 16]}
        A2 = tx(r"A(z)=\pi\big[(R^2-z^2)-a^2\big]", SA, cA2, y=Y_A)
        # S2: os blocos r_ext² e r_int² do A(z) saem ANTES; as cópias nascem no corredor e descem para as vagas
        self.transito = "C03_A*"
        self.play(FadeOut(A1[0][7:12]), FadeOut(A1[0][13:18]), run_time=0.3)
        cR, cA = no_corredor([X[0][6:11], I[0][6:8]], [A2[0][8:13], A2[0][15:17]])
        self.gm(A1, A2,
                (list(range(7)), list(range(7))),
                (list(range(7, 12)), FadeOut, {"run_time": 0.05}),
                (move_de(cR), [8, 9, 10, 11, 12], {"delay": 0.4}),
                ([], [7, 13], {"delay": 1.0}), ([12], [14]),
                (list(range(13, 18)), FadeOut, {"run_time": 0.05}),
                (move_de(cA), [15, 16], {"delay": 0.4}),
                ([18], [17]), rt=0.7)
        self.recua(X, I, rt=0.2)

        self.ate("eq_reagrupa")
        # r_ext² e r_int² já foram usados: saem antes do próximo passo (a linha de cima fica livre)
        self.sai(X, I, rt=0.4)
        # S3: a² e z² trocam de lugar em arcos opostos e largos (um por cima, outro por baixo da linha)
        cA3 = {R_C: [8, 9], A_C: [11, 12], GEO: [2, 15, 16]}
        A3 = tx(r"A(z)=\pi\big[(R^2-a^2)-z^2\big]", SA, cA3, y=Y_A)
        ga, gz = A2[0][15:17], A2[0][11:13]
        self.transito = "C03_A*"
        self.play(ga.animate.shift(UP * 0.55), gz.animate.shift(DOWN * 0.55), run_time=0.3)
        self.play(ga.animate.set_x(A3[0][11:13].get_x()), gz.animate.set_x(A3[0][15:17].get_x()), run_time=0.5)
        self.play(ga.animate.move_to(A3[0][11:13]), gz.animate.move_to(A3[0][15:17]), run_time=0.3)
        self.transito = "transito"
        A3.grupo = A2.grupo
        self.tira(A2)
        self.add(A3)

        self.ate("destaca_par")
        chv = self.nomeia("C03_A", Brace(A3[0][7:14], DOWN, buff=0.1, color=BLUE_L))
        ret_m = self.nomeia("memo_destaque", SurroundingRectangle(memo_tex[0][0:5], color=WHITE, buff=0.05, corner_radius=0.06))
        self.play(GrowFromCenter(chv), Create(ret_m), run_time=0.8)
        self.play(Indicate(memo_tex[0][0:5], color=WHITE, scale_factor=1.12), run_time=0.8)

        self.ate("R_some")       # MOMENTO CENTRAL: pulso + seta até o lembrete; o bloco some e o (h/2)² desce do lembrete
        cA4 = {H_C: range(7, 13), GEO: [2, 14, 15]}
        A4 = tx(r"A(z)=\pi\big[" + HF + r"^2-z^2\big]", SA, cA4, y=Y_A)
        seta = self.nomeia("C03_A", Arrow(A3[0][7:14].get_top() + UP * 0.06,
                                          [memo_tex[0][0:5].get_x(), memo_box.get_bottom()[1] - 0.08, 0],
                                          buff=0, color=BLUE_L, stroke_width=4, tip_length=0.16,
                                          max_tip_length_to_length_ratio=0.25))
        self.play(Indicate(A3[0][7:14], color=WHITE, scale_factor=1.08), GrowArrow(seta), run_time=0.8)
        h2 = memo_tex[0][6:12].copy().set_y(-2.3)
        self.transito = "C03_A*"
        self.play(FadeOut(A3[0][7:14]), FadeOut(chv), FadeOut(ret_m), FadeOut(seta),
                  Indicate(memo_tex[0][6:12], color=WHITE, scale_factor=1.08), FadeIn(h2, shift=DOWN * 0.1), run_time=0.4)
        self.gm(A3, A4, (list(range(7, 14)), FadeOut, {"run_time": 0.05}), (move_de(h2), list(range(7, 13))), rt=0.6)
        self.play(Indicate(A4[0][7:13], color=WHITE, scale_factor=1.12), run_time=0.35)
        self.ate("R_sumiu_txt")
        self.play(Indicate(memo_tex[0][0:5], color=WHITE, scale_factor=1.1), run_time=0.5)

        self.ate("caixa_area")
        cxA = self.nomeia("C03_A", fundo(A4))
        self.zona(VGroup(A4, cxA), grupo="C03_A")
        self.play(FadeIn(cxA), run_time=0.4)

        self.ate("fatia_sai")
        Y_a = -1.15
        A5 = self.nomeia("C04_A5", tx(r"A_{\text{anel}}(z)=\pi\big[" + HF + r"^2-z^2\big]", 44 * S,
                                       {H_C: range(11, 17), GEO: [6, 18, 19]}, y=Y_a))
        self.sai(fz, fext, fint, fR, memo_tex, memo_box, cxA, rt=0.4)
        self.ate("cav_desce_eq")
        # S4 (v5): primeiro a linha sobe inteira (mesmo tamanho do destino); depois o índice "anel" entra já na posição de
        # subscrito, com o A se afastando um pouco para abrir espaço
        A4.grupo = "C04_A5"
        A4m = A4.copy().scale(A5[0][9].height / A4[0][5].height)
        A4m.shift(A5[0][9].get_center() - A4m[0][5].get_center())
        self.transito = "C04_A5*"
        self.play(Transform(A4, A4m), run_time=0.6)
        self.transito = "transito"
        self.tira(A4)
        self.add(A4m)
        A4m.grupo = "C04_A5"
        self.gm(A4m, A5, ([0], [0]), ([], [1, 2, 3, 4], {"delay": 0.6}), (list(range(1, 17)), list(range(5, 21))), rt=0.9)
        self.zona(A5)

        # ── C04 · Cavalieri: de onde vem a área da esfera pequena ───────────────────────────────────────────
        self.ate("cav_rotulos")
        # "raio h/2" acima da silhueta projetada da esfera pequena (≥ 12 px), centrado nela e dentro da margem
        lesf = eq(r"\text{raio}\ \tfrac{h}{2}", size=52)
        lesf[0][4:].set_color(H_C)
        self.nomeia("C04_raio", lesf)

        def poe_raio(m):
            b = self.cx("esf")
            if b is None:
                return
            x = min(max((b[0] + b[2]) / 2, -4.1 + m.width / 2), 4.1 - m.width / 2)
            m.move_to([x, b[3] + 12 / 60 + m.height / 2, 0])
        poe_raio(lesf)
        lesf.add_updater(poe_raio)
        self.play(FadeIn(lesf, shift=DOWN * 0.1), run_time=0.4)

        self.ate("cav_tri")
        # L1 (v5): a câmera aproxima a esfera pequena; ρ, z e h/2 ficam FORA da esfera (≥ 18 px), ligados por linha-guia
        # fina ao segmento de cada um
        def fora(tex, cor, ancora, lado, size=58, abaixo_de=None):
            lab = MathTex(tex, font_size=size, color=cor)
            guia = Line(ORIGIN, RIGHT, color=cor, stroke_width=2)

            def poe(m):
                b, p = self.cx("esf"), self.anc(ancora)
                if b is None:
                    return
                x = b[2] + 0.22 + m.width / 2 if lado > 0 else b[0] - 0.22 - m.width / 2
                x = min(max(x, -4.1 + m.width / 2), 4.1 - m.width / 2)
                y = p[1]
                if abaixo_de is not None:              # nunca encosta no rótulo de cima (folga ≥ 8 px)
                    y = min(y, abaixo_de.get_bottom()[1] - 8 / 60 - m.height / 2)
                m.move_to([x, y, 0])
            poe(lab)
            lab.add_updater(poe)

            def liga(l):
                p = self.anc(ancora)
                ini = lab.get_left() + LEFT * 0.06 if lado > 0 else lab.get_right() + RIGHT * 0.06
                if np.linalg.norm(p - ini) > 0.05:
                    l.put_start_and_end_on(ini, p)
            liga(guia)
            guia.add_updater(liga)
            return VGroup(guia, lab)
        lrho = fora(r"\rho", ESF, "cav_rho_meio", +1)
        lhip = fora(r"\tfrac{h}{2}", H_C, "cav_hip_meio", +1, size=54, abaixo_de=lrho[1])
        lzc = fora("z", GEO, "cav_z_meio", -1)
        self.nomeia("rot_aux", lrho, lzc, lhip)
        self.play(LaggedStart(*[FadeIn(m) for m in (lzc, lrho, lhip)], lag_ratio=0.3), run_time=0.9)

        self.ate("cav_eq_esfera")
        Y_b, SB = -2.25, 44 * S
        S1 = self.nomeia("C04_S", tx(r"\rho^2+z^2=" + HF + "^2", SB, {ESF: [0, 1], GEO: [3, 4], H_C: range(6, 12)}, y=Y_b))
        self.zona(S1)
        self.entra(S1)
        self.play(Indicate(lrho[1], color=WHITE), Indicate(lzc[1], color=WHITE), Indicate(lhip[1], color=WHITE), run_time=0.5)
        self.ate("cav_eq_esfera_isola")
        # z² atravessa a igualdade por BAIXO (o slot de baixo ainda está vazio); "+" some antes, "−" nasce depois
        S2 = tx(r"\rho^2=" + HF + "^2-z^2", SB, {ESF: [0, 1], H_C: range(3, 9), GEO: [10, 11]}, y=Y_b)
        # v5: o "+" e o "=" saem antes de tudo; o "=" renasce no lugar novo (não desliza para junto do ρ²)
        self.play(FadeOut(S1[0][2], scale=0.6), FadeOut(S1[0][5]), run_time=0.25)
        self.gm(S1, S2, ([0, 1], [0, 1]), ([3, 4], [10, 11], {"path_arc": PI}), ([2, 5], FadeOut, {"run_time": 0.05}),
                ([], [9], {"delay": 0.6}), ([], [2], {"delay": 0.6}), (list(range(6, 12)), list(range(3, 9))), rt=1.3)
        self.ate("cav_eq_esfera2")
        # S5 (v5): primeiro os termos andam para a direita (abrem espaço); só depois "A_esf(z) = π", "π[" e "]" entram
        cS3 = {ESF: [9, 10], H_C: range(14, 20), GEO: [5, 21, 22]}
        S3 = tx(r"A_{\text{esf}}(z)=\pi\rho^2=\pi\big[" + HF + r"^2-z^2\big]", SB, cS3, y=Y_b)
        self.gm(S2, S3, ([], list(range(9)), {"delay": 1.0}), ([0, 1], [9, 10]), ([2], [11]), ([], [12, 13], {"delay": 1.0}),
                (list(range(3, 9)), list(range(14, 20))), ([9], [20]), ([10, 11], [21, 22]), ([], [23], {"delay": 1.0}),
                rt=1.6)
        self.zona(S3)

        self.ate("cav_pareia")
        # A_esf(z) = π[(h/2)² − z²], alinhada sob A_anel pelo sinal de igual
        S4 = tx(r"A_{\text{esf}}(z)=\pi\big[" + HF + r"^2-z^2\big]", SB, {H_C: range(10, 16), GEO: [5, 17, 18]}, y=Y_b)
        S4.shift(RIGHT * (A5[0][8].get_x() - S4[0][7].get_x()))
        self.play(FadeOut(S3[0][8:12]), run_time=0.3)
        self.gm(S3, S4, ([8, 9, 10, 11], FadeOut, {"run_time": 0.05}), (list(range(8)), list(range(8))),
                (list(range(12, 24)), list(range(8, 20))), rt=0.6)
        # S6 (v5): pareamento por pulsos simultâneos nos termos iguais (sem linhas atravessando glifos)
        pares = [(A5[0][9], S4[0][8]), (A5[0][11:17], S4[0][10:16]), (A5[0][17], S4[0][16]), (A5[0][18:20], S4[0][17:19])]
        self.play(*[Indicate(VGroup(a, b), color=CIANO, scale_factor=1.1) for a, b in pares], run_time=0.7)
        self.sai(lesf, lrho, lzc, lhip, rt=0.3)

        self.ate("cav_contadores")
        # a varredura do plano vem antes da conclusão (ordem da fala): as linhas usadas e os rótulos saem; os
        # contadores (Remotion) ocupam os slots
        self.sai(A5, S4, rt=0.4)
        self.ate("cav_eq_iguais")
        IG = self.nomeia("C04_IG", tx(r"A_{\text{anel}}(z)=A_{\text{esf}}(z)", 50 * S, {GEO: [6, 14]}, y=-3.5))
        cxI = self.nomeia("C04_IG", fundo(IG))
        self.zona(VGroup(IG, cxI), grupo="C04_IG")
        self.entra(IG, extras=[FadeIn(cxI)])
        self.ate("cav_sai")
        self.sai(IG, cxI, rt=0.4)

        # ── C05 · volume: rota 1 (Cavalieri, contas à vista) e rota 2 (integral, conferência curta) ──────────
        # zona de álgebra do C05: 384–745 px (y 1,6 a −4,42); o 3D sobe para 124–372 px
        SV = 58 * S
        self.ate("volume_igual")
        V0 = self.nomeia("C05_V0", tx(r"V_{\text{anel}}=V_{\text{esf}}", 50 * S, y=1.31))
        self.zona(V0)
        self.entra(V0)
        self.ate("volume_formula")
        Y1 = -0.3
        V1 = self.nomeia("C05_V", tx(r"V=\dfrac{4}{3}\pi" + HD + "^3", SV, {H_C: range(6, 12)}, y=Y1))
        self.zona(V1)
        self.entra(V1)
        self.recua(V0, rt=0.3)
        self.ate("volume_passo")
        # S7 (v5): dois tempos. (h/2)³ = h³/2³ (o expoente vai para o h e para o 2) …
        V1b = tx(r"V=\dfrac{4}{3}\pi\cdot\dfrac{h^3}{2^3}", SV, {H_C: [7, 8]}, y=Y1)
        self.play(FadeOut(V1[0][6]), FadeOut(V1[0][10]), run_time=0.25)
        self.gm(V1, V1b, (list(range(6)), list(range(6))), ([6, 10], FadeOut, {"run_time": 0.05}), ([7], [7]), ([8], [9]),
                ([9], [10]), ([11], [8]), ([], [11], {"delay": 0.5}), ([], [6], {"delay": 0.5}), rt=0.9)
        self.ate("volume_oito")
        # … e, em "sobre oito", 2³ = 8 com tudo numa fração só (o 2³ sai e o 8 nasce no lugar dele; sem morfo de dígito)
        V3 = tx(r"V=\dfrac{4\,\pi h^3}{3\cdot 8}", SV, {H_C: [4, 5]}, y=Y1)
        V1b.grupo = V3.grupo = "C05_V"
        self.sai(V1b, rt=0.25)
        self.entra(V3)
        self.ate("volume_risca")
        # 4/8 = 1/2 (S8): o 1 e o 2 nascem afastados ≥ 6 px do algarismo riscado e da linha de cima
        r4, r8 = risco(V3[0][2]), risco(V3[0][9])
        um, dois = nota(V3[0][2], "1", UP), nota(V3[0][9], "2", DOWN)
        self.nomeia("C05_V", um, dois)
        self.nomeia("C05_V_risco", r4, r8)
        self.play(Create(r4), Create(r8), FadeIn(um), FadeIn(dois), run_time=0.4)
        self.ate("volume_meio")
        V4 = tx(r"V=\dfrac{\pi h^3}{3\cdot 2}", SV, {H_C: [3, 4]}, y=Y1)
        self.play(FadeOut(V3[0][2]), FadeOut(V3[0][9]), FadeOut(r4), FadeOut(r8), FadeOut(um), run_time=0.3)
        self.gm(V3, V4, ([2, 9], FadeOut, {"run_time": 0.05}), (move_de(dois[0]), [8]),
                ([0, 1], [0, 1]), ([3, 4, 5], [2, 3, 4]), ([6], [5]), ([7], [6]), ([8], [7]), rt=0.7)
        self.tira(dois)
        self.ate("volume_final")
        # S9 (v5): 3·2 sai e o 6 entra no mesmo ponto (sem morfo de dígitos); a linha de cima (já usada) sai antes
        V5 = tx(r"V=\dfrac{\pi h^3}{6}", SV, {H_C: [3, 4]}).move_to([0, Y1, 0])
        self.play(FadeOut(V0), run_time=0.3)
        self.gm(V4, V5, (list(range(6)), list(range(6))), ([6, 7, 8], FadeOut), ([], [6], {"delay": 0.6}), rt=0.7)
        self.ate("volume_caixa")
        cxV = self.nomeia("C05_V", fundo(V5, buff=0.2))
        self.play(FadeIn(cxV), run_time=0.4)
        self.ate("volume_sobe")
        rota1 = VGroup(cxV, V5)
        self.play(rota1.animate.scale(0.75).move_to([0, 0.8, 0]), run_time=0.5)
        self.zona(rota1, grupo="C05_V")

        # rota 2 (conferência curta: a fala da integral saiu no corte 1): integral → primitiva → mesmo resultado
        self.ate("integral")
        Y2, Y3, SI = -0.95, -2.6, 42 * S
        I1 = self.nomeia("C05_I1", tx(r"\int_{-h/2}^{h/2}\pi\Big[" + HF + r"^2-z^2\Big]\,dz", SI,
                                      {H_C: [1, 5, *range(10, 16)], GEO: [17, 18, 21]}, y=Y2))
        self.zona(I1)
        self.entra(I1)
        self.ate("integral_primitiva")
        I2 = self.nomeia("C05_I", tx(r"=\pi\Big[\tfrac{h^2}{4}\,z-\tfrac{z^3}{3}\Big]_{-h/2}^{h/2}", SI,
                                     {H_C: [3, 4, 15, 18], GEO: [7, 9, 10]}, y=Y3))
        self.zona(I2)
        self.entra(I2)
        self.ate("integral_resultado")
        I6 = self.nomeia("C05_I", tx(r"=\dfrac{\pi h^3}{6}", 52 * S, {H_C: [2, 3]}, y=Y3))
        self.play(FadeOut(I2), run_time=0.3)
        self.entra(I6)

        self.ate("rotas_iguais")
        # as duas rotas terminam no mesmo π h³ / 6: a integral sai e o resultado dela sobe pelo slot que ela liberou
        I6b = I6.copy().move_to([0, -1.45, 0])
        self.play(FadeOut(I1), run_time=0.25)
        self.play(Transform(I6, I6b), run_time=0.35)
        lig = DoubleArrow(I6.get_top() + UP * 0.08, cxV.get_bottom() + DOWN * 0.08, color=CIANO, buff=0, stroke_width=4,
                          tip_length=0.16, max_tip_length_to_length_ratio=0.4)
        rot1 = words("CAVALIERI", 0, 32, BRANCO).next_to(cxV, LEFT, buff=0.3)
        rot2 = words("INTEGRAL", 0, 32, BRANCO).next_to(I6, LEFT, buff=0.3).set_x(rot1.get_x())
        self.nomeia("C05_rotas", lig, rot1, rot2)
        self.zona(rot1, rot2, I6)
        self.play(GrowFromCenter(lig), FadeIn(rot1), FadeIn(rot2), Indicate(V5, color=WHITE, scale_factor=1.06),
                  Indicate(I6, color=WHITE, scale_factor=1.1), run_time=0.4)
        self.ate("volume_sai")
        self.sai(V5, cxV, I6, lig, rot1, rot2, rt=0.4)

        # ── C06 · por que é plausível: a parede de cada anel no equador (corte meridiano, mesma escala) ─────────
        self.ate("paredes_entra")
        kp, yc, cols = 0.6, 2.75, [-2.6, 0.0, 2.6]
        paredes, medidas = VGroup(), []
        for r, col, val in zip([5, 7, 10], cols, ["1,00 cm", "0,68 cm", "0,46 cm"]):
            a = np.sqrt(r * r - 9.0)
            e = (r - a) * kp
            pts = ([[0, -3 * kp, 0]] + [[(np.sqrt(r * r - z * z) - a) * kp, z * kp, 0] for z in np.linspace(-3, 3, 61)]
                   + [[0, 3 * kp, 0]])
            pol = Polygon(*pts, fill_color="#2E5BD8", fill_opacity=1, stroke_color=BLUE_L, stroke_width=3)
            pol.shift([col - e / 2, yc, 0])
            borda = Line([col - e / 2, yc - 3 * kp - 0.15, 0], [col - e / 2, yc + 3 * kp + 0.15, 0], color=A_C,
                         stroke_width=3)
            regua = VGroup(Line([col - e / 2, yc, 0], [col + e / 2, yc, 0], color=WHITE, stroke_width=4),
                           *[Line([x, yc - 0.1, 0], [x, yc + 0.1, 0], color=WHITE, stroke_width=4)
                             for x in (col - e / 2, col + e / 2)])
            # L4 (v5): rótulos em Space Grotesk, como os demais
            rr = words(f"R = {r} cm", yc + 3 * kp + 0.42, 26, BRANCO, x=col)
            vv = words(val, yc - 3 * kp - 0.45, 28, BRANCO, x=col)
            paredes.add(VGroup(pol, borda, rr))
            medidas.append(VGroup(regua, vv))
        self.nomeia("C06_paredes", paredes, *medidas)
        self.play(FadeIn(paredes, shift=UP * 0.1), run_time=0.4)
        for tv, m in zip(E["paredes_val"], medidas):
            self.ate(tv)
            self.play(FadeIn(m), run_time=0.4)
        self.ate("paredes_sai")
        self.play(FadeOut(paredes), *[FadeOut(m) for m in medidas], run_time=0.4)

        # ── C06 · prova ao vivo: h fixo, R cresce; R = 100 cm ─────────────────────────────────────────────────
        self.ate("prova_formula_a")
        FA = self.nomeia("C06_FA", tx(r"a=\sqrt{R^2-\tfrac{h^2}{4}}", 52, {A_C: [0], R_C: [4, 5], H_C: [7, 8]}))
        FA.move_to([-2.0, -1.17, 0])
        # o lembrete do C02 volta por 2 s ao lado: a = √(R² − h²/4) é a mesma relação de Pitágoras
        mt = tx(r"R^2-a^2=" + HF + "^2", 58 * S * 0.62, {R_C: [0, 1], A_C: [3, 4], H_C: range(6, 12)})
        mt.move_to([2.15, -1.17, 0])
        mb = fundo(mt, buff=0.14)
        self.nomeia("C06_FA", FA)
        self.nomeia("C06_memo", mt, mb)
        self.zona(FA, VGroup(mt, mb))
        self.entra(FA, extras=[FadeIn(mb), FadeIn(mt, shift=UP * 0.12)])
        self.play(Indicate(mt[0][0:5], color=WHITE, scale_factor=1.08), Indicate(FA[0][2:], color=WHITE, scale_factor=1.06),
                  run_time=0.8)
        self.ate("memo_c06_sai")
        self.sai(mt, mb, rt=0.4)
        self.ate("R100_texto")
        # S13: o contador (Remotion) já saiu por completo quando esta linha entra no mesmo slot
        R1 = self.nomeia("C06_R1", tx(r"R=100\ \text{cm},\quad h=6\ \text{cm}", 48, {R_C: [0], H_C: [8]}, y=-2.04))
        self.zona(R1)
        self.entra(R1)
        self.ate("R100_l2")
        R2 = self.nomeia("C06_R2", tx(r"a=\sqrt{100^2-3^2}=\sqrt{9991}\approx 99{,}96\ \text{cm}", 44, {A_C: [0]}, y=-2.72))
        self.zona(R2)
        self.entra(R2)
        self.ate("R100_l3")
        R3 = self.nomeia("C06_R3", tx(r"V=\dfrac{\pi\cdot 6^3}{6}=36\pi\ \text{cm}^3", 44, y=-3.74))
        cx3 = self.nomeia("C06_R3", fundo(R3))
        self.zona(VGroup(R3, cx3), grupo="C06_R3")
        self.entra(R3, extras=[FadeIn(cx3)])
        self.ate("protecao_c06")
        # a frase de proteção (Remotion) entra nos slots que estas linhas liberam; a conta de V fica
        self.sai(FA, R1, R2, rt=0.4)
        self.ate("prova_sai")
        self.sai(R3, cx3, rt=0.4)

        # ── C07 · casos-limite (vistos no 3D) e fecho ──────────────────────────────────────────────────────────
        SL = 48 * S
        self.ate("limites")
        L1 = self.nomeia("C07_L1", tx(r"a=0\ \Rightarrow\ h=2R", SL, {A_C: [0], H_C: [4], R_C: [7]}, y=-1.45))
        self.zona(L1)
        self.entra(L1)
        self.ate("limite_esfera")
        Yl = -2.9
        L2 = self.nomeia("C07_L", tx(r"V=\dfrac{\pi(2R)^3}{6}", SL, {R_C: [5]}, y=Yl))
        self.zona(L2)
        self.entra(L2)
        self.recua(L1, rt=0.3)
        self.ate("limite_8")
        # (2R)³ = 8R³: os parênteses saem primeiro, o 2 vira 8 no lugar e o expoente passa para o R
        L3 = tx(r"V=\dfrac{\pi\cdot 8R^3}{6}", SL, {R_C: [5]}, y=Yl)
        self.play(FadeOut(L2[0][3]), FadeOut(L2[0][6]), run_time=0.2)
        self.gm(L2, L3, ([0, 1], [0, 1]), ([2], [2]), ([3, 6], FadeOut, {"run_time": 0.05}), ([], [3], {"delay": 0.5}),
                ([4], FadeOut), ([], [4], {"delay": 0.5}), ([5], [5]), ([7], [6]), ([8], [7]), ([9], [8]), rt=0.5)
        self.ate("limite_43")
        # 8/6 = 4/3 (S8): o 4 e o 3 nascem afastados ≥ 6 px; 0,6 s depois a forma limpa
        r8b, r6 = risco(L3[0][4]), risco(L3[0][8])
        qu, tr = nota(L3[0][4], "4", UP), nota(L3[0][8], "3", DOWN)
        self.nomeia("C07_L", qu, tr)
        self.nomeia("C07_L_risco", r8b, r6)
        self.play(Create(r8b), Create(r6), FadeIn(qu), FadeIn(tr), run_time=0.4)
        self.wait(0.6)
        L4 = tx(r"V=\dfrac{4}{3}\pi R^3", SL, {R_C: [6]}, y=Yl)
        # 8/6 = 4/3 → forma limpa: troca no mesmo slot = sai tudo, depois entra
        L3.grupo = L4.grupo = "C07_L"
        self.sai(L3, r8b, r6, qu, tr, rt=0.25)
        self.entra(L4)
        self.ate("limite_zero")
        L5 = self.nomeia("C07_L5", tx(r"h\to 0\ \Rightarrow\ V\to 0", SL, {H_C: [0]}, y=-4.0))
        self.zona(L5)
        self.entra(L5)
        self.ate("limites_sai")
        self.sai(L1, L4, L5, rt=0.3)

        self.ate("conclusao_txt")
        fin = self.nomeia("C07_fin", tx(r"V=\dfrac{\pi h^3}{6}", 60, {H_C: [3, 4]}, y=-3.42))
        cxF = self.nomeia("C07_fin", fundo(fin))
        self.zona(VGroup(fin, cxF), grupo="C07_fin")
        self.acima(fin, cxF)
        self.play(FadeIn(fin, shift=UP * 0.1), FadeIn(cxF), run_time=0.4)
        self.ate("fecho_sai")
        self.sai(fin, cxF, rt=0.4)
        self.fecha("CenaMat")


class CenaUI(Base):
    # LEGADO v1: não é renderizada desde o v2 (o Remotion faz a interface) e não acompanha o timeline v3.
    # Objetos "vivos": refeitos a cada quadro a partir das âncoras/valores do 3D. Não passam por FadeIn/Indicate
    # (interpolar algo que se refaz quebra); a entrada, a saída e o pulso vêm de ValueTrackers.
    def vivo(self, construtor):
        h = VGroup()
        h.alfa, h.pulso = ValueTracker(0), ValueTracker(0)

        def upd(m):
            novo = construtor()
            p = h.pulso.get_value()
            if p > 0:
                novo.scale(1 + 0.15 * p)
            novo.set_opacity(h.alfa.get_value())
            m.become(novo)
        upd(h)
        h.add_updater(upd)
        self.add(h)
        return h

    def entra(self, *vs, rt=0.6, extras=()):
        self.play(*[v.alfa.animate.set_value(1) for v in vs], *extras, run_time=rt)

    def some(self, *vs, rt=0.6, extras=()):
        self.play(*[v.alfa.animate.set_value(0) for v in vs], *extras, run_time=rt)
        for v in vs:
            v.clear_updaters()
            self.remove(v)

    def pulsa(self, *vs, rt=0.8):
        self.play(*[v.pulso.animate(rate_func=there_and_back).set_value(1) for v in vs], run_time=rt)

    def contador(self, fmt, nomes, y=None, anc=None, off=ORIGIN, size=26, color=TEXT_COLOR, t2c=None):
        """Texto numérico (valores do ancoras.json, os mesmos do 3D e do Remotion); cache por string."""
        cache, off = {}, np.array(off, dtype=float)

        def mk():
            s = fmt(*[self.val(n) for n in nomes])
            if s not in cache:
                cache[s] = words(s, 0, size, color, t2c=t2c or {})
            return cache[s].copy().move_to((self.anc(anc) + off) if anc else np.array([0, y, 0]) + off)
        return self.vivo(mk)

    def regua(self, cima, baixo, rotulo="6 cm", cor=H_C, rot_cima=False):
        """Régua vertical ancorada ao 3D: haste + travessões + rótulo à esquerda."""
        t0 = words(rotulo, 0, 20, cor)

        def mk():
            a, b = self.anc(cima), self.anc(baixo)
            g = VGroup(Line(b, a, color=cor, stroke_width=3),
                       Line(a + LEFT * 0.12, a + RIGHT * 0.12, color=cor, stroke_width=3),
                       Line(b + LEFT * 0.12, b + RIGHT * 0.12, color=cor, stroke_width=3))
            t = t0.copy().next_to(g[0], UP if rot_cima else LEFT, buff=0.12)
            if t.get_left()[0] < -4.35:                     # nunca sai do quadro
                t.shift(RIGHT * (-4.35 - t.get_left()[0]))
            g.add(t)
            return g
        return self.vivo(mk)

    def construct(self):
        wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.4).to_corner(UR, buff=0.28)
        serie = words("ABSURDO CALCULÁVEL · EP. 03", 0, 20, TEXT_COLOR).set_opacity(0.65).to_corner(UL, buff=0.4)
        self.add(wm, serie)
        Y_T, Y_T2 = 6.45, 5.8

        # ── C01 · gancho ────────────────────────────────────────────────────────────────────────────────────
        self.ate("hook_titulo")
        tit = words("QUAL TEM MAIS VOLUME?", Y_T, 36)
        self.play(FadeIn(tit, shift=UP * 0.12), run_time=0.7)
        self.ate("hook_rotulos")
        rotR = [self.segue(words(f"R = {r['R']:g} cm", 0, 24, TRIO_C[i], t2c={"R": R_C}), f"rot{i}", lado="esq")
                for i, r in enumerate(G["trio"])]
        self.play(LaggedStart(*[FadeIn(m, shift=LEFT * 0.15) for m in rotR], lag_ratio=0.3), run_time=1.2)
        self.ate("hook_regua")
        reguas = [self.regua(f"regua{i}_cima", f"regua{i}_baixo") for i in range(3)]
        self.entra(*reguas, rt=1.0)
        self.ate("hook_titulo2")
        tit2 = words("MESMA ALTURA: h = 6 cm", Y_T2, 28, t2c={"h = 6 cm": H_C})
        self.play(FadeIn(tit2, shift=UP * 0.1), run_time=0.7)
        self.ate("hook_sai")
        self.some(*reguas, extras=[FadeOut(m) for m in (tit, tit2, *rotR)])
        for m in rotR:
            m.clear_updaters()

        # ── C03 · o raio sumiu ──────────────────────────────────────────────────────────────────────────────
        self.ate("R_sumiu_txt")
        sumiu = words("O RAIO DA ESFERA SUMIU", -4.05, 28, t2c={"RAIO DA ESFERA": R_C})
        self.acima(sumiu)
        self.play(FadeIn(sumiu, shift=UP * 0.1), run_time=0.7)
        self.ate("caixa_area")
        self.play(FadeOut(sumiu), run_time=0.5)

        # ── C04 · Cavalieri: contadores ligados ao z do plano ───────────────────────────────────────────────
        fmtA = lambda v: f"A = {v:.2f}π cm²".replace(".", ",")
        self.ate("cav_contadores")
        cA = self.contador(fmtA, ["A_anel_pi"], anc="anel_base", off=[0, -0.6, 0], size=24)
        cE = self.contador(fmtA, ["A_esfera_pi"], anc="esf_base", off=[0, -0.6, 0], size=24)
        cz = self.contador(lambda z: f"z = {z:+.1f} cm".replace(".", ",").replace("+0,0", "0,0"), ["z"],
                           y=0.15, off=[0, 0, 0], size=22, color=GEO)
        self.entra(cA, cE, cz)
        self.ate("cav_titulo")
        titC = words("MESMA ÁREA EM TODA ALTURA", Y_T, 34)
        self.play(FadeIn(titC, shift=UP * 0.12), run_time=0.7)
        for tp in E["cav_pulso"][1:]:
            self.ate(tp)
            self.pulsa(cA, cE)
        self.ate("cav_conclusao")
        titC2 = words("LOGO, MESMO VOLUME", Y_T2, 30, t2c={"MESMO VOLUME": H_C})   # ⇒ não existe na Space Grotesk
        self.play(FadeIn(titC2, shift=UP * 0.1), run_time=0.7)
        self.ate("cav_sai")
        self.some(cA, cE, cz, rt=0.8, extras=[FadeOut(titC), FadeOut(titC2)])

        # ── C06 · prova ao vivo ─────────────────────────────────────────────────────────────────────────────
        self.ate("prova_contador")
        rg = self.regua("regua_anel_cima", "regua_anel_baixo", "h = 6 cm", rot_cima=True)
        ra = self.contador(lambda R, a: f"R = {R:.1f} cm     a = {a:.1f} cm".replace(".", ","), ["R", "a_furo"],
                           y=-2.3, size=26, t2c={"R =": R_C, "a =": A_C})
        vtxt = words("V = 36π cm³ ≈ 113,1 cm³", 0, 30)
        vchip = chip(vtxt).move_to([0, -3.35, 0])
        self.acima(vchip)
        self.entra(rg, ra, rt=0.7, extras=[FadeIn(vchip)])
        self.ate("forma_muda_txt")
        tf = words("MUDA A FORMA. NÃO MUDA O VOLUME.", Y_T, 32)
        self.play(FadeIn(tf, shift=UP * 0.12), run_time=0.7)
        self.ate("desde_que_txt")
        tf2 = words("DESDE QUE h SEJA A MESMA.", Y_T2, 30, t2c={"h": H_C})
        self.play(FadeIn(tf2, shift=UP * 0.1), run_time=0.7)
        self.ate(E["R100_texto"] - 0.4)
        self.some(ra, rt=0.4, extras=[FadeOut(vchip)])
        self.ate("protecao_c06")
        p1 = words("NÃO É QUALQUER FURO QUE DÁ O MESMO VOLUME.", Y_T, 26)
        p2 = VGroup(words("O QUE PRECISA SER IGUAL É A ALTURA h", Y_T2, 26, t2c={"ALTURA h": H_C}),
                    words("DO ANEL QUE SOBRA.", Y_T2 - 0.5, 26))
        self.play(FadeOut(tf), FadeOut(tf2), run_time=0.4)
        self.play(FadeIn(p1, shift=UP * 0.1), FadeIn(p2, shift=UP * 0.1), run_time=0.8)
        self.ate("prova_sai")
        self.some(rg, extras=[FadeOut(p1), FadeOut(p2)])

        # ── C07 · trio de volta, volumes iguais, conclusão ──────────────────────────────────────────────────
        self.ate("trio_final")
        rotR = [self.segue(words(f"R = {r['R']:g} cm", 0, 22, TRIO_C[i], t2c={"R": R_C}), f"rot{i}", off=[0, 0.22, 0], lado="esq")
                for i, r in enumerate(G["trio"])]
        reguas = [self.regua(f"regua{i}_cima", f"regua{i}_baixo") for i in range(3)]
        self.entra(*reguas, rt=0.8, extras=[FadeIn(m) for m in rotR])
        self.ate("trio_volumes")
        vols = [self.segue(words("V = 36π cm³", 0, 22), f"rot{i}", off=[0, -0.22, 0], lado="esq") for i in range(3)]
        self.play(LaggedStart(*[FadeIn(m, shift=LEFT * 0.15) for m in vols], lag_ratio=0.3), run_time=1.0)
        self.ate("conclusao_txt")
        tc = words("SÓ A ALTURA DETERMINA O VOLUME", Y_T, 32, t2c={"ALTURA": H_C})
        self.play(FadeIn(tc, shift=UP * 0.12), run_time=0.8)
        self.ate("protecao_fecho")
        q1 = words("NÃO É QUALQUER FURO QUE DÁ O MESMO VOLUME.", Y_T, 26)
        q2 = VGroup(words("O QUE PRECISA SER IGUAL É A ALTURA h", Y_T2, 26, t2c={"ALTURA h": H_C}),
                    words("DO ANEL QUE SOBRA.", Y_T2 - 0.5, 26))
        self.play(FadeOut(tc), run_time=0.4)
        self.play(FadeIn(q1, shift=UP * 0.1), FadeIn(q2, shift=UP * 0.1), run_time=0.8)
        self.ate("fecho_sai")
        for m in rotR + vols:
            m.clear_updaters()
        self.some(*reguas, extras=[FadeOut(m) for m in (q1, q2, *rotR, *vols)])

        # ── END · cartão final (separado da conclusão matemática) ───────────────────────────────────────────
        self.ate("endcard")
        self.play(FadeOut(wm), FadeOut(serie), run_time=0.4)
        logo = ImageMobject(str(WATERMARK_PATH)).set_width(4.4).move_to([0, 2.3, 0])
        linha1 = words("SE ESSA CONEXÃO ENTRE EQUAÇÃO\nE FENÔMENO AJUDOU,", -0.2, 30)
        linha2 = words("SEGUE O PARALLAX LAB", -1.45, 38)
        handle = words("@labparallax", -2.6, 40).set_color_by_gradient(CYAN, PINK)
        self.play(FadeIn(logo, scale=0.96), run_time=0.7)
        self.play(FadeIn(linha1, shift=UP * 0.08), run_time=0.6)
        self.play(FadeIn(linha2, shift=UP * 0.08), FadeIn(handle, shift=UP * 0.08), run_time=0.6)
        self.ate("endcard_sai")
        self.play(FadeOut(Group(logo, linha1, linha2, handle)), run_time=0.5)
        self.fecha("CenaUI")
