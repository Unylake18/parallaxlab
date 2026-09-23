# vid_0001 — Integração por partes

- Exercício do primeiro ciclo: ∫ x²eˣ dx.
- Cena aprovada: `cena.py`, classe `Integral001` (Manim 0.21.0, quadro lógico 9×16).
- Resultado: eˣ(x² − 2x + 2) + C; duas aplicações de integração por partes e checagem pela derivada.
- Roteiro final reconstruído em `roteiro.md` a partir da cena, da narração e do SRT; não havia roteiro separado no repositório inicial.
- Voz final: `audio/narracao_final.mp3`, 68,939 s. Os sete blocos MP3 originais são fontes não regeneráveis e foram preservados.
- Legenda final: `legenda.srt`, 29 entradas, embutida na versão legendada.
- Master limpo: `renders/vid_0001_integracao_por_partes_final_master_limpo.mp4`.
- Final legendado: `renders/vid_0001_integracao_por_partes_final_legendado.mp4`.
- Ambos: 1080×1920, 30 fps, 2.085 frames e 69,500 s. O áudio termina em 68,939 s.
- Capa local: `capa_instagram.png`. Publicação: ver `publicacao.md`.
- QA técnico concluído; reprodução física em celular e backup externo dos MP4 ainda não verificados.

Os MP4 em `renders/` são ignorados pelo Git. A unidade versionada preserva cena,
narração, blocos originais, legenda, capa e documentação; para recuperar o
arquivo final sem refazer a montagem, também é preciso preservar os dois MP4
fora do Git. Não há confirmação de backup externo nesta consolidação.

## Reconstrução a partir das fontes

Na raiz, com o ambiente Manim funcional, renderizar `Integral001` em
1080×1920/30 fps. O visual silencioso padrão é
`media/videos/cena/1920p30/Integral001.mp4`. Depois:

```powershell
python videos/montar_master.py media/videos/cena/1920p30/Integral001.mp4 videos/vid_0001_integracao_por_partes/audio/narracao_final.mp3 renders/vid_0001_integracao_por_partes_final_master_limpo.mp4
python videos/montar_legendado.py renders/vid_0001_integracao_por_partes_final_master_limpo.mp4 videos/vid_0001_integracao_por_partes/legenda.srt renders/vid_0001_integracao_por_partes_final_legendado.mp4 --style piloto
```

Os scripts foram testados nesta consolidação. A reconstrução mantém conteúdo
e formato, mas nova codificação não promete bytes idênticos ao MP4 aprovado.
