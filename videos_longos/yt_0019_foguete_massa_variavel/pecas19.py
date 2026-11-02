"""yt_0019 — peças: simulação do foguete com o gás (massa e momento de verdade), fundos Three.js ('rampa' e 'esp'), desenhos 2D (foguete,
carrinho, esteira, patinadores, manequim, barras de massa) e as contas de conferência (Anexo A).

SimEsp (T2-6, T3-7/T3-8): m₀ = 10.000 kg, propelente 8.000 kg (R = 5), v_ex = 2.500 m/s, vazão 100 kg/s → t_q = 80 s. A cada Δt = 0,05 s sai uma
parcela Δm = 5 kg com velocidade v′ − v_ex, onde v′ = v + Δm v_ex / m (m antes da parcela): m v = (m − Δm) v′ + Δm (v′ − v_ex), exato. Cada
parcela vira um par de partículas de 2,5 kg (o desenho mostra 1 par a cada 4; o ⊕ e o momento usam todas) com velocidades transversais ±(v_y, v_z) (⊕ transversal nulo). Depois de nascer, cada partícula segue
reta a velocidade constante. O ponto de massa do foguete é a saída do bocal (o desenho, FORA DE ESCALA, vai para a frente a partir dele).
Tempo de tela: a queima inteira em 12 s (FAT = 80/12 s de simulação por s de tela, constante).
"""
from prob2 import *  # noqa: F401,F403

SAND = MAS                                  # v5: areia âmbar (massa)
GAS_C = "#FFB866"                           # v5: gás = a mesma massa do tanque: âmbar
FAT = 80.0 / 12.0                           # s de simulação por s de tela (T2-6, T3-7/T3-8)
S_V = 1.2 / 2500.0                          # setas de velocidade no espaço: 1,2 unidade por 2.500 m/s


# ════════════════════════════════════════ simulação ════════════════════════════════════════
class SimEsp:
    M0, MP, VEX, MDOT, DT = 10000.0, 8000.0, 2500.0, 100.0, 0.05

    def __init__(self, sig=0.08, seed=7):
        self.TQ = self.MP / self.MDOT
        n = int(round(self.TQ / self.DT))
        self.dm = self.MDOT * self.DT
        rng = np.random.default_rng(seed)
        m, v, x = self.M0, 0.0, 0.0
        ev, gas = [], []
        for k in range(n):
            t = k * self.DT
            vn = v + self.dm * self.VEX / m                 # conserva o momento exatamente
            vg = vn - self.VEX                              # a parcela nasce com v_foguete − v_ex
            vy, vz = rng.normal(0, sig) * self.VEX, rng.normal(0, 0.5 * sig) * self.VEX
            for s in (1, -1):                               # par simétrico: ⊕ transversal em zero
                gas.append((t, x, vg, s * vy, s * vz, vn, vg > 0))
            m -= self.dm
            v = vn
            ev.append((t, x, v, m))
            x += v * self.DT
        self.ev = ev
        self.vf, self.xq = v, x
        g = np.array([(a, b, c, d, e) for a, b, c, d, e, _, _ in gas], float)
        self.g_t0, self.g_x0, self.g_vx, self.g_vy, self.g_vz = g.T
        self.g_vnasc = np.array([q[5] for q in gas])        # velocidade do foguete logo depois de cada parcela (auditoria)
        self.g_frente = np.array([q[6] for q in gas])       # cor fixada no nascimento: para a frente (branco) ou para trás (DIM)
        self.mg = self.dm / 2                               # massa de cada partícula
        self.t_cruza = next(e[0] for e in ev if e[2] > self.VEX)   # primeira parcela com v′ > v_ex

    def foguete(self, ts):
        """(x, v, m) do foguete no tempo de simulação ts (entre parcelas: movimento uniforme)."""
        if ts < 0:
            return 0.0, 0.0, self.M0
        k = min(int(ts / self.DT + 1e-9), len(self.ev) - 1)
        t0, x, v, m = self.ev[k]
        return x + v * (ts - t0), v, m

    def gas(self, ts):
        """Partículas já expelidas: (x, y, z, idade, índice)."""
        k = self.g_t0 <= ts + 1e-9
        a = ts - self.g_t0[k]
        return self.g_x0[k] + self.g_vx[k] * a, self.g_vy[k] * a, self.g_vz[k] * a, a, np.nonzero(k)[0]

    def cm(self, ts):
        x, v, m = self.foguete(ts)
        gx, gy, gz, _, _ = self.gas(ts)
        return (m * x + self.mg * gx.sum()) / self.M0, (self.mg * gy.sum()) / self.M0

    def momento(self, ts):
        x, v, m = self.foguete(ts)
        k = self.g_t0 <= ts + 1e-9
        return m * v + self.mg * self.g_vx[k].sum()

    def meia(self, ts, h0=6000.0):
        """Meia-largura do enquadramento (m): foguete e gás mais distante, centrado no ⊕."""
        x, _, _ = self.foguete(ts)
        gx = self.gas(ts)[0]
        L = max(x, -gx.min() if len(gx) else 0.0)
        return math.sqrt(h0 ** 2 + (1.15 * L) ** 2)


# ════════════════════════════════════════ fundos 3D ════════════════════════════════════════
def est_foguete(x=0.0, y=0.0, z=0.0, esc=1.0, eixo="z", **kw):
    d = {"x": x, "y": y, "z": z, "esc": esc, "eixo": eixo}
    d.update(kw)
    return d


class EspSim:
    """Fundo 3D 'esp' dirigido pela SimEsp: câmera de frente centrada no ⊕ (x = 0), recuando para caber foguete e gás (unidade 3D = km).
    `ts` (ValueTracker) é o tempo de simulação; `modo` 'neutro' (T2-6) ou 'sentido' (T3-7/T3-8, cor pelo sentido visto de fora)."""
    L_TELA = 2.9                                            # comprimento do foguete na tela (FORA DE ESCALA); v3: ≥ 160 px

    def __init__(self, cena, sim, modo="neutro", yc=-0.35, op=0.0, larg=6.3, xc=0.0):
        self.c, self.s, self.modo, self.yc, self.larg, self.xc = cena, sim, modo, yc, larg, xc
        self.ts = ValueTracker(0.0)
        self.chama = ValueTracker(0.0)
        self.rec = ValueTracker(0.0)                           # recuo extra da câmera (voo livre): meia-largura × (1 + rec)
        self.f3d = Fundo3D(cena, "esp", self.estado, op=op)

    def cam(self, ts):
        K = self.larg / (self.s.meia(ts) * (1.0 + self.rec.get_value()) / 1000.0)
        return cam_frente(K=K, xc=self.xc, yc=self.yc, camx=0.0, fov=16, el=0)

    def tela(self, ts, xm, ym=0.0):
        """Ponto do eixo (m) → Manim (a mesma câmera do 3D)."""
        return projeta3d(self.cam(ts), (xm / 1000.0, 0.0, ym / 1000.0))

    def estado(self, t):
        ts = self.ts.get_value()
        cam = self.cam(ts)
        x, v, m = self.s.foguete(ts)
        esc = self.L_TELA / cam["K"]
        gx, gy, gz, age, idx = self.s.gas(ts)
        sel = (idx // 2) % 4 == 0                               # desenho: 1 par a cada 4 parcelas (a física usa todas)
        gx, gy, gz, age, idx = gx[sel], gy[sel], gz[sel], age[sel], idx[sel]
        if self.modo == "sentido":
            cor = np.where(self.s.g_frente[idx], 2, 1)
        else:
            cor = np.zeros(len(idx), int)
        a = np.maximum(0.45, np.exp(-age / 90.0))
        p = np.stack([gx / 1000, gz / 1000, gy / 1000], axis=1).reshape(-1)
        queima = ts < self.s.TQ - 1e-9
        return {"f": r4(est_foguete(x / 1000, 0.0, 0.0, esc, "x", ch1=self.chama.get_value() * (1.0 if queima else 0.0), torre=0)),
                "gas": {"p": [round(float(q), 4) for q in p], "c": [int(q) for q in cor], "a": [round(float(q), 2) for q in a], "s": 3.5},
                "cam": r4(cam)}


def seta_tr(a, b, color=VREL, width=5, tip=0.2, op=1.0, z=8, dash=0.12):
    """Seta TRACEJADA (velocidade RELATIVA: v_ex, u_rel): haste tracejada e ponta cheia. As setas de aceleração seguem cheias."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    L = np.linalg.norm(b - a)
    if L < 0.03:
        return VMobject()
    u = (b - a) / L
    n = np.array([-u[1], u[0], 0.0])
    tl = min(tip, 0.45 * L)
    base = b - u * tl * 0.92
    haste = DashedLine(a, base, dash_length=dash, dashed_ratio=0.6).set_stroke(color, width, opacity=op)
    ponta = Polygon(b, base + n * tl * 0.42, base - n * tl * 0.42).set_fill(color, op).set_stroke(width=0)
    return VGroup(haste, ponta).set_z_index(z)


def jato_lateral(t, bx, z0, n=160, comp=0.62, aber=0.05, vel=0.9):
    """Jato de partículas deitado (3D, unidades do foguete): n partículas saindo do bocal em x = bx, para −x, abrindo com a idade (determinístico em t).
    Devolve (p, a): posições (x, y, z) e brilho."""
    P, A = [], []
    for i in range(n):
        a = (t * vel + i / n) % 1.0
        P += [bx - 0.07 - comp * a, aber * a * math.sin(i * 12.9898), z0 + aber * a * math.sin(i * 78.233)]
        A.append(round(1.0 - 0.75 * a, 2))
    return [round(q, 4) for q in P], A


def cam_obl_(el, alvo, K, xc=0.0, yc=0.0, fov=18, az=-90.0):
    return {"modo": "obl", "az": az, "el": el, "alvo": list(alvo), "K": K, "xc": xc, "yc": yc, "fov": fov}


# ════════════════════════════════════════ desenhos 2D ════════════════════════════════════════
def piso_grade(x0, x1, y, prof=0.75, passo=0.5, desl=0.0, op=0.35):
    """Piso com grade ciano (rampa, trilho, esteira): linha do chão e grade em perspectiva rasa para baixo. `desl` rola a grade (câmera que segue)."""
    g = VGroup(Line(P3(x0, y), P3(x1, y)).set_stroke(CYAN, 2.2, opacity=0.55))
    for k in range(1, 4):
        yy = y - prof * k / 3
        g.add(Line(P3(x0, yy), P3(x1, yy)).set_stroke(CYAN, 1.2, opacity=op * (1 - 0.2 * k)))
    xs = np.arange(math.floor((x0 - desl) / passo) * passo + desl, x1 + 1e-6, passo)
    for xx in xs:
        if x0 - 1e-6 <= xx <= x1 + 1e-6:
            g.add(Line(P3(xx, y), P3(xx - 0.25 * (xx - (x0 + x1) / 2) / 4, y - prof)).set_stroke(CYAN, 1.1, opacity=op * 0.8))
    return g.set_z_index(-5)


def FogueteMestre(h=3.2, w=0.62, estagios=1, corte=False, nivel=1.0, janela=False, horizontal=False, bocal=None, centro=None, ogiva=True, com_aletas=True):
    """G29 · FOGUETE ÚNICO (2D): silhueta lateral do modelo 3D de f19.js (bocal, 1º estágio, anel de interestágio, 2º estágio, carenagem em ogiva, aletas),
    aço com a luz B. Mesmas proporções do 3D (altura 1): bocal 0–0,06 · casco 0,06–0,85 (anel em 0,60–0,65 se 2 estágios) · ogiva 0,85–1.
    estagios=1|2 · corte=True (tanques visíveis: CARGA no topo, TANQUE com nível 0–1, ESTRUTURA) · janela=True (recorte da cápsula, para o passageiro)
    · horizontal=True (nariz em +x, bocal na origem ou em `bocal`/`centro`). Todo foguete 2D do vídeo nasce aqui.
    .pts: bocal, topo, centro, yb, yt, ys (anel, 2 estágios), w, h; corte: carga, tanque, tq, yc0, hcar; janela: janela (centro), jw, jh."""
    g = VGroup()
    yb, yt = 0.06 * h, (0.85 * h if ogiva else h)                 # ogiva=False: o 1º estágio sozinho (topo reto, onde o 2º se apoia)
    hc = h - yt
    casco = RoundedRectangle(corner_radius=0.05, width=w, height=yt - yb).move_to(P3(0, (yb + yt) / 2))
    og = VMobject().set_points_smoothly([P3(-w / 2, yt), P3(-w * 0.40, yt + hc * 0.50), P3(-w * 0.16, yt + hc * 0.86), P3(0, h),
                                        P3(w * 0.16, yt + hc * 0.86), P3(w * 0.40, yt + hc * 0.50), P3(w / 2, yt)]) if ogiva else VGroup()
    if ogiva:
        og.add_line_to(P3(-w / 2, yt))
    sino = Polygon(P3(-w * 0.22, yb), P3(w * 0.22, yb), P3(w * 0.36, 0), P3(-w * 0.36, 0))
    aletas = VGroup(Polygon(P3(-w / 2, yb + 0.20 * h), P3(-w / 2 - 0.30 * w, yb - 0.01 * h), P3(-w / 2, yb)),
                    Polygon(P3(w / 2, yb + 0.20 * h), P3(w / 2 + 0.30 * w, yb - 0.01 * h), P3(w / 2, yb)))
    for m in ((casco, og, sino, aletas) if ogiva else (casco, sino, aletas)):
        aco(m, 2.0)
        for x_ in m.family_members_with_points():
            x_._degrade = "aco"
    pts = {"bocal": P3(0, 0), "topo": P3(0, h), "centro": P3(0, h / 2), "yb": yb, "yt": yt, "w": w, "h": h}
    if com_aletas:
        g.add(aletas)
    g.add(sino, casco)
    if ogiva:
        g.add(og)
    if estagios == 2:
        ys = yb + 0.69 * (yt - yb)                              # 0,60 h de altura total do modelo 3D, anel de 0,60 a 0,65
        anel = Rectangle(width=w * 1.04, height=0.05 * h).move_to(P3(0, ys + 0.025 * h)).set_fill("#3A4252", 1).set_stroke("#7FB2FF", 1.4, opacity=0.6)
        g.add(anel)
        pts["ys"] = ys
    if janela:
        jw, jh = w * 0.62, 0.30 * h
        jy = yt - 0.20 * h
        jan = RoundedRectangle(corner_radius=0.08, width=jw, height=jh).move_to(P3(0, jy)).set_fill("#0A1A38", 1).set_stroke("#9AA6B8", 3)
        jan.set_z_index(2)
        g.add(jan)
        g.jan = jan
        pts.update(janela=P3(0, jy), jw=jw, jh=jh)
    if corte:
        casco.set_fill("#9AA6B8", opacity=0.0).set_stroke("#9AA6B8", 5, opacity=0.9)         # v3: uma cor só (sem gradiente do aço escondido no corte)
        casco._degrade = None
        hcar = 0.42 * h / 3.2
        yc0 = (yt - hcar - 0.04) if ogiva else yt
        tq0, tq1 = yb + 0.08, (yc0 - 0.1 if ogiva else yt - 0.1)
        tanque = RoundedRectangle(corner_radius=0.04, width=w * 0.74, height=tq1 - tq0).move_to(P3(0, (tq0 + tq1) / 2)).set_stroke(GEO, 2, opacity=0.8).set_fill(GEO, opacity=0)
        hn = max(0.001, (tq1 - tq0 - 0.06) * nivel)
        liq = Rectangle(width=w * 0.66, height=hn).move_to(P3(0, tq0 + 0.03 + hn / 2)).set_stroke(width=0).set_fill(MAS, 0.75)
        if nivel < 0.002:
            liq.set_fill(opacity=0)
        g.add(tanque, liq)
        pts.update(tanque=tanque.get_center(), casco_lado=P3(w / 2, (yb + yt) / 2), tq=(tq0, tq1), yc0=yc0, hcar=hcar)
        g.liq, g.tanque, g.casco = liq, tanque, casco
        if ogiva:
            carga = RoundedRectangle(corner_radius=0.05, width=w * 0.72, height=hcar).move_to(P3(0, yc0 + hcar / 2)).set_fill(WHITE_, 0.18).set_stroke(WHITE_, 2.5)
            g.add(carga)
            g.carga = carga
            pts.update(carga=carga.get_center())
    if not horizontal:
        g.pts = pts
        return g
    g.rotate(-PI / 2, about_point=ORIGIN)                        # o bocal fica na origem; nariz em +x
    b = np.asarray(bocal, float) if bocal is not None else (np.asarray(centro, float) - P3(h / 2, 0) if centro is not None else ORIGIN.copy())
    g.shift(b)
    g.pts = pts
    g.bocal, g.nariz = b.copy(), b + P3(h, 0)
    g.meio = (g.bocal + g.nariz) / 2
    return g


def foguete2d(h=3.2, w=0.62, corte=False, nivel=1.0, estagios=1, rotulos=False, **kw):
    return FogueteMestre(h, w, estagios=estagios, corte=corte, nivel=nivel, **kw)


def fog_h(L=2.2, w=0.46, centro=None, bocal=None, **kw):
    """Foguete-mestre deitado (nariz em +x), posicionado pelo `bocal` ou pelo `centro`. .bocal, .nariz, .meio."""
    return FogueteMestre(L, w, horizontal=True, bocal=bocal, centro=centro, **kw)


def chama2d(base, comp=0.6, larg=0.26, vertical=True, op=0.9):
    """Chama branco-azulada (sem laranja: laranja é calor)."""
    d = DOWN if vertical else LEFT
    n = RIGHT if vertical else UP
    a, b, c = base + n * larg / 2, base - n * larg / 2, base + d * comp
    ext = VMobject().set_points_smoothly([a, base + d * comp * 0.45 + n * larg * 0.42, c, base + d * comp * 0.45 - n * larg * 0.42, b]).close_path()
    ext.set_fill(GAS_C, 0.55 * op).set_stroke(width=0)
    nuc = ext.copy().scale(0.55, about_point=base).set_fill(WHITE_, 0.85 * op)
    return VGroup(ext, nuc).set_z_index(3)


def carrinho2d(w=1.9, h=0.78, nivel=1.0):
    """Carrinho de aço com caçamba de areia (y = 0 no trilho, centro em x = 0). .furo: ponto do furo no fundo da caçamba."""
    r = 0.17
    rodas = VGroup(*[aco(Circle(radius=r).move_to(P3(s * w * 0.32, r)), 2) for s in (-1, 1)])
    eixo_ = VGroup(*[Dot(P3(s * w * 0.32, r), radius=0.04, color=GEO) for s in (-1, 1)])
    yb = 2 * r + 0.04
    chassi = aco(Rectangle(width=w, height=0.12).move_to(P3(0, yb + 0.06)), 2)
    cac = Polygon(P3(-w / 2, yb + 0.12 + h), P3(-w / 2 + 0.12, yb + 0.12), P3(w / 2 - 0.12, yb + 0.12), P3(w / 2, yb + 0.12 + h))
    cac.set_fill(opacity=0).set_stroke("#9AA6B8", 5)
    hn = max(0.0, (h - 0.12) * nivel)
    yi = yb + 0.18
    t_ = hn / h
    areia = Polygon(P3(-w / 2 + 0.12 + 0.02 - 0.0, yi), P3(w / 2 - 0.14, yi), P3(w / 2 - 0.14 + 0.12 * t_, yi + hn), P3(-w / 2 + 0.14 - 0.12 * t_, yi + hn)) \
        .set_fill(SAND, 0.9).set_stroke(width=0)
    if hn < 0.01:
        areia.set_fill(opacity=0)
    furo = P3(0.0, yb)
    g = VGroup(areia, cac, chassi, rodas, eixo_)
    g.furo, g.yb = furo, yb
    return g


def patinador(x, y, sen=1, alt=1.75, pose=None):
    p = PessoaPerfil(x, y, alt=alt, sen=sen, pose=pose or dict(cf=0.25 * sen * 0 + 0.25, jf=0.1, ct=-0.35, jt=-0.35, bf=1.35, af=1.5, bt=0.3, at=0.5, tr=0.12))
    s = silhueta(p)
    return s


def manequim(x, y, alt=1.25):
    """Passageiro sentado (aço, luz B), de perfil olhando para a esquerda; o assento embaixo. y = assento."""
    p = PessoaPerfil(x, y, alt=alt, sen=-1, pose="sentado", quadril=y + 0.02)
    s = silhueta(p)
    assento = aco(VGroup(RoundedRectangle(corner_radius=0.04, width=0.62, height=0.1).move_to(P3(x - 0.05, y - 0.06)),
                         RoundedRectangle(corner_radius=0.04, width=0.1, height=0.75).move_to(P3(x + 0.27, y + 0.3))), 2)
    return VGroup(assento, s)


def barra_massa(x, yb, H, fracs, larg=0.6, cores=None, nomes=None, size=24, lado=RIGHT, mostra=1.0):
    """Barra vertical de massa: fatias de baixo para cima (fração, cor). mostra 0 → 1 enche de baixo para cima."""
    cores = cores or [MAS, STEEL, WHITE_]
    g, y = VGroup(), yb
    alvo = mostra * H
    for f, c in zip(fracs, cores):
        h = min(f * H, max(0.0, alvo - (y - yb)))
        if h > 0.002:
            g.add(Rectangle(width=larg, height=h).move_to(P3(x, y + h / 2)).set_stroke(width=0).set_fill(c, 0.9 if c != WHITE_ else 1.0))
        y += f * H
    moldura = Rectangle(width=larg, height=H).move_to(P3(x, yb + H / 2)).set_stroke(GEO, 2, opacity=0.8).set_fill(opacity=0)
    return VGroup(g, moldura).set_z_index(4)


# ════════════════════════════════════════ números de conferência (Anexo A) ════════════════════════════════════════
def numeros():
    g = 9.8
    e = math.e
    R15 = math.exp(1.5)
    f2 = (R15 - 1) / (1.1 - 0.1 * R15)                 # (P + 1,1 f)/(P + 0,1 f) = R → f = (R − 1) P / (1,1 − 0,1 R)
    m02 = 1 + 1.1 * f2
    m01 = m02 * m02
    f1 = f2 * m02
    prop = f1 + f2
    estr = 0.1 * prop
    return {
        "e": e, "e2": e ** 2, "e3": e ** 3, "95%": 1 - 1 / e ** 3, "63%": 1 - 1 / e,
        "F_emp": 2500 * 120, "peso": 20000 * g, "a0": (300000 - 196000) / 20000, "t_q": 16000 / 120, "vexln5": 2500 * math.log(5),
        "perda": g * 16000 / 120, "dv_E1": 2500 * math.log(5) - g * 16000 / 120, "a_f": (300000 - 4000 * g) / 4000, "a_sent": 300000 / 4000,
        "dv11": 3 * math.log(11), "R15": R15, "f2": f2, "m02": m02, "m01": m01, "prop%": 100 * prop / m01, "estr%": 100 * estr / m01,
        "carga%": 100 / m01, "conf_est1": 3 * math.log((m02 + 1.1 * f1) / (m02 + 0.1 * f1)), "F_E3": 20 * 1.5, "P_E3": 30 * 1.5, "K_E3": 0.5 * 20 * 1.5 ** 2,
        "EN2": 1 - 1 / e ** 2,
    }


NUM = numeros()


def pinta(m, idx, k, pares):
    """Cor por glifo dentro de uma parte k de M(): pares (offset, cor). Para tokens compostos como 'mv' (m branco, v violeta)."""
    for off, c in pares:
        m[0][idx[k][off]].set_color(c)
    return m


def nuvem(c, n=14, r=0.28, seed=2, cor=GAS_C, op=0.85):
    rng = np.random.default_rng(seed)
    return VGroup(*[Dot(np.asarray(c, float) + P3(rng.normal(0, r * 0.5), rng.normal(0, r * 0.35)), radius=0.04, color=cor).set_opacity(op)
                    for _ in range(n)]).set_z_index(3)
