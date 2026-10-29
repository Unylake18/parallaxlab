"""Gera threejs/timeline_c01.json e timeline_c13.json a partir de ancoras.json (durações nominais da narração congelada).
Única fonte de tempo dos trechos 3D: o cena3d (Three.js) e a camada Manim leem os mesmos arquivos. Depois da voz, só os
tempos mudam e os dois lados são re-renderizados."""
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ANC = json.loads((AQUI / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]


def inicios(ids):
    t, out = 0.0, {}
    for a in ids:
        out[a] = t
        t += ANC[a]["dur"]
    return out, t


# ── T1 · C01-1 a C01-5 ────────────────────────────────────────────────────────────────────────────────────
ST, T1 = inicios(["C01-1", "C01-2", "C01-3", "C01-4", "C01-5"])
V = 0.9
t_expl = round(ST["C01-2"] + 3.2, 2)
e1_fim = round(t_expl + 5.6, 2)
e2_ini, e2_move = round(ST["C01-3"] - 2.0, 2), round(ST["C01-3"] + 0.7, 2)
e3_ini = round(ST["C01-4"] + 0.2, 2)
e3_fim = round(e3_ini + 12.5, 2)
e4_ini = round(ST["C01-5"] + 1.0, 2)
cx3_fim = e3_fim
TL1 = {
    "_leia_me": "Fonte única de tempos do trecho C01 (T1). Quadro do Manim 16×9 (x −8..8, y −4,5..4,5).",
    "duracao_s": round(T1, 2),
    "ancoras": ST,
    "geometria": {"fator_3d_manim": 1.0, "centro_manim": [0.0, -0.5], "carrinho_meia_largura": 1.0, "fov_frente": 14, "el_frente": 0,
                  "obl": {"az": -62, "d_az": 1.0, "el": 16, "fov": 26, "alt": 8.0, "alvo": [0, 0, 0.25], "yc": 0.0, "xc": 0.0}},
    "ensaios": [
        {"tipo": "explosao", "vis": [0.0, e1_fim], "t_evento": t_expl, "x0": 1.4, "v": V},
        {"tipo": "colisao", "vis": [e2_ini, round(e3_ini - 0.8, 2)], "t_move": e2_move, "x0": 6.0, "v": V},
        {"tipo": "colisao", "vis": [e3_ini, e3_fim], "t_move": e3_ini, "x0": 6.0, "v": V, "visao_do_carro": True},
        {"tipo": "colisao", "vis": [e4_ini, round(T1, 2)], "t_move": e4_ini, "x0": 6.0, "v": V, "visao_do_carro": True},
    ],
    "camera": [{"t": 0.0, "modo": "obl"}, {"t": 7.0, "modo": "obl"}, {"t": 12.0, "modo": "frente"}, {"t": round(T1, 2), "modo": "frente"}],
    "cam_x": [{"t": 0.0, "x": 0.0}, {"t": round(e3_ini - 1.2, 2), "x": 0.0}, {"t": e3_ini, "x": -6.0},
              {"t": e3_fim, "x": round(-6.0 + V * (e3_fim - e3_ini), 3), "ease": "linear"},
              {"t": round(e4_ini - 0.4, 2), "x": -6.0}, {"t": e4_ini, "x": -6.0},
              {"t": round(T1, 2), "x": round(-6.0 + V * (T1 - e4_ini), 3), "ease": "linear"}],
    "realce_3d": [{"t": 0.0, "v": 0.0}, {"t": round(e4_ini + 1.0, 2), "v": 0.0}, {"t": round(e4_ini + 2.4, 2), "v": 0.7},
                  {"t": round(T1, 2), "v": 0.7}],
    "fade_out": [{"t": 0.0, "v": 0.0}, {"t": round(T1 - 1.6, 2), "v": 0.0}, {"t": round(T1, 2), "v": 1.0}],
    "eventos": {"explosao": t_expl, "visao_do_carro_1": e3_ini, "visao_do_carro_2": e4_ini, "equacao_entra": round(e4_ini + 1.6, 2)},
    "qa_alinhamento": {"quadros": [int(25 * 15), int((e2_move + 3) * 15), int((e3_ini + 3) * 15), int((e3_ini + 9) * 15), int((e4_ini + 8) * 15)]},
}
(AQUI / "threejs" / "timeline_c01.json").write_text(json.dumps(TL1, indent=1), encoding="utf-8")

# ── T2 · C13-2 a C13-5 ────────────────────────────────────────────────────────────────────────────────────
S2, T2 = inicios(["C13-2", "C13-3", "C13-4", "C13-5"])
TL2 = {
    "_leia_me": "Fonte única de tempos do trecho C13 (T2).",
    "duracao_s": round(T2, 2),
    "ancoras": S2,
    "geometria": {"fator_3d_manim": 1.0, "centro_manim": [-2.6, 0.3], "fov_frente": 14, "el_frente": 0,
                  "obl": {"az": -70, "d_az": 0.6, "el": 14, "fov": 26, "alt": 9.5, "alvo": [0, 0, -1.2], "yc": 0.0, "xc": 0.0}},
    "raio": {"theta1": 50.0, "n": 1.333, "v1": 2.4, "L": 3.6, "periodo": 0.30, "t_troca": round(S2["C13-3"] + 1.0, 2), "z_fundo": -3.8},
    "tanque": {"x0": -4.9, "x1": 4.1},
    "camera": [{"t": 0.0, "modo": "obl"}, {"t": 3.0, "modo": "obl"}, {"t": 7.0, "modo": "frente"}, {"t": round(T2, 2), "modo": "frente"}],
    "fade_out": [{"t": 0.0, "v": 0.0}, {"t": round(T2 - 1.6, 2), "v": 0.0}, {"t": round(T2, 2), "v": 1.0}],
    "eventos": {"espelho": S2["C13-2"], "troca_espelho_agua": round(S2["C13-3"] + 1.0, 2), "equacao_snell": S2["C13-3"] + 10.0,
                "constante": S2["C13-4"], "aproxima_normal": S2["C13-5"]},
    "qa_alinhamento": {"quadros": [int(12 * 15), int((S2["C13-3"] + 6) * 15), int((S2["C13-5"] + 4) * 15)]},
}
(AQUI / "threejs" / "timeline_c13.json").write_text(json.dumps(TL2, indent=1), encoding="utf-8")
print("T1", round(T1, 2), "s,", round(T1 * 15), "quadros | T2", round(T2, 2), "s,", round(T2 * 15), "quadros")
