# POR QUE A CORRENTE RESISTE A MUDAR? — Indutância e energia magnética

- **ID:** yt_0012 (yt_0011 está ocupado no outro PC)
- **formato:** longo_horizontal
- **natureza:** derivacao_aplicada
- **macroassunto:** eletromagnetismo
- **modulo:** indutancia_e_circuitos_com_indutores (mapa curricular 6.11; depois de 6.10 Indução, antes de 6.12 Maxwell)
- **solido_3d:** nenhum (o campo, a corrente e a fem precisam responder quadro a quadro ao mesmo tracker temporal; uma sequência PNG do `solenoide_corrente` não acompanha I(t), B(t) e ℰ_L(t). O 2D explica melhor aqui. `capacitor_placas_paralelas` também não: no gancho final o capacitor é um elemento de circuito, não um campo de placas.)
- **Status:** final entregue (2026-10-25): master 1920×1080/30 fps, CRF 14, 20:41,6, voz ElevenLabs v4 (`narracao_sugestao_v2.md` → `narracao_tags.md` → `audio/narracao_v4.wav`), SRT e capítulos. Pasta: `entregas/Vídeos Longos/Eletromagnetismo - Eletrodinâmica - Indutância e energia magnética`. Sem capa.
- **Sincronia:** `an(frase)` na cena (215 âncoras) + alinhamento forçado (`audio/alinhar.py`) → passe a seco (`SYNC_LOG`) → `ritmo.py` → render com `SYNC=ritmo.json` (tempo absoluto por play, vale em qualquer fps) → `montar_sync.py` (voz com pausas, SRT, capítulos) → `montar_final.py` → `conferir_sync.py`. Comandos em `_render_final.sh`. Mudou a cena: refazer passe a seco e ritmo.
- **Classe:** `IndutanciaYT012` em `cena.py`

## Pergunta central
O que impede a corrente de mudar instantaneamente — e onde fica a energia?

## Aparato único
Bateria ℰ₀ + chave de duas posições + solenoide (L) + resistor R, desenhados como um circuito só.
A chave liga a bateria (posição a, carga). Em C16 aparece o ramo de desvio (posição b): a bateria sai e o caminho continua fechado pelo resistor (descarga).
C03–C04 acrescentam uma bobina secundária coaxial (N₂ espiras) com medidor; C20 troca o solenoide por um capacitor.

## Payoffs protegidos
1. ℰ_L = −L dI/dt: o indutor se opõe à **mudança** da corrente (C05–C06).
2. P_fonte = P_Joule + dU_B/dt (C12).
3. U_B = ½ L I² (C12).
4. u_B = B²/(2μ₀) (C14; generalização em C15).
5. ∫ P_R dt = U_B,0 (C19).

## Física congelada
- Carga: I = I_∞(1 − e^{−t/τ}), I_∞ = ℰ₀/R, τ = L/R; dI/dt = (ℰ₀/L) e^{−t/τ}; ℰ_L = −ℰ₀ e^{−t/τ}; B = μ₀ n I.
- Descarga: I = I₀ e^{−t/τ}; ℰ_L = +R I₀ e^{−t/τ} (sustenta a corrente); U_B = ½ L I₀² e^{−2t/τ}; P_R = R I₀² e^{−2t/τ} = −dU_B/dt; Q_R = U_B,0(1 − e^{−2t/τ}).
- Mútua (solenoide longo, secundária externa): Λ₂ = N₂ B₁ A = μ₀ n N₂ A I₁ ⇒ M = μ₀ n N₂ A (A = seção do solenoide; B₁ só existe dentro dele).
- Autoindutância: L = μ₀ n² A ℓ; U_B = (B²/2μ₀) Aℓ ⇒ u_B = B²/(2μ₀).
- Campo elétrico induzido (solenoide ideal): r < a, E_φ = −(μ₀ n r/2) dI/dt; r > a, E_φ = −(μ₀ n a²/2r) dI/dt.

## Convenções visuais (fixas em C01–C20)
- +x à direita. Corrente convencional no sentido horário do circuito: sobe pela bateria, atravessa o solenoide da esquerda para a direita, desce pelo resistor.
- Enrolamento: nas espiras da frente a corrente desce ⇒ **B aponta para +x** dentro do solenoide (vista de topo, C10: B saindo da tela, ⊙).
- Seta ciano de ℰ_L = sentido em que a fem empurra a corrente; "+" na ponta, "−" na cauda. Carga (dI/dt > 0): seta para a esquerda, + à esquerda. Descarga (dI/dt < 0): seta para a direita.
- Corte transversal (C10): com dI/dt > 0, E_φ < 0 ⇒ circulação horária vista de frente (Lenz).

## Cores (V3: `docs/padrao_video_longo.md`, tabela `TOKCOL` em `kit.py`)
- corrente / I: **verde `#3FE08B`**, desenhada como **traços verdes** que correm pelo fio (como em Biot–Savart/Ampère), velocidade ∝ I, espaçamento fixo;
- toda fem e campo elétrico induzido (ℰ₀, ℰ_L, ℰ₁, ℰ₂, E_φ, P_fonte): **ciano**;
- B, Λ, Φ, U_B, u_B: magenta · τ, t: violeta · calor (P_R, P_Joule, E_calor, Q_R): laranja `#FF7A3D`;
- geometria (A, ℓ, V, n, N₂, r, a, dτ): `GEO #B8C4DA` · R, L, M e operadores: branco · fios e espiras: aço.
- Cor por token em `MathTex` de string única (`E(tex, *tokens)` do kit).

## Tipografia, índice e transformações (V3)
- Manchete em MAIÚSCULAS (Space Grotesk, corpo 30, y = 3,42), troca sequencial; sem frases de narração na tela.
- **Índice de variáveis**: cada símbolo novo ganha uma linha em minúsculas no cartão (`defn`, ex.: "L: autoindutância, em henry"), com o símbolo na cor dele e o texto apagado.
- Cartões por slot (`show`/`drop`/`relayout`), sem caixa branca; auditoria automática de sobreposição texto-texto (`audit`, grava `layout_issues` no `tempos.json`).
- Álgebra: MF-Tools `TransformByGlyphMap` (`gmap`, auto_fade em duas fases); substituições conceituais são fade.
- Infraestrutura: cópias locais `kit.py`/`base.py` do yt_0006 (o yt_0006 não foi tocado).

## 2.5D
Solenoide em 10 anéis 3D de aço (frente em tubo, fundo a 0,38), bobina 2, capacitor e superfícies de Ampère são objetos 3D projetados (giro `ang` em torno do eixo vertical + leve elevação).
C10 gira o mesmo solenoide da vista lateral para a axial; C14 varre a seção A ao longo de ℓ para formar o volume.

## Trackers
- `tc` (t/τ da carga) → I, dI/dt, B, ℰ_L, U_B, P_fonte, P_Joule, dU_B/dt, E_φ(r), velocidade das cargas, ponto dos gráficos.
- `td` (t/τ da descarga) → I, dI/dt, B, ℰ_L, U_B, P_R, Q_R, brilho do resistor, ponto dos gráficos.
- `sp` (só C06): corrente imposta (sobe, constante, desce) → I, dI/dt, ℰ_L e reta tangente do gráfico.
- C20: `tc` volta a valer como carga RC do capacitor (I = e^{−t/τ}, q = 1 − e^{−t/τ}).

## Comandos
```bash
# preview completo (silencioso) — grava tempos.json
uv run python -m manim -r 960,540 --fps 15 videos_longos/yt_0012_indutancia_energia_magnetica/cena.py IndutanciaYT012
# só algumas cenas (as demais são puladas, mas o estado é construído) — grava tempos_SEG_<lista>.json
SEG=c07,c13 uv run python -m manim -r 960,540 --fps 15 videos_longos/yt_0012_indutancia_energia_magnetica/cena.py IndutanciaYT012
```
Um render por vez (dois em paralelo já deram MemoryError). Tempos provisórios: constantes `T_*` no topo de `cena.py`.
