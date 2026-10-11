# Por que uma integral dupla calcula volume?

- id: vid_0020_integral_dupla_volume (confirmado pelo usuário)
- formato: curto_vertical
- família: POR TRÁS DA FÓRMULA
- número público na série: EP. 07 (confirmado pelo usuário)
- estado: final legendado renderizado e conferido em 1080×1920 / 30 fps
- arquivo_final: final_legendado.mp4
- duracao_final: 171,80 s (áudio aprovado: 171,36 s)
- relatorio_final: render_final.md
- solido_3d: nenhum

Versão intencionalmente produzida em Manim 2D. Blender não é dependência
desta unidade. Prismas e superfície usam a mesma projeção axonométrica fixa.

## Matemática verificada

Pergunta central: por que uma integral dupla pode calcular volume?
Função f(x,y)=4−x²−y²; R=[−1,1]². Sólido: 0≤z≤f(x,y), (x,y)∈R.
f(0,0)=4; f(±1,±1)=2; f>0 em toda a região.

Partições n×n, Δx=Δy=2/n, amostras nos centros reais das células.
Base ΔA=ΔxΔy; altura h=f(x_i,y_j); contribuição ΔV≈hΔA.
O prisma aproximante tem volume exatamente hΔA; a aproximação se refere
à contribuição sob a superfície curva naquela célula.

V=∫ de −1 a 1 ∫ de −1 a 1 (4−x²−y²)dy dx.
Primitiva interna: (4−x²)y−y³/3; avaliação: 22/3−2x².
Primitiva externa: 22x/3−2x³/3; avaliação: 40/3≈13,33.
Checagem independente: 16−4/3−4/3=40/3.
Somas dos pontos médios: S_n=40/3+8/(3n²), para n=4,8,16,32,64.
Erros uniformes das alturas: 0,875; 0,46875; 0,2421875; 0,123046875;
0,06201171875. Em 64×64, S_n=13,333984375 e ΔA=1/1024.
Área das seções: A(x)=∫ de −1 a 1 f(x,y)dy=22/3−2x².
Não se afirma que toda integral dupla é volume e não se descreve dA como
um quadradinho infinitamente pequeno.

## Construção V5, preservando a V4

Cabeçalho baseado apenas na implementação visual de vid_0011: marca com
largura 1,8/opacidade 0,35/margem 0,28; série à esquerda, EP. 07,
margem 0,4/opacidade 0,65. vid_0014 não está neste checkout.

Um mesmo sistema x/y/z e a região R permanecem reconhecíveis. A superfície
é traçada nos eixos e recebe rótulo com seta. A região divide-se em 4×4.
Uma cópia de leitura amplia a base sem deslocar a célula original.
Δx e Δy geram ΔA=ΔxΔy. O ponto médio lança uma vertical até f(x_i,y_j);
só depois a célula extruda. Base e altura geram seus termos na fórmula.
As outras colunas crescem em onda ordenada de trás para frente.

Refinamento 4×4→8×8→16×16→32×32: cada mãe divide-se em quatro filhas que herdam
inicialmente sua altura; depois os topos movem-se aos valores dos novos
pontos médios. Superfície, eixos, projeção e domínio permanecem fixos.
Tempos de subdivisão e ajuste diminuem a cada nível. n crescente e Δx/Δy
decrescentes acompanham ΔA=4/n². n→∞ e ΔA→0 explicitam o limite na passagem
do somatório para a integral dupla. As arestas são mais finas nos níveis densos.
O estágio 64×64 aparece brevemente: 4.096 topos nos pontos médios exatos,
faces de fronteira e degraus expostos agrupados em três caminhos compostos.
Faces internas ocultas são omitidas. Incluir os degraus expostos evita
frestas escuras entre os topos, sem construir 4.096 animadores individuais.
O indicador mostra Δx=Δy=2/n, ΔA=4/n² e, em 64×64, 4/4096=1/1024.
n→∞/ΔA→0 entra antes da transformação do somatório para a integral.
128×128 não faz parte desta rodada.

Uma seção real x=x_0 revela a curva z=4−x_0²−y² e a área sob ela. A seção
começa com x fixo: a vertical magenta percorre y, preenchendo a área da
seção. dy recebe destaque. Depois o plano percorre x, recalculando curva e
área juntas; A(x) permanece visível e a integral externa recebe dx em
violeta-claro. O bloco interno é copiado da expressão de A(x) para a
integral externa. Na seção, a casca curva exata deixa a área legível depois
da exposição curta da malha 64×64. As linhas internas da base ficam atenuadas
durante a seção; contorno de R e eixos permanecem reconhecíveis.

A conta reduz temporariamente a escala e a opacidade da geometria, preservando
os preenchimentos originais e a projeção. A integral externa fica como contexto
atenuado. Isolar a integral em y e explicitar x constante; separar o fator
4−x². Os apoios ∫dy=y e ∫y²dy=y³/3 geram a primitiva por cópias. Mostrar
y=1 e y=−1 em duas linhas, simplificar os valores e subtraí-los. Transformar
2(4−x²)−2/3 → 8−2x²−2/3 → A(x)=22/3−2x². Retomar a área da seção antes
de abrir a conta externa. Copiar A(x) para V=∫A(x)dx e seus termos para
a integral explícita; separar as integrais e construir 22x/3 e 2x³/3 a partir
dos respectivos apoios. Montar a primitiva e aplicar limites. Mostrar
22/3−2/3=20/3 e −22/3+2/3=−20/3, depois transportar esses valores para
20/3−(−20/3) → (20+20)/3 → 40/3≈13,33.

Payoff: colunas crescem sob a referência, a superfície recebe destaque,
e a geometria gera V=∬_R f(x,y)dA. “Somar pequenas contribuições sobre toda
a área.” O payoff usa 16×16 para leitura dos prismas. A leitura de volume
se aplica neste exemplo de alturas positivas.
Uma sequência curta ΔV→ΣΔV→∬_R f dA retoma a pergunta inicial.

## Semântica e ritmo

Ciano: domínio/base/ΔA e referência exata. Magenta: altura f(x_i,y_j).
Violeta: volume e somatório. Azul-violeta escuro: demais colunas.
Ciano-claro (#8CEBFF): área da seção, integral interna, y e dy ativos.
Violeta-claro (#C4B5FF): acumulação externa, x e dx ativos.
Branco: constantes, conectivos e textos neutros. A variável x fica branca
durante a integração em y, pois nessa etapa ela é constante.
Sem títulos grandes permanentes. Pausas explícitas limitadas a 1,2 s;
as ações constroem, transferem, extrudam, subdividem ou varrem a geometria.
Microtextos temporários guiam célula, base, altura, repetição, limite e cálculo.

## MF-Tools na V5

TransformByGlyphMap (1.4.9 já instalado) usa MathTex de string única com
faixas de glifos nomeadas e verificadas. auto_fade=True; nenhum índice/debug
aparece no vídeo. No somatório→integral dupla, ∑ gera os dois sinais de
integração; i,j e os índices das amostras desaparecem por fade, e R entra
separadamente. f, x, y e A preservam seus próprios glifos. Outras entradas:
estrutura na expansão da integral iterada e isolamento da integral em y;
separação dos termos de y e x; colchetes/limites nas primitivas já montadas;
cópias das substituições em ±1; agrupamento e simplificação da área;
cópia de A(x) para a integral externa; reunião dos dois 20/3 e conservação
de 40/3 na aproximação decimal. TransformFromCopy público monta as regras
de potência, as primitivas a partir dos apoios e a substituição dos termos
calculados de A(x). Não se força um glyph map nessas montagens. A dedução
por seções copia o bloco interno da fórmula de A(x), preservando a estrutura
externa. As letras y/x ativas recebem cor sem recolorir constantes e conectivos.

## Histórico: validação V4

py_compile passou. Render V4 concluído em 540×960/15 fps, 2.137 frames,
duração medida de 142,46 s e nenhuma faixa de áudio.
Checks locais passaram: cobertura do quadrado, alturas positivas, convergência,
somas dos pontos médios e área das seções em cinco posições de x comparada
numericamente com 22/3−2x². Apenas uma seção de 65 amostras tem updater;
os prismas usam estados pré-construídos. Uma seção parcial e sua vertical
possuem updater apenas durante a varredura em y.

Inspeção visual localizada de 31 estados e sete conferências adicionais em
timestamps: cabeçalho EP. 07; eixos e superfície; célula/vertical/coluna;
fórmula com cores herdadas da base e altura; geração das colunas; níveis
8/16/32 e leitura explícita do limite; preenchimento da seção em y;
varredura em x; substituição de A(x) pelo bloco interno; função expandida;
primitivas, avaliações e payoff. A entrada de A(x_0) foi separada da escrita
dos outros termos para evitar disputa sobre os mesmos glifos. A(x) é copiado
para a integral externa. Os quadros de leitura não conservam fórmulas residuais.

O indicador automático de pouca mudança encontrou intervalo máximo de
2,40 s. A medida usa imagem reduzida e não substitui a inspeção visual.
Os marcos de cena são aproximados; os JPEGs registram os tempos do MP4.
Artefatos de inspeção: media/vid_0020_preview_v4/inspecao/.

Limitações: em 32×32 as bases individuais ficam pequenas no preview;
a leitura de ΔA ocorre na malha 4×4 com cópia ampliada. A representação
usa projeção 2D fixa, com camadas e transparência para revelar a seção.

Prévias anteriores preservadas em media/vid_0020_preview/ e
media/vid_0020_preview_v2/. Os três arquivos anteriores à V4 foram copiados
para media/vid_0020_preview_v4/fonte_anterior/ (artefatos ignorados).

Saída V4: media/vid_0020_preview_v4/videos/cena/960p15/IntegralDuplaVolume020.mp4.
Marcos: media/vid_0020_preview_v4/marcos.json.

Comando: uv run --no-sync python -m manim -r 540,960 --fps 15 --media_dir media/vid_0020_preview_v4 videos/vid_0020_integral_dupla_volume/cena.py IntegralDuplaVolume020.
Sem voz, áudio, legendas, capa, master, final ou QA global.

## Validação V5

Diff comparado com a cópia da V4; py_compile passou. Checks locais passaram
em 4, 8, 16, 32 e 64: cobertura literal de R, alturas f nos pontos médios,
positividade, somas e erros uniformes decrescentes. Área da seção conferida
numericamente em cinco posições de x. O campo denso tem exatamente 4.096
topos. Faces expostas fecham os degraus; faces internas ocultas são omitidas.
64×64 foi viável no render. 128×128 não foi testado: o alvo era 64×64.

Render consolidado concluído: 540×960, alvo de 15 fps, 3.019 frames,
201,263 s e nenhuma faixa de áudio. Foram conferidos 33 estados mais dois
frames específicos da base/extrusão: célula→coluna, 32→64, limite explícito,
soma→integral, seção e sweep, separação e regras de y/x, primitivas montadas,
substituições em ±1, subtrações, A(x), transporte para a integral externa,
40/3, aproximação decimal e retorno à interpretação geométrica.

A primeira prova revelou frestas ao omitir os degraus visíveis em 64×64;
eles foram incluídos. A atenuação da malha preserva seus preenchimentos
originais, evitando fechar e preencher as curvas da superfície. As cores
ativas foram conferidas nos frames: y/dy em ciano-claro, x/dx em violeta-claro;
constantes e conectivos neutros. Nenhum índice de desenvolvimento em tela.

Limitações: células de 64×64 não são individualmente legíveis em celular;
a explicação de ΔA ocorre na malha 4×4. A visualização densa é otimizada para
a projeção fixa aprovada. O payoff usa 16×16 para leitura dos prismas.

Cópia da fonte V4 preservada em media/vid_0020_preview_v5/fonte_v4/.
Saída: media/vid_0020_preview_v5/videos/cena/960p15/IntegralDuplaVolume020.mp4.
Inspeção e metadados: media/vid_0020_preview_v5/inspecao/.
Marcos de cena: media/vid_0020_preview_v5/marcos.json. A inspeção também
registra marcos no relógio do MP4 a partir dos 169 clipes de animação.

Comando: uv run --no-sync python -m manim -r 540,960 --fps 15 --media_dir media/vid_0020_preview_v5 videos/vid_0020_integral_dupla_volume/cena.py IntegralDuplaVolume020.
Somente preview silencioso; nenhuma etapa posterior, commit ou push.
