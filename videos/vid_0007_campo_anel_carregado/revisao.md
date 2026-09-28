# vid_0007 — Revisão e QA final

## Finais

| Arquivo | Vídeo | Frames | Duração | Áudio |
|---|---|---|---|---|
| `renders/vid_0007_campo_anel_carregado_final_master_limpo.mp4` (8.347.125 B) | H.264, 1080×1920, 30 fps | 4.449 | 148,3 s | AAC 44,1 kHz estéreo, 148,0 s |
| `renders/vid_0007_campo_anel_carregado_final_legendado.mp4` (7.772.992 B) | H.264, 1080×1920, 30 fps | 4.449 | 148,3 s | AAC 44,1 kHz estéreo, 148,0 s |

Reprodução, na raiz do repositório:

```powershell
uv run python -m manim -r 1080,1920 --fps 30 videos/vid_0007_campo_anel_carregado/cena.py CampoAnel007
uv run python videos/montar_master.py media/videos/cena/1920p30/CampoAnel007.mp4 videos/vid_0007_campo_anel_carregado/audio/narracao_final.wav renders/vid_0007_campo_anel_carregado_final_master_limpo.mp4
uv run python videos/montar_legendado.py renders/vid_0007_campo_anel_carregado_final_master_limpo.mp4 videos/vid_0007_campo_anel_carregado/legenda.srt renders/vid_0007_campo_anel_carregado_final_legendado.mp4 --color-module videos/vid_0007_campo_anel_carregado/cena.py
uv run python videos/vid_0007_campo_anel_carregado/gerar_capa.py
```

## Física

- Posição de P, comprimento da seta e marcador do gráfico saem de e(u) com um único
  `self.u`; a varredura do C8 só muda o ritmo (rate_func), não a função.
- Asserts no import de `cena.py`: E(0) = 0; argmax em u = 1/√2 e E_max ≈ 0,3849 kQ/R²;
  dE/dz > 0 antes, 0 e < 0 depois do pico (e igual à derivada numérica); z ≫ R ⇒ E·z² → kQ;
  E_z(−z) = −E_z(z); k dq/s² · z/s = kz dq/(R² + z²)^{3/2}; pico do gráfico = pico físico.
- Na cena: par oposto com laterais opostas e axiais iguais; θ desenhado = arccos(z/s) e o
  mesmo θ dentro do triângulo; R/√2 só surge com o marcador no pico (assert).
- Sem Lei de Gauss; o triângulo R, z, s só no corte lateral (verdadeira grandeza).

## QA visual

Três previews silenciosos 540×960/15 fps com revisões da Produção (escala e centralização
do anel, C4 em nove estados, C5 com a origem de s³ e de 3/2, colisão do ∫dq = Q) e preview
sincronizado com o áudio; margens verificadas pela própria cena (`check_safe_area`: nada
abaixo de y = −4,6 nem fora de |x| < 3,5) e pelo dry run da timeline. Folhas de frames
com os estados críticos a 360 px de largura: sem colisões, fórmulas legíveis, uma relação
principal por estado, cores com significado fixo.

## QA de áudio

`audio/narracao_final.wav` intacta (sem corte, ganho ou normalização): fala de 0,04 a
147,83 s; pico −5,4 dBFS, sem clipping; nível estável (mediana −26,9 a −29,4 dB por
trecho de 16 s); maior pausa interna 0,34 s. Áudio presente e completo no master e no
legendado.

## QA de legenda

`legenda.srt`: 54 cues de 0,04 a 147,97 s, até duas linhas, linha mais larga 449 px
(limite 468 px do `montar_legendado.py`); quebras preferindo pontuação e evitando palavra
fraca no fim da linha; tempos das pausas medidas no áudio. Amostra de frames do legendado
final em 1080p (meio das cues): faixa da legenda abaixo do conteúdo. Termos coloridos:
elemento de carga (ciano), outro do lado oposto (magenta), hipotenusa, três meios,
R sobre raiz de dois e 0,71 R (violeta).

## Capa

`capa_instagram.png` (1080×1920), gerada por `gerar_capa.py`: “ONDE O / CAMPO ELÉTRICO /
É MAIS FORTE?”; painel com o anel carregado (P no máximo, seta, rótulo “anel” na fonte das
fórmulas com linha-guia) e o gráfico E(z) com o pico em magenta, pelas funções da cena.
Escolhida entre variações de headline e de rótulo; conferida em tamanho cheio e miniatura.

## Limitações reais

- Sincronia obtida por pausas do áudio, não por transcrição; conferida por amostras.
- Na miniatura muito reduzida (~180 px), o rótulo “anel” e a linha da série viram detalhe;
  headline, anel, seta e pico seguem legíveis.
- QA físico em celular, backup externo dos MP4s e publicação ainda não registrados.
