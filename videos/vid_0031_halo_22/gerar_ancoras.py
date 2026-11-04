"""Âncoras do vid_0031: nome -> instante real (s) da voz, a partir de alinhamento_palavras.json.
Cada âncora marca o início de uma frase falada que dispara um evento visual. Ordem crescente obrigatória.
Saída: ancoras.json  {"A": {nome: t}, "order": [...], "audio_end": s, "fim": s}"""
import json
import re
import wave
from pathlib import Path

PASTA = Path(__file__).resolve().parent
PAL = json.loads((PASTA / "alinhamento_palavras.json").read_text(encoding="utf-8"))
norm = lambda s: re.sub(r"[^\wáéíóúâêôãõàçü]", "", s.lower())
W = [norm(p["word"]) for p in PAL]


def acha(frase, apos=0):
    seq = [norm(x) for x in frase.split()]
    for i in range(apos, len(W) - len(seq) + 1):
        if W[i:i + len(seq)] == seq:
            return i
    raise KeyError(frase)


# nome: frase falada (início); 71 âncoras (handoff v8 §C.2)
F = [
    ("C01_halo", "isso é um halo solar"),
    ("C01_cristais", "sempre com vinte e dois graus"),
    ("C01_seguranca", "e nunca olha direto"),
    ("C02_raio_no_cristal", "o halo é luz do sol"),
    ("C02_lupa", "prismas de seis lados"),
    ("C02_pessoa", "um cristal desvia um raio"),
    ("C02_paralelas", "como os raios do sol chegam paralelos"),
    ("C02_arcos", "o ângulo entre o sol e o cristal"),
    ("C02_igual", "é o desvio da luz"),
    ("C02_22", "dentro do gelo"),
    ("C03_arco_iris", "lembra do arco-íris"),
    ("C03_gotas", "e a luz voltava de gotas"),
    ("C03_vira", "aqui você olha para o sol"),
    ("C03_halo", "e quem desvia é o gelo"),
    ("C04_frio", "e não precisa de país frio"),
    ("C04_acima", "lá em cima é abaixo de zero"),
    ("C04_globo", "o halo aparece no mundo todo"),
    ("C04_brasil", "até no brasil"),
    ("C05_oposta", "por que justo esse ângulo"),
    ("C05_oposta2", "pela oposta passa reto"),
    ("C05_vizinha", "pela vizinha reflete inteiro"),
    ("C05_alternada", "pela alternada ele sai"),
    ("C05_60", "essas duas faces formam um prisma"),
    ("C06_b1_snell1", "em cada face a luz dobra"),
    ("C06_b1_incidencia", "o seno da incidência"),
    ("C06_b1_refracao", "vezes o seno da refração"),
    ("C06_b2_triangulo", "as normais se cruzam"),
    ("C06_b2_eq", "cento e vinte mais as duas refrações"),
    ("C06_b2_r60", "então as refrações somam sessenta"),
    ("C06_b3_viradas", "em cada face o desvio"),
    ("C06_b4_D1", "a incidência menos a refração"),
    ("C06_b4_soma", "somando as duas faces"),
    ("C06_b4_D2", "o desvio é a soma das incidências"),
    ("C06_b4_D2b", "menos a soma das refrações"),
    ("C06_payoff", "menos sessenta graus"),
    ("C07_grafico", "o que muda o desvio"),
    ("C07_giro", "girando ele cai"),
    ("C07_vale", "um vale só"),
    ("C07_fundo", "no fundo girar mais de vinte graus"),
    ("C07_menos1", "muda menos de um grau"),
    ("C08_ida_volta", "e onde fica o fundo"),
    ("C08_par", "cada ponto tem um par"),
    ("C08_coincide", "girando os dois se encontram"),
    ("C08_simetria", "como o vale é um só"),
    ("C08_snell_1", "ali ida e volta são iguais"),
    ("C08_r30", "trinta graus de refração"),
    ("C08_snell_2", "um vírgula trinta e um"),
    ("C08_snell_3", "a incidência dá"),
    ("C08_snell_4", "uns quarenta e um graus"),
    ("C08_mf4", "o desvio duas vezes isso"),
    ("C08_payoff", "vinte e um vírgula oito"),
    ("C09_pontos", "joga no gráfico orientações"),
    ("C09_empilham", "no fundo achatado elas se empilham"),
    ("C09_nenhum", "nenhum cristal desvia menos"),
    ("C09_lado", "no seu olho os cristais nessa direção"),
    ("C09_muita_luz", "mandam muita luz"),
    ("C09_perto", "mais perto nada"),
    ("C09_longe", "mais longe pouca"),
    ("C09_cone", "ao redor de você isso é um cone"),
    ("C09_anel", "visto de frente é o anel"),
    ("C10_zoom", "e o gelo não tem um índice só"),
    ("C10_vermelho", "o do vermelho é menor"),
    ("C10_21_7", "vinte e um vírgula sete"),
    ("C10_violeta", "o violeta vinte e dois vírgula cinco"),
    ("C10_cores_ceu", "por isso o anel é vermelho"),
    ("C10_azulado", "e violeta por fora"),
    ("C11_sintese", "resumindo"),
    ("C11_duas_faces", "quando a luz atravessa essas duas faces"),
    ("C11_fios", "e como muitos raios saem"),
    ("C11_halo", "aparece o halo"),
    ("C11_cta", "siga o parallax lab"),
]

if __name__ == "__main__":
    out, pos = [], 0
    for nome, frase in F:
        k = acha(frase, pos)
        out.append((nome, round(PAL[k]["start"], 3)))
        pos = k + 1
    assert all(b[1] > a[1] for a, b in zip(out, out[1:])), [(a, b) for a, b in zip(out, out[1:]) if b[1] <= a[1]]
    with wave.open(str(PASTA / "audio" / "narracao_v4.wav")) as w:
        audio_end = w.getnframes() / w.getframerate()
    A = dict(out)
    (PASTA / "ancoras.json").write_text(json.dumps(dict(A=A, order=[n for n, _ in out], audio_end=round(audio_end, 3),
                                                         fim_fala=PAL[-1]["end"]), indent=1), encoding="utf-8")
    print(len(A), "âncoras; fala termina", PAL[-1]["end"], "áudio", round(audio_end, 3))
