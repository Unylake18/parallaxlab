# Teste VoiceStudio × ElevenLabs — relatório (2026-11-16)

Pasta: `K:\PycharmProjects\manim-fisica\experimentos\voz_voicestudio\` (não rastreada; nada no Git, nada na `.venv` do projeto).

## Resumo
1. Na RTX 2060 (6 GB), o **OmniVoice** é rápido: o trecho A (≈62 s) sai em **15–19 s** (RTF 0,23–0,31). Mas os pesos são **CC-BY-NC**, então ele não serve para o canal.
2. O **VoxCPM2** (Apache-2.0, o candidato real) lê tudo certo, mas aqui é **lento demais**: RTF **13–29**, ou seja, **15–32 min** para cada 1 min de fala. O modelo usa 6,2–6,8 GB de VRAM e transborda para a RAM. Pelo app, ele estoura o limite de 900 s e é abandonado.
3. A pronúncia, conferida por transcrição (não por ouvido), saiu certa em todos os motores: épsilon, delta, "zero vírgula quatro um" (e 0,7 / 0,21 / 0,10), téta, x, y, "C um" e R.
4. O **WhisperX do app dá timestamps por palavra**. No A_elevenlabs, contra o alinhamento original do yt_0028, o erro de início é de **13 ms na mediana e 28 ms no p90**: serve para a sincronia sem o ElevenLabs.
5. Falta **ouvir** os arquivos: timbre, entonação de professor e semelhança do clone com a voz Dioke só se julgam de ouvido. Comece por A_elevenlabs × A_voxcpm2_clone × A_omnivoice_clone.

## Hardware (medido)
- GPU NVIDIA GeForce RTX 2060, **6 GB VRAM** (driver 616.92, arquitetura sm_75 Turing, sem bfloat16 nativo)
- CPU Intel Core i5-10400F · RAM 31,9 GB · disco livre no início: C: 48,9 GB, K: 219,3 GB

## VoiceStudio: versão e instalação
- **v0.5.8** (release de 12/11/2026), `VoiceStudio-0.5.8-win-x64.exe` (232,8 MB). Instalado pelo script oficial `install.ps1` (lido antes de rodar), com SHA256 conferido, em `%LOCALAPPDATA%\Programs\VoiceStudio`. O setup adicionou ao PATH do usuário só a pasta do CLI do próprio app (`resources\cli`); não mexeu no Python global.
- O primeiro setup do backend só sai por um botão na janela do app. A permissão para controlar essa janela foi negada (não havia ninguém no PC), então montei o backend **sem a janela**, replicando o que o setup faz: copiei o projeto empacotado para `K:\VoiceStudio_runtime\project` e rodei `uv sync --frozen --no-dev --managed-python --python 3.11` com o `uv` e o `uv.lock` do próprio app. Isso gerou um runtime de 5,5 GB, com torch 2.10+cu128 e CUDA ok. Acrescentei o pacote de compatibilidade cuDNN 8 que o setup oficial também instala (`nvidia-cudnn-cu12==8.9.7.29` em `cudnn8_compat`), sem o qual o WhisperX não sobe.
- O backend roda em `127.0.0.1:3907` com `OMNIVOICE_DATA_DIR`/`OMNIVOICE_CACHE_DIR` no K: (modelos: OmniVoice 2,3 GB + tokenizer 0,8 GB, VoxCPM2 4,7 GB, Whisper large-v3 2,9 GB, wav2vec2-pt 1,6 GB). O VoxCPM2 foi instalado pelo instalador de motores do app, num venv próprio em `K:\VoiceStudio_runtime\data\engines\voxcpm2`.
- Licenças aceitas no app com o OK do Kaio na thread (16/11, 13:31 UTC): k2-fsa/OmniVoice (CC-BY-NC), eustlb/higgs-audio-v2-tokenizer (NOASSERTION) e openbmb/VoxCPM2 (Apache-2.0). Systran/faster-whisper-large-v3 (MIT) foi aceito dentro do "pode tudo" do Kaio para este teste.
- Observações do app: as saídas pelo `/generate` passam pelo efeito `broadcast` (padrão) e recebem **marca d'água AudioSeal** (aparece no render trace). Sem `HF_TOKEN`, os downloads do Hugging Face são lentos: os pesos do VoxCPM2 levaram 31 min.

## Motores e como cada arquivo foi gerado
| motor | modo | como |
|---|---|---|
| OmniVoice (k2-fsa/OmniVoice, CC-BY-NC) | voice design | pelo app (CLI `speak`). O design do OmniVoice só aceita atributos fixos: a descrição virou `male, young adult, moderate pitch` ("caloroso/animado/professor" não existem nesse motor) |
| OmniVoice | clone | pelo app, perfil clonado com `ref1_yt0034.wav` + ref_text |
| VoxCPM2 (openbmb/VoxCPM2, Apache-2.0) | voice design nativo | **direto pela biblioteca `voxcpm`** do venv do app (mesmos pesos e parâmetros do sidecar: cfg 2,0, 10 passos, seed 42), com a descrição livre em inglês: *Brazilian Portuguese male voice, about 30 years old, warm and energetic prep-course teacher, enthusiastic, friendly, very clear diction, native Brazilian Portuguese accent* |
| VoxCPM2 | clone (continuação) | direto, `prompt_wav` + `prompt_text` + `reference_wav` = ref1 (como o sidecar faz) |
| VoxCPM2 | clone multi | direto, referência montada com 2 vídeos (ver abaixo) |

Por que o VoxCPM2 foi gerado fora do app: pelo app, o primeiro B foi abandonado no limite de 905 s de computação (download + geração a 1,9 s por passo). O trecho A estouraria sempre. A geração direta usa o mesmo motor, mas sem o efeito broadcast e sem a marca d'água do app. O trecho A foi dividido em 3 blocos de frases (o app também divide, em blocos de até 800 caracteres), emendados com 0,25 s de silêncio. Teste de dtype numa frase: bf16 RTF 10,6 × fp16 RTF 10,0, com o mesmo pico de 5,7 GB. O gargalo é a VRAM, não o tipo numérico.

Sobre o comando `voices design` do app: com o VoxCPM2, ele não usa o design nativo. Mapeia a descrição para atributos do OmniVoice e grava um áudio de referência. Por isso descartei esse caminho.

## Referência ElevenLabs
- `A_elevenlabs.wav`: corte de `videos_longos/yt_0028_limite_continuidade_derivadas_parciais/audio/narracao_final.wav`, **139,990–201,570 s** (61,58 s), palavras 448–640 do `alinhamento_palavras.json` (193 palavras = trecho A exato).

## Referências do clone (Cálculo III; o yt_0028 ficou de fora)
Em `referencias/` (WAV + `.txt` com o ref_text exato do alinhamento; `referencias.json`):

| arquivo | origem (`videos_longos/.../audio/narracao_final.wav`) | corte (s) | duração |
|---|---|---|---|
| ref1_yt0034.wav (principal) | yt_0034_regioes_gerais_troca_ordem | 1086,86–1106,73 | 19,87 s |
| ref_multi_yt0034_yt0032.wav | ref1 + 0,35 s de silêncio + yt_0032_propriedades_integral_dupla 619,28–625,06 | — | 26,00 s |
| ref2_yt0032.wav / ref3_yt0027.wav | yt_0032 619,28–637,09 · yt_0027_rotacional_divergente 283,92–303,15 | — | 17,8 / 19,2 s (separadas, não usadas sozinhas) |

Nenhum dos motores aceita várias referências no app (o VoxCPM2 usa uma só e corta nos primeiros 30 s; o OmniVoice usa até 20 s). Por isso o "multi" é uma referência única de 26 s com trechos de 2 vídeos. O yt_0027 não coube no limite de 30 s. A autorização do clone é do Kaio: a voz "Dioke" do ElevenLabs é a voz dele (thread, 16/11, 12:46 UTC).

## Medidas (A = 193 palavras, B = 56)
| arquivo | geração (s) | duração (s) | palavras/s | RTF | sr | LUFS |
|---|---|---|---|---|---|---|
| A_elevenlabs | — | 61,58 | 3,13 | — | 44,1k | −20,6 |
| A_omnivoice | 14,5 | 61,99 | 3,11 | 0,23 | 24k | −17,7 |
| A_omnivoice_clone | 18,9 | 60,95 | 3,17 | 0,31 | 24k | −19,7 |
| A_voxcpm2 | 1142 | 61,30 | 3,15 | 18,6 | 48k | −14,7 |
| A_voxcpm2_clone | 885 | 54,58 | 3,54 | 16,2 | 48k | −20,9 |
| A_voxcpm2_clone_multi | 1048 | 55,22 | 3,50 | 19,0 | 48k | −20,7 |
| B_omnivoice | 9,6 | 16,64 | 3,37 | 0,58 | 24k | −16,0 |
| B_omnivoice_clone | 5,6 | 16,88 | 3,32 | 0,33 | 24k | −19,2 |
| B_voxcpm2 | 287 | 21,12 | 2,65 | 13,6 | 48k | −19,1 |
| B_voxcpm2_clone | 467 | 16,32 | 3,43 | 28,6 | 48k | −19,9 |

- Os tempos do OmniVoice são com o modelo já carregado. A primeira geração levou 1059 s, porque incluiu o download.
- As durações do VoxCPM2 no A incluem 2 × 0,25 s de emenda entre blocos.
- O pico de VRAM do VoxCPM2 foi de 6,15–6,77 GB, acima dos 6 GB físicos da placa.

## Pronúncia (por transcrição WhisperX large-v3, pt; não é escuta)
Todos os 10 arquivos (incluindo o ElevenLabs) foram reconhecidos com: **épsilon**, **delta**, **0,7**, **0,41** ("zero vírgula quatro um"), **0,21**, **0,10**, **θ** (téta), **x**, **y**, **C1** ("C um") e "raio **r**". O WER aproximado ficou entre 5% e 12% em todos, inclusive no ElevenLabs (11,4%); a diferença vem quase toda de números escritos em dígitos e da pontuação.

Desvios que a transcrição mostrou (vale ouvir esses pontos):
- A_elevenlabs: "cabe no disco **Y**" (o épsilon soou ambíguo para o ASR) e "Δ".
- A_omnivoice: "Diminui o **tau**" (delta) e "Achou isso que existe delta, quer dizer" (entonação de pergunta).
- A_omnivoice_clone: "raio, **delta E**", "uma **vancha**" (mancha).
- A_voxcpm2: "Achou? É isso que existe delta? Quer dizer..." (entonação de pergunta onde é afirmação).
- A_voxcpm2_clone: limpo.
- A_voxcpm2_clone_multi: trocou "para" por "**pra**" (3×) e inseriu "Com **um** delta".
- B_omnivoice_clone: "derivadas **parsis**".

## Timestamps por palavra (WhisperX no app)
- Funciona pelo endpoint `POST /v1/audio/transcriptions` (`response_format=verbose_json`, `timestamp_granularities[]=word`), com WhisperX + alinhamento forçado wav2vec2 em português (`jonatasgrosman/wav2vec2-large-xlsr-53-portuguese`). O modelo baixou para int8_float16 porque a VRAM livre estava no limite.
- `A_voxcpm2_palavras.json`: 183 palavras com `start`/`end` (formato igual ao `alinhamento_palavras.json`). As transcrições completas de todos os arquivos estão em `transcricoes/`.
- **Precisão medida** no A_elevenlabs contra o alinhamento original do yt_0028: 171/193 palavras casadas; erro de início médio de 19 ms, **mediana de 13 ms, p90 de 28 ms**, máximo de 553 ms (um caso isolado).
- Tempo: 4–22 s por arquivo. A primeira transcrição estourou o limite de 300 s na carga a frio e passou na segunda tentativa.

## Conclusão prática (sugestão, não decisão)
- **VoxCPM2 nesta máquina:** inviável para produção (≈20× o tempo real; um longo de 20 min levaria ~7 h só de voz). Só vira opção com uma GPU de ≥12 GB (ou GPU alugada). A qualidade de leitura dele foi a mais limpa do teste; falta o Kaio julgar o timbre.
- **OmniVoice:** rápido e com leitura boa, mas é **não comercial**. Não serve para o canal monetizado.
- **WhisperX:** dá para usar já, independentemente do TTS, para gerar o `alinhamento_palavras.json` de qualquer voz.

## Arquivos
- Áudios: `A_*.wav`, `B_*.wav` (10 arquivos). O `B_omnivoice_frio` saiu idêntico ao `B_omnivoice` (seed 42) e foi apagado.
- `A_voxcpm2_palavras.json`, `transcricoes/*.json`, `referencias/`, `trecho_A.txt`, `trecho_B.txt`, `teste_dtype/` (frase bf16 × fp16).
- `logs/` (medidas.txt, analise.txt, analise_asr.json, logs de instalação e geração).
- Fora do repositório: `K:\VoiceStudio_runtime\` (≈34 GB: runtime, motores, modelos e caches). Parei o backend no fim do teste, e a GPU ficou livre. Para subir de novo: `cd K:\VoiceStudio_runtime\project\backend` e rodar `..\.venv\Scripts\python.exe main.py` com `OMNIVOICE_PORT=3907`, `OMNIVOICE_DATA_DIR=K:\VoiceStudio_runtime\data` e `OMNIVOICE_CACHE_DIR=K:\VoiceStudio_runtime\cache`. Para desinstalar: "Uninstall VoiceStudio" e apagar `K:\VoiceStudio_runtime`.
