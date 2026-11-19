# COLISÕES EM 2D — PARA ONDE OS CORPOS PODEM SAIR?

- **ID:** yt_0014 (provisório; segundo longo do módulo Colisões; complemento direto de `yt_0013_colisoes_1d`)
- **formato:** longo_horizontal
- **natureza:** teoria_visual
- **curso/eixo:** Física I · **macroassunto:** Mecânica · **módulo:** Colisões (mapa curricular §4.10)
- **título na tag do canto:** `MECÂNICA · COLISÕES EM 2D` (linha 1: 17 pt, opacidade 0,5, fixa; linha 2 = título de cada cena em **24 pt** — o `yt_0013` usa 30; reduzido a pedido do usuário em 25/10)
- **pergunta_central:** quando a colisão deixa de acontecer sobre uma linha, o que realmente muda? (a física é a mesma; o momento revela sua geometria vetorial)
- **pre_requisitos:** `yt_0013` (momento, impulso, elástica × completamente inelástica, método "momento + condição física")
- **próximo_vídeo:** Torque e dinâmica de rotação — *Por que uma força faz um corpo girar?* (mapa curricular §4.11; gancho em C14 e no CTA; narração em `gancho_proximo.md`)
- **duração alvo:** ~15–16 min (a voz define o ajuste final; a cena se estica, não se comprime)
- **solido_3d:** nenhum (candidatos avaliados: `colisao_2d` no hook e `explosao` em C12) — decisão: Manim 2D limpo; vetores e ângulos exigem leitura exata e o `yt_0013` já migrou para 2D por preferência do usuário. Valores, vetores, ângulos e rótulos são sempre do Manim.
- **Status:** v4 — **versão final entregue** (2026-10-25): voz ElevenLabs v4 (`audio/narracao_v4.wav`, 887,8 s) com **324 âncoras** sincronizadas (alinhamento forçado → `ritmo.json`; **0 pausas inseridas na voz**; atraso por âncora ≤ 1 quadro) e master 1920×1080 / 30 fps / H.264 CRF 14 (`final/master - 0014.mp4`, 889,7 s), legenda `.srt` e capítulos. A tela nunca fica parada: esperas da voz viram pulso suave ("respiração") no que acabou de entrar. Entrega: `entregas/Vídeos Longos/Mecânica - Colisões - Colisões em 2D`. Backups: `cena_v1_backup.py`, `cena_v2_backup.py`, `cena_v3_pre_sync_backup.py`, `cena_v4_pre_ocioso_backup.py`, `cena_v5_pre_nopad_backup.py`.
- **Classe:** `Colisoes2DYT014` em `cena.py` (seções: `hook, abertura, c01 … c14, cta`; `SECOES=c07,c09` isola trechos; `AUDITORIA=1 … --dry_run` audita sobreposições; `STILL=t` com `-s` salva um quadro no instante absoluto `t`)

## Tese e hipóteses
Método do 1D continua: **momento + condição física da colisão**. Mecânica clássica, choque curto, impulso externo desprezível durante o
impacto, massas constantes, movimento num plano, partículas quanto à cinemática do choque, alvo inicialmente parado nos problemas de
espalhamento, elástica só quando indicada. Fora do escopo: coeficiente de restituição, CM formal, 3D geral, potencial central, seção de
choque, Rutherford, relatividade, rotação de corpo rígido, momento angular, dinâmica do contato.

## Estrutura (tempo nominal · conteúdo)
hook + bem-vindos + título + retomada (C01, ~45 s) · C02 momento é vetor: triângulo de momentos (~60 s) · C03 uma conservação vetorial =
duas equações escalares; falta a condição física (~60 s) · C04 massas iguais → v⃗₁f ⊥ v⃗₂f (~80 s) · C05 bilhar 30°/60°, 5√3 e 5 m/s
(~50 s) · C06 massas diferentes, λ = m₂/m₁, quadrática em p₁f (~85 s) · C07 a quadrática é um círculo: completar o quadrado em passos e troca de plano
(~90 s) · C08 1D, direções oblíquas, tangência; fecha o hook (~70 s) · C09 θ_max = arcsin(m₂/m₁); tracker em λ: λ<1, λ=1 (Thales), λ>1 (~80 s) ·
C10 alfa × nêutron (~65 s) · C11 acidente 2D completamente inelástico + deslizamento (~90 s) · C12 explosão (~45 s) · C13 método e síntese (~60 s) ·
**C14 gancho: o mesmo impulso no centro e fora do centro (~55 s)** · CTA com a prévia do próximo vídeo.

## Sistema de layout (v2)
Margens seguras de 0,6 u; texto mínimo 22 pt (M ≥ 26; equação principal ≥ 48; frase de ideia ≥ 30); a tag fixa da linha 1 do header (17 pt) é a única exceção.
Três layouts: **L-PALCO** (plano de p₁f grande à esquerda, coluna direita com no máximo duas coisas: C07 fase B, C08, C09, C10), **L-EQUAÇÃO**
(equação em destaque; passos anteriores recuam para cima, menores e apagadas — `Pilha`: C04, C06, C07 fase A) e **L-CENA** (aparato em tela cheia:
hook, C01, C02, C05, C11, C12, C13, C14). Acabamento: painéis com gradiente e filete, círculo de estados ciano com halo e vinheta, rótulos com contorno
escuro, uma caixa dupla de payoff por cena.

## Dois planos (nunca confundir)
**Espaço físico** (corpos, trajetórias, momentos, direções reais): marca discreta `ESPAÇO FÍSICO` só onde a especificação pede (título do triângulo de C02 e a
miniatura de C08). **Plano de p⃗₁f** (círculo de estados): painel com grade e eixos próprios + aviso `PLANO DE p⃗₁f` dentro do painel; transição própria em
C07 (a álgebra sai do centro, o painel entra).

## MF-Tools (usado em todas as cadeias de equações — v3)
Regra do vídeo: **nenhuma equação some e a seguinte aparece**; os termos NAVEGAM da equação anterior (ou do rótulo da figura) até o lugar que ocupam na próxima.
`TransformByGlyphMap` (mapa por **partes nomeadas**, classes `Eq`/`EqJ`, métodos `Scene.avanca` e `Scene.nasce` em `cena.py`; nenhum índice de debug no vídeo);
partes de mesmo nome seguem juntas, o resto entra/sai por fade; cópias deliberadas (um termo vai para dois lugares) e cancelamentos (o termo encolhe e sai).
Só entra por fade a afirmação genuinamente nova (ex.: K_i = K_f depois da relação de velocidades, |v⃗_f| depois de tg θ).
- C02: p⃗₁ᵢ, p⃗₁f, p⃗₂f saem dos rótulos da figura para P⃗ᵢ e P⃗f; P⃗ᵢ = P⃗f vira p⃗₁ᵢ = p⃗₁f + p⃗₂f. C03: a equação vetorial se desfaz nas equações dos eixos x e y (seta some, cos/sen entram).
- C04: rótulos v⃗ → m v⃗ᵢ = m v⃗f + m v⃗₂f → (massas encolhem e saem) → K_i = K_f → ½mv² (K vira v, o índice fica) → (v⃗₁ᵢ)² = (v⃗₁f + v⃗₂f)² nasce da relação recuada → abre em
  v₁ᵢ² = v₁f² + v₂f² + 2 v⃗₁f·v⃗₂f (o expoente 2 vira o 2 do termo cruzado) → cancela o que é igual à energia → 2 v⃗₁f·v⃗₂f = 0 → v⃗₁f ⊥ v⃗₂f. C05: v₁f = v₁ᵢ cos 30° → v₂f = v₁ᵢ sen 30°.
- C06: rótulos do triângulo → p⃗₂f = p⃗₁ᵢ − p⃗₁f → lei dos cossenos (cada vetor vira o quadrado, o termo cruzado nasce) → energia (numeradores vêm dos termos recuados) → p₂f² = λ(p₁ᵢ² − p₁f²)
  → igualar os dois p₂f² (cópias dos dois passos recuados) → quadrática (o λ se reparte em 1+λ e 1−λ).
- C07: p₁ᵢ cosθ₁ p₁f → p⃗₁ᵢ·p⃗₁f → dividir por (1+λ) (o (1+λ) desce para baixo de cada termo) → **completar o quadrado** (o termo (p₁ᵢ/(1+λ))² nasce do termo central, é somado nos dois lados e
  (1−λ)/(1+λ) p₁ᵢ² atravessa a igualdade) → agrupar o quadrado perfeito → lado direito simplificado (conferência 1/(1+λ)² − (1−λ)/(1+λ) = λ²/(1+λ)²) → |p⃗₁f − C⃗| = R com C⃗ e R definidos abaixo
  (a fração viaja para a definição) enquanto o plano de p₁f entra.
- C09: sen θ_max = R/C = λ → θ_max = arcsen(m₂/m₁). C10: θ_max → cos θ_max → (p₁f/p₁ᵢ)² → 60 % → 0,40. C11: P⃗ᵢ = P⃗f abre nas componentes x e y → v_fx, v_fy → tg θ = v_fy/v_fx → θ;
  ½(M+m)v² = μ(M+m)gd → d = v²/(2μg) (o ½ vira o 2, os (M+m) se anulam). C12: Σ p⃗ₖ = 0 → p⃗₁ + p⃗₂ + p⃗₃ = 0.

## Semântica de cor
velocidade violeta `#9C8CFF` · momento magenta `#EA63FF` (segundo p⃗ do par: mesma cor, mais clara) · energia cinética **e círculo de estados** ciano
`#35D9FF` · energia interna/dissipada laranja `#FF7A3D` · impulso J azul-claro `#9CC7FF` · ângulos: arcos brancos finos · geometria (R, C, d, régua)
`#B8C4DA` · corpos em aço chato (m₁ aço claro `#B8C4DA`, m₂ aço `#7A8696`; aro mais escuro + rótulo m₁/m₂; sem brilho nem sombra).

**C11 (acidente):** veículos vistos de cima com o desenho do `vid_0026` (classe `Carro`: rodas, teto, para-brisa, faróis e lanternas em vidro), mas **em aço**:
caminhão em aço claro e carro em aço escuro, pista cinza-azulada neutra. Azul-claro é da força e violeta é da velocidade, então as cores ficam só para os vetores
(decisão do chat de Produção em 25/10; uma versão azul/violeta chegou a ser feita e foi descartada). Voltar às cores é trocar `CAR1`/`CAR2` em `cena.py`.

## Notação (igual ao `yt_0013` atual)
v⃗₁ᵢ, v⃗₂ᵢ (antes) · v⃗₁f, v⃗₂f (depois) · v_f (comum) · p⃗₁ᵢ, p⃗₁f, p⃗₂f, P⃗ᵢ, P⃗f · θ₁ (desvio da incidente), θ₂ (recuo do alvo, medido abaixo do eixo) ·
**λ = m₂/m₁** (novo; definido em C06). Nenhum `u`. Exemplo do círculo: **λ = 1/4** (hook, C07, C08, C10); o triângulo de C02/C03/C06 é genérico
(elástico, λ = 1/2 por construção) e não mostra número de λ.

## Números verificados (asserts em `cena.py`)
θ_max(1/4) = 14,48° ≈ 14,5° · p₁f/p₁ᵢ = √15/5 ≈ 0,775 · K₁f/K₁ᵢ = 60 % → K_n,f = 0,40 K_α,i (no ângulo limite; **não** é transferência máxima) ·
θ₂ ≈ 37,8° · frontal 4λ/(1+λ)² = 16/25 = 64 % · bilhar: θ₂ = 60°, v₁f = 5√3 m/s, v₂f = 5 m/s · acidente: v_f = (6,25; 12,5) m/s, 63,4° a partir do leste,
|v_f| ≈ 13,98 m/s, d = v_f²/(2μ_k g) ≈ 19,53 m · o círculo passa por p₁ᵢ e por (1−λ)/(1+λ) p₁ᵢ sobre o eixo e a tangência cai em sen θ = λ · o desfecho
real do hook (disco pesado × leve, θ₁ ≈ 10,9°) cai sobre o círculo; a direção impossível do hook é 40° (> 14,5°) · álgebra de C07 conferida numericamente
(1/(1+λ)² − (1−λ)/(1+λ) = λ²/(1+λ)² para λ = 1/4, 1/2 e 2).

## Pendências do preview v2
- Voz, SRT, âncoras de sincronia, master e entrega: não abertos.
- Texto do gancho: decisão do Kaio sobre trocar "efeitos completamente diferentes" (ver `gancho_proximo.md`).
