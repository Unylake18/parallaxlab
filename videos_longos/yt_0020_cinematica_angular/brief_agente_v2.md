# Brief comum dos agentes do HANDOFF v2 (yt_0020)

Pasta: `videos_longos/yt_0020_cinematica_angular/`. Responda em pt-BR.

## Leia
- `AGENTS.md` da raiz (regras gerais) e, na unidade, `estado_v2.md` (onde paramos) e `handoff_v2.md` (especificação soberana): §2 (escrita da álgebra), §3 (G28), §6 (cor), §7.5 (2,5D), §8 (parados/colunas vazias), mais os itens do §4 e as linhas do §5 do SEU lote.
- `prob2.py` só o necessário para usar `Prob2.escreve`, `voa`, `passo` (escrita em ordem de x, já implementada e validada no PT3); `pecas20.py`/`kit.py` para as peças (selo, rótulo, `L20.marcador_mob`/`troca_marcador`, pilha). Use `sec_t3.py` como exemplo de lote já migrado.

## Regras
- Edite **somente o `sec_*.py` do seu lote**. `kit.py`, `prob.py`, `prob2.py`, `pecas20.py`, `cena.py`, `threejs/`, `qa20.py` e os outros `sec_*.py` são compartilhados: não altere; se uma peça compartilhada tiver bug que bloqueie, descreva no relatório (arquivo, linha, correção sugerida) e contorne no seu `sec_*.py` se der.
- Narração e números congelados. Duração do lote (`[tempo] total` no log) **igual** à atual; nenhum `[abertura] … atrasada`.
- Nunca encolher equação abaixo de 0,85; linha larga quebra em duas pelo `=`. Tamanhos mínimos do G1 (selo ≥ 24, frase-chave ≥ 30, rótulo MathTex no ESQUEMA ≥ 36, equação na CONTA ≥ 46). `\operatorname{sen}`, nunca `sin`.
- Bash estraga barras invertidas em heredoc/sed: edite código com Edit/Write.
- Não rode `qa20.py`, `montar_preview.py`, `conferencia20.py`, `prancha_humana.py`. Não crie voz, SRT, master, entrega, commit nem push.

## Ciclo de verificação (memória curta: 15,7 GB para vários agentes)
1. `uv run --no-sync python -m py_compile sec_X.py`.
2. `./render.sh LOTE` e **depois** `./auditar.sh LOTE` (um após o outro, nunca em paralelo, e sem `&`). Lotes com 3D novo (PT4, PT5, PE3, PS, PH): `./seco.sh LOTE` e o 3D como em `render_v3.sh`, depois render e auditoria em sequência. Rode em background e espere a notificação (render leva 5–10 min).
3. Se o log terminar em `latex failed but did not produce a log file`, é concorrência do LaTeX entre processos: rode de novo.
4. `PYTHONIOENCODING=utf-8 uv run --no-sync python g28.py LOTE`: meta 0 real; cada ocorrência que sobrar precisa de motivo escrito de falso positivo.
5. Quadros: `uv run --no-sync python _quadros.py LOTE t1 t2 ...` → `renders/_q_LOTE.png` (abra com Read). Escrita em ordem: `uv run --no-sync python _seq.py media_LOTE/videos/cena/540p15/LOTE.mp4 t0 t1 10 480 60 960 330 renders/_seq_LOTE.png`. Confira os quadros de referência do §4 do seu lote; `grep "\[alg\]" log_aud_LOTE.txt` para ver como cada linha foi construída (meta: 0 linha de equação por FadeIn).
6. Itere só o seu lote. Máximo de 3 rodadas completas de render; o que não fechar vai para o relatório.

## Relatório final (texto curto, é lido por outro agente)
- Para cada item S/C/D do §4 do lote: corrigido / não corrigido / mudou de solução, com o quadro conferido (tempo em s).
- Linhas do §5: como cada uma foi construída (E/V/GM/TMT).
- G28 antes → depois por classe; o que sobrou e por quê.
- `[tempo] total` final; caminho do mp4; pendências reais; bugs em peças compartilhadas.
