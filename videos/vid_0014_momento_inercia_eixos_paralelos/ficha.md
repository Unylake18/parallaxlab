# vid_0014 — Por que o eixo muda o momento de inércia?

```
id: vid_0014
serie: POR TRÁS DA FÓRMULA · EP. 05
formato: curto_vertical
area: Física I / Mecânica
tema: Momento de inércia e Teorema dos Eixos Paralelos
headline: POR QUE O EIXO MUDA O MOMENTO DE INÉRCIA?
pergunta_central: Por que a distância ao eixo entra ao quadrado no momento de inércia — e por que mover esse eixo acrescenta exatamente Md²?
duracao_alvo: ~165–170 s
status: final 1080×1920 gerado (master limpo e legendado em renders/, 2026-10-06); capa escolhida: `capa_instagram.png` (as 12 propostas foram descartadas); publicação não iniciada
```

- Cena: `cena.py`, classe `MomentoInercia014`. `ATE=k` (1–17) renderiza só até o bloco k.
- Roteiro e narração aprovada: `roteiro.md`.
- Preview: `uv run python -m manim -r 540,960 --fps 15 videos/vid_0014_momento_inercia_eixos_paralelos/cena.py MomentoInercia014`.

## Hipóteses

Barra fina, rígida, homogênea, massa total M, comprimento L. Eixo perpendicular à barra, primeiro pelo centro de massa; depois deslocado paralelamente por d (caso final d = L/2). Em rotação rígida há uma única ω; r é a distância perpendicular ao eixo.

## Solução verificada

- `v = ωr`, `dK = ½v²dm = ½ω²r²dm`, `K = ½ω² ∫r²dm`, logo `I = ∫r²dm` e `K = ½Iω²` (a combinação aparece naturalmente na energia cinética; sem apresentar I como definição arbitrária).
- `dm = (M/L)dx`; `∫_{-L/2}^{L/2} x² dx = L³/12`; `I_CM = (1/12)ML²`.
- Eixo deslocado: `x' = x − d` (coordenada com sinal; só `(x−d)²` importa). `I' = ∫(x−d)²dm = ∫x²dm − 2d∫x dm + d²∫dm`.
- `∫x dm = M x_CM = 0` porque a origem foi escolhida no CM (não depende da simetria da barra). Logo `I' = I_CM + Md²`.
- Ponta: `d = L/2`; `I = (1/12 + 3/12)ML² = (1/3)ML²`; razão `(1/3)/(1/12) = 4`: `I_ponta = 4I_CM`.
- Dimensões: `[I] = ML²`.

## Payoff

Fechar o gancho: o fator 4 é `1 + 3`, com `3 I_CM = M(L/2)²` vindo de mudar o eixo (`Md²`), e `r²` vindo da rotação.

## Equações centrais

`v=ωr` · `dK=½v²dm` · `dK=½ω²r²dm` · `K=½ω²∫r²dm` · `I=∫r²dm` · `K=½Iω²` · `dm=(M/L)dx` · `I_CM=(M/L)∫x²dx=(1/12)ML²` · `x'=x−d` · `I'=∫(x−d)²dm` · `I'=∫x²dm−2d∫x dm+d²∫dm` · `∫x dm=Mx_CM=0` · `I'=I_CM+Md²` · `I_ponta=(1/3)ML²=4I_CM`.

## Voz, sincronia e legenda (preview)

- Voz: `audio/narracao_final.wav` (ElevenLabs, 174,16 s, estéreo 44,1 kHz; arquivo recebido do Produção, sem edição). Texto lido: `texto_narracao.txt` (498 palavras; versão V3 do texto em `narracao_sugestao.md`).
- Sincronia por âncoras (sem ASR, como nos vídeos 11/12): `gerar_sync.py` alinha o texto ao WAV (sílabas + pausas medidas) e gera `sync.json` (56 âncoras, uma por sentença/ideia visual) e `legenda.srt` (69 cues, ≤ 2 linhas). `native.json` guarda o tempo nominal de cada âncora; refazer só se a cena ou o áudio mudarem: `uv run python videos/vid_0014_momento_inercia_eixos_paralelos/gerar_sync.py` e `SYNC_CAL=1 uv run python -m manim -r 108,192 --fps 5 videos/vid_0014_momento_inercia_eixos_paralelos/cena.py MomentoInercia014`.
- Cena: `ancora("bNx")` em cada ponto de fala; `play`/`wait` escalados entre âncoras (0,45–2,0×); `until`/`seg` viraram no-op. A barra para de girar pouco antes de "Na barra uniforme" (duração da fase de giro vem de `sync.json`). Ordem de b2, b8 e b10 ajustada para seguir a fala (seta de velocidade antes do raio; eixo desliza em "paralelamente"; varredura do `dm` antes da identidade do centro de massa). Render sincronizado sem `SYNC atraso`.
- Preview sincronizado (540×960, 15 fps, 174,6 s): `media/videos/cena/960p15/vid_0014_preview_sync_master.mp4` (com áudio) e `..._legendado.mp4` (legenda queimada, `--style solid --color-module cena.py`; termos coloridos por `SUBTITLE_TERM_COLORS`). Final 1080×1920 e master/legendado definitivos **não** gerados.

## Storyboard resumido (15 blocos, V6)

1 gancho (eixo do centro à ponta, `I: 1× → 4×`) · 2 `v = ωr_⊥` com `dm` móvel · 3 `r²` nasce · 4 1:4:9 · 5 soma → integral → `I` · 6 `r_⊥ = |x|` e barra uniforme · 7 `I_CM` · 8 eixo por `d`, `x' = x − d` · 9 expansão de `(x−d)²`, `d` constante, `I_CM` e `M` · 10 termo cruzado nulo · 11 Steiner · 12 ponta · 13 comparação 4× · 14 síntese · 15 CTA. Detalhes em `roteiro.md`.

## V6 (movimento e continuidade; escala e conteúdo da V5)

- **Termo a termo (MF-Tools `TransformByGlyphMap` + cópias):** `v² → (ωr_⊥)² → ω²r_⊥²`; `Σ r_i²Δm_i → ∫r_⊥²dm` (`½ω²` fica); `I` copiado da integral de `K` e `K = ½Iω²`; `r_⊥ → r_⊥²` e `|x| → x²`; `M/L` copiado para o lugar de `λ`; `dm → dx` com `M/L` saindo da integral e limites copiados do eixo `x`; `x² → x³/3`; `x−d` copiado para dentro de `(x')²`; `(x−d)²` copiado, expansão e entrada na integral; distribuição em três integrais e `d` fora (`d é constante`); `∫x dm` copiado do termo cruzado → `Mx_CM`; o `0` de `x_CM = 0` copiado para `−2d·0`; `Steiner` sobra da equação anterior; `L/2` copiado da seta para `M(L/2)²`; `1/4 → 3/12 → (1+3)/12 → 4/12 → 1/3`.
- **Fade por segurança (estado completo → estado completo):** avaliação final `[x³/3] → ML²/12`, `(x−d)²` isolado → igualdade completa, `I_CM`/`M` por chaves.
- **Mapa cromático:** `v` e seta de velocidade em azul elétrico; `ω` e `r_⊥`/`r`/`x` em ciano; `d`, `d²` e `Md²` em violeta; termo cruzado em magenta; `dm`/`Δm` neutros; ciano para `I`, `I_CM`, `I_ponta`. Na cena `r, 2r, 3r` as cores são do caso (ciano/violeta/magenta), e a barra volta ao padrão global ao sair dela.
- **Blocos finais:** a fórmula `I_ponta = I_CM + Md²` gera os blocos; "cada bloco, de qualquer cor = 1/12 ML²" com unidade neutra (contorno branco); quatro blocos idênticos com divisórias; ciano = `I_CM` (1/12 ML²), violeta = `Md²` (3/12 ML²), rótulos maiores e sem esmaecer; `I_ponta = 4/12 ML²` sai quando `I_ponta = 4I_CM` entra. A cor indica origem, não valor.
- **Polimento pós-V6:** o 4 da pergunta inicial em ciano; vetores e rótulos `v, 2v, 3v` sempre azuis (só pontos, `r, 2r, 3r` e barras 1×/4×/9× mudam de cor por caso); condição de Steiner com `CM` ciano e `d` violeta; síntese com "ao quadrado" ciano e `Md²` violeta; `x_CM = 0` separado do rótulo `CM`; notas de `x'` maiores e mais longas; limites da integral entram só depois de `dm → dx`; distribuição da integral abre espaço antes; `∫x²dm → I_CM` assenta antes de `∫dm → M`; `ML²` único como destino na soma das frações; `4/12 → 1/3` só na fração.

## QA físico (checklist do briefing)

Conferido na implementação: r perpendicular ao eixo; ω única; `v=ωr`; `r²` de `v∝r` + `K∝v²`; massas iguais em 1:4:9; barra constante; `I_CM = ML²/12`; eixos paralelos; d perpendicular entre eixos; `x−d` como coordenada relativa; termo cruzado visível até a justificativa; `∫x dm = Mx_CM = 0` na tela, com a razão "origem no CM, não a simetria"; Steiner só depois do CM; sem eixos inclinados; `d = L/2`; `I_ponta = ML²/3 = 4I_CM`; sem τ=Iα, tensor, torque ou momento angular. Revisão humana pendente.

## QA visual

Preview V6 (polido) 540×960 / 15 fps renderizado (≈ 169 s); movimento conferido em tiras de 0,3 s nos trechos alterados (revisão por frames, não em reprodução contínua). Inspecionados quadros de abertura, `v = ωr_⊥`, `r²`, 1:4:9, soma → integral, ponte `r_⊥ → x`, `I_CM`, eixo e `x' = x − d`, expansão, identificação de `I_CM` e `M`, termo cruzado, Steiner, ponta, comparação 4×, síntese e CTA. Pendências: revisão humana em movimento; legibilidade em celular não comprovada; duração depende da futura voz.

## Narração aprovada

Ver `roteiro.md` (texto completo e referência de timing). Voz, SRT, capa, final e publicação **não** iniciados.

## Final e capas (2026-10-06)
- Render: `uv run python -m manim -r 1080,1920 --fps 30 videos/vid_0014_momento_inercia_eixos_paralelos/cena.py MomentoInercia014` (174,59 s, sem atraso de sincronia).
- Master: `renders/vid_0014_momento_inercia_eixos_paralelos_final_master_limpo.mp4` (1080×1920, 30 fps, áudio 174,16 s); legendado: `..._final_legendado.mp4` (69 cues, `--color-module cena.py`). Fora do Git.
- Capas: `gerar_capa.py` → `capas/capa_01..06.png` (painel padrão da série); `gerar_capa_v2.py` → `capas_v2/capa_v2_01..06.png` (painel maior, algumas sem moldura). Escolha pendente.

