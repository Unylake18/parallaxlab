# Lei de Faraday — Como um campo magnético cria um campo elétrico?

**STATUS: CENA (18 estados) E PREVIEW SILENCIOSO V4 (paleta da série, texto enxuto, end card) 960×540 / 15 fps PRONTOS (7:13) — SEM VOZ.** Preview: `media/videos/cena/540p15/LeiFaraday011.mp4`. Data: 2026-10-23. Física, ordem didática, storyboard e narração conceitual aprovados pelo chat de Produção. Não há voz, SRT, master, 1080p, capa nem publicação.

## Identificação

- id: `yt_0011` (ID escolhido pelo handoff; nenhuma pasta `yt_0011_*` existia em nenhum worktree. `yt_0001`–`yt_0008` existem entre `main` e os worktrees `parallax-long*`; `yt_0009` e `yt_0010` ainda não existem nos checkouts, mas ficam reservados para a sequência.)
- formato: `longo_horizontal`
- natureza: `teoria_visual`
- macroassunto: `eletromagnetismo`
- modulo: `inducao_eletromagnetica`
- solido_3d: `nenhum` — justificativa: o núcleo depende de controle quantitativo sincronizado de B(t), fluxo, circulação, campo elétrico induzido e do gráfico E(r); Manim 2D/2.5D dá esse controle e a sincronização melhor que um sólido do Blender.
- classe da cena: `LeiFaraday011` (`cena.py`)
- proporção: 16:9; preview 960×540 / 15 fps; final futuro 1920×1080 / 30 fps.
- duração: expectativa editorial 12–16 min (preview silencioso não persegue minutos; a voz fixará o ritmo).

## Pergunta central e tese

pergunta_central: **Se o circuito está completamente parado, o que empurra as cargas quando o campo magnético muda?**

Tensão do vídeo: `u = 0`, `I ≠ 0` ⇒ `u × B = 0` mas `ℰ ≠ 0`. O mecanismo novo é `∂B/∂t → E_induzido`, inequivocamente distinto da fem de movimento.

tese / payoff: **a circulação de E é `−dΦ_B/dt` (global); localmente `∇×E = −∂B/∂t`; mas rotacional zero localmente não significa campo nulo — fora do solenoide ideal B ≈ 0 e E ≠ 0. O fio não cria o campo: apenas revela sua existência.**

## Pré-requisitos essenciais

Fluxo magnético; força de Lorentz; fem de movimento (vídeo anterior da série); circulação de um campo vetorial; noção de rotacional (vídeo `yt_0003`).

## Física verificada (Ḃ > 0 e unidades de dB/dt = 1 na cena)

- Faraday (circuito estacionário): `∮_C E·dℓ = −dΦ_B/dt`.
- Exemplo cilíndrico: solenoide ideal muito longo, efeitos de borda desprezados; `B = B(t) ẑ` para `r < R`, desprezível para `r > R`. No modelo ideal, considerando o campo induzido associado à variação de B e sem acrescentar um campo eletrostático independente, a simetria leva a `E = E_φ(r) φ̂` (a simetria sozinha não excluiria um campo radial). Só neste exemplo as linhas de E são círculos concêntricos (não generalizar).
- Dentro: `Φ_B = Bπr²` ⇒ `E_φ = −(r/2) Ḃ`, `|E| ∝ r`.
- Fora: `Φ_B = BπR²` ⇒ `E_φ = −(R²/2r) Ḃ`, `|E| ∝ 1/r`.
- Continuidade: `E(R⁻) = E(R⁺) = −(R/2)Ḃ`. Limites: `E → 0` para `r → 0` e `r → ∞`. Unidades: `m·T/s = V/m`.
- Forma diferencial: `(∇×E)_z = (1/r) d(rE_φ)/dr` = `−Ḃ` dentro, `0` fora. Verificada numericamente em `_checagem_fisica()` de `cena.py`.

## Orientação e sinais (congelados)

`+ẑ` para fora da tela; `B = B(t) ẑ`; `Ḃ > 0`; contorno positivo anti-horário (`+φ̂`); logo `dΦ_B/dt > 0`, `∮E·dℓ < 0`, `E_φ < 0`: o campo induzido aponta no sentido **horário**. A convenção aparece (estado 9) antes da conta que usa o sinal (estado 10).

## Local × global (proteção)

Fora do solenoide ideal: `∂B/∂t = 0` localmente ⇒ `∇×E = 0` localmente, mas `E ≠ 0` e uma curva que envolve o solenoide tem `∮E·dℓ = −πR²Ḃ ≠ 0`. Sem contradição. Na tela: mensagem curta. No QA técnico (não na narração): a região exterior ao cilindro removido não é simplesmente conexa; uma curva que envolve o eixo não se contrai a um ponto dentro do exterior; qualquer superfície com esse bordo intercepta a região excluída se aplicarmos Stokes ao campo no espaço completo.

## Fora de escopo desta unidade

Indutância (`ℰ_L = −L dI/dt`), energia magnética (`U_B = ½LI²`, `u_B = B²/2μ₀`), Maxwell–Ampère: pertencem ao próximo vídeo (a ponte é só conceitual).

## Fases

Esta rodada: unidade documental + `cena.py` com 18 estados + preview silencioso. Próximo passo (só quando pedido): revisão do preview, narração final → voz → sync → SRT → master.
