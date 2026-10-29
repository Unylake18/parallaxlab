"""Gera as timelines dos trechos Three.js do v2 a partir de ancoras.json (durações nominais da narração congelada v3):
threejs/timeline_hook.json (H1–H3, manequim), timeline_e4.json (E4-1, muro recuado) e timeline_trilho.json (T2-1..T2-4).
Única fonte de tempo: o cena3d (Three.js) e a camada Manim leem os mesmos arquivos. Depois da voz, só os tempos mudam."""
import json
import math
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ANC = json.loads((AQUI / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
FPS = 15
G_, H_ = 9.8, 2.5
T_PREP, T_QUEDA = 1.0, math.sqrt(2 * H_ / G_)
T_C = T_PREP + T_QUEDA                                   # τ do contato com o chão


def inicios(ids):
    t, out = 0.0, {}
    for a in ids:
        out[a] = round(t, 2)
        t += ANC[a]["dur"]
    return out, round(t, 2)


def lin(keys, x):
    if x <= keys[0][0]:
        return keys[0][1]
    for (a, va), (b, vb) in zip(keys, keys[1:]):
        if x <= b:
            return va + (vb - va) * (x - a) / (b - a)
    return keys[-1][1]


def salto(n, f_ini, lento, tau_fim, tau_ini=0.0):
    """τ por quadro: parado em tau_ini até f_ini; depois dτ/dt = r(τ) (1 → `lento` perto do contato → 1) até tau_fim."""
    r = [(T_C - 0.32, 1.0), (T_C - 0.1, lento), (T_C + 0.24, lento), (T_C + 0.5, 1.0)]
    out, tau = [], tau_ini
    sub = 16
    for f in range(n):
        out.append(round(tau, 5))
        if f >= f_ini and tau < tau_fim:
            for _ in range(sub):
                tau = min(tau_fim, tau + lin(r, tau) / (FPS * sub))
    return out


def primeiro(lista, alvo):
    return next(i for i, v in enumerate(lista) if v >= alvo)


# câmeras 3/4 baixas (fov 30°); alvo em metros; (xc, yc) = onde o alvo aparece no quadro do Manim
C1 = {"az": -78, "el": 8, "fov": 30, "alt": 6.2, "alvo": [0.45, 0, 1.95], "xc": -0.5, "yc": -0.7}
C2 = {"az": -90, "el": 12, "fov": 30, "alt": 5.6, "alvo": [2.6, 0, 1.45], "xc": 0.0, "yc": -0.65}   # H3: vista de frente, cenários espelhados em x = 2,6
C1D = dict(C1, alt=round(6.2 * 0.92, 3))                                                          # v5: 8% mais perto
C1Z = {"az": -74, "el": 7, "fov": 30, "alt": 3.7, "alvo": [0.9, 0, 1.4], "xc": 0.8, "yc": -0.3}
C3 = {"az": -78, "el": 8, "fov": 30, "alt": 6.2, "alvo": [0.45, 0, 1.95], "xc": -3.0, "yc": -0.7}    # E4-1: a câmera do hook, cena no PALCO
GEOM = {"fator_3d_manim": 1.0, "centro_manim": [0.0, 0.0]}

# ── HOOK · H1–H3 ─────────────────────────────────────────────────────────────────────────────────────────
S, T = inicios(["H1", "H2", "H3"])
n = round(T * FPS)
fH2, fH3 = round(S["H2"] * FPS), round(S["H3"] * FPS)
tauA = salto(fH2, round(1.2 * FPS), 0.18, T_C + 1.6)                                    # H1: pernas duras
tauA += salto(fH3 - fH2, round(1.0 * FPS), 0.18, T_C + 1.6)                           # H2: joelhos (reset)
t3 = salto(n - fH3, round(3.6 * FPS), 0.22, T_C + 1.6)                                # H3: os dois juntos
tauA += t3
tauB = [-1.0] * fH3 + t3
modoA = "d" * fH2 + "j" * (fH3 - fH2) + "d" * (n - fH3)
modoB = "j" * n
c1, c2 = fH2 + primeiro(tauA[fH2:], T_C), fH3 + primeiro(t3, T_C)
contatos = {"H1": round(primeiro(tauA, T_C) / FPS, 2), "H2": round(c1 / FPS, 2), "H3": round(c2 / FPS, 2)}
lentos =[[round((primeiro(tauA[f0:], T_C - 0.12) + f0) / FPS, 2), round((primeiro(tauA[f0:], T_C + 0.3) + f0) / FPS, 2)] for f0 in (0, fH2, fH3)]
TLH = {
    "_leia_me": "Hook H1–H3: manequim no muro. tau[f] = tempo físico do salto do ator no quadro f (−1 = oculto); modo 'd'/'j'.",
    "duracao_s": T, "ancoras": S, "geometria": GEOM,
    "atores": [{"id": "A", "x": 0.0, "tau": tauA, "modo": modoA}, {"id": "B", "x": 5.2, "espelho": True, "tau": tauB, "modo": modoB}],
    "camera": [{"t": 0.0, "modo": "obl", "cfg": C1}, {"t": 4.0, "modo": "obl", "cfg": C1},           # v5: dolly-in lento (−8%) depois do pouso
               {"t": round(S["H2"] - 0.45, 2), "modo": "obl", "cfg": C1D}, {"t": S["H2"], "modo": "obl", "cfg": C1D},
               {"t": round(S["H2"] + 0.07, 2), "modo": "obl", "cfg": C1}, {"t": round(S["H2"] + 2.2, 2), "modo": "obl", "cfg": C1},
               {"t": round(S["H2"] + 3.8, 2), "modo": "obl", "cfg": C1Z}, {"t": round(S["H3"] + 0.2, 2), "modo": "obl", "cfg": C1Z},
               {"t": round(S["H3"] + 3.2, 2), "modo": "obl", "cfg": C2}, {"t": T, "modo": "obl", "cfg": C2}],
    "fade_out": [{"t": 0.0, "v": 1.0}, {"t": 0.6, "v": 0.0},
                 {"t": round(S["H2"] - 0.4, 2), "v": 0.0}, {"t": S["H2"], "v": 1.0}, {"t": round(S["H2"] + 0.4, 2), "v": 0.0},
                 {"t": round(S["H3"] - 0.4, 2), "v": 0.0}, {"t": S["H3"], "v": 1.0}, {"t": round(S["H3"] + 0.4, 2), "v": 0.0},
                 {"t": round(T - 0.7, 2), "v": 0.0}, {"t": T, "v": 1.0}],
    "eventos": {"contato": contatos, "camera_lenta": lentos},
    "proj": {"c1": 30, "c2": round((S["H3"] + 4.0) * FPS)},
    "qa_alinhamento": {"janelas": [[0, fH2 - 1, 30], [round((S["H3"] + 3.3) * FPS), n - 12, round((S["H3"] + 4.0) * FPS)]]},
}
(AQUI / "threejs" / "timeline_hook.json").write_text(json.dumps(TLH), encoding="utf-8")
print("hook", T, "s,", n, "quadros; contatos", contatos, "; câmera lenta", lentos)

# ── E4-1 · muro recuado ──────────────────────────────────────────────────────────────────────────────────
T4 = round(ANC["E4-1"]["dur"], 2)
n4 = round(T4 * FPS)
TLE = {
    "_leia_me": "E4-1: o cenário do hook recuado (realce_3d) atrás dos números do Manim.",
    "duracao_s": T4, "geometria": GEOM,
    "atores": [{"id": "A", "x": 0.0, "tau": [round(0.05 + 0.4 * f / n4, 4) for f in range(n4)], "modo": "d" * n4}],
    "camera": [{"t": 0.0, "modo": "obl", "cfg": C3}, {"t": T4, "modo": "obl", "cfg": C3}],
    "realce_3d": [{"t": 0.0, "v": 0.6}, {"t": T4, "v": 0.6}],
    "fade_out": [{"t": 0.0, "v": 1.0}, {"t": 0.45, "v": 0.0}, {"t": round(T4 - 0.6, 2), "v": 0.0}, {"t": T4, "v": 1.0}],
    "proj": {"c3": 20},
    "qa_alinhamento": {"janelas": [[0, n4 - 1, 20]]},
}
(AQUI / "threejs" / "timeline_e4.json").write_text(json.dumps(TLE), encoding="utf-8")
print("e4", T4, "s,", n4, "quadros")

# ── T2 · trilho de ar (T2-1..T2-4) ───────────────────────────────────────────────────────────────────────
ST, T1 = inicios(["T2-1", "T2-2", "T2-3", "T2-4"])
V = 0.9
t_expl = round(ST["T2-1"] + 14.2, 2)
e1_fim = round(ST["T2-2"] - 0.3, 2)
e2_ini, e2_move = round(ST["T2-2"] - 0.2, 2), round(ST["T2-2"] + 0.4, 2)
e3_ini = round(ST["T2-3"] + 0.2, 2)
e3_fim = round(e3_ini + 12.5, 2)
e4_ini = round(ST["T2-4"] + 0.4, 2)
TL1 = {
    "_leia_me": "Fonte única de tempos do trecho T2 (trilho de ar). Quadro do Manim 16×9 (x −8..8, y −4,5..4,5).",
    "duracao_s": T1,
    "ancoras": ST,
    "geometria": {"fator_3d_manim": 1.0, "centro_manim": [0.0, -0.3], "carrinho_meia_largura": 1.0, "fov_frente": 22, "el_frente": 7,
                  "obl": {"az": -62, "d_az": 1.0, "el": 16, "fov": 26, "alt": 8.0, "alvo": [0, 0, 0.25], "yc": 0.0, "xc": 0.0}},
    "ensaios": [
        {"tipo": "explosao", "vis": [0.0, e1_fim], "t_evento": t_expl, "x0": 1.4, "v": V},
        {"tipo": "colisao", "vis": [e2_ini, round(e3_ini - 0.6, 2)], "t_move": e2_move, "x0": 6.0, "v": V},
        {"tipo": "colisao", "vis": [e3_ini, e3_fim], "t_move": e3_ini, "x0": 6.0, "v": V, "visao_do_carro": True},
        {"tipo": "colisao", "vis": [e4_ini, T1], "t_move": e4_ini, "x0": 6.0, "v": V, "visao_do_carro": True},
    ],
    "camera": [{"t": 0.0, "modo": "obl"}, {"t": 6.0, "modo": "obl"}, {"t": 11.0, "modo": "frente"}, {"t": T1, "modo": "frente"}],
    "cam_x": [{"t": 0.0, "x": 0.0}, {"t": round(e3_ini - 1.2, 2), "x": 0.0}, {"t": e3_ini, "x": -6.0},
              {"t": e3_fim, "x": round(-6.0 + V * (e3_fim - e3_ini), 3), "ease": "linear"},
              {"t": round(e4_ini - 0.3, 2), "x": -6.0}, {"t": e4_ini, "x": -6.0},
              {"t": T1, "x": round(-6.0 + V * (T1 - e4_ini), 3), "ease": "linear"}],
    "realce_3d": [{"t": 0.0, "v": 0.0}, {"t": round(e4_ini + 1.0, 2), "v": 0.0}, {"t": round(e4_ini + 2.4, 2), "v": 0.7},
                  {"t": T1, "v": 0.7}],
    "fade_out": [{"t": 0.0, "v": 1.0}, {"t": 0.45, "v": 0.0}, {"t": round(ST["T2-4"] + 10.2, 2), "v": 0.0},
                 {"t": round(ST["T2-4"] + 11.0, 2), "v": 1.0}, {"t": T1, "v": 1.0}],
    "eventos": {"explosao": t_expl, "visao_do_carro_1": e3_ini, "visao_do_carro_2": e4_ini, "equacao_entra": round(e4_ini + 6.2, 2),
                "casos": round(ST["T2-4"] + 11.0, 2)},
    "qa_alinhamento": {"quadros": [int(18 * 15), int((e2_move + 3) * 15), int((e3_ini + 3) * 15), int((e3_ini + 9) * 15), int((e4_ini + 8) * 15)]},
}
(AQUI / "threejs" / "timeline_trilho.json").write_text(json.dumps(TL1, indent=1), encoding="utf-8")
print("trilho", T1, "s,", round(T1 * 15), "quadros; explosão em", t_expl)

# ── F2 · o cavalo e a corda (asset CC0 da Quaternius) ───────────────────────────────────────────────────────
TF = round(ANC["F2"]["dur"], 2)
TLC = {
    "_leia_me": "F2: cavalo CC0 (assets_unidade/cavalo) puxando a pedra; vista lateral alinhada ao Manim (plano y = 0).",
    "duracao_s": TF,
    "geometria": {"fator_3d_manim": 1.0, "centro_manim": [0.0, -2.55], "fov_frente": 18, "el_frente": 4},
    "camera": [{"t": 0.0, "modo": "frente"}, {"t": TF, "modo": "frente"}],
    "cavalo": {"comprimento": 6.3, "x_cavalo": 1.6, "x_pedra": -5.2, "pedra_r": 0.72, "yaw": round(math.pi / 2, 5), "incl": 0.07,
               "ritmo": 0.55, "tau0": 0.0, "v_ini": 0.02, "t_desliza": round(0.7 * TF, 2), "a_desliza": 0.07,
               "peito_fx": -0.41, "peito_fz": 0.56},                           # v5: gancho na traseira, na altura do quadril
    "fade_out": [{"t": 0.0, "v": 1.0}, {"t": 0.5, "v": 0.0}, {"t": round(TF - 0.6, 2), "v": 0.0}, {"t": TF, "v": 1.0}],
    "proj_todos": True,
}
(AQUI / "threejs" / "timeline_cavalo.json").write_text(json.dumps(TLC, indent=1), encoding="utf-8")
print("cavalo", TF, "s,", round(TF * FPS), "quadros")

# ── manequim de pé (imagem para o E5-5): sem muro, sem chão, sem estrelas ─────────────────────────────────────
TLM = {"_leia_me": "Um quadro do manequim de pé (depois do pouso de pernas duras), para recortar como PNG.", "duracao_s": round(1 / FPS, 4),
       "geometria": GEOM, "sem_ceu": True, "sem_chao": True,
       "atores": [{"id": "A", "x": 0.0, "sem_muro": True, "tau": [round(T_C + 1.6, 4)], "modo": "d"}],
       "camera": [{"t": 0.0, "modo": "obl", "cfg": {"az": -62, "el": 6, "fov": 20, "alt": 2.3, "alvo": [1.05, 0, 0.9], "xc": 0, "yc": 0}},
                  {"t": 1.0, "modo": "obl", "cfg": {"az": -62, "el": 6, "fov": 20, "alt": 2.3, "alvo": [1.05, 0, 0.9], "xc": 0, "yc": 0}}]}
(AQUI / "threejs" / "timeline_manequim.json").write_text(json.dumps(TLM), encoding="utf-8")
