# Conteúdo nulo e integrabilidade

- **ID:** `yt_0031`
- **formato:** `longo_horizontal`
- **tipo:** `teoria_visual`
- **Série pública:** **CÁLCULO III · EP. 06**
- **disciplina:** `Cálculo III`
- **modulo:** `3.2 Integrais duplas` (o `docs/mapa_curricular.md` do repositório ainda usa a numeração antiga)
- **bloco:** `3.2-T2`
- **referencia:** Guidorizzi, Um Curso de Cálculo, vol. 3, §2.3, §2.4 e Apêndice B — só na descrição do YouTube; nada de livro na tela nem na fala.
- **título:** Conteúdo nulo e integrabilidade
- **unidades:** x e y em metros; densidade em kg/m²; massa em kg
- **solido_3d:** nenhum do arsenal Blender (caixinhas e tampas são prismas retos, feitos direto em Three.js como no EP. 05)
- **3d_threejs:** `b13` (prédio por baixo + tampas, x² + y², n = 4; estados `afunda`, `tampas`, `cresce`, `chao`; lotes PB1 e PB6), `b21` (dois metais, n = 16,
  muro de tampas na solda; `cresce`, `muro`; lotes PB2 e PS), `b52` (quarto de disco com f = 1 estendida por zero; `cresce`, `muro`; lotes PB5 e PB6). O `b21s` (n = 64, opcional) não foi usado.
  Porte exato de `referencia/c3d31.html` em `threejs/cena3d/c31.js` (uma página por cena); a câmera vai no estado de cada quadro.
- **duracao:** 20:11,07 (master 1080p30) = voz 20:10,08 (ElevenLabs v4, narração v2.3, 3.612 palavras, 2,98 palavras/s) + 1 s de cauda
- **Status (2026-11-13):** FINAL (handoff `handoff_final.md`): correções F1–F11, narração v2.3, voz, sincronização no tempo real da voz, `legenda.srt`,
  master 1080p30 CRF 14 em `renders/yt_0031_master_final_1080p30.mp4`, capítulos em `renders/capitulos_final.txt`; entrega em `entregas/`. Sem capa, commit ou push.
- **final:** QA com R5 a cada 0,2 s inclusive glifos em trânsito (`_r5b`) e glifos embolados por quadro (`_embolado`); voos por rota (`via_px`/`via_tfc`);
  pipeline de voz `gerar_voz_elevenlabs.py` → `alinhar_voz.py --stt` → `gerar_ancoras.py` (voz real) → `seco.sh` + `ritmo31.py` → `render_todos.sh` →
  `qa_sync.py` → `render1080_todos.sh` → `montar_final.py` → `montar_master.py`; `gerar_srt.py`, `capitulos.py`, `qa_voz.py`, `qa31f.py`, `qa_al1080.py`, `stills_final.py`.
- **quadros_alvo:** `yt_0031_quadros_alvo_v3` (os 31 do v2 + 21b, 23b, 28a) em `referencia_v3/`; v2 em `referencia_v2/`, v1 em `referencia/`
- **sistema_visual:** fundo violeta liso `#18143A → #0F0C26` (`assets/calculo/papel.py`, `_arq()`) + grade `#2B2558` de 0,25 m (60 px) que nasce
  dos eixos da chapa (canto (0, 0) em (360, 780) px, 240 px/m); sem grade nas cenas 3D e nos cartões
- **canto:** linha 1 `CÁLCULO III · INTEGRAL DUPLA`; linha 2: `PISO, TETO E TAMPAS`, `A CHAPA DE DOIS METAIS`, `CONTEÚDO NULO`,
  `CURVAS TÊM CONTEÚDO NULO`, `FRONTEIRA`, `CONTINUIDADE UNIFORME`, `O TEOREMA`, `QUANDO FALHA`, `NUM EXERCÍCIO`, `SÍNTESE`. H, A e S2 sem canto.
- **ordem:** H → A → B1 → … → B9 → S (lotes `PH`, `PA`, `PB1`…`PB9`, `PS`)
- **preview v3 (histórico):** preview visual silencioso v3 (handoff v3 `yt_0031_v2_avaliacao_e_handoff_v3.md`, 2026-11-13) em `renders/v3/` (20:10,27; cortes por bloco em `renders/v3/blocos/`); v2 em `renders/v2/`, v1 em `renders/v1/`. Sem voz, SRT, 1080p, master, entrega ou commit.
- **v3:** frase nova no B7-2 (`narracao.md`); B7-2 com as escolhas de ε e os cancelamentos (`\cancel`, mapas 3a–4d), B6-3 com a figura da contradição, B9-1 com as perguntas grandes; mapas com saída antecipada (`cedo=True`: `FadeOutCedo`/`CanetaTarde`); R5 com espessura do traço, grade grossa e recorte de imagem; `qa31v3.py` (+ `--extra`: cortes e costuras), `cadeia_v3.sh [lotes]`.
- **v2:** MF-Tools `TransformByGlyphMap` de verdade (`B31.tbgm`, `CombineTex`, caneta como introdutor); R5 ampliado amostrado no render; parados (G3), começo de bloco (G2), glyph maps e origens em `qa31v2.py`; ritmo por trecho em `ritmo31.json` (`seco.sh` + `ritmo31.py`; refazer depois de mudar a ordem das animações de um lote); `cadeia_v2.sh` roda tudo.

## Arquivos
- `yt_0031_handoff_v1.md`, `yt_0031_narracao_v2.md` — handoff e narração aprovada (cópias)
- `narracao.md` (Anexo A) → `gerar_ancoras.py` → `ancoras.json` (tempos estimados, 3 palavras/s)
- `kit.py` — cópia do kit do yt_0028 (relógio por quadro, âncoras `an`/`gat`, caneta, portão FLASH, `Fundo3D`); mudou o título do canto
- `v31.py` — peças desta unidade: texto/fórmula/placa (copiados do v28), chapa e mapas por numpy, solda, câmera do three.js em Python
  (`proj3d`, `cam_pouso`), `Palco3D` (estados + rótulos presos), `entra3d`/`sai3d` (pousos), `B31.tbgm` (MF-Tools; o `mapa_glifos` do v1 foi aposentado), `B31` (caneta rápida, voos,
  sublinhado de leitura, marcas dos alvos, QA R5)
- `sec_h.py`, `sec_a.py`, `sec_b1.py` … `sec_b9.py`, `sec_s.py` — um lote por bloco; `cena.py` registra os lotes
- `render.sh` (540p15), `render3d.sh` (passagem seca → `threejs/pedidos3d` → `node threejs/r3d.js` → render), `render_todos.sh` (3 em paralelo),
  `still.sh`, `montar.py` (concatena), `comparar.py` (prancha render × alvo), `qa31.py` (relatórios)
- `threejs/` — `r3d.js` e `package.json` do yt_0027/yt_0029 (playwright-core via `NODE_PATH` do yt_0020), `cena3d/` (`c31.js`, `b13/b21/b52.html`,
  `three.min.js` r128), `fixos/` (quadros 1080p do muro e do prédio, para miniaturas)
- `verificacao/` — script sympy do handoff (o sympy não está na `.venv`; não instalado) e `verifica_numeros_numpy.py` (13/13 True)
- `referencia/` — cópia de `yt_0031_quadros_alvo_v1/`
