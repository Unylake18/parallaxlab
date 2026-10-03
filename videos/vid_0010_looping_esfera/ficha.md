# vid_0010 — Esfera maciça rolando num looping

- Série pública: **EXERCÍCIO RESOLVIDO · EP. 04**.
- **Concluído tecnicamente em 2026-10-01: voz, sincronia por âncoras, legenda e master gerados; aprovação humana do vídeo final, capa e publicação pendentes.**
- Pergunta: qual a altura mínima para uma esfera maciça completar um looping? Partícula (5/2 do raio) → esfera (27/10 do raio), com o momento de inércia derivado por discos finos.
- Cena: `cena.py`, classe `LoopingEsfera010` (módulo único; helper `Eq` local para os mapas de glifos do MF-Tools 1.4.9). Modelo: trajetória do CM de raio R; pista física R + a (a/R = 0,12); rolamento sem deslizamento; um único parâmetro de arco `s` comanda posição, giro, vetores, barra e gráfico de energia.
- Final: `renders/vid_0010_looping_esfera_final_master_limpo.mp4` e `..._final_legendado.mp4` — 1080×1920, 30 fps, 5.048 quadros, 168,25 s; AAC 168,24 s. Sem âncora atrasada (`SYNC atraso`: 0).
- Narração: `audio/narracao_final.wav` (ElevenLabs, 168,24 s, estéreo 44,1 kHz, intacta; texto em `texto_narracao.txt` e `roteiro.md`). `gerar_sync.py` alinha o texto ao WAV (sílabas + pausas medidas, programação dinâmica por ritmo de frase; sem ASR) e gera `sync.json` (50 âncoras + 4 instantes extras do fecho) e `legenda.srt` (71 cues). `native.json` guarda o tempo nativo de cada âncora. Refazer só se a cena ou o áudio mudarem:
  `uv run python videos/vid_0010_looping_esfera/gerar_sync.py` e
  `SYNC_CAL=1 uv run python -m manim -r 108,192 --fps 15 videos/vid_0010_looping_esfera/cena.py LoopingEsfera010`.
- Comandos: `uv run python -m manim -r 1080,1920 --fps 30 videos/vid_0010_looping_esfera/cena.py LoopingEsfera010`; `videos/montar_master.py` (render + WAV); `videos/montar_legendado.py … --color-module videos/vid_0010_looping_esfera/cena.py`.
- Legenda: largura ≤ 440 px (a 540), 2 linhas, cues de 0,8–3,6 s; cores de `SUBTITLE_TERM_COLORS` (velocidade/translação ciano; rotação/momento de inércia magenta; altura/potencial violeta; normal azul claro).
- Cores da cena: azul = pista/geometria e normal; ciano = velocidade e translação; magenta = rotação e momento de inércia; violeta = energia potencial e altura; branco = texto, equações e energia total.
- Replay: enquanto a conta está aberta (caso clássico, altura da partícula, energia da esfera, volta à energia, altura da esfera), o corpo repete a descida e a subida até ~137° e some por fade (nunca chega ao topo); ao sair cada resultado ele faz uma corrida completa. Detalhes no próprio `cena.py` (`drive`, `replay_on`, `replay_off`).

## Sincronia: o que foi comprimido

A cena tem 164,5 s em tempo nativo e a voz 168,24 s; o motor (`ancora`) escala `play`/`wait` entre âncoras (0,45–2,0×) e segura o último quadro quando sobra tempo. Trechos mais apertados (≈0,5–0,6×): cinco meios (partícula), integral e massa total (I_CM), `27/10` e a subida de 2,5 para 2,7 (esfera). Para caber, a corrida da partícula usa 0,62× da escala física e a corrida final da esfera divide o tempo com o fecho. Nenhum passo físico foi removido.

## Pendências

- Aprovação humana do vídeo final; capa; `publicacao.md`; `revisao.md`; publicação não registrada.
- O título de abertura diz "LOOP" e a voz diz "looping" (decisão de texto de tela mantida).
