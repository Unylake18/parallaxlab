# yt_0005 — fechamento visual, físico e técnico pré-narração

Entrega: **um** contínuo silencioso B01 → B09 + CTA, 960×540 / 30 fps, **14:57,63**. Sem voz, SRT, capa, master ou publicação. Sem commit/branch/push. Nada fora desta unidade foi alterado.
Ponto de partida: `cena.py` local idêntico (diff vazio) ao da entrega `renders/entrega_gpt/yt0005_continuo_final_para_gpt.zip` (15:18). O ZIP antigo `continuo_B01_B09_para_gpt.zip` não foi usado.

## Arquivos (pasta `renders/entrega_pre_narracao/`)
- `yt0005_continuo_pre_narracao_540p30.mp4` — render único (sem `SEG`), tentativa 1, 0 erros no log.
- `cena.py` — idêntica byte a byte ao código do render (`cmp` OK).
- `qa/` — `qa_b06.py` + `qa_b06.txt` (QA numérico), `verifica_mp4.py` + `integridade_mp4.txt`, `sheet.py`, `antes_depois.py`, `patch_final.py`, `patch_pulso.py`, `render_seg.sh`.
- `folhas/` — amostra regular do vídeo todo (cada 15 s), densas (hipóteses/determinante, síntese, gancho/CTA), correções (P_B, integrais, B06, B08) e antes/depois.

## Cores finais
- **STEEL = `#7A8696`** (matéria condutora). **GREEN = `#3FE08B`** (corrente I, K, J, dI, ∇·J). B magenta `#EA63FF`, E ciano, carga azul (`BLUE`/`BLUE_L`), v violeta, F `#5AA2FF`.
- **BLUE_L → STEEL (só corpo material):** fios da abertura (`cena.py:375`), linha/lâmina/prisma do B05 (2366–2374), fio do B05 (2571), fio da síntese (3396), fios do gancho (3452–3453). Justificativa: são matéria condutora neutra; antes liam como azul-de-carga.
- **BLUE_L mantidos:** `Orbit` e trilhas (trajetórias), hélice do B03 e da síntese, círculo da síntese, feixe de Thomson e do analisador, carga/λ/σ/ρ/dq/Q (grandeza carga), dA_sup e dτ destacados, volume de controle e fronteira do B06, portadores internos, painéis/caixas/cards (contorno), gráficos. Justificativa: não são matéria condutora (trajetória ≠ enrolamento; volume de controle ≠ corpo material).
- **Marcadores de corrente:** `pulso()` (`cena.py:105`): traço alongado verde, `stroke_width` 7,5, pontas redondas (`CapStyleType.ROUND`), contorno na cor do fundo (+3,5), cabeça (metade da frente) opaca e cauda a 55 %, z-index 2. Usado nos fios da abertura e do gancho. Fluxos de J em setas verdes (B05/B06/B09) mantidos. Nenhum `Dot` verde. `dℓ` branco.

## O que foi feito
1. **Matéria ≠ corrente:** STEEL aplicado (lista acima); verde da corrente destaca do aço e em movimento (ver `antes_depois_*`).
2. **Hipóteses (uma vez, no início do K):** "B uniforme e constante, só a força magnética, regime não relativístico".
3. **Álgebra sempre completa:** `morph()` passou a uma só passada (o termo que sai sobe, o que entra vem de baixo; troca limpa da expressão inteira quando os símbolos se deslocam > 1 unidade). Corrigidos `P_B = ·v`, integrais sem integrando, B sumindo no B08, "=" revelado antes do lado direito (menores do determinante, soma de quadrados da circunferência) e substituição de `dv_z/dt` na EDO.
4. **B06 quantitativo:** uma única fonte (`BalancoB06`: portadores que entraram A e saíram B). Q_int = (A−B)/N0 obedece exatamente a dQ/dt = I_ent − I_sai; dQ/dt exibido, Q e a população de portadores saem do mesmo estado; nenhum portador nasce/some no interior. Nota discreta "câmera lenta: 1 s de tela = 0,11 s". Ver QA numérico.
5. **Transições sem tela vazia:** esquema de energia → fio (troca cruzada), prisma de J → fluxo do volume (o prisma vira referência e se dissolve), volume → aparato de Thomson (o volume se dissolve enquanto entram feixe e B).
6. **Síntese:** a legenda anterior sai antes da nova ("muitas cargas: corrente" × "regime estacionário").
7. **Acabamentos:** determinante só entra depois que o texto de hipóteses sai; legendas do B08 afastadas do título "Razão carga–massa"; rótulo "F_B força magnética" dentro do círculo (não cruza o arco).

## QA numérico do B06 (`qa/qa_b06.txt`) — TUDO OK
Roteiro real de `b06_volume` (rampas `smooth`), modelo quadro a quadro a 30 fps vs. integral de referência: erro máximo 1,8e‑3 C; ΔQ em todas as janelas (equilíbrio, rampas, estados estáveis, retornos) dentro de 2,5e‑3; estado 1 e 4: ΔQ ≈ 0; I_sai > I_ent: dQ/dt = −0,110 C/s de tela (= −S_PHYS), I_ent > I_sai: +0,110 (sem saturação); Q mín 0,28 C (N ≥ 6,7 portadores); Q final = Q0; portadores só entram na face de entrada, só saem na de saída e nunca recuam (0 violações); nº desenhado ≈ Q·N0 (≤ 1).

## Integridade do MP4 (`qa/integridade_mp4.txt`)
960×540, 30,000 fps, 26.930 quadros decodificados, 14:57,63; 0 tempos não crescentes; 0 lacunas > 50 ms (maior intervalo 33,3 ms); 0 erros no log.

## Revisão visual feita
Amostra a cada 15 s do vídeo todo; sequências densas em hipóteses/determinante, B04 (P_B), B05 (integral linha→superfície→volume), B06 (balanço, "V é qualquer", transições), B06→B07, B08, síntese, gancho e CTA; previews 15 fps de cor (abertura, B05, síntese) e 30 fps de álgebra (B04–B08).

## Limitações reais (não declaro o vídeo aprovado)
- Revisão por amostragem, não quadro a quadro; defeitos de poucos quadros podem existir fora das sequências densas.
- Trocas de fórmula ainda mostram, por ~0,3 s, o termo antigo e o novo em fade (separados verticalmente); nunca em branco nem incompletos, mas não são instantâneas.
- Pausas estáticas de leitura de 3–4 s permanecem; a sincronização fina será feita com a voz. O K tem ~4 min (hipóteses → determinante → EDO → ω_c → gráficos → integração → circunferência → hélice).
- B08, ~14:05: três legendas empilhadas na coluna direita (|v| constante ⇒ W_B=0; sentido da curva; título) ficam justas, mas sem sobreposição.
- Teste do arsenal: nenhum sólido Blender integrado (B06 é 2.5D em Manim).

## Tempos atualizados (aprox., ±1 s) e âncoras para a narração
| # | Trecho | Tempo | Frase-guia |
|---|---|---|---|
| 1 | fenômeno dos fios → carga em movimento | 0:06–0:25 | "dois fios neutros se atraem ou se repelem: se a carga líquida é zero, de onde vem a força? — olhe para uma carga em movimento" |
| 2 | Lorentz → análise do movimento | 1:20–1:30 | "a perspectiva muda, a física não: B ao longo de x, v com três componentes, só a força magnética" |
| 3 | velocidade → posição e trajetória | 3:50–4:30 | "integrando v_y e v_z obtemos y(t) e z(t): a trajetória sai da velocidade" |
| 4 | círculo → hélice e passo | 4:35–4:55 e 6:00–6:50 | "a circunferência já continha a hélice; com v∥ ≠ 0 o círculo avança, e o passo é p = 2π m v∥/(|q|B)" |
| 5 | aceleração → trabalho e energia | 7:05–8:20 | "a partícula acelera, mas não fica mais rápida: P = F·v e a força magnética não realiza trabalho" |
| 6 | uma carga → corrente e força no condutor | 8:30–9:25 | "muitas cargas em movimento formam a corrente: dF = I dℓ × B" |
| 7 | densidade de corrente → conservação da carga | 9:30–12:05 | "J é a corrente por área; o balanço no volume leva a ∇·J = −∂ρ/∂t, e na magnetostática ∇·J = 0" |
| 8 | retorno à carga individual → seletor | 12:05–12:25 | "de volta a uma carga: campos cruzados E e B" |
| 9 | velocidade selecionada → medida de |q|/m | 13:00–14:10 | "v = E/B seleciona a velocidade; só com B o raio mede |q|/m = E/(B²R)" |
| 10 | B conhecido → origem de B | 14:33–14:44 | "sabemos o que B faz; como uma corrente cria B?" |

Blocos (aprox.): abertura 0:00 · B01 0:06 · B02 1:20 (K, verificação, período, duas partículas) · B03 6:00 · B04 7:00 · B05 8:30 · B06 10:25 · B07 12:10 · B08 13:25 · síntese 14:10 · fios/gancho 14:33 · CTA 14:44–14:57.

## Comando de render
```
uv run python -m manim -r 960,540 --fps 30 videos_longos/yt_0005_magnetostatica_forca_lorentz/cena.py YT0005MagnetostaticaM1 -o yt0005_continuo_final_540p30.mp4
```
(sem `SEG`; ~34 min no PC de trabalho).
