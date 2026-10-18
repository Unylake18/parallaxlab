# Continuidade — vid_0024 — carga em hélice

Estado salvo em 17/10/2026. Última versão: **layout, legibilidade e ritmo**.
Fase aberta: preview visual silencioso em Manim 2.5D. Não há voz, SRT ou master final.
O próximo agente deve analisar este preview e aguardar/seguir a próxima orientação do usuário.

## Arquivos principais

- `cena.py`: implementação atual completa; classe `CargaHelice024`.
- `media_layout_ritmo/videos/cena/960p15/CargaHelice024.mp4`: preview atual completo, 540×960, 15 fps nominais, 2.649 quadros, 176,6 s, sem áudio.
- `media_layout_ritmo/qa/estados_video.json`: marcos medidos no MP4 entregue; usar para localizar trechos.
- `media_layout_ritmo/estados.json`: marcos registrados pela cena durante o render; podem diferir alguns quadros devido ao cache.
- `media_layout_ritmo/qa/{metadados,fisica,ritmo}.json`: resultados das verificações já realizadas.
- `continuidade_manifesto.json`: tamanho e SHA-256 do Python e do MP4 transferidos.
- `briefings/01_implementacao_manim_2_5d.md` a `04_layout_legibilidade_ritmo.md`: especificações e revisão recebidas, em ordem.
- `ficha.md`: identificação e histórico inicial; o preview atual é o indicado neste guia.

## Resultado da última rodada

Gráfico ampliado e exposto por aproximadamente 10,93 s; componente paralela verde `#63E6BE`;
referências algébricas, rótulos e medidas reposicionados; repetição inferior removida;
síntese desacelerada e frase final inteiramente visível por aproximadamente 2,73 s.
End card somente com `@labparallax`. Área inferior reservada para futuras legendas.
Física e representações continuam em Manim 2.5D, sem Blender ou arsenal 3D.

QA já realizado: compilação Python; 1.800 estados físicos com erro máximo de derivada
aproximadamente 1,67e-10; decodificação dos 2.649 quadros; inspeção visual de 112 capturas,
incluindo estados intermediários das transformações MF-Tools; faixa inferior vazia.
Não há necessidade de repetir esse QA apenas para abrir o projeto.

O MP4 entregue inclui rerenders localizados da abertura, entrada/saída do gráfico e
transição da condição de raio, concatenados sem recompressão. Essas correções estão no
Python atual. Os caches e manifests locais de concatenação não são necessários para
continuar: renderizar a cena completa a partir do código quando houver uma mudança.

## Abrir e continuar em outro computador

Repositório: https://github.com/Unylake18/parallaxlab
Branch: `main`. Unidade: `videos/vid_0024_carga_helice`.
Em um checkout existente, salvar o trabalho local e atualizar com `git pull --ff-only origin main`.
Em um computador novo, usar `git clone https://github.com/Unylake18/parallaxlab.git`.

Ler o `AGENTS.md` da raiz, este guia e o briefing mais recente. Assistir ao MP4 acima.
Preservar física, narrativa, glyph maps existentes e a fase de preview.
Os briefings históricos limitavam commit/push às respectivas rodadas; este salvamento
no Git foi autorizado posteriormente pelo usuário, em 17/10/2026.

As dependências Python estão em `pyproject.toml` e `uv.lock` na raiz. Reutilizar o ambiente
local existente quando disponível. Em uma máquina nova, preparar o ambiente com `uv sync`.
Manim/MathTex também requerem LaTeX com dvisvgm no sistema; as fontes Space Grotesk e Inter
vêm de `assets/fonts/` e são registradas pelo helper `template/fonts.py`. Não copiar a `.venv` entre computadores.
O código usa `template/config.py`, `template/fonts.py`, `template/qualidade.py` e a marca
em `assets/branding/overlays/parallax_lab_watermark.png`, mantidos no próprio repositório.

Para gerar um novo preview, executar na raiz:

```powershell
uv run python -m manim -ql -r 540,960 --fps 15 videos/vid_0024_carga_helice/cena.py CargaHelice024
```

O código grava na pasta `media_layout_ritmo`. Antes de uma nova rodada, escolher outra
pasta de saída na unidade para preservar o MP4 enviado. Não produzir voz, legendas,
master ou publicação sem solicitação.

## Arquivos temporários deixados somente neste computador

Frames, ZIPs de análise, caches, renders parciais, logs e previews anteriores não foram
incluídos no Git. Os frames podem ser extraídos novamente do MP4 atual quando necessários.
Nenhum desses arquivos locais foi apagado durante este salvamento.
