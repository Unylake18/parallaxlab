# Produção — yt_0011 · Lei de Faraday

Fonte de verdade para reconstruir a cena (`cena.py`, classe `LeiFaraday011`). Física e roteiro: `ficha.md`, `storyboard.md`, `narracao.md`.

## Estrutura e execução

- `construct()` chama `s01()`…`s18()`; cada método é um estado do storyboard e abre uma seção (`begin(k, nome)`).
- `SO=10` (ou `SO=10,11`) renderiza só esses estados; os demais rodam em modo `skip_animations` (o estado anterior continua existindo como setup lógico).
- `GUIAS=1` liga a safe area em toda a cena: as guias ficam em `self.guias` e são preservadas por `wipe()`.
- Preview: `uv run python -m manim -r 960,540 --fps 15 --media_dir videos_longos/yt_0011_lei_faraday/media videos_longos/yt_0011_lei_faraday/cena.py LeiFaraday011`. A primeira execução compila todo o LaTeX (cache em `media/Tex`); `media/` fica dentro da unidade.
- Texto na tela: Space Grotesk via `screen_text`; matemática em `MathTex` com `TexTemplate` + `xcolor` (o template padrão do Manim não carrega `xcolor`); B/E coloridos com `\color[HTML]`.

## Modelo temporal vigente

Um único tempo físico, `tau` (`ValueTracker`). Funções, todas só de `tau`:

- `sfun(tau)`: dB/dt normalizado, smoothstep de 0 a 1 em `tau ∈ [0, W]` e constante depois.
- `bdot(tau) = BETA·sfun(tau)`: Ḃ(τ).
- `bfun(tau) = B0 + ∫₀^τ bdot`: B(τ), em forma fechada. `bdot` é a derivada exata de `bfun` (testado em `_checagem_temporal`).
- `carrier_phase(tau) ∝ bfun(tau) − B0`: posição angular dos portadores (carga deslocada ∝ ∫I dt ∝ B − B0).

Consequências:

- No trecho linear Ḃ = BETA constante: B cresce e, para geometria fixa, |E| fica constante (E depende de Ḃ, não de B).
- Pausa editorial = `tau` parado: B, ponteiro, portadores e setas de E congelam juntos; o quadro é uma fotografia da evolução, com Ḃ ≠ 0 naquele instante. Nada se move por `dt` de apresentação.
- Faixa usada: `tau ∈ [0; TAU_MAX = 2,2]` (`drift()` recusa valores acima; a checagem temporal varre toda essa faixa). Estados 1–6 evoluem `tau` crescente; do 9 em diante `tau` fica parado em 0,5.
- Opacidade de B é só mapeamento visual do valor físico: `min(bfun/B_VIS_MAX, 1)`, com `B_VIS_MAX = bfun(TAU_MAX)`, para não saturar antes do fim da evolução. Não altera B(τ) nem Ḃ(τ).
- Portadores (pontos âmbar): representam, de forma qualitativa, a corrente convencional / portadores positivos fictícios (movem-se no sentido de E; horário para Ḃ > 0 fora da tela). A velocidade visual não é um modelo quantitativo da velocidade de deriva nem da dinâmica completa do circuito (sem resistência quantitativa, autoindutância, RL ou reação sobre o campo). Esse aviso não vai à tela.

## Física espacial

`rT` é o raio do círculo de integração. Perfil com Ḃ = 1: `eabs(r) = r/2` (r < R), `R²/2r` (r > R); `eph(r) = −eabs(r)`. `_checagem_fisica()` (ao importar) confere sinais, continuidade em R, E(0) = 0, E(R/2) = E(2R) = R/4, E(R) = R/2, `∮E·dℓ = −dΦ/dt`, e `(∇×E)_z = (1/r) d(rE_φ)/dr` = −Ḃ dentro e 0 fora. Unidades: [r·Ḃ] = m·T/s = V/m.

`e_circle`: 12 setas fixas, comprimento ∝ |E_φ|(r)·sfun(tau); círculo e setas somem continuamente em r → 0.

## Objetos dinâmicos, gates e fades

Objetos com updater/`always_redraw` ignoram `FadeIn/FadeOut`; por isso um *gate* (`ValueTracker`) multiplica a opacidade e anima-se o gate.

- `Circuit` tem dois gates independentes: **`visB`** (região magnética: disco magenta e símbolos ⊙) e **`det`** (detector: espira, amperímetro, ponteiro, portadores, rótulo q). Estado 17: `det → 0`; `visB` não é tocado.
- `dyn(fn)` cria um objeto redesenhado por quadro com gate. `wipe()` zera os gates registrados em `self.reg`, faz FadeOut do resto (exceto marca, tag e guias) e remove tudo.
- Updaters de opacidade em textos (ramo ativo do estado 13) são limpos antes de qualquer fade.

## Paleta, texto e encerramento (padrão da série: yt_0003/0005/0006/0009)

- Cores: B magenta · E, ℰ (fem) e V ciano · I e J verde · carga azul (corpo `BLUE_L`, halo `BLUE`) · força `FC` · fluxo `FLUX` (`#D6CCFF`, yt_0003) · geometria, dℓ, S, C, r, R, A, u violeta · matéria (fio, amperímetro) `STEEL` · texto secundário `DIM`. Não existe amarelo/âmbar no vídeo.
- Texto de tela: Space Grotesk em CAIXA ALTA; minúsculas apenas ao definir variável (índice). Pouco texto: títulos curtos, nomes de fórmula final, rótulos específicos; a narração e a legenda explicam o resto. Variáveis novas entram num “ÍNDICE” (`defs()`) no topo da coluna direita (u, q, Φ_B, A, ℰ, E, C, dℓ, R, Ḃ, E_φ).
- Cargas 2.5D: esfera com halo, corpo e brilho especular; corrente = pulso verde atrás de cada carga (idioma do yt_0009); fio em tubo (sombra, corpo, realce); amperímetro com bisel, escala e ponteiro verde.
- Encerramento: o mesmo end card da série (yt_0005): anéis violeta tracejados, logo Parallax Lab centralizado (`parallax_lab_logo_horizontal.png`) e “PRÓXIMO VÍDEO: INDUTÂNCIA E ENERGIA MAGNÉTICA”. Sem texto de CTA (like/inscrição ficam só na narração).
- Auditoria de sobreposição antes de renderizar: `QA=1 uv run python -m manim -r 480,270 --fps 5 --dry_run ... LeiFaraday011` imprime `AUDIT` para qualquer interseção parcial entre textos, fórmulas e molduras e para conteúdo fora da área útil (não cobre texto × geometria; esses casos exigem olhar o quadro).

## Escolhas visuais e didáticas

- Sentido horário só aparece depois da convenção (+z fora da tela, +φ̂ anti-horário, estado 9); nos estados 1–8 a corrente/setas circulam no sentido horário (Lenz) sem invocar sinal.
- Estado 7: curva C genérica (não circular) com E local não tangente; estado 9: círculos concêntricos só depois da simetria.
- Glyph maps (MF-Tools) só nos estados 10 (`πr²/2πr → r/2`) e 12 (`πR²/2πr → R²/2r`). Estado 15 usa `TransformMatchingTex` com partes que casam; textos de passo trocam por fade sequencial.
- Estado 15: dℓ positivo (violeta, anti-horário) nunca usa a cor/direção de E real (ciano, horário).
- Estado 16: a razão topológica completa fica só neste arquivo, nunca na tela nem na narração. QA técnico: a região exterior ao solenoide não é simplesmente conexa; uma curva que envolve o eixo não se contrai a um ponto dentro do exterior, e toda superfície com esse bordo intercepta a região onde B varia. Modelo ideal: solenoide muito longo, campo imposto, regime quase-estático; a espira é detector passivo (sem reação sobre o campo nem autoindutância, assuntos do próximo vídeo).
- Estado 18: formulação qualificada global × local; CTA e ponte só depois do respiro do payoff; ponte sem fórmulas de indutância/energia.
- Branding: marca d’água e tag de série entram após o gancho (estado 1), como no `yt_0004`.
