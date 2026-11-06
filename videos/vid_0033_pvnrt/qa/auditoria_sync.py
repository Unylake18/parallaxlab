"""Auditoria de sincronia do vid_0033: cada evento visual × a palavra da voz que o dispara (alinhamento_palavras.json).
Atraso = início real da animação (qa_trans.json, tempo de vídeo) − início da palavra. Limite: 0 ≤ atraso ≤ 0,2 s (tolerância de 1 quadro = 0,067 s para antes).
Uso (a partir da pasta do vid): uv run python qa/auditoria_sync.py"""
import json
import re
from pathlib import Path

U = Path(__file__).resolve().parents[1]
P = json.loads((U / 'alinhamento_palavras.json').read_text(encoding='utf-8'))
TR = sorted(json.loads((U / __import__('os').environ.get('MIDIA', 'media_preview') / 'qa_trans.json').read_text(encoding='utf-8')))
norm = lambda x: re.sub(r'[^\wáéíóúâêôãõàçü]', '', x.lower())
W = [norm(p['word']) for p in P]


def palavra(frase, apos=0):
    seq = [norm(x) for x in frase.split()]
    for i in range(apos, len(W) - len(seq) + 1):
        if W[i:i + len(seq)] == seq:
            return i
    raise KeyError(frase)


# (evento, frase falada que o dispara, tempo (s) em que o cena.py o dispara)
EV = [
    ('C01 selos + fórmula', 'pressão vezes volume igual', .1), ('C01 "de onde vem isso?"', 'de onde vem isso', 6.1),
    ('C01 chip "só com moléculas…"', 'acompanhando moléculas', 7.9),
    ('C02 p = mv', 'o momento dela', 15.33), ('C02 rótulo massa', 'massa vezes velocidade', 16.27), ('C02 rótulo velocidade', 'velocidade', 17.0),
    ('C02 pᵢ = mvₓ', 'na batida', 17.92), ('C02 pᵢ, p_f', 'passa de positivo', 22.5), ('C02 Δp = p_f − pᵢ', 'final menos inicial', 24.66),
    ('C02 −mvₓ − mvₓ', 'inicial', 25.3), ('C02 −2mvₓ', 'duas vezes massa', 26.62), ('C02 setas de impulso', 'o oposto', 29.9),
    ('C02 J = +2mvₓ', 'o impulso mais duas', 30.6),
    ('C03 seta L', 'duas vezes o lado', 37.1), ('C03 rótulo lado', 'lado da caixa', 37.92), ('C03 Δt = (L+L)/vₓ', 'o intervalo entre', 38.78),
    ('C03 Δt = 2L/vₓ', 'dividida pela velocidade', 41.2), ('C03 fixa J, Δt', 'a força média', 42.75), ('C03 F̄ = J/Δt', 'o impulso dividido', 43.78),
    ('C03 F̄ = 2mvₓ/(2L/vₓ)', 'dividido pelo intervalo', 44.45), ('C03 o 2 cancela', 'o dois cancela', 45.74), ('C03 F̄ = mvₓ²/L', 'sobra massa vezes', 46.9),
    ('C03 P₁ = F̄/A', 'e pressão é força', 50.55), ('C03 rótulo área', 'área', 51.88), ('C03 P₁ = (…)/L²', 'ao quadrado a', 53.3),
    ('C03 P₁ = …/L³', 'lado ao cubo', 54.85), ('C03 rótulo volume', 'o volume', 55.66), ('C03 P₁ = …/V', 'volume pressão de', 55.93), ('C03 P₁V = mvₓ²', 'pelo volume', 60.4),
    ('C04 rótulo molécula i', 'todas as moléculas', 61.65), ('C04 Σ', 'pressão vezes volume é a massa', 62.82), ('C04 m Σ', 'a massa vezes a soma', 64.35),
    ('C04 N m ⟨vₓ²⟩', 'o número de moléculas vezes', 67.55), ('C04 definição da média', 'a média desses', 69.1), ('C04 diagrama', 'e o um terço', 70.5),
    ('C04 vetor v', 'vem de pitágoras', 71.5), ('C04 componentes', 'no espaço', 72.3), ('C04 vᵢ² = soma', 'o quadrado da velocidade', 73.05),
    ('C04 ⟨v²⟩ = soma', 'e na média', 77.0), ('C04 três moléculas', 'uma molécula sozinha', 78.0), ('C04 barras (n)', 'mas num gás', 81.25),
    ('C04 médias iguais', 'as três médias são', 84.48), ('C04 ⟨v²⟩ = 3⟨vₓ²⟩', 'como as três somam', 86.08), ('C04 barra empilhada ⅓', 'cada uma é um', 88.95),
    ('C04 ⟨vₓ²⟩ = ⟨v²⟩/3', 'uma é um terço', 89.5), ('C04 PV = N m ⟨vₓ²⟩', 'pressão vezes volume é um', 91.2), ('C04 substituição', 'é um terço do', 92.7),
    ('C04 PV = ⅓ N m ⟨v²⟩', 'vezes a média do quadrado', 95.5),
    ('C05 ⟨E_c⟩ = ½ m⟨v²⟩', 'metade da massa', 98.84), ('C05 m⟨v²⟩ = 2⟨E_c⟩', 'é a energia cinética', 101.45), ('C05 PV = ⅓N·2⟨E_c⟩', 'então pressão vezes volume', 102.72),
    ('C05 PV = ⅔N⟨E_c⟩', 'é dois terços', 104.5), ('C05 gráfico', 'termômetro de gás', 112.45), ('C05 ponto 273,15 K', 'em qualquer temperatura', 113.74),
    ('C05 ponto 373,15 K', 'temperatura pressão vezes', 114.2), ('C05 reta', 'pressão vezes volume dividido', 114.9), ('C05 tabela', 'dividido pelo número de moléculas', 116.2),
    ('C05 PV/(NT) = const.', 'dá a mesma constante', 119.45), ('C05 k_B', 'de boltzmann', 120.95), ('C05 PV = N k_B T', 'logo pressão vezes', 121.6),
    ('C05 contorno PV = N k_B T', 'temperatura', 126.85), ('C05 ⅔N⟨E_c⟩ = N k_B T', 'as duas expressões', 128.4), ('C05 ⟨E_c⟩ = 3/2 k_B T', 'a energia cinética média vale', 129.45),
    ('C06 N = nN_A', 'o número de moléculas é', 135.65), ('C06 PV = nN_A k_B T', 'avogadro e a constante', 138.2), ('C06 R ≡ N_A k_B', 'constante dos gases é', 139.15),
    ('C06 6,022·10²³ × 1,38·10⁻²³', 'boltzmann substituindo', 141.5), ('C06 PV = nRT', 'pressão vezes volume igual a número', 143.65),
    ('C07 contadores 34 → 67', 'contador registra', 152.2), ('C07 ×2', 'o dobro de batidas', 153.55),
    ('C07 temperatura constante', 'com a temperatura constante', 155.3), ('C07 PV = const. ⇒ …', 'isso é o dobro', 156.75), ('C07 nitrogênio', 'no nitrogênio', 161.35),
    ('C07 velocidade quadrática média', 'a velocidade quadrática', 163.4), ('C07 517 m/s', 'quinhentos e dezessete', 165.35),
]
linhas, pos, ruins = [], 0, 0
for nome, frase, t in EV:
    try:
        i = palavra(frase, max(0, pos - 6))
    except KeyError:
        i = palavra(frase)
    pos = i
    t_w = P[i]['start']
    real = min(TR, key=lambda x: abs(x - t))
    atraso = real - t_w
    ok = -.067 <= atraso <= .2 and abs(real - t) < .13
    ruins += not ok
    linhas.append(f'{nome:34s} palavra "{P[i]["word"]}" @ {t_w:7.2f}  evento @ {real:7.2f}  atraso {atraso:+.2f}  {"OK" if ok else "FORA"}')
linhas.append(f'{len(EV)} eventos; fora do limite (−0,067 … +0,2 s): {ruins}')
(U / 'qa' / 'auditoria_sync.txt').write_text('\n'.join(linhas), encoding='utf-8')
print('\n'.join(linhas))
