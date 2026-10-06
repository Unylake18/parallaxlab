# vid_0012 — O campo máximo está na superfície?

- Série pública: **EXERCÍCIO RESOLVIDO · EP. 05**. Headline: “O CAMPO MÁXIMO ESTÁ NA SUPERFÍCIE?”.
- **Vídeo final aprovado em 2026-10-02** (voz, sincronia por âncoras, legenda colorida, master e legendado). **2026-10-03: termo trocado para carga envolvida, Q_env** (voz regravada, sincronia, legenda, final e capa 6 refeitos; finais anteriores guardados com sufixo `_qenc`). **Pendentes: capa e publicação** (seguem em outro computador).
- Final: `renders/vid_0012_campo_esfera_nao_uniforme_final_master_limpo.mp4` e `..._final_legendado.mp4` — 1080×1920, 30 fps, 4.978 quadros, 165,92 s; AAC estéreo 165,04 s (o último quadro fica além da fala para o handle ficar legível). Preview silencioso anterior: 540×960, 15 fps, 170,9 s (`renders/..._preview_final.mp4`).
- Problema: esfera isolante de raio R, ρ(r) = ρ0 (1 − r/R) para r ≤ R, ρ = 0 fora. Campo E(r) em todo o espaço e onde o módulo é máximo.
- Cena: `cena.py`, classe `CampoEsfera012` (módulo único; `Eq` local para os mapas de glifos do MF-Tools).
- Comando do preview: `uv run python -m manim -r 540,960 --fps 15 videos/vid_0012_campo_esfera_nao_uniforme/cena.py CampoEsfera012`. `ATE=k` (1–12) renderiza só até o segmento k. Saída: `media/videos/cena/960p15/CampoEsfera012.mp4`. Pranchas de QA em `frames_preview/`.
- Texto da voz e notas de gravação (pausas): `texto_narracao.txt`, `narracao_sugestao.md`.

## Matemática (aprovada)

- Gauss: ∮E⃗·dA⃗ = Q_env/ε0; E ∥ dA (θ = 0, cos 0 = 1) e |E| constante na gaussiana ⇒ E 4πr² = Q_env(r)/ε0.
- Cascas: dV = 4πr'² dr', dQ = ρ(r') dV; Q_env(r) = 4πρ0 (r³/3 − r⁴/4R); E_in = (ρ0/ε0)(r/3 − r²/4R); Q = πρ0R³/3; E_out = ρ0R³/(12ε0 r²).
- dE/dr = (ρ0/ε0)[d/dr(r/3) − d/dr(r²/4R)] = (ρ0/ε0)(1/3 − 2r/4R) = (ρ0/ε0)(1/3 − r/2R); = 0 ⇒ 1/3 = r/2R ⇒ 3r = 2R ⇒ r_max = 2R/3; E'' = −ρ0/(2Rε0) < 0.
- E(R) = ρ0R/(12ε0); E_max = ρ0R/(9ε0) = (4/3) E(R) (valor de E_max não aparece). QA somente: E'(R⁻) = E'(R⁺) = −ρ0/(6ε0).
- `_qa()` no `cena.py` (roda ao importar): integral numérica das cascas × fórmula, Gauss, E(0) = 0, E(2R/3), E(R), razão 4/3, continuidade de E e E' em R, E″ < 0, E → 0, máximo global em 2R/3, 0 < 2R/3 < R, derivada termo a termo, 3r = 2R, versão adimensional do gráfico e a interpretação por Δr.

## V2.1 — o que mudou em relação à V2

- **Layout dinâmico (estados com posições absolutas e transições animadas):** SOLO_CENTER (esfera sozinha no centro: S1–S3 e S10–S12), PRIMARY_LEFT (esfera à esquerda só enquanto a definição de ρ e a casca aberta estão à direita: S4–S5), SPHERE_GRAPH (esfera centrada sobre o gráfico, ambos no eixo central: S6–S7, S10–S12), MATH_FOCUS (esfera pequena no canto só durante a função por partes e a derivação: S8–S9). Gráfico centrado em x = 0 (GX0 = −GSX·XMAX/2), maior (GSX = 2,0), rótulos posicionados à parte. Sem `next_to` encadeado nem grupos com itens já removidos; nenhum objeto com opacidade zero influencia posição.
- **Lei de Gauss por geometria (S3):** gaussiana tracejada violeta de raio r (raio marcado); 6 vetores E⃗ ciano sobre a gaussiana (mesmo comprimento); 4 vetores d⃗A lavanda, menores e ao lado; um ponto destacado (35°) com patch dA (arco na gaussiana), normal n̂ (lavanda, radial, para fora), E⃗ paralelo; o rótulo n̂ vira d⃗A e a equação `d⃗A = n̂ dA` nasce por cópia dos glifos dos rótulos; `E⃗ ∥ d⃗A ⇒ θ = 0`; `E⃗·d⃗A = E dA cos θ → cos 0 = 1 → E dA` (cópias de glifos de ∮E⃗·d⃗A); todos os vetores voltam (E⃗ ∥ d⃗A e |E⃗| = E(r) em toda a gaussiana); ∮E dA → E∮dA → E·4πr² (a gaussiana se destaca: ∮dA = área da esfera = 4πr²) → E 4πr² = Q_env(r)/ε0, linha que persiste até o fim das contas.
- **Cascas (S4):** etapa A (r' cresce, círculos r' e r'+dr', faixa fina), etapa B (a casca se abre: área × espessura ⇒ dV), etapa C (a casca aberta sai; dQ = ρ(r')dV reaproveita dV e o dQ da integral). Menos coisas ao mesmo tempo, sem glifos sobrepostos.
- **Q_env → E_in (S6):** o resultado volta ao Gauss; 4π (dos dois lados) é riscado e aparece `÷ 4πr²`; depois a transformação até E_in(r).
- **r = R e campo externo (S7):** x chega a 1 (gaussiana = superfície, ponto na fronteira), Q = Q_env(R) = πρ0R³/3; E_in vira um rótulo do ramo interno; E_in(r) vira E_out(r) (cópia de glifos) enquanto a gaussiana cresce para fora e o ponto continua pelo ramo externo; E_out vira rótulo do ramo externo; sem caixas concorrentes.
- **Derivação (S9):** dE/dr = (ρ0/ε0)[d/dr(r/3) − d/dr(r²/4R)] → 1/3 − 2r/4R → 1/3 − r/2R (termo a termo); tangente dinâmica (> 0 até o pico); só então `dE/dr = 0`; ρ0/ε0 > 0; `1/3 − r/2R = 0 → 1/3 = r/2R → 3r = 2R → r = 2R/3` (r atravessa a igualdade).
- **Interpretação (S11):** sem números. O mesmo Δr perto do centro (ρ é grande, Q_env cresce mais que r² → E aumenta) e perto da borda (ρ já é pequena, Q_env cresce menos que r² → E diminui); brilho da casca nova ∝ ρ local; o ponto sobe e depois desce.
- **Checagens (S12):** E(0)=0 → E(R⁻)=E(R⁺) → E(r)→0 no mesmo gráfico, e a frase final.
- Tracker único `x = r/R` (T.X) e curva revelada por ele (T.RV). Sem guia esfera–gráfico (a esfera agora é centrada e não compartilha escala com o gráfico).

## V2.2 — acabamento final

- **Interpretação (S11):** o gráfico desce 0,55 (sempre centrado em x = 0) só durante a interpretação e volta em S12; frases em duas linhas com espaço: “Perto do centro: ρ é grande / Q_env cresce rápido o suficiente → E aumenta” e “Perto da borda: ρ já é pequena / Q_env cresce devagar demais → E diminui”; sem comparar Q_env e r² como grandezas soltas (a fórmula já dá o contexto). Tracker/gráfico: `GTR` (deslocamento) lido por `gpt()`.
- **Gauss:** rótulos n̂/d⃗A e E⃗ mais separados (direções e cores inalteradas).
- **Resumo (S13):** Gauss → Q_env(r) → E(r), seta para dE/dr = 0 e depois r_max = 2R/3 (caixa maior com brilho ciano), animados em sequência; esfera, gráfico e conta saem antes; frase final “A distribuição de carga muda / onde o campo é mais intenso.” (segunda linha em ciano).
- **CTA (S14):** logo Parallax Lab (recortado de `assets/branding/overlays/parallax_lab_logo_horizontal.png`), “Para mais física assim, siga @labparallax” (@labparallax em gradiente ciano, dentro da safe area); some a tag da série e a marca d'água para não duplicar branding. Fala: “Se curtiu, segue o arroba labparallax.” (a voz repete o handle que a tela mostra; `texto_narracao.txt`, `narracao_sugestao.md`).
- Respiro de 1,5 s depois do payoff e checagens mais curtas (sem mini-slides).

## Polish final de tipografia e layout (preview final, 170,9 s)

- Hierarquia fixa a partir de 1:37: equações principais > resultado destacado > texto explicativo > rótulos auxiliares. “Encontramos o campo / Mas o exercício ainda não acabou” 34 → 28 (mais respiro vertical); “E_out ∝ 1/r² só diminui” 40/28 → 34/24; dedução de r = 2R/3 em tamanho intermediário (70 → 50; só o payoff mantém 70); interpretação 26/24 → 22/20 (duas linhas, mais espaçamento).
- Gráfico: desce 0,5 na derivação (S9) e 0,75 na interpretação (S11), sempre centrado (`gshift`); marcas do eixo ocultas só em S11; E₀ **oculto** em S9 (derivação) e discreto fora do payoff; o gráfico volta à posição normal no payoff e nas checagens.
- Vetores E⃗ de S11 encurtados (FL = 0,55) e a fórmula subiu/desceu para não encostar na esfera. Cadeia da resolução e nota ρ0/ε0 > 0 reposicionadas para não colidir.
- Resumo e CTA intactos.
- Removida a frase “não é linear: parábola côncava para baixo” (S6, ~1:20): encostava na caixa de E_in(r) e não havia espaço livre até o gráfico. A curva já mostra a parábola; a fala “É uma parábola côncava para baixo” continua em `texto_narracao.txt`. Tempos inalterados (170,9 s).

## Voz, sincronia e legenda

- Narração: `audio/narracao_final.wav` (ElevenLabs, take Q_env de 2026-10-03, 165,04 s, estéreo 44,1 kHz, intacta; take anterior em `audio/narracao_final_qenc_antiga.wav`; texto em `texto_narracao.txt`, 14 parágrafos).
- Sincronia (como nos vídeos 0009–0011, motor de `ancora` copiado do 0011): `gerar_sync.py` alinha o texto ao WAV (sílabas + pausas medidas, sem ASR, margem ~±0,6 s) e gera `sync.json` (58 âncoras de fala) e `legenda.srt` (65 cues, ≤ 2 linhas, ≤ 440 px a 540). A cena tem 58 pontos `self.ancora("sNx")` (um por etapa visual); `native.json` guarda o tempo nominal de cada um. Âncoras fora do `sync.json` são ignoradas (`s7d` e `s9f` ficaram sem fala). Refazer só se a cena ou o áudio mudarem: `uv run python videos/vid_0012_campo_esfera_nao_uniforme/gerar_sync.py` e `SYNC_CAL=1 uv run python -m manim -r 108,192 --fps 15 videos/vid_0012_campo_esfera_nao_uniforme/cena.py CampoEsfera012`. `PAUSAS_FIXAS` (no `gerar_sync.py`) fixa duas pausas conferidas à mão no take Q_env ("ao quadrado," 44,18 s; "cascas finas:" 53,92 s), em que o alinhador errava s3k e s4d; revisar se o áudio mudar. Render sincronizado: nenhum aviso `SYNC atraso`. Trechos mais comprimidos (≈0,45–0,55×): E∥dA/produto escalar (Gauss), tangente da derivada, checagens e CTA.
- A tela do CTA passou a "Se curtiu, segue @labparallax" para casar com a fala (antes "Para mais física assim, siga @labparallax").
- Legenda: `montar_legendado.py … --color-module videos/vid_0012_campo_esfera_nao_uniforme/cena.py` (estilo padrão, faixa translúcida); cores de `SUBTITLE_TERM_COLORS` (campo ciano, densidade/carga magenta, gaussiana/área violeta, normal lavanda).
- Comandos de render final: `uv run python -m manim -r 1080,1920 --fps 30 videos/vid_0012_campo_esfera_nao_uniforme/cena.py CampoEsfera012`; `uv run python videos/montar_master.py media/videos/cena/1920p30/CampoEsfera012.mp4 videos/vid_0012_campo_esfera_nao_uniforme/audio/narracao_final.wav renders/vid_0012_campo_esfera_nao_uniforme_final_master_limpo.mp4`; `videos/montar_legendado.py`.

## Divergência objetiva registrada (briefing)

“Mais carga adicionada” perto do centro e “pouca carga adicionada” perto da borda, para o mesmo Δr, é falso em termos **absolutos**: dQ/dr ∝ x²(1 − x) tem pico em x = 2/3, então a casca da borda carrega **mais** carga que a do centro. O que decide E ∝ Q_env/r² é o crescimento **relativo**. A cena usa “ρ é grande / ρ já é pequena” (brilho da casca ∝ ρ) e “Q_env cresce mais/menos que r²”, que são corretos.

## Pendências

- Capa e publicação: não iniciadas. Os MP4 finais ficam em `renders/` (fora do Git); copiar manualmente para o outro computador.
