# yt_0008 · 5.3 — relatório da rodada (preview silencioso)

Data: 2026-10-19. Escopo: implementar N01–N23 e gerar um preview 960×540 / 15 fps. Sem voz, SRT, master, 1080p, capa ou publicação.
Sem commit e sem push. O trabalho foi feito no worktree `../parallax-long-0008` (branch `video/long-0008`, criada a partir do `origin/main`
com autorização do usuário). Nenhum arquivo fora da unidade foi alterado.

## Arquivos (todos novos, em `videos_longos/yt_0008_magnetostatica_ampere/`)
- `cena.py`: a classe `YT0008Ampere`, uma cena contínua. `SEG`, `DE` e `ATE` servem para renderizar por trechos.
- `kit.py` e `base.py`: copiados do yt_0006 e estendidos:
  - famílias de cor r/r′;
  - pintura por subtermo (um termo continua sendo um token, mas J fica verde, F violeta e ∇ ciano dentro dele);
  - layout `app`;
  - `src` com vários tokens;
  - `drop()` que remove os netos.
- `geo.py`: laço orientado com a parte de trás atenuada, disco/coroa, caixa 3D, anel de B, barra de estratégia e `view_to`. Usa `tau < 0` = vista de cima, com projeção destra.
- `sec1.py` a `sec7.py`: os blocos N01–N05, N06–N07, N08–N10, N11–N13, N14–N16, N17–N20 e N21–N23.
- `fisica.py` (estados) e `qa_fisica.py` (QA numérico).
- `_grupo.sh`, `juntar.py` e `contato.py`: render por trecho, junção e folhas de contato.
- `ficha.md` e este relatório.

## Preview
- Arquivo: `renders/preview/YT0008Ampere_preview.mp4`. Dura 16min30s (990,0 s), com 14.850 quadros, H.264/yuv420p, 960×540, 15 fps e 47,7 MB. Os quadros foram decodificados por inteiro, sem tempos fora de ordem.
- Foi renderizado em 5 trechos, um processo por vez por causa da memória: r1 N01–N05 (3:00), r2b N06–N10 (4:33), r3 N11–N15 (3:32), r4 N16–N20 (4:22), r5 N21–N23 (1:03). Os trechos foram juntados com `juntar.py` (CRF 16).
- Quadros de estado de cada trecho em `renders/<trecho>/estados/`.

## Verificações
- `qa_fisica.py`: 27 itens, todos OK. Cobrem: rotacional e divergente nulos fora do fio; laço local 0 e global μ0I; cilindro (μ0J dentro, continuidade e C_ext); a→0 com I fixo; fluxo 4π de R/R³; ∇F = −∇′F; lâmina μ0K/2; solenoide longo calculado por Biot–Savart numérico (dentro ≈ μ0nI uniforme, fora ≈ 0); toroide.
- Compilação de todos os módulos com warnings tratados como erro. Rodada de fumaça (`SEG=nenhuma`) de N01–N23 sem exceção.
- Auditoria de enquadramento: 1 aviso, no texto do esquema do solenoide finito, que fica rente à borda do cartão e continua legível.

## Limitações conhecidas
- As 4 junções entre trechos (N05→N06, N10→N11, N15→N16, N20→N21) são cortes secos. Cada trecho começa da cena limpa; num render único, o `clear()` faria um fade de 0,9 s.
- O texto da narração não veio no handoff. As legendas são notas curtas da operação, e as pausas são estimadas.
- Inspeção por estados e junções, não quadro a quadro.
