# HANDOFF — yt_0008 (5.3) · fase de voz → sincronização → render final em qualidade máxima

Cole este texto como primeira mensagem no Claude Code da outra conta. Responda em pt-BR. Leia `AGENTS.md` do repositório.

## Onde está tudo
- Worktree: `C:\Users\KaioOrtiz\PycharmProjects\parallax-long-0008` · branch `video/long-0008` · unidade `videos_longos/yt_0008_magnetostatica_ampere/`.
- Ambiente: não criar venv; usar `UV_PROJECT_ENVIRONMENT=C:\Users\KaioOrtiz\PycharmProjects\manim-fisica\.venv` e `uv run --no-sync`. Não mexer em `template/`, `docs/` globais, 5.1 (`yt_0005`) nem 5.2 (`yt_0006`).
- Chave ElevenLabs: só na variável de ambiente `ELEVENLABS_API_KEY` da sessão (PowerShell). Nunca em arquivo, commit, chat ou handoff. Se não estiver definida, peça ao usuário.
- Último preview silencioso (V6, 19:12,9, 960×540/15 fps): `renders/preview/YT0008Ampere_preview_v6.mp4`. **O código já mudou depois dele** (abertura nova + `I_env`), então o vídeo atual da cena é ≈ 20:50 (V6 + 100 s de abertura).

## Estado (fechado antes desta fase)
1. **Narração fechada** (decisão do usuário: manter a versão longa, ≈ 26–27 min; aceita-se o vídeo final por volta disso):
   - `texto_narracao.txt` — fala limpa, sem tags (fonte da legenda/SRT/ASR). 4.432 palavras.
   - `narracao_tags.md` — a mesma fala com 62 audio tags ElevenLabs v4; seção `## Texto corrido (para gravação)`. Símbolos LaTeX já trocados pela fala (ésse, jota, erre linha, efe, cá, ele maiúsculo, ene, ene maiúsculo, cê, esse maiúsculo).
   - `narracao_revisada_gpt.md` — texto-fonte do GPT (sem tags, com LaTeX); `narracao_sugestao.md` — v1 antiga (só consulta; tem a tabela de "Na tela" por bloco).
   - `narracao_ancoras.md` — remapeamento em 198 unidades: âncora no relógio do V6, janela de animação, palavras, voz, "segurar", início final. **Os tempos são do V6 sem a abertura nova**: somar o comprimento real da abertura a todas as âncoras seguintes. Gerado por `renders/tempos/remap.py`; tags por `tags.py`; `fecha.py` gera o `texto_narracao.txt`.
   - Origem dos tempos: `renders/tempos/log_tempos.json` (+ `log_legivel.txt`), levantado por `log_runner.py` (monkeypatch externo, sem editar a unidade; rodar com media dir **sem `~`**, ex.: `renders/tempos`).
2. **Animação já alterada (código), ainda sem render completo:**
   - **Abertura nova**: seção `abertura` (`sec1.py`, primeira em `SECOES` de `cena.py`): fio + traços verdes + 3 anéis + equação ∇×B = 0 (s > 0) + legenda "Fora do fio, o rotacional é zero. Como pode?", e `self.clear()`; depois `pergunta` refaz a sequência original do fio. Duração controlada por `ABERTURA_S = 100.0` em `sec1.py` (estimativa; **ajustar à fala real** do gancho + saudação até "Comecemos pelo exemplo mais simples").
   - **Corrente envolvida**: `I_{\rm enc}` → `I_{\rm env}` e "corrente encerrada" → "corrente envolvida" em `geo.py`, `kit.py`, `sec1.py`, `sec5.py`, `sec6.py` (inclui legendas, checkpoint `n14_corrente_envolvida`, barra de estratégia). Falta **conferir no render** (glyph maps, cores, larguras) e que não ficou nenhum "enc"/"encerrada" visível.
   - Toroide: na fala, "Pela simetria do toroide ideal" vem **antes** de "Na seção mostrada" (já trocado nos arquivos de texto; a animação mostra vista de cima → seção).
   - `qa_fisica.py`: 38 testes OK.
3. Git: commits locais em `video/long-0008` (sem push). Nada foi enviado ao remoto.

## Tarefa desta sessão (em ordem; parar e reportar ao fim de cada etapa)
**Etapa 1 — Voz (gasta crédito: confirmar com o usuário antes de gerar).**
- Simular: `uv run --no-sync python videos/gerar_voz_elevenlabs.py videos_longos/yt_0008_magnetostatica_ampere/narracao_tags.md videos_longos/yt_0008_magnetostatica_ampere/audio/narracao_v4.wav --voz qw7jgPZWOKrl10GsjQ82 --secao "## Texto corrido (para gravação)" --seco`. Mostrar os 7 blocos (≤ 4.500 caracteres) ao usuário.
- Gerar com voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4` (nunca turbo), `mp3_44100_192` → WAV mono 16 bits 44,1 kHz, em `audio/narracao_v4.wav`. Não criar `narracao_final.wav` até o usuário aprovar.
- Ouvir/checar: tags lidas em voz alta, pronúncia (jota, erre linha, ésse, mi zero, delta de Dirac, ampère), emendas entre os 7 blocos, números. Regerar só o bloco ruim (ajustando tags). Registrar modelo, voz, versão do texto e se houve tags.
- Medir a duração real; se passar muito de ~27 min, **reportar** antes de seguir (o usuário aceitou 26–27 min).

**Etapa 2 — Sincronização bem ancorada, sem atrasos.**
- Modelo: `videos_longos/yt_0005_magnetostatica_forca_lorentz/sync_voz.py` (alinha o WAV ao texto sem ASR, pesos por sílabas + pausas medidas no WAV, programação dinâmica em faixa; gera `sync.json` com o instante de cada célula). Adaptar para o yt_0008 (cópia dentro da unidade) usando `texto_narracao.txt` e as unidades de `narracao_ancoras.md` como "células".
- Para cada unidade: calcular quando a **voz** começa e terminar a unidade; a animação deve estar exatamente no evento da âncora nesse instante. O vídeo se molda à voz: onde a voz é maior que a janela, **segurar** o quadro (ou estender holds); onde sobra animação, **encurtar holds / acelerar** — nunca cortar o conteúdo. Nada de a animação chegar na equação antes (ou depois) de a voz falá-la.
- Regras de ritmo: a equação/legenda entra junto com a frase que a introduz; resultados importantes têm respiro antes (pausa curta); a abertura segura o fio durante o gancho + saudação e só então reexibe a sequência ("Comecemos pelo exemplo mais simples").
- Implementar o retiming dentro da unidade (ex.: tabela de durações por âncora lida pelos `hold`/`wait`, ou mapa tempo-de-voz → tempo-de-cena), sem tocar em `template/`. Gerar `sync.json` e um `legenda.srt` (texto **sem** tags) quando o usuário abrir a fase de legenda.

**Etapa 3 — Render final em qualidade máxima.**
- 1920×1080 (config horizontal da unidade), 30/60 fps conforme o padrão dos longos do repositório (conferir `docs/formatos.md` e o `config_horizontal`); H.264 yuv420p **CRF 14** (padrão do projeto; o template já troca o CRF automaticamente em 1080p; conferir `crf=14.0` no stream). Render por seção/grupo (`_grupo.sh`) e junção (`juntar.py`), sem recompressão desnecessária.
- Master = render do Manim + voz colada sem recomprimir o vídeo (`videos/montar_master.py`; para longos com `.srt` separado não há legendado embutido). Não sobrescrever finais antigos.

**Etapa 4 — Reassistir e garantir (QA de fechamento obrigatório).**
- Reassistir **o vídeo inteiro com o áudio** (contact sheet + trechos de 5 s + quadros críticos em resolução cheia + checkpoints `n00`…`n23`). Para cada bloco B00–B23 conferir: o que a voz diz = o que está na tela, a álgebra aparece quando é falada, cada passo (identidade vetorial, delta de Dirac, integração por partes, Stokes, solenoide/toroide) tem tempo suficiente, a legenda não sobrepõe equação, nada fica fantasma/atrás, cores do capítulo 5 (aço, corrente verde, caminho branco, B magenta).
- Conferir especificamente: (a) **abertura** sincronizada com gancho + saudação e a reexibição do fio; (b) **`I_env`/“corrente envolvida”** em tela em todos os pontos (fio, lâmina, solenoide, toroide, independência da superfície) e nenhuma ocorrência de "enc"/"encerrada"; (c) toroide: vista de cima → seção na ordem da fala.
- Rodar `qa_fisica.py` e a verificação de lifecycle (`census_after_clear` em `qa_timeline.json`). Corrigir o que aparecer e re-renderizar só o trecho afetado.
- Pendências visuais menores conhecidas: rótulo "altura fora de escala" encosta no cone da delta (N09); rótulos N09/N10 apertados na legenda inferior; token `(nL)` ainda violeta; 5.1/5.2 não têm a convenção de cores nova (não mexer).

**Etapa 5 — Fechamento.** Relatório de entrega (arquivos alterados, verificações e renders com resultados, caminhos do master/áudio/SRT, limitações). Só então: `uv run python videos/entregar.py` **somente se o usuário pedir**; atualizar `ficha.md`/`RELATORIO` da unidade **somente se pedido**. Commit/push só se o usuário pedir.

## Regras que valem sempre
- pt-BR; sem commit/push/branch/PR sem pedido; não gerar voz/SRT/master fora da etapa aberta; não sobrescrever `audio/narracao_final.wav` de vídeo fechado; chave de API nunca em texto.
- Briefing de física/didática é soberano: não reescrever a matemática por conta própria; inconsistência objetiva → reportar antes.
- Previews: 960×540/15 fps; render completo só no fechamento.
