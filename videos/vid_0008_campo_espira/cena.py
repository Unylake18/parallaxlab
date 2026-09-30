"""Campo magnético no eixo de uma espira: B_z(z) = mu0 I R^2 / 2(R^2+z^2)^{3/2}.

POR TRÁS DA FÓRMULA · EP. 03. Preview silencioso 540x960 / 15 fps.

A fórmula NASCE da geometria. Regras da linguagem visual:

1) OBJETOS PERSISTENTES. A espira, o eixo, P e os segmentos R, z e r ficam em cena o
   vídeo inteiro.
2) A COR ACOMPANHA A VARIÁVEL, do desenho até dentro da equação: o LaTeX carrega a cor
   (\\vR, \\vZ, \\vr, \\vL em comum.py), inclusive dentro de \\frac.
3) TRANSFORMAÇÃO, NÃO TROCA. Cada passo algébrico passa por self.morph, que casa os
   glifos das duas expressões por FORMA (e, no empate, pela cor e pela proximidade):
   os símbolos que continuam viajam até o novo lugar, os que mudam aparecem ou somem
   no próprio lugar. Nada de crossfade da expressão inteira, que parecia corte.
4) RÓTULOS SEM PLACA. halo() contorna cada glifo com a cor do fundo; a placa
   retangular cortava raios, eixos e setas.
5) ESMAECER SEM ESTRAGAR. recua()/volta() usam fade() multiplicativo + Restore: o
   set_opacity(1) antigo PREENCHIA formas abertas (o elemento virava bola cheia, o
   ângulo reto virava triângulo) e reacendia o que era para ficar apagado.

Cadeia, na ordem em que aparece:
  A2  r^2 = R^2 + z^2: cada rótulo do desenho voa para a equação e só então ganha o
      expoente; a equação encolhe e vai para a ficha GEOMETRIA.
  A3  Biot-Savart: dB = (mu0 I/4pi)(dl x r)/r^3. Com dl perpendicular a r o produto
      vetorial vira produto simples; r^3 se abre em r^2 r e o r do numerador cancela
      com o r solto: r/r^3 -> 1/r^2. O resultado vai para a ficha BIOT-SAVART.
  A4  o elemento diametralmente oposto (db_dirs): as transversais se encaixam ponta a
      ponta e fecham o caminho (soma zero); as axiais deslizam ponta a ponta e os dois
      rótulos montam dB_z + dB_z = 2 dB_z. Segue-se com UMA parcela.
  A5  o ângulo entre dB e o eixo é o MESMO ângulo do triângulo; R e r saem do triângulo
      e formam R/r; dB_z = |dB| R/r, e a ficha BIOT-SAVART devolve |dB|.
  A6  a vista de frente nasce da espira e assume o centro; o arco se desenrola:
      dl = R dphi, que vira a ficha ARCO.
  A7  a ficha ARCO devolve R dphi; R x R -> R^2, r^2 x r -> r^3; a ficha GEOMETRIA
      devolve r^3 = (r^2)^{3/2} = (R^2+z^2)^{3/2}.
  A8  B_z = ∫ dB_z é escrito primeiro; o integrando chega por cópia; os fatores sem phi
      saem da integral; os dois pi se cancelam; 2/4 -> 1/2 -> denominador.
  A9  P vai ao centro com z lido em tempo real; z -> 0 na fórmula;
      (R^2)^{3/2} -> R^3; R^2/R^3 -> 1/R.
  A9B a espira encolhe e P segue AO LONGO DO EIXO até z >> R: R^2+z^2 ≃ z^2,
      (z^2)^{3/2} = z^3, B_z ≃ mu0 I R^2 / 2 z^3, logo B_z ∝ 1/z^3 (sem dipolo).
  A10 a fórmula geral volta, vira ficha e a espira é copiada 1 -> 2 -> 3.

O modelo numérico (b_loop, db_dirs, dbz_phi) e as conferências de import estão em
comum.py, junto com a paleta e a infraestrutura de quadro.

SINCRONIA COM A NARRAÇÃO (audio/narracao_final.wav, 152,3 s). Cada self.ancora("X") casa um
ponto do código com um instante da fala (sync.json). Entre duas âncoras, play e wait são
escalados para o trecho durar o que a fala dura; se a cena acabar antes, a âncora seguinte
segura o último quadro. native.json guarda o tempo NATIVO de cada âncora e é regenerado com
    SYNC_CAL=1 uv run python -m manim -r 108,192 --fps 15 videos/vid_0008_campo_espira/cena.py CampoEspira008
sempre que a cena mudar (sem native.json/sync.json a cena roda em tempo nativo, sem áudio).
Os tempos dos comentários de bloco abaixo são os da fala.
"""

import json
import os
import sys
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, PI, RIGHT, UP, Arc, Circle, Create, DashedLine, Dot, FadeIn, FadeOut,
    FadeTransform, Flash, ImageMobject, Scene, Indicate, Line, ReplacementTransform, Restore, SurroundingRectangle, config,
    Transform, TransformFromCopy, TransformMatchingTex, VGroup, VMobject, ValueTracker,
    always_redraw, color_to_rgb, linear, rate_functions,
)

sys.path.insert(0, str(Path(__file__).resolve().parent))   # montar_legendado.py importa esta cena
from comum import (
    BEAT, BLUE, CYAN, CYAN_L, MAGENTA, READ, READ_RES, SAFE_X, VIOLET, WHITE, CenaBase,
    angle_arc, b_loop, by_height, db_dirs, dbz_phi, ficha, ficha_mini, fit, glyphs, halo, mtex, odot,
    otimes, panel, pulse_ring, right_angle, span_mark, tag, tex, text, vec,
)
from template.config import WATERMARK_PATH

SUAVE = rate_functions.ease_in_out_sine

# Termos coloridos na legenda (montar_legendado.py --color-module), com o mesmo significado da cena:
# R ciano, z azul, r violeta, operação/cancelamento/ângulo magenta.
SUBTITLE_TERM_COLORS = {
    "raio": CYAN, "raios": CYAN,
    "distância axial": BLUE,
    "distância": VIOLET,
    "cancelam": MAGENTA, "cancela": MAGENTA, "transversais": MAGENTA,
    "cosseno": MAGENTA, "ângulo": MAGENTA,
    "dois pi": MAGENTA, "pi": MAGENTA,
}

PASTA = Path(__file__).resolve().parent
CAL = os.environ.get("SYNC_CAL") == "1"        # calibragem: mede o tempo NATIVO de cada âncora

# ── Geometria de tela da espira (unidades de tela por R) ────────────────────
DR = 2.35                 # raio desenhado
DOX, DOY = -2.05, 2.45    # centro O da espira
DZ = 1.45                 # z do ponto P, em unidades de R
DTILT = 0.34              # achatamento da profundidade na projeção oblíqua
LDB = 1.50                # comprimento de desenho de dB
D_O = np.array([DOX, DOY, 0.0])
D_P = np.array([DOX + DR * DZ, DOY, 0.0])
D_TOP = np.array([DOX, DOY + DR, 0.0])   # elemento em phi = 0: corrente saindo do plano
D_BOT = np.array([DOX, DOY - DR, 0.0])   # elemento oposto: corrente entrando

# vista de frente: nasce pequena no centro da espira (0) e cresce à direita (1)
AUX_C0, AUX_R0 = D_O.copy(), 0.35
AUX_C1, AUX_R1 = np.array([0.95, 1.05, 0.0]), 1.25
AUX_PHI = 0.40                                       # início do arco dl
AUX_DPHI = 1.00                                      # abertura final de dphi

OP_Y, NOTE_Y = -2.05, -1.00              # expressão ativa e nota curta
SIDE_Y = -0.95                           # linha auxiliar acima da expressão ativa
PAYOFF_Y = -1.95                         # o resultado final, com placa
SHELF_Y = -3.60                          # prateleira: os resultados já estabelecidos
ZREAD = np.array([0.95, 1.55, 0.0])      # leitura de z durante a checagem
STAGE_Y = 0.10                          # onde a ficha ativa se abre, legivel
SIDE2_Y = -1.25                          # linha auxiliar da ficha GEOMETRIA (A7)
EXY7 = -2.30                             # expressão ativa em A7 (abre espaço para ficha e linha auxiliar)
ESC_FAR = 0.30                           # escala da espira na checagem de longe (A9B)
Z_FAR = 7.0                              # z, em unidades de R, na checagem de longe
GX0, GY0, GH = 0.0, -4.15, 0.90            # gráfico: origem z = 0 no eixo, base e altura (B/B(0) = 1)
GXS, GZMAX = 0.44, 7.2                    # unidades de tela por R e semi-largura em z/R
STACK_DX = DR * 0.5                      # deslocamento das espiras do gancho final

# ── Conferências específicas desta cena, no import ──────────────────────────
_R, _zt = 1.0, DZ
_r2 = _R ** 2 + _zt ** 2
_r = np.sqrt(_r2)
assert np.isclose(np.hypot(_R, _zt) ** 2, _r2)                    # r^2 = R^2 + z^2
_d1, _d2 = db_dirs(_zt)
assert np.isclose(np.dot(_d1, [_zt, -_R, 0.0]), 0.0)              # dB perpendicular a r
assert np.isclose(np.dot(_d2, [_zt, _R, 0.0]), 0.0)
assert np.isclose(_d1[1], -_d2[1]) and abs(_d1[1]) > 0            # transversais opostas
_u1, _u2 = _d1 / np.linalg.norm(_d1), _d2 / np.linalg.norm(_d2)
assert np.allclose(_u1 + _u2, [2 * _u1[0], 0.0, 0.0])             # a soma do par é axial…
assert np.isclose(np.linalg.norm(_u1 + _u2), 2 * _u1[0])          # …e vale 2x a projeção de uma
assert np.isclose(_u1[0], _R / _r)                                # fração axial = R/r
# o ângulo dB-eixo em P é o mesmo ângulo do triângulo no elemento
_ang_P = np.arccos(np.dot(_u1, [1.0, 0.0, 0.0]))
_e_to_o, _e_to_p = np.array([0.0, -1.0, 0.0]), np.array([_zt, -_R, 0.0]) / _r
assert np.isclose(_ang_P, np.arccos(np.dot(_e_to_o, _e_to_p)))
assert np.isclose(np.cos(_ang_P), _R / _r)
# dl = R dphi (comprimento de arco) e dB_z = (mu0 I/4pi)(dl/r^2)(R/r)
assert np.isclose(AUX_R1 * AUX_DPHI, AUX_R1 * AUX_DPHI)           # arco = raio x ângulo
assert np.isclose(dbz_phi(_zt), (1.0 / _r2) * (_R / _r) * _R)
assert np.isclose(dbz_phi(_zt), _R ** 2 / _r2 ** 1.5)
assert np.isclose(_r ** 3, _r2 ** 1.5)                            # r^3 = (r^2)^{3/2}
# integrar: só dphi depende de phi; 2pi/(4pi) = 1/2
assert np.isclose(2 * PI / (4 * PI), 0.5)
assert np.isclose(2 * PI * dbz_phi(_zt) / (4 * PI) * 2, b_loop(_zt))   # confere com b_loop
# checagem no centro: z = 0 => r = R e R^2/R^3 = 1/R
assert np.isclose(np.hypot(_R, 0.0), _R) and np.isclose(_R ** 2 / _R ** 3, 1.0 / _R)
assert np.isclose(2 * PI * dbz_phi(0.0) / (4 * PI) * 2, 1.0)
assert np.isclose((_R ** 2) ** 1.5, _R ** 3)                      # (R^2)^{3/2} = R^3
# checagem de longe, AO LONGO DO EIXO: z >> R => R^2+z^2 ≃ z^2 e B_z ≃ mu0 I R^2 / 2 z^3
assert abs(b_loop(Z_FAR) * Z_FAR ** 3 - 1.0) < 0.05               # B_z z^3 -> constante (3% em z = 7 R)
assert abs(b_loop(2 * Z_FAR) / b_loop(Z_FAR) - 1 / 8) < 0.02      # z -> 2z => B -> B/8
assert np.isclose((Z_FAR ** 2) ** 1.5, Z_FAR ** 3)                # (z^2)^{3/2} = z^3
assert DOX + DR * ESC_FAR * Z_FAR + 0.6 < 3.5                      # P e o rótulo cabem na margem
# a geometria desenhada está em verdadeira grandeza
assert np.isclose(np.linalg.norm(D_TOP - D_O) / DR, _R)           # cateto R
assert np.isclose(np.linalg.norm(D_P - D_O) / DR, _zt)            # cateto z
assert np.isclose(np.linalg.norm(D_P - D_TOP) / DR, _r)           # hipotenusa r
assert D_TOP[1] + 0.5 < 6.0 and D_BOT[1] - 0.3 > OP_Y + 1.0       # a espira cabe no quadro
# a vista de frente fica abaixo do eixo (não cobre P) e acima da expressão ativa
assert AUX_C1[1] + AUX_R1 < DOY - 0.1
assert AUX_C1[1] - AUX_R1 - 0.40 - 0.62 > OP_Y + 0.45
assert AUX_C1[0] - AUX_R1 > DOX + DR * DTILT                       # e não encosta na espira
assert GY0 - 0.25 > -4.6 and GX0 + GXS * GZMAX < 3.5           # gráfico acima da legenda e na margem
assert SHELF_Y - 0.45 > -4.6                                       # prateleira acima da legenda


def forma(g):
    """Chave de forma de um glifo, independente de posição e tamanho.

    Traços de fração casam entre si qualquer que seja o comprimento: um traço que
    muda de largura estica, em vez de sumir e reaparecer.
    """
    pts = g.points
    if len(pts) == 0:
        return None
    w, h = g.width, g.height
    if w > 6 * max(h, 1e-6):
        return ("barra",)
    esc = max(w, h, 1e-6)
    p = (pts - g.get_center()) / esc
    idx = np.linspace(0, len(p) - 1, min(len(p), 16)).astype(int)
    return (len(pts),) + tuple(np.round(p[idx, :2].flatten(), 2))


class CampoEspira008(CenaBase):
    op_y, note_y = OP_Y, NOTE_Y

    def check_safe(self):
        """Margens (CenaBase) + nenhuma expressão fantasma na faixa da expressão ativa."""
        super().check_safe()
        vivas = [m for m in self.mobjects
                 if "Tex" in type(m).__name__ and abs(m.get_center()[1] - OP_Y) < 0.45
                 and any(max(g.get_fill_opacity(), g.get_stroke_opacity()) > 0.05
                         for g in m.family_members_with_points())]
        assert len(vivas) <= 1, "expressões empilhadas na faixa ativa: %d [%s]" % (
            len(vivas), ", ".join(getattr(m, "tex_string", "?")[:30] for m in vivas))

    # ── Sincronia com a narração ────────────────────────────────────────────
    # Cada âncora casa um ponto do código com um instante do áudio (sync.json). Entre duas
    # âncoras, play/wait são escalados para o trecho durar o que a fala dura; se a cena
    # acabar antes, a âncora seguinte segura o último quadro até a fala chegar.
    def sync_init(self):
        self.tscale, self.nativos = 1.0, {}
        arq = PASTA / "sync.json"
        self.anc = json.load(open(arq))["anchors"] if arq.exists() else []
        self.nat = json.load(open(PASTA / "native.json")) if (PASTA / "native.json").exists() and not CAL else {}

    def _quadro(self, t):
        """Duração em quadros inteiros, arredondada para o mais próximo (o Manim arredonda para cima)."""
        fps = config.frame_rate
        return max(1, round(t * fps)) / fps

    def play(self, *args, **kwargs):
        if abs(self.tscale - 1.0) > 1e-6 and args and not getattr(self, '_cru', False):
            anims = self.compile_animations(*args, **kwargs)
            for a in anims:
                a.run_time = self._quadro(a.run_time * self.tscale)
            return super().play(*anims)
        return super().play(*args, **kwargs)

    def esperar_cru(self, duracao):
        """Espera SEM escala: Scene.wait chama self.play, que escalaria de novo."""
        self._cru = True
        try:
            Scene.wait(self, duracao)
        finally:
            self._cru = False

    def wait(self, duration=1.0, *a, **k):
        self.esperar_cru(self._quadro(duration * self.tscale))

    def ancora(self, nome):
        agora = self.renderer.time
        if CAL:
            self.nativos[nome] = round(agora, 3)
            if nome == "FIM":
                json.dump(self.nativos, open(PASTA / "native.json", "w"), indent=1)
            return
        if not self.anc or nome not in self.nat:
            return
        nomes = [n for n, _ in self.anc]
        i = nomes.index(nome)
        if os.environ.get("SYNC_DBG") and getattr(self, "_ult", None):
            n0, t0, sc0 = self._ult
            print('DBG %-5s nat %.2f x esc %.2f = %.2f previsto, real %.2f' % (
                n0, self.nat[nome] - self.nat[n0], sc0, (self.nat[nome] - self.nat[n0]) * sc0, agora - t0))
        t_a = self.anc[i][1]
        if agora < t_a:
            self.esperar_cru(t_a - agora)
            agora = t_a
        elif agora - t_a > 0.25:
            print('SYNC atraso %.2f s em %s' % (agora - t_a, nome))
        if i + 1 < len(self.anc):
            prox, t_prox = self.anc[i + 1]
            gap_nat = max(0.2, self.nat[prox] - self.nat[nome])
            self.tscale = float(np.clip((t_prox - agora) / gap_nat * 0.985, 0.45, 2.0))
            self._ult = (nome, agora, self.tscale)
        else:
            self.tscale = 1.0

    # ── Ferramentas de transformação ────────────────────────────────────────
    def tira(self, m):
        """Remove m e TODA a família.

        Scene.remove não desce aos filhos: uma expressão montada peça por peça (cada
        parte entrou por uma animação) continuava na tela depois de "removida", e as
        expressões seguintes se empilhavam por cima dela.
        """
        self.remove(*m.get_family())

    def solda(self, m):
        """Depois de montar uma expressão por partes, ela passa a ser um objeto só."""
        self.tira(m)
        self.add(m)
        return m

    def casar(self, src, dst):
        """Animações que levam cópias dos glifos de src até os glifos de dst.

        Casa cada glifo de dst com um glifo de src de mesma forma, o mais próximo
        (cor diferente pesa como distância extra). Casados viajam; os demais somem ou
        aparecem no próprio lugar. Glifos já apagados em src (cancelados) não entram.
        Devolve (animações, sobras a remover depois do play). src não é tocado.
        """
        S = [g for g in src.family_members_with_points()
             if max(g.get_fill_opacity(), g.get_stroke_opacity()) > 0.05]
        D = list(dst.family_members_with_points())
        kS, kD = [forma(g) for g in S], [forma(g) for g in D]
        cand = []
        for j, d in enumerate(D):
            cd = np.array(color_to_rgb(d.get_fill_color()))
            for i, sg in enumerate(S):
                if kS[i] is None or kS[i] != kD[j]:
                    continue
                dist = float(np.linalg.norm(sg.get_center() - d.get_center()))
                if not np.allclose(np.array(color_to_rgb(sg.get_fill_color())), cd, atol=0.05):
                    dist += 1.0
                cand.append((dist, i, j))
        cand.sort()
        usados_s, usados_d, pares = set(), set(), []
        for _, i, j in cand:
            if i in usados_s or j in usados_d:
                continue
            usados_s.add(i)
            usados_d.add(j)
            pares.append((i, j))
        movers = [S[i].copy() for i, _ in pares]
        ins = [D[j].copy() for j in range(len(D)) if j not in usados_d]
        anims = [Transform(m, D[j].copy()) for m, (_, j) in zip(movers, pares)]
        anims += [FadeOut(S[i].copy()) for i in range(len(S)) if i not in usados_s]
        anims += [FadeIn(x) for x in ins]
        return anims, movers + ins

    def morph(self, src, dst, *extra, run_time=0.9, rate_func=SUAVE):
        """Passo algébrico como transformação real, glifo a glifo (ver casar)."""
        anims, sobras = self.casar(src, dst)
        self.tira(src)
        self.play(*anims, *extra, run_time=run_time, rate_func=rate_func)
        self.remove(*sobras)
        self.add(dst)
        return dst

    def abre(self, small, big, dim=(), run_time=0.90):
        """A mini-ficha da prateleira se abre num card grande e legível.

        Os demais elementos (geometria viva e estática, outras fichas) recuam para
        abrir foco; a mini-ficha de origem fica no lugar. Termina com uma pausa de
        leitura: o espectador nunca lê a versão minúscula.
        """
        self._dim = list(dim)
        self.play(TransformFromCopy(small[0], big[0]), TransformFromCopy(small[1], big[1]),
                  FadeIn(big[2], scale=0.7), *self.recua(self._dim, 0.35),
                  run_time=run_time, rate_func=SUAVE)
        self.wait(0.7)

    def fecha(self, small, big, run_time=0.80):
        """O card volta ao tamanho e ao lugar da prateleira; o resto volta ao normal."""
        self.play(Transform(big[0], small[0].copy()), Transform(big[1], small[1].copy()),
                  FadeOut(big[2], scale=0.7), *self.volta(self._dim),
                  run_time=run_time, rate_func=SUAVE)
        self.tira(big)

    def slot(self, sel, color=MAGENTA):
        """Moldura fina em torno do termo que vai ser substituído: o encaixe."""
        return SurroundingRectangle(sel, color=color, buff=0.09, corner_radius=0.06,
                                    stroke_width=3.5)

    def apaga(self, g, color=MAGENTA):
        """Termo desprezado: acende em magenta, encolhe e some. O original apaga na hora."""
        c = g.copy()
        g.set_opacity(0)
        self.add(c)
        self.play(c.animate.set_color(color).scale(1.6), run_time=0.50)
        self.play(c.animate.scale(0.2).set_opacity(0),
                  Flash(c.get_center(), color=color, line_length=0.12, num_lines=10,
                        flash_radius=0.30), run_time=0.70)
        self.remove(c)

    def pulse(self, sel, color, *extra, scale=1.3, run_time=0.6):
        """Realce de um termo por uma cópia por cima: o original não sai do lugar."""
        c = sel.copy()
        self.add(c)
        self.play(Indicate(c, color=color, scale_factor=scale), *extra, run_time=run_time)
        self.remove(c)

    def cancel(self, a, b, color=MAGENTA):
        """Dois termos iguais acendem, se encontram e somem.

        Anima cópias; os originais apagam na hora, então somem também do próximo morph.
        """
        ca, cb = a.copy(), b.copy()
        a.set_opacity(0)
        b.set_opacity(0)
        self.add(ca, cb)
        meio = (a.get_center() + b.get_center()) / 2
        self.play(ca.animate.set_color(color).scale(1.6), cb.animate.set_color(color).scale(1.6),
                  run_time=0.55)
        self.play(ca.animate.move_to(meio).scale(0.3).set_opacity(0),
                  cb.animate.move_to(meio).scale(0.3).set_opacity(0),
                  Flash(meio, color=color, line_length=0.14, num_lines=12, flash_radius=0.34),
                  run_time=0.80)
        self.remove(ca, cb)

    def recua(self, mobs, nivel):
        """Esmaece geometria viva e estática juntas, sem preencher formas abertas."""
        for m in mobs:
            m.save_state()
        return [self.geo.animate.set_value(nivel)] + [m.animate.fade(1 - nivel) for m in mobs]

    def volta(self, mobs):
        """Desfaz recua() exatamente, cada objeto no seu estado anterior."""
        return [self.geo.animate.set_value(1.0)] + [Restore(m) for m in mobs]

    # ── Objetos vivos ───────────────────────────────────────────────────────
    def dpt(self, phi, dx=0.0):
        """Ponto da espira: y = R cos(phi), profundidade R sin(phi) achatada por DTILT."""
        e = self.esc.get_value()
        return np.array([DOX + dx + DR * e * DTILT * np.sin(phi), DOY + DR * e * np.cos(phi), 0.0])

    def loop(self):
        """A espira; metade de trás (sin phi < 0) mais apagada. Persiste o vídeo inteiro."""
        op = self.loop_op.get_value() * self.geo.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        for near in (False, True):
            phis = np.linspace(0, PI, 41) + (0 if near else PI)
            g.add(VMobject().set_points_as_corners([self.dpt(p) for p in phis])
                  .set_stroke(BLUE, 7, op * (1.0 if near else 0.38)))
        return g

    def stack(self):
        """Gancho final: as espiras seguintes, ainda sem conta nenhuma."""
        op = self.stack_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        for k in (1, 2):
            o = op * float(np.clip(op * 2 - (k - 1), 0.0, 1.0))
            for near in (False, True):
                phis = np.linspace(0, PI, 31) + (0 if near else PI)
                g.add(VMobject().set_points_as_corners([self.dpt(p, k * STACK_DX) for p in phis])
                      .set_stroke(BLUE, 6, o * (1.0 if near else 0.38)))
        return g

    def current(self):
        """Sentido da corrente na face da frente: ela desce na tela (phi = pi/2)."""
        op = self.cur_op.get_value() * self.geo.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        for phi in (PI / 3, PI / 2, 2 * PI / 3):
            c = self.dpt(phi)
            t = np.array([DR * DTILT * np.cos(phi), -DR * np.sin(phi), 0.0])
            t = t / np.linalg.norm(t) * 0.30
            g.add(vec(c - t, c + t, CYAN_L, 4).set_opacity(op))
        return g

    def runner(self):
        """Marcador com cauda que percorre a espira; com trail = 1 deixa o rastro inteiro."""
        op = self.loop_op.get_value() * self.geo.get_value() * self.run_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        end, tr = self.phi.get_value(), self.trail.get_value()
        if tr > 0.01 and end > 1e-3:
            for a, b, o in ((0.0, min(end, PI), 1.0), (PI, end, 0.38)):
                if b > a + 1e-3:
                    pts = [self.dpt(p) for p in np.linspace(a, b, max(2, int(36 * (b - a))))]
                    g.add(VMobject().set_points_as_corners(pts).set_stroke(CYAN_L, 11, op * tr * o))
        # cauda curta: é o que faz o ponto ler como corrente correndo
        cauda, n = 0.9, 7
        for k in range(n):
            a = end - cauda + cauda * k / n
            b = end - cauda + cauda * (k + 1) / n
            if b <= 0:
                continue
            a = max(a, 0.0)
            o = 1.0 if np.sin(((a + b) / 2) % (2 * PI)) >= 0 else 0.38
            pts = [self.dpt(t) for t in np.linspace(a, b, 4)]
            g.add(VMobject().set_points_as_corners(pts)
                  .set_stroke(CYAN_L, 8, op * o * (k + 1) / n * (1 - 0.6 * tr)))
        return g.add(Dot(self.dpt(end % (2 * PI)), 0.12, color=CYAN_L).set_opacity(op))

    def p_point(self):
        """P sobre o eixo, a z do centro (z = self.dz, em unidades de R)."""
        return np.array([DOX + DR * self.esc.get_value() * self.dz.get_value(), DOY, 0.0])

    def triangle(self):
        """Cateto z (azul) e hipotenusa r (violeta) + P: seguem P e colapsam em z = 0.

        Com far = 1 os segmentos somem e fica só P, para a checagem de longe.
        """
        op = self.tri_op.get_value() * self.geo.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        p, zl = self.p_point(), DR * self.esc.get_value() * self.dz.get_value()
        sop = op * (1.0 - self.far.get_value())
        if sop > 0.01:
            if zl > 0.14:
                g.add(Line(D_O, p).set_stroke(BLUE, 4, sop))
                g.add(halo(tex("z", 38, BLUE)).move_to([(DOX + p[0]) / 2, DOY - 0.38, 0])
                      .set_opacity(sop))
            g.add(Line(D_TOP, p).set_stroke(VIOLET, 5, sop))
            g.add(halo(tex("r", 38, VIOLET)).move_to((D_TOP + p) / 2 + np.array([0.34, 0.28, 0]))
                  .set_opacity(sop))
        pop = op * self.p_op.get_value()
        if pop > 0.01:
            g.add(Dot(p, 0.1, color=WHITE).set_opacity(pop))
            g.add(halo(tex("P", 36)).move_to(p + np.array([-0.26, -0.40, 0])).set_opacity(pop))
        return g

    def axial_arrow(self):
        """Seta axial em P: mostra que com z = 0 o campo continua puramente axial."""
        op = self.ax_op.get_value() * self.geo.get_value()
        if op < 0.01:
            return VMobject()
        p = self.p_point()
        # o comprimento acompanha B_z(z): cresce ao chegar ao centro e cai com z^3 longe
        L = max(0.06, 1.3 * float(b_loop(self.dz.get_value())))
        return vec(p, p + RIGHT * L, CYAN, 8).set_opacity(op)

    def aux_view(self):
        """Vista de frente: nasce no centro da espira, cresce à direita e o arco acende."""
        op = self.aux_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        k = self.aux_grow.get_value()
        c = AUX_C0 + (AUX_C1 - AUX_C0) * k
        rad = AUX_R0 + (AUX_R1 - AUX_R0) * k
        d = self.dphi.get_value()
        p0, p1 = AUX_PHI, AUX_PHI + d
        g.add(Circle(rad, color=BLUE, stroke_width=4).set_stroke(opacity=op).move_to(c))
        g.add(Dot(c, 0.05, color=WHITE).set_opacity(0.7 * op))
        for a in (p0, p1):
            g.add(Line(c, c + rad * np.array([np.cos(a), np.sin(a), 0]))
                  .set_stroke(CYAN, 2.5 + 1.5 * k, 0.85 * op))
        if d > 0.02:
            g.add(Arc(rad, p0, d, arc_center=c).set_stroke(CYAN_L, 9 + 4 * k, op))
            g.add(Arc(0.18 + 0.27 * k, p0, d, arc_center=c).set_stroke(WHITE, 2.5, 0.9 * op))
        return g

    def z_read(self):
        """z lido em tempo real enquanto P anda (passos de 0,05 para reaproveitar o cache)."""
        op = self.zr_op.get_value()
        if op < 0.01:
            return VMobject()
        v = round(max(0.0, self.dz.get_value()) * 20) / 20
        txt = ("%.2f" % v).replace(".", "{,}")
        return halo(mtex(r"\vZ", "=", txt, r"\,\vR", size=34)).move_to(ZREAD).set_opacity(op)

    def graph(self):
        """B_z/B_z(0) contra z/R, normalizado; o dot segue P (self.dz) sobre a curva."""
        op = self.gr_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        zs = np.linspace(-GZMAX, GZMAX, 260)
        pts = [[GX0 + GXS * z, GY0 + GH * float(b_loop(z)), 0] for z in zs]
        g.add(Line([GX0 - GXS * GZMAX - 0.1, GY0, 0], [GX0 + GXS * GZMAX + 0.1, GY0, 0])
              .set_stroke(WHITE, 1.6, 0.35 * op))
        g.add(Line([GX0, GY0 - 0.08, 0], [GX0, GY0 + GH + 0.20, 0]).set_stroke(WHITE, 1.6, 0.30 * op))
        g.add(VMobject().set_points_as_corners(pts).set_stroke(CYAN, 5, op))
        z = self.dz.get_value()
        d = np.array([GX0 + GXS * z, GY0 + GH * float(b_loop(z)), 0.0])
        g.add(Line([d[0], GY0, 0], d).set_stroke(MAGENTA, 1.6, 0.45 * op))
        g.add(Dot(d, 0.20, color=MAGENTA).set_opacity(0.22 * op))
        g.add(Dot(d, 0.09, color=MAGENTA).set_opacity(op))
        return g

    # ── Cena ────────────────────────────────────────────────────────────────
    def construct(self):
        self.start_frame()
        self.sync_init()
        watermark = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35)
        self.add(watermark.to_corner(UP + RIGHT, buff=0.28))
        series = text("POR TRÁS DA FÓRMULA · EP. 03", 20, opacity=0.65).to_corner(UP + LEFT, buff=0.4)

        self.loop_op, self.cur_op, self.stack_op = (ValueTracker(0) for _ in range(3))
        self.phi, self.dz = ValueTracker(0), ValueTracker(DZ)
        self.tri_op, self.p_op, self.ax_op = (ValueTracker(0) for _ in range(3))
        self.aux_op, self.dphi, self.aux_grow = (ValueTracker(0) for _ in range(3))
        self.run_op, self.trail, self.zr_op = (ValueTracker(0) for _ in range(3))
        self.geo = ValueTracker(1.0)          # esmaecimento da geometria viva
        self.esc, self.far = ValueTracker(1.0), ValueTracker(0.0)
        self.gr_op = ValueTracker(0.0)
        self.add(self.phi, self.dz, self.dphi, self.geo, self.aux_grow, self.esc, self.far, self.gr_op)

        loop = always_redraw(self.loop)
        stack = always_redraw(self.stack)
        cur = always_redraw(self.current)
        run = always_redraw(self.runner)
        tri = always_redraw(self.triangle)
        axarr = always_redraw(self.axial_arrow)
        aux = always_redraw(self.aux_view)
        zread = always_redraw(self.z_read)
        graf = always_redraw(self.graph)
        self.add(stack, loop, run, cur, tri, axarr, aux, zread, graf)
        self.bleed = [series, stack]
        self.add(series)

        # a prateleira: três fichas montadas já nas posições finais, que entram uma a uma
        f_geo = ficha_mini("GEOMETRIA", mtex(r"\vr^2", "=", r"\cdots", size=32))
        f_bs = ficha_mini("BIOT-SAVART", mtex(r"\left|d\vec B\right|", size=32))
        f_arc = ficha_mini("ARCO", mtex(r"\vL", size=32))
        big_geo = ficha("GEOMETRIA", mtex(r"\vr", r"^2", "=", r"\vR", r"^2", "+", r"\vZ", r"^2",
                                          size=66), lab_size=26)
        big_bs = ficha("BIOT-SAVART", mtex(r"\left|d\vec B\right|", "=", r"\frac{\mu_0 I}{4\pi}",
                                           r"\frac{\vL}{\vr^2}", size=60), lab_size=26)
        big_arc = ficha("ARCO", mtex(r"\vL", "=", r"\vR", r"\,d\phi", size=72), lab_size=26)
        for b, dy in ((big_geo, 0.0), (big_bs, -0.05), (big_arc, 0.0)):
            fit(b, 6.6).move_to([0, STAGE_Y + dy, 0])
        fila = VGroup(f_geo, f_bs, f_arc).arrange(RIGHT, buff=0.30)
        fit(fila, 2 * SAFE_X - 0.2).move_to([0, SHELF_Y, 0])

        # ══ A1. O gancho: a espira viva e a pergunta junto de P (0–8 s) ════════════════════════════════
        self.ancora("A1")
        self.play(FadeIn(series), *self.caption("DE ONDE VEM O CAMPO",
                                                "MAGNÉTICO DE UMA ESPIRA?"),
                  self.loop_op.animate.set_value(1), run_time=0.90)
        el_top = odot(D_TOP, CYAN_L)
        i_lab = halo(tex("I", 36, CYAN_L)).next_to(el_top, LEFT, 0.18)
        self.play(FadeIn(el_top), FadeIn(i_lab), self.cur_op.animate.set_value(1),
                  self.run_op.animate.set_value(1), run_time=0.70)
        # a corrente corre: uma volta do marcador com cauda
        self.play(self.phi.animate.set_value(2 * PI), run_time=1.80, rate_func=linear)

        self.ancora("A1b")
        axis_line = DashedLine(D_O + LEFT * 0.60, D_P + RIGHT * 1.25, dash_length=0.12
                               ).set_stroke(BLUE, 2, 0.55)
        z_axis_lab = halo(tex("z", 30, BLUE)).move_to(D_P + np.array([1.45, 0.0, 0])).set_opacity(0.8)
        p_dot = Dot(D_P, 0.10, color=WHITE)
        p_lab = halo(tex("P", 36)).move_to(D_P + np.array([-0.26, -0.40, 0]))
        ring, ring_anim = pulse_ring(D_P, WHITE, 0.62)
        self.add(ring)
        self.play(Create(axis_line), FadeIn(z_axis_lab), FadeIn(p_dot), FadeIn(p_lab),
                  self.run_op.animate.set_value(0), run_time=0.70)
        self.phi.set_value(0.0)
        ask = halo(tag("QUAL É O CAMPO AQUI?", 34, 0.95)).move_to([0.30, -1.55, 0])
        guia = DashedLine(D_P + DOWN * 0.55, [0.30, -1.15, 0], dash_length=0.10
                          ).set_stroke(WHITE, 1.6, 0.30)
        self.play(ring_anim, FadeIn(ask, shift=UP * 0.12), Create(guia), run_time=0.85)
        self.remove(ring)
        self.check_safe()
        self.wait(READ_RES)

        # ══ A2. A geometria: r² = R² + z² sai dos rótulos do desenho (8–23 s) ══════════════════════════
        self.ancora("A2")
        self.play(*self.caption("COMEÇA PELA GEOMETRIA"), FadeOut(ask), FadeOut(i_lab),
                  FadeOut(guia), self.cur_op.animate.set_value(0.40), run_time=0.64)
        seg_R = Line(D_O, D_TOP).set_stroke(CYAN, 5)
        lab_R = halo(tex("R", 38, CYAN)).move_to(D_O + np.array([-0.32, DR / 2, 0]))
        seg_z = Line(D_O, D_P).set_stroke(BLUE, 4)
        lab_z = halo(tex("z", 38, BLUE)).move_to([(DOX + D_P[0]) / 2, DOY - 0.38, 0])
        corner = right_angle(D_O, RIGHT, UP, 0.24, WHITE, 0.6)
        seg_r = Line(D_TOP, D_P).set_stroke(VIOLET, 5)
        lab_r = halo(tex("r", 38, VIOLET)).move_to((D_TOP + D_P) / 2 + np.array([0.34, 0.28, 0]))
        self.ancora("A2b")
        self.play(Create(seg_R), FadeIn(lab_R), run_time=0.60)
        self.play(Create(seg_z), FadeIn(lab_z), Create(corner), run_time=0.60)
        self.play(Create(seg_r), FadeIn(lab_r), run_time=0.60)
        self.wait(BEAT)

        # cada rótulo voa e pousa sobre si mesmo na equação; só depois vêm os expoentes
        self.ancora("A2c")
        pit = mtex(r"\vr", r"^2", "=", r"\vR", r"^2", "+", r"\vZ", r"^2", size=58)
        fit(pit).move_to([0, self.op_y, 0])
        self.play(TransformFromCopy(lab_r, pit[0], path_arc=-0.7),
                  TransformFromCopy(lab_R, pit[3], path_arc=0.7),
                  TransformFromCopy(lab_z, pit[6], path_arc=0.45),
                  run_time=1.15, rate_func=SUAVE)
        self.play(*(FadeIn(pit[i], shift=DOWN * 0.08) for i in (1, 4, 7)),
                  FadeIn(pit[2]), FadeIn(pit[5]), run_time=0.60)
        self.expr = self.solda(pit)
        # os segmentos do desenho passam a ser os do tracker (seguem P daqui em diante)
        self.add(tri)
        self.play(FadeOut(VGroup(seg_z, seg_r, lab_z, lab_r, p_dot, p_lab)),
                  self.tri_op.animate.set_value(1), self.p_op.animate.set_value(1),
                  run_time=0.50)
        self.check_safe()
        self.wait(READ_RES)

        # a própria equação encolhe e vai para a prateleira
        self.ancora("A2d")
        self.play(FadeIn(f_geo[0]), FadeIn(f_geo[1]), FadeTransform(pit, f_geo[2]),
                  run_time=0.90, rate_func=SUAVE)
        self.solda(f_geo)
        self.expr = None
        self.wait(BEAT)

        # ══ A3. Biot-Savart: r³ se abre e o r do numerador cancela com o r solto (23–37 s) ═════════════
        self.ancora("A3")
        self.play(*self.caption("BIOT-SAVART"), run_time=0.58)
        bs = mtex(r"d\vec B", "=", r"\frac{\mu_0 I}{4\pi}", r"\frac{\vLv\times\vrv}{\vr^3}", size=48)
        fit(bs).move_to([0, self.op_y, 0])
        self.play(FadeIn(bs, shift=UP * 0.10), run_time=0.70)
        self.expr = bs
        # o elemento no fio e o termo na fórmula acendem juntos; depois r no desenho e na fórmula
        self.ancora("A3b")
        dl_lab = halo(tex(r"d\vec\ell", 34, CYAN_L)).next_to(el_top, UP, 0.18)
        self.pulse(glyphs(bs[3], CYAN_L), CYAN_L, Indicate(el_top, color=CYAN_L, scale_factor=1.5),
                   FadeIn(dl_lab), run_time=0.70)
        r_flash = tri[2].copy().set_stroke(VIOLET, 9, 1.0)   # cópia estática: tri é redesenhado
        self.add(r_flash)
        self.pulse(glyphs(bs[3], VIOLET), VIOLET, Indicate(r_flash, color=VIOLET, scale_factor=1.0),
                   run_time=0.64)
        self.remove(r_flash)
        rhat = (D_P - D_TOP) / np.linalg.norm(D_P - D_TOP)
        perp_mark = right_angle(D_TOP, rhat, np.array([-rhat[1], rhat[0], 0.0]), 0.22, CYAN_L, 0.95)
        self.play(Create(perp_mark), run_time=0.52)
        self.note(tag("o seno de 90 graus vale 1", 22, 0.85))

        # com dl perpendicular a r, o produto vetorial vira produto simples
        dot_form = mtex(r"\left|d\vec B\right|", "=", r"\frac{\mu_0 I}{4\pi}",
                        r"\frac{\vL\,\vr}{\vr^3}", size=48)
        fit(dot_form).move_to([0, self.op_y, 0])
        self.morph(bs, dot_form, run_time=0.95)
        self.wait(BEAT)
        # r³ = r²·r: o r extra fica à mostra, e é ele que cancela com o do numerador
        self.ancora("A3c")
        dot2 = mtex(r"\left|d\vec B\right|", "=", r"\frac{\mu_0 I}{4\pi}",
                    r"\frac{\vL\,\vr}{\vr^2\,\vr}", size=48)
        fit(dot2).move_to([0, self.op_y, 0])
        self.morph(dot_form, dot2, run_time=0.80)
        self.wait(BEAT)
        viol = by_height(glyphs(dot2[3], VIOLET))
        solto = max(viol[1:], key=lambda g: g.get_center()[0])
        self.cancel(viol[0], solto)
        mag = mtex(r"\left|d\vec B\right|", "=", r"\frac{\mu_0 I}{4\pi}", r"\frac{\vL}{\vr^2}", size=48)
        fit(mag).move_to([0, self.op_y, 0])
        self.morph(dot2, mag, FadeOut(perp_mark), run_time=0.85)
        self.expr = mag
        self.note(None)
        self.check_safe()
        self.wait(READ_RES)

        d1, d2 = db_dirs(DZ)
        u1, u2 = d1 / np.linalg.norm(d1), d2 / np.linalg.norm(d2)
        db1 = vec(D_P, D_P + LDB * u1, WHITE, 6)
        db1_lab = halo(tex(r"d\vec B_1", 30)).next_to(db1.get_end(), RIGHT, 0.12)
        # a seta nasce enquanto o |dB| da fórmula acende: é a mesma grandeza
        self.pulse(mag[0], WHITE, Create(db1), FadeIn(db1_lab), scale=1.15, run_time=0.80)
        self.check_safe()
        self.wait(BEAT)

        # ══ A4. Elementos opostos: as transversais fecham o caminho; as axiais somam (37–54 s) ═════════
        self.ancora("A4")
        self.play(*self.caption("ELEMENTOS OPOSTOS"), FadeIn(f_bs[0]), FadeIn(f_bs[1]),
                  FadeTransform(mag, f_bs[2]), run_time=0.90, rate_func=SUAVE)
        self.solda(f_bs)
        self.expr = None
        self.ancora("A4b")
        el_bot = otimes(D_BOT, CYAN_L)
        seg_r2 = Line(D_BOT, D_P).set_stroke(VIOLET, 4, 0.5)
        db2 = vec(D_P, D_P + LDB * u2, WHITE, 6)
        db2_lab = halo(tex(r"d\vec B_2", 30)).next_to(db2.get_end(), RIGHT, 0.12)
        self.play(FadeIn(el_bot), Create(seg_r2), run_time=0.58)
        self.play(Create(db2), FadeIn(db2_lab), run_time=0.64)
        self.wait(BEAT)

        # decompor: axial (ciano) + transversal (magenta)
        self.ancora("A4c")
        a_len = LDB * float(u1[0])                     # projeção axial de UMA contribuição
        ax_end = D_P + RIGHT * a_len
        top_t, bot_t = D_P + LDB * u1, D_P + LDB * u2
        ax1 = vec(D_P, ax_end, CYAN, 6)
        ax2v = vec(D_P, ax_end, CYAN, 6)
        t1 = vec(ax_end, top_t, MAGENTA, 9)
        t2 = vec(ax_end, bot_t, MAGENTA, 9)
        self.play(Create(ax1), Create(t1), Create(ax2v), Create(t2),
                  FadeOut(VGroup(db1, db2, db1_lab, db2_lab)), run_time=0.84)
        self.check_safe()
        self.wait(BEAT)

        # a transversal de baixo sobe e se encaixa na ponta da de cima: o caminho fecha
        self.ancora("A4d")
        self.play(*self.caption("TRANSVERSAIS CANCELAM"), run_time=0.52)
        self.play(Transform(t2, vec(top_t, ax_end, MAGENTA, 9)), run_time=0.95, rate_func=SUAVE)
        zero_mark = halo(tex(r"\vec 0", 36, MAGENTA)).move_to(ax_end + np.array([0.62, 0.30, 0]))
        self.play(FadeOut(VGroup(t1, t2), scale=0.15),
                  Flash(ax_end, color=MAGENTA, line_length=0.20, num_lines=14, flash_radius=0.46),
                  FadeIn(zero_mark, scale=1.5), run_time=0.80)
        self.check_safe()
        self.wait(READ)

        # as axiais deslizam ponta a ponta e os dois rótulos montam a soma
        lab1 = halo(tex("dB_z", 30, CYAN)).next_to(ax1, UP, 0.12)
        lab2 = halo(tex("dB_z", 30, CYAN)).next_to(ax1, DOWN, 0.12)
        self.ancora("A4e")
        self.play(*self.caption("AXIAIS SOMAM"), FadeOut(zero_mark), FadeIn(lab1), FadeIn(lab2),
                  run_time=0.64)
        ax_sum = vec(ax_end, ax_end + RIGHT * a_len, CYAN, 6)
        self.play(Transform(ax2v, ax_sum), lab2.animate.next_to(ax_sum, DOWN, 0.12),
                  run_time=0.90, rate_func=SUAVE)
        sum_span = span_mark(D_P + DOWN * 0.86, ax_end + RIGHT * a_len + DOWN * 0.86, WHITE, op=0.7)
        self.play(Create(sum_span), run_time=0.52)
        soma = mtex(r"\vB", "+", r"\vB", "=", r"2\,\vB", size=50)
        fit(soma).move_to([0, self.op_y, 0])
        # os rótulos descem casando glifo a glifo (o índice dos glifos não coincide)
        a1, s1 = self.casar(lab1, soma[0])
        a2, s2 = self.casar(lab2, soma[2])
        self.play(*a1, *a2, FadeIn(soma[1]), run_time=0.95, rate_func=SUAVE)
        self.remove(*s1, *s2)
        self.add(soma[0], soma[1], soma[2])
        # as duas parcelas viram uma só, vezes dois
        a3, s3 = self.casar(VGroup(soma[0], soma[2]), soma[4])
        self.play(*a3, FadeIn(soma[3]), run_time=0.84, rate_func=SUAVE)
        self.remove(*s3)
        self.expr = self.solda(soma)
        self.check_safe()
        self.wait(READ_RES + 0.8)

        # segue-se com UMA parcela; a outra vira fantasma, e a soma fica só com ela
        self.ancora("A4f")
        one_lab = halo(tex("dB_z", 32, CYAN)).next_to(ax1, DOWN, 0.16)
        one = mtex(r"\vB", size=50).move_to(soma[0])
        self.morph(soma, one, FadeOut(VGroup(sum_span, lab1, lab2)), FadeIn(one_lab),
                   ax2v.animate.fade(0.82), run_time=0.80)
        self.expr = one
        self.wait(BEAT)

        # ══ A5. Só sobra o eixo: cos α = R/r, e a ficha BIOT-SAVART devolve |dB| (54–72 s) ═════════════
        self.ancora("A5")
        self.play(*self.caption("SÓ SOBRA O EIXO"), run_time=0.58)
        self.ancora("A5b")
        db1b = vec(D_P, D_P + LDB * u1, WHITE, 5)
        ang_db = float(np.arctan2(u1[1], u1[0]))
        arc_p = angle_arc(D_P, D_P + RIGHT, D_P + u1, 0.52, MAGENTA, 1.0, 6)
        al_p = halo(tex(r"\alpha", 38, MAGENTA)).move_to(
            D_P + 0.82 * np.array([np.cos(ang_db / 2), np.sin(ang_db / 2), 0]))
        be = (-PI / 2 + float(np.arctan2(*(D_P - D_TOP)[1::-1]))) / 2
        arc_e = angle_arc(D_TOP, D_O, D_P, 0.52, MAGENTA, 1.0, 6)
        al_e = halo(tex(r"\alpha", 38, MAGENTA)).move_to(
            D_TOP + 0.74 * np.array([np.cos(be), np.sin(be), 0]))
        self.play(Create(db1b), Create(arc_p), FadeIn(al_p), run_time=0.70)
        self.add(one_lab)        # a seta de dB acabou de entrar: o rótulo volta para a frente
        self.play(Create(arc_e), FadeIn(al_e), run_time=0.64)
        mesmo = halo(tag("MESMO ÂNGULO", 26, 1.0, MAGENTA)).move_to([1.15, 4.75, 0])
        self.play(FadeIn(mesmo, scale=1.1), Indicate(arc_p, color=MAGENTA, scale_factor=1.35),
                  Indicate(arc_e, color=MAGENTA, scale_factor=1.35), run_time=0.90)
        self.check_safe()
        self.wait(BEAT)

        proj = mtex(r"\frac{\vB}{\left|d\vec B\right|}", "=", r"\cos\vA", size=48)
        fit(proj).move_to([0, self.op_y, 0])
        self.morph(one, proj, FadeOut(mesmo), run_time=0.85)
        self.wait(BEAT)
        # R e r saem do triângulo e se encaixam na fração
        self.ancora("A5c")
        proj2 = mtex(r"\frac{\vB}{\left|d\vec B\right|}", "=", r"\cos\vA", "=",
                     r"\frac{\vR}{\vr}", size=48)
        fit(proj2).move_to([0, self.op_y, 0])
        alvo_R = glyphs(proj2[4], CYAN).get_center()
        alvo_r = glyphs(proj2[4], VIOLET).get_center()
        self.play(ReplacementTransform(proj[0], proj2[0]), ReplacementTransform(proj[1], proj2[1]),
                  ReplacementTransform(proj[2], proj2[2]), FadeIn(proj2[3]), run_time=0.70)
        frac_Rr = proj2[4].set_opacity(0)
        self.add(frac_Rr)
        voa_R, voa_r = lab_R.copy(), tri[3].copy()
        self.add(voa_R, voa_r)
        self.play(voa_R.animate.move_to(alvo_R).scale(0.62).set_opacity(0),
                  voa_r.animate.move_to(alvo_r).scale(0.62).set_opacity(0),
                  frac_Rr.animate.set_opacity(1), run_time=1.00, rate_func=SUAVE)
        self.remove(voa_R, voa_r)
        self.expr = self.solda(proj2)
        self.check_safe()
        self.wait(READ_RES)

        # dB_z = |dB| · R/r: o |dB| sobe do denominador para a direita
        self.ancora("A5d")
        proj3 = mtex(r"\vB", "=", r"\left|d\vec B\right|", r"\cdot", r"\frac{\vR}{\vr}", size=48)
        fit(proj3).move_to([0, self.op_y, 0])
        self.morph(proj2, proj3, run_time=0.95)
        self.wait(READ)
        # a ficha BIOT-SAVART acende e manda o que |dB| vale
        chain = mtex(r"\vB", "=", r"\frac{\mu_0 I}{4\pi}", r"\frac{\vL}{\vr^2}", r"\cdot",
                     r"\frac{\vR}{\vr}", size=46)
        fit(chain).move_to([0, self.op_y, 0])
        self.ancora("A5e")
        sl5 = self.slot(proj3[2])
        self.play(Create(sl5), proj3[2].animate.set_color(MAGENTA), run_time=0.55)
        dim5 = [seg_R, lab_R, el_top, el_bot, dl_lab, axis_line, z_axis_lab, corner, seg_r2,
                ax1, ax2v, one_lab, db1b, arc_p, arc_e, al_p, al_e, f_geo]
        self.abre(f_bs, big_bs, dim=dim5)
        voo = VGroup(big_bs[2][2], big_bs[2][3]).copy()
        self.play(ReplacementTransform(proj3[0], chain[0]), ReplacementTransform(proj3[1], chain[1]),
                  ReplacementTransform(proj3[3], chain[4]), ReplacementTransform(proj3[4], chain[5]),
                  FadeOut(proj3[2], shift=UP * 0.25), FadeOut(sl5),
                  FadeTransform(voo, VGroup(chain[2], chain[3])), run_time=1.05, rate_func=SUAVE)
        self.expr = self.solda(chain)
        self.fecha(f_bs, big_bs)
        self.check_safe()
        self.wait(BEAT)

        # ══ A6. Arco = raio × ângulo: a vista de frente nasce da espira (72–81 s) ══════════════════════
        self.ancora("A6")
        self.play(*self.caption("ARCO = RAIO VEZES ÂNGULO"),
                  FadeOut(VGroup(arc_p, arc_e, al_p, al_e, db1b)), run_time=0.58)
        self.ancora("A6b")
        fundo = [seg_R, lab_R, el_top, el_bot, dl_lab, axis_line, z_axis_lab, corner, seg_r2,
                 ax1, ax2v, one_lab, f_geo, f_bs]
        self.play(self.aux_op.animate.set_value(1), self.aux_grow.animate.set_value(1.0),
                  *self.recua(fundo, 0.08), run_time=1.20, rate_func=SUAVE)
        mid = AUX_PHI + AUX_DPHI / 2
        # R fora da cunha, junto do primeiro raio; dphi na bissetriz, entre o arco interno e a borda
        base_R = AUX_C1 + 0.60 * np.array([np.cos(AUX_PHI), np.sin(AUX_PHI), 0])
        normal = np.array([np.sin(AUX_PHI), -np.cos(AUX_PHI), 0])
        aux_R = halo(tex("R", 30, CYAN)).move_to(base_R + 0.24 * normal)
        self.play(FadeIn(aux_R), self.dphi.animate.set_value(AUX_DPHI), run_time=0.90)
        aux_dphi = halo(tex(r"d\phi", 30)).move_to(
            AUX_C1 + 0.80 * np.array([np.cos(mid), np.sin(mid), 0]))
        self.play(FadeIn(aux_dphi), run_time=0.50)
        self.wait(BEAT)

        # o arco se desenrola num segmento reto: esse é o comprimento dl
        self.ancora("A6c")
        arco_src = Arc(AUX_R1, AUX_PHI, AUX_DPHI, arc_center=AUX_C1).set_stroke(CYAN_L, 13)
        comp = AUX_R1 * AUX_DPHI
        y_reta = AUX_C1[1] - AUX_R1 - 0.40
        reta = Line(np.array([AUX_C1[0] - comp / 2, y_reta, 0]),
                    np.array([AUX_C1[0] + comp / 2, y_reta, 0])).set_stroke(CYAN_L, 13)
        self.add(arco_src)
        self.play(Transform(arco_src, reta), run_time=1.00, rate_func=SUAVE)
        self.wait(0.6)
        dl_eq = mtex(r"\vL", "=", r"\vR", r"\,d\phi", size=46).move_to([AUX_C1[0], y_reta - 0.62, 0])
        self.play(FadeTransform(arco_src.copy(), dl_eq[0]), FadeIn(dl_eq[1]),
                  TransformFromCopy(aux_R, dl_eq[2]), TransformFromCopy(aux_dphi, dl_eq[3]),
                  run_time=1.05)
        self.solda(dl_eq)
        self.check_safe()
        self.wait(READ_RES)

        # a igualdade vai para a prateleira e a geometria volta como estava
        self.ancora("A7")
        self.play(*self.caption("ENCAIXA AS PEÇAS"),
                  FadeIn(f_arc[0]), FadeIn(f_arc[1]), FadeTransform(dl_eq, f_arc[2]),
                  self.aux_op.animate.set_value(0), FadeOut(VGroup(aux_R, aux_dphi, arco_src)),
                  *self.volta(fundo), run_time=1.10, rate_func=SUAVE)
        self.solda(f_arc)

        # ══ A7. Encaixa as peças: ficha ARCO, R·R, r²·r e ficha GEOMETRIA (81–98 s) ════════════════════
        # a ficha ARCO se abre; R dφ sai dela e substitui dℓ (o termo trocado fica magenta)
        step2 = mtex(r"\vB", "=", r"\frac{\mu_0 I}{4\pi}", r"\frac{\vR\,d\phi}{\vr^2}", r"\cdot",
                     r"\frac{\vR}{\vr}", size=46)
        fit(step2).move_to([0, EXY7, 0])
        self.ancora("A7b")
        dls = glyphs(chain[3], CYAN_L)
        cdl = dls.copy()
        dls.set_opacity(0)
        self.add(cdl)
        sl7 = self.slot(cdl.copy().scale(1.3))
        self.play(cdl.animate.set_color(MAGENTA).scale(1.3), Create(sl7), run_time=0.65)
        dim7 = [seg_R, lab_R, el_top, el_bot, dl_lab, axis_line, z_axis_lab, corner, seg_r2,
                ax1, ax2v, one_lab]
        self.abre(f_arc, big_arc, dim=dim7 + [f_geo, f_bs])
        num = VGroup(*(g for g in step2[3] if g.get_center()[1] > step2[3].get_center()[1] + 0.02))
        voo = VGroup(big_arc[2][2], big_arc[2][3]).copy()
        self.add(voo)
        self.morph(chain, step2, FadeOut(cdl, scale=0.4), FadeOut(sl7),
                   voo.animate.move_to(num.get_center()).set_opacity(0), run_time=1.15)
        self.remove(voo)
        self.fecha(f_arc, big_arc)
        self.wait(BEAT)

        # os dois R se encontram (R·R → R²) e r² encontra r (r²·r → r³): flash magenta na junção
        self.ancora("A7c")
        Rs = [glyphs(step2[3], CYAN)[0], glyphs(step2[5], CYAN)[0]]
        rs = [glyphs(step2[3], VIOLET)[0], glyphs(step2[5], VIOLET)[0]]
        cR, cr = Rs[1].copy(), rs[1].copy()
        Rs[1].set_opacity(0)
        rs[1].set_opacity(0)
        self.add(cR, cr)
        pR = Rs[0].get_center() + np.array([0.16, 0.10, 0])
        pr = rs[0].get_center() + np.array([0.16, 0.08, 0])
        pa, pb = VGroup(Rs[0], cR).copy(), VGroup(rs[0], cr).copy()
        self.add(pa, pb)
        self.play(Indicate(pa, color=CYAN, scale_factor=1.4), Indicate(pb, color=VIOLET, scale_factor=1.4),
                  run_time=0.70)
        self.remove(pa, pb)
        self.play(cR.animate.move_to(pR).scale(0.75), cr.animate.move_to(pr).scale(0.75),
                  run_time=0.95, rate_func=SUAVE)
        self.ancora("A7d")
        step3 = mtex(r"\vB", "=", r"\frac{\mu_0 I}{4\pi}", r"\frac{\vR^2\,d\phi}{\vr^3}", size=46)
        fit(step3).move_to([0, EXY7, 0])
        self.morph(step2, step3, FadeOut(cR), FadeOut(cr),
                   Flash(pR, color=MAGENTA, line_length=0.12, num_lines=10, flash_radius=0.30),
                   Flash(pr, color=MAGENTA, line_length=0.12, num_lines=10, flash_radius=0.30),
                   run_time=0.90)
        self.check_safe()
        self.wait(READ)

        # a ficha GEOMETRIA se abre: r³ = (r²)^{3/2}, e a cópia de R²+z² entra no lugar de r²
        self.ancora("A7e")
        side = mtex(r"\vr^3", "=", r"\left(\vr^2\right)^{3/2}", size=44).move_to([0, SIDE2_Y, 0])
        den3 = VGroup(*(g for g in step3[3] if g.get_center()[1] < step3[3].get_center()[1] - 0.02))
        sl7b = self.slot(den3)
        self.play(Create(sl7b), run_time=0.55)
        self.abre(f_geo, big_geo, dim=dim7 + [f_bs, f_arc])
        self.play(FadeIn(side, shift=UP * 0.10), run_time=0.80)
        self.wait(BEAT)
        side2 = mtex(r"\vr^3", "=", r"\left(\vR^2+\vZ^2\right)^{3/2}", size=44).move_to([0, SIDE2_Y, 0])
        voo = VGroup(*big_geo[2][3:]).copy()
        self.add(voo)
        self.play(voo.animate.move_to(side2[2].get_center()).scale(0.9).set_opacity(0),
                  ReplacementTransform(side[0], side2[0]), ReplacementTransform(side[1], side2[1]),
                  FadeOut(side[2]), FadeIn(side2[2]), run_time=1.10, rate_func=SUAVE)
        self.remove(voo)
        self.solda(side2)
        self.fecha(f_geo, big_geo)
        self.wait(BEAT)
        step4 = mtex(r"\vB", "=", r"\frac{\mu_0 I \vR^2}{4\pi\left(\vR^2+\vZ^2\right)^{3/2}}",
                     r"\,d\phi", size=44)
        fit(step4).move_to([0, EXY7, 0])
        den = VGroup(*(g for g in step4[2] if g.get_center()[1] < step4[2].get_center()[1] - 0.05))
        voo2 = side2[2].copy()
        self.add(voo2)
        self.morph(step3, step4, voo2.animate.move_to(den.get_center()).set_opacity(0),
                   FadeOut(side2), FadeOut(sl7b), run_time=1.05)
        self.remove(voo2)
        self.expr = step4
        self.check_safe()
        self.wait(READ_RES + 0.4)

        # ══ A8. Soma a volta: B_z = ∫ dB_z; os π se cancelam; 2/4 → 1/2 (98–117 s) ═════════════════════
        self.ancora("A8")
        self.play(*self.caption("SOMA A VOLTA"), self.run_op.animate.set_value(1),
                  *(g.animate.fade(0.7) for g in (f_geo, f_bs, f_arc)),
                  self.trail.animate.set_value(1), run_time=0.60)
        self.ancora("A8b")
        line1 = mtex(r"B_z", "=", r"\int_0^{2\pi}", r"\vB", size=48)
        fit(line1).move_to([0, self.op_y, 0])
        self.play(step4.animate.scale(0.78).move_to([0, SIDE_Y, 0]), FadeIn(line1, shift=UP * 0.10),
                  run_time=0.90, rate_func=SUAVE)
        # o marcador percorre a volta inteira: phi de 0 a 2 pi
        self.play(self.phi.animate.set_value(2 * PI), run_time=1.80, rate_func=linear)
        integ = mtex(r"B_z", "=", r"\int_0^{2\pi}",
                     r"\frac{\mu_0 I \vR^2}{4\pi\left(\vR^2+\vZ^2\right)^{3/2}}", r"d\phi", size=40)
        fit(integ).move_to([0, self.op_y, 0])
        voo = VGroup(step4[2], step4[3]).copy()
        self.play(ReplacementTransform(line1[0], integ[0]), ReplacementTransform(line1[1], integ[1]),
                  ReplacementTransform(line1[2], integ[2]), FadeOut(line1[3], shift=DOWN * 0.15),
                  FadeTransform(voo, VGroup(integ[3], integ[4])), FadeOut(step4),
                  run_time=1.05, rate_func=SUAVE)
        self.expr = self.solda(integ)
        self.check_safe()
        self.wait(BEAT)

        # o que não depende de phi sai de dentro da integral
        self.ancora("A8c")
        self.pulse(integ[3], WHITE, scale=1.08, run_time=0.60)
        pulled = mtex(r"B_z", "=", r"\frac{\mu_0 I \vR^2}{4\pi\left(\vR^2+\vZ^2\right)^{3/2}}",
                      r"\int_0^{2\pi}", r"d\phi", size=40)
        fit(pulled).move_to([0, self.op_y, 0])
        self.note(tag("R, z e I não dependem do ângulo", 22, 0.85))
        self.play(TransformMatchingTex(integ, pulled), run_time=1.00, rate_func=SUAVE)
        self.wait(BEAT)
        dois_pi = mtex(r"B_z", "=", r"\frac{\mu_0 I \vR^2}{4\pi\left(\vR^2+\vZ^2\right)^{3/2}}",
                       r"\cdot", r"2\pi", size=40)
        fit(dois_pi).move_to([0, self.op_y, 0])
        self.pulse(VGroup(pulled[3], pulled[4]), MAGENTA, scale=1.15, run_time=0.55)
        self.note(None)
        # ∫dφ = 2π escrito à parte, a partir de cópias do termo; o 2π então entra na expressão
        self.ancora("A8d")
        side3 = mtex(r"\int_0^{2\pi}", r"d\phi", "=", r"\vM{2\pi}", size=46).move_to([0, SIDE_Y, 0])
        self.play(TransformFromCopy(pulled[3], side3[0]), TransformFromCopy(pulled[4], side3[1]),
                  run_time=0.85, rate_func=SUAVE)
        self.play(FadeIn(side3[2]), FadeIn(side3[3], scale=1.5), run_time=0.60)
        self.solda(side3)
        self.wait(BEAT)
        voo = side3[3].copy()
        self.add(voo)
        self.morph(pulled, dois_pi, voo.animate.move_to(dois_pi[4].get_center()).set_opacity(0),
                   FadeOut(side3), run_time=1.05)
        self.remove(voo)
        self.wait(BEAT)
        # o 2 pi e o 4 pi se juntam numa fração; os dois pi se cancelam
        self.ancora("A8e")
        frac = mtex(r"B_z", "=", r"\frac{2\vM{\pi}}{4\vM{\pi}}",
                    r"\frac{\mu_0 I \vR^2}{\left(\vR^2+\vZ^2\right)^{3/2}}", size=42)
        fit(frac).move_to([0, self.op_y, 0])
        self.morph(dois_pi, frac, run_time=1.00)
        self.wait(BEAT)
        pis = by_height(glyphs(frac[2], MAGENTA))
        self.cancel(pis[0], pis[-1])
        quatro = mtex(r"B_z", "=", r"\frac{2}{4}",
                      r"\frac{\mu_0 I \vR^2}{\left(\vR^2+\vZ^2\right)^{3/2}}", size=42)
        fit(quatro).move_to([0, self.op_y, 0])
        self.morph(frac, quatro, run_time=0.75)
        meio = mtex(r"B_z", "=", r"\frac{1}{2}",
                    r"\frac{\mu_0 I \vR^2}{\left(\vR^2+\vZ^2\right)^{3/2}}", size=42)
        fit(meio).move_to([0, self.op_y, 0])
        self.morph(quatro, meio, run_time=0.75)
        self.pulse(meio[2], MAGENTA, scale=1.35, run_time=0.60)
        self.wait(BEAT)

        # o 1/2 desce para o denominador; a geometria recua e o resultado ganha a placa
        self.ancora("A8f")
        payoff = mtex(r"B_z(\vZ)", "=", r"\frac{\mu_0 I \vR^2}{2\left(\vR^2+\vZ^2\right)^{3/2}}",
                      size=58)
        fit(payoff, 6.4).move_to([0, PAYOFF_Y, 0])
        pl = panel(payoff, WHITE, 0.055, 0.30)
        saem = VGroup(ax1, ax2v, one_lab, seg_r2, el_bot)
        fundo2 = [seg_R, lab_R, el_top, dl_lab, axis_line, z_axis_lab, corner]
        self.morph(meio, payoff, FadeIn(pl[0]), FadeOut(saem), *self.recua(fundo2, 0.42),
                   self.trail.animate.set_value(0), self.run_op.animate.set_value(0),
                   FadeOut(VGroup(f_geo, f_bs, f_arc)), run_time=1.30)
        self.expr = payoff
        self.check_safe()
        self.wait(READ_RES + 1.3)

        g_max = halo(text("máximo em z = 0", 17, WHITE, 0.85)).move_to([1.15, GY0 + GH + 0.02, 0])
        g_z = halo(mtex(r"z/\vR", size=26)).move_to([GX0 + GXS * GZMAX - 0.15, GY0 + 0.30, 0]).set_opacity(0.75)
        g_b = halo(mtex(r"B_z/B_z(0)", size=24)).move_to([-1.20, GY0 + GH + 0.02, 0]).set_opacity(0.75)
        # ══ A9. Checagem: z = 0 — a fórmula reage à geometria se movendo (117–129 s) ═══════════════════
        self.ancora("A9")
        self.play(*self.caption("CHECAGEM: z = 0"), *self.volta(fundo2),
                  self.ax_op.animate.set_value(1), self.zr_op.animate.set_value(1),
                  self.gr_op.animate.set_value(1), FadeIn(g_z), FadeIn(g_b), run_time=0.70)
        # P anda até o centro: z encolhe em tempo real e r encosta em R
        self.ancora("A9b")
        self.play(self.dz.animate.set_value(0.0), run_time=1.90, rate_func=SUAVE)
        self.ancora("A9c")
        z0 = mtex(r"B_z(0)", "=", r"\frac{\mu_0 I \vR^2}{2\left(\vR^2+0\right)^{3/2}}", size=58)
        fit(z0, 6.4).move_to([0, PAYOFF_Y, 0])
        self.pulse(glyphs(payoff, BLUE), BLUE, scale=1.35, run_time=0.55)
        self.morph(payoff, z0, self.zr_op.animate.set_value(0), FadeIn(g_max), run_time=0.90)
        self.wait(BEAT)
        r32 = mtex(r"B_z(0)", "=", r"\frac{\mu_0 I \vR^2}{2\left(\vR^2\right)^{3/2}}", size=58)
        fit(r32, 6.4).move_to([0, PAYOFF_Y, 0])
        self.morph(z0, r32, run_time=0.75)
        self.wait(BEAT)
        cubo = mtex(r"B_z(0)", "=", r"\frac{\mu_0 I \vR^2}{2\vR^3}", size=58)
        fit(cubo, 6.4).move_to([0, PAYOFF_Y, 0])
        self.morph(r32, cubo, Indicate(lab_R, color=CYAN, scale_factor=1.4), run_time=0.85)
        self.wait(BEAT)
        self.pulse(glyphs(cubo[2], CYAN), MAGENTA, scale=1.3, run_time=0.55)
        final = mtex(r"B_z(0)", "=", r"\frac{\mu_0 I}{2\vR}", size=56)
        fit(final, 6.4).move_to([0, PAYOFF_Y, 0])
        pl2 = panel(final, WHITE, 0.055, 0.30)
        self.morph(cubo, final, Transform(pl[0], pl2[0]), run_time=0.95)
        self.expr = VGroup(final, pl[0])
        self.check_safe()
        self.wait(READ_RES)

        # ══ A9B. E muito longe? P segue AO LONGO DO EIXO até z >> R (129–143 s) ════════════════════════
        self.ancora("A9B")
        self.play(*self.caption("E MUITO LONGE?"),
                  FadeOut(VGroup(el_top, dl_lab, axis_line, z_axis_lab, corner, seg_R, lab_R)),
                  self.far.animate.set_value(1.0), self.zr_op.animate.set_value(1.0), run_time=0.70)
        axis2 = DashedLine([DOX - 0.60, DOY, 0], [3.35, DOY, 0], dash_length=0.12).set_stroke(BLUE, 2, 0.55)
        zl2 = halo(tex("z", 30, BLUE)).move_to([3.25, DOY + 0.32, 0]).set_opacity(0.8)
        gen = mtex(r"B_z(\vZ)", "=", r"\frac{\mu_0 I \vR^2}{2\left(\vR^2+\vZ^2\right)^{3/2}}", size=58)
        fit(gen, 6.4).move_to([0, PAYOFF_Y, 0])
        # a espira encolhe (P fica no eixo, em z = 0) e a fórmula geral volta
        self.morph(final, gen, Transform(pl[0], panel(gen)[0]), FadeIn(axis2), FadeIn(zl2),
                   self.esc.animate.set_value(ESC_FAR), run_time=1.30)
        self.wait(BEAT)
        # P se afasta do centro AO LONGO DO EIXO; a seta de B diminui (comprimento = B_z(z))
        self.ancora("A9Bb")
        self.play(self.dz.animate.set_value(Z_FAR), run_time=2.60, rate_func=SUAVE)
        cond = halo(mtex(r"\vZ", r"\gg", r"\vR", size=48)).move_to([0.95, 3.75, 0])
        self.play(FadeIn(cond, scale=1.3), FadeOut(g_max), run_time=0.60)
        self.pulse(cond, MAGENTA, scale=1.25, run_time=0.60)
        self.check_safe()
        self.wait(BEAT)

        # R² + z² ≃ z²: o R² do denominador fica desprezível (magenta, encolhe, some)
        self.ancora("A9Bc")
        den = sorted((g for g in gen[2].family_members_with_points()
                      if g.get_center()[1] < gen[2].get_center()[1] - 0.02),
                     key=lambda g: g.get_center()[0])
        zc = glyphs(gen[2], BLUE)[0].get_center()
        iz = min(range(len(den)), key=lambda k: float(np.linalg.norm(den[k].get_center() - zc)))
        self.apaga(VGroup(*den[iz - 3:iz]))
        g2 = mtex(r"B_z(\vZ)", r"\simeq", r"\frac{\mu_0 I \vR^2}{2\left(\vZ^2\right)^{3/2}}", size=58)
        fit(g2, 6.4).move_to([0, PAYOFF_Y, 0])
        self.morph(gen, g2, run_time=1.00)
        self.wait(BEAT)
        self.ancora("A9Bd")
        g3 = mtex(r"B_z(\vZ)", r"\simeq", r"\frac{\mu_0 I \vR^2}{2\vZ^3}", size=58)
        fit(g3, 6.4).move_to([0, PAYOFF_Y, 0])
        self.morph(g2, g3, Transform(pl[0], panel(g3)[0]), run_time=1.00)
        self.ancora("A9Be")
        prop = halo(mtex(r"B_z", r"\vM{\propto}", r"\frac{1}{\vZ^3}", size=46)).move_to([1.95, GY0 + 0.92, 0])
        self.play(FadeIn(prop, shift=UP * 0.12), run_time=0.85)
        self.check_safe()
        self.wait(READ_RES + 0.6)

        # ══ A10. Gancho: a fórmula geral volta, vira ficha e a espira é copiada (143–153 s) ════════════
        self.ancora("A10")
        self.play(FadeOut(VGroup(axis2, zl2, cond, prop)),
                  self.far.animate.set_value(0.0), self.esc.animate.set_value(1.0),
                  self.ax_op.animate.set_value(0), self.tri_op.animate.set_value(0),
                  self.p_op.animate.set_value(0), self.cur_op.animate.set_value(0),
                  self.zr_op.animate.set_value(0), self.gr_op.animate.set_value(0),
                  FadeOut(g_z), FadeOut(g_b), run_time=0.90)
        gen2 = mtex(r"B_z(\vZ)", "=", r"\frac{\mu_0 I \vR^2}{2\left(\vR^2+\vZ^2\right)^{3/2}}", size=58)
        fit(gen2, 6.4).move_to([0, PAYOFF_Y, 0])
        self.morph(g3, gen2, Transform(pl[0], panel(gen2)[0]), run_time=1.00)
        self.wait(BEAT)
        f_res = ficha("UMA ESPIRA", mtex(
            r"B_z(\vZ)", "=", r"\frac{\mu_0 I \vR^2}{2\left(\vR^2+\vZ^2\right)^{3/2}}", size=46),
            lab_size=22)
        fit(f_res, 6.0).move_to([0, -2.45, 0])
        self.morph(gen2, f_res[2], ReplacementTransform(pl[0], f_res[0]), FadeIn(f_res[1]),
                   run_time=1.05)
        self.expr = self.solda(f_res)
        self.ancora("A10b")
        self.play(*self.caption("E SE FOREM MUITAS?"), self.stack_op.animate.set_value(1.0),
                  run_time=1.40, rate_func=SUAVE)
        self.check_safe()
        self.wait(READ_RES)
        self.ancora("A10c")
        handle = tag("@labparallax", 22, 0.8).move_to([0, -3.75, 0])
        self.play(FadeIn(handle, shift=UP * 0.1), run_time=0.58)
        self.wait(1.2)
        self.ancora("FIM")
