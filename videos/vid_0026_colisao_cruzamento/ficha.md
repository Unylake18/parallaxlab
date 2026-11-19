# O que uma marca no asfalto consegue contar sobre uma batida?

- ID: `vid_0026`
- Pasta: `videos/vid_0026_colisao_cruzamento/`
- Série pública: **EXERCÍCIO RESOLVIDO · EP. 9**
- formato: `curto_vertical`
- Área: Física I / Mecânica · Colisões (2D, completamente inelástica) + trabalho–energia
- Headline: `O QUE UMA MARCA NO ASFALTO CONSEGUE CONTAR SOBRE UMA BATIDA?`
- Pergunta central: conhecendo as massas, a marca de deslizamento e o atrito, quais eram as velocidades imediatamente antes do impacto?
- Payoff: a direção dos destroços dá a razão dos **momentos**, não a das velocidades; o momento se conserva no impacto, a energia cinética não.
- Duração alvo do preview: 125–140 s (a cena se estica na fase de voz).
- solido_3d: nenhum, porque a vista superior e os vetores 2D explicam melhor.
- **Entregue (25/10/2026):** `entregas/Exercício Resolvido - EP 09 - O que uma marca no asfalto consegue contar sobre uma batida - 0026/`
  (master 1080×1920/30 fps CRF 14, 168 s; voz; ficha; texto). Sem legendado nem SRT (decisão do usuário). Capa: não feita.
- Fase aberta inicialmente (25/10/2026): `cena.py` + preview silencioso 540×960 / 15 fps. Voz, SRT, legenda, master, capa, cartão final (CTA) e entrega **não abertos**.
- Versão atual: preview v4 (146,5 s; handoff v4: hook do acidente, coluna lateral de parâmetros, margens 0,45 u, cortes, cartão final `@labparallax` com `ESTICA['cta']`); v1–v3 em `cena_v1.py`…`cena_v3.py` e `renders/preview_v1…v3_540p15.mp4`.
- Voz e sincronização (25/10/2026): narração `narracao_tags_v3_curta.md` (v2 sem bem-vindos), voz `eleven_v4` cortada para
  `audio/narracao_v3_curta.wav` (163,1 s); alinhamento forçado → `voz_ancoras.json` (39 âncoras, `gerar_ancoras.py`) → `MEDIR=1` (`nat.json`) →
  `plan_sync.py` (`sync.json` + `audio/narracao_sync.wav`) → render `SYNC=sync.json` 1080×1920/30 fps CRF 14 (169,5 s) →
  master sem legenda `renders/master_v4_sync_0026.mp4`. Sem SRT nem legendado (decisão do usuário).
- Carros (decisão local deste vídeo): carro 1 azul `#267BFF` (borda `#7FB2FF`), carro 2 violeta da marca `#745CFF` (borda `#A99BFF`); setas de velocidade `#9C8CFF` sempre fora do corpo.
- Classe: `ColisaoCruzamento026` em `cena.py` (seções `c01 … c07`; `SECOES=c03,c04` renderiza só esses blocos; o dicionário `ESTICA` estica cada bloco).
- Referência visual: curtos recentes (vid_0023: tag da série, cabeçalho, Space Grotesk em maiúsculas) + longos de colisões (yt_0013/yt_0014: paleta, corpos de aço chatos, setas, arcos brancos finos, régua de fases).

## Problema (congelado)

Vista superior, norte para cima, leste para a direita.
- Veículo 1: m₁ = 2000 kg, vem do oeste (+x), v⃗₁ᵢ = v₁ᵢ î.
- Veículo 2: m₂ = 1000 kg, vem do sul (+y), v⃗₂ᵢ = v₂ᵢ ĵ.
- Ficam unidos (completamente inelástica) e deslizam até parar.
- Dados: μ_k = 0,50; g = 10 m/s²; marca de 8 m para leste e 6 m para norte (d = 10 m; tan θ = 3/4; θ só como arco).

## Solução (conferida)

1. Deslizamento (trabalho–energia): 0 − ½Mv_f² = −μ_k M g d → v_f = √(2μ_k g d) = 10 m/s; v⃗_f = (8; 6) m/s. A massa total cancela.
2. Impacto (momento): P⃗ᵢ = P⃗_f → v₁ᵢ = 3000·8/2000 = 12 m/s = 43,2 km/h; v₂ᵢ = 3000·6/1000 = 18 m/s = 64,8 km/h.
   p₁ᵢ = 24 000 e p₂ᵢ = 18 000 kg·m/s; |P⃗| = 30 000. tan θ = p₂ᵢ/p₁ᵢ = 3/4 (não 18/12).
3. Energia: K_antes = 144 + 162 = 306 kJ; K_depois = 150 kJ; 156 kJ ≈ 51 % convertidos em deformação, calor, som, vibração.

Hipóteses: impacto curto; impulso externo horizontal desprezível no impacto; estrada horizontal; partículas; unidos; marca começa no impacto e é
reta; um μ_k efetivo constante; sem propulsão; sem rotação. Modelo idealizado, não perícia.

## Notação e cores

v⃗₁ᵢ, v⃗₂ᵢ, v⃗_f, K_antes, K_depois (nunca V, V_t, u, K_f duplo, "sumiu", Δt, fórmula geral de ΔK).
Velocidade violeta `#9C8CFF` · momento magenta `#EA63FF` · energia convertida laranja `#FF7A3D` · corpos em aço (m₁ aço claro `#B8C4DA`,
m₂ aço `#7A8696`, como no yt_0014) · marca branco/cinza claro · ângulos em arco branco fino · sem verde.

## Blocos (preview)

C01 mistério · C02 começar pelo fim (trabalho–energia, massa cancela, triângulo de velocidade) · C03 voltar ao impacto (momento por componentes,
12 e 18 m/s, km/h) · C04 três triângulos 3–4–5 + pegadinha velocidade × momento · C05 conferência de ida e volta · C06 energia (306/150/156 kJ) ·
C07 cada intervalo, sua lei + ponte para a colisão elástica (insinuação do círculo).
