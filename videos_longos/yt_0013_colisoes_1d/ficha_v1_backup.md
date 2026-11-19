# COLISÕES EM 1D — COMO SABER O QUE ACONTECE DEPOIS?

- **ID:** yt_0013 (primeiro longo da seção de Mecânica)
- **formato:** longo_horizontal
- **natureza:** teoria_visual
- **curso/eixo:** Física I · **macroassunto:** Mecânica · **módulo:** Colisões (mapa curricular §4.10)
- **duração esperada:** ~10–12 min
- **solido_3d:** `colisao_1d`, somente em C01 e C03 (C04–C12 em Manim puro; `colisao_2d` e `explosao` reservados ao vídeo seguinte)
- **Status:** cena completa silenciosa C01–C12 (preview 960×540 / 15 fps); voz, SRT e final ainda não abertos
- **Classe:** `Colisoes1DYT013` em `cena.py`

## Estrutura congelada (briefing de Produção)
C01 o mesmo começo, três finais · C02 impulso externo desprezível · C03 classificação (nomes formais só aqui) ·
C04 completamente inelástica (v_f) · C05 momento conservado ≠ K conservada · C06 segunda equação da elástica
(ramo trivial + velocidade relativa) · C07 fórmulas gerais como consequência · C08 três casos-limite ·
C09–C11 pêndulo balístico (impacto: P_x; subida: energia mecânica) · C12 método + ponte para 2D.

## colisao_1d (parâmetros documentados da ficha do arsenal)
`m1=2.0, m2=1.0, v1=2.0, v2=-2.0, instante=0.65, mostrar_cm=0`, `restituicao` = 1.0 (rebatem / elástica),
0.5 (se separam / inelástica), 0.0 (ficam juntos / completamente inelástica); 60 quadros, 960×540, alpha.
Colisão frontal escolhida para que o enquadramento automático do sólido seja idêntico nas três variantes.
Preparar com `ponte.py` (comando no cabeçalho de `cena.py`) antes de renderizar em outra resolução.

## Convenções de cor
corpo 1 azul · corpo 2 violeta (no 3D o bloco 2 é azul-claro, padrão do arsenal) · vetores físicos branco ·
resultado/payoff e energia cinética ciano · energia interna laranja.
