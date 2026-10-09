# Torricelli: onde furar para o jato ir mais longe

- ID: `vid_0016_torricelli_alcance`
- formato: `curto_vertical`
- Série pública: **DA EQUAÇÃO AO FENÔMENO · EP. 05**.
- solido_3d: `tanque_torricelli` (aprovado; estilo de jato 1, `voltas_jato`), sequências do Blender via `ponte.py`.
- Cena: `Vid0016` em `cena.py` (versão sincronizada com a voz); a linha do tempo silenciosa anterior está em `cena_silencioso.py`.

## Física (congelada)

Bernoulli entre a superfície e o furo → `v = √(2g(H−y))`; queda livre com `v_y(0) = 0` → `t = √(2y/g)`;
alcance `x = v t = 2√(y(H−y))` (a gravidade cancela no modelo ideal); normalizado `x/H = 2√(u(1−u))`, `u = y/H`,
que é um semicírculo `(2u−1)² + (x/H)² = 1`. Máximo em `u = 1/2`, com `x_max = H`; `u = 0,2` e `u = 0,8` têm o mesmo alcance.

## Entrega

- Voz: `audio/narracao_final.wav` (154,24 s); montagem com 1,1 s de silêncio antes e 0,8 s depois: `audio/narracao_montagem.wav`.
- Texto da voz: `texto_narracao.txt` (459 palavras); sincronia por `gerar_sync.py` (`palavras_tempos.json`, `sync.json`), legendas em `legenda.srt`
  (cores das grandezas em `legendas_cores.py`).
- Final 1080×1920 / 30 fps, 156,2 s: `renders/vid_0016_torricelli_alcance_postagem_master.mp4` e `..._postagem_legendado.mp4`
  (a tag "· EP. 05" foi aplicada com `patch_tag_ep.py`; a `cena.py` já sai com ela). Cópias organizadas: `entregas/`.
- Sequências do Blender do final em 1296×2304, 30 quadros/s (comandos no fim da `cena.py`).
- Capa escolhida: `capa_instagram.png` ("DOIS FUROS, UM MESMO ALCANCE", 941×1672); as dez propostas geradas por `gerar_capa.py` foram descartadas.
