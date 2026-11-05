# Brief dos agentes do HANDOFF v3 (yt_0020)

Pasta: `videos_longos/yt_0020_cinematica_angular/`. Responda em pt-BR. Fase: preview visual silencioso 960×540/15 fps.

## Leia
`AGENTS.md` da raiz; `brief_agente_v2.md` (regras comuns, ciclo de render/auditoria, relatório: **vale inteiro**, exceto onde este arquivo disser o contrário); `handoff_v3.md` (especificação soberana: §2 cor dos operadores já implementada no `kit.py`, §3 cor, §4 escala/colunas, §5 defeitos, §7 `TransformMatchingTex`, §9 álgebra, §11 por lote). `handoff_v2.md` continua valendo para o que o v3 não muda. Use `sec_t3.py`/`sec_e3.py` como exemplo de lote migrado.

## Regras específicas do v3
- Edite **somente o `sec_*.py` do seu lote**. `kit.py`, `prob.py`, `prob2.py`, `pecas20.py`, `cena.py`, `threejs/`, `qa20.py` e os outros `sec_*.py` são compartilhados: não altere; bug em peça compartilhada → descreva (arquivo, linha, correção) e contorne no seu `sec_*.py`. Exceção: arquivos de `threejs/cena3d/` exclusivos do seu lote.
- A regra de cor dos operadores (§2) já é aplicada por `eqp`/`M` (pós-passe `_operadores_neutros`). Confira por quadro que todas as equações do lote com d, dt, ∫, lim saem certas; se alguma MathTex não passar pelo `eqp` (Mc, MathTex direto, `lbl`), aplique a regra à mão.
- Duração do lote **igual** à atual (`[tempo] total`), sem `[abertura] … atrasada`. Narração e números congelados.
- Cor por capítulo (§3): aumentar cor de família **de verdade** (setas, arcos, números grandes, contornos de CORPO), nunca pintar aço, fundo nem tipografia neutra.
- Não mexa no que está certo (§1 "Mantido da v2"). Se uma mudança sua afetar outra coisa do lote, confira o quadro.
- Render: `./render.sh LOTE` e depois `./auditar.sh LOTE` (sequenciais, nunca juntos); lotes com 3D novo: `./seco.sh LOTE`, `rm -rf threejs/q3d/LOTE_960x540`, `(cd threejs && CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe" node r3d.js --lote LOTE) > log_3d_LOTE.txt 2>&1`, depois render e auditoria. Rode em background e espere a notificação. Máximo de **3 rodadas** completas; use `_quadros.py`/`_seq.py` (descritos no `brief_agente_v2.md`) para conferir por imagem cada item antes de gastar uma rodada. Outros agentes renderizam outros lotes ao mesmo tempo (memória curta): se o log terminar vazio ou com `latex failed`, rode de novo.
- Se restar sobreposição, corte, rótulo sobre desenho, coluna vazia > 5 s ou linha nascendo sobre outra, **não declare fechado**: reporte com o tempo.
- Registre no overlay (`self.reg`) o que o handoff §6 pedir para o seu lote.

## Relatório final (curto)
Para cada item do `handoff_v3.md` que cabe ao seu lote: corrigido / não corrigido / mudou de solução + quadro conferido (tempo). G28 antes → depois por classe e o que sobrou com motivo; `[tempo] total`; caminho do mp4 e dos PNGs de quadros; pendências reais; bugs em peças compartilhadas; o que não foi visto. Não crie voz, SRT, master, entrega, commit nem push; não rode `qa20.py`, `montar_preview.py`, `conferencia20.py`, `prancha_humana.py`.

## Itens por lote (números = seções do `handoff_v3.md`)
- **PH** (`sec_hook.py`: lotes PH e PA — o arquivo cobre hook e abertura; renderize PH e depois o lote da abertura conforme `cena.py`): §11 PH e PA, §3 (hook/abertura), §4 hélice D ≈ 65% da altura (H1 centrada e maior), §5.17, §5.14. Há 3D (`seco` + `r3d.js --lote PH`).
- **PT1** (`sec_t1.py`): §11 PT1 (T1-1…T1-5), §3 (T1), §4 coluna T1-1, cor operadores.
- **PT2** (`sec_t2.py`): §11 PT2, §3 (T2), §4 colunas T2-1/T2-3/T2-4 e hélice ≥ 55%, §5.14, `dt` violeta no T2-2.
- **PT3** (`sec_t3.py`): §4 (discos do T3, colunas T3-2/T3-3), §5.5 (T3-4), §7 `tmt` T3-1/T3-5, §6 (2 MathTex sem partes), cor operadores T3-1/T3-4 (ω da integral igual aos outros).
- **PT4** (`sec_t4.py`, 3D): §4 (T4-1 coluna, T4-3 coluna, disco 59%, hélice), §5.6, §5.7, §5.8, §9.3, §7 `tmt` T4-1/T4-4, §6 rótulo `θ` do T4-1 fora do arco, cor operadores T4-1/T4-4, §3 (T4).
- **PT5** (`sec_t5.py`, 3D): §5.9–§5.13, §9.1 (regra do produto), §3 (T5), §7 `tmt` T5-4, §6 registrar `a3d` para o produto vetorial do T5-8.
- **PE1** (`sec_e1.py`): §5.1–§5.4, §7 `tmt` E1-4, §3 (E1), §6 (1 MathTex sem partes, `a_c : a_t` do inset), `m/s²` branco no eixo do E1-6.
- **PE2** (`sec_e2.py`): §9.2 (E2-3), §5.16, §4 colunas E2-1/E2-5, §3 (E2), r₁/r₂ da fração em GEO cheio.
- **PE3** (`sec_e3.py`, 3D): §5.15, §3 (E3: arco âmbar 1° maior, ω⃗ grosso, faixa âmbar da latitude, v⃗, λ), §7 `tmt` E3-3.
- **PS** (`sec_fim.py`, 3D): §3 (Resumo e Encerramento), §4 hélice do PS ≥ 65% da altura, §5.14 (282,7 legível).
