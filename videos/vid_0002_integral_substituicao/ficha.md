# vid_0002 — Integral por substituição

- Série: Cálculo + aplicações físicas; exercício 2 do primeiro ciclo.
- Cena: `cena.py`, classe `Integral002`; alternativa `Integral002SemCoda`.
- Questão: ∫ 2x cos(x²) dx.
- Resposta: sin(x²) + C.
- Ideia central: reconhecer a função interna x² e sua derivada 2x; a substituição desfaz a regra da cadeia.
- Formato: 9:16, área lógica 9×16; preview de produção 540×960/15 fps.
- Áudio-fonte aprovado: `audio/narracao_final.wav` (71,024 s, intacto).
  `preparar_audio.py` recria `audio/narracao_montagem.wav` (69,224 s) com
  corte de 1,8 s de silêncio inicial e correção pontual de +1,2 dB.
- Legendas: `legenda.srt`, 25 entradas alinhadas à narração da montagem.
- Finais 1080×1920/30 fps: `renders/vid_0002_integral_substituicao_final_master_limpo.mp4`
  (sem legenda embutida) e `renders/vid_0002_integral_substituicao_final_legendado.mp4`.
- Duração final: 69,433 s; áudio aprovado: 69,224 s. Status: exportação e QA técnico
  concluídos; pendente revisão física em celular. Sem publicação.
- Capa local: `capa_instagram.png`; estado de publicação em `publicacao.md`.
- Template, piloto e dependências preservados. Componentes específicos ficam nesta unidade.

## Matemática verificada

u = x²; du = 2x dx. Logo ∫ 2x cos(x²) dx = ∫ cos(u) du = sin(u) + C
= sin(x²) + C. Pela regra da cadeia, d/dx[sin(x²) + C] = cos(x²) · 2x
= 2x cos(x²). A constante tem derivada zero.

Na coda, F(x) = sin(x²) é o representante C = 0 da família de primitivas.
F′(x) = 2x cos(x²). Em 0 < x < √(π/2), F cresce; em √(π/2), a tangente
é horizontal; depois desse máximo, até x = 1,6, F decresce.

## Execução

Na raiz, quando o Python da `.venv` estiver disponível:

```powershell
uv run python -m manim -s -r 540,960 --fps 15 videos/vid_0002_integral_substituicao/cena.py Integral002
uv run python -m manim -r 540,960 --fps 15 videos/vid_0002_integral_substituicao/cena.py Integral002
uv run python -m manim -r 1080,1920 --fps 30 videos/vid_0002_integral_substituicao/cena.py Integral002
```

Para remover a coda, selecionar `Integral002SemCoda`: a resolução se encerra
após a síntese, sem depender dos gráficos. A sincronização e a cópia derivada
da narração estão registradas em `revisao.md`. Os MP4 são ignorados pelo Git;
o backup externo deles ainda não foi verificado. A partir do render visual
silencioso, `videos/montar_master.py` combina vídeo e
`audio/narracao_montagem.wav`; `videos/montar_legendado.py` usa o master limpo
e o SRT. Uma recodificação futura não garante MP4 idêntico bit a bit.

Para reconstruir após novo render de `Integral002` em 1080×1920/30 fps:

```powershell
python videos/vid_0002_integral_substituicao/preparar_audio.py
python videos/montar_master.py media/videos/cena/1920p30/Integral002.mp4 videos/vid_0002_integral_substituicao/audio/narracao_montagem.wav renders/vid_0002_integral_substituicao_final_master_limpo.mp4
python videos/montar_legendado.py renders/vid_0002_integral_substituicao_final_master_limpo.mp4 videos/vid_0002_integral_substituicao/legenda.srt renders/vid_0002_integral_substituicao_final_legendado.mp4
```
