# Revisão visual V4 — vid_0022

Feedback atendido nesta rodada: abertura com pouca ação, construção das grandezas concentrada, diagrama radial com aparência estática e pedido de `@labparallax` menor em degradê.

## Alterações

- 0–16 s: deformação da superfície, desenho do perfil, setor girando por ciclos completos e textos explicando centro/borda e co-rotação. A troca de texto sobre velocidade angular deixa de ocupar uma longa transformação de letras.
- 16–23 s: corte, extração, sentido positivo radial, medida da distância e zoom distribuídos pelas frases da narração. Âncoras próprias em `sync_v4.json`; sincronização anterior preservada.
- 23–34 s: área, espessura, volume e massa construídos separadamente, seguidos de velocidade e aceleração. Um único elemento retangular percorre a órbita; os vetores são tangente e radial para dentro, e a aceleração só aparece na sua frase.
- Explicação radial: a órbita continua durante as pausas de álgebra. O elemento ampliado representa o zoom local que acompanha o material; não recebe oscilação artificial na direção das forças.
- Balanço vertical: termos da equação vêm dos rótulos das forças. Destaques sequenciais mostram pressão inferior, pressão superior, peso e o sinal do gradiente. A posição vertical permanece em equilíbrio.
- Campo de pressão: percurso da região menos intensa à mais intensa. Tangente: percurso adicional pelo perfil, ligado à relação entre distância e inclinação.
- Encerramento: `@labparallax` em 28, antes 33, com degradê ciano, azul claro e azul.

## Arquivos e reprodução

Novos: `cena_v4.py`, `planejar_v4.py`, `validar_v4.py`, `montar_v4.py`, `verificar_v4.py`, `sync_v4.json`, `timing_v4.json`, `operacoes_v4.json`, `marcos_v4.json` e este relatório. `ficha.md` atualizada. Logs e QA ficam na própria unidade. Nenhum arquivo global ou versão anterior foi alterado nesta rodada.

Planejamento: `uv run --no-sync python videos/vid_0022_liquido_rotacao/planejar_v4.py`.

Render completo: `uv run --no-sync python -m manim videos/vid_0022_liquido_rotacao/cena_v4.py LiquidoRotacao022V4 -r 540,960 --fps 30 -o preview_v4_fonte --disable_caching --progress_bar none`.

Iteração localizada da abertura: mesmo comando, com `-n 0,28 -o preview_v4_abertura_fonte`. A montagem utiliza os 1.028 quadros dessa revisão inicial e os demais blocos do render completo, sem reamostragem temporal. Depois: `montar_v4.py` e `verificar_v4.py` via `uv run --no-sync python`.

## Verificações executadas

- Compilação Python aprovada.
- Construção completa validada: 141 operações, 12 mapas explícitos de glifos; fonte de 175,0667 s antes da seleção/reordenação dos blocos narrados.
- Um render completo de preview e uma iteração localizada da abertura; montagem com a voz recebida e legendas coloridas existentes.
- Ambos os previews: 540×960, 30 fps constantes, 5.124 quadros decodificados, duração de 170,8 s, áudio completo de 166,8 s, H.264/yuv420p e faststart. CRF 20 na montagem do preview; os finais anteriores em CRF 14 foram preservados.
- Texto das legendas conferido: 458 palavras, 65 entradas, até duas linhas, sem sobreposição temporal e dentro da largura segura.
- Inspeção visual de 55 instantes em sete painéis, incluindo todas as etapas alteradas e o encerramento em degradê. Verificadas 15 transições matemáticas, com movimentos de até 1,4 s e sem sequência quase estática acima de seis quadros no interior dos movimentos.
- Evidências: `qa_v4/validacao.json`, `qa_v4/painel_*.jpg`, `validar_v4_final.log`, `render_v4.log`, `render_v4_abertura.log`, `montar_v4.log`, `verificar_v4.log`.

## Teste do arsenal e entrega

`liquido_rotacao` reutilizado em 540×960, 24 amostras, a partir dos caches V2 existentes. Nenhum render Blender adicional. Setor translúcido preservado, sem tracers; o retângulo em órbita é a representação didática do elemento isolado, com seus vetores. Álgebra e anotações permanecem Manim 2D.

Saídas: `preview_v4_legendado.mp4` e `preview_v4_sincronizado.mp4`, na pasta da unidade. A voz mantém os tempos aprovados, estimados por pausas/frases, sem alinhamento fonético automático. Esta entrega é preview de revisão visual; os masters anteriores e a pasta oficial de postagem permanecem preservados. Nenhuma publicação, capa nova, commit ou push.
