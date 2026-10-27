# yt_0004 — Lei de Gauss + superposição

## Estado

**NARRAÇÃO, STORYBOARD E CENA (PREVIEW SILENCIOSO V3) PRONTOS — SEM VOZ.** Data: 2026-10-13. Física e arquitetura didática aprovadas pelo chat de Produção. Existem `cena.py` (classe `GaussSuperposicao004`) e um preview 960×540/15 fps; não há voz, SRT, master, 1080p, capa nem publicação.

## Estado (V3)

Escopo ampliado em 2026-10-13 a pedido do usuário: V3 silenciosa mais didática, para quem ainda não domina vetores (narração, storyboard e cena revisados em conjunto). Retiradas as restrições de preservar a narração da V1/V2 e de limitar o N05 a ~80 s. Física e arquitetura permanecem; ainda sem voz, SRT, master, 1080p, capa ou publicação.

## Identificação do ID

`yt_0004` confirmado pelo usuário em 2026-10-13: o `yt_0003` (divergente e rotacional do campo, delta de Dirac, noções de Stokes; fechamento da teoria) está planejado no PC pessoal e ainda não existe neste checkout. Este `yt_0004` passa a ser o bloco de exemplos mais elaborados de Gauss, mudança de planejamento aprovada pelo usuário. Slug: `yt_0004_gauss_superposicao`.

## Classificação

- id: `yt_0004`
- formato: `longo_horizontal`
- natureza: `exercicio_resolvido`
- curso: `Física III — Eletricidade e Magnetismo`
- macroassunto: `eletromagnetismo`
- modulo: `eletrostatica_lei_de_gauss_superposicao`
- duracao_alvo: `12–15 min (referência ≈ 14:15)` — revisão V3, mais didática (antes: ~9:30–10:30)
- solido_3d: `nenhum` — justificativa: o conteúdo depende de vetores posição, transparências, sobreposição de distribuições, movimento do ponto P e relações geométricas; 2D/2.5D em Manim comunica melhor que um sólido Blender.
- proporção: 16:9; preview futuro 960×540 / 15 fps; final futuro 1920×1080 / 30 fps.

## Fonte e distinção editorial

- Problema principal: Griffiths, 3ª ed., Problema 2.18 (duas esferas de mesmo raio, +ρ e −ρ; mostrar campo constante na sobreposição). Sem página ou citação literal.
- **Cavidade esférica deslocada: generalização do Parallax Lab** (mesmo princípio de superposição). Não é enunciado do Griffiths.
- **Analogia 1D fora do roteiro principal**; só contingência de rodada futura.

## Pergunta, payoff e arquitetura

pergunta_central: **Duas esferas carregadas se sobrepõem, uma com +ρ e outra com −ρ. Qual é o campo na região comum — e muda se o ponto mudar?**

payoff_principal: **A Lei de Gauss não falhou: falhou a simetria da configuração inteira. Uma configuração difícil se reconstrói como soma ou diferença de configurações simples que sabemos resolver: geometria difícil → decomposição → problemas simétricos → superposição.**

Resultado: `E⃗ = (ρ/3ε₀) d⃗` (uniforme) na sobreposição; `E⃗_cav = (ρ/3ε₀) d⃗` na cavidade esférica deslocada (condição `a + |d⃗| < R`).

Arquitetura (16 blocos, N01–N16): pergunta → conflito (Gauss válida, E direto não) → superposição → ferramenta `E⃗ = C r⃗` (~2:10, V3) → vetores `r⃗₊ = d⃗ + r⃗₋` → soma `E⃗ = C d⃗` → mover P → `ΔE⃗ = 0` → −ρ como carga removida → cavidade → limites → checagens → estratégia.

## Pré-requisitos

yt_0001 e yt_0002 (fluxo, gaussiana, simetria, `Q_env`). Vetores e superposição básica.

## Estimativa

V3: 1568 palavras na narração integral (N01–N16); ≈ 10 min de fala a 150 palavras/min, mais pausas e construções; referência 14:15, faixa 12–15 min. Preview silencioso V3 renderizado (ver `storyboard.md`, seção V3); cronometragem de voz pendente.

## Checagens físicas registradas

`d⃗=0 ⇒ E⃗=0`; `ρ→0 ⇒ E⃗→0`; trocar sinais inverte E⃗; `[ρd/ε₀]=N/C`. Detalhe em `producao.md` §4.

## Pacote

`producao.md` (solução, limites, decisões, portas, QA reservado), `narracao.md` (texto integral N01–N16), `storyboard.md` (blocos com objetivo, fala, tela, movimento, estado final, duração).

## Pendências reais

Cronometragem de voz; legibilidade em preview; verificação visual do movimento de P; render. Pertencem às fases posteriores, que só abrem com handoff explícito.
