# yt_0020 · estado do HANDOFF v2 (pausado em 2026-11-03, ~14:00)

Especificação soberana: `handoff_v2.md` (nesta pasta). Regras: AGENTS.md da raiz (pt-BR; sem voz, SRT, master, entrega, commit, push; narração e números congelados).
Preview v1 entregue: `renders/preview_yt0020_v1_960x540.mp4` + `renders/yt0020_v1_qa_pranchas.zip` (`renders/qa_v1.txt` guarda o QA do v1).

## Pronto e verificado
- **Escrita da álgebra em ordem de x (§2)** em `prob2.py` (`Prob2.escreve`, `_Temporizado`, `_unidades`, `_ordena_glifos`): todo `FadeIn` de linha da CONTA com MathTex vira escrita da esquerda para a direita (numerador → barra → denominador); `voa` delega a ela (partes que voam pousam no instante da vaga); `passo` ordena os mapas por x (removedores primeiro). `eqp` marca cada glifo com `_unid`; `_selo_tag` em selos (selo/DICA/texto puro seguem por FadeIn). Testado no PT3 inteiro: duração igual (164,9 s), sem atraso de âncora, `ORDEM` = 0 falhas em 14 linhas, caixa vazia = 0. Quadros conferidos: `α = dω/dt` nasce α → = → fração.
- **QA**: `qa20.py` tem `ORDEM` e `CAIXA VAZIA` e gera `renders/algebra.txt` (lê `[alg]` dos `log_aud_*.txt`). `passo` imprime `[alg]`. FALTA no qa20: auditorias `MOSTRADOR` (lê `reg("mostrador", mostrador_deg=…, acum_rad=…)`), `PARADO` 3 s, `COLUNA VAZIA` 5 s, tamanho do objeto, cor só de família (§9).
- **Ferramentas**: `g28.py LOTE` (resumo do G28 por ocorrência única; usar `PYTHONIOENCODING=utf-8`), `_seq.py` (sequência de quadros; sempre passar caminho de saída), `_comp3d.py`, `_quadros.py`. `L20.marcador_mob/troca_marcador` (marcador de canto, um por vez). Bug de `_gnum` corrigido em `pecas20.num_mob`.
- **3D (§7.1–7.4)** em `threejs/cena3d/r20.js` + `gerar_texturas.py` (tex20.js regenerado): hélice com aerofólio torcido, faixa clara na ponta, spinner e parafusos; disco de aço com chanfro, linha âmbar, pino e sombra (luz neutra); livros com capa azul / contracapa grafite / lombada ciano e seta normal à capa (`e.on`, `e.oNg`, pontos `nb*/nt*/ngt`); Terra com relevo suave, atmosfera e faixa âmbar de latitude. Conferido só em quadros avulsos (`node r3d.js --sonda …`, `renders/_3d/`). **Nenhum lote 3D foi re-renderizado**: os PNGs de `threejs/q3d/` ainda são do v1.
- **Hook (`sec_hook.py`) editado, NÃO renderizado**: `LoteHook(L20)`; hélice K_H=2,45 em C_H=(−3,7; −0,3); rastros (DT_RASTRO) e anel no ponto de 10 cm; seta curva no cubo e `2.700 RPM` na legenda; marcador de canto; barra do som com marca violeta `78%` e linha tracejada ligada ao `≈ 970 km/h`; ícones/partícula da Abertura maiores. Falta: `./render_v3.sh PH` (roda seco + 3D + render + auditoria), conferir quadros, G28.

## Agentes (todos PARADOS; relatórios NÃO recebidos)
Cada um editava só o próprio `sec_*.py`. Estado no disco (compilam): `sec_t1.py` (13:51), `sec_t3.py` (13:46), `sec_e1.py` (13:59) foram alterados pelos agentes; `sec_t2.py` e `sec_e2.py` ainda NÃO foram alterados por eles (PT2 e PE2 caíram no limite de sessão antes de editar). Não sei quais itens de PT1/PT3/PE1 ficaram completos: conferir com `git diff` de cada arquivo, rodar `./render_v3.sh LOTE --sem3d` e `python g28.py LOTE`, e olhar os quadros. Três processos python de render deles podiam ainda estar rodando ao pausar (`media_PT1/PT3/PE1`, `log_*`); confira `[tempo] total` nos logs antes de confiar.
Briefing usado (por lote): itens do §4 + linhas do §5 + §3/§6/§8 do handoff; regras: editar só o próprio `sec_*.py`, não rodar `qa20/montar_preview/conferencia20/prancha_humana`, manter `[tempo] total` (PT1 133,7 · PT2 106,7 · PT3 164,9 · PE1 196,3 · PE2 169,3) sem `[abertura] … atrasada`, nunca encolher equação < 0,85 (quebrar pelo `=`), Bash estraga barras invertidas em heredocs (usar Edit/Write).

## Falta fazer
1. Fechar PT1, PT2, PT3, PE1, PE2 (agentes novos ou à mão).
2. Segunda onda, com 3D novo: PT4, PT5, PE3, PS (e o D14 hélice grande no T2-4; D2/D24 no PT4; D25–D31/C1 no PT5; D38–D42 no PE3; D43/D44 no PS). Re-renderizar o 3D de cada lote (`./render_v3.sh LOTE`, sem `--sem3d`).
3. Render do PH. Depois, no vídeo inteiro: `python montar_preview.py v2`, `prancha_humana.py v2`, `conferencia20.py v2`, `qa20.py v2` (+ auditorias que faltam), zip `yt0020_v2_qa_pranchas.zip` com comparação v1 × v2 e sequências de escrita (T3-4 integral, T4-5, T5-8, E2-3), relatório item a item (corrigido / não corrigido / mudou de solução).

## Cuidados
- Máquina: 8 CPUs, 15,7 GB; com 5 agentes renderizando a memória livre caiu a 0,7 GB. No máximo 3–4 processos manim ao mesmo tempo.
- O limite de sessão da API derrubou os agentes uma vez (reseta ~12:40). Agentes não passam de uma conta para a outra.
