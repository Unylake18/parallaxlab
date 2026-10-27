# VID 0022 — cena silenciosa para revisão

Implementação do handoff “Superfície de um líquido em rotação”, série POR TRÁS DA FÓRMULA. Escopo concluído: cena silenciosa e um preview vertical. Nenhuma inconsistência objetiva de física ou de storyboard foi encontrada.

## Artefato

- Preview: [preview_silencioso.mp4](media/videos/cena/960p15/preview_silencioso.mp4).
- Caminho absoluto: `C:\Users\Pichau\PycharmProjects\manim-fisica\videos\vid_0022_liquido_rotacao\media\videos\cena\960p15\preview_silencioso.mp4`.
- Duração: 174 s planejados; 173,998 s no contêiner MP4 (2min54s).
- 540×960, 15 fps nominais, 2.610 quadros, H.264/yuv420p, sem faixa de áudio; 2.258.522 bytes.
- Inspeção: [folha de QA](qa/folha_qa.png), 24 quadros individuais em `qa/` e [metadados](qa/metadados.json).

## Arquivos criados ou alterados

Na unidade `videos/vid_0022_liquido_rotacao/`:

- `cena.py`: classe `LiquidoRotacao022`, com todos os passos do storyboard.
- `ficha.md`: especificação da unidade e marcos temporais.
- `configuracao_3d.py`: parâmetros das quatro sequências necessárias.
- `preparar_3d.py`: preparação pela ponte existente e exportação da seção projetada.
- `inspecionar_preview.py`: leitura dos metadados e extração dos quadros de QA do único preview.
- `cache_3d.json`, `projecao_3d.json`, `duracao_preview.json`, logs, este relatório e artefatos em `media/` e `qa/`.

No arsenal, somente o registro `experimentos/blender/arsenal/solidos/liquido_rotacao.json` foi atualizado nesta rodada: status `aprovado` e nota da aprovação explícita do handoff. As alterações preexistentes no arsenal foram preservadas. Não houve alteração de `template/`, dependências ou implementação do asset nesta rodada.

## Integração do 3D

As sequências foram preparadas por `ponte.sequencia` e carregadas por `Solido3D(render='nunca')`. O render Manim consome os PNGs existentes sem disparar Blender implicitamente.

Na abertura, plano, morph e estado final usam `fenomeno`, com o setor angular aprovado e sem tracers. A fase angular permanece contínua entre as sequências; a mudança da forma usa somente a metade crescente do morph. Forma e fase continuam independentes. O morph é uma interpolação didática entre estados, sem pretensão de simular o transiente.

O miolo analítico é inteiramente Manim 2D. No payoff, a curva completa é transformada para as coordenadas da seção meridiana exportadas pela mesma câmera do Blender. O volume é então revelado por opacidade no modo `geometria`, com seção e grade, sem setor de rotação. A indicação de Δh usa pontos projetados das alturas final no eixo e na borda.

## Verificações e QA

- `py_compile` dos quatro módulos Python: passou.
- Import localizado de `LiquidoRotacao022`: passou.
- Preparação das quatro sequências 3D: concluída; nenhuma variante adicional foi renderizada.
- Um render Manim completo em 540×960/15 fps: concluído, 92 animações, sem erro.
- Metadados e ausência de áudio verificados por PyAV. A pequena diferença do fps médio (15,000168) decorre dos timestamps de concatenação; a taxa nominal é 15.
- `git diff --check`: sem erros de whitespace; apenas aviso de conversão LF/CRLF em arquivo preexistente do arsenal.
- Inspeção visual de 24 estados do preview, incluindo abertura 3D → Manim e perfil 2D → seção 3D.
- Força interna para fora, externa para dentro e maior; aceleração voltada ao eixo e `a_r=-ω²r`.
- Gradiente radial construído após as forças e a expansão local de pressão; cancelamentos visuais e interpretação positiva do gradiente.
- Hidrostática vertical, derivada total e regra da cadeia explícitas; tangentes mais inclinadas com o raio.
- Integração em `r≥0`, identificação de `z0` com a altura final no eixo e espelhamento somente depois do resultado.
- Fórmula final de Δh, legibilidade no formato vertical e área inferior conferidas; sem clipping ou sobreposição impeditiva nos estados inspecionados.
- Sem força centrífuga, exemplo numérico ou partículas editoriais.

## Teste do arsenal

- Sólido: `liquido_rotacao`, aprovado e autorizado para esta unidade.
- Resolução: 540×960, fundo transparente, 24 amostras.
- Custo: 321 PNGs, 167,6 s de render Blender registrados; 151.366.840 bytes (144,35 MiB) de cache. Preview Manim: 2,15 MiB.
- Caches em `renders/arsenal3d/liquido_rotacao/`: `b470c0bd943c` (plano, 96 quadros), `5798281ceb3d` (morph, 128), `7871f61b0bca` (final, 96), `bbef21120408` (geometria, 1).
- Funcionou: enquadramento vertical, setor contínuo na abertura, correspondência da seção projetada e prioridade da geometria no payoff.
- Faltou: nenhum recurso geométrico necessário ao handoff. Qualidade e custo em 1080×1920 não foram avaliados nesta fase.
- Resultado: encaixou na abertura e no payoff; o desenvolvimento analítico permanece mais claro em 2D.

## Limites da rodada

Este arquivo é um preview para revisão. Não foram produzidos render 1080×1920, voz, SRT, master, capa ou publicação. Não houve commit ou push. A revisão editorial pelo usuário permanece como próxima decisão; nenhuma etapa posterior foi iniciada.
