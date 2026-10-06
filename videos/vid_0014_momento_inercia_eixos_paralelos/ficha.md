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
status: preview Manim V5 (silencioso; sem voz, SRT, capa, final ou publicação)
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

## Storyboard resumido (15 blocos, V5)

1 gancho (eixo do centro à ponta, `I: 1× → 4×`) · 2 `v = ωr_⊥` com `dm` móvel · 3 `r²` nasce · 4 1:4:9 · 5 soma → integral → `I` · 6 `r_⊥ = |x|` e barra uniforme · 7 `I_CM` · 8 eixo por `d`, `x' = x − d` · 9 expansão de `(x−d)²`, `d` constante, `I_CM` e `M` · 10 termo cruzado nulo · 11 Steiner · 12 ponta · 13 comparação 4× · 14 síntese · 15 CTA. Detalhes em `roteiro.md`.

## V5 (polimento de ritmo e escala sobre a V4; matemática idêntica)

- **Abertura (0–15 s):** um estado por vez e mais permanência: título (com `EIXO` em ciano) → "centro → ponta" com o eixo deslizando (sem "só o eixo mudou") → `I_ponta = 4I_CM ?` e "de onde vem esse 4?" → mapa das duas perguntas entrando completo; a 2ª esmaece e a 1ª fica destacada ao começar o giro.
- **Escala:** payoffs, equações principais e de apoio com tamanhos normalizados por largura máxima (`w`): `dK` e `K` ~6 un.; `I = ∫r_⊥²dm` e `K = ½Iω²` menores; `r_⊥ = |x|`, `dm = λdx`, `dm = (M/L)dx` reduzidos; `I_CM` 80 (box mantido); expansão e equação distribuída com margem; `∫x dm = Mx_CM = 0` sem box e saindo logo após o `0`; Steiner 76; passos da ponta 52 e resultado 60; `I_ponta = 4I_CM` 68.
- **Notas aumentadas:** "mesmo dm • mesma ω", "mais pedaços, cada Δm menor", `r_⊥ = distância…`, texto de `I_CM`, "d é constante", "x' é coordenada com sinal", "origem escolhida no CM", condições de Steiner, síntese.
- **Cortes:** "Não." isolado; cópia de `∫r_⊥²dm` por cima do original (agora destaque na equação de K e entrada da definição); legenda `= 1/3 ML²` na comparação; box da identidade do CM e box de `I_ponta = 1/3 ML²`.
- **Comparação final:** "cada bloco = 1/12 ML²" sozinho, depois `I_CM` (1 bloco) e `I_ponta = 4/12 ML²` (4 blocos), depois `I_ponta = 4I_CM`.
- **Síntese e CTA:** síntese sem barra; símbolo + `@labparallax` entra logo após (~2,4 s).

## QA físico (checklist do briefing)

Conferido na implementação: r perpendicular ao eixo; ω única; `v=ωr`; `r²` de `v∝r` + `K∝v²`; massas iguais em 1:4:9; barra constante; `I_CM = ML²/12`; eixos paralelos; d perpendicular entre eixos; `x−d` como coordenada relativa; termo cruzado visível até a justificativa; `∫x dm = Mx_CM = 0` na tela, com a razão "origem no CM, não a simetria"; Steiner só depois do CM; sem eixos inclinados; `d = L/2`; `I_ponta = ML²/3 = 4I_CM`; sem τ=Iα, tensor, torque ou momento angular. Revisão humana pendente.

## QA visual

Preview V5 540×960 / 15 fps renderizado (≈ 169 s). Inspecionados quadros de abertura, `v = ωr_⊥`, `r²`, 1:4:9, soma → integral, ponte `r_⊥ → x`, `I_CM`, eixo e `x' = x − d`, expansão, identificação de `I_CM` e `M`, termo cruzado, Steiner, ponta, comparação 4×, síntese e CTA. Pendências: revisão humana em movimento; legibilidade em celular não comprovada; duração depende da futura voz.

## Narração aprovada

Ver `roteiro.md` (texto completo e referência de timing). Voz, SRT, capa, final e publicação **não** iniciados.
