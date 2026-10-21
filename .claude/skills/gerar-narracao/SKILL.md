---
name: gerar-narracao
description: Escreve a fala (estilo professor de cursinho, audio tags [ ] do ElevenLabs v4) e gera a narração com a voz e o modelo fixos do projeto. Usar só quando o usuário abrir a fase de voz ou pedir roteiro com tags, teste de tags (respiração, pausa) ou geração de narração.
---

# Gerar narração (ElevenLabs v4)

Fase de voz: só execute quando pedida. Referência completa: `docs/roteiro_voz_elevenlabs_v4.md` (leia ao escrever a fala ou ajustar tags).

## Configuração fixa
- Voz: `qw7jgPZWOKrl10GsjQ82` · Modelo: `eleven_v4` (nunca `eleven_v4_turbo`).
- Stability/Similarity no padrão. Style e Speed não existem no v4.
- Formato `mp3_44100_192` → WAV mono 16 bits 44,1 kHz.
- A chave vem só de `ELEVENLABS_API_KEY` (ambiente). Nunca em arquivo, commit ou chat.

## Caminho oficial (narração completa)
1. Roteiro limpo → cópia `narracao_tags*.md` com a seção `## Texto corrido (para gravação)`.
2. Simular sem gastar crédito: `uv run --no-sync python videos/gerar_voz_elevenlabs.py ARQ.md SAIDA.wav --voz qw7jgPZWOKrl10GsjQ82 --secao "## Texto corrido (para gravação)" --seco`
3. Mostrar os blocos ao usuário e **pedir confirmação antes de gerar** (gasta crédito).
4. Gerar com outro nome (`audio/narracao_v4.wav`); nunca sobrescrever `narracao_final.wav` de vídeo fechado.
5. Ouvir, ajustar tags, regerar só o necessário; promover depois.

## Uso do MCP `elevenlabs` (testes e trechos soltos)
Sempre passar explicitamente `voice_id` `qw7jgPZWOKrl10GsjQ82` e `model_id` `eleven_v4`; o padrão do MCP pode ser um modelo antigo que ignora as tags. Não passar style/speed. Salvar em `renders/elevenlabs_mcp/`. Confirmar antes de cada geração.

## Regras de tags
Uma tag por frase, descritivas, em inglês, fora da legenda e do `.srt`. Base `[thoughtful]`/`[curious]`; `[excited]` só na descoberta; sem postura/música/efeitos. Pausa: `[short pause]`, `[long pause]`, reticências.

## Respiração (a testar)
Candidatas a validar em teste curto, uma por frase, comparando com e sem: `[sighs]`, `[clears throat]`, `[gulp]`, `[short pause]`, `[long pause]`, `[slightly pause]`, `[quietly]`, `[softly]`, `[hushed]`. O blog oficial (elevenlabs.io/pt/blog/elevenlabs-audio-tags-list) diz que o conjunto de tags não é fixo (descrições livres funcionam, ex.: `[nervous, trying to sound confident]`), que não há tag documentada de inspirar/expirar (`[inhales]`/`[exhales]` podem ser lidas em voz alta) e que o v4 pode acrescentar pequenos toques humanos sozinho conforme a emoção. A tag lida em voz alta indica formato errado ou tag não suportada. Combinar com vírgula dentro de um só colchete: `[whispering, playful]`. Menor Stability = entrega mais expressiva; SSML (`<break>`) não é suportado. Registrar o que funcionar em `docs/roteiro_voz_elevenlabs_v4.md` (somente com pedido do usuário).
