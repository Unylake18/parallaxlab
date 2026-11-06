"""vid_0033 v5 — De onde vem PV = nRT? Camada Manim (transparente) sobre o 3D (cena3d/, render3d.js). Preview silencioso.

Menos texto: a narração carrega os motivos; na tela fica só a conta. No máximo DUAS linhas de álgebra ao mesmo tempo: a linha ATIVA (embaixo, grande)
e o RESULTADO FIXO do passo anterior (em cima, menor, com contorno fino na cor da grandeza). As variáveis nascem dos objetos da cena (rótulo preso ao
objeto → uma cópia viaja até a equação). Troca de linha sempre limpa: sai a antiga (0,25 s) e entra a nova; mapa de glifos só onde a transformação é o ponto.
Posições do 3D vêm de proj.json (px 540×960 → Manim: x = (px−270)/60, y = (480−py)/60). Zonas (px): selos 0–80 · Z_3D 60–400 · Z_EQ 410–750 ·
legenda 760–840 (livre) · chips 850–930; margem de 24 px.
Render (raiz; --disable_caching é obrigatório):
    uv run python -m manim -t --disable_caching -r 540,960 --fps 15 videos/vid_0033_pvnrt/cena.py GasIdeal033
Modo seco: SECO=1 ... --dry_run --progress_bar none · stills: STILLS=q1,q2 SECO=1 ... --dry_run
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
from template.config import BACKGROUND_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text
import fisica as F
import roteiro as RT

config.media_dir = str(UNIT / os.environ.get('MIDIA', 'media_preview'))
config.background_color = BACKGROUND_COLOR
FPS = RT.FPS
TL = json.loads((UNIT / 'timeline.json').read_text(encoding='utf-8'))
PJ = {int(k): v for k, v in json.loads((UNIT / 'proj.json').read_text(encoding='utf-8')).items()} if (UNIT / 'proj.json').exists() else {}
S = RT.CENAS
TT = TexTemplate()
TT.add_to_preamble(r'\usepackage{xcolor}')

# cores por grandeza — operadores ficam brancos
VEL, EC, IMP, MOM, MASS, CNT, GEO, CONST, PC = '9C8CFF', '35D9FF', '9CC7FF', 'EA63FF', 'FFC24D', 'FF5FA2', 'B8C4DA', '8FA3C4', '5AA2FF'
VIOLET, CYAN, ICE, DIM, MAG = '#' + VEL, '#' + EC, '#' + IMP, '#8FA3C4', '#' + MOM
NEUT = ['#F5F7FF', '#B8C4DA', '#6F86A8']                 # barras do C04: neutras (sem violeta)
FUNDO_TXT = '#050816'
Y_CHIP, Y_TAG, Y_SELOS = -6.83, 7.45, 6.78
FIXY, ACTY = -.15, -2.6                                   # linha fixa (em cima) e linha ativa (embaixo) na Z_EQ
FIX_FS, ACT_FS, EQW = 58, 72, 8.0
LIM_X, LIM_Y = 4.5 - .4, 8. - .4                           # margem de 24 px

EQ_LOG = []


def c(h, s):
    return r'{\color[HTML]{%s}%s}' % (h, s)


PV_ = c(PC, 'P') + c(GEO, 'V')
N_, m_, vx_, L_ = c(CNT, 'N'), c(MASS, 'm'), c(VEL, 'v_x'), c(GEO, 'L')
AVG_VX, AVG_V2, AVG_EC = c(VEL, r'\langle v_x^2\rangle'), c(VEL, r'\langle v^2\rangle'), c(EC, r'\langle E_c\rangle')
AVG_VY, AVG_VZ = c(VEL, r'\langle v_y^2\rangle'), c(VEL, r'\langle v_z^2\rangle')
FBAR = c(PC, r'\overline{F}')
JJ = c(IMP, 'J')


def legivel(m):
    sombra = m.copy().set_fill(opacity=0).set_stroke(FUNDO_TXT, 8, .3)
    m.set_stroke(FUNDO_TXT, 2.2, .8, background=True)
    g = VGroup(sombra, m)
    g._qa = 'texto'
    return g.set_z_index(40)


def T(s, size=26, color=TEXT_COLOR, maius=True, wmax=7.6):
    m = screen_text(s.upper() if maius else s, max(size, 26), color=color, oversample=2)
    if m.width > wmax:
        m.scale_to_fit_width(wmax)
    g = legivel(m)
    g.texto = s
    return g


def MT(*parts, size=52):
    """MathTex com cor por símbolo (\\color) e traço da mesma cor (não branqueia a 540 px); constantes com traço mais grosso."""
    m = MathTex(*parts, font_size=size, tex_template=TT).set_z_index(40)
    for g in m.family_members_with_points():
        col = g.get_fill_color()
        g.set_stroke(col, 1.6 if str(col).upper().endswith(CONST) else .8, 1)
    m._qa = 'texto'
    m.texto = None
    m._fs = size
    cores = [str(g.get_fill_color()).upper() for g in m.family_members_with_points()]
    EQ_LOG.append({'tex': ' | '.join(parts)[:90], 'glifos': len(cores), 'coloridos': sum(1 for x in cores if x not in ('#FFFFFF', '#F5F7FF'))})
    return m


def fit(m, w, h):
    h0 = m.height
    if m.width > w:
        m.scale_to_fit_width(w)
    if m.height > h:
        m.scale_to_fit_height(h)
    if hasattr(m, '_fs'):
        m._fs = m._fs * m.height / max(h0, 1e-6)           # tamanho efetivo (para o QA)
    return m


def tabnum(txt, size=100, color=TEXT_COLOR):
    """Texto com os dígitos em células de largura fixa (tabular): a rolagem de um número não treme nem se sobrepõe."""
    base = screen_text(txt, size, color=color, oversample=2)
    cell = screen_text('0', size, color=color, oversample=2).width * 1.06
    glifos = list(base.submobjects)
    assert len(glifos) == len([ch for ch in txt if ch != ' ']), txt
    x, gi = 0., 0
    for ch in txt:
        if ch == ' ':
            x += cell * .4
            continue
        g = glifos[gi]
        gi += 1
        w = cell if ch.isdigit() else g.width + cell * .14
        g.shift(RIGHT * (x + w / 2 - g.get_center()[0]))
        x += w
    out = VGroup(*glifos)
    out.shift(LEFT * out.get_center()[0])
    out.set_stroke(FUNDO_TXT, 2.2, .8, background=True)
    out._qa = 'texto'
    out.texto = txt
    return out.set_z_index(40)


def px(p):
    return np.array([(p[0] - 270) / 60, (480 - p[1]) / 60, 0.])


def traco(m):
    m._qa = 'traco'
    return m


def clamp_pt(p, mx=.15):
    return np.array([np.clip(p[0], -LIM_X + mx, LIM_X - mx), np.clip(p[1], -LIM_Y + mx, LIM_Y - mx), 0.])


def seta(a, b, cor, w=5., op=1.):
    m = Arrow(a, b, buff=0, stroke_width=w, max_tip_length_to_length_ratio=.35, tip_length=.2, color=cor).set_stroke(opacity=op)
    return traco(m.set_z_index(20))


def tracejada(a, b, cor=GEO, w=2.5, op=.8):
    return traco(DashedLine(a, b, dash_length=.1, dashed_ratio=.55).set_stroke('#' + cor if len(cor) == 6 else cor, w, op).set_z_index(18))


def p_act(eq, y=ACTY):
    fit(eq, EQW, 1.6)
    eq.move_to([0, y, 0])
    eq._linha = 1
    return eq


def p_fix(eq):
    fit(eq, EQW, 1.15)
    eq.move_to([0, FIXY, 0])
    eq._linha = 0
    return eq


class GasIdeal033(Scene):
    # ---------- contagem de quadros, modo seco e QA (a cada 2 quadros; a cada quadro perto das trocas) ----------
    def setup(self):
        self.nq, self.amostras, self.trans, self.passos, self.apres, self.pend = 0, [], [], [], {}, []
        self.A = self.Fx = None                       # linha ativa e linha fixa
        self.off = 0.                                 # deslocamento de tempo da cena (os tempos literais são os do v5)
        orig_add, orig_uf, orig_gf = self.renderer.add_frame, self.renderer.update_frame, self.renderer.get_frame
        rend = self.renderer
        rend.save_static_frame_data = lambda scene, static_mobjects: setattr(rend, 'static_image', None)

        def desenha_tudo(scene, time, moving_mobjects=None):
            if rend.skip_animations:
                rend.add_frame(None)
                return
            rend.update_frame(scene)
            rend.add_frame(rend.get_frame())
        rend.render = desenha_tudo
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
            rend.update_frame, rend.get_frame = uf, gf

        def conta(frame, num_frames=1):
            if self.nq % 2 == 0 or any(-.8 <= self.nq / FPS - tt <= 2.5 for tt in self.trans):
                self.amostra()
            self.nq += num_frames
            if not seco:
                return orig_add(frame, num_frames)
        rend.add_frame = conta

    def amostra(self):
        itens = []
        for m in self.mobjects:
            q = getattr(m, '_qa', None)
            if q is None:
                continue
            fam = [f for f in m.get_family() if f.has_points()]
            if not fam:
                continue
            op = max(max(f.get_fill_opacity(), f.get_stroke_opacity()) for f in fam)
            if op < .5:
                continue
            pts = np.vstack([f.get_anchors() for f in fam])[:, :2]
            it = {'tipo': q, 'caixa': [float(pts[:, 0].min()), float(pts[:, 1].min()), float(pts[:, 0].max()), float(pts[:, 1].max())], 'op': round(float(op), 2),
                  'fora': bool(getattr(m, '_fora', False)), 'txt': getattr(m, 'texto', None), 'linha': getattr(m, '_linha', None),
                  'fs': round(float(getattr(m, '_fs', 0)), 1), 'guia': bool(getattr(m, '_guia', False)), 'cab': bool(getattr(m, '_cab', False)),
                  'selo': bool(getattr(m, '_selo', False))}
            if q == 'traco':
                pls = []
                for f in fam:
                    an = np.asarray(f.get_anchors())[:, :2]
                    pls.append(an.round(3).tolist() if len(an) < 60 else an[::max(1, len(an) // 40)].round(3).tolist())
                it['pls'] = pls
            itens.append(it)
        self.amostras.append({'q': self.nq, 'itens': itens})

    def ate(self, t):
        t = t + self.off
        d = t * FPS - self.nq
        if d >= 1:
            self.wait(d / FPS)
        elif d < -1.5:
            print(f'ATRASO {t:.2f}s: {-d / FPS:.2f}s')

    def jogar(self, t, *anims, run_time=.6, **kw):
        self.ate(t)
        self._flush()
        self.trans.append(t + self.off)
        self.play(*anims, run_time=run_time, **kw)

    def pt(self, chave, q=None):
        q = self.nq if q is None else q
        return px(PJ[min(max(q, 0), RT.NQ - 1)][chave])

    def passo(self, chave):
        self.pend.append(chave)               # registrado com o tempo real do próximo passo

    def _flush(self):
        for k in self.pend:
            self.passos.append((round(self.nq / FPS, 2), k))
        self.pend = []

    def chip(self, t, txt, cor=ICE, run_time=.5, y=Y_CHIP):
        m = T(txt, 26, cor).move_to([0, y, 0])
        self.jogar(t, FadeIn(m), run_time=run_time)
        return m

    # ---------- caderno de DUAS linhas: ativa (embaixo) e fixa (em cima) ----------
    def ent(self, eq):
        """FadeIn em linhas curtas (menos glifo solto); Write só nas longas (≥ 14 glifos)."""
        return FadeIn(eq)

    def act_write(self, t, eq, ocultas=(), run=.9):
        """Escreve a linha ativa (as partes em `ocultas` nascem depois, por voo)."""
        p_act(eq, ACTY if self.Fx else -.25)       # sem linha fixa, a primeira linha fica mais alta
        self.A = dict(eq=eq, out=None)
        if ocultas:
            for i in range(len(eq)):
                eq[i].set_opacity(0)
            self.add(eq)
            self.jogar(t, *[eq[i].animate.set_opacity(1) for i in range(len(eq)) if i not in ocultas], run_time=run)
        else:
            self.jogar(t, self.ent(eq), run_time=run)

    def act_troca(self, t, novo, modo='seq', glifos=None, run=.9):
        """Troca a linha ativa: 'seq' = sai a antiga (0,25 s) e entra a nova; 'tmt' = TransformMatchingTex; 'gm' = mapa de glifos."""
        a = self.A
        p_act(novo, ACTY if self.Fx else -.25)
        if modo == 'seq':
            saindo = [a['eq']] + ([a['out']] if a['out'] is not None else [])
            self.jogar(t, *[FadeOut(x) for x in saindo], run_time=.25)
            self.jogar(t + .25, self.ent(novo), run_time=.4)
        else:
            self.ate(t)
            self._flush()
            self.trans.append(t + self.off)
            if a['out'] is not None:
                self.remove(a['out'])
            if modo == 'gm':
                self.play(TransformByGlyphMap(a['eq'], novo, *glifos, auto_fade=True), run_time=run)
            else:
                self.play(TransformMatchingTex(a['eq'], novo), run_time=run)
        self.A = dict(eq=novo, out=None)

    def act_to_fix(self, t, novo=None, run=.8, extra=()):
        """A linha ativa sobe e vira o resultado fixo (a fixa antiga sai). Com `novo`, a fixa é trocada por esse objeto (sem sobreposição)."""
        sai = []
        if self.Fx:
            sai += [self.Fx['eq']] + ([self.Fx['out']] if self.Fx['out'] is not None else [])
        if novo is not None:
            if self.A:
                sai += [self.A['eq']] + ([self.A['out']] if self.A['out'] is not None else [])
            p_fix(novo)
            if sai:
                self.jogar(t, *[FadeOut(x) for x in sai], run_time=.25)
            self.jogar(t + .25 if sai else t, self.ent(novo), run_time=max(.5, run - .25))
            self.Fx, self.A = dict(eq=novo, out=None), None
            return
        a = self.A
        eq = a['eq']
        k = FIX_FS / eq._fs
        k = min(k, EQW / eq.width)
        if sai or extra:
            self.jogar(t, *[FadeOut(x) for x in sai], *extra, run_time=.25)
            t = t + .25
        mover = [eq.animate.scale(k).move_to([0, FIXY, 0])] + ([a['out'].animate.scale(k).move_to([0, FIXY, 0])] if a['out'] is not None else [])
        self.jogar(t, *mover, run_time=max(.5, run - .25))
        eq._fs = eq._fs * k
        eq._linha = 0
        self.Fx, self.A = dict(eq=eq, out=a['out']), None

    def fix_troca(self, t, novo, run=.8):
        """Troca só a linha fixa (sai a antiga em 0,25 s; entra a nova)."""
        p_fix(novo)
        sai = [self.Fx['eq']] + ([self.Fx['out']] if self.Fx['out'] is not None else [])
        self.jogar(t, *[FadeOut(x) for x in sai], run_time=.25)
        self.jogar(t + .25, self.ent(novo), run_time=max(.5, run - .25))
        self.Fx = dict(eq=novo, out=None)

    def contorno(self, t, onde, cor, run=.5):
        L = self.A if onde == 'A' else self.Fx
        r = SurroundingRectangle(L['eq'], color=cor, buff=.14, corner_radius=.14, stroke_width=2.4).set_z_index(35)
        L['out'] = r
        self.jogar(t, FadeIn(r), run_time=.35)

    def limpa(self, t, onde, run=.4, extra=()):
        anims = list(extra)
        for nome in onde:
            L = self.A if nome == 'A' else self.Fx
            if L:
                anims += [FadeOut(L['eq'])] + ([FadeOut(L['out'])] if L['out'] is not None else [])
        if nome == 'A' or 'A' in onde:
            self.A = None
        if 'F' in onde:
            self.Fx = None
        if anims:
            self.jogar(t, *anims, run_time=run)

    def voa(self, t, fonte, alvo, run=.6):
        """Uma cópia da variável (rótulo preso ao objeto) viaja até o seu lugar na equação (TransformFromCopy)."""
        cp = fonte.copy()
        cp._qa = None
        self.add(cp)
        tgt = alvo.copy().set_opacity(1)
        self.jogar(t, Transform(cp, tgt), run_time=run)
        alvo.set_opacity(1)
        self.remove(cp)

    def rotulo(self, nome, sim_tex, cor, x, y, alvo, lado):
        """Rótulo preso a um objeto, fora da silhueta da caixa, com linha-guia. Devolve (grupo, símbolo, linha)."""
        txt = T(nome, 26, DIM, maius=False, wmax=1.45)
        sim = MT(c(cor, sim_tex), size=52)
        g = VGroup(txt, sim).arrange(DOWN, buff=.06).move_to([x, y, 0])
        g._qa = 'texto'
        g.texto = nome
        g._fora = True
        borda = lambda: np.array([x + (-g.width / 2 if lado == 'D' else g.width / 2), y, 0.])
        lin = tracejada(borda(), alvo(), '#B8C4DA', 1.8, .55)
        lin._guia = True
        lin.add_updater(lambda m: m.become(tracejada(borda(), alvo(), '#B8C4DA', 1.8, .55)))
        return g, sim, lin

    # ---------- construção ----------
    def construct(self):
        tag = screen_text('POR TRÁS DA FÓRMULA · EP. 10', 22, oversample=2).set_opacity(.8)
        tag.move_to([-4.5 + .4 + tag.width / 2, Y_TAG, 0]).set_z_index(60)
        tag._qa = 'texto'
        tag.texto = 'tag'
        tag._cab = True
        self.selos = VGroup(T('modelo ideal', 26, DIM), T('câmera lenta', 26, DIM)).arrange(RIGHT, buff=.45)
        self.selos.move_to([0, .55, 0]).set_z_index(60)
        self.selos._qa = 'texto'
        self.selos._selo = True
        self.selos.texto = 'selos'
        logo = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(.35).move_to([4.5 - .4 - .9, Y_TAG, 0])
        self.add(tag, logo)
        self.add(Mobject().add_updater(lambda m, dt: None))
        self.c01(); self.c02(); self.c03(); self.c04(); self.c05(); self.c06(); self.c07(); self.cta()
        self.ate(RT.DURACAO)
        assert self.nq == RT.NQ, (self.nq, RT.NQ)
        pasta = Path(config.media_dir)
        pasta.mkdir(parents=True, exist_ok=True)
        (pasta / 'qa_amostras.json').write_text(json.dumps(self.amostras), encoding='utf-8')
        (pasta / 'qa_trans.json').write_text(json.dumps(self.trans), encoding='utf-8')
        (UNIT / 'qa' / 'cores_eq.json').write_text(json.dumps(EQ_LOG, ensure_ascii=False), encoding='utf-8')
        (UNIT / 'qa' / 'passos.json').write_text(json.dumps({'passos': self.passos, 'apresentacao': self.apres}, ensure_ascii=False), encoding='utf-8')

    # ══ C01 — hook: o balão e o bombardeio ═══════════════════════════════════════════════════════════════════
    def c01(self):
        self.off = 0.
        eqq = MT(c(PC, 'P') + c(GEO, 'V') + '=' + c(CNT, 'n') + c(CONST, 'R') + c(VEL, 'T'), size=104).move_to([0, -1.6, 0])
        pre = T('de onde vem isso?', 40).move_to([0, -3.1, 0])
        av = T('~48 moléculas representam 10²³', 26, DIM).move_to([0, Y_CHIP, 0])
        # a caixa com as partículas já está no primeiro quadro (3D); selos e a fórmula entram por cima
        self.jogar(.1, FadeIn(self.selos), FadeIn(av), FadeIn(eqq), run_time=.7)
        self.jogar(6.1, FadeIn(pre), run_time=.5)
        self.jogar(7.2, FadeOut(eqq), FadeOut(pre), FadeOut(self.selos), FadeOut(av), run_time=.45)
        sl = self.chip(7.9, 'só com moléculas batendo na parede', ICE)
        self.jogar(10.3, FadeOut(sl), run_time=.3)

    # ══ C02 — uma batida ════════════════════════════════════════════════════════════════════════════════════
    def c02(self):
        self.off = 0.
        qb = int(RT.T_BATIDA * FPS)
        mol = lambda: self.pt('m')
        tipo = lambda k: clamp_pt(self.pt(k), .2)

        def alfa():                                   # vetores: entram em 19,6 s e saem em 80,2 s (fim do passo 1 do C04)
            t = self.nq / FPS
            return float(np.clip((t - 16.2) / .8, 0, 1) * np.clip((70.9 - t) / .5, 0, 1))

        def upd_set(k):
            def f(m):
                s, e = mol(), tipo(k)
                if np.linalg.norm(e - s) > .12 and alfa() > 0:
                    m.put_start_and_end_on(s, e)
                    o = (1 if k == 'tx' else .65) * alfa()
                    m.set_stroke(opacity=o)
                    m.tip.set_fill(opacity=o)
                else:
                    m.set_stroke(opacity=0)
                    m.tip.set_fill(opacity=0)
            return f

        def upd_tr(k):
            def f(m):
                s, e = mol(), tipo(k)
                if np.linalg.norm(e - s) > .15 and alfa() > 0:
                    m.become(tracejada(s, e, op=.8 * alfa()))
                else:
                    m.set_stroke(opacity=0)
            return f
        v_tot, v_x = seta(mol(), tipo('tv'), VIOLET, 3.5, .65), seta(mol(), tipo('tx'), VIOLET, 8.)
        v_y, v_z = tracejada(mol(), tipo('ty')), tracejada(mol(), tipo('tz'))
        v_tot.add_updater(upd_set('tv')); v_x.add_updater(upd_set('tx'))
        v_y.add_updater(upd_tr('ty')); v_z.add_updater(upd_tr('tz'))
        self.v_vet = VGroup(v_tot, v_x, v_y, v_z)
        self.add(self.v_vet)
        # rótulos presos aos objetos (as variáveis nascem do desenho)
        g_m, sim_m, lin_m = self.rotulo('massa', 'm', MASS, -3.25, 5.0, lambda: self.pt('m'), 'E')
        g_v, sim_v, lin_v = self.rotulo('velocidade', 'v_x', VEL, 3.25, 3.6, lambda: tipo('tx'), 'D')
        # p = m vₓ: a equação nasce em "o momento"; m e vₓ viajam dos rótulos quando a fala os nomeia
        e1 = MT(c(MOM, 'p'), '=', m_, vx_, size=ACT_FS)
        self.passo('p=mv')
        self.act_write(15.33, e1, ocultas=(2, 3), run=.5)
        self.jogar(16.27, FadeIn(g_m), Create(lin_m), run_time=.4)
        self.apres['m'] = self.nq / FPS
        self.jogar(17.0, FadeIn(g_v), Create(lin_v), run_time=.4)
        self.apres['v_x'] = self.nq / FPS
        for lin in (lin_m, lin_v):
            lin.clear_updaters()
        cps = []
        for fonte, alvo in ((sim_m, e1[2]), (sim_v, e1[3])):
            cp = fonte.copy()
            cp._qa = None
            self.add(cp)
            cps.append((cp, alvo.copy().set_opacity(1)))
        self.jogar(17.45, *[Transform(cp, tg) for cp, tg in cps], FadeOut(VGroup(g_m, lin_m, g_v, lin_v)), run_time=.4)
        e1[2].set_opacity(1)
        e1[3].set_opacity(1)
        for cp, _ in cps:
            self.remove(cp)
        # antes e depois da batida
        ea = MT(c(MOM, 'p_i') + '=' + m_ + vx_, size=ACT_FS)
        eb = MT(c(MOM, 'p_i') + '=' + m_ + vx_ + ',\\;' + c(MOM, 'p_f') + '=-' + m_ + vx_, size=ACT_FS)
        self.passo('p_i,p_f')
        self.act_troca(17.92, ea, 'seq', run=.9)
        self.act_troca(22.5, eb, 'gm', glifos=[(list(range(6)), list(range(6)))], run=1.0)
        # Δp = p_f − p_i → −m vₓ − m vₓ → −2 m vₓ
        s1 = MT(c(IMP, r'\Delta p'), '=', c(MOM, 'p_f'), '-', c(MOM, 'p_i'), size=ACT_FS)
        s2 = MT(c(IMP, r'\Delta p') + '=-' + m_ + vx_ + '-' + m_ + vx_, size=ACT_FS)
        s3 = MT(c(IMP, r'\Delta p') + '=-2' + m_ + vx_, size=ACT_FS)
        self.act_to_fix(23.8)
        self.passo('dp=pf-pi')
        self.act_write(24.66, s1, run=.55)
        self.passo('-mv-mv')
        self.act_troca(25.3, s2, 'seq', run=.9)
        self.passo('-2mv')
        self.act_troca(26.62, s3, 'seq', run=.9)
        # J = +2 m vₓ: a parede recebe o oposto (duas setas de impulso nas colunas laterais, com a linha-guia)
        self.act_to_fix(28.8)
        j1 = MT(JJ + '=+2' + m_ + vx_, size=ACT_FS)
        yc = self.pt('parede', qb + int(round(FPS * 14 / 15)))[1]
        a_mol = seta(np.array([-2.7, yc, 0.]), np.array([-3.6, yc, 0.]), ICE, 6.)
        a_par = seta(np.array([2.7, yc, 0.]), np.array([3.6, yc, 0.]), ICE, 10.)
        guia = tracejada(np.array([-2.65, yc, 0.]), np.array([2.65, yc, 0.]), ICE, 1.6, .3)
        guia._guia = True
        l_mol = MT(c(IMP, r'-2mv_x'), size=30).move_to([-3.15, yc + .45, 0])
        l_par = MT(c(IMP, r'+2m|v_x|'), size=30).move_to([3.2, yc + .45, 0])
        l_mol._fora = l_par._fora = True
        glow = traco(a_par.copy().set_stroke(ICE, 20, .22))
        self.jogar(29.9, GrowArrow(a_mol), GrowArrow(a_par), Create(guia), FadeIn(glow), FadeIn(l_mol), FadeIn(l_par), run_time=.7)
        self.passo('J')
        self.act_write(30.6, j1, run=.5)
        self.contorno(33.15, 'A', ICE)
        self.jogar(33.55, FadeOut(VGroup(a_mol, a_par, guia, l_mol, l_par, glow)), run_time=.45)
        self.act_to_fix(34.05)

    # ══ C03 — nasce a pressão ═══════════════════════════════════════════════════════════════════════════════
    def c03(self):
        self.off = 0.
        q40 = int(S['C03'] * FPS) + int(round(FPS * 2 / 3))
        cA = lambda i: px(PJ[q40]['cA'][i])
        bl, br = cA(4), cA(5)
        yb = bl[1] - .32
        xm = (bl[0] + br[0]) / 2
        rl1 = traco(Arrow([bl[0], yb, 0], [xm - .05, yb, 0], buff=0, stroke_width=3, tip_length=.16, color='#' + GEO))
        rl2 = traco(Arrow([br[0], yb, 0], [xm + .05, yb, 0], buff=0, stroke_width=3, tip_length=.16, color='#' + GEO))
        lL1 = MT(c(GEO, 'L'), size=40).move_to([(bl[0] + xm) / 2, yb - .3, 0])
        lL2 = MT(c(GEO, 'L'), size=40).move_to([(br[0] + xm) / 2, yb - .3, 0])
        g_L, sim_L, lin_L = self.rotulo('lado', 'L', GEO, -3.25, 2.6, lambda: np.array([bl[0], yb, 0.]), 'E')
        self.jogar(37.1, Create(rl1), FadeIn(lL1), run_time=.4)
        self.jogar(37.5, Create(rl2), FadeIn(lL2), run_time=.4)
        self.jogar(37.92, FadeIn(g_L), Create(lin_L), run_time=.4)
        self.apres['L'] = self.nq / FPS
        self.g_i = self.rotulo('molécula i', 'v_{x,i}', VEL, 3.25, 3.6, lambda: clamp_pt(self.pt('tx'), .2), 'D')
        # Δt = (L + L)/vₓ → 2L/vₓ
        d1 = MT(r'\Delta t=(', L_, '+', L_, ')/', vx_, size=ACT_FS)
        d2 = MT(r'\Delta t=\frac{2' + L_ + '}{' + vx_ + '}', size=ACT_FS)
        self.passo('dt=(L+L)/v')
        self.act_write(38.78, d1, ocultas=(2, 4), run=.4)
        self.voa(39.3, lL1, d1[2], run=.4)
        self.voa(39.75, lL2, d1[4], run=.4)
        self.passo('dt=2L/v')
        self.act_troca(41.2, d2, 'seq', run=.9)
        # a fixa passa a ter J e Δt
        comb = MT(JJ + '=+2' + m_ + vx_ + r'\quad\quad ' + r'\Delta t=\frac{2' + L_ + '}{' + vx_ + '}', size=FIX_FS)
        self.act_to_fix(42.75, novo=comb, run=.8)
        # F̄ = J/Δt → 2 m vₓ/(2L/vₓ) → m vₓ²/L (o 2 cancela)
        f1 = MT(FBAR, '=', JJ, '/', r'\Delta t', size=ACT_FS)
        F2 = MT(FBAR + r'=\frac{2' + m_ + vx_ + '}{2' + L_ + '/' + vx_ + '}', size=ACT_FS)
        F3 = MT(FBAR + r'=\frac{' + m_ + c(VEL, 'v_x^2') + '}{' + L_ + '}', size=ACT_FS)
        gm = [([0, 1, 2], [0, 1, 2]), ([4], [3]), ([5], [4]), ([6], [6]), ([11, 12], [5]), ([7], [7]), ([9], [8]), ([3, 8, 10], [])]
        self.passo('F=J/dt')
        self.act_write(43.78, f1, run=.5)
        self.passo('F=2mv/(2L/v)')
        self.act_troca(44.45, F2, 'seq', run=.9)
        self.passo('cancela 2')
        self.jogar(45.74, FadeOut(F2[0][3]), FadeOut(F2[0][8]), run_time=.6)
        self.act_troca(46.9, F3, 'seq', run=.9)
        self.act_to_fix(49.7)
        # P₁ = F̄/A → (m vₓ²/L)/L² → m vₓ²/L³ → m vₓ²/V
        g_A, sim_A, lin_A = self.rotulo('área', 'A', GEO, 3.25, 4.0, lambda: self.pt('wc'), 'D')
        g_V, sim_V, lin_V = self.rotulo('volume', 'V', GEO, -3.25, 4.2, lambda: self.pt('bc'), 'E')
        p1 = MT(c(PC, 'P_1'), '=', FBAR, '/', c(GEO, 'A'), size=ACT_FS)
        p2 = MT(c(PC, 'P_1'), '=', '(', m_, c(VEL, 'v_x^2'), '/', L_, ')', '/', c(GEO, 'L^2'), size=ACT_FS)
        p3 = MT(c(PC, 'P_1'), '=', m_, c(VEL, 'v_x^2'), '/', c(GEO, 'L^3'), size=ACT_FS)
        p4 = MT(c(PC, 'P_1'), '=', m_, c(VEL, 'v_x^2'), '/', c(GEO, 'V'), size=ACT_FS)
        p5 = MT(c(PC, 'P_1') + c(GEO, 'V') + '=' + m_ + c(VEL, 'v_x^2'), size=ACT_FS)
        self.passo('P1=F/A')
        self.act_write(50.55, p1, ocultas=(4,), run=.5)
        self.jogar(51.88, FadeIn(g_A), Create(lin_A), run_time=.4)
        self.apres['A'] = self.nq / FPS
        self.passo('A')
        self.voa(52.3, sim_A, p1[4], run=.4)
        self.passo('P1=(mv2/L)/L2')
        self.act_troca(53.3, p2, 'seq', run=.9)
        self.passo('L3')
        self.act_troca(54.85, p3, 'seq', run=.9)
        self.jogar(55.66, FadeIn(g_V), Create(lin_V), run_time=.25)
        self.apres['V'] = self.nq / FPS
        self.passo('L3=V')
        p4[5].set_opacity(0)
        self.act_troca(55.93, p4, 'seq', run=.9)
        p4[5].set_opacity(0)
        self.voa(56.6, sim_V, p4[5], run=.4)
        self.passo('P1V')
        self.act_troca(60.4, p5, 'tmt', run=.8)
        self.contorno(61.25, 'A', '#' + PC)
        for lin in (lin_L, lin_A, lin_V):
            lin.clear_updaters()
        self.act_to_fix(61.65, extra=[FadeOut(VGroup(rl1, rl2, lL1, lL2, g_L, lin_L, g_A, lin_A, g_V, lin_V)), FadeIn(self.g_i[0]), Create(self.g_i[2])])

    # ══ C04 — o um terço ════════════════════════════════════════════════════════════════════════════════════
    def cuboide(self, o, a, b, cz, cor_arestas=GEO, w=2):
        ez = np.array([.6, .42, 0.])
        P = lambda x, y, z: o + np.array([x * a, y * b, 0]) + z * cz * ez
        ed = [((0, 0, 0), (1, 0, 0)), ((0, 1, 0), (1, 1, 0)), ((0, 0, 1), (1, 0, 1)), ((0, 1, 1), (1, 1, 1)), ((0, 0, 0), (0, 1, 0)), ((1, 0, 0), (1, 1, 0)),
              ((0, 0, 1), (0, 1, 1)), ((1, 0, 1), (1, 1, 1)), ((0, 0, 0), (0, 0, 1)), ((1, 0, 0), (1, 0, 1)), ((0, 1, 0), (0, 1, 1)), ((1, 1, 0), (1, 1, 1))]
        g_ = VGroup(*[tracejada(P(*p), P(*q), cor_arestas, w, .5) for p, q in ed])
        g_._qa = 'traco'
        return P, g_

    def c04(self):
        self.off = 0.
        g_i, sim_i, lin_i = self.g_i
        # somando as N moléculas
        sm1 = MT(PV_, '=', r'\sum_i', m_, c(VEL, r'v_{x,i}^2'), size=ACT_FS)
        sm2 = MT(PV_, '=', m_, r'\sum_i', c(VEL, r'v_{x,i}^2'), size=ACT_FS)
        sm3 = MT(PV_, '=', N_, m_, AVG_VX, size=ACT_FS)
        defn = MT(AVG_VX, '=', r'\frac{\sum_i', c(VEL, r'v_{x,i}^2'), '}{', N_, '}', size=FIX_FS)
        self.passo('soma')
        self.act_write(62.82, sm1, run=.5)
        self.passo('m sum')
        self.act_troca(64.35, sm2, 'tmt', run=.9)
        self.passo('N<vx2>')
        self.passo('media def')
        self.act_troca(67.55, sm3, 'seq', run=.9)
        self.fix_troca(69.1, defn, run=.8)
        lin_i.clear_updaters()
        # decomposição + Pitágoras (a Z_3D inteira é do diagrama)
        o = np.array([-1.9, 2.7, 0.])
        P, cub = self.cuboide(o, 3.0, 2.1, 1.7)
        vt = seta(P(0, 0, 0), P(1, 1, 1), VIOLET, 6)
        vx_a, vy_a, vz_a = seta(P(0, 0, 0), P(1, 0, 0), VIOLET, 5), seta(P(1, 0, 0), P(1, 1, 0), VIOLET, 5), seta(P(1, 1, 0), P(1, 1, 1), VIOLET, 5)
        l_x = MT(c(VEL, 'v_x'), size=44).next_to(P(.5, 0, 0), DOWN, .3)
        l_y = MT(c(VEL, 'v_y'), size=44).next_to(P(1, .5, 0), RIGHT, .35)
        l_z = MT(c(VEL, 'v_z'), size=44).move_to(P(1, 1, .5) + np.array([.85, -.1, 0]))
        l_v = MT(c(VEL, 'v'), size=52).move_to(P(1, 1, 1) + np.array([-.25, .5, 0]))
        # PV = N m ⟨vₓ²⟩ fica como resultado fixo (a definição sai); o 3D sai
        self.act_to_fix(70.5, run=.8, extra=[FadeIn(cub), FadeOut(g_i), FadeOut(lin_i)])
        diag1 = VGroup(cub, vt, vx_a, vy_a, vz_a, l_x, l_y, l_z, l_v)
        self.jogar(71.5, GrowArrow(vt), FadeIn(l_v), run_time=.5)
        self.jogar(72.3, GrowArrow(vx_a), FadeIn(l_x), GrowArrow(vy_a), FadeIn(l_y), GrowArrow(vz_a), FadeIn(l_z), run_time=.6)
        pi1 = MT(c(VEL, 'v_i^2') + '=' + c(VEL, 'v_{x,i}^2') + '+' + c(VEL, 'v_{y,i}^2') + '+' + c(VEL, 'v_{z,i}^2'), size=ACT_FS)
        pi2 = MT(AVG_V2 + '=' + AVG_VX + '+' + AVG_VY + '+' + AVG_VZ, size=ACT_FS)
        self.passo('pit i')
        self.act_write(73.05, pi1, run=.5)
        self.passo('pit media')
        self.act_troca(77.0, pi2, 'seq', run=.9)
        # as três moléculas
        v = F.amostra()
        ia, ib, ic = F.tres_moleculas(v)
        grupos = []
        nomes = ['só em x', 'só em y', 'equilibrada']
        for k, (idx, xc) in enumerate(zip((ia, ib, ic), (-2.7, 0., 2.7))):
            q = v[idx] ** 2 / (F.KB * 300. / F.M_N2)
            comp = np.sqrt(q)
            esc = .85
            o2 = np.array([xc - .75, 3.7, 0.])
            P2, cb = self.cuboide(o2, comp[0] * esc, comp[1] * esc, comp[2] * esc, GEO, 1.8)
            g = VGroup(cb, seta(P2(0, 0, 0), P2(1, 1, 1), VIOLET, 5))
            base_y = 2.1
            barras = VGroup()
            for j in range(3):
                h = min(1.1, max(.06, .24 * q[j]))
                r = Rectangle(width=.4, height=h).set_fill(VIOLET, .9).set_stroke(width=0)
                r.move_to([xc - .5 + .5 * j, base_y + h / 2, 0])
                r._qa = 'traco'
                barras.add(r)
            rot = VGroup(*[MT(c(VEL, s_), size=34).move_to([xc - .5 + .5 * j, base_y - .3, 0]) for j, s_ in enumerate(('x', 'y', 'z'))])
            nm = T(nomes[k], 26, DIM, maius=False).move_to([xc, 6.3, 0])
            for m_x in g[0]:
                m_x._qa = 'traco'
            gg = VGroup(g, barras, rot, nm)
            gg._qa = 'texto'
            gg.texto = nomes[k]
            grupos.append(gg)
        self.jogar(78.0, FadeOut(diag1), *[FadeIn(g) for g in grupos], run_time=.5)
        # as médias convergem (contador n acima das barras)
        ns = [1, 5, 50, 500, 5000, 200000]
        med = F.medias_prefixo(v, ns)
        base_y, esc = 2.6, 1.35
        xs = [-3.0, -1.8, -0.6]

        def barras_n(n):
            g = VGroup()
            for j in range(3):
                h = max(.05, esc * med[n][j])
                r = Rectangle(width=.9, height=h).set_fill(NEUT[j], .95).set_stroke(width=0).move_to([xs[j], base_y + h / 2, 0])
                r._qa = 'traco'
                g.add(r)
            g._qa = 'traco'
            return g
        bars = barras_n(1)
        rotb = VGroup(*[MT(c(['F5F7FF', 'B8C4DA', '6F86A8'][j], s_), size=38).move_to([xs[j], base_y - .52, 0]) for j, s_ in enumerate((r'\langle v_x^2\rangle', r'\langle v_y^2\rangle', r'\langle v_z^2\rangle'))])
        linha = tracejada([-3.6, base_y + esc, 0], [0.4, base_y + esc, 0], TEXT_COLOR, 2, .55)
        cnt = tabnum('n = 1', 44).move_to([0, 5.0, 0])
        self.jogar(81.25, FadeOut(VGroup(*grupos)), FadeIn(bars), FadeIn(rotb), Create(linha), run_time=.45)
        self.jogar(81.7, FadeIn(cnt), run_time=.25)
        tt = 81.95
        for n in ns[1:]:
            novo = barras_n(n)
            self.ate(tt)
            cnt.become(tabnum('n = ' + f'{n:,}'.replace(',', ' '), 44).move_to([0, 5.0, 0]))
            self.play(ReplacementTransform(bars, novo), run_time=.42)
            bars = novo
            tt += .5
        pilha = VGroup(*[Rectangle(width=1.1, height=esc).set_fill(NEUT[j], .95).set_stroke(width=0).move_to([1.7, base_y + esc * (j + .5), 0]) for j in range(3)])
        pilha._qa = 'traco'
        rotb._qa = 'texto'
        l_v2 = MT(c(VEL, r'\langle v^2\rangle'), size=38).move_to([1.7, base_y - .52, 0])
        l_13 = MT(r'\tfrac{1}{3}', size=48).move_to([2.95, base_y + esc * .5, 0])
        ig = MT(AVG_VX, '=', AVG_VY, '=', AVG_VZ, size=ACT_FS)
        d1 = MT(AVG_V2 + '=3' + AVG_VX, size=ACT_FS)
        d2 = MT(AVG_VX + '=\\frac{' + AVG_V2 + '}{3}', size=ACT_FS)
        self.passo('medias iguais')
        self.act_troca(84.48, ig, 'seq', run=.9)
        self.jogar(85.2, FadeOut(cnt), run_time=.25)
        self.passo('<v2>=3<vx2>')
        self.act_troca(86.08, d1, 'seq', run=.9)
        self.jogar(88.95, FadeIn(pilha, shift=UP * .15), FadeIn(l_v2), FadeIn(l_13), run_time=.5)
        gm = [([6], [0]), ([7], [1]), ([8], [2]), ([9], [3]), ([10], [4]), ([4], [5]), ([0], [6]), ([1], [7]), ([2], [8]), ([3], [9]), ([5], [11])]
        self.passo('<vx2>=<v2>/3')
        self.act_troca(89.5, d2, 'gm', glifos=gm, run=.85)
        # substituição: a regra fica fixa e PV = N m ⟨vₓ²⟩ volta como linha ativa
        self.act_to_fix(90.4)
        sb0 = MT(PV_, '=', N_, m_, AVG_VX, size=ACT_FS)
        sb1 = MT(PV_, '=', N_, m_, r'\frac{' + AVG_V2 + '}{3}', size=ACT_FS)
        sb2 = MT(PV_, '=', c(CNT, r'\frac{1}{3}'), N_, m_, AVG_V2, size=ACT_FS)
        self.act_write(91.2, sb0, run=.4)
        self.passo('subst')
        self.act_troca(92.7, sb1, 'seq', run=.9)
        self.passo('1/3Nm<v2>')
        self.act_troca(95.5, sb2, 'seq', run=.9)
        self.contorno(96.95, 'A', VIOLET)
        self.act_to_fix(97.4, extra=[FadeOut(VGroup(bars, rotb, linha, pilha, l_v2, l_13))])       # as barras ficam até a linha final

    # ══ C05 — energia e temperatura ═════════════════════════════════════════════════════════════════════════
    def c05(self):
        self.off = 0.
        ec1 = MT(AVG_EC, '=', r'\frac{1}{2}', m_, AVG_V2, size=ACT_FS)
        ec2 = MT(m_, AVG_V2, '=2', AVG_EC, size=ACT_FS)
        sb = MT(PV_, '=', c(CNT, r'\frac{1}{3}'), N_, r'\cdot', '2', AVG_EC, size=ACT_FS)
        sc = MT(PV_, '=', c(CNT, r'\frac{2}{3}'), N_, AVG_EC, size=ACT_FS)
        self.passo('Ec=1/2mv2')
        self.act_write(98.84, ec1, run=.5)
        self.passo('m<v2>=2Ec')
        self.act_troca(101.45, ec2, 'seq', run=.9)
        self.limpa(102.45, 'F', run=.25)
        self.passo('subst Ec')
        self.act_troca(102.72, sb, 'seq', run=.9)
        self.passo('2/3NEc')
        self.act_troca(104.5, sc, 'tmt', run=.9)
        self.contorno(108.0, 'A', CYAN)
        self.act_to_fix(108.4)
        # gráfico PV/N × T (a Z_3D é só dele: o 3D saiu)
        ax = Axes(x_range=[0, 400, 100], y_range=[0, 6, 2], x_length=6.0, y_length=3.7, tips=False, axis_config={'color': '#' + GEO, 'stroke_width': 3, 'include_ticks': False}).move_to([.2, 4.3, 0])
        traco(ax.x_axis), traco(ax.y_axis)
        ax._qa = 'traco'
        lx = MT(c(VEL, 'T') + r'\,(\mathrm{K})', size=44).next_to(ax.x_axis, DOWN, .25).align_to(ax.c2p(400, 0), RIGHT)
        ly = MT(c(PC, r'PV/N') + r'\,(10^{-21}\mathrm{J})', size=40).next_to(ax.y_axis, UP, .3).align_to(ax.c2p(0, 6), LEFT)
        sel = T('gás quase ideal · 1 atm', 26, DIM).move_to([-1.0, 1.75, 0])
        self.jogar(112.45, Create(ax), FadeIn(lx), FadeIn(ly), FadeIn(sel), run_time=.8)
        reta = traco(Line(ax.c2p(0, 0), ax.c2p(400, 5.52), color='#' + PC, stroke_width=4).set_opacity(.9))
        p0 = Dot(ax.c2p(273.15, 3.77), radius=.1, color=TEXT_COLOR).set_z_index(30)
        p1 = Dot(ax.c2p(373.15, 5.15), radius=.1, color=TEXT_COLOR).set_z_index(30)
        t0 = MT(c(VEL, r'273{,}15\,\mathrm{K}'), size=34).next_to(p0, RIGHT, .16).shift(DOWN * .25)
        t1 = MT(c(VEL, r'373{,}15\,\mathrm{K}'), size=34).next_to(p1, LEFT, .16).shift(UP * .3)
        self.jogar(113.74, FadeIn(p0), FadeIn(t0), run_time=.4)
        self.jogar(114.2, FadeIn(p1), FadeIn(t1), run_time=.4)
        self.jogar(114.9, Create(reta), run_time=.5)
        ta = MT(r'\frac{' + c(EC, r'3{,}77\cdot10^{-21}') + '}{' + c(VEL, r'273{,}15') + '}=' + c(CONST, r'1{,}38\cdot10^{-23}'), size=FIX_FS)
        tb = MT(r'\frac{' + c(EC, r'5{,}15\cdot10^{-21}') + '}{' + c(VEL, r'373{,}15') + '}=' + c(CONST, r'1{,}38\cdot10^{-23}'), size=ACT_FS)
        self.passo('tabela')
        self.fix_troca(116.2, ta, run=.8)
        self.act_write(119.45, tb, run=.6)
        kb = MT(c(CONST, r'k_B=1{,}38\cdot10^{-23}\,\mathrm{J/K}'), size=44).move_to([0, Y_CHIP, 0])
        self.jogar(120.95, FadeIn(kb), run_time=.3)
        self.limpa(121.28, 'AF', run=.3, extra=[FadeOut(VGroup(ax, lx, ly, sel, reta, p0, p1, t0, t1, kb))])
        # PV = N k_B T e a energia
        pk = MT(PV_ + '=' + N_ + c(CONST, 'k_B') + c(VEL, 'T'), size=ACT_FS)
        q1 = MT(c(CNT, r'\frac{2}{3}') + N_ + AVG_EC + '=' + N_ + c(CONST, 'k_B') + c(VEL, 'T'), size=ACT_FS)
        q2 = MT(AVG_EC + '=' + c(CONST, r'\frac{3}{2}') + c(CONST, 'k_B') + c(VEL, 'T'), size=ACT_FS)
        self.passo('PV=NkBT')
        self.act_write(121.6, pk, run=.4)
        self.contorno(126.85, 'A', '#' + PC)
        self.act_to_fix(127.25, novo=MT(PV_ + '=' + N_ + c(CONST, 'k_B') + c(VEL, 'T'), size=FIX_FS), run=.8)
        self.Fx['out'] = None
        self.contorno(128.05, 'F', '#' + PC)
        self.passo('2/3NEc=NkBT')
        self.act_write(128.4, q1, run=.5)
        gf = [([4, 5, 6, 7], [0, 1, 2, 3]), ([8], [4]), ([0], [7]), ([1], [6]), ([2], [5]), ([10], [8]), ([11], [9]), ([12], [10]), ([3, 9], [])]
        self.passo('Ec=3/2kBT')
        self.act_troca(129.45, q2, 'gm', glifos=gf, run=1.0)
        self.contorno(134.1, 'A', CYAN)

    # ══ C06 — a fórmula ═════════════════════════════════════════════════════════════════════════════════════
    def c06(self):
        self.off = 0.
        self.limpa(134.55, 'A', run=.25)
        B = MT(PV_ + '=' + N_ + c(CONST, 'k_B') + c(VEL, 'T'), size=FIX_FS)
        C = MT(PV_ + '=' + c(CNT, 'n') + c(CNT, 'N_A') + c(CONST, 'k_B') + c(VEL, 'T'), size=FIX_FS)
        D = MT(PV_ + '=' + c(CNT, 'n') + c(CONST, 'R') + c(VEL, 'T'), size=FIX_FS)
        # a linha fixa vira o objeto B (para o mapa de glifos)
        p_fix(B)
        self.remove(self.Fx['eq'])
        if self.Fx['out'] is not None:
            self.remove(self.Fx['out'])
        self.add(B)
        self.Fx = dict(eq=B, out=None)
        h1 = MT(N_ + '=' + c(CNT, 'n') + c(CNT, 'N_A'), size=ACT_FS)
        self.passo('N=nNA')
        self.act_write(135.65, h1, run=.5)
        p_fix(C)
        self.ate(138.2)
        self._flush()
        self.trans.append(138.2 + self.off)
        self.play(TransformByGlyphMap(B, C, ([0], [0]), ([1], [1]), ([2], [2]), ([3], [4, 5]), ([4], [6]), ([5], [7]), ([6], [8]), auto_fade=True), run_time=.9)
        self.Fx = dict(eq=C, out=None)
        h2 = MT(c(CONST, 'R') + r'\equiv' + c(CNT, 'N_A') + c(CONST, 'k_B'), size=ACT_FS)
        h3 = MT(c(CNT, r'6{,}022\cdot10^{23}') + r'\times' + c(CONST, r'1{,}3806\cdot10^{-23}') + r'\\[4pt] =' + c(CONST, r'8{,}314\,\mathrm{J/(mol\,K)}'), size=ACT_FS)
        self.passo('R=NAkB')
        self.act_troca(139.15, h2, 'seq', run=.9)
        self.passo('8,314')
        self.act_troca(141.5, h3, 'seq', run=.9)
        self.passo('PV=nRT')
        self.fix_troca(143.65, D, run=.8)
        self.limpa(148.5, 'A', run=.5, extra=[D.animate.scale(1.75).move_to([0, -.3, 0])])
        r = SurroundingRectangle(D, color='#' + PC, buff=.3, corner_radius=.2, stroke_width=3).set_z_index(35)
        self.Fx['out'] = r
        self.jogar(149.05, FadeIn(r), run_time=.35)

    # ══ C07 — pistão isotérmico e o número ══════════════════════════════════════════════════════════════════
    def c07(self):
        self.off = 0.
        sel = T('temperatura constante', 26, ICE).move_to([0, Y_CHIP, 0])
        et1 = T('estado 1 · V', 26, DIM, wmax=2.9).move_to([-1.55, -.8, 0])
        et2 = T('estado 2 · V/2', 26, DIM, wmax=2.9).move_to([1.55, -.8, 0])
        W = RT.PIST['W']
        nA, nB = TL['cont_estado1'], TL['cont_estado2']                 # valores medidos (qa/contadores.txt), texto fixo
        numA = tabnum(str(nA), 100).move_to([-1.55, -2.0, 0])
        numB = tabnum(str(nB), 100).move_to([1.55, -2.0, 0])
        dobro = MT(r'\times2', size=72).move_to([0, -2.0, 0])
        leg = T(f'batidas na parede em {str(W).replace(".", ",")} s', 26, DIM).move_to([0, -3.15, 0])
        # o pistão comprime com a equação final do C06 ainda na tela; os dois contadores entram juntos em "o contador registra"
        self.jogar(152.05, FadeOut(self.Fx['eq']), FadeOut(self.Fx['out']), run_time=.15)
        self.Fx = None
        self.jogar(152.2, FadeIn(et1), FadeIn(numA), FadeIn(et2), FadeIn(numB), FadeIn(leg), run_time=.35)
        self.jogar(153.55, FadeIn(dobro), run_time=.3)
        self.jogar(155.3, FadeIn(sel), run_time=.4)
        r2x = MT(c(PC, r'P') + c(GEO, 'V') + r'=\mathrm{const.}\ \Rightarrow\ ' + c(GEO, r'V/2') + r'\Rightarrow ' + c(PC, r'2P'), size=52).move_to([0, -4.0, 0])
        self.jogar(156.75, FadeIn(r2x), run_time=.5)
        self.jogar(159.3, FadeOut(VGroup(et1, numA, et2, numB, dobro, leg, r2x, sel)), run_time=.4)
        n517 = MT(c(VEL, r'517\ \mathrm{m/s}'), size=100).move_to([0, -3.6, 0])
        out517 = SurroundingRectangle(n517, color=VIOLET, buff=.3, corner_radius=.2, stroke_width=2.5).set_z_index(35)
        sub = T('nitrogênio · 300 K', 28, TEXT_COLOR).move_to([0, -1.5, 0])
        rot = T('velocidade quadrática média', 28, VIOLET).move_to([0, -2.25, 0])
        self.jogar(161.35, FadeIn(sub), run_time=.4)
        self.jogar(163.4, FadeIn(rot), run_time=.4)
        self.jogar(165.35, FadeIn(n517), FadeIn(out517), run_time=.5)
        self.c07_obj = VGroup(n517, out517, sub, rot)

    # ══ CTA — só @labparallax (3D apagado, texto no meio do quadro) ═════════════════════════════════════════
    def cta(self):
        self.off = 0.
        handle = screen_text('@labparallax', 64, oversample=2).set_color_by_gradient(CYAN, VIOLET, MAG)
        handle = legivel(handle).move_to([0, 0, 0])
        self.jogar(S['CTA'], FadeOut(self.c07_obj), FadeIn(handle, scale=.96), run_time=.5)
