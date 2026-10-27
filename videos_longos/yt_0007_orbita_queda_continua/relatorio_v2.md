# yt_0007 — revisão visual v2 (preview silencioso)

Preview: `media_v2/preview_v2_0007_960x540_15fps.mp4` — 512,267 s, 7.684 quadros, 960×540, 15 fps, sem áudio.
Tempos novos: `timing_v2.json` (N01 0–57,5 · N06 124,5–153,5 · N08 181,7–194,8 · N10 222,4–242,1 · N12 278,7–303,8 · N13 303,8–381,6 · N17 449,0–483,9 · N18 483,9–512,3).
Evidências extraídas do próprio MP4: `qa_v2/*.png` (pranchas com o tempo em cada quadro). Preview e ZIPs anteriores preservados.

## Arquivos alterados (só esta unidade)
`encenacao.py`, `cadeia_equacoes.py`, `sistema_lunar.py`, `geometria_visual.py`. `modelo_orbital.py`, `superficie.py`, `matematica_visual.py`, `cena.py`, template e assets intactos.

## Resolvido (evidência no MP4)
- **A01 títulos/notas sobrepostos:** `trocar()` faz saída → entrada em sequência (um só texto legível por vez; conferido no meio da troca em 16 blocos). `junto=` mantém o movimento físico (usado em N18).
- **A02 N10:** Terra à esquerda, fórmula, relógio “tempo físico” e nota na coluna direita; chamadas terminam no arco certo; sem cotas sobre a fórmula (236,6 s).
- **A03 N08:** cotas, 4,35 m, relógio, fórmula e fantasmas saem antes de desfazer o estiramento; só os avisos ficam durante a distorção (182,3–183,8 s). Nenhum quadro com cota fora do corpo.
- **A04 N13:** controle em coluna própria à direita (trilho com 5 marcas, valor v₀ ao vivo), previsão recortada numa janela com seta de continuação; nomes: “impacto · ligada”, “elipse ligada”, “circular”, “elipse externa · ligada”, “aberta”, em branco (não mais ciano). Voo reenquadra após o ajuste.
- **A05 N12:** encerra o círculo (a = r), reenquadra com a trajetória oculta, desenha a elipse com o corpo; Terra no foco, centro da elipse e cota de `a` do centro ao vértice oposto (não cruza a Terra).
- **A06/A07 faixas:** avisos movidos para y ≥ −2,9; faixa escura em degradê sob o título protege a leitura nos reenquadramentos (globo pode ser cortado; texto não).
- **N03/N04/N05/N16/N17:** rótulos de ramos; vetores ampliados com rótulos de lados opostos e Δv em ciano; M/m/r/F_g com chamadas e placas; Lua com vetores saindo do disco, título “A mesma lei gravitacional” → “A Lua também está caindo.”; N17 com rótulos fora da envoltória do globo e conclusão sem colidir.
- **N06 troca de lados:** `path_arc` nos blocos (um passa por cima, outro por baixo; sem compressão sobre o “=”).
- **N09:** setas ligadas aos corpos e à estação; forças (F_g nos dois, N só no apoiado) separadas de aceleração (g); razão com `R_T`.
- **N14:** legenda azul sólida / violeta tracejada; **N15:** reencontra o canhão e abre as quatro curvas; **N18:** zoom em dois passos (sem tela vazia).
- Brilho discreto no corpo e halo na curva ativa; rastros anteriores mais tênues.

## Verificações
`py_compile`; `modelo_orbital.py` (validar() passou, valores a 400 km conferem); render completo sem erros; auditoria de amarelo nos 7.684 quadros (1 px/4, marca excluída): nenhuma ocorrência; quadros estáticos por marco (`QUADROS=1`) em `qa_v2_estatico/`.

## Pendências / atenção
- Não conferi quadro a quadro: amostrei 6–12 instantes por ponto crítico. Em N13 os cinco voos foram vistos em amostras, não em fases completas.
- N14 (≈391 s): no close do impacto aparece um retalho retangular mais escuro na superfície (amostragem do recorte da Terra, comportamento anterior; não alterado).
- N17: conferidas 4 fases do movimento local; vale revisão artística da hierarquia de linhas.
- N01–N03 e N09 foram verificados só por quadros de marco e amostras; N04 tem Δt maior (0,07 T) para a diferença ciano ficar visível.
- Teste 1080p não repetido (superfície inalterada).
- Aprovação artística permanece com o usuário.
