# VID 0022 — V2 visual silenciosa

V2 implementada para **POR TRÁS DA FÓRMULA · EP. 08**, com física e resultados preservados. A V1, sua cena e seu preview continuam disponíveis. Nenhuma etapa de voz ou finalização foi iniciada.

## Preview

- [Abrir preview V2](media/videos/cena_v2/960p15/preview_silencioso_v2.mp4).
- Caminho absoluto: `C:\Users\Pichau\PycharmProjects\manim-fisica\videos\vid_0022_liquido_rotacao\media\videos\cena_v2\960p15\preview_silencioso_v2.mp4`.
- Duração: **168 s / 2min48s**, seis segundos menor que a V1. MP4: 167,999 s.
- 540×960, 15 fps nominais, 2.520 quadros; H.264/yuv420p, sem faixa de áudio; 2.697.322 bytes (2,57 MiB).
- [QA: primeira parte](qa_v2/folha_qa_1.png), [segunda parte](qa_v2/folha_qa_2.png), [branding](qa_v2/166_branding.png) e [metadados](qa_v2/metadados.json).

## Mudanças estruturais

O elemento agora nasce de uma pequena região destacada dentro do líquido 3D, sobre a seção vertical. A seção e a região passam suavemente para a representação frontal; a região é ampliada antes de receber A, dr, coordenadas e massa. O mesmo objeto permanece durante a construção da força, Newton e a rotação para a análise vertical.

As contribuições de pressão aparecem nas faces e se reduzem às duas componentes radiais. A seta externa é aproximadamente 25% maior e aponta para dentro. A interpretação do gradiente positivo recebe uma faixa de regiões cuja intensidade aumenta para fora, na mesma altura.

A superfície isobárica retorna ao Blender com destaque em toda a interface e três rótulos de pressão atmosférica. A metade positiva da seção faz match com a curva 2D. Um ponto percorre essa curva com dr e dz antes da derivada total e da regra da cadeia.

Ponto, tangente e indicação do raio compartilham um ValueTracker. Na integração, outro tracker faz a curva crescer enquanto a álgebra se transforma. A metade direita é completada antes do espelhamento. z0 continua sendo a altura final no eixo.

A síntese causal usa a faixa de pressão, o movimento sobre a superfície isobárica, a rotação da tangente e o destaque da parábola. O payoff alinha a curva com a meridiana branca, revela superfície e grid com paralaxe real de 4° e apresenta Δh. O vídeo termina com a frase aprovada, seguida de logo e **@labparallax**.

O header copia escala, margens, opacidades e composição do último curto aprovado, `vid_0020`: série/episódio à esquerda, logo à direita. EP. 08 foi confirmado pelo usuário. Cores semânticas: coordenadas ciano, pressão violeta/magenta, forças brancas e superfície azul-ciano.

## MF-Tools

Foram usados **12 TransformByGlyphMap**, com MathTex de string única, faixas de glifos verificadas e `auto_fade=True`, sem índices no vídeo:

1. Substituição de Taylor a partir das duas expressões visíveis.
2. Cancelamento dos dois termos p(r)A e reorganização da força restante.
3. Montagem de Newton usando os termos da força, massa e aceleração.
4. Cancelamento de A dr e dos sinais negativos; a densidade permanece no gradiente radial.
5. Expansão local do balanço vertical.
6. Redução ao gradiente hidrostático.
7. Derivada total → regra da cadeia.
8. Substituição dos dois gradientes.
9. Cancelamento de ρ e isolamento da inclinação.
10. Derivada → diferencial, transportando dr para o outro membro.
11. Diferencial → integrais.
12. Integrais → solução, junto do crescimento da curva.

Os mapas e tempos efetivos estão em `marcos_v2.json`. TransformMatchingTex foi mantido na passagem final para Δh.

## Blender e teste do arsenal

Asset: **liquido_rotacao**, já aprovado. Quatro inserções: fenômeno, extração do elemento, superfície isobárica e payoff. Nenhum tracer editorial foi reintroduzido; os pontos de análise têm significado de posição/pressão.

Os três caches da abertura foram reaproveitados via ponte/Solido3D. `preparar_3d_v2.py` prepara um still de seção sem grid e uma sequência editorial local usando os controles existentes de revelação do asset. O leitor de PNGs da ponte reproduz essa sequência como ciclo único. Não houve modificação global da ponte ou do construtor.

- Resolução: 540×960, RGBA, 24 amostras.
- Novos renders: 77 PNGs (um still e 76 quadros do payoff), aproximadamente 58,7 s de Blender; 36.965.343 bytes (35,25 MiB).
- Caches novos: `renders/arsenal3d/liquido_rotacao/ac264bc46cc7` e `renders/vid_0022_v2/60afba7d4b85`.
- Caches efetivamente usados na V2: 397 PNGs incluindo os 320 reaproveitados da abertura; aproximadamente 179,12 MiB no total.
- Funcionou: origem espacial do elemento, projeção da seção para match, rótulos da superfície, revelação progressiva e paralaxe.
- Nenhum sólido ou parâmetro físico novo foi necessário. A álgebra continua em Manim. Qualidade/custo em 1080×1920 não foram avaliados.

## Arquivos desta rodada

Criados na unidade: `cena_v2.py`, `preparar_3d_v2.py`, `validar_v2.py`, `inspecionar_v2.py`, `cache_3d_v2.json`, `projecao_3d_v2.json`, `marcos_v2.json`, este relatório, logs e artefatos de preview/QA. `ficha.md` foi atualizada para a V2 e o EP. 08.

As alterações preexistentes do repositório foram preservadas. `cena.py` e o MP4 da V1 não foram sobrescritos. Nenhum arquivo global de template, arsenal ou dependências foi alterado nesta rodada.

## Verificações e limites

`py_compile` passou nos quatro módulos novos. Importação e construção completa sem gravação de vídeo passaram: 168 s, 102 animações e 12 mapas, sem modo de debug. Quadros estáticos foram conferidos antes do único render completo V2.

O render completo terminou sem erro. PyAV confirmou duração, resolução, fps e ausência de áudio. Foram inspecionados 33 quadros extraídos do próprio MP4, cobrindo origem/zoom do elemento, forças, cancelamentos, transição vertical, isobárica 3D, deslocamento dr/dz, regra da cadeia, tangente, integração, espelhamento, síntese, match, paralaxe, Δh e branding. A presença do header também foi conferida diretamente nos pixels dos 32 estados anteriores ao cartão final. Não foi encontrado clipping impeditivo ou inconsistência física objetiva.

`git diff --check` não apontou erros de whitespace; houve apenas aviso LF/CRLF em arquivo preexistente do arsenal.

Sem bloqueios técnicos conhecidos nesta fase. A aprovação editorial da V2 fica para a revisão do usuário. Não foram produzidos voz, SRT, 1080×1920, master, capa ou publicação; não houve commit/push.
