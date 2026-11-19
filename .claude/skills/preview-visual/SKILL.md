---
name: preview-visual
description: Renderiza o preview de um vídeo (540×960/15fps curto ou 960×540/15fps longo), só da cena afetada, e gera a prancha de quadros para o usuário repassar ao GPT. Usar quando pedirem preview, "ver como ficou", conferir quadros ou iterar visualmente uma cena.
---

# Preview visual

Fase de preview: **não** crie voz, SRT, master, legendado nem publicação.

## Passos

1. `git status --short` e preserve alterações existentes.
2. Leia `videos/vid_NNNN_*/ficha.md` (ou `videos_longos/yt_NNNN_*/ficha.md`) e veja `formato:` (`curto_vertical` ou `longo_horizontal`). Leia `cena.py` só se a cena for afetada.
3. Renderize **somente a classe/variante afetada**:
   - Curto: `uv run python -m manim -r 540,960 --fps 15 videos/vid_NNNN_*/cena.py Classe`
   - Longo: `uv run python -m manim -r 960,540 --fps 15 videos_longos/yt_NNNN_*/cena.py Classe`
4. Se houver sólido 3D (`solido_3d:`), confirme que as sequências foram preparadas com `ponte.py` e confira os quadros do sólido.
5. Extraia quadros nos instantes relevantes (início, transições, estado final de cada beat; use `-s` do Manim ou ffmpeg) e monte uma prancha. Guarde em `renders/` da unidade (preview, não final).
6. Envie a prancha ao usuário com `SendUserFile` (ele repassa ao GPT). Descreva em uma linha o que cada quadro mostra.

## Economia de contexto (tokens)
- **Render com saída filtrada:** rode o Manim com `--progress_bar none` e redirecione o log para arquivo (`> renders/_log_preview.txt 2>&1`); leia só o fim ou os erros (`tail -n 30`, `grep -iE "error|traceback" -A 15`). Nunca despeje o log inteiro no contexto.
- **Olhar crítico não se negocia:** todo quadro que você confere é lido em **resolução cheia do preview**, nunca reduzido. A economia vem de escolher os quadros, não de encolhê-los: confira os beats afetados pela correção (início, transição, estado final) e os vizinhos que podem ter sido atingidos; não reconfira beats que não mudaram.
- **Detalhe fino:** para alinhamento, rótulo ou borda, recorte a região em tamanho real (ou maior, `ffmpeg -vf crop=...,scale=iw*2:-1`) além do quadro inteiro.
- A prancha completa para o usuário continua igual (todos os quadros, via `SendUserFile`).
- **`cena.py` por trechos:** localize com `Grep` (nome da classe, `def`, texto da fala) e leia com `offset`/`limit`; leia o arquivo inteiro só se for reestruturar a cena.
- **Não reler para confirmar:** depois de um `Edit` bem-sucedido, não releia o arquivo; confirme com `py_compile`.

## Verificações baratas primeiro
`py_compile` do `cena.py`, inspeção do diff e render do preview. Não rerenderize variantes que não mudaram nem faça QA completo a cada alteração pequena.

## Matemática
Conferir se nenhum índice/debug de MF-Tools (`show_indices`, `bounding_box`) ficou na cena.

## Fechamento
Siga o relatório de entrega do `AGENTS.md`: arquivos alterados, o que foi renderizado, caminho do preview e da prancha, pendências. Depois pare.
