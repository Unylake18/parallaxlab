"""yt_0037 · handoff v2 (G1–G8): regras novas e auditorias por quadro, por cima do polar37.py.
- G1: tamanhos mínimos (constantes SZ_*); caneta com traço 0,8 (G8: nada de traço grosso sobre letra pequena).
- G4: `escreve_seq` escreve em ordem de leitura; quando chega no lugar de um glifo que voa, a caneta espera o pouso.
  `placa_min` e `moldura_de` ficam ligadas ao texto (QA de caixa vazia).
- G5: auditoria de glifos duplicados ao fim de cada play.
- G6: R5 v2 (folga de 10 px texto × traço, texto × borda de 40 px, texto × 3D, glifo em voo incluído).
- G7: o pulso automático do palco vivo do kit sai (o movimento é de conteúdo, escrito nas seções).
Tudo loga linhas [esqueleto], [vazia], [dup], [coluna], [R5v2] para o qa_v2.py."""
import kit as _kit
import lib37 as _lib37
import p37 as _p37
import pecas37 as _pc
import v37 as _v37
from polar37 import *  # noqa: F401,F403

_kit.CANETA_W = 0.7
_p37.VIVO_LIM = 2.5
_pulso0 = _p37._pulso


def _formas_palco(sc):
    fix = sc.fixos()
    out = []
    for m in sc.mobjects:
        if m in fix or m is getattr(sc, "grade", None) or isinstance(m, (ValueTracker, ImageMobject)) or type(m).__name__ == "Fundo3D":
            continue
        if isinstance(m, Group) and not isinstance(m, VGroup):
            continue
        for x in m.family_members_with_points():
            if not isinstance(x, VMobject) or getattr(x, "_tex", None) is not None or getattr(x, "_txt", None) is not None:
                continue
            if (x.z_index or 0) <= -9 or getattr(x, "_sem_foco", False) or getattr(x, "_saindo", False) or getattr(x, "_voando", False):
                continue
            if getattr(x, "_canto", False) or x.width * 120 > 1400:
                continue
            cx, cy = pxof(x.get_center())
            if cx >= 1090 or cy < 190:
                continue
            if x.get_stroke_width() < .5 and x.get_fill_opacity() < .3:
                continue
            out.append(x)
    return out


def _pulso_v2(sc, rt):
    """G7 (v2): o palco ocioso há 2,5 s ganha uma leitura no desenho durante o próximo play/espera: todos os traços do palco acendem num
    contorno largo e claro que sobe e desce, e os preenchimentos clareiam e voltam (a mudança passa de 1 % da área do palco). Sem forma no
    palco (só 3D ou só rótulos), o pulso do kit (o rótulo preso acende)."""
    if getattr(sc, "alvo", None) is not None and sc.alvo / FPS - 2.0 <= sc.t <= sc.alvo / FPS + .2:
        return None, None                                 # os 2 s finais da âncora ficam limpos (o quadro do alvo sai daí)
    fs = _formas_palco(sc)
    f3 = [m for m in sc.mobjects if type(m).__name__ == "Fundo3D" and m.op.get_value() > .5]
    if not fs and not f3:
        return _pulso0(sc, rt)
    ov = VGroup()
    for x in fs:
        y = x.copy()
        y.clear_updaters()
        if x.get_fill_opacity() >= .3:
            c0 = ManimColor(x.get_fill_color()).to_hex()
            y.set_fill(mixh(c0, BR, .45), 0)
        else:
            y.set_fill(opacity=0)
        if x.get_stroke_width() >= .5:
            c1 = ManimColor(x.get_stroke_color()).to_hex()
            y.set_stroke(mixh(c1, BR, .55), W(12), 0)
        else:
            y.set_stroke(width=0)
        y._cheio = x.get_fill_opacity() >= .3
        y._traco = x.get_stroke_width() >= .5
        ov.add(y)
    for y in ov.get_family():
        y._txt = None
        y._voando = True
        y._sem_foco = True
    sem_ctn(ov).set_z_index(3)
    sc.add(ov)
    op0 = {id(f): f.op.get_value() for f in f3}

    def upd(m, al):
        tt = al * rt
        per = 1.6 if rt > 2.0 else rt                     # play longo: o pulso se repete (cada um de ~1,6 s), nunca lento demais
        k = 0.0 if al >= .999 else math.sin(math.pi * ((tt % per) / per))
        for f in f3:                                      # o 3D respira: a opacidade desce 18 % e volta (o sino inteiro muda)
            f.op.set_value(op0[id(f)] * (1 - .32 * k))
        for y in m:
            if y._cheio:
                y.set_fill(opacity=.36 * k)
            if y._traco:
                y.set_stroke(opacity=.42 * k)
    return ov, UpdateFromAlphaFunc(ov, upd, rate_func=linear, run_time=rt)


_p37._pulso = _pulso_v2
_p37.VIVO_LIM = 2.0


def _no_palco_v2(self, anims):
    """Só zera o relógio do palco vivo a animação GRANDE no palco (a mudança estimada passa de ~1,5 % da área): rótulo e traço fino não contam."""
    fix = self.fixos()
    tot = 0.0
    for a in anims:
        for m in _p37._mobs_de(a):
            if m is self.clk or m in fix or type(m) is Mobject or isinstance(m, ValueTracker):
                continue
            try:
                x, y = pxof(m.get_center())
                w_, h_ = m.width * 120, m.height * 120
            except Exception:
                continue
            if x < 1090 and y > 190:
                if isinstance(m, (ImageMobject, Group)) and not isinstance(m, VMobject):
                    tot += w_ * h_
                elif getattr(m, "_tex", None) is not None or getattr(m, "_txt", None) is not None:
                    tot += .3 * w_ * h_
                elif min(w_, h_) < 30:
                    tot += max(w_, h_) * 12
                else:
                    tot += .5 * w_ * h_
    return tot >= 14000


_p37._no_palco = _no_palco_v2


def _wait_vivo_v2(self, duration=1.0, *a, **kw):
    """Espera simples (o portão de tela parada foi dispensado: sem tracer, sem pulso; o tempo de cada espera é o da sincronia)."""
    return _p37._wait_b35(self, duration, *a, **kw)


_p37.B37.wait = _wait_vivo_v2
_p37.B37._sem_vivo = True        # FINAL: sem palco vivo automático (nem _pulso_v2, nem _pulso do kit)

SZ_COL, SZ_SEC, SZ_ROT, SZ_LEG, SZ_TIT = 46, 40, 40, 30, 34     # KaTeX px (fórmula principal, secundária, rótulo do palco); Text px

# ── placas e molduras ligadas ao texto ─────────────────────────────────────────────────────────────────────────────────
_pm0 = _v37.placa_min


def placa_min(m, padx=6, pady=4, op=0.88):
    r = _pm0(m, padx, pady, op)
    r._de = m
    m._placa = r                                  # traço abaixo da placa fica coberto (o R5 não conta)
    return r


_v37.placa_min = placa_min
_lib37.placa_min = placa_min
_pc.placa_min = placa_min


def moldura_de(texto, X0, Y0, w, h, cor=GEO, alpha=.55, wpx=2, raio=10):
    m = moldura(X0, Y0, w, h, cor, alpha, wpx, raio)
    m._de = texto
    return m


def em_volta(texto, cor=GEO, pad=16, wpx=2, alpha=.7, raio=10):
    """Moldura ligada ao texto, a `pad` px em volta da caixa dele."""
    x0, y0 = pxof(texto.get_corner(UL))
    x1, y1 = pxof(texto.get_corner(DR))
    return moldura_de(texto, x0 - pad, y0 - pad, x1 - x0 + 2 * pad, y1 - y0 + 2 * pad, cor, alpha, wpx, raio)


def poe_com_moldura(sc, texto, mol, voos_=(), rt_voo=0.9):
    """A moldura nasce junto com o texto (G4): Create da moldura no mesmo play do primeiro trecho da caneta."""
    escreve_seq(sc, texto, voos_, rt_voo=rt_voo, extra0=[Create(mol)])


# ── G4: escrita em ordem de leitura com os voos no lugar ───────────────────────────────────────────────────────────────
def _ordem(F):
    """Ordem de leitura: esquerda → direita (e de cima para baixo no mesmo x); numa fração, o traço, depois o numerador e o denominador."""
    g = list(F[0])
    n = len(g)
    key = {i: (round(g[i].get_left()[0], 2), 0, -g[i].get_center()[1]) for i in range(n)}
    feito = set()
    cand = sorted([b for b in range(n) if g[b].width >= 3 * max(g[b].height, 1e-3)], key=lambda b: -g[b].width)
    for b in cand:                                    # o traço mais largo primeiro (a fração de fora); o vínculo da raiz fica dentro dela
        gb = g[b]
        if b in feito:
            continue
        x0, x1, yb = gb.get_left()[0], gb.get_right()[0], gb.get_center()[1]
        dentro_x = [i for i in range(n) if i != b and x0 - .01 <= g[i].get_center()[0] <= x1 + .01]
        acima = [i for i in dentro_x if g[i].get_bottom()[1] > yb]
        abaixo = [i for i in dentro_x if g[i].get_top()[1] < yb]
        if not acima or not abaixo:
            continue                                  # não é traço de fração (um sinal de menos)
        k0 = round(x0, 2)
        key[b] = (k0, 0, 0.0)
        feito.add(b)
        for i in acima:
            if i not in feito:
                key[i] = (k0, 1, g[i].get_left()[0])
                feito.add(i)
        for i in abaixo:
            if i not in feito:
                key[i] = (k0, 2, g[i].get_left()[0])
                feito.add(i)
    return sorted(range(n), key=lambda i: key[i])


def escreve_seq(sc, F, voos_=(), rt_voo=0.9, extra0=(), passo=None, arco=-0.6, so=None):
    """F (L/TC) escrita na ordem de leitura. voos_ = [(fonte, chave|índices)]. Os trechos sem fonte vão pela caneta; ao chegar no primeiro glifo
    de um grupo que voa, a caneta espera e o grupo pousa (TransformFromCopy da fonte); depois a caneta continua. Nunca há buraco à esquerda."""
    grupos = []
    arcos = []
    for v in voos_:
        src, ks = v[0], v[1]
        arcos.append(v[2] if len(v) > 2 else arco)        # arco por voo (opcional): (fonte, chave, arco)
        idx = sel(F, ks if isinstance(ks, (list, tuple)) else [ks]) if not (isinstance(ks, (list, tuple)) and ks and isinstance(ks[0], (int, np.integer))) else list(ks)
        grupos.append((src, set(idx)))
    voado = {i: k for k, (_, s) in enumerate(grupos) for i in s}
    ordem = _ordem(F)
    if so is not None:                                # FINAL: só uma parte da fórmula (a outra vem num gatilho seguinte)
        so = set(so)
        ordem = [i for i in ordem if i in so]
    blocos, cur, feitos = [], [], set()
    for i in ordem:
        if i in voado:
            if cur:
                blocos.append(("pena", cur))
                cur = []
            k = voado[i]
            if k not in feitos:
                feitos.add(k)
                blocos.append(("voo", k))
        else:
            cur.append(i)
    if cur:
        blocos.append(("pena", cur))
    ex = list(extra0)
    for tipo, b in blocos:
        if tipo == "pena":
            sc.pena(parte(F, b, "trecho"), passo=passo, extra=ex)
        else:
            src, s = grupos[b]
            alvo = parte(F, sorted(s), "voo")
            alvo._fonte = src
            voos(sc, [(src.copy(), alvo)], rt=rt_voo, arco=arcos[b], extra=ex)
            alvo._fonte = None
        ex = []
    F._esc = True
    return F


# ── G5/G4: auditorias ao fim de cada play ─────────────────────────────────────────────────────────────────────────────
_LOGQ = {}


def _loga(sc, tipo, chave, txt):
    k = (tipo, chave, int(sc.t))
    if k in _LOGQ:
        return
    _LOGQ[k] = 1
    print(f"[{tipo}] {sc.lote} {sc._aid} {sc.t:7.2f}s {txt}")


def _ids_cena(sc):
    s = set()
    for m in sc.mobjects:
        for x in m.get_family():
            s.add(id(x))
    return s


def _audita(sc):
    if sc._aid is None:
        return
    fix = sc.fixos()
    ids = _ids_cena(sc)
    # glifos de texto visíveis
    folhas, vistos = [], set()
    for m in sc.mobjects:
        if m in fix:
            continue
        for x in m.get_family():
            if getattr(x, "_tex", None) is None and getattr(x, "_txt", None) is None:
                continue
            for g in x.family_members_with_points():
                if id(g) in vistos or not isinstance(g, VMobject) or g.get_fill_opacity() < .3:
                    continue
                vistos.add(id(g))
                folhas.append(g)
    # G5 · duplicados: o mesmo glifo (mesmo tamanho e mesmo nº de pontos) visível duas vezes quase no mesmo lugar (IoU > 0,3 ⇔ centros a menos
    #       de ~1/3 do tamanho). Hash por célula de 4 px (O(n)); vizinhos das 9 células.
    if len(folhas) > 1:
        tab = {}
        for g in folhas:
            c = g.get_center()
            w, h = g.width * 120, g.height * 120
            if w < 2 and h < 2:
                continue
            k = (int(c[0] * 30), int(c[1] * 30))
            tab.setdefault(k, []).append((c, w, h, len(g.points), g))
        achou = 0
        for (i, j), lst in tab.items():
            viz = [e for di in (-1, 0, 1) for dj in (-1, 0, 1) for e in tab.get((i + di, j + dj), [])]
            for c, w, h, npt, g in lst:
                for c2, w2, h2, npt2, g2 in viz:
                    if g2 is g or npt2 != npt or id(g2) < id(g):
                        continue
                    if abs(w - w2) > .15 * max(w, w2) + .5 or abs(h - h2) > .15 * max(h, h2) + .5:
                        continue
                    d = np.hypot(*(c[:2] - c2[:2])) * 120
                    if d < max(2.0, .3 * min(max(w, h), max(w2, h2))):
                        p_ = pxof(c)
                        _loga(sc, "dup", f"{p_[0]:.0f},{p_[1]:.0f}", f"glifo duplicado em ({p_[0]:.0f}, {p_[1]:.0f}) px")
                        achou += 1
                if achou > 5:
                    break
    # G4 · esqueleto: fórmula escrita por partes com buraco à esquerda de um glifo visível
    pais = {}
    for m in sc.mobjects:
        for x in m.get_family():
            F = getattr(x, "_pai", None)
            if F is not None:
                pais[id(F)] = F
    for F in pais.values():
        if getattr(F, "_matriz", False):
            continue                              # matriz: a leitura é linha a linha (a ordem de x não vale)
        gl = list(F[0])
        vis = [id(g) in ids and g.get_fill_opacity() > .05 for g in gl]
        if all(vis) or not any(vis):
            continue
        rk = {i: k for k, i in enumerate(_ordem(F))}          # prefixo na ordem de leitura (frações: traço, numerador, denominador)
        # buraco: um glifo visível depois (na leitura) de um invisível E à direita dele (limites empilhados de ∫ não contam)
        if any(rk[a] > rk[b] and gl[a].get_left()[0] > gl[b].get_right()[0] + .02
               for a, va in enumerate(vis) if va for b, vb in enumerate(vis) if not vb):
            _loga(sc, "esqueleto", F._tex[:40], f"buraco em {F._tex[:70]!r}")
            if os.environ.get("DBG_ESQ"):
                o = _ordem(F)
                print("[dbgesq]", "".join("#" if vis[i] else "." for i in o), [(i, round(gl[i].get_left()[0] * 120 + 960), round(540 - gl[i].get_center()[1] * 120)) for i in o])
    # G4 · caixa vazia: placa/moldura visível sem nenhum glifo do seu texto
    for m in sc.mobjects:
        for x in m.get_family():
            de = getattr(x, "_de", None)
            if de is None or not len(x.points):
                continue
            if max(x.get_fill_opacity(), x.get_stroke_opacity() if x.get_stroke_width() > 0.1 else 0) < .3:
                continue
            if not any(id(g) in ids and g.get_fill_opacity() > .05 for g in de.family_members_with_points()):
                _loga(sc, "vazia", getattr(de, "_tex", "?")[:40], f"caixa/placa sem texto: {str(getattr(de, '_tex', '?'))[:60]!r}")
    # G2 · coluna: linhas de conta visíveis
    iv = sorted((pxof(m.get_top())[1], pxof(m.get_bottom())[1]) for m in sc.mobjects
                if getattr(m, "_col", False) and any(g.get_fill_opacity() > .3 for g in m.family_members_with_points()))
    n, fim = 0, -1e9
    for t_, b_ in iv:                              # linhas visuais: faixas verticais que se sobrepõem contam uma vez (degraus lado a lado)
        if t_ > fim - 8:
            n += 1
            fim = b_
        else:
            fim = max(fim, b_)
    if n > 6:
        _loga(sc, "coluna", "n", f"{n} linhas de conta na coluna")


_play_v2 = B37.play


def _play_aud(self, *a, **k):
    _play_v2(self, *a, **k)
    if not getattr(self, "_sem_aud", False):
        _audita(self)


B37.play = _play_aud


def col(*ms):
    """Marca linhas de conta da coluna (QA G2)."""
    for m in ms:
        m._col = True
    return ms[0] if len(ms) == 1 else ms


# ── G6 · R5 v2 ─────────────────────────────────────────────────────────────────────────────────────────────────────
FOLGA, BORDA = 10, 40


def _caixa(x):
    x0, y0 = pxof(x.get_corner(UL))
    x1, y1 = pxof(x.get_corner(DR))
    return x0, y0, x1, y1


def _parente(x, y):
    """y é a fonte ou o destino do voo/glyph map de x (o glifo em trânsito não conta contra a própria origem nem contra a fórmula onde pousa)."""
    f = getattr(x, "_fonte", None)
    if f is not None:
        fi = {id(z) for z in f.get_family()}
        yi = {id(z) for z in y.get_family()}
        if fi & yi:
            return True
    p = getattr(x, "_pai", None)
    if p is not None and (y is p or y in p.get_family()):
        return True
    return False


def gmap(sc, n, A, B, pares, voos=(), rt=1.2, copia=True, nota="", extra=()):
    B._fonte = A
    import polar37 as _p
    return _p.gmap(sc, n, A, B, pares, voos=voos, rt=rt, copia=copia, nota=nota, extra=extra)


def r5v2(self, onde="anim"):
    fix = self.fixos()
    textos, dono = [], {}
    for m in self.mobjects:
        if m in fix:
            continue
        for x in m.get_family():
            if getattr(x, "_txt", None) is None or getattr(x, "_saindo", False) or getattr(m, "_canto", False):
                continue
            if any(y is not x and getattr(y, "_txt", None) is not None and x in y.get_family() for y in m.get_family()):
                continue
            gls = [g for g in x.family_members_with_points() if isinstance(g, VMobject)]
            if not gls or max(g.get_fill_opacity() for g in gls) < 0.3:
                continue
            textos.append((str(x._txt), _caixa(x), x, m))
            for g in x.get_family():
                dono[id(g)] = x
    # o glifo em voo também entra (G6): grupos de glifos em trânsito (partes de fórmula pousando)
    for m in self.mobjects:
        if m in fix:
            continue
        for x in m.get_family():
            if not getattr(x, "_voando", False) or getattr(x, "_tex", None) is None or getattr(x, "_txt", None) is not None or id(x) in dono:
                continue
            gls = [g for g in x.family_members_with_points() if isinstance(g, VMobject)]
            if not gls or max(g.get_fill_opacity() for g in gls) < 0.3:
                continue
            textos.append(("voo: " + str(x._tex), _caixa(x), x, m))
            for g in x.get_family():
                dono[id(g)] = x
    linhas = []
    for m in self.mobjects:
        if m in fix or isinstance(m, (ValueTracker, ImageMobject)) or isinstance(m, Group) and not isinstance(m, VGroup):
            continue
        for x in m.family_members_with_points():
            if not isinstance(x, VMobject) or id(x) in dono or (x.z_index or 0) <= -9 or (x.z_index or 0) == 31:
                continue
            if x.get_stroke_width() < 0.5 or x.get_stroke_opacity() < 0.3 or getattr(x, "_saindo", False):
                continue
            P = x.points
            if len(P) < 2:
                continue
            t = np.linspace(0, 1, 6)[:, None, None]
            Q = (P[:-1][None] * (1 - t) + P[1:][None] * t).reshape(-1, 3)
            linhas.append((type(x).__name__ + " " + ManimColor(x.get_stroke_color()).to_hex(), Q[:, 0] * 120 + 960, 540 - Q[:, 1] * 120,
                           getattr(x, "_guia_de", None), m, x.z_index or 0))
    fundos = [m for m in self.mobjects if isinstance(m, Fundo3D) and m.op.get_value() > .05]
    _vis = {id(x) for m in self.mobjects for x in m.get_family()}       # a placa pode estar dentro do grupo do rótulo (TP)
    n = 0
    for i, (ta, (ax0, ay0, ax1, ay1), xa, ma) in enumerate(textos):
        for tb, (bx0, by0, bx1, by1), xb, mb in textos[i + 1:]:
            if xa in xb.get_family() or xb in xa.get_family():
                continue
            if getattr(xa, "_pai", None) is not None and getattr(xa, "_pai", None) is getattr(xb, "_pai", None):
                continue
            if _parente(xa, xb) or _parente(xb, xa):
                continue
            ox, oy = min(ax1, bx1) - max(ax0, bx0), min(ay1, by1) - max(ay0, by0)
            if ox > 2 and oy > 2:
                self._r5.append((self._aid, self.t, ta, tb, ox, oy))
                print(f"[R5] {self._aid} {self.t:7.2f}s {ta[:50]!r} x {tb[:50]!r} ({ox:.0f}x{oy:.0f} px) {onde}" + (f" A=({ax0:.0f},{ay0:.0f},{ax1:.0f},{ay1:.0f}) B=({bx0:.0f},{by0:.0f},{bx1:.0f},{by1:.0f})" if os.environ.get("DBG_R5") else ""))
                n += 1
        pl_ = getattr(xa, "_placa", None) or getattr(getattr(xa, "f", None), "_placa", None)
        zpl = (pl_.z_index or 0) if pl_ is not None and pl_.get_fill_opacity() > .05 and id(pl_) in _vis else None
        for nome, X, Y, guia, ml, zl in linhas:
            if guia is not None and (guia is xa or xa in guia.get_family() or guia in xa.get_family()) or ml is ma or ta.startswith("voo: ") \
                    or getattr(xa, "_voando", False):
                continue
            if zpl is not None and zl < zpl:
                continue                     # traço coberto pela placa do próprio rótulo                     # o glifo em trânsito conta contra texto e borda; contra traço, só parado
            fg = -2 if getattr(xa, "_dentro", False) else FOLGA          # rótulo dentro da própria região (o "?" na célula): folga do v1
            k = int(np.count_nonzero((X > ax0 - fg) & (X < ax1 + fg) & (Y > ay0 - fg) & (Y < ay1 + fg)))
            if k and os.environ.get("DBG_R5"):
                msk = (X > ax0 - fg) & (X < ax1 + fg) & (Y > ay0 - fg) & (Y < ay1 + fg)
                print(f"[dbgR5] {ta[:20]} {nome} pts {list(zip(X[msk][:3].round(), Y[msk][:3].round()))} linha x {X.min():.0f}-{X.max():.0f} y {Y.min():.0f}-{Y.max():.0f}")
            if k:
                self._r5.append((self._aid, self.t, ta, nome, k, 0))
                print(f"[R5L] {self._aid} {self.t:7.2f}s {ta[:50]!r} x traço {nome} ({k} pts, folga {FOLGA} px) caixa ({ax0:.0f},{ay0:.0f})-({ax1:.0f},{ay1:.0f}) {onde}")
                n += 1
        if ax0 < BORDA or ay0 < BORDA or ax1 > 1920 - BORDA or ay1 > 1080 - BORDA:
            print(f"[R5B] {self._aid} {self.t:7.2f}s {ta[:50]!r} a menos de {BORDA} px da borda ({ax0:.0f},{ay0:.0f})–({ax1:.0f},{ay1:.0f}) {onde}")
            self._r5.append((self._aid, self.t, ta, "borda", 0, 0))
            n += 1
        for f in fundos:
            al = getattr(f, "alfa", None)
            if al is None or not al.any() or getattr(xa, "_ok3d", False) or getattr(ma, "_ok3d", False):
                continue
            if ta.startswith("voo: ") or getattr(xa, "_voando", False):
                continue                     # o glifo em trânsito do rótulo do palco para a coluna passa sobre o 3D (conta contra texto e borda)
            hh, ww = al.shape
            s = ww / 1920
            c0, c1 = max(0, int(ax0 * s)), min(ww, int(ax1 * s) + 1)
            r0, r1 = max(0, int(ay0 * s)), min(hh, int(ay1 * s) + 1)
            if c1 > c0 and r1 > r0:
                k = int(np.count_nonzero(al[r0:r1, c0:c1] > 8))
                if k > 4:
                    print(f"[R53D] {self._aid} {self.t:7.2f}s {ta[:50]!r} x 3D ({k} px de alfa) {onde}")
                    self._r5.append((self._aid, self.t, ta, "3D", k, 0))
                    n += 1
    return n


_pc.r5b = r5v2
B37.r5 = r5v2


def ok3d(*ms):
    """Rótulo que nomeia o objeto 3D sobre o qual está (com placa): lista branca do texto × 3D."""
    for m in ms:
        for x in m.get_family():
            x._ok3d = True
    return ms[0] if len(ms) == 1 else ms


def saindo(ms):
    """Marca o que está saindo numa troca de bloco (fora do R5 enquanto some)."""
    for m in ms:
        for x in m.get_family():
            x._saindo = True
            x._esc = True
    return ms


def dentro(*ms):
    """Rótulo escrito dentro da região que ele nomeia (o "?" na célula, METADE DE CIMA na metade): folga de 2 px contra a borda dela."""
    for m in ms:
        for x in m.get_family():
            x._dentro = True
    return ms[0] if len(ms) == 1 else ms


def guia_px(A, B, cor, de, wpx=2.5, head=12):
    """Linha-guia fina do rótulo `de` até o ponto (não conta no R5 contra o próprio rótulo)."""
    s = seta_px(A, B, cor, wpx, head, z=7)
    for x in s.get_family():
        x._guia_de = de
    return s


# ── FINAL (handoff final §6): PRESSA, duas passadas para a cena seguir a voz real (portado do lib34.py do yt_0034) ─────────────────────────
# Passada 1 (PRESSA=grava, --dry_run): cada trecho entre dois gatilhos (gat, an, fim) anota o tempo de animação dele e o atraso com que chegou ao
# gatilho do fim. Fator do trecho = (tempo − atraso que o próprio trecho criou − 0,1 s) ÷ tempo, com piso 0,4.
# Passadas seguintes (PRESSA=usa, o padrão): os plays e as esperas do trecho andam com esse fator. A voz nunca muda; só a construção encurta.
import json as _json
import os as _os
from pathlib import Path as _Path

PRESSA = _os.environ.get("PRESSA", "usa")
_DIRPR = _Path(__file__).resolve().parent / "renders" / "pressa"
_B = _p37.B37
_play_pr0, _wait_pr0, _gat_pr0, _an_pr0, _fim_pr0 = _B.play, _B.wait, _B.gat, _B.an, _B.fim


def _pr(self):
    if not hasattr(self, "_prs"):
        self._prs, self._seg, self._em_gat = {}, 0, False
        arq = _DIRPR / f"{self.lote}.json"
        self._fat = {} if PRESSA != "usa" or not arq.exists() else {int(k): v for k, v in _json.loads(arq.read_text(encoding="utf-8"))["fator"].items()}
    return self._prs


def _play_pr(self, *anims, run_time=None, **kw):
    from manim.animation.animation import prepare_animation
    S = _pr(self)
    anims = [prepare_animation(a) for a in anims]
    rt = run_time if run_time is not None else max([a.run_time for a in anims] or [1.0])
    f = self._fat.get(self._seg, 1.0)
    if abs(f - 1.0) > 0.001:
        for a in anims:
            a.run_time *= f
        rt *= f
        run_time = rt if run_time is not None else None
    S.setdefault(self._seg, {"rt": 0.0, "late": 0.0, "nome": ""})["rt"] += rt
    return _play_pr0(self, *anims, run_time=run_time, **kw)


def _wait_pr(self, duration=1.0, *a, **k):
    S = _pr(self)
    if not self._em_gat and duration > 0.2:
        f = self._fat.get(self._seg, 1.0)
        duration *= f
        S.setdefault(self._seg, {"rt": 0.0, "late": 0.0, "nome": ""})["rt"] += duration
        if duration < 1 / _kit.FPS:
            return
    return _wait_pr0(self, duration, *a, **k)


def _fecha_seg(self, late, nome):
    S = _pr(self)
    S.setdefault(self._seg, {"rt": 0.0, "late": 0.0, "nome": ""}).update(late=round(late, 3), nome=nome)
    self._seg += 1


def _gat_pr(self, frase):
    _pr(self)
    k = self._k_frase(self._aid, frase)
    if k is not None:
        alvo = self._q0 + max(0.0, _kit.ANC[self._aid]["t"][k] - _kit.LEAD) * _kit.FPS
        _fecha_seg(self, (self.nq - alvo) / _kit.FPS, f"{self._aid}: {frase}")
    self._em_gat = True
    try:
        return _gat_pr0(self, frase)
    finally:
        self._em_gat = False


def _an_pr(self, aid):
    _pr(self)
    if self._off is not None:
        _fecha_seg(self, (self.nq - (round(_kit.ANC[aid]["ini"] * _kit.FPS) - self._off)) / _kit.FPS, f"início de {aid}")
    self._em_gat = True
    try:
        return _an_pr0(self, aid)
    finally:
        self._em_gat = False


def _fim_pr(self):
    S = _pr(self)
    _fecha_seg(self, (self.nq - self.alvo) / _kit.FPS, "fim do lote")
    self._em_gat = True
    if PRESSA == "grava":
        fat, ant = {}, 0.0
        for s in sorted(S):
            d = S[s]
            need = d["late"] - max(0.0, ant)
            if need > 0.05 and d["rt"] > 0.2 and not (self.lote == "PS" and d["nome"] == "fim do lote"):
                fat[s] = round(max(0.4, (d["rt"] - need - 0.1) / d["rt"]), 3)
            elif -d["late"] > 1.2 and d["rt"] > 0.15 and not (d["nome"] == "fim do lote" or d["nome"].startswith("in")):
                # FINAL (K1, "divida a espera entre os gatilhos"): trecho com folga: a construção se estica até perto do próximo gatilho (teto 2,6×),
                # para a tela não ficar parada esperando a voz (nada de brilho: é a própria animação que dura mais)
                fat[s] = round(min(2.6, (d["rt"] - d["late"] - 0.4) / d["rt"]), 3)
            ant = d["late"]
        _DIRPR.mkdir(parents=True, exist_ok=True)
        (_DIRPR / f"{self.lote}.json").write_text(_json.dumps({"fator": fat, "trechos": S}, ensure_ascii=False, indent=0), encoding="utf-8")
        print(f"[pressa] {self.lote}: {len(fat)} trechos encurtados; menor fator {min(fat.values()) if fat else 1:.2f}")
    return _fim_pr0(self)


_B.play, _B.wait, _B.gat, _B.an, _B.fim = _play_pr, _wait_pr, _gat_pr, _an_pr, _fim_pr
