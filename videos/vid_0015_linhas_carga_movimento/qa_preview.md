# QA — vid_0015, compressão de ritmo V4

Rodada de 2026-10-06. V4 implementada sobre a V3, mantendo direção visual,
física, tipografia, recursos e MF-Tools. Escopo encerrado no preview silencioso.

V3: **348,40 s** (5min48,4s).
V4: **173,06 s** (2min53,1s).
Economia no MP4: **175,34 s**.
Alvo 170–175 s atendido; abaixo do máximo absoluto de 180 s.

## Economia por bloco

| Bloco | V3 (s) | V4 (s) | Economia (s) |
| --- | ---: | ---: | ---: |
| Enunciado e conflito | 14,40 | 11,40 | 3,00 |
| Gauss | 53,13 | 30,73 | 22,40 |
| Força elétrica | 24,07 | 9,93 | 14,13 |
| Superfície → curva | 13,67 | 5,87 | 7,80 |
| Ampère | 34,67 | 17,67 | 17,00 |
| Mão direita e força magnética | 38,47 | 19,80 | 18,67 |
| Igualdade → primeiro payoff | 34,00 | 18,20 | 15,80 |
| Corrente → v=c | 53,40 | 17,27 | 36,13 |
| Derivação da razão | 34,67 | 11,87 | 22,80 |
| Gráfico sincronizado | 28,67 | 22,20 | 6,47 |
| Conclusão | 19,27 | 8,13 | 11,13 |

Os blocos usam os tempos medidos no render completo, registrados em
`comparacao_ritmo_v4.json`, sem codificação posterior para acelerar o vídeo.
A soma da cena é 173,07 s; o MP4 tem diferença inferior
à duração de um quadro por arredondamento de PTS na concatenação.

## Waits e montagem

Todos os waits foram auditados: uma chamada localizada no helper checkpoint,
com tempos explícitos ou política local por estado. Soma de waits:
**184,8 s → 38,0 s**, economia de **146,8 s**. Nenhum wait acima de 1,8 s.
Os dois payoffs mantêm pausa de 1,8 s cada. Passos algébricos rápidos usam 0,2 s
entre transformações; resultados/geometrias recebem respiro conforme necessidade.
TransformMatchingTex fica entre 0,6 e 1,2 s; MF-Tools entre 0,8 e 1,5 s,
quantizados em quadros de 15 fps. Os tempos definitivos de voz permanecem fora
 desta rodada.

Fundidos:

- Campo radial, lateral, vetor área e relação E paralelo a dA.
- Duas tampas simultâneas, duas perpendicularidades e dois fluxos zero individuais.
- Remoção da superfície e mudança E·dA → B·dℓ na mesma transição; seção preservada.
- Cadeias algébricas como evolução da expressão corrente na região matemática.
- Retorno ao movimento: mudar I para v, destacar cargas e frase aprovada juntos.
- Recuperar primeiro payoff e indicar o lado esquerdo coincidente juntos.
- Gráfico: três rampas contínuas, 0 → 0,6 → 0,95 → 0,995. Pausas de 0,4 s em
  0,6 e 1,0 s em 0,995; nenhuma pausa em 0,95. Deslocamento simultâneo das linhas.
- Último título e saída das setas individuais F_E/F_B e da condição já apresentada.
  O último frame mantém a resultante repulsiva, a razão <1 e F_B<F_E.

A primeira medição ficou em 143,1 s. O ajuste devolveu tempo às geometrias e à
comparação das forças, mantendo os payoffs. Foi retirado o título redundante
antes da derivação da razão. Reduzidas as permanências dos textos auxiliares;
nenhum conteúdo físico ou passo matemático obrigatório foi removido.

## Preservação matemática e física

Auditoria compara os argumentos LaTeX da cena V3 preservada com a V4: nenhuma
expressão removida. Os **41 passos matemáticos registrados na V3** continuam
presentes na V4. Cadeias completas de Gauss, força elétrica, Ampère, força
magnética, igualdade dos módulos, origem da corrente e razão das forças.

Conferidos: campo E radial; dA lateral paralelo ao campo; em cada tampa E
perpendicular ao vetor área axial e fluxo zero individual. Gauss usa superfície;
Ampère usa curva, tangência e circulação. Cilindro não comprimido; seção persiste.
Q_enc=λℓ, A_lat=2πdℓ, E(d), q=λℓ e F_E/ℓ permanecem. Ampère inclui a lei,
I_enc=I, retirada de B da integral, comprimento 2πd, B(2πd)=μ₀I e B(d).

Corrente +x na linha superior; B=−z na inferior, com ⊗ separado e guia neutra.
+x×(−z)=+y: F_B para cima, F_E para baixo; campo da linha 1 atua na linha 2,
sem força por campo próprio. Produto vetorial, seno de 90°, módulo, substituição
de B e F_B/ℓ mantidos. Igualdade dos módulos, cancelamento explícito de 2πd,
λ²=μ₀ε₀I², reorganização, raiz/módulos e definição de c mantidos.

|I|/|λ|=c precede |I|=|λ|v. Retorno aprovado preservado literalmente. O trecho
vΔt atravessa P fixo; Δq, definição de I, substituição, cancelamento de Δt,
I=λv, módulos e recuperação do primeiro payoff continuam visíveis. v=c somente
após retornar ao movimento. A razão parte da divisão completa das forças,
cancela fatores, recupera I/λ, eleva ao quadrado e usa μ₀ε₀=1/c² antes do gráfico.

Modelo ideal explícito durante a exploração; β≤0,995. Um tracker controla ponto,
curva, F_B, resultante, readouts e movimento qualitativo; F_E é constante.
F_B nunca ultrapassa F_E. Conclusão progressiva após saída do gráfico:
v<c → razão<1 → F_B<F_E → REPULSÃO LÍQUIDA. No último estado só a seta
resultante permanece, evitando três forças competindo com o payoff.

Tipografia oficial preservada: Space Grotesk Medium pelo helper do template;
MathTex para matemática, DecimalNumber para números. Auditoria confirma fonte,
34 expressões GlyphEq e 24 transformações MF-Tools. Sem índices/debug.

## Validação e inspeção

```powershell
uv run --no-sync python -m py_compile videos/vid_0015_linhas_carga_movimento/cena.py videos/vid_0015_linhas_carga_movimento/auditar_ritmo.py videos/vid_0015_linhas_carga_movimento/auditar_cena.py videos/vid_0015_linhas_carga_movimento/inspecionar_preview.py
uv run --no-sync python videos/vid_0015_linhas_carga_movimento/auditar_ritmo.py
uv run --no-sync python videos/vid_0015_linhas_carga_movimento/auditar_cena.py
uv run --no-sync python -m manim -r 540,960 --fps 15 --media_dir videos/vid_0015_linhas_carga_movimento/media -o vid_0015_preview_v4_silencioso videos/vid_0015_linhas_carga_movimento/cena.py LinhasCarga015
uv run --no-sync python videos/vid_0015_linhas_carga_movimento/inspecionar_preview.py
uv run --no-sync python videos/vid_0015_linhas_carga_movimento/auditar_ritmo.py --renderizado
```

Todos encerrados com código 0 na implementação entregue. Resultado H.264,
540×960, 15 fps nominal, **2596 quadros decodificados**,
nenhum stream de áudio. Decoder verifica duração, resolução, todos os quadros,
intervalos compatíveis com 15 fps, limite de 180 s e pausas dos payoffs.

Inspecionados **77 estados e 30 quadros intermediários** extraídos do MP4,
incluindo estados fundidos, todas as cadeias matemáticas, 24 mapas de glifos,
seção, enrolamento, trecho que passa por P, gráfico contínuo e conclusão.
Geometria das tampas e cancelamento foram também conferidos em PNG 540×960.
O último estado simplificado foi novamente conferido após a atualização.
Sem sobreposição ou perda de conteúdo identificada nos pontos inspecionados.

## Arquivos e entrega

Alterados somente na unidade: `cena.py`, `ficha.md`, `inspecionar_preview.py`,
`auditar_cena.py` e `qa_preview.md`. Criado `auditar_ritmo.py` para a medição local.
Preservados V3, MP4, frames, dados técnicos e cópias `cena_v3.py`,
`inspecionar_preview_v3.py`, `auditar_cena_v3.py` e `qa_preview_v3.md`.

Preview: `media/videos/cena/960p15/vid_0015_preview_v4_silencioso.mp4`.
Dados: `qa_estados_v4.json`, `qa_tecnico_v4.json`, `comparacao_ritmo_v4.json`,
`auditoria_v4.json` e logs locais. Imagens: `frames_preview_v4/` e
`frames_producao_v4/`. Pacote `vid_0015_v4_frames_producao.zip` com exatamente
**18 JPGs**, seis frames por imagem, mantendo 540×960 por célula. São 107 frames,
abaixo do limite de 20 anexos da Produção.

Limite preservado: deslocamento qualitativo, sem integração de dinâmica,
massa, aceleração ou tempo físico. Não foi encontrada inconsistência física
objetiva nem pendência técnica nos pontos inspecionados. Nenhum global ou arquivo
de outra unidade foi alterado; alterações preexistentes preservadas. Sem voz,
SRT, master, legenda, capa, render final, branch, commit ou push.
