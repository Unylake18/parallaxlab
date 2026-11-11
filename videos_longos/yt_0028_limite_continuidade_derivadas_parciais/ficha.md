# Limite, continuidade e derivadas parciais

- **ID:** `yt_0028`
- **formato:** `longo_horizontal`
- **tipo:** `teoria_visual`
- **Série pública:** **CÁLCULO III · EP. 03**
- **disciplina:** `Cálculo III`
- **modulo:** `3.1 Funções de várias variáveis reais a valores vetoriais (no repositório: 11.1)`
- **bloco:** `3.1-T3`
- **referencia:** Guidorizzi, Um Curso de Cálculo, vol. 3, §1.5 e §1.6 — só na descrição do YouTube; nada de livro na tela nem na fala.
- **título:** Limite, continuidade e derivadas parciais
- **solido_3d:** nenhum do arsenal Blender, porque o vídeo é inteiro no plano
- **3d_threejs:** nenhuma cena
- **duracao_alvo:** 15:47 de voz real (`audio/narracao_final.wav`, 947,36 s, 2.865 palavras, 3,02 palavras/s); o vídeo termina 3 s depois da fala (CTA)
- **quadros_alvo:** `yt_0028_quadros_alvo_v4` (01–37) em `referencia_v4/` + `yt_0028_quadros_alvo_v5` (38–42: abertura, gancho, seta em destaque, caminhantes) em `referencia_v5/` (v3 em `referencia_v3/`, v2 em `referencia_v2/`, v1 em `referencia_v1/`)
- **sistema_visual:** fundo violeta liso + grade que nasce dos eixos (papel.py v2); painéis com número inteiro de quadradinhos (variante B, `FUNDO_PAINEL = "grade"`)
- **fundo:** violeta liso parado (`assets/calculo/papel.py` v2, `_arq()`); grade só dentro dos painéis e nos gráficos de tela cheia (alvos 07, 13, 22, 30, 31)
- **canto:** a partir do bloco A. Linha 1 `CÁLCULO III · LIMITE, CONTINUIDADE E DERIVADAS PARCIAIS`; linha 2: `CHEGAR PERTO`, `QUANDO O LIMITE NÃO EXISTE`, `CONTINUIDADE`, `DERIVADA PARCIAL`, `O ENGANO`, `A TABELA`, `QUATRO NÚMEROS, QUATRO MEDIDAS`, `O DESAFIO`, `RESUMO`
- **ordem:** H → A → B1 → B2 → B3 → B4 → B5 → B6 → B7 → S (o B7-5 do handoff foi cortado na v1.2)
- **Status:** versão final (handoff final, `handoff_final.md`): ajustes §2 (A1 com a logo, gancho do próximo vídeo, campos em onda, seta em destaque no B1, caminhantes no B3-2, quadradinho que age uma vez no B7-3, tag do zoom dentro da moldura), voz ElevenLabs v4, sincronização pela voz real, `legenda.srt`, master 1080p30 CRF 14 e entrega em `entregas/`. Preview v4 em `renders/v4/` e `v3_bak/` (*_v4.py).

## Arquivos
- `narracao.md` — Anexo A do handoff v2, uma âncora por parágrafo (`H1–H3`, `A1`, `B1-1…6`, `B2-1…4`, `B3-1…3`, `B4-1…5`, `B5-1…4`, `B6-1…4`,
  `B7-1…5`, `S1–S2`). Atenção: as âncoras são PARÁGRAFOS da fala, não as cenas do handoff (ex.: a âncora `B1-6` é a cena B1-7, a `B7-5` é a B7-6).
- `gerar_ancoras.py` → `ancoras.json`, `duracoes_estimadas.json` (2,8 palavras/s)
- `kit.py` — kit copiado do yt_0027 (relógio por quadro, âncoras, canto, caneta, auditorias); mudaram título, fundo e altura do canto (73/118 px)
- `v28.py` — helpers do `v27.py` (copiados) + peças do `sb28.html`: campos, clareira R1 (retângulo, disco, polígono, segmento; viva por quadro),
  pedacinho de fluido `Pedaco` (chapa + malha 4×4 + contorno, transformado inteiro pelo fluxo exato), QA R5 da seta inteira, CTA
- `sec_*.py` — um lote por seção (`PH`, `PB1`…`PB7`, `PS`); `cena.py` registra os lotes
- `render.sh` / `render_todos.sh` (540p15), `montar_preview.py [rodada]`, `comparar.py` (render × alvo, v4), `transicoes.py` (R10, v4), `qa_sobrepos_rel.py`, `qa_holds.py` + `holds_motivos.py`,
  `erros_v1_v2.py` (v2), `alinhamento.py` + `still1080.sh` (R9, stills 1080p), `antes_depois.py`, `holds_motivos.py`, `quadro.py`
- `verificacao/` — o script sympy do handoff (não roda aqui: sympy não está na `.venv`) e `verifica_numeros_numpy.py` com a saída
