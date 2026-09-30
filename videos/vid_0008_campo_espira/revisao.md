# vid_0008 — Revisão e QA final

## Finais

| Arquivo | Vídeo | Frames | Duração | Áudio |
|---|---|---|---|---|
| `renders/vid_0008_campo_espira_final_master_limpo.mp4` (11.427.517 B) | H.264, 1080×1920, 30 fps | 4.581 | 152,7 s | AAC 44,1 kHz estéreo, 152,3 s |
| `renders/vid_0008_campo_espira_final_legendado.mp4` (10.226.886 B) | H.264, 1080×1920, 30 fps | 4.581 | 152,7 s | AAC 44,1 kHz estéreo, 152,3 s |

Reprodução, na raiz do repositório:

```powershell
uv run python -m manim -r 1080,1920 --fps 30 videos/vid_0008_campo_espira/cena.py CampoEspira008
uv run python videos/montar_master.py media/videos/cena/1920p30/CampoEspira008.mp4 videos/vid_0008_campo_espira/audio/narracao_final.wav renders/vid_0008_campo_espira_final_master_limpo.mp4
uv run python videos/montar_legendado.py renders/vid_0008_campo_espira_final_master_limpo.mp4 videos/vid_0008_campo_espira/legenda.srt renders/vid_0008_campo_espira_final_legendado.mp4 --color-module videos/vid_0008_campo_espira/cena.py
uv run python videos/vid_0008_campo_espira/gerar_capa.py
```

`renders/` não é versionado (`.gitignore`); os finais se reproduzem pelos comandos acima.

## Física

Conferências no import de `cena.py` (todas passam): r² = R² + z²; dB ⟂ r nos dois elementos;
transversais opostas e soma do par = 2× a projeção de um; cos α = R/r igual no elemento e em P;
dℓ = R dφ; dB_z = R²/r³ por duas vias; r³ = (r²)^{3/2}; ∫dφ = 2π e 2π/4π = 1/2; B_z coincide
com `b_loop`; B_z(0) = μ₀I/2R; (R²)^{3/2} = R³; B_z z³ → 1 e z → 2z ⇒ B → B/8 (z ≫ R);
geometria desenhada em verdadeira grandeza (catetos R e z, hipotenusa r). Dimensional em tesla
em `comum.py`. No limite usa-se ≃, nunca =; “longe” é longe do centro AO LONGO DO EIXO.

## Sincronia

45 âncoras (`sync.json`); nenhuma âncora atrasada no render final. Duração 152,69 s contra 152,32 s
de áudio (0,37 s de respiro final). Correções que a instrumentação achou: `Scene.wait` chama
`self.play`, então as esperas eram escaladas duas vezes (corrigido com `esperar_cru`); o Manim
arredonda cada animação para cima, então a escala quantiza para o quadro mais próximo.

## QA de legenda

`legenda.srt`: 64 cues de 0,05 a 152,24 s, até duas linhas, linha mais larga 468 px (limite do
`montar_legendado.py`); quebras preferindo pontuação, sem separar “distância axial”, “dois pi”,
“três meios”; cue mais curta 0,83 s, mais longa 3,7 s. Amostra de frames do legendado final em
1080p: faixa da legenda abaixo do conteúdo; termos coloridos com a semântica da cena.

## QA visual

Varredura de 1 frame/s do preview e amostra do legendado. Corrigidos ao longo do processo:
expressões que ficavam empilhadas (fantasmas), esmaecimento que preenchia formas abertas, placa
opaca que cortava raios e setas (trocada por contorno da cor do fundo), fichas ilegíveis
(prateleira agora é memória; a ficha abre grande quando usada) e pico do gráfico encostando na
placa da fórmula. O `check_safe` da cena confere margem lateral, faixa inferior e uma só expressão
na faixa ativa.

## Limitações

- Alinhamento por pausas (sem ASR): ±0,5 s por frase.
- Em A2 e A5 a fala é mais longa que a animação; a cena segura o último quadro.
- Fórmula pequena nas capas B, C, D e F (dividem o painel com um ícone).
