# yt_0018 — versão final (1920×1080 / 30 fps, H.264 CRF 14, voz contínua)

Entrega: `entregas/Vídeos Longos/Mecânica - Momento - Exercícios de centro de massa/` (master, legenda .srt, capítulos, audio/, texto/, manifesto; sem capa, não pedida).
Master: `master - yt0018.mp4` — **849,73 s (14,16 min)**, 25.492 quadros, 227 MB, CRF 14.0 conferido no stream, áudio AAC 192 kb/s mono 44,1 kHz.

## O que mudou desde o v7 intermediário (por causa do seu retorno)
- **Chiado no áudio:** era a cama de ruído rosa que eu tinha posto a −54 dBFS sob a voz inteira, para zerar as auditorias de silêncio. Retirei. Agora o piso é o natural da voz (mediana −59,5 dBFS) mais um dither de −76 dBFS, e as bordas abruptas são tratadas por rampas de 20 ms. VOZ CONTÍNUA 0, BORDA ABRUPTA 0 (maior salto 31,9 dB), 3 junções (crossfade 25 ms, 0,34 s).
- **Quadros piscando:** removi todos os realces ciano, os pulsos de opacidade e os `Indicate` de enchimento. Nada mais pisca.
- **No lugar deles, escrita nova alinhada com a fala:** 125 anotações curtas em 32 âncoras (`notas18.py`), que nascem na palavra, ficam até 2,1 s e saem em fade; o lugar é escolhido quando nascem (primeiro candidato que não encosta em nada). Só repetem o que a voz acabou de dizer. No CTA final, ondas que se expandem a partir do logo, presas ao relógio da cena.

## Verificações (no preview 960×540/15 fps, que é onde as auditorias rodam)
- ATRASO dos gatilhos (−0,15…+0,20 s): 94 gatilhos, 0 fora, maior atraso +0,01 s, maior adiantamento −0,14 s.
- G28: portão aberto com 7 justificativas (amostras únicas em transição: TRÂNSITO ×2, FORA DA MARGEM, PALCO 3D, 3D × TEXTO, ENCOSTADO, FORA DA ZONA). Zerados: TEXTO SOBRE OBJETO/CAIXA, SOBREPOSIÇÃO, SELO DUPLO, LINHA ÓRFÃ, FUNDO 0%, VAZIO 0, BALANÇA (≤ 0,041 kg), alinhamento Three.js × Manim 0,000 px, GAFANHOTO × FÍSICA ≤ 0,18 px, água/lua OK.
- Congelamento (freezedetect n=0,0005, d=1,5 s, com fala): **12 trechos, 19,2 s (2,3%), maior 1,9 s** (v6: 97 trechos, 235,6 s, maior 6,4 s). Gafanhoto parado no ar: 0. Pausas ≥ 4 s: 0. Os 12 restantes são de 1,5 a 1,9 s.

## Render final
- 7 lotes em 1920×1080 / 30 fps, em paralelo de dois (três ao mesmo tempo estouraram a memória e dois lotes caíram; foram refeitos). 3D: pedidos a 30 fps → Three.js em 1920×1080 (PH 1.613, PX3 6.759, PX2 819 quadros renderizados mais cópias; ~0,1–0,2 s/quadro). Duração de cada lote igual ao esperado pela voz (PH 82,33 · PX0 112,2 · PX2 89,0 · PX3 225,27 · PX4 96,27 · PX5 138,47 · PEP 106,2 s). Master montado por `montar_final.py` (emenda com fundo de 10 quadros entre lotes) e voz por `montar_audio.py` (pacotes de vídeo copiados, sem recodificar).
- **Limite honesto:** as auditorias de tela (G28, congelamento) rodaram no preview, não no 1080p. O detector de congelamento é calibrado para 540p direto e **não vale no 1080p decimado** (dá 79 trechos porque o ruído de render do 540p inflava a diferença entre quadros). Conferi à parte que preview e final mudam a mesma quantidade de pixels em trechos de 3 s (2,1% × 2,0%), mas não rodei o portão G28 sobre o 1080p.
- Três anotações do CTA (823, 827 e 828 s) continuam sem lugar livre e não aparecem.

## Não feito / pendências
- **Escuta:** eu não ouvi os takes. Pronúncia, tags lidas em voz alta e ritmo ficam para a sua escuta (nada foi regerado: 14.754 caracteres de crédito).
- Do §3 do handoff v7: A2, A4, X2-2/X2-4 (cubo girando, cota que cresce) e X5-6/X5-7 ficaram com o plano() e as anotações genéricas, sem o movimento específico.
- Capa: não pedida, não feita.
- Nada foi commitado.

## Arquivos
Novos: `notas18.py`, `montar_final.py`, `render_f1080.sh`, `entregar_yt0018.py`, `renders/relatorio_final.md`, `renders/master_yt0018_1920x1080.mp4`. Alterados: `kit.py` (anotações, `FPS_RENDER`), `prob2.py` (pulsa/wait sem realce), `unir_voz.py`, `montar_audio.py`, `sec_fim.py`, `sec_x*.py`, `sec_hook.py`, `gerar_srt.py`. Backups de pedidos 15 fps em `threejs/pedidos3d/_15fps/`.
