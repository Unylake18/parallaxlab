# liquido_rotacao — refinamento visual, rodada 2

Asset mantido como **estudo**, para avaliação humana. Fórmula, raio, nível, desnível e altura do recipiente da ficha preservados: R=1,2; h0=1,35; Δh=1; H=2,6. Sem integração ao vid_0022.

## Arquivos desta rodada

Todos os caminhos abaixo são relativos a `experimentos/blender/arsenal/`:

- `liquido_rotacao.py`: refinamento da implementação existente; materiais, tracers, fades editoriais e roteiros de animação.
- `solidos/liquido_rotacao.json`: ficha alinhada aos controles atuais, modos visuais, parâmetros e limitações. Status continua `estudo`.
- `construtores.py`: somente o adaptador de `liquido_rotacao`, corrigido para a assinatura atual e argumentos nomeados.
- `verificar_liquido_rotacao.py`: verificações da malha fechada, normais, controles independentes, modos, morph e compatibilidade da ficha.
- `preview_liquido_rotacao.py`: novo gerador dedicado dos stills e sequências curtas.
- `montar_previews_liquido_rotacao.py`: novo empacotador local de MP4 e folhas comparativas usando as dependências existentes.
- `previews/liquido_rotacao_rodada2/`: previews, sequências PNG, estados por quadro, logs, resumo e este relatório.

As alterações preexistentes em `catalogo.md`, `abrir/LEIA-ME.md`, o atalho `abrir/liquido_rotacao.bat` e o preview antigo `previews/liquido_rotacao.png` foram preservados. Nenhum documento global foi atualizado nesta rodada.

## Visual e geometria

- Corpo do líquido fechado, com topo paraboloidal, lateral e fundo; material azul diferente do recipiente. A camada interna existente mantém a leitura da parede posterior e do fundo através da transparência.
- Recipiente e aro superior mais discretos. Fundo do líquido continua fechado, com material e contorno atenuados.
- Interface branca fina: raio de traço 0,005; emissão 0,35. Não há segundo recipiente modelado na interface.
- `fenomeno`: líquido e tracers; sem grade, seção ou referência por padrão.
- `geometria`: grade discreta e uma seção meridiana branca, sem tracers por padrão. Seção com azimute configurável em `fi_meridiana`.
- `qa`: grade, seção, tracers e referência magenta tracejada em h0. Os flags `grade`, `meridiana`, `marcadores` e `referencia` aceitam -1 (segue modo), 0 (oculta), 1 (mostra).
- Tracers facetados pequenos, todos com raio 0,028: 8 no anel interno e 10 no externo, uniformemente espaçados. Emissão 0,25, sem adicionar bloom.
- Tesselação: **128 divisões azimutais × 32 anéis radiais**, 256 pontos nos anéis de curva. Smooth shading com quinas preservadas entre topo/lateral/fundo. Nenhuma subdivisão pesada.
- Enquadramento vertical mais próximo, usando a circunferência do recipiente em vez da diagonal da caixa; elevação 27°, margem nominal 3,5%. Espaço acima e abaixo para futura composição.

## Controles independentes

`controle.estado(lam=...)` modifica a altura da superfície e suas curvas:

`z(r, λ) = h0 − λ α R²/2 + λ α r²`, com `α = Δh/R² = ω²/(2g)`.

`controle.estado(fase_rotacao=...)` modifica somente posição angular e orientação dos tracers:

`φ = φ0 + 2π × voltas × fase_rotacao`.

Raio e altura dos tracers permanecem constantes inclusive durante o morph. Para permanecerem dentro do líquido em todos os λ, sua altura é fixada na construção em `min(h0, z(r,1)) − prof_marcador`. Com a ficha atual: anéis em r=0,60 / 1,02 e z=1,02 / 1,27. São marcadores internos; não acompanham a interface livre.

`estado_editorial(tipo, fase)` fornece os controles dos previews. O morph não escreve `fase_rotacao`; a rotação não escreve `lam`. O loop de QA continua disponível em `atualizar(fase)` com `movimento=1, varrer_lambda=1`, sem se tornar o comportamento do morph editorial.

## Previews

Todos em **540×960**, Eevee, 24 amostras. Cada animação tem **48 quadros, 15 fps, 3,2 s**, sem áudio. MP4 em H.264, yuv420p, CRF 14, preset medium; são arquivos de avaliação, não masters.

- [Fenômeno, λ=0](fenomeno_lambda0.png)
- [Fenômeno, λ=1](fenomeno_lambda1.png)
- [Geometria e seção meridiana](geometria_meridiana.png)
- [Comparação dos três stills](comparacao.png)
- [Morph one-shot](morph.mp4): hold inicial; smoothstep monotônico de λ=0 a 1 entre 15% e 75% da duração; hold final de aproximadamente 0,8 s. Tracers imóveis para isolar o controle da forma.
- [Rotação dos tracers](rotacao.mp4): λ=1 fixo, uma volta; apenas movimento azimutal.
- [Payoff seção → superfície](payoff.mp4): λ=1; seção inicialmente isolada, revelação suave do líquido/grid, paralaxe de câmera de apenas 4°, hold final. A seção continua destacada.
- [Loop de QA](loop_qa.mp4): λ=0→1→0 e uma volta dos tracers, para comparação com o editorial.
- [Folha de estados das quatro animações](sequencias.png)

PNGs de cada animação em `morph/`, `rotacao/`, `payoff/` e `loop_qa/`. Os arquivos `*_estados.json` registram os controles usados em cada quadro; `resumo.json` registra custo de render, duração e peso dos MP4.

## Verificações realizadas

- `py_compile` nos cinco módulos Python envolvidos: passou.
- `git diff --check`: sem erros de whitespace; apenas aviso já existente de conversão LF/CRLF em `abrir/LEIA-ME.md`.
- Verificador executado no Blender com `--python-exit-code 1`: **RESULTADO: OK**. Log em [qa.log](qa.log).
- Volume analítico πR²h0 = 6,107256118579, preservado nos sete λ verificados; erro numérico relativo máximo 4,36×10⁻¹⁶.
- Corpo fechado/manifold e normais do topo para fora nos sete estados. Centro 1,35→0,85; borda 1,35→1,85, ambos monotônicos.
- Aproximação poligonal da malha: volume 6,104804→6,105540, variação relativa **0,0121%** entre λ=0 e 1. A fórmula não recebe correção manual; essa diferença vem da discretização linear.
- Tracers: raio/altura invariantes, giro de 90° em um quarto de volta, fechamento em uma volta; fase não altera a malha e λ não altera posições dos tracers.
- Modos e referência opcional conferidos; ficha compatível com o adaptador do arsenal.
- Morph monotônico, hold final e ausência de retorno ao plano verificados; loop QA preservado.
- Enquadramento testado por projeção em todos os quadros das quatro sequências, incluindo paralaxe: sem clipping do recipiente.
- MP4 decodificados integralmente após montagem: 48 quadros por arquivo. Stills e folhas de estados inspecionados visualmente para leitura do volume, superfície, seção, grade e tracers.

## Limitações e parada

Prévia suficiente para avaliação editorial; **nenhum render 1080×1920 foi executado**. O contorno usa tesselação e smooth shading apropriados, mas a aparência nessa resolução ainda depende de futura avaliação. Transparências continuam estilizadas no Eevee, sem refração ou simulação física de água. A discretização tem o pequeno erro de volume informado acima.

O morph é somente interpolação didática entre estados, não dinâmica real do transiente. O payoff usa revelação por opacidade; não há uma simulação de preenchimento nem integração de curva do Manim.

Asset permanece em estudo. Sem mudanças no vid_0022, template, dependências ou documentação global; sem voz, SRT, capa, publicação, commit ou push. Próximo passo depende da avaliação humana destes previews.
