# Estado da implementação — preview em construção

Escopo preservado: vídeo inteiro silencioso, 960×540/15 fps. Nenhum áudio, SRT, master, entrega final ou operação Git.

## Concluído

- Handoff v2 preservado; Anexo A extraído sem reescrita: 62 âncoras, 4.933 palavras.
- Kit copiado do yt_0022; arquivos locais cena.py, cena23.py, conteudo.py, visual23.py, fisica.py e modelos Three.js f23.js.
- Correção de herança de cor em subscritos, posicionamento de rótulos da haste e projeção dos pontos 3D.
- 178 expressões LaTeX compiladas, zero erro; quatro precisam de quebra de linha (tratamento local implementado, layout ainda não revalidado).
- 25/25 conferências do modelo físico passaram; sintaxe dos cinco módulos principais validada.
- Todos os gatilhos das contas encontrados na narração aprovada.
- Sonda estática E2-8 e sonda 3D do carretel geradas. Não constituem preview completo aprovado.

## Pendências reais

- Completar os detalhes específicos do storyboard: barras de energia e composição, comparação de volantes, trilhas de itens, voos semânticos e glyph maps, diagramas completos e passagens de síntese.
- Rever pacing de cada âncora: a implementação atual contém esperas extensas que não atendem PARADO.
- Revisar dimensões, fontes, colisões e quatro fórmulas largas após quebra. Não declarar G28 aprovado.
- Medir cores dos números substituídos, operadores e subscritos nos quadros.
- Concluir pedidos e render Three.js; medir alinhamento e vínculo nos quadros efetivos, não apenas no modelo.
- Renderizar os sete lotes completos, montar preview, executar todos os portões, gerar pranchas, capítulos e zip sem mp4.

## Artefatos de diagnóstico

- renders/compilacao_equacoes.json: 178 resultados de compilação e dimensões.
- renders/fisica_modelo.json: conferências do modelo; não substitui auditoria dos quadros.
- renders/carretel_sonda.png: geometria 3D inicial.
- media_teste/images/cena/PE2_ManimCE_v0.21.0.png: primeira sonda da haste, anterior às correções de subscritos/rótulos.
- renders/ph_check.log: execução da sonda do lote PH; conferir resultado antes de reexecutar.

Ambiente existente preservado. uv/MiKTeX precisaram rodar fora do sandbox para persistir caches. Chrome existente usado pelo Playwright, via CHROMIUM_PATH; NODE_PATH aponta para node_modules do kit de origem, sem instalação.
