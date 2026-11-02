from pathlib import Path
U = Path(__file__).resolve().parent
NAO = {
 3: "1:34 é a emenda PH→PT1 (0,4 s de céu entre lotes, por regra G39); amostra cai nela",
 15: "−dm ainda a 0,2 u da borda tracejada",
 18: "balanço mantém a linha antiga com buracos durante o fechamento",
 19: "linha seguinte ainda entra esmaecida em 5:48 (fade além de 0,35 s)",
 21: "6:48 ainda cena escura com só a caixa (troca T2-6→T2-7)",
 23: "bloco esquerdo do T2-7 continua denso",
 38: "11:50 continua quase vazio (janela de troca T4-2→T4-3)",
 40: "rótulos de perda do T4-3 ainda apertados junto à linha vermelha",
 43: "número em voo (2.500 → 2.500·120) ainda vira borrão em 12:57",
 47: "FORÇA DO ASSENTO fica a ~0,1 u da seta e do joelho",
 50: "HIPÓTESES do E2 ainda com tamanhos mistos (9 km/s em fonte numérica)",
 55: "coluna direita do E2-4 ainda com 2 linhas por ~15 s",
 68: "chip VISTO DO CHÃO não foi alterado (sem evidência do defeito original)",
 70: "20:46 vazio (EN2, marca d'água ao fundo)",
}
OK = {
 1: "traços ciano sob os patinadores sumiram", 2: "P CONSTANTE a 100% em t + 0,67 s (extra_fades.png)", 4: "TENTAÇÃO? a 100% em t + 0,33 s (extra_fades.png)",
 5: "SE A CONTA VALESSE e dm/dt a 100% em t + 0,67 s (extra_fades.png)", 6: "seta v do fantasma fora da caçamba, à frente", 7: "TRILHO SEM ATRITO abaixo do piso",
 8: "Pilha com o NÃO fica até o T1-4", 9: "contorno único em L, seta v acima dele", 10: "pergunta do T2 entra com o foguete", 11: "3:33 a 100% em t + 0,67 s (extra_fades.png)",
 12: "u_rel embaixo de cada objeto", 13: "painel t + dt entra vazio com o painel t", 14: "HIPÓTESES numa linha",
 16: "linhas de velocidade afastadas (Y1/Y2 = −1,20/−1,66; painel desceu 0,08 u)", 17: "o 'm+dm' duplicado é a cópia que parte (3 quadros em 11:24–11:24,5); não há duplicata parada",
 20: "unidades em uma linha (m/s·kg/s = kg·m/s² = N) fora da margem", 22: "nenhuma seta de areia abaixo do trilho",
 24: "NADA NA HORIZONTAL em duas linhas, à esquerda da queda do grão (a seta v do grão fica livre)",
 25: "dv dos dois insets voa para a vaga do ∫ e há a linha do sinal (−ln m_f/m_0 = ln m_0/m_f) antes de Δv (extra_tsiolkovsky.png)", 26: "sopa de glifos de 8:03 removida: a integral entra por fade em 0,35 s",
 27: "Δv/v_ex a 100% em t + 0,67 s (extra_fades.png)", 28: "8:45 tem eixos + linha-alvo tracejada + Δv = v_ex ln R", 29: "8:46 idem",
 30: "'10 min' acima e à esquerda da ponta, fora da curva", 31: "9:06 tem a fórmula Δv/v_ex = ln R no canto livre", 32: "e² ≈ 7,4 a 100%", 33: "ORÇAMENTO a 100% e colorido",
 34: "título do inset inteiro dentro da janela (VISTO DE FORA (O FOGUETE PARTIU DO REPOUSO))", 35: "F_emp à direita e mg à esquerda, fora do casco", 36: "sem HIPÓTESES esmaecido no quadro",
 37: "o 'mg' duplicado é a cópia que parte (3 quadros em 11:24–11:24,5); não há duplicata parada",
 39: "240 kg/s e 120 kg/s afastados na origem (−0,28 e −0,62 u)", 41: "EM RELAÇÃO AO FOGUETE começa à direita da seta v_ex, sem cruzar a perna da torre nem a seta",
 42: "pergunta na coluna direita", 44: "setas fora do foguete", 45: "m₀g separado de PROPELENTE", 46: "linhas a 100%", 48: "CONFERE em uma linha",
 49: "ESTRUTURA 0,1 f a 0,85 u da aleta", 51: "P→0 riscado, sai e a linha fecha", 52: "Δv e 7,2 km/s < 9 km/s em violeta saturado",
 53: "quatro rótulos de estágio na mesma margem esquerda", 54: "1º estágio sólido e esmaecido (40%) depois da separação, sem tracejado",
 56: "m₀₂ a 100% em t + 0,67 s (extra_fades.png)", 57: "barra entra junto com os rótulos", 58: "NESTE MODELO virou cabeçalho do bloco 1 t DE CARGA → 47 t NA RAMPA",
 59: "5% O RESTO à esquerda da barra, longe da observação", 60: "pergunta do E3 entra junto com a esteira", 61: "HIPÓTESES do E3 em um só estilo (sem v itálico)",
 62: "grãos somem atrás do rolete", 63: "SISTEMA à direita da coluna", 64: "30 kg·m/s a 100%", 65: "contorno maior; setas dentro e abaixo da lona",
 66: "18:33 sem sopa numérica", 67: "barras 0,35 u mais altas (yb = −3,60)", 69: "título afastado da marca d'água",
}
L = ["# R0 v6 — 70 itens (v5 × v6, olhado nas folhas renders/v6/r0_folha_N.png). Só resolvido / não resolvido.", "", "| # | status | o que se vê |", "|---|---|---|"]
for n in range(1, 71):
    if n in NAO:
        L.append(f"| {n} | não resolvido | {NAO[n]} |")
    else:
        L.append(f"| {n} | resolvido | {OK[n]} |")
L += ["", f"resolvidos: {70 - len(NAO)} · não resolvidos: {len(NAO)}"]
(U / "renders" / "v6" / "r0_tabela.md").write_text("\n".join(L), encoding="utf-8")
print(L[-1])
