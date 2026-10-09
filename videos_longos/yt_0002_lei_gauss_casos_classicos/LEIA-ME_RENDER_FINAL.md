# yt_0002 — handoff para o render final (Codex)

Tudo o que dependia de decisão editorial e de sincronização **já está pronto e sincronizado com a voz final (v2.2)**. O que falta é **só o render 1080p, a junção com a voz e a entrega**.

## Estado (verificado)

- **Vídeo:** `LeiGaussCasosClassicos002` em `cena.py`, **versão 2D fechada** (sem a parte 3D/Blender; esses experimentos são separados). Duração sincronizada: **957,9 s (15:58)**.
- **Voz:** 4 WAV do ElevenLabs em `audio/partes/narracao_parte{1,2,3,4}.wav` (243,8 + 214,9 + 238,3 + 254,1 s; ~3,0 palavras/s). **Fora do Git** (`.gitignore` ignora `videos_longos/*/audio/`). Texto falado: `texto_narracao.txt` e `texto_narracao_bloco1..4.txt` (2.862 palavras; Markdown canônico: `narracao_sugestao.md`, v2.2). A voz antiga (12:56) está em `audio/partes/_v2.1_12min/`.
- **Sincronização** (sem ASR, mesmo método do yt_0001): `gerar_sync.py alinhar` → `audio/narracao_final.wav` (953,8 s) e `sync.json` (palavras, pausas e 88 nós `[tempo editorial, tempo da voz]`, um por linha do roteiro). A cena converte cada `at(t)` editorial pelo mapa linear por partes desses nós.
- **Ritmo:** `ritmo.json` (40 trechos comprimidos onde a animação não cabia na fala) e `pads.json` (**4 esperas pedidas à voz, +2,99 s**: um silêncio de 0,84 s antes da primeira palavra, 0,15 s em 17,4 s e os **2,0 s de silêncio antes do CTA**).
- **Áudio de montagem:** `audio/narracao_montagem.wav` (**956,81 s**: fala intacta + as esperas). Fora do Git.
- **Legenda:** `legenda.srt` (**301 cues**, até 2 linhas de 42 caracteres, no tempo do vídeo final, sem sobreposição, maior cue 5,2 s). Arquivo separado para subir no YouTube (**não embutida**, como no yt_0001).
- **Capítulos:** `capitulos_youtube.txt` (16 capítulos, derivados de `blocos.json`). `blocos.json`: início de cada bloco no vídeo final e `fim` = 957,9 s.
- **Teste prévio:** o bloco 27 foi renderizado em 1080p/30 fps/CRF 14 com o `render_final.py`: 1920×1080, H.264, duração exata esperada. O pipeline de grupos paralelos, CRF e contagem de quadros está validado.

## O que o Codex precisa rodar (nesta ordem)

1. **Conferir os artefatos** (só leitura):
   ```bash
   uv run --no-sync python -c "import json;d='videos_longos/yt_0002_lei_gauss_casos_classicos/';p=json.load(open(d+'pads.json'))['pads'];b=json.load(open(d+'blocos.json'));print(len(p),'esperas',round(sum(x for _,x in p),2),'s; fim',b['fim'],'s')"
   ```
   Esperado: `4 esperas 2.99 s; fim 957.9 s`.

2. **Render final em grupos paralelos + junção + voz** (um comando):
   ```bash
   uv run --no-sync python videos_longos/yt_0002_lei_gauss_casos_classicos/render_final.py --grupos 6
   ```
   - Renderiza `1920×1080`, `30 fps`, `crf 14` (variável `CRF=14` já tratada pela cena), cada grupo de blocos com `SO=...` e `--media_dir` próprio em `renders/yt_0002_final/gN/`.
   - Junta os trechos sem recompressão (`montar_final.py`; para se os parâmetros do H.264 diferirem) e muxa `audio/narracao_montagem.wav` em AAC 320 kbit/s.
   - Saída: `renders/yt_0002_final/master_yt0002.mp4`.
   - Se um grupo falhar: `renders/yt_0002_final/gN.log`; corrigir e repetir só a junção com `--montar-apenas`.

3. **Verificar** o master:
   - vídeo ≈ **957,9 s** e áudio ≈ **956,8 s** (o vídeo termina ~1,1 s depois da voz, de propósito);
   - 1920×1080, 30 fps, H.264 + AAC;
   - quadros em instantes-chave e texto da cena batendo com a fala. Instantes de referência no vídeo final: início de cada capítulo em `capitulos_youtube.txt`; por exemplo, a fala "o campo vale sigma sobre duas vezes épsilon zero" cai em ~07:21 (capítulo "Folha infinita", 06:08–07:41) e a fala do CTA ("No próximo vídeo de Gauss…") começa em ~15:43.

4. **Entrega** (regra do repositório, `docs/entregas.md`): copiar para `entregas/` com `videos/entregar.py` (vídeos longos usam `yt0002`). Acompanham o master: `legenda.srt` (arquivo separado) e `capitulos_youtube.txt`. Informar o caminho da pasta em `entregas/` no relatório.

## Se algo mudar (texto, cena ou voz)

```bash
# 1) alinhar a voz (se o texto ou os WAV mudarem): gera audio/narracao_final.wav e sync.json
uv run --no-sync python videos_longos/yt_0002_lei_gauss_casos_classicos/gerar_sync.py alinhar
# 2) passada a seco que recalcula ritmo.json (só o fps importa: 30)
AJUSTAR=1 SO=99 uv run --no-sync python -m manim -r 960,540 --fps 30 --disable_caching --media_dir media/yt0002_sync videos_longos/yt_0002_lei_gauss_casos_classicos/cena.py LeiGaussCasosClassicos002
# 3) outra passada a seco: grava pads.json e blocos.json com o ritmo novo
SO=99 uv run --no-sync python -m manim -r 960,540 --fps 30 --disable_caching --media_dir media/yt0002_sync videos_longos/yt_0002_lei_gauss_casos_classicos/cena.py LeiGaussCasosClassicos002
# 4) áudio de montagem, legenda e capítulos
uv run --no-sync python videos_longos/yt_0002_lei_gauss_casos_classicos/gerar_sync.py montar
uv run --no-sync python videos_longos/yt_0002_lei_gauss_casos_classicos/gerar_capitulos.py
```
(Cada passada a seco leva ~10 min e não gera vídeo. No Windows, definir `PYTHONIOENCODING=utf-8` evita erro de codificação nos logs.)

## Cuidados

- **Qualidade:** padrão único CRF 14 (AGENTS.md, "Qualidade de render e codificação"). Em 1080p o `template/qualidade.py` já aplica CRF 14 sozinho; este roteiro também passa `CRF=14` explicitamente. Conferir o master: `crf=14.0` no stream.
- O fps do render final **precisa** ser 30: ele define a contagem de quadros que mantém vídeo e voz sem deriva.
- `SEM_VOZ=1` faz a cena rodar como o preview sem voz (18:01), útil só para comparar.
- O `cena.py` sem sincronização (preview 18:01, sem voz) está no commit `c38ba17` (`git show c38ba17:videos_longos/yt_0002_lei_gauss_casos_classicos/cena.py`). A alteração atual é só o mecanismo de ritmo (`voz`, `at`, `_tocar`, `begin`, `respiro`, CRF/`_qualidade_final`), sem mexer nas animações.
- Não rodar renders de grupos diferentes na **mesma** `--media_dir` (colidem); o script já usa uma por grupo.
- Os WAV e `narracao_montagem.wav` estão fora do Git; se o Codex rodar em outra máquina/checkout, copiar `audio/` junto.
- Nada desta pasta foi commitado depois do commit `c38ba17`.

## Como o ritmo funciona (resumo)

A voz (15:51) é mais curta que o orçamento editorial original (18:01), então a cena converte cada marco editorial no instante da fala correspondente, comprime animações (até 62% da duração) e esperas (até 40%) onde a fala é mais curta, e só pede silêncio à voz onde ainda não cabe (4 esperas, +2,99 s). Se, ao assistir, algum trecho parecer apressado, o ajuste é regerar o bloco correspondente no ElevenLabs mais lento (ou acrescentar uma frase) e refazer os passos de "Se algo mudar".
