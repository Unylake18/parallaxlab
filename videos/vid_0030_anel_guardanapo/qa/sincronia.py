"""QA de sincronia (v5): cada par fala ↔ tela, com o instante da palavra (alinhamento forçado do ElevenLabs,
alinhamento_palavras.json) e o instante em que a tela começa a mostrar a coisa (evento/chave do timeline.json, corrigido
pelos atrasos reais da cena do Manim, media_preview/estados_CenaMat.json). Tolerância: ±0,2 s (pedido do Kaio).
Uso (raiz): uv run python videos/vid_0030_anel_guardanapo/qa/sincronia.py
"""
import json
from pathlib import Path

UNIT = Path(__file__).resolve().parents[1]
TOL = 0.2
TL = json.loads((UNIT / "timeline.json").read_text(encoding="utf-8"))
E, CH = TL["eventos"], TL["chaves"]
P = json.loads((UNIT / "alinhamento_palavras.json").read_text(encoding="utf-8"))
palavras = [w["word"].lower().strip(".,:;!?…") for w in P]
est = UNIT / "media_preview" / "estados_CenaMat.json"
ATRASO = {a["evento"]: a["chegou"] for a in json.loads(est.read_text(encoding="utf-8"))["atrasos"]} if est.exists() else {}


def fala(trecho, depois=0.0):
    alvo = trecho.lower().split()
    for i in range(len(P) - len(alvo) + 1):
        if P[i]["start"] >= depois and palavras[i:i + len(alvo)] == alvo:
            return P[i]["start"]
    raise ValueError(trecho)


def ev(nome, i=None):
    v = E[nome] if i is None else E[nome][i]
    return ATRASO.get(nome, v) if i is None else v


def muda(nome, apos=0.0, fim=False):
    """Instante em que a chave começa (ou termina, fim=True) a primeira mudança depois de `apos`."""
    ch = CH[nome]
    for a, b in zip(ch, ch[1:]):
        if b["t"] > apos and a["v"] != b["v"]:
            return b["t"] if fim else a["t"]
    raise ValueError(nome)


PARES = [  # (fala, depois de, instante da tela, o que a tela mostra)
    ("anel que segura", 0, ev("tag_guardanapo"), "etiqueta ANEL DE GUARDANAPO"),
    ("esfera e fura", 14, muda("esfera_fantasma", 14), "a esfera fantasma envolve o anel"),
    ("fura bem no meio", 14, ev("tag_furada"), "etiqueta = ESFERA FURADA"),
    ("furadeira", 0, muda("broca_L", 15), "a broca atravessa a esfera"),
    ("o que sobra", 20, muda("esfera_fantasma", 20), "a esfera some e o anel se destaca"),
    ("três esferas", 0, muda("trio_tampa", 20), "as três esferas aparecem"),
    ("pequena", 0, ev("hook_rotulos", 0), "R = 5 cm"),
    ("média", 0, ev("hook_rotulos", 1), "R = 7 cm"),
    ("grande", 25, ev("hook_rotulos", 2), "R = 10 cm"),
    ("furadas", 0, muda("trio_broca_L", 25), "as três brocas entram"),
    ("anéis fiquem", 0, muda("trio_junta", 25), "os anéis se juntam no trio"),
    ("mesma altura", 30, ev("hook_titulo2"), "MESMA ALTURA: h = 6 cm"),
    ("seis centímetros", 0, ev("hook_regua"), "réguas de 6 cm"),
    ("qual deles", 0, ev("hook_titulo"), "QUAL TEM MAIS VOLUME?"),
    ("cortando", 0, muda("corte_v", 30), "o corte vertical abre o anel"),
    ("raio da esfera", 36, muda("tri_R", 30), "lado R do triângulo"),
    ("raio do furo", 37, muda("tri_a", 30), "lado a"),
    ("metade da altura", 39, muda("tri_h", 30), "lado h/2"),
    ("triângulo retângulo", 0, muda("tri_hcheia", 30, fim=True), "triângulo completo"),
    ("por pitágoras", 42, ev("eq_pitagoras"), "R² = a² + (h/2)²"),
    ("menos", 44, ev("eq_relacao"), "a² muda de lado: R² − a² = (h/2)²"),
    ("anota essa relação", 0, ev("memo"), "a relação vira o lembrete"),
    ("fatiar", 0, muda("plano_z", 50), "o plano sobe pelo anel"),
    ("tipo um cd", 0, ev("rotulos_fatia"), "coroa destacada com os raios"),
    ("o raio de fora", 0, ev("eq_rext"), "r_ext² = R² − z²"),
    ("o raio de dentro", 0, ev("eq_rint"), "r_int² = a²"),
    ("a área é pi", 0, ev("eq_area"), "A(z) = π(r_ext² − r_int²)"),
    ("diferença desses", 0, ev("eq_area_subst"), "substitui os quadrados"),
    ("reorganizando", 0, ev("eq_reagrupa"), "a² e z² trocam de lugar"),
    ("justamente", 0, ev("destaca_par"), "R² − a² destacado no lembrete"),
    ("isso vale", 0, ev("R_some"), "o bloco sai e (h/2)² entra"),
    ("o raio da esfera sumiu", 0, ev("R_sumiu_txt"), "O RAIO DA ESFERA SUMIU + esfera fantasma"),
    ("uma esfera de raio", 0, muda("cav_vis", 80), "esfera pequena aparece"),
    ("raio igual", 0, ev("cav_rotulos"), "raio h/2"),
    ("nela", 0, ev("cav_tri"), "triângulo na esfera pequena (ρ, z, h/2)"),
    ("por pitágoras", 92, ev("cav_eq_esfera"), "ρ² + z² = (h/2)²"),
    ("diferença entre", 0, ev("cav_eq_esfera2"), "A_esf(z) = πρ² = π[(h/2)² − z²]"),
    ("sobe o plano", 0, muda("plano_z", 95), "o plano sobe"),
    ("desce o plano", 0, muda("plano_z", 100.95), "o plano desce"),
    ("as áreas continuam", 0, ev("cav_titulo"), "MESMA ÁREA EM TODA ALTURA"),
    ("princípio de cavalieri", 0, ev("cav_eq_iguais"), "A_anel(z) = A_esf(z) na caixa"),
    ("mesmo volume", 108, ev("cav_conclusao"), "LOGO, MESMO VOLUME"),
    ("então o volume", 0, ev("volume_igual"), "V_anel = V_esf"),
    ("quatro terços", 0, ev("volume_formula"), "V = (4/3)π(h/2)³"),
    ("o cubo da metade é", 0, ev("volume_passo"), "(h/2)³ = h³/2³"),
    ("sobre oito", 120, ev("volume_oito"), "2³ = 8 numa fração só"),
    ("quatro sobre oito", 0, ev("volume_risca"), "riscos: 4 → 1, 8 → 2"),
    ("um meio vezes", 0, ev("volume_meio"), "V = πh³/(3·2)"),
    ("dá um sexto", 0, ev("volume_final"), "3·2 → 6"),
    ("pi vezes a altura ao cubo", 126, ev("volume_caixa"), "caixa V = πh³/6"),
    ("olha as paredes", 0, ev("paredes_entra"), "corte das três paredes"),
    ("um centímetro", 0, ev("paredes_val", 0), "1,00 cm"),
    ("sessenta e oito", 0, ev("paredes_val", 1), "0,68 cm"),
    ("quarenta e seis", 0, ev("paredes_val", 2), "0,46 cm"),
    ("aumentando a esfera", 0, muda("R_anel", 140), "R começa a crescer (contador)"),
    ("só um cuidado", 0, ev("protecao_c06") + 0.4, "frase de proteção"),
    ("sem furo", 0, muda("h_anel", 150), "o anel engrossa até a esfera"),
    ("fórmula devolve", 0, ev("limite_esfera"), "V = π(2R)³/6"),
    ("aumenta o furo", 0, muda("h_anel", 159), "o anel afina"),
    ("a altura e o volume", 160, ev("limite_zero"), "h → 0 ⇒ V → 0 (o fio já chegou a h = 0)"),
    ("pergunta respondida", 0, muda("trio_vis", 160), "o trio volta"),
    ("empate triplo", 0, ev("trio_volumes"), "V = 36π nos três"),
    ("só a altura determina", 0, ev("conclusao_txt"), "SÓ A ALTURA DETERMINA O VOLUME + V = πh³/6"),
    ("qual era o seu", 0, ev("endcard"), "cartão final"),
]
linhas, ruins = [], 0
for frase, depois, t_tela, oque in PARES:
    t_fala = fala(frase, depois)
    d = round(t_tela - t_fala, 2)
    ok = abs(d) <= TOL + 1e-9
    ruins += not ok
    linhas.append({"fala": frase, "t_fala": t_fala, "t_tela": round(t_tela, 2), "tela_menos_fala": d, "ok": ok, "tela": oque})
out = {"tolerancia_s": TOL, "pares": len(PARES), "fora_da_tolerancia": ruins,
       "maior_desvio_s": max(abs(l["tela_menos_fala"]) for l in linhas), "atrasos_manim": ATRASO, "tabela": linhas}
(UNIT / "qa" / "sincronia_v5.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for l in linhas:
    print(f"{'ok ' if l['ok'] else 'XX '} {l['t_fala']:7.2f} → {l['t_tela']:7.2f} ({l['tela_menos_fala']:+.2f})  {l['fala']}  ·  {l['tela']}")
print("pares:", len(PARES), "| fora de ±0,2 s:", ruins, "| maior desvio:", out["maior_desvio_s"], "| atrasos Manim:", ATRASO)
