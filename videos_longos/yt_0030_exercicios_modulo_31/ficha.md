formato: longo_horizontal
Série pública: **CÁLCULO III · EP. 04**
# Exercícios do módulo 3.1: campos, rotacional, divergente, limite e derivadas parciais
disciplina: Cálculo III
bloco: 3 · Funções de várias variáveis a valores vetoriais
modulo: 3.1 · Campos vetoriais, rotacional, divergente, limite, continuidade e derivadas parciais
item: 3.1-E1 · exercícios integradores do módulo
referencia: Guidorizzi vol. 3 (exercícios 1.1–1.5 e §1.6) e Stewart cap. 16, só como inspiração e régua de rigor (nada disso aparece na tela ou na fala)
duracao_alvo: 39:33,70 (real: voz v3.4 de 39:32,69 + 1,0 s de cauda; 6.956 palavras a 2,932 p/s). A v3.3 tinha 31:02,77
quadros_alvo: v1 em referencia_v1/ (sb30.html) + v2 em referencia_v2/ (sb30v2.html) + 11 do v3 em referencia_v3/ (sb30v3.html); no v3 valem 50
sistema_visual: o do EP. 03 (yt_0028 v4/v5): fundo violeta liso + grade que nasce dos eixos (assets/calculo/papel.py v2), variante B (FUNDO_PAINEL = "grade")
3d_threejs: nenhuma cena (decisão do Kaio: 2D simples e bem feito, com movimento; o 3D atrapalha a leitura dos vetores)
solido_3d: nenhum do arsenal Blender
anterior: yt_0028 · EP. 03 (o gancho dele promete o desafio do D5)
proximo: yt_0029 · EP. 05 · Soma de Riemann e integral dupla (cartão NO PRÓXIMO VÍDEO no fim)

## Estado

- 2026-11-11 · preview silencioso v1 (handoff v1): `renders/v1/yt_0030_preview_v1_540p15.mp4` (960×540, 15 fps, sem áudio, 26:14).
  Sem voz, SRT, 1080p, master ou entrega.
- 2026-11-11 · preview silencioso v2 (handoff v2 = `handoff_v2.md`, R11–R16, narração v3.1): `renders/v2/yt_0030_preview_v2_540p15.mp4`
  (960×540, 15 fps, sem áudio, 28:57,47). QA em `renders/v2/qa/` (51 alvos ≤ 4 px a 1080p; 138 glyph maps; 0 sem origem; 0 holds > 6 s;
  gatilhos ≤ 0,16 s). Pendente de aprovação; sem voz, SRT, 1080p, master ou entrega. Cópia do v1 em `v1_bak/`.
- 2026-11-12 · preview silencioso v3 (handoff v3 = `handoff_v3.md`, narração v3.2 com leitura dos símbolos): `renders/v3/yt_0030_preview_v3_540p15.mp4`.
  Gancho em jogo de pares, abertura/P2/resumo em escada (`escada30.py`), palcos vivos, D5 com chaves P/Q e derivadas no caminho até a célula,
  A4 com morfose z^s e Mercator, cartão 8 × 16 kg. QA em `renders/v3/qa/` (inclui `qa_v3.py`). Cópia do v2 em `v2_bak/`. Sem voz, SRT, 1080p ou master.
- 2026-11-13 · FINAL (handoff final = `handoff_final.md`, narração v3.3; a v3.2 ficou em `narracao_v32.md`): correções C1–C7; voz ElevenLabs v4
  (`audio/narracao_final.wav`, 31:01,76, 8 blocos, 2,908 palavras/s); tempos da voz real (`tempos.py` → `ancoras.json`, alinhamento forçado);
  master `renders/yt_0030_master_final_1080p30.mp4` (1920×1080, 30 fps, 31:02,77, CRF 14); `legenda.srt` (508 blocos); capítulos
  `renders/capitulos_final.txt`; preview com voz `renders/final/yt_0030_preview_final_540p15_voz.mp4`. QA em `qa/` e `renders/final/qa/`
  (sync: 69 âncoras + 459 gatilhos + 23 fins de sublinhado, atraso −0,17 a +0,05 s; emendas ±0 quadro). Polimento final: eixos que cruzavam
  rótulos de painel (D1, D4-5, A4) param em 828 px; o gráfico do A3-3 desceu 22 px (o |B| saiu de baixo da ‖B‖). Entrega em
  `entregas/Vídeos Longos/Cálculo III/Cálculo III - EP 04 - Exercícios do módulo 3.1 - 0030/` (master, srt, WAV, texto/ com tags, limpa,
  handoff e capítulos; manifesto com 9 arquivos). Lotes 1080p sem perdas apagados depois do QA. Sem capa, commit ou push.
- 2026-11-14 · FINAL v4 "conta inteira" (handoff `handoff_v4.md`, narração v3.4 = `narracao.md`; a v3.3 ficou em `*_v33.*`): as 21 contas C1–C21
  degrau a degrau na tela e na fala (provas em `qa/contas_v34/` + prancha `qa/contas_v34.jpg`); motor `alg30.py` com `deriva_cel`, `le_abre`/`le_fecha`.
  Voz: 11 trechos novos ElevenLabs v4 (`audio/v34/T01–T11`, T03 em take 2) emendados na voz v3.3 (`emendar_voz.py`) → `audio/narracao_final.wav`
  (39:32,69; 2,932 p/s); QA da emenda em `qa/emenda_v34.txt` (11 OK) e `qa/emendas_v34.txt` (8 "FALHA" de nível/salto justificadas no próprio arquivo;
  falta a escuta do Kaio). Master `renders/yt_0030_master_final_1080p30.mp4` (1920×1080, 30 fps, 39:33,70, CRF 14); `legenda.srt` (648 blocos);
  capítulos `renders/capitulos_final.txt`; master v3.3 guardado em `renders/v33/`. Sync: 69 âncoras + 586 gatilhos, atraso −0,18 a +0,14 s, emendas ±0.
  Entrega na mesma pasta de `entregas/` (substitui a v3.3). Sem capa, commit ou push.

## Arquivos da unidade

- `escada30.py` (v3: escada com ícones de mini-campo, usada na abertura, no P2 e no resumo) · `narracao_v31.md` (a narração do v2)
- `cena.py` (lotes PH, PD1, PD2, PD3, PD3B, PD4, PD5, PA1, PA2, PA4, PA3, PS) · `sec_*.py` (um bloco do roteiro por arquivo)
- `kit.py` + `v30.py` (cópias do kit/v28 do yt_0028) · `lib30.py` (acréscimos do sb30) · `alg30.py` (v2: motor das contas — `Lin` por peças,
  `gm` glyph map por chave com voos, `cancela` R14, `acende` R15, fusões `Duas`, auditorias R11 `[sem-origem]` e R13 `[r13]`)
- `tempos.py` + `narracao.md`: gatilhos por posição da palavra ÷ 3 (na fase da voz, trocar pelos tempos medidos no WAV contínuo)
- `render.sh`, `render_todos.sh`, `auditar.sh` (QA R5), `montar.py` (emenda com a costura de 0,4 s), `comparar.py` (render × alvo), `qa30.py`, `qa_v2.py` (origens, glyph maps,
  gatilhos, R12, R13), `numeros.py`, `zip_gpt.py`; ferramentas de iteração `holds_fala.py` (fala dentro de cada hold) e `quadros_v2.py` (quadros por gatilho)
