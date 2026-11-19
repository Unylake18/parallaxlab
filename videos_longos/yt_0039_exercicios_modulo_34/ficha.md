# Exercícios do módulo: jacobiano, polares e centro de massa

Série pública: **CÁLCULO III · EP. 14**

```
formato: longo_horizontal
tipo: exercicios
serie_publica: CÁLCULO III · EP. 14
titulo: Exercícios do módulo: jacobiano, polares e centro de massa
disciplina: Cálculo III
modulo: 3.4 Mudança de variáveis na integral dupla (o docs/mapa_curricular.md do repositório ainda usa a numeração antiga)
bloco: 3.4-E1
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, Exercícios 4.2 (1h, 2e, 4, 5, 6) e 4.3 (1b, 1f, 3); Stewart, Cálculo, vol. 2, §15.9 (u = xy, v = y/x). Só na descrição do YouTube: nada de livro na tela nem na fala
unidades: E1 é exercício de coordenadas adimensionais (o expoente y − x² precisa ser adimensional); E2 em coordenadas normalizadas (L = 1 m, densidade de referência 1 kg/m²), por isso a massa sai em kg; E3 a E6 com comprimentos na unidade de referência; k carrega a unidade e cancela em ȳ. Não inserir unidades novas nas fórmulas
solido_3d: nenhum do arsenal Blender (o oitavo de esfera e os sólidos de revolução são superfícies simples feitas direto em Three.js, como nos EP. 05 a 13)
3d_threejs: cena1 = octante (E3: quarto de disco no chão + casca da esfera no 1º octante, com pouso de cima para o 2D); cena2 = pappus (E6: chapa em pé sobre o eixo x varrendo o sólido por um ângulo φ; formas meio disco, meia arruela e disco deslocado; quadradinho com o anel 2πy; círculo do centroide); cena3 = massa (E4-3 meia elipse ρ = k y e E5-4 meia arruela ρ = k r: chapa que ganha altura ρ, inclinação de ≈ 1,5 s e pouso de cima para o 2D); o toro do E6-5 é a forma toro da cena pappus
duracao_alvo: 26:57 (WAV 26:56,24 + 1,0 s; voz v3.1, 5.181 palavras, 3,21 p/s)
```

## Fontes

- Handoff: `referencia/yt_0039_handoff_v1_1.md` (v1.1, 2026-11-15); proposta `referencia/calculo3_34e1_exercicios_integradores_proposta_v1.md` (§3.1 = texto da coluna);
  narração `narracao_v1.md` (cópia de `referencia/yt_0039_narracao_v1.md`); verificação sympy `referencia/verificacao/` (67/67 `True`, reexecutada no checkout).
- Quadros-alvo e geradores: `referencia/yt_0039_quadros_alvo_v1/` (`sb39.html`, `c3d39.html`).

## Código

- Kit copiado do `yt_0037` (sem importar): `kit.py`, `v39.py`, `lib39.py`, `pecas39.py`, `p39.py`, `polar39.py`, `v2kit.py`; peças do vídeo em `k39.py`.
- `cena.py` (lotes `PH PA PE1 PE2 PE3 PE4 PE5 PE6 PS`; `PT` = teste localizado, fora do vídeo); seções `sec_h.py`, `sec_a.py`, `sec_e1.py` … `sec_e6.py`, `sec_s.py`.
- 3D: `threejs/cena3d/c39.js` (`octante.html`, `pappus.html`), porte do `c3d39.html` com a câmera vinda do Manim; `threejs/r3d.js` (pedidos por quadro).
- Âncoras estimadas: `gerar_ancoras.py` → `ancoras.json`, `duracoes_estimadas.json` (0,15 + palavras/3 + 0,35 s).
- Comandos: `./seco.sh LOTE` (passada seca), `./render.sh LOTE` (540p15), `./render3d.sh LOTE` (PE3, PE6), `./still.sh LOTE t`; `vigia.ps1` encerra
  `latex`/`dvisvgm` desta unidade se o log parar > 150 s.
- Conversão: 1 u do Manim = 120 px a 1080p (`PX()`); os palcos dos alvos são dados em px.


## Estado (fechamento 2026-11-16)
Master 1080p30 CRF 14: renders/yt_0039_master_final_1080p30.mp4 (1617,23 s); legenda.srt (425 blocos); voz ElevenLabs v4 (narracao_final.wav); sincronia por reamostragem do tempo do vídeo (warp.py); entrega em entregas/Cálculo III - EP 14 - Exercícios do módulo 3.4 - 0039/.
