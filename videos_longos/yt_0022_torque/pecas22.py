"""yt_0022 — peças comuns: números de conferência (Anexo A), tabelas RK4 ('regua' e 'tombamento'), câmeras 3D ('regua' e 'porta'),
peças 2,5D (porta2d, chave_roda, regua2d, roda, motor, engrenagens, gangorra, vassoura, lapis, disco_furado, mao_direita, dedo_silhueta,
arco_torque, zoom_inset, DiscoPedacos, eixo_cruz, cm_pt, seta_curva, barra_E, braco) e a base dos lotes (Lote22)."""
from prob2 import *  # noqa: F401,F403

# ── números de conferência (Anexo A; qa22.py confere cada valor da tela contra esta tabela) ─────────────────────────────────
G = 9.8
L_REGUA = 1.0
ALPHA0 = 1.5 * G / L_REGUA                                   # 14,7 rad/s²
AT_PONTA0 = 1.5 * G                                          # 14,7 m/s²
AT_MEIO0 = 0.75 * G                                          # 7,35 m/s²
R_CRIT = 2.0 * L_REGUA / 3.0                                 # 0,667 m (66,7 cm)
OMEGA_MOTOR = 4000.0 * 2.0 * math.pi / 60.0                  # 418,879 rad/s
P_MOTOR_W = 100.0 * OMEGA_MOTOR                              # 41887,9 W
P_MOTOR_KW = P_MOTOR_W / 1000.0                              # 41,8879 kW
P_MOTOR_CV = P_MOTOR_W / 735.5                               # 56,95 cv


def _integra_regua(dt=1e-4, tmax=0.52):
    """Integração RK4 de Δt = 10⁻⁴ s para:
    (1) Régua uniforme L = 1,0 m: θ̈ = (3g / 2L) cos θ;
    (2) Moeda 1 no meio (r0 = 0,50 m, μ_e = 0,5, μ_c = 0,4): normal N/m = g cos θ − r θ̈ − 2 ṙ θ̇;
        parada até |r θ̇² + g sen θ| > μ_e (N/m) (ocorre em θ ≈ 2,86°, t ≈ 0,0824 s); depois r̈ = r θ̇² + g sen θ − μ_c (N/m)
        até N ≤ 0 (t ≈ 0,201 s, θ ≈ 17,0°), quando entra em queda livre;
    (3) Moeda 2 na ponta (x0 = 1,0 m): N(0⁺) = m(g − 3g/2) < 0 → queda livre vertical desde t = 0⁺: z_m2 = −½ g t²;
    (4) Régua com bloco extra de massa M na ponta (EN2): I = M L²/3 + M L² = 4/3 M L², τ = −(M g L/2 + M g L) = −3/2 M g L
        ⇒ θ̈ = (9g / 8L) cos θ, a_ponta(0) = 9g/8 = 1,125 g > g (a moeda na ponta também descola!)."""
    n = int(round(tmax / dt)) + 1
    ts = np.linspace(0.0, tmax, n)
    th = np.zeros(n)
    om = np.zeros(n)
    al = np.zeros(n)
    r1 = np.full(n, 0.50)
    vr1 = np.zeros(n)
    nm1 = np.zeros(n)
    m1x = np.zeros(n)
    m1z = np.zeros(n)
    m2x = np.full(n, L_REGUA)
    m2z = np.zeros(n)
    folga2 = np.zeros(n)
    # EN2 (massa extra M na ponta)
    th_en2 = np.zeros(n)
    om_en2 = np.zeros(n)

    t_slip = None
    th_slip = None
    t_descola1 = None
    th_descola1 = None
    t_vert = None
    em_contato1 = True
    vx1_livre, vz1_livre = 0.0, 0.0

    def f_reg(theta, omega):
        return omega, (1.5 * G / L_REGUA) * math.cos(theta)

    def f_en2(theta, omega):
        return omega, (1.125 * G / L_REGUA) * math.cos(theta)

    for i in range(n):
        t = ts[i]
        c, s = math.cos(th[i]), math.sin(th[i])
        al[i] = (1.5 * G / L_REGUA) * c
        m2z[i] = -0.5 * G * t * t
        z_ponta = -L_REGUA * s
        folga2[i] = m2z[i] - z_ponta

        if em_contato1:
            N_m = G * c - r1[i] * al[i] - 2.0 * vr1[i] * om[i]
            nm1[i] = N_m
            m1x[i] = r1[i] * c
            m1z[i] = -r1[i] * s
            if N_m <= 0.0 and i > 0:
                em_contato1 = False
                t_descola1 = t
                th_descola1 = math.degrees(th[i])
                vx1_livre = vr1[i] * c - r1[i] * om[i] * s
                vz1_livre = -vr1[i] * s - r1[i] * om[i] * c
        else:
            nm1[i] = 0.0

        if i == n - 1:
            break

        # Passo RK4 para a régua
        k1_t, k1_w = f_reg(th[i], om[i])
        k2_t, k2_w = f_reg(th[i] + 0.5 * dt * k1_t, om[i] + 0.5 * dt * k1_w)
        k3_t, k3_w = f_reg(th[i] + 0.5 * dt * k2_t, om[i] + 0.5 * dt * k2_w)
        k4_t, k4_w = f_reg(th[i] + dt * k3_t, om[i] + dt * k3_w)
        th[i + 1] = th[i] + (dt / 6.0) * (k1_t + 2 * k2_t + 2 * k3_t + k4_t)
        om[i + 1] = om[i] + (dt / 6.0) * (k1_w + 2 * k2_w + 2 * k3_w + k4_w)
        if t_vert is None and th[i + 1] >= math.pi / 2:
            frac = (math.pi / 2 - th[i]) / max(1e-12, th[i + 1] - th[i])
            t_vert = t + frac * dt

        # Passo RK4 para EN2
        e1_t, e1_w = f_en2(th_en2[i], om_en2[i])
        e2_t, e2_w = f_en2(th_en2[i] + 0.5 * dt * e1_t, om_en2[i] + 0.5 * dt * e1_w)
        e3_t, e3_w = f_en2(th_en2[i] + 0.5 * dt * e2_t, om_en2[i] + 0.5 * dt * e2_w)
        e4_t, e4_w = f_en2(th_en2[i] + dt * e3_t, om_en2[i] + dt * e3_w)
        th_en2[i + 1] = th_en2[i] + (dt / 6.0) * (e1_t + 2 * e2_t + 2 * e3_t + e4_t)
        om_en2[i + 1] = om_en2[i] + (dt / 6.0) * (e1_w + 2 * e2_w + 2 * e3_w + e4_w)

        # Passo para a moeda 1 (meio)
        if em_contato1:
            f_tan = r1[i] * om[i] ** 2 + G * s
            N_m = max(0.0, G * c - r1[i] * al[i] - 2.0 * vr1[i] * om[i])
            if t_slip is None:
                if f_tan > 0.5 * N_m:
                    t_slip = t
                    th_slip = math.degrees(th[i])
                    ar = max(0.0, f_tan - 0.4 * N_m)
                else:
                    ar = 0.0
            else:
                ar = max(0.0, f_tan - 0.4 * N_m)
            r1[i + 1] = r1[i] + vr1[i] * dt + 0.5 * ar * dt * dt
            vr1[i + 1] = vr1[i] + ar * dt
        else:
            m1x[i + 1] = m1x[i] + vx1_livre * dt
            m1z[i + 1] = m1z[i] + vz1_livre * dt - 0.5 * G * dt * dt
            vz1_livre -= G * dt
            r1[i + 1] = r1[i]

    return {
        "dt": dt, "ts": ts, "th": th, "om": om, "al": al,
        "r1": r1, "vr1": vr1, "nm1": nm1, "m1x": m1x, "m1z": m1z,
        "m2x": m2x, "m2z": m2z, "folga2": folga2,
        "th_en2": th_en2, "om_en2": om_en2,
        "t_vert": t_vert, "t_slip": t_slip, "th_slip": th_slip,
        "t_descola1": t_descola1, "th_descola1": th_descola1,
    }


TAB_REGUA = _integra_regua()


def estado_regua(t, massa_ponta=False, moedas=True, op=1.0):
    """Estado interpolado da cena 3D 'regua' no instante físico t (s)."""
    dt = TAB_REGUA["dt"]
    idx = min(len(TAB_REGUA["ts"]) - 1, max(0, int(round(t / dt))))
    if massa_ponta:
        th = float(TAB_REGUA["th_en2"][idx])
        return {
            "th": round(th, 5), "massa_ponta": True, "moedas": moedas,
            "m2x": round(0.972, 4), "m2z": round(-0.5 * G * t * t + 0.042, 5),
            "op": round(float(op), 3),
        }
    return {
        "th": round(float(TAB_REGUA["th"][idx]), 5),
        "r1": round(float(TAB_REGUA["r1"][idx]), 5),
        "m1x": round(float(TAB_REGUA["m1x"][idx]), 5),
        "m1z": round(float(TAB_REGUA["m1z"][idx]), 5),
        "m2x": round(float(TAB_REGUA["m2x"][idx]), 5),
        "m2z": round(float(TAB_REGUA["m2z"][idx]), 5),
        "moedas": moedas,
        "op": round(float(op), 3),
    }


def _integra_tombamento(L, th0=0.05, dt=1e-4, tmax=2.0):
    """Integração RK4 de θ̈ = (3g / 2L) sen θ de θ0 até π/2 (vassoura L = 1,2 m vs lápis L = 0,15 m)."""
    n = int(round(tmax / dt)) + 1
    ts = np.linspace(0.0, tmax, n)
    th = np.zeros(n)
    om = np.zeros(n)
    th[0] = th0
    t_queda = tmax

    def f(theta, omega):
        return omega, (1.5 * G / L) * math.sin(theta)

    for i in range(n - 1):
        if th[i] >= math.pi / 2:
            th[i + 1:] = math.pi / 2
            break
        k1_t, k1_w = f(th[i], om[i])
        k2_t, k2_w = f(th[i] + 0.5 * dt * k1_t, om[i] + 0.5 * dt * k1_w)
        k3_t, k3_w = f(th[i] + 0.5 * dt * k2_t, om[i] + 0.5 * dt * k2_w)
        k4_t, k4_w = f(th[i] + dt * k3_t, om[i] + dt * k3_w)
        th[i + 1] = th[i] + (dt / 6.0) * (k1_t + 2 * k2_t + 2 * k3_t + k4_t)
        om[i + 1] = om[i] + (dt / 6.0) * (k1_w + 2 * k2_w + 2 * k3_w + k4_w)
        if th[i + 1] >= math.pi / 2:
            frac = (math.pi / 2 - th[i]) / max(1e-12, th[i + 1] - th[i])
            t_queda = ts[i] + frac * dt
            th[i + 1] = math.pi / 2
    return {"dt": dt, "ts": ts, "th": th, "om": om, "t_queda": t_queda, "L": L}


TAB_VASSOURA = _integra_tombamento(1.20)
TAB_LAPIS = _integra_tombamento(0.15)


NUM = {
    "alpha0": ALPHA0,                                             # 14,7 rad/s²
    "at_ponta0": AT_PONTA0,                                       # 14,7 m/s²
    "at_meio0": AT_MEIO0,                                         # 7,35 m/s²
    "r_crit": R_CRIT,                                             # 0,6667 m
    "r_crit_cm": R_CRIT * 100.0,                                  # 66,67 cm
    "folga_005_cm": float(TAB_REGUA["folga2"][500]) * 100.0,      # ~0,61 cm
    "folga_010_cm": float(TAB_REGUA["folga2"][1000]) * 100.0,     # ~2,44 cm
    "folga_015_cm": float(TAB_REGUA["folga2"][1500]) * 100.0,     # ~5,42 cm
    "folga_020_cm": float(TAB_REGUA["folga2"][2000]) * 100.0,     # ~9,30 cm
    "th_015_deg": math.degrees(float(TAB_REGUA["th"][1500])),     # ~9,47°
    "t_vert": float(TAB_REGUA["t_vert"]),                         # ~0,4835 s
    "th_slip_deg": float(TAB_REGUA["th_slip"]),                   # ~2,86°
    "t_slip": float(TAB_REGUA["t_slip"]),                         # ~0,0824 s
    "slip_015_mm": (float(TAB_REGUA["r1"][1500]) - 0.50) * 1000,  # ~1,5 mm
    "th_descola1_deg": float(TAB_REGUA["th_descola1"]),           # ~16,96°
    "t_descola1": float(TAB_REGUA["t_descola1"]),                 # ~0,2009 s
    # Porta (T1)
    "tau_porta_perto": 0.15 * 20.0,                               # 3,0 N·m
    "tau_porta_mac": 0.75 * 20.0,                                 # 15,0 N·m
    "tau_porta_30": 0.75 * 20.0 * 0.5,                            # 7,5 N·m
    "tau_porta_0": 0.0,                                           # 0 N·m
    # Chave de roda (T1-5, T2-4, T2-5)
    "tau_chave_90": 0.40 * 250.0,                                 # 100 N·m
    "tau_chave_30": 0.40 * 250.0 * 0.5,                           # 50 N·m
    "tau_cano": 0.80 * 125.0,                                     # 100 N·m
    "tau_P": 0.20 * 250.0,                                        # 50 N·m
    # Motor e engrenagens (T5-3, T5-4)
    "omega_motor": OMEGA_MOTOR,                                   # 418,9 rad/s
    "P_motor_W": P_MOTOR_W,                                       # 41888 W
    "P_motor_kW": P_MOTOR_KW,                                     # 41,9 kW
    "P_motor_cv": P_MOTOR_CV,                                     # 57,0 cv
    "razao_eng": 3.0,                                             # 3:1
    # Vassoura vs lápis (T4-5)
    "razao_alpha_vl": 1.20 / 0.15,                                # 8,0
    "razao_tempo_vl": math.sqrt(1.20 / 0.15),                     # √8 ≈ 2,8284
    "t_vassoura": float(TAB_VASSOURA["t_queda"]),
    "t_lapis": float(TAB_LAPIS["t_queda"]),
    # Gangorra (T6-3)
    "tau_gangorra_esq": 30.0 * G * 1.5,                           # 441 N·m
    "tau_gangorra_dir": 45.0 * G * 1.0,                           # 441 N·m
    "N_gangorra": (30.0 + 45.0) * G,                              # 735 N
}


def br(x, n=2):
    """Número com vírgula decimal (padrão brasileiro) para MathTex: 0,282 → '0{,}282'."""
    return f"{x:.{n}f}".replace(".", "{,}")


def clamp(x, a, b):
    """Restringe x ao intervalo [a, b]."""
    return min(b, max(a, float(x)))


def P3(x, y, z=0.0, *_):
    """Ponto 3D no plano da tela (aceita 2 ou mais argumentos, compatível com projeta3d)."""
    return np.array([float(x), float(y), 0.0])


def vet_unit(v):
    """Vetor unitário 3D na direção de v."""
    v = np.asarray(v, float)
    n = float(np.linalg.norm(v))
    return v / n if n > 1e-12 else np.array([1.0, 0.0, 0.0])


def nm(s, cor, size=40):
    """Número/unidade como MathTex de uma cor (herda a cor da grandeza)."""
    m = MathTex(s.replace(",", "{,}") if "{,}" not in s else s, font_size=size, color=cor)
    m._partes = [(s, cor)]
    return m


# ── câmeras 3D ('regua' e 'porta') ──────────────────────────────────────────────────────────────────────────
def cam_regua_frente(K=5.4, xc=-1.6, yc=0.65, camx=0.42, camz=-0.06, el=0.0):
    """Câmera frontal ao plano xz da queda da régua (el = 0 na vista frontal pura)."""
    if abs(el) < 1e-4:
        return cam_frente(K=K, xc=xc, yc=yc, camx=camx, fov=14, el=0.0) | {"camz": camz}
    return cam_obl(az=-90.0, el=el, alvo=(camx, 0.0, camz), K=K, xc=xc, yc=yc, fov=14)


def cam_regua_obl(u, K=5.4, xc=-1.6, yc=0.65, camx=0.42, camz=-0.06):
    """Interpolação suave de câmera 3/4 alta (u = 0: az = -64°, el = 22°) até frontal pura (u = 1: az = -90°, el = 0°)."""
    s = smooth(clamp(u, 0.0, 1.0))
    if s >= 0.999:
        return cam_regua_frente(K=K, xc=xc, yc=yc, camx=camx, camz=camz, el=0.0)
    az = -64.0 + (-90.0 - (-64.0)) * s
    el = 22.0 * (1.0 - s)
    return cam_obl(az=az, el=el, alvo=(camx, 0.0, camz), K=K, xc=xc, yc=yc, fov=14)


def tela_regua(cam, r, th=0.0, dz=0.0):
    """Projeta ponto a distância r ao longo da régua (inclinada de th) na tela Manim via projeta3d."""
    c, s = math.cos(th), math.sin(th)
    return projeta3d(cam, (r * c + dz * s, 0.0, -r * s + dz * c))


def cam_porta_topo(K=4.6, xc=-3.6, yc=-0.1, camx=0.38, camy=0.18):
    """Câmera de topo sobre a porta (olhando de +z para o plano xy)."""
    return cam_topo(K=K, xc=xc, yc=yc, camx=camx, camy=camy, fov=16)


def cam_porta_obl(u, K0=4.6, K1=3.3, xc=-3.5, yc=-0.25):
    """Interpola da vista de topo (u = 0) para a vista 3/4 (u = 1: az = -58°, el = 28°)."""
    s = smooth(clamp(u, 0.0, 1.0))
    az = -90.0 + (-58.0 - (-90.0)) * s
    el = 89.9 * (1.0 - s) + 28.0 * s
    K = K0 + (K1 - K0) * s
    alvo = (0.38 * (1 - s) + 0.35 * s, 0.18 * (1 - s) + 0.10 * s, 0.0)
    return cam_obl(az=az, el=el, alvo=alvo, K=K, xc=xc, yc=yc, fov=16)


def tela_porta(cam, r, ang=0.0, z=0.0):
    """Projeta ponto a distância r da dobradiça da porta (girada de ang) na cota vertical z."""
    return projeta3d(cam, (r * math.cos(ang), r * math.sin(ang), z))


# ── marcas e peças 2D / 2,5D (§4.2) ────────────────────────────────────────────────────────────────────────
def eixo_cruz(c, s=0.2, cor=GEO, z=14):
    """Eixo visto de topo (perpendicular à tela): círculo + cruz em GEO."""
    c = np.asarray(c, float)
    g = VGroup(Circle(radius=s * 0.6).move_to(c).set_stroke(cor, 2.6).set_fill(BACKGROUND_COLOR, 0.6),
               Line(c + s * LEFT, c + s * RIGHT).set_stroke(cor, 2.6), Line(c + s * DOWN, c + s * UP).set_stroke(cor, 2.6))
    return g.set_z_index(z)


def cm_pt(c, r=0.1, z=16):
    """Centro de massa: ponto branco simples com contorno GEO."""
    g = VGroup(Dot(np.asarray(c, float), radius=r, color=WHITE_), Circle(radius=r + 0.035).move_to(c).set_stroke(GEO, 2.4))
    g._cm = True
    return g.set_z_index(z)


def seta_curva(c, r, a0, da, cor=VEL, w=6, tip=0.24, z=12, op=1.0):
    """Seta curva (ω ou α): arco de raio r a partir do ângulo a0, varrendo da (rad), com ponta legível."""
    c = np.asarray(c, float)
    arc = Arc(radius=r, start_angle=a0, angle=da, arc_center=c).set_stroke(cor, w, opacity=op)
    a1 = a0 + da
    p = c + r * np.array([math.cos(a1), math.sin(a1), 0])
    tg = np.sign(da) * np.array([-math.sin(a1), math.cos(a1), 0])
    n = np.array([-tg[1], tg[0], 0])
    ponta = Polygon(p + tg * tip, p - tg * tip * 0.2 + n * tip * 0.55, p - tg * tip * 0.2 - n * tip * 0.55).set_stroke(cor, 1, opacity=op).set_fill(cor, op)
    return VGroup(arc, ponta).set_z_index(z)


def arco_torque(c, r=0.52, sentido=1, a0=0.35, amp=2.2, cor=TQ, w=6, tip=0.24, z=14, op=1.0):
    """Arco de sentido do torque τ em azul-força (#5AA2FF): sentido = +1 (anti-horário) ou -1 (horário)."""
    da = abs(amp) * (1 if sentido >= 0 else -1)
    return seta_curva(c, r, a0, da, cor=cor, w=w, tip=tip, z=z, op=op)


def barra_E(x, yb, h, larg=0.42, cor=KC, hmax=None, op=0.9, z=10):
    """Barra vertical crescendo da base yb até a altura h (moldura até hmax)."""
    g = VGroup()
    if hmax:
        fr = Rectangle(width=larg + 0.08, height=hmax + 0.08).move_to(P3(x, yb + hmax / 2)).set_stroke(GEO, 1.6, opacity=0.6).set_fill(PANEL, 0.4)
        fr._fundo = True
        g.add(fr)
    if h > 0.004:
        g.add(Rectangle(width=larg, height=h).move_to(P3(x, yb + h / 2)).set_stroke(cor, 2).set_fill(cor, op))
    return g.set_z_index(z)


def braco(mao, ang, comp=2.2, cor="#5E6A80", z=18, op=1.0):
    """Braço em silhueta 2D (antebraço + mão, cápsulas preenchidas), visto de cima."""
    mao = np.asarray(mao, float)
    u = np.array([math.cos(ang), math.sin(ang), 0])
    cot = mao + u * comp * 0.55
    omb = mao + u * comp
    g = VGroup(capsula2d(cot, omb, 0.2, cor), capsula2d(mao + u * 0.12, cot, 0.15, cor),
               Circle(radius=0.17).move_to(mao).set_stroke(width=0).set_fill(cor, 1))
    for m in g.family_members_with_points():
        m.set_fill(cor, op).set_stroke(mix(cor, 0.25), 1.2, opacity=op)
    return g.set_z_index(z)


def dedo_silhueta(ponta, dir_dedo=UP, comp=0.95, cor="#6C7A94", z=18):
    """Silhueta 2,5D discreta de dedo apoiando por baixo ou segurando a ponta da régua."""
    ponta = np.asarray(ponta, float)
    u = vet_unit(dir_dedo)
    base = ponta - u * comp
    c1 = capsula2d(base, ponta - u * 0.12, 0.14, cor)
    c2 = Circle(radius=0.13).move_to(ponta - u * 0.12).set_fill(mix(cor, 0.18), 1).set_stroke(GEO, 1.4)
    return VGroup(c1, c2).set_z_index(z)


def mao_direita(c, escala=1.0, sentido=1, z=16):
    """Ícone 2D limpo da regra da mão direita: dedos curvados no sentido do giro e polegar apontando para fora (⊙) ou ao longo do eixo."""
    c = np.asarray(c, float)
    fundo = RoundedRectangle(width=1.75 * escala, height=1.45 * escala, corner_radius=0.18 * escala).move_to(c)
    fundo.set_fill(PANEL, 0.88).set_stroke(GEO, 1.8)
    fundo._fundo = True
    arco = seta_curva(c + P3(0, -0.05 * escala), 0.44 * escala, -0.5, 2.3 * sentido, cor=VETC, w=4.5, tip=0.18 * escala, z=z + 2)
    pol = VGroup(
        Circle(radius=0.18 * escala).move_to(c + P3(0, -0.05 * escala)).set_stroke(TQ, 2.6).set_fill(BACKGROUND_COLOR, 0.9),
        Dot(c + P3(0, -0.05 * escala), radius=0.055 * escala, color=TQ),
    ).set_z_index(z + 3)
    return VGroup(fundo, arco, pol).set_z_index(z)


def porta2d(dob, comp=3.2, esp=0.22, ang=0.0, z=8):
    """Esquema 2D limpo da porta vista de cima: dobradiça em `dob`, folha de comprimento `comp` girada de `ang`."""
    dob = np.asarray(dob, float)
    u = np.array([math.cos(ang), math.sin(ang), 0.0])
    n = np.array([-u[1], u[0], 0.0])
    c = dob + u * (comp / 2.0)
    folha = Polygon(
        dob - n * (esp / 2), dob + u * comp - n * (esp / 2),
        dob + u * comp + n * (esp / 2), dob + n * (esp / 2),
    )
    aco(folha, 2.2)
    mac = Circle(radius=0.08).move_to(dob + u * (comp * 0.75 / 0.80)).set_fill(WHITE_, 0.95).set_stroke(GEO, 1.8)
    piv = eixo_cruz(dob, s=0.17, z=z + 3)
    g = VGroup(folha.set_z_index(z), mac.set_z_index(z + 2), piv)
    g.dob = dob
    g.ponta = dob + u * comp
    g.mac = dob + u * (comp * 0.75 / 0.80)
    g.perto = dob + u * (comp * 0.15 / 0.80)
    return g


def chave_roda(porca, comp=2.8, ang=0.0, cano=False, comp_cano=5.2, z=8):
    """Chave de roda 2,5D com porca sextavada em `porca`, cabo de comprimento `comp` (0,40 m) e cano extensor opcional (0,80 m)."""
    porca = np.asarray(porca, float)
    u = np.array([math.cos(ang), math.sin(ang), 0.0])
    # Cabeça sextavada externa + porca sextavada interna
    cab = RegularPolygon(n=6, radius=0.34).move_to(porca).rotate(ang)
    aco(cab, 2.2)
    haste = capsula2d(porca + u * 0.22, porca + u * comp, 0.13, "#7A8696")
    aco(haste, 2.0)
    punho = capsula2d(porca + u * (comp - 0.55), porca + u * comp, 0.16, "#5C687C")
    porca_hex = RegularPolygon(n=6, radius=0.19).move_to(porca).set_fill("#DCE4F2", 0.95).set_stroke(GEO, 2.2)
    eixo = eixo_cruz(porca, s=0.13, z=z + 4)
    g = VGroup(haste.set_z_index(z), punho.set_z_index(z + 1), cab.set_z_index(z + 2), porca_hex.set_z_index(z + 3), eixo)
    if cano:
        tubo = capsula2d(porca + u * (comp * 0.45), porca + u * comp_cano, 0.20, "#6E84A8")
        aco(tubo, 2.2, op=0.92)
        g.add(tubo.set_z_index(z + 1))
        g.ponta = porca + u * comp_cano
    else:
        g.ponta = porca + u * comp
    g.porca = porca
    g.meio = porca + u * (comp * 0.5)
    g.ponta_chave = porca + u * comp
    return g


def regua2d(dob, comp=5.2, esp=0.26, ang=0.0, n_fatias=0, bancada=True, z=8):
    """Régua 2,5D com dobradiça em `dob`, bancada opcional à esquerda, marcações de 10 em 10 cm e fatias opcionais (N = 12 em T4-4)."""
    dob = np.asarray(dob, float)
    u = np.array([math.cos(ang), math.sin(ang), 0.0])
    n = np.array([-u[1], u[0], 0.0])
    g = VGroup()
    if bancada:
        mesa = Polygon(
            dob + LEFT * 1.55 + UP * (esp * 0.35),
            dob + LEFT * 0.08 + UP * (esp * 0.35),
            dob + LEFT * 0.08 + DOWN * 0.65,
            dob + LEFT * 1.55 + DOWN * 0.65,
        ).set_fill("#2E3748", 0.95).set_stroke(GEO, 2.0).set_z_index(z - 1)
        g.add(mesa)
    corpo = Polygon(
        dob - n * (esp / 2), dob + u * comp - n * (esp / 2),
        dob + u * comp + n * (esp / 2), dob + n * (esp / 2),
    )
    aco(corpo, 2.2)
    g.add(corpo.set_z_index(z))
    fatias = VGroup()
    if n_fatias > 0:
        for k in range(n_fatias):
            r0 = comp * k / n_fatias
            r1 = comp * (k + 1) / n_fatias
            fk = Polygon(
                dob + u * r0 - n * (esp / 2), dob + u * r1 - n * (esp / 2),
                dob + u * r1 + n * (esp / 2), dob + u * r0 + n * (esp / 2),
            ).set_fill(MAS, 0.18).set_stroke(GEO, 1.4, opacity=0.85).set_z_index(z + 1)
            fatias.add(fk)
        g.add(fatias)
    else:
        riscos = VGroup()
        for k in range(1, 10):
            p = dob + u * (comp * k / 10.0)
            cor_r = MAS if k == 5 else GEO
            h_r = esp * 0.42 if k == 5 else esp * 0.28
            riscos.add(Line(p + n * (esp / 2), p + n * (esp / 2 - h_r)).set_stroke(cor_r, 2.4 if k == 5 else 1.5))
        g.add(riscos.set_z_index(z + 1))
    piv = eixo_cruz(dob, s=0.16, z=z + 3)
    g.add(piv)
    g.dob = dob
    g.cm = dob + u * (comp * 0.5)
    g.dois_tercos = dob + u * (comp * 2.0 / 3.0)
    g.ponta = dob + u * comp
    g.fatias = fatias
    g.u = u
    g.n = n
    g.comp = comp
    return g


def roda(c, R=1.65, ang=0.0, raios=6, z=6):
    """Roda / polia 2,5D com aro metálico, cubo central e raios que mostram a rotação por `ang`."""
    c = np.asarray(c, float)
    disco = Circle(radius=R).move_to(c).set_fill("#1B2436", 0.85).set_stroke(GEO, 2.0)
    aro = Annulus(inner_radius=R * 0.84, outer_radius=R).move_to(c)
    aco(aro, 2.2)
    g_raios = VGroup()
    for k in range(raios):
        a = ang + 2 * math.pi * k / raios
        u = np.array([math.cos(a), math.sin(a), 0.0])
        g_raios.add(Line(c + u * (R * 0.18), c + u * (R * 0.84)).set_stroke(GEO, 3.6, opacity=0.85))
    cubo = Circle(radius=R * 0.20).move_to(c)
    aco(cubo, 2.0)
    marca = Dot(c + R * 0.92 * np.array([math.cos(ang), math.sin(ang), 0.0]), radius=0.075, color=MAS)
    eixo = eixo_cruz(c, s=0.16, z=z + 4)
    return VGroup(disco.set_z_index(z), g_raios.set_z_index(z + 1), aro.set_z_index(z + 2), cubo.set_z_index(z + 3), marca.set_z_index(z + 3), eixo)


def motor(c, escala=1.0, ang=0.0, z=6):
    """Motor elétrico/mecânico 2,5D com carcaça aletada, base e rotor frontal girando por `ang`."""
    c = np.asarray(c, float)
    carc = RoundedRectangle(width=2.5 * escala, height=1.85 * escala, corner_radius=0.26 * escala).move_to(c)
    aco(carc, 2.2)
    aletas = VGroup()
    for dy in (-0.55, -0.28, 0.0, 0.28, 0.55):
        aletas.add(Line(c + P3(-0.95 * escala, dy * escala), c + P3(0.95 * escala, dy * escala)).set_stroke("#38445A", 3.2))
    base = Polygon(
        c + P3(-0.95 * escala, -0.92 * escala), c + P3(0.95 * escala, -0.92 * escala),
        c + P3(1.15 * escala, -1.12 * escala), c + P3(-1.15 * escala, -1.12 * escala),
    ).set_fill("#4A566C", 0.95).set_stroke(GEO, 2.0)
    rotor = roda(c, R=0.62 * escala, ang=ang, raios=4, z=z + 2)
    return VGroup(base.set_z_index(z), carc.set_z_index(z), aletas.set_z_index(z + 1), rotor)


def _roda_dentada(c, R_pitch, n_dentes, mod_dente, ang=0.0, cor_corpo="#68768E", z=6):
    """Engrenagem 2,5D com dentes trapezoidais reais ao redor do raio primitivo R_pitch."""
    c = np.asarray(c, float)
    r_in = R_pitch - 0.55 * mod_dente
    r_out = R_pitch + 0.50 * mod_dente
    pts = []
    da = 2.0 * math.pi / n_dentes
    for k in range(n_dentes):
        a = ang + k * da
        # Perfil trapezoidal simétrico de cada dente
        for f, r in ((-0.36, r_in), (-0.22, r_in), (-0.11, r_out), (0.11, r_out), (0.22, r_in), (0.36, r_in)):
            th = a + f * da
            pts.append(c + np.array([r * math.cos(th), r * math.sin(th), 0.0]))
    corpo = Polygon(*pts).set_fill(cor_corpo, 0.95).set_stroke(GEO, 1.8).set_z_index(z)
    anel = Annulus(inner_radius=R_pitch * 0.28, outer_radius=R_pitch * 0.68).move_to(c).set_fill("#3E4A60", 0.85).set_stroke(GEO, 1.5).set_z_index(z + 1)
    raios = VGroup()
    for k in range(4):
        th = ang + k * math.pi / 2.0
        u = np.array([math.cos(th), math.sin(th), 0.0])
        raios.add(Line(c + u * (R_pitch * 0.25), c + u * (R_pitch * 0.68)).set_stroke(GEO, 3.2))
    cubo = Circle(radius=R_pitch * 0.25).move_to(c).set_fill("#8A98B0", 0.95).set_stroke(GEO, 1.8).set_z_index(z + 2)
    eixo = eixo_cruz(c, s=0.13, z=z + 3)
    return VGroup(corpo, anel, raios.set_z_index(z + 2), cubo, eixo)


def engrenagens(c_par, ang1=0.0, r1=0.58, razao=3, n1=8, z=6):
    """Par de engrenagens acopladas em razão 3:1 (n1 = 8 dentes, n2 = 24 dentes) sem interpenetração."""
    c_par = np.asarray(c_par, float)
    n2 = int(n1 * razao)
    r2 = r1 * razao
    mod = 2.0 * r1 / n1 * 0.82
    # Centros das engrenagens separados por r1 + r2
    c1 = c_par + LEFT * (r2 * 0.68)
    c2 = c1 + RIGHT * (r1 + r2 + 0.02)
    # Fase de engrenamento: quando a engrenagem 1 tem dente em 0 (apontando para +x), a engrenagem 2 tem vão em π (apontando para -x)
    ang2 = math.pi + math.pi / n2 - ang1 / razao
    g1 = _roda_dentada(c1, r1, n1, mod, ang=ang1, cor_corpo="#7C8CA6", z=z + 1)
    g2 = _roda_dentada(c2, r2, n2, mod, ang=ang2, cor_corpo="#5E6E88", z=z)
    g = VGroup(g2, g1)
    g.c1 = c1
    g.c2 = c2
    g.r1 = r1
    g.r2 = r2
    return g


def gangorra(piv, escala=1.0, ang=0.0, z=8):
    """Gangorra 2,5D com cavalete central em `piv`, prancha de 2,5 m (1,5 m à esq, 1,0 m à dir) e blocos de 30 kg e 45 kg."""
    piv = np.asarray(piv, float)
    u = np.array([math.cos(ang), math.sin(ang), 0.0])
    n = np.array([-u[1], u[0], 0.0])
    # Escala: 1 m = 1,85 unid Manim * escala
    km = 1.85 * escala
    r_esq, r_dir = 1.5 * km, 1.0 * km
    esp = 0.18 * escala
    cavalete = Polygon(piv, piv + P3(-0.36 * escala, -0.68 * escala), piv + P3(0.36 * escala, -0.68 * escala))
    aco(cavalete, 2.2)
    base_chao = Line(piv + P3(-2.8 * escala, -0.68 * escala), piv + P3(2.3 * escala, -0.68 * escala)).set_stroke(GEO, 2.4)
    prancha = Polygon(
        piv - u * (r_esq + 0.22 * escala),
        piv + u * (r_dir + 0.22 * escala),
        piv + u * (r_dir + 0.22 * escala) + n * esp,
        piv - u * (r_esq + 0.22 * escala) + n * esp,
    )
    aco(prancha, 2.2)
    p_esq = piv - u * r_esq + n * esp
    p_dir = piv + u * r_dir + n * esp
    h30, w30 = 0.42 * escala, 0.48 * escala
    h45, w45 = 0.54 * escala, 0.58 * escala
    b30 = Polygon(p_esq - u * (w30 / 2), p_esq + u * (w30 / 2), p_esq + u * (w30 / 2) + n * h30, p_esq - u * (w30 / 2) + n * h30)
    b30.set_fill(MAS, 0.82).set_stroke(WHITE_, 1.8)
    b45 = Polygon(p_dir - u * (w45 / 2), p_dir + u * (w45 / 2), p_dir + u * (w45 / 2) + n * h45, p_dir - u * (w45 / 2) + n * h45)
    b45.set_fill(MAS, 0.92).set_stroke(WHITE_, 1.8)
    eixo = eixo_cruz(piv, s=0.14 * escala, z=z + 4)
    g = VGroup(base_chao.set_z_index(z - 1), cavalete.set_z_index(z), prancha.set_z_index(z + 1), b30.set_z_index(z + 2), b45.set_z_index(z + 2), eixo)
    g.piv = piv
    g.p30 = p_esq
    g.p45 = p_dir
    g.c30 = p_esq + n * (h30 / 2)
    g.c45 = p_dir + n * (h45 / 2)
    return g


def vassoura(pe, comp=3.2, th=0.0, z=8):
    """Vassoura 2,5D com pé apoiado em `pe`, inclinada de `th` rad em relação à vertical (+y) para a direita (+x)."""
    pe = np.asarray(pe, float)
    u = np.array([math.sin(th), math.cos(th), 0.0])
    n = np.array([math.cos(th), -math.sin(th), 0.0])
    cabo = capsula2d(pe, pe + u * (comp * 0.88), 0.055, "#C9A27A")
    # Piaçava / escova no topo (ou na base — tratando como barra uniforme com detalhe visual leve no topo)
    topo = pe + u * comp
    base_esc = pe + u * (comp * 0.86)
    esc = Polygon(
        base_esc - n * 0.16, base_esc + n * 0.16,
        topo + n * 0.24, topo - n * 0.24,
    ).set_fill("#8A6240", 0.92).set_stroke(GEO, 1.6)
    piv = Dot(pe, radius=0.06, color=GEO)
    g = VGroup(cabo.set_z_index(z), esc.set_z_index(z + 1), piv.set_z_index(z + 2))
    g.pe = pe
    g.topo = topo
    g.cm = pe + u * (comp * 0.5)
    return g


def lapis(pe, comp=0.65, th=0.0, z=8):
    """Lápis 2,5D (15 cm) com pé apoiado em `pe`, inclinado de `th` rad em relação à vertical."""
    pe = np.asarray(pe, float)
    u = np.array([math.sin(th), math.cos(th), 0.0])
    n = np.array([math.cos(th), -math.sin(th), 0.0])
    r = 0.048
    p_meio = pe + u * (comp * 0.80)
    topo = pe + u * comp
    corpo = Polygon(pe - n * r, pe + n * r, p_meio + n * r, p_meio - n * r).set_fill("#E2A84B", 0.95).set_stroke(GEO, 1.5)
    ponta = Polygon(p_meio - n * r, p_meio + n * r, topo).set_fill("#DCE4F2", 0.95).set_stroke(GEO, 1.4)
    piv = Dot(pe, radius=0.055, color=GEO)
    g = VGroup(corpo.set_z_index(z), ponta.set_z_index(z + 1), piv.set_z_index(z + 2))
    g.pe = pe
    g.topo = topo
    return g


def disco_furado(eixo, R=1.65, ang=0.0, z=6):
    """Disco horizontal visto de cima (sem gravidade no plano do giro) com furo excêntrico: gira em torno de `eixo`,
    mas o CM está deslocado do eixo, descrevendo um círculo tracejado."""
    eixo = np.asarray(eixo, float)
    u = np.array([math.cos(ang), math.sin(ang), 0.0])
    n = np.array([-u[1], u[0], 0.0])
    # O disco está centrado no eixo, mas tem um furo circular grande de raio 0.52*R a +0.42*R na direção -u,
    # deslocando o CM para +0.36*R na direção +u!
    disco = Circle(radius=R).move_to(eixo)
    aco(disco, 2.2)
    p_furo = eixo - u * (R * 0.44)
    furo = Circle(radius=R * 0.42).move_to(p_furo).set_fill(BACKGROUND_COLOR, 0.98).set_stroke(GEO, 2.0)
    # Raios discretos para leitura nítida da rotação
    lin1 = Line(eixo + n * (R * 0.16), eixo + n * (R * 0.92)).set_stroke(GEO, 2.4, opacity=0.65)
    lin2 = Line(eixo - n * (R * 0.16), eixo - n * (R * 0.92)).set_stroke(GEO, 2.4, opacity=0.65)
    r_cm = R * 0.36
    p_cm = eixo + u * r_cm
    trilha_cm = DashedVMobject(Circle(radius=r_cm).move_to(eixo).set_stroke(MAS, 2.0, opacity=0.65), num_dashes=28)
    marca_cm = cm_pt(p_cm, r=0.095, z=z + 4)
    marca_eixo = eixo_cruz(eixo, s=0.16, z=z + 5)
    g = VGroup(disco.set_z_index(z), lin1.set_z_index(z + 1), lin2.set_z_index(z + 1), furo.set_z_index(z + 2), trilha_cm.set_z_index(z + 3), marca_cm, marca_eixo)
    g.eixo = eixo
    g.cm = p_cm
    g.r_cm = r_cm
    g.u = u
    return g


def zoom_inset(c, w=2.9, h=2.0, folga_cm=5.4, th=0.165, z=20):
    """Lupa retangular ×3 (H2) mostrando a ponta da régua e a moeda da ponta separadas por `folga_cm` (5,4 cm em t = 0,15 s)."""
    c = np.asarray(c, float)
    cx = RoundedRectangle(width=w, height=h, corner_radius=0.16).move_to(c)
    cx.set_fill(PANEL, 0.92).set_stroke(GEO, 2.2)
    cx._fundo = True
    # Escala ampliada dentro da lupa: 5,4 cm ≈ 0,72 unidades de altura
    h_gap = clamp(folga_cm / 5.4 * 0.72, 0.05, 0.85)
    y_moeda = c[1] + 0.34
    y_ponta = y_moeda - h_gap
    # Moeda ampliada
    moeda = RoundedRectangle(width=0.68, height=0.13, corner_radius=0.04).move_to(P3(c[0] + 0.15, y_moeda))
    moeda.set_fill("#EAF0FA", 0.98).set_stroke(WHITE_, 1.8)
    # Ponta da régua inclinada ampliada
    u = np.array([math.cos(-th), math.sin(-th), 0.0])
    n = np.array([-u[1], u[0], 0.0])
    p_fim = P3(c[0] + 0.42, y_ponta)
    p_ini = p_fim - u * 1.45
    esp = 0.18
    reg = Polygon(p_ini, p_fim, p_fim - n * esp, p_ini - n * esp)
    aco(reg, 2.0)
    # Cota vertical da folga
    x_cota = c[0] + 0.68
    cota = VGroup(
        Line(P3(x_cota, y_ponta), P3(x_cota, y_moeda)).set_stroke(ACC, 2.8),
        Line(P3(x_cota - 0.10, y_ponta), P3(x_cota + 0.10, y_ponta)).set_stroke(ACC, 2.4),
        Line(P3(x_cota - 0.10, y_moeda), P3(x_cota + 0.10, y_moeda)).set_stroke(ACC, 2.4),
    )
    g = VGroup(cx.set_z_index(z), reg.set_z_index(z + 1), moeda.set_z_index(z + 2), cota.set_z_index(z + 3))
    g.cota = cota
    g.moeda = moeda
    g.ponta = p_fim
    return g


def pedaco(c, r0, r1, a0, da, op, z=6):
    """Pedaço de disco (setor de anel) em rosa: opacidade = massa relativa."""
    s = AnnularSector(inner_radius=r0, outer_radius=r1, start_angle=a0, angle=da, arc_center=np.asarray(c, float))
    return s.set_fill(MAS, op).set_stroke(mix(MAS, 0.2), 1.6, opacity=0.9).set_z_index(z)


def disco_aco(c, R, z=4):
    d = Circle(radius=R).move_to(c)
    aco(d, 2.2)
    return d.set_z_index(z)


class DiscoPedacos(VGroup):
    """Disco uniforme de raio R em nr anéis × nt setores (T3-1 a T3-6)."""

    def __init__(self, c, R, nr=4, nt=10, M=1.0, op0=0.28, op1=0.7):
        super().__init__()
        self.c, self.R, self.M = np.asarray(c, float), R, M
        self.corpo = disco_aco(c, R)
        self.pec, self.dados = VGroup(), []
        A = math.pi * R ** 2
        for i in range(nr):
            r0, r1 = R * i / nr, R * (i + 1) / nr
            area = (r1 ** 2 - r0 ** 2) * math.pi / nt
            for k in range(nt):
                a0 = 2 * math.pi * k / nt
                op = op0 + (op1 - op0) * (area / ((R ** 2 - (R * (nr - 1) / nr) ** 2) * math.pi / nt))
                self.pec.add(pedaco(c, r0, r1, a0, 2 * math.pi / nt, op))
                self.dados.append({"m": M * area / A, "r": math.sqrt((r0 ** 2 + r1 ** 2) / 2), "a": a0 + math.pi / nt, "r0": r0, "r1": r1})
        self.add(self.corpo, self.pec)

    def centro_de(self, k):
        d = self.dados[k]
        return self.c + d["r"] * np.array([math.cos(d["a"]), math.sin(d["a"]), 0])


class Lote22(Prob2):
    """Base dos lotes do yt_0022: canto de duas linhas, selo único na faixa, CONTA em Pilha (x 0,6…6,7; y −3,25…2,35)."""
    FUNDO = "fundo_lab.png"

    def construct(self):
        self.setup_base()
        self.corpo()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def corpo(self):
        raise NotImplementedError

    def lab(self, s, alvo, lados=(UP, RIGHT, DOWN, LEFT, UR, DR, UL, DL), size=40, cor=None, buffs=(0.14, 0.26, 0.38), ignorar=(), zona=None):
        """Rótulo MathTex (cor por token) posto com teste de colisão a ≤ 0,4 do dono."""
        m = T(s, size, cor)
        r = self.rotulo(m, alvo, lados=lados, buffs=buffs, ignorar=ignorar, zona=zona or (-7.45, 7.45, -4.0, 2.5), chamada=False)
        return r[0]


def _monta(self, A, ia, voos, rt=1.0, arco=-0.5, ate=None):
    """Linha A (já posta na Pilha) construída da esquerda para a direita: partes em `voos` voam do desenho; o resto escreve na sua vez."""
    pares = [(src, mp(A, ia, [k])) for k, src in voos.items()]
    resto = [k for k in range(len(ia)) if k not in voos and ia[k] and (ate is None or k <= ate)]
    self.voa(pares, extra=[], rt=rt, origem=False, arco_esq=arco, escrever=[mp(A, ia, [k]) for k in resto])
    self.foco = A


Lote22.monta = _monta
Lote21 = Lote22


import kit as _kit  # noqa: E402


def gidx(m, idx, simbolo, k=0):
    """Índice (em m[0]) do glifo de `idx` que a forma reconhece como `simbolo` com tamanho óptico k (0 principal, 1 índice, 2 expoente)."""
    for j in idx:
        r = _kit._id_glifo(m[0][j])
        if r is not None and r == (simbolo, k):
            return j
    return idx[0]
