# Postagem — vid_0022 · EP. 08

Fechamento autorizado em 12/10/2026. Vídeo final de 170,8 s em 1080×1920, 30 fps nativos, H.264/yuv420p/CRF 14. Master com voz e versão com legendas coloridas, ambos com início rápido de reprodução (faststart).

## Fluidez

- Render novo a 30 fps; o preview de 15 fps não é a fonte dos finais.
- Transformações algébricas duram no máximo 1,4 s. O tempo restante fica em pausas de leitura após a conclusão da transformação, preservando a sincronização aprovada.
- Os 12 mapas explícitos de glifos permanecem. Interpolação temporal local dos PNGs 3D suaviza a mudança de pose e de fase, preservando transparência.
- Montagem por seleção dos blocos nativos, sem repetir ou descartar quadros dentro dos movimentos utilizados. Ordem de narração e voz recebida preservadas.

## Arquivos desta rodada

Cena: `cena_postagem.py`. Preparação e planejamento: `preparar_3d_postagem.py`, `planejar_postagem.py`, `suavizar_3d.py`. Montagem e verificações: `montar_postagem.py`, `validar_postagem.py`, `verificar_postagem.py`. Metadados: `cache_3d_postagem.json`, `projecao_3d_postagem.json`, `timing_postagem.json`, `operacoes_postagem.json`, `marcos_postagem.json`, `montagem.json`. Ficha atualizada. Versões anteriores e alterações externas preservadas; nenhum arquivo global alterado nesta rodada.

## Verificações e renders

- Compilação Python dos auxiliares e cena: aprovada.
- Construção prévia: 125 operações e 12 mapas de glifos, aprovada.
- Um render completo Manim em 1080×1920/30 fps, seguido de montagem de master e legendado.
- Ambos os finais: 5.124 quadros decodificados, cadência constante de 30 fps, 170,8 s, CRF 14, áudio AAC estéreo completo de 166,8 s e faststart conferido.
- Legendas: 65 entradas, 458 palavras correspondentes ao texto confirmado, até duas linhas, sem sobreposição temporal e dentro da largura segura. Branco com destaques ciano, violeta e azul conforme o significado no vídeo.
- Inspeção visual de 41 instantes, incluindo cancelamentos, regra da cadeia, integração, paraboloide, desnível e encerramento. Verificados 15 intervalos de transformação matemática; maior sequência quase estática no interior desses movimentos: 4 quadros (0,133 s). Pausas intencionais de leitura não entram nessa métrica.
- Evidências: `qa_postagem/validacao.json`, seis painéis em `qa_postagem/` e logs locais de preparação, render, montagem e verificação.

## Teste do arsenal

Sólido: `liquido_rotacao`, sem tracers, com setor angular translúcido. Preparadas 397 imagens em 1080×1920, 24 amostras; 657,1 MiB e aproximadamente 421,6 s de Blender. A resolução nativa e a interpolação local funcionaram nas inserções aprovadas. A álgebra e as anotações permanecem Manim 2D. O morph da abertura é uma interpolação didática, não uma simulação do transiente; nenhum ajuste global do asset foi necessário.

## Entrega e limites

Origens: `renders/vid_0022_postagem_master.mp4` e `renders/vid_0022_postagem_legendado.mp4`. Entrega oficial por `videos/entregar.py vid_0022`, com SRT, voz, textos e manifesto. Master: 14.182.224 bytes; legendado: 15.624.150 bytes.

Os tempos de fala mantêm o alinhamento por pausas e frases aprovado pelo usuário, sem alinhamento fonético automático. Nenhuma capa nova, publicação, commit ou push foi realizada.
