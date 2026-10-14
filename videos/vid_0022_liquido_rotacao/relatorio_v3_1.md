# VID 0022 — V3.1 de acabamento editorial

V3.1 implementada a partir da V3 estruturalmente aprovada, para **POR TRÁS DA FÓRMULA · EP. 08**. Física, álgebra, asset, header e cartão final preservados. A V3 e seu preview continuam disponíveis para comparação.

## Preview

- [Abrir preview V3.1](media/videos/cena_v3_1/960p15/preview_silencioso_v3_1.mp4).
- Caminho absoluto: `C:\Users\Pichau\PycharmProjects\manim-fisica\videos\vid_0022_liquido_rotacao\media\videos\cena_v3_1\960p15\preview_silencioso_v3_1.mp4`.
- **168 s / 2min48s**, mesma duração da V3. MP4: 167,998 s.
- 540×960, 15 fps nominais, 2.520 quadros, H.264/yuv420p, sem faixa de áudio.
- 2.746.251 bytes / 2,62 MiB.
- [Metadados](qa_v3_1/metadados.json); [marcos e auditoria das headlines](marcos_v3_1.json).

## Textos e alinhamentos

As headlines seguem centro x=0, y=5,65 e largura máxima de 7,4 unidades, com Space Grotesk 28 e ajuste apenas quando necessário. O header aprovado não foi alterado. Foram registradas e verificadas **11 entradas de headline**.

Principais reformulações:

- “Um corte vertical do líquido” → “Veja o líquido em uma seção pelo eixo”.
- “A face externa empurra um pouco mais” → “A pressão é maior na face externa”.
- “A diferença deixa uma resultante para o eixo” → “Essa diferença fornece a força centrípeta”.
- Superfície: “Em toda a superfície:” com p=p_atm em MathTex na mesma linha.
- “Quanto mais longe do eixo, maior a inclinação” → “A inclinação cresce com r”.
- “Integrar a inclinação constrói a curva” → “Integrar a inclinação revela a forma”.
- Payoff: “Esta parábola é uma seção da superfície 3D”.

Removidos: título durante o zoom, headline durante os cancelamentos, frase inferior longa de extração e headlines concorrentes na conclusão. A headline de integração também sai antes da solução final. O movimento e as fórmulas ficam sozinhos nesses intervalos.

Rótulos locais:

- “elemento do líquido” acompanha a região durante a extração, abaixo da seção e sem encostar em seu contorno.
- “mais longe do eixo → maior pressão” fica imediatamente junto da faixa de pressão, substituindo quatro pequenos rótulos e a headline redundante.
- “r e z mudam — p não” fica junto da curva isobárica; p_atm acompanha o ponto.
- A relação r↑ ⇒ dz/dr↑ acompanha a posição do ponto/tangente, com limites laterais para permanecer na área segura. A indicação inferior distante foi removida.
- z(0)=z0 permanece no próprio gráfico.

O texto de estado estabilizado foi aproximado do objeto. O zoom mantém uma região azul translúcida ao redor do elemento antes de retirar o contexto. A faixa de pressão usa 64 segmentos contíguos de intensidade crescente, substituindo os oito blocos separados. Na regra da cadeia, dr e o termo radial compartilham ciano; dz e o termo vertical compartilham azul-ciano. Não foram introduzidas novas cores.

## Payoff e conclusão

O Blender está **13,6% maior** que na V3: a escala de 0,88 passou a 1,00. A fórmula e o bracket foram acomodados à direita sem reduzir o objeto. O bracket permanece conectado às alturas do centro e da borda, com Δh=z(R)−z(0)=ω²R²/(2g).

As três batidas usam o mesmo cache:

1. Aproximadamente 154,9–157 s: paraboloide grande, bracket e Δh; sem headline ou mensagem concorrente.
2. Aproximadamente 157,6–160,2 s: Δh sai, a meridiana branca ganha destaque e o restante do objeto fica discreto. dz/dr∝r transforma-se visualmente em z−z0∝r²; as duas fórmulas não permanecem simultaneamente.
3. Aproximadamente 160,8–164 s: volta o paraboloide limpo; entra maior “A FORMA É CONSEQUÊNCIA DA DINÂMICA.”. Bracket, Δh e demais fórmulas já saíram.

Depois, fade para o cartão aprovado: logo Parallax Lab e @labparallax. A síntese causal anterior, a estrutura 3D/2D e os **12 TransformByGlyphMap** foram mantidos. A troca da relação na conclusão usa TransformMatchingTex.

## Arquivos desta rodada

Criados: `cena_v3_1.py`, `validar_v3_1.py`, `inspecionar_v3_1.py`, `marcos_v3_1.json`, este relatório, `validar_v3_1.log`, `render_v3_1.log`, preview e pastas `qa_v3_1/` e `qa_v3_1_preflight_01/`.

Atualizado: `ficha.md`, para registrar a versão atual e seu acabamento. V3 e versões anteriores preservadas. Nenhuma modificação em template, dependências, ponte ou asset Blender nesta rodada. Alterações preexistentes do repositório preservadas.

## Validação e QA

- `py_compile` passou nos três módulos V3.1.
- Importação e construção localizada passaram: 168 s, 125 animações incluindo esperas e 12 mapas MF-Tools. Quadros estáticos permitiram revisar a composição antes do preview; o ajuste final do rótulo da seção foi confirmado no MP4.
- **Um único render completo V3.1**, concluído sem erro.
- PyAV confirmou resolução, duração, fps, quadros, codec e ausência de áudio.
- **49 quadros** extraídos do MP4, organizados em quatro folhas; estados críticos também vistos em tamanho integral.
- Conferidos: todas as headlines, rótulos locais, contexto azul do zoom, ausência de título nos cancelamentos, faixa radial, isóbara, cores dr/dz e regra da cadeia, indicação móvel junto da tangente, integração/z0, síntese, match e escala do payoff, Δh isolado, transformação da relação matemática, paraboloide limpo com frase final e branding.
- A auditoria geométrica confirmou centro e largura segura das 11 headlines. A presença do header foi verificada nos pixels dos 48 quadros amostrados anteriores ao cartão final.
- Não foram encontrados textos cortados, sobreposição impeditiva ou competição persistente entre as três batidas finais nos estados conferidos.
- `git diff --check` passou, com apenas aviso LF/CRLF em arquivo preexistente do arsenal.

Folhas: [parte 1](qa_v3_1/folha_qa_1.png), [parte 2](qa_v3_1/folha_qa_2.png), [parte 3](qa_v3_1/folha_qa_3.png), [branding](qa_v3_1/folha_qa_4.png).

## Teste do arsenal e limites

Sólido: **liquido_rotacao**, aprovado; quatro inserções, sem tracers editoriais. Todos os caches e projeções existentes foram reutilizados, em 540×960 RGBA / 24 amostras: 397 PNGs, aproximadamente 179,12 MiB. **Nenhum render Blender novo.**

Funcionou: ampliação do payoff, projeções alinhadas à nova escala, bracket conectado ao objeto e destaque independente da meridiana na conclusão. Nenhum parâmetro novo ou ajuste do asset foi necessário.

Pronta para revisão final de imagem antes da voz, sem bloqueio técnico conhecido. A inspeção se limita ao preview 540p/15 fps desta fase. Não foram criados voz, SRT, master, capa, render final ou publicação; sem commit/push.
