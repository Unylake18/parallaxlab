# Produção — yt_0004 · Gauss + superposição

Data: 2026-10-13. Escopo: pré-produção editorial. Física, estratégia e arquitetura didática aprovadas pelo chat de Produção; nada aqui as reabre. Fala: `narracao.md`; tela: `storyboard.md`; consolidação: `ficha.md`.

## 1. Fonte e distinção editorial

- Problema principal: **Griffiths, *Introduction to Electrodynamics*, 3ª ed., Problema 2.18**: duas esferas de mesmo raio, parcialmente sobrepostas, densidades volumétricas uniformes `+ρ` e `−ρ`; mostrar que o campo na região de sobreposição é constante. Sem número de página nem citação literal (PDF não consultado).
- **A cavidade deslocada é uma generalização do Parallax Lab**, construída pelo mesmo princípio de superposição. Nunca apresentá-la como enunciado do Griffiths.

## 2. Modelo

Eletrostática no vácuo. As duas esferas do problema são distribuições volumétricas idealizadas de carga, de densidade uniforme; a sobreposição é uma construção matemática, não a descrição de dois corpos materiais impenetráveis ocupando o mesmo espaço (o mesmo raciocínio permite, depois, escrever a cavidade como +ρ + (−ρ)). “Esfera negativa” e “esfera fictícia” são decomposições do campo, não carga adicional.

## 3. Solução verificada

**Campo interno (ferramenta).** Gaussiana esférica de raio `r<R` concêntrica: `Q_env = ρ(4/3)πr³`; `E·4πr² = Q_env/ε₀` ⇒ `E = ρr/3ε₀`. Com `E⃗ = E r̂` e `r⃗ = r r̂`: `E⃗ = (ρ/3ε₀) r⃗ = C r⃗`, `C = ρ/3ε₀`. Vale para qualquer `r` interno; `R` não aparece.

**Griffiths 2.18.** `O₊` (+ρ), `O₋` (−ρ), `d⃗ = O₊→O₋`, `P` na região comum (`|r⃗₊|<R`, `|r⃗₋|<R`).
- `r⃗₊ = d⃗ + r⃗₋` ⇒ `r⃗₊ − r⃗₋ = d⃗`.
- `E⃗₊ = C r⃗₊` (para fora de O₊); `E⃗₋ = −C r⃗₋` (para O₋).
- `E⃗ = C(r⃗₊ − r⃗₋) = C d⃗ = (ρ/3ε₀) d⃗`: uniforme; direção de O₊ para O₋.
- Uniformidade: `Δr⃗₊ = Δr⃗₋` (mesmo P, centros fixos) ⇒ `ΔE⃗ = C Δr⃗₊ − C Δr⃗₋ = 0`.
- Observação: na lente `ρ_total = 0` e `E ≠ 0` (a neutralidade local não implica campo nulo).

**Cavidade (generalização).** Esfera maciça isolante, raio `R`, densidade uniforme `ρ`; cavidade esférica de raio `a`, centro deslocado por `d⃗` do centro grande; condição estrita `a + |d⃗| < R`. Decomposição: esfera cheia `+ρ` (raio R) + esfera fictícia `−ρ` (raio a, centro na cavidade). Em `P` na cavidade: `r⃗ = d⃗ + r⃗'`; `E⃗ = C r⃗ − C r⃗' = C d⃗ = (ρ/3ε₀) d⃗`. Como `a + |d⃗| < R`, todo ponto da cavidade está dentro da esfera grande; a fórmula interna vale para cada esfera no seu domínio. Não generalizar para cavidades não esféricas ou densidade não uniforme.

## 4. Checagens físicas (para a ficha; narradas de forma curta em N16)

| Checagem | Resultado |
| --- | --- |
| `d⃗ = 0` | `E⃗ = 0` (cavidade concêntrica; esferas coincidentes) |
| `ρ → 0` | `E⃗ → 0` |
| trocar `+ρ ↔ −ρ` | `E⃗` inverte (`C → −C`) |
| unidades | `[ρ d/ε₀] = (C/m³)(m)/(C²/N·m²) = N/C` ✓ |

## 5. Limites (N15)

Superposição vale sempre; utilidade depende de resolver as partes. Uniformidade decorre de: ρ original uniforme; cavidade esférica; E linear em `r⃗`; mesmo `|C|`; `r⃗ − r⃗' = d⃗` fixo. Proibido: “toda cavidade produz campo uniforme”; “qualquer geometria sem simetria resolve-se assim”; “Gauss não funciona”.

## 6. Decisões e restrições

- `solido_3d: nenhum`: vetores posição, transparências, sobreposição e movimento de P comunicam melhor em 2D/2.5D no Manim.
- Analogia 1D (`Cx − C(x−d) = Cd`) **fora do roteiro**; contingência para nova rodada, caso a relação vetorial se mostre pouco clara na implementação.
- Linguagem: isolante; não usar o vocabulário de condutor.
- Equações públicas: `ρ_total=ρ₁+ρ₂ ⇒ E_total=E₁+E₂`; `Q_env=ρ(4/3)πr³`; `E·4πr²=Q_env/ε₀`; `E=ρr/3ε₀`; `E⃗=(ρ/3ε₀)r⃗`; `C=ρ/3ε₀`; `r⃗₊=d⃗+r⃗₋`; `E⃗₊=Cr⃗₊`; `E⃗₋=−Cr⃗₋`; `E⃗=Cd⃗`; `ΔE⃗=0`; `r⃗=d⃗+r⃗'`; `E⃗_cav=(ρ/3ε₀)d⃗`; `a+|d⃗|<R`.
- `Q_env` / carga envolvida, como nos yt_0001/yt_0002.
- Glyph maps (MF-Tools) só após o LaTeX estabilizado; padrão `TransformMatchingTex`.

## 7. Continuidade visual

Seguir yt_0001/yt_0002 e helpers horizontais vigentes: header, watermark, margens, cores (azul fonte, ciano campo, violeta gaussiana, magenta para negativa/fictícia, branco para vetores posição), 960×540/15 fps no preview e 1920×1080/30 fps no final. Nenhuma alteração em `template/` ou `assets/`.

## 8. Portas de implementação futuras

| Unidade | Blocos | Critério |
| --- | --- | --- |
| Abertura e conflito | N01–N04 | Desconforto antes da resposta; Gauss nunca “falha” |
| Ferramenta | N05 | ~80 s; sem integral de volume |
| Vetores | N06–N07 | Geometria antes da álgebra; setas ponta com cauda |
| Resultado e P móvel | N08–N11 | E_total idêntico em todas as posições; ΔE⃗=0 |
| Generalização | N12–N14 | Cavidade ≠ enunciado Griffiths; `a+|d⃗|<R` |
| Fechamento | N15–N16 | Limites; checagens; cadeia final |
| Integração | todos | QA completo; sincronia real só com voz |

Cada porta só abre com handoff explícito.

## 9. QA reservado (fases futuras)

Legibilidade de `r⃗₊/r⃗₋/d⃗` em 960×540; atualização simultânea no movimento de P; o `E⃗_total` realmente imóvel; ausência de índices de debug; duração real × alvo.

## 10. Estimativa (V3)

Narração: 1568 palavras, 16 blocos. A 150 palavras/min ≈ 10 min de fala; com pausas, leituras e construções, referência ≈ 14:15 (faixa 12–15 min). Distribuição: N01–N04 ≈ 2:35; N05 ≈ 2:10; N06–N09 ≈ 3:50; N10–N11 ≈ 1:40; N12–N14 ≈ 2:55; N15–N16 ≈ 1:05. O tempo extra veio de definições, construções geométricas e comparações, não de esperas.

## 11. Escopo didático V3

Mapa de variáveis ligado ao desenho (símbolo + descrição + elemento geométrico, um de cada vez) nos dois problemas; anatomia do vetor (início, ponta, comprimento = distância, direção e sentido); soma ponta com cauda; vetor oposto; C como abreviação; distância (vetor posição) × intensidade (campo) em escalas distintas; marcador de percurso (anel) distinto de P; P como "o lugar onde calculamos o campo"; Δ = depois − antes; R ≠ r e r⃗′ com apóstrofo = outra origem (não derivada); comparações de parâmetros (a, direção de d⃗, |d⃗|, d⃗ = 0, sinal de ρ). Fora do escopo: cavidade não esférica (apenas sinalizada como "sem garantia").
