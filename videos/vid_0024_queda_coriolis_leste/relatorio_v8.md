# Rodada V8 — separação Coriolis / queda

## Identidade e arquivos

- Pasta inteira movida de `videos/vid_0023_queda_coriolis_leste` para `videos/vid_0024_queda_coriolis_leste`, incluindo fontes, versões preservadas, previews e QA anteriores. A unidade não estava rastreada: `git mv` não era aplicável.
- Classe `QuedaCoriolis023` → `QuedaCoriolis024`; nomes e referências internas migrados. Lista detalhada de 13 renomeações internas e 33 arquivos textuais atualizados em `migracao_0024.json`.
- Criados: `cena_v7_preservada.py`, `revisar_v8.py`, este relatório e artefatos V8 de render/QA. Fora desta unidade, somente `videos/vid_0023_coriolis/ficha.md` foi criado.
- Alterados nesta rodada: `cena.py`, `ficha.md`, `docs/decisoes.md` e `docs/estado_atual.md`. Alterações preexistentes de outras unidades e do arsenal preservadas.
- O 0023 fica PLANEJADO — NÃO INICIADO, apenas ficha, sem cena ou storyboard. Produção após terminar tecnicamente o 0024; publicação pretendida 0023 → 0024. Header público EP. 06 preservado.

## Mudanças didáticas e visuais

- Removida da cena ativa toda a derivação extensa: conservação do momento angular, comparação quantitativa das contribuições que originavam o fator 2, reorganização dessa soma e demonstração do referencial girante. Nenhuma haste/disco de prova.
- Globo 2.5D girante, malha discreta, equador ciano, polos, eixo e vetor angular alinhados; arco de giro separado. Intuição breve com dois raios, arcos e vetores tangenciais diferentes.
- Recap distingue velocidade relativa à Terra da velocidade de rotação anterior, com cores e legendas para os três vetores, sem derivar a expressão.
- Equador, radial, tangente, eixo e ponto do experimento transformam-se em chão, eixos locais, norte, torre e bola.
- Soltura mostra `v(0)=0 → a_C(0)=0`; cópias de termos físicos constroem a substituição. A direção x aparece junto à seta ciano para leste.
- Um único tempo controla bola, trajetória e vetores; comprimentos limitados e vetor vertical limitado pelo chão. O fator de exagero lateral cai animadamente até 1, com ampliação ligada ao impacto.
- Integrais definidas com condições iniciais; a velocidade obtida se transforma na relação `dx/dt=v_x`. Valores numéricos entram um por vez e conversões antecedem o payoff limpo.

## Ferramentas de animação

`TransformByGlyphMap` (MF-Tools) cancela os dois fatores 2 e a barra da fração, preservando os glifos restantes na primeira integral. `TransformMatchingTex` atende à reorganização das relações e operações algébricas. Cópias congeladas dos objetos físicos e substituições por slot controlam a montagem vetorial e numérica, sem necessidade de mapas frágeis nessas passagens.

## Render e QA

Comando do preview:

```powershell
$env:UV_CACHE_DIR = Join-Path $PWD '.uv-cache'
uv run --no-sync python -m manim -r 540,960 --fps 15 --progress_bar none videos/vid_0024_queda_coriolis_leste/cena.py QuedaCoriolis024
```

Preview: `media_v8/videos/cena/960p15/QuedaCoriolis024.mp4`.

Primeiro render completo: 122,665 s (2min02,7s), 540×960, 1.840 quadros, aproximadamente 15 fps. Decodificação completa com timestamps estritamente crescentes. Inspecionados os 19 checkpoints e 123 amostras cronológicas, incluindo transformações intermediárias.

Na primeira inspeção, corrigidos: rótulo móvel de velocidade próximo dos eixos ao chegar ao chão (retirado antes da queda livre animada, após identificar o vetor); sincronização da entrada de `x̂` com a seta ciano (escrita da identidade separada do resultado); fórmula numérica elevada de y=1,2 para y=1,65 para dar respiro ao topo da torre. Rerenderização V8 corrigida concluída sem erros. Os 19 checkpoints foram reinspecionados, assim como as transições afetadas da direção leste, queda e substituição numérica; os problemas observados foram resolvidos.

Verificações: `py_compile` da cena e do extrator de QA sem erros; `git diff --check` dos dois documentos globais sem erros; auditoria de estrutura confirma classe 024, EP.06, ausência de derivação longa, único tempo físico e reserva 0023 contendo apenas a ficha. O ensaio seco inicial foi interrompido, e a tentativa com `-ql` foi substituída pelo comando de resolução explícita acima. Um SVG temporário vazio foi removido individualmente e regenerado; sem limpeza ampla ou mudanças no ambiente.

Limitação de QA: inspeção por quadros cronológicos e decodificação integral não equivalem a assistir continuamente em tempo real. O controle do player local permaneceu indisponível na sessão; reprodução contínua não foi confirmada. Essa etapa do pedido permanece pendente, sem alegação de QA integral concluído.

Resultado final: **122.665 s (2min02,7s)**, **540×960 / 15 fps**, **1840 quadros** decodificados sem erro, timestamps crescentes. 19 checkpoints e 123 amostras intermediárias extraídos novamente do MP4 corrigido. A estrutura restante foi conferida na inspeção cronológica anterior, e os 19 estados finais conferidos novamente.

Artefatos: `qa_v8/19_frames_01.jpg`, `qa_v8/frame_01.png` até `frame_19.png`, `19_frames_v8.zip`, `qa_v8/verificacao.json`, `qa_v8_estrutura.json`, `qa_v8_timestamps.json` e `render_v8.log`.

## Precisão do resultado

Mantido o payoff solicitado de 0,77 cm. O valor intermediário é 0,776 cm; arredondamento convencional a duas casas seria 0,78 cm. A substituição mostra `3,19…` para preservar a precisão interna do tempo de queda. Modelo idealizado, equatorial, sem arrasto e em primeira ordem na rotação.

## Teste do arsenal

Nenhum sólido Blender integrado: o briefing pede geometria vetorial 2.5D transformável no Manim. Resolução do preview: 540×960; custo/peso do arsenal não se aplica. Não foram alterados sólidos ou bibliotecas compartilhadas nesta rodada.
