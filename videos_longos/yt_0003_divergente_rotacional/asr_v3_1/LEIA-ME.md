# Transcrição ASR independente — yt_0003 (áudio do preview com voz)

- **Áudio transcrito:** `audio/narracao_montagem.wav` (o mesmo áudio do `preview_v3_1_com_voz.mp4`; 1484,56 s). Original preservado, nada foi alterado.
- **Modelo:** `large-v3` (Systran/faster-whisper-large-v3), faster-whisper 1.2.1 + ctranslate2 4.8.3, GPU local (RTX 2060 6 GB), `float16`. Processamento: 146,7 s. Nenhum áudio saiu do computador (só o modelo foi baixado, ~3 GB).
- **Configuração:** `language="pt"` (detecção confirmou pt, prob 1,0), `beam_size=5`, `word_timestamps=True`, `vad_filter=False`, `condition_on_previous_text=False`, `temperature=0.0`, `no_speech_threshold=0.6`, `compression_ratio_threshold=2.4`. **Sem `initial_prompt`**: o texto V3.1 não foi usado para guiar o reconhecimento.
- **Ambiente isolado:** venv fora do repositório (scratchpad da sessão); `.venv`, `pyproject.toml` e `uv.lock` do projeto não foram tocados. Pacotes: faster-whisper, nvidia-cublas-cu12, nvidia-cudnn-cu12, `av<17` (a versão 19 era incompatível).
- **Correções de termos técnicos:** nenhuma foi aplicada (a transcrição está como o modelo reconheceu).
- **Arquivos:** `transcricao_asr.json` (358 segmentos, 4.083 palavras com `start`/`end`/`prob`), `transcricao_asr.srt` (por segmento), `comparacao_asr_vs_estimado.json`, `transcrever_faster_whisper.py`.

## Verificação (ASR × tempos estimados por pausas, `timestamps_gpt/`)
- 4.008 de 4.118 palavras do texto V3.1 casaram com o ASR (**97,3%**): o que foi pronunciado corresponde ao roteiro.
- Offset de início por palavra (estimado − ASR): mediana **+0,19 s** (o estimado é um pouco mais tardio; início de palavra do Whisper tende a ser adiantado), p10 −0,02 s, p90 +0,40 s. |d| < 0,3 s em 79,4%; < 0,5 s em 94,9%; > 1 s em 1,2%.
- Blocos (âncoras) com início estimado errado em mais de 0,5 s: **D12** (+1,47 s: a fala começa ~1,5 s antes do estimado), **K01** (+1,55 s, idem), **F01** (−0,59 s: a fala começa ~0,6 s depois do estimado). Os outros 89 ficaram dentro de 0,5 s.
- Amostras conferidas: **início** (H01: offsets −0,17 a +0,16 s nas primeiras palavras), **delta de Dirac** (P06 −0,01 a +0,35 s; P08 +0,08 a +0,35 s), **final** (CTA02 +0,14 a +0,29 s).
- Os tempos do ASR também têm imprecisão (tipicamente décimos de segundo); `prob` por palavra está no JSON.
