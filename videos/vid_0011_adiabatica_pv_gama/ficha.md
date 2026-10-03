# vid_0011 — De onde vem PV^γ = constante

- Série pública: **POR TRÁS DA FÓRMULA · EP. 04**.
- **Concluído tecnicamente em 2026-10-02: voz, sincronia por âncoras, legenda colorida, master e legendado gerados; aprovação humana do vídeo final, capa e publicação pendentes.**
- Cena: `cena.py`, classe `AdiabaticaPVGama011` (módulo único; `Eq` local para os mapas de glifos do MF-Tools; classe `Cyl` para o cilindro).
- Comandos: preview `uv run python -m manim -r 540,960 --fps 30 videos/vid_0011_adiabatica_pv_gama/cena.py AdiabaticaPVGama011`. `ATE=k` (1–10) renderiza só até o segmento k.
- Final: `renders/vid_0011_adiabatica_pv_gama_final_master_limpo.mp4` e `..._final_legendado.mp4` — 1080×1920, 30 fps, 158,35 s; AAC estéreo 158,16 s.
- Narração: `audio/narracao_final.wav` (ElevenLabs, 158,16 s, estéreo 44,1 kHz, intacta; texto lido em `texto_narracao.txt`, 450 palavras; a versão ampliada com síntese e aplicações ficou em `texto_narracao_v3_opcional.txt`, não usada). "Máier" é a grafia de fala; a legenda mostra "Mayer".
- Sincronia: `gerar_sync.py` alinha o texto ao WAV (sílabas + pausas medidas, sem ASR) e gera `sync.json` (34 âncoras) e `legenda.srt` (63 cues, ≤ 2 linhas, ≤ 440 px a 540). `native.json` guarda o tempo nominal de cada âncora; refazer só se a cena ou o áudio mudarem: `uv run python videos/vid_0011_adiabatica_pv_gama/gerar_sync.py` e `SYNC_CAL=1 uv run python -m manim -r 108,192 --fps 15 videos/vid_0011_adiabatica_pv_gama/cena.py AdiabaticaPVGama011`. O render sincronizado não imprimiu `SYNC atraso`. A maior distorção é o aquecimento do Mayer, esticado ×2 (a fala ali é longa).
- Legenda: `montar_legendado.py … --style solid --color-module videos/vid_0011_adiabatica_pv_gama/cena.py`; cores de `SUBTITLE_TERM_COLORS` (energia interna/calor específico/adiabática ciano; trabalho violeta; calor/temperatura/isotérmica magenta; gama/Mayer azul claro). A máscara sólida cobre abaixo de y ≈ −4,4: o fecho (hipóteses e CTA) fica em y = −4,0.
- Comandos de render final: `uv run python -m manim -r 1080,1920 --fps 30 videos/vid_0011_adiabatica_pv_gama/cena.py AdiabaticaPVGama011`; `videos/montar_master.py` (render + WAV).
- Pranchas de QA em `frames_preview/` (preview V3, sem legenda).

## Estrutura (segundos, marcos do briefing)

| Seg. | Tempo | Conteúdo |
| --- | --- | --- |
| 1 | 0–15 | cilindro isolado, pesos retirados, δQ = 0, pergunta |
| 2 | 15–35 | dU = δQ − δW → dU = −P dV (quase-estática, sem dissipação); V↑ U↓ T↓ |
| 3 | 35–55 | U = U(T), definição de C_V, dU = nC_V dT, nC_V dT = −P dV, PV = nRT |
| 4 | 55–68 | P → nRT/V, cancela n, T atravessa a igualdade, dV sobe: C_V dT/T = −R dV/V |
| 5 | 68–90 | Mayer em split-screen (δQ_V, δQ_P): C_P − C_V = R |
| 6 | 90–100 | γ = C_P/C_V; R/C_V = γ − 1 |
| 7 | 100–125 | dT/T = −(γ−1) dV/V, hipótese γ ≈ cte, ∫, ln, TV^(γ−1) = cte |
| 8 | 125–140 | T = PV/nR dentro da expressão → PV^γ = cte (payoff) |
| 9 | 140–160 | gráfico P×V único, isotérmica (calor entra) × adiabática, P_ad < P_iso em V igual |
| 10 | 160–170 | convergência: pistão, gráfico, PV^γ = constante e hipóteses |

## Modelo (fonte única de movimento)

`Cyl.prog` = pesos retirados. P_ext = 0,4 + 0,075·(8 − pesos retirados); volume v = P_ext^(−1/g) (g = γ = 1,4 adiabático; g = 1 isotérmico); T = v^(1−g). Pistão, gás, termômetro, velocidade dos pontos do gás e o ponto do gráfico P×V leem o mesmo `prog`. γ = 1,4 só serve para desenhar; a dedução é simbólica. Isotérmica e adiabática partem de (V₀, P₀) = (1, 1) e terminam no mesmo V_f = 0,4^(−1/1,4) ≈ 1,92 (a isotérmica usa pesos mais leves: P_ext final 1/V_f ≈ 0,52 contra 0,4 da adiabática); a comparação P_ad < P_iso é feita nesse V_f.

Cores: ciano = energia interna (dU, nC_V dT) e adiabática; violeta = trabalho (P dV, nR dT); magenta = calor/temperatura e isotérmica; branco = texto.

## V2 (continuidade matemática, sem mudar roteiro nem duração)

- δW dentro de `dU = −δW` ganha moldura e vira `P dV` por cópia dos glifos de `δW = P dV`.
- C_V nasce da pergunta "Como U muda quando T muda?": definição rotulada → `nC_V = dU/dT` → `dU = nC_V dT`, que se junta a `dU = −P dV`.
- `PV = nRT` → `P = nRT/V`, e essa fração substitui o `P` de `nC_V dT = −P dV`. Manchete "Ligando temperatura e volume" (antes "Álgebra").
- Mayer sem a equação adiabática no rodapé; os dois lados aquecem juntos (mesma subida de T); payoff boxeado é `C_P − C_V = R`.
- γ − 1 = C_P/C_V − 1 = (C_P − C_V)/C_V = R/C_V, com o `R` copiado da caixa de Mayer.
- `C` rotulado como constante de integração; γ ≈ cte continua antes das integrais.
- T boxeado e substituído por PV/nR; `V·V^(γ−1) → V^γ`; nR atravessa a igualdade e entra na constante.
- Gráfico: mesmo V_f nos dois pistões (isotérmica com pesos mais leves, mesma P_ext inicial; adiabática com P_ext final 0,4), linha tracejada em V_f, `P_ad < P_iso (mesmo V_f)`, rótulos δQ > 0 · T = cte e δQ = 0 · T↓. Isotérmica some no fechamento (sem curva fantasma).
- Pesos: sobem e saem lateralmente rápido; o pistão responde só depois. Velocidade dos pontos do gás cresce com T.

## V3 (causalidade visual; mesmo conteúdo e duração)

- Primeira Lei: o `δQ` da equação nasce (por glifo) do `δQ = 0` do sistema e sai da própria equação; sem o estado `dU = 0 − δW`.
- Origem de C_V: `U = U(T)` pulsa enquanto `(∂U/∂T)_V` vira `dU/dT` (parênteses e subscrito V saem), depois `nC_V = dU/dT` → `dU = nC_V dT`.
- Mayer como demonstração: mesmos T iniciais, calor entra nos dois lados, T sobe igual; barras de energia (ΔU ciano nos dois, W violeta só no pistão) mostram C_P > C_V antes da álgebra. Depois `δQ_P = dU + P dV` (dU vem de `nC_V dT` do lado A), `PV = nRT → P dV = nR dT` entra na cadeia por cópia de glifos, cancelamento de `n dT` e `C_P − C_V = R` maior e com pausa. Sem microtexto de rodapé.
- Hierarquia: sistema físico recua (opacidade 0,35–0,5) quando a matemática é protagonista e volta a 1 no gráfico.
- nR: `PV^γ/(nR) = cte → PV^γ = nR cte → PV^γ = cte′ → cte`, com moldura em nR.
- Gráfico: os dois pistões sobem juntos até V_f e os pontos percorrem as curvas em tempo real; só no fim entram a linha tracejada em V_f, P_iso, P_ad e a caixa `P_ad < P_iso (mesmo V_f)`.
- Partículas: trajetórias retilíneas com reflexão (onda triangular), velocidade cresce com T.
- `C: constante de integração` e `γ ≈ cte no intervalo` em corpo 28.

## Observações do preview

- Violeta das equações clareado para `#9C8CFF` (o `#745CFF` da marca tinha pouco contraste sobre o fundo escuro).
- Tempos seguem os marcos do briefing, mas alguns segmentos estouram até ~3 s antes de realinhar (impresso como `ATRASO`: antes de 70, 74, 126, 133, 142; o payoff do seg. 8 chega ~3,4 s depois do marco). Sem voz não há como medir; ajustar após a locução natural.
- Mayer é desenhado com dois cilindros próprios (A rígido, B com pistão e pesos fixos); o cilindro principal faz fade e volta no segmento 6.
- Plano de corte do briefing (comparação para 10–12 s, C_V só visual, menos estados na integração) não foi necessário: 169,5 s < 3:00.

## Pendências

- Aprovação humana do preview (continuidade, causalidade, legibilidade, ritmo).
- Capa, `publicacao.md`, `revisao.md`, conferência em celular e publicação: não iniciados.
