---
name: relatorio-entrega
description: Monta o relatório de entrega obrigatório do AGENTS.md (arquivos alterados, verificações, artefatos, pendências, "Teste do arsenal") e o zip com todos os frames e o vídeo. Usar ao concluir qualquer briefing/handoff ou quando pedirem relatório ou zip para o GPT.
---

# Relatório de entrega

Em pt-BR. Seja factual: se algo falhou ou não foi verificado, diga.

## Estrutura

1. **Arquivos alterados** — `git status --short` / `git diff --stat` (link para cada arquivo).
2. **Verificações, testes e renders** — o que rodou e o resultado (py_compile, preview, timestamps checados).
3. **Artefatos** — caminho do preview, prancha de quadros, demais gerados.
4. **Limitações e pendências reais** — incluindo o que não pôde ser verificado.
5. **Teste do arsenal** — só se houver sólido 3D ou se a ficha pedir avaliação: sólido(s) e `id`; resolução e se o cache foi preparado com `ponte.py`; custo de render e peso das sequências; legibilidade (vertical/horizontal, preview/final); o que funcionou; o que faltou (ajuste desejado, parâmetro novo, sólido ausente); veredito (encaixou / encaixou com ajustes / não encaixou).

## Zip para o GPT (toda entrega)
Gere um zip com **todos os frames** do preview e o vídeo, dentro da pasta de renders da unidade (também na versão final: zip não vai para `entregas/`), e informe o caminho. Depois da aprovação final, `videos/limpar_rastro.py` apaga o zip junto com o resto do rastro. Mídia pesada não é versionada pelo git.

## Economia de contexto (tokens)
- Monte o zip com um comando só e informe o caminho; não liste nem leia os frames um a um.
- Para "arquivos alterados", use `git diff --stat` (não o diff completo).
- Não reabra pranchas já vistas na sessão só para descrevê-las no relatório.

## Regras
- Não inicie outra fase da produção; pare após o relatório.
- Não faça commit/branch/PR/push sem pedido.
- Não atualize docs globais por conta própria.
