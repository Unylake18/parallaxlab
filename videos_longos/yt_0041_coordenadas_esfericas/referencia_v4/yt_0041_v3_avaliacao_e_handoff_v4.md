# HANDOFF v4 (correções finas) · yt_0041 · CÁLCULO III · EP. 16 · Coordenadas esféricas

Data: 2026-11-16. Fase: **preview v4** (540p15, silencioso). Sem voz, SRT, 1080p, entrega ou commit.
Base: preview v3 (`yt_0041_preview_v3_540p15.mp4`, 22:12,87 = narração v1.4) e o handoff v3 (`yt_0041_v2_avaliacao_e_handoff_v3.md`), que continua valendo em tudo o que este documento não muda.

## 0. Veredito do v3

O v3 melhorou muito e a estrutura está certa: octante, papel e piso sob o 3D, 3D só na metade esquerda, legenda no lugar das hastes, duas vistas do endereço, receita sólida, cortes 2D, menores do B2-3, duração igual à narração v1.4, flash 0 e alinhamento 3D 0,014 px.

**Ainda não está pronto para a narração**, por 12 defeitos pontuais que o QA do v3 não pegou (linhas órfãs, 3D escondido atrás de painel, 3D cortado na borda, texto pequeno). Todos têm tempo e critério de aceite abaixo. É uma rodada curta: só os blocos listados voltam ao render.

## 1. Defeitos do v3 (tempo no preview v3 → o que fazer → aceite)

| # | Tempo | Bloco | Defeito | O que fazer | Aceite |
|---|---|---|---|---|---|
| D1 | 4:30–5:20 | B1-3 | A linha `y = 1·sen π/3 = √3/2`, sobra do bloco anterior, fica **em cima da bola** e entre as colunas, sem pertencer à cena | Apagar toda a coluna do ponto de exemplo (as 6 linhas) ao sair do B1-2/ponto; a cena B1-3 só mostra o que é dela | Zero texto do bloco anterior em B1-3; nenhuma fórmula sobre o 3D |
| D2 | 9:40–9:50 | B2-3 | O rótulo `LINHA DE BAIXO: + − +` fica sozinho sem o determinante (o determinante já virou chips) | O rótulo sai junto com o determinante | Zero rótulo sem seu objeto |
| D3 | 18:30 até 20:20 | B6-1/B6-2 | A casquinha 3D encolhe, é **cortada na borda esquerda** e depois fica **atrás do painel do corte** (de 18:40 em diante só aparece uma sobra azul na borda) | Casquinha 3D inteira à esquerda **acima** do painel (como no alvo 13a: 3D até y ≈ 540, painel abaixo, ou painel de x = 430 a 970 e 3D de x = 0 a 400 sem encostar), com o piso. Nunca painel sobre 3D | A casquinha inteira visível o tempo todo, nenhum pixel do 3D sob o painel |
| D4 | 5:30–6:50 | B2-1 | A caixinha curva é cortada na borda esquerda (eixo e arco saem do quadro) e os rótulos `r Δφ` e `r sen φ Δθ` são placas **em cima das arestas** | Reenquadrar para a caixinha e o eixo ficarem inteiros dentro de x = 60..975; os rótulos viram legenda colorida abaixo do 3D (G4), com no máximo 2 hastes ≤ 90 px | Nada do 3D fora de x = 60..975; nenhuma placa sobre aresta |
| D5 | 20:20–21:00 e 21:20–22:12 | S2 | O CTA "INSCREVA-SE" fica sobre o fim do S2 (3 sobreposições do QA) | CTA só depois do S2 terminar, em tela lisa, ou o S2 sobe até o CTA entrar | R5 = 0 no S2 |
| D6 | 8:10–9:20 | B2-3 | O determinante e os menores usam ≈ 33 px a 1080p e a metade de baixo da tela fica vazia | Subir para KaTeX 44–50 (a coluna cabe: sobra mais de 500 px de altura) | Altura do x ≥ 34 px a 1080p; nenhuma fórmula < 44 px de corpo |
| D7 | 18:40–20:20 | B6-2 | A integral e a escada da substituição estão ≈ 26 px a 1080p | Subir para 44; as linhas da escada podem passar a 2 colunas ou ocupar a largura inteira, já que o 3D e o painel ficam só à esquerda | Nenhum texto < 26 px; ladder em 44 |
| D8 | 7:00–8:00 | B2-2 | Painéis 2D e conta com texto ≈ 28 px e a metade direita vazia até o 2º painel entrar (B3-1 não foi conferido em detalhe: aplicar a mesma regra) | Aplicar a regra de tamanho do handoff v2 §2 (50–54 principal, 44 secundária, 30 legenda) | Idem D6 |
| D9 | 1:00–1:30 | H2 | A grade nova: o painel "A GRADE NOVA" tem o interior vazio durante 20 s e as legendas dos pedaços saem do 3D | Painel só aparece com a primeira linha (CASCAS); legenda ao lado do pedaço, no papel | Zero painel vazio |
| D10 | 2:20–2:40 e 3:00–3:10 | B1-1 | A linha `y = s sen θ = r sen φ sen θ` aparece com um trecho minúsculo/sobreposto (`r sen φ`) na escrita | A caneta escreve a linha toda na altura da linha, sem glifo menor | Linha inteira legível a cada quadro |
| D11 | 18:00–18:20 | B6-1 | `r² = 2r cos φ ⇒ r = 2 cos φ` com sobreposição do glifo em voo no meio da linha | O voo parte da origem sem cruzar a linha já escrita | R5V = 0 nessa linha |
| D12 | vídeo todo | — | Atrasos de gatilho: B6-1 +3,1 s ("embaixo o cone"), B6-2 +1,5 s, H2 +1,5 s, B2-3 +1,1 s, B7 +1,0 s | Reposicionar o início do degrau para ≤ 0,3 s da frase. Se não couber, **não comprimir a escrita**: relatar a âncora e os segundos que faltam | `chk_gat.py` com atraso ≤ 0,3 s ou escada listada |

## 2. Itens aceitos como estão
- Rótulos de r, φ e θ em placa pequena no B1-3 e na caixinha, **desde que** fora das arestas (D4).
- B1-2 sem as duas vistas (a coluna cheia é melhor ali); as duas vistas ficam no B1-1.
- Menores do B2-3 (linhas 2 e 3 sem glyph map): aceitos.

## 3. QA do v4 (relatório)
1. **Linha órfã:** varredura a cada 0,5 s de todo texto/fórmula visível sem o objeto de origem; zero.
2. **3D escondido/cortado:** para cada cena 3D, pixels do 3D fora de x = 60..975 e sob painéis; zero.
3. **Tamanho:** altura do x por bloco (tabela); nenhum texto < 26 px; fórmula principal ≥ 44 px de corpo.
4. **R5 / R5V / margens:** zero R5 e zero R6 (as 4 margens do B1-1 → B1-2 também).
5. **Gatilhos:** tabela com cada degrau × frase (D12).
6. **Comparação com os alvos v3/v2:** prancha lado a lado (7 alvos v3 + 07, 08a, 08b, 13b do v2). A `comparacao_v3.jpg` usou os alvos v1.1 e não vale como prova.
7. **G1–G6 por cena 3D** e **prancha 3D 2×3**, como no handoff v3 §5.
8. Sem pulso, brilho, palco vivo, tracer ou efeito novo.

## 4. Não mexer
Tudo o que o v3 acertou (§0), a matemática, as cores, a notação, a caneta, a ordem dos blocos, o kit de QA, a duração 22:12 e documentos globais.

## 5. Entrega
Preview 540p15 silencioso, relatório do §3 e prancha de comparação. Pare, sem voz, sem 1080p e sem entrega.
