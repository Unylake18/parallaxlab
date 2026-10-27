# Narração V2 — VID 0029 · POR TRÁS DA FÓRMULA · EP. 09 (base congelada para a voz)

Texto da Produção (2026-10-26), lapidado sobre a sugestão do Claude Code (`narracao_sugestao.md`): mesmos 10 blocos, mesma
ordem de eventos. **Base congelada:** `texto_narracao.txt` (texto corrido com as tags do ElevenLabs v4). Os blocos e as
janelas estão em `narracao_blocos.py` → `narracao_sugestao.json`.

## Orçamento (estimativa pelo texto; a voz ainda não foi gerada)

**458 palavras** · a 2,7 palavras/s: **169,6 s** de fala · a 2,5 palavras/s: **183,2 s**. Com respiros e end card, ~3:00.
Primeiro corte se a voz sair lenta: "No modelo ideal, as espiras são bem juntinhas" (B02); o chip `MODELO IDEAL` fica na tela.

| Beat | Palavras | Fala a 2,7/s | Janela proposta (s) |
|---|---:|---:|---|
| B01 | 32 | 11,9 | 0–12 |
| B02 | 35 | 13,0 | 12–26 |
| B03 | 61 | 22,6 | 26–49 |
| B04 | 61 | 22,6 | 49–74 |
| B05 | 23 | 8,5 | 74–84 |
| B06 | 81 | 30,0 | 84–115 |
| B07 | 46 | 17,0 | 115–133 |
| B08 | 44 | 16,3 | 133–151 |
| B09 | 38 | 14,1 | 151–166 |
| B10 | 37 | 13,7 | 166–180 |

As janelas são proposta; na sincronização, elas saem da voz medida e só o `timeline.json` muda.

## O que a V2 muda e como a tela acompanha

- **"Raio do tubo"** (era "raio da seção"): a definição na tela do B03 virou `a: raio do tubo`.
- **"Raio do caminho"** para o r: entrou na tela a definição `r: raio do caminho`, junto com a seta de raio (B03), até o chip `B ∥ dℓ`.
- **Três testes:** os títulos de região viraram `TESTE 1 · NO BURACO`, `TESTE 2 · DENTRO DO ENROLAMENTO` e `TESTE 3 · FORA DO ANEL`.
- **Hook com os dois zeros:** a tela segue com o chip `E FORA DO ANEL?`; o "no buraco do meio" é só fala no B01 (provado no teste 1).
- **Tags:** `[excited]` só no resultado do B06 e no solenoide do B09; `[thoughtful, emphatic]` na simetria (B03) e no "campo zero"
  de fora (B07). Há tags no meio de blocos (B03, B06, B07, B08, B09): cada uma vale até a próxima. Sem `[slowly]`.
- **Ênfase por maiúscula** só em PRENDE, DUAS e DOBRO.

Física conferida frase a frase com o briefing: simetria na formulação aprovada (mesmo módulo, acompanhando o círculo), "modelo
ideal" explícito (B02, B03, B10), corrente atravessando o disco, sentidos (sobe dentro, desce fora), 1/r, quase o dobro, caso-limite
e "confina o próprio campo". Nada de "polo", número falado ou "zero na vida real".
