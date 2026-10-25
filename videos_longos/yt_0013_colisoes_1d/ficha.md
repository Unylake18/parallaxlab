# COLISÕES EM 1D — COMO SABER O QUE ACONTECE DEPOIS?

- **ID:** yt_0013 (primeiro longo da seção de Mecânica)
- **formato:** longo_horizontal
- **natureza:** teoria_visual
- **curso/eixo:** Física I · **macroassunto:** Mecânica · **módulo:** Colisões (mapa curricular §4.10)
- **duração esperada:** ~10–12 min (a voz define o ajuste final)
- **solido_3d:** nenhum — fenômeno em uma linha, representado em Manim 2D/2.5D por decisão do usuário
- **Status:** final (2026-10-25) — voz ElevenLabs v4 (`audio/narracao_v4.wav`) sincronizada por 265 âncoras
  (alinhamento forçado → `ritmo.py` → render 1080p30 CRF 14 em 5 grupos → `montar_sync.py`/`montar_final.py`; `conferir_sync.py`:
  desvio medido −0,05 a +0,03 s); master 15:13 entregue em `entregas/Vídeos Longos/Mecânica - Colisões - Colisões em 1D`;
  v6 — notação em v (v₁ᵢ, v₂ᵢ iniciais; v₁f, v₂f finais; v_f comum; pêndulo vᵢ e V_t), K/U_g dentro do painel; v5 — header de duas linhas (tag apagada em cima, título da cena branco embaixo), corpos e painéis 2D chatos, setas com ponta sempre visível, mais animação (C05, C09, C12) (preview 960×540 / 15 fps e stills 1080p em `renders/v5/`);
  voz, SRT e final ainda não abertos
- **Classe:** `Colisoes1DYT013` em `cena.py` (backups v1–v4 em `cena_v1_backup.py` … `cena_v4_backup.py`)
- **Notas para a voz:** `direcao_v2.md` (intenções de fala continuam válidas; a tela da v3 tem menos texto)

## Estrutura v3
hook (mesmo começo, três finais, POR QUÊ?) · C01 momento (p = mv, sinais, P = p₁ + p₂, ANTES | equação | DEPOIS) ·
C02 impulso (F(t) sincronizado, P TOTAL constante, J_ext ≈ 0) · C03 tipos (medidores P/K do mesmo estado; nomes depois
do fenômeno) · C04 ficam juntos (setas se fundem; média ponderada ao vivo) · C05 K_f = K_i/2 · C06 elástica (equações
nascem dos medidores; ramo trivial; d(t)) · C07 fórmulas gerais (poucos estados) · C08 casos-limite (previsão →
movimento → confere) · C09–C11 pêndulo bifilar com linha do tempo A → B → C (A→B magenta, B→C ciano) · C12 método em
fluxo · ponte 2D · CTA.

## Semântica de cor (v4, decidida em 2026-10-24)
velocidade u, v violeta #9C8CFF · força F azul-claro #5AA2FF · impulso J (e área sob F(t)) azul-claro + 40 % branco ≈ #9CC7FF ·
momento p, P, Δp magenta #EA63FF · energia cinética K ciano #35D9FF · energia interna laranja #FF7A3D ·
U_g ciano + 45 % branco · corpos em aço (#7A8696 e #B8C4DA, distintos por tom e índice) · d, régua GEO #B8C4DA ·
eixos DIM #8FA3C4 · massa, números e texto branco. Header: linha 1 `MECÂNICA · COLISÕES EM 1D` (17, DIM, opacidade 0,5); linha 2 título da cena (30, branco 0,95; o antigo sai antes de o novo entrar). Corpos: m₁ aço claro #B8C4DA (rótulo escuro), m₂ aço #7A8696 (rótulo branco).

## Notação (v6, pedido do usuário em 2026-10-24)
velocidades sempre com v: v_{1i}, v_{2i} (antes) · v_{1f}, v_{2f} (depois) · v_f (comum, ficam juntos) · pêndulo: v_i (projétil antes) e V_t (conjunto logo depois). Definidas na tela em C01 e no pêndulo. Na cena.py os textos seguem escritos com u/v/V e a função notacao() traduz.
