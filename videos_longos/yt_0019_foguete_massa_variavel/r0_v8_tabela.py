from pathlib import Path
U = Path(__file__).resolve().parent
T = [
 ("1", "5:13–5:16", "resolvido", "o rótulo original “m + dm (dm < 0)” some no 1º quadro do play em que a cópia parte; as duas ficam visíveis juntas por 2 quadros (≈ 0,13 s, abaixo dos 0,2 s) — seq. de 12 quadros a 15 fps conferida"),
 ("2", "6:21–6:30", "resolvido", "escala de 100 km e inset “NO FOGUETE” subiram 0,3–0,4 u: margem inferior 71 px (medida); a escala (à esquerda) e a moldura do inset (à direita) ficam separadas por ≈ 400 px na horizontal e não se tocam (zoom_02.png)"),
 ("3", "7:16–7:19", "resolvido", "“NADA NA HORIZONTAL” perdeu a seta inicial e foi para 18 pt; termina a ≈ 30 px da setinha do grão (zoom_03.png; pedido ≥ 15 px)"),
 ("4", "8:49–8:53", "resolvido", "“QUEIMA DE 10 MIN” fixo desde o início na posição final, ao lado do Δv; a reta tracejada cresce sem cortá-lo (r0/04_8m51.png)"),
 ("5", "9:29–9:31", "resolvido", "o “×e” só entra depois do arco desenhado (0,9 s depois, em play próprio de 0,3 s) e já vem embaixo dele; 9:30 só mostra o arco"),
 ("6", "10:37–10:43", "resolvido", "F_emp entra já na posição final, 0,18 u mais alto, e “v − v_ex > 0” ficou 1 u mais à esquerda: sem sobreposição em 10:43"),
 ("7", "11:23–11:27", "resolvido", "“mg” fica ao lado da seta de peso (não é mais removido); 11:25 mostra F_emp e mg juntos"),
 ("8", "14:08–14:35", "resolvido", "“FORÇA DO ASSENTO” foi para o canto superior esquerdo do inset, longe da seta azul e da pessoa (zoom_08.png)"),
 ("9 (D1)", "14:50–15:05", "resolvido", "medidor de ORÇAMENTO na metade direita desde a entrada da pergunta: 3 blocos violeta com v_ex = 3,0 km/s e chave Δv ≈ 9 km/s (r0/09_D1_14m55.png)"),
 ("10", "15:43–15:48", "resolvido", "seta e rótulo de v_ex deslocados 0,35 u para a direita, fora das aletas do 1º estágio (zoom_10.png)"),
 ("11", "16:10–16:35", "resolvido", "“R = 4,48” em 34 pt, violeta, com traço preso ao 2º estágio (zoom_11.png)"),
 ("12a", "18:55–19:40", "resolvido", "inset “VISTO DO CHÃO” e barras subiram: margem inferior 61 px (medida na linha clara mais baixa do quadro)"),
 ("12b", "14:45", "resolvido", "DICA “COMPARE EMPUXO E PESO”: margem inferior 76 px"),
 ("12c", "20:10–20:30", "resolvido", "pilha de 3 cartões: margem inferior 61 px (medida); título subiu 0,35 u e o 1º cartão desceu: vão ≈ 26 px até o título (zoom_12c_sintese.png; pedido ≥ 25 px); o cartão 3 foi compactado (gráfico a 68%)"),
 ("D2", "17:40–18:00", "não tentado", "opcional; ampliar a esteira em 20% mexe na geometria da física do E3 (porção acompanhada, grãos) — deixei como está, como o handoff autoriza"),
 ("D3", "5:10", "resolvido", "contorno tracejado do SISTEMA em ciano nos dois painéis do T2; setas e rótulos mantêm as cores das grandezas (r0/D3_5m10.png)"),
]
L = ["# R0 v8 — 12 itens do handoff v8 §2 (+ D1 e D3; D2 não tentado). Antes (v7) × depois (v8) no mesmo instante. Só resolvido / não resolvido.", "",
     "| # | tempo | status | o que se vê na prancha |", "|---|---|---|---|"]
for n, t, s, o in T:
    L.append(f"| {n} | {t} | {s} | {o} |")
L += ["", "itens obrigatórios resolvidos: 14 de 14 (1–11, 12a, 12b, 12c) · opcionais: D1 e D3 resolvidos, D2 não tentado"]
(U / "renders" / "v8" / "r0_tabela.md").write_text("\n".join(L), encoding="utf-8")
print(L[-1])
