# vid_0025 — relatório da rodada r5 (referencial dos 42°, caixa alta, arte nova, sem sobreposição)

Data: 25/10/2026. Preview silencioso. Sem voz, SRT, master, capa, publicação, commit ou push.

## Preview r5

- `media/videos/cena/960p15/ArcoIris025.mp4` (cópia em `renders/preview_r5_ArcoIris025.mp4`), 540×960, 15 fps, sem áudio, **173,93 s (2:53,93)**, 2.609 quadros. Limite pedido: máx. 2:59. Render limpo (`--disable_caching`, partial_movie_files apagados).
- Marcas (s): C01 0 · C02 14,4 · C03 20,5 · C04 29,5 · C05 42,7 · C06 66,6 · C07 80,9 · C08 94,8 · C09 129,1 · C10 140,5 · C11 167,3 · fim 173,9.
- Pranchas: `renders/preview_r5_prancha_01..09.png`; zip para o GPT: `renders/preview_r5_para_gpt.zip` (todos os quadros + MP4 + cena.py; temporário).

## O que mudou

- **Referencial dos 42° (pedido principal).** C01 agora constrói a referência antes do ângulo: Sol → raio pela cabeça → sombra da cabeça; a linha inteira é a *direção antissolar*, em destaque, com legenda "A REFERÊNCIA: A DIREÇÃO ANTISSOLAR / DO SOL, PELA SUA CABEÇA, ATÉ A SUA SOMBRA". Depois a gota de chuva, a luz da gota ao olho, o arco de 42° entre a direção antissolar e a linha de visão e a legenda "OS 42° SÃO MEDIDOS A PARTIR DA DIREÇÃO ANTISSOLAR / NÃO DO CHÃO, NÃO DO HORIZONTE". Abertura medida pelos vetores do desenho = 42,078107° (asserção no código).
- **C10 refeito para explicar o semicírculo.** Vista lateral com eixo antissolar e ponto antissolar rotulados → uma geratriz percorre o cone ("TODA GOTA A 42° DO EIXO ENVIA LUZ PARA O SEU OLHO") → giro para a vista ao longo do eixo → círculo de todas as direções a 42° do ponto antissolar (centro = sombra da cabeça, raios de 42°) → o horizonte corta o círculo → indicador separado da altura do Sol → Sol no horizonte = semicírculo exato ("CADA PESSOA TEM O SEU CENTRO: A PRÓPRIA SOMBRA") → Sol sobe: o centro desce e o arco encolhe → acima de 42°, arco abaixo do horizonte (estado final a 45°, topo = −3°).
- **Arte nova:** pessoa de perfil (cabeça, nariz, camisa, braços, pernas, olhando para a direita), Sol com brilho e raios, gotas de chuva em formato de lágrima, chão em degradê, brilho nas linhas-chave, painéis azuis (PANEL/BLUE_L) nas equações de destaque.
- **Tipografia e cores (padrão dos longos):** todo texto fora do MathTex em Space Grotesk MAIÚSCULO (helper `words` com caixa alta; símbolos e variáveis sempre em MathTex, inclusive em linhas mistas via `mix`); geometria (b, R, normais, referências) em cinza `GEO`; azul-claro nos lados R; paleta de ângulos do briefing mantida (i violeta, r magenta, θ ciano). Exceção deliberada: o handle `@labparallax` fica em minúsculas.
- **Auditor de sobreposição no código:** a cada pausa de leitura (`wait`) a cena confere texto×texto, texto×traço (inclusive tracejados), limites do quadro e a faixa inferior reservada (y < −5,65). Resultado do render final: **zero avisos**. Trocas de legenda/nota passaram a ser saída-depois-entrada (nunca dois textos juntos); círculo inferior da vista de frente recortado acima da área das legendas.
- **Ritmo:** fator de andamento por cena (`SCENE_PACE`), álgebra de C05/C08 mantida mais lenta; nenhum passo removido.

## Verificação

- `py_compile`: OK. Render limpo: exit 0. Física inalterada (helpers e QA numérico do r3/r4 valem); abertura do gancho = θmáx por asserção; direção de saída da gota após o zoom = direção da gota ao olho (desvio 0,0000°).
- Quadros inspecionados em 540×960 (pranchas e quadros-chave de todas as cenas). Pontos conferidos: gancho com referência explícita, sem texto fora do quadro, legendas fora da faixa reservada, vermelho fora/violeta dentro (C09, C10, C11), indicador solar separado, cinco saídas e contagem em C07.

## Pendências reais

- A duração-alvo de 180–190 s do handoff foi substituída pelo teto de 2:59 pedido pelo usuário; a narração congelada (~180–190 s) terá de caber em 2:59 na fase de voz.
- O auditor mede caixas de texto e amostras de traços; não detecta sobreposição entre desenho e desenho (por exemplo, gotas de chuva sobre linhas), conferida apenas visualmente.
- C07 (~86 s): a cunha do detalhe angular ×10 continua estreita a 360×640; se precisar, ampliar para ×20 declarado.
- O handle `@labparallax` em minúsculas é exceção ao "tudo maiúsculo"; trocar se for decisão da marca.

Teste do arsenal: não se aplica (solido_3d: nenhum).
