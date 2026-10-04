# AGENTS.md — Parallax Lab

Instruções operacionais para agentes de código que trabalham neste repositório.

## Princípio

Use o menor contexto suficiente para concluir corretamente a tarefa.

Não releia o repositório inteiro, vídeos anteriores ou toda a documentação por padrão.
Amplie o contexto somente quando houver uma dependência concreta.

## Antes de editar

1. Execute `git status --short`.
2. Preserve qualquer alteração existente.
3. Leia o briefing/handoff recebido.
4. Leia somente os arquivos necessários para aquela tarefa.

Para trabalho comum em um vídeo, comece por:
- `videos/vid_NNNN_*/ficha.md`, quando existir;
- os arquivos específicos citados no handoff;
- `cena.py` somente quando a cena for afetada.

Consulte conforme necessidade:
- `docs/estado_atual.md` — estado operacional atual;
- `docs/padroes_producao.md` — padrões observados entre vídeos;
- `docs/identidade_visual.md` — identidade e marca;
- `docs/decisoes.md` — decisões permanentes;
- `docs/guia_mestre.md` — estratégia ampla.

Não leia automaticamente todos esses documentos.

## Briefing aprovado

Matemática, física, storyboard, direção didática, textos e critérios de QA fornecidos pelo chat de Produção são especificação de implementação.

Não rediscuta ou redesenhe essas decisões por conta própria, salvo inconsistência objetiva.

Se encontrar uma inconsistência, reporte antes de ampliar o escopo.

## Implementação e verificações

Comece pela verificação mais barata que seja suficiente.

Prefira, conforme a tarefa:
- inspeção do diff;
- `py_compile`;
- import localizado;
- preview 540×960 / 15 fps;
- inspeção de timestamps ou estados específicos.

Só amplie testes ou inspeção se houver motivo concreto.

Durante iteração visual:
- renderize somente a variante afetada;
- não rerenderize versões que não mudaram;
- não faça QA completo do vídeo a cada pequena alteração.

QA completo continua obrigatório no fechamento final da unidade.

## Fases da produção

Respeite a fase explicitamente aberta.

Se a tarefa é preview visual, não crie automaticamente:
- voz;
- SRT;
- master final;
- vídeo legendado;
- publicação.

Essas etapas só começam quando forem solicitadas.

## Documentação

Não atualize documentação global automaticamente após cada alteração.

Edite somente os documentos explicitamente pedidos ou aqueles que ficariam factualmente incorretos por causa da própria mudança.

## Git

Nos primeiros dez vídeos, o trabalho normal ocorre em `main`.

Não faça automaticamente:
- branch;
- PR;
- commit;
- push.

Faça essas ações somente quando o handoff pedir.

## Ambiente

Preserve o ambiente validado.

Não execute por rotina:
- `uv init`;
- recriação de `.venv`;
- reinstalação de Python ou Manim;
- alteração de dependências;
- limpeza ampla de cache.

O fluxo operacional de Manim é:

`uv run python -m manim ...`

## Animações matemáticas

Manim Community é a base. MF-Tools 1.4.9 (`from MF_Tools import ...`) é uma dependência utilitária **seletiva**: ao iniciar uma cena com matemática, **considere** o MF-Tools; usá-lo não é obrigatório.

Hierarquia para transformar expressões:
1. `TransformMatchingTex` — padrão, quando a correspondência é clara e didaticamente correta.
2. `TransformByGlyphMap` — quando o controle explícito de termos melhora a compreensão: cancelamentos, reorganização algébrica, termo atravessando a igualdade, cópia deliberada, matching ruim do passo 1.
3. `FadeOut`/`FadeIn` — quando qualquer matching visual seria enganoso.

Regras:
- A animação deve explicar a matemática; não use MF-Tools só para produzir movimento.
- Construa glyph maps somente depois que a expressão/LaTeX estiver estabilizada: eles são frágeis a qualquer mudança no LaTeX. Use `MathTex` de string única nos dois lados.
- `show_indices`, `indexx_labels` e `bounding_box` são ferramentas de desenvolvimento; nunca deixe índices ou debug no vídeo final.
- Prefira `auto_fade` a `auto_morph`; não use `Scene.keep_orientation()`.
- `SurroundingRectangleUnion` exige `unbuff=0` (falha com numpy 2.x); não é padrão.
- Não refaça vídeos anteriores só por causa da biblioteca.

## Formatos e paralelismo

Referência: `docs/formatos.md`.

- Identifique o formato lendo `formato:` na `ficha.md` da unidade: `curto_vertical` ou `longo_horizontal`.
- Curto (`videos/vid_NNNN_*`) usa `template/config.py`, sem mudança. Longo (`videos_longos/yt_NNNN_*`) usa `template/config_horizontal.py` e, se útil, `template/layout_horizontal.py`.
- Nunca converta um formato no outro automaticamente nem use crop como solução.
- Produção de vídeo altera apenas a própria unidade por padrão.
- `template/`, `assets/`, `pyproject.toml`, `uv.lock`, `AGENTS.md` e `docs/` globais são compartilhados: não altere no meio de uma unidade sem handoff explícito. Dois agentes nunca editam arquivos globais ao mesmo tempo.
- Dois agentes em paralelo: um worktree e uma branch por agente (ex.: `video/short-NNNN`, `video/long-NNNN`), sem mexer na pasta do outro vídeo.
- Não crie ambientes Python separados: worktrees usam a `.venv` do checkout principal via `UV_PROJECT_ENVIRONMENT` e `uv run --no-sync`.
- O briefing de Produção continua soberano sobre a implementação.

## Escopo e parada

Não inicie espontaneamente:
- refatoração;
- limpeza;
- automação;
- novo QA;
- nova etapa da produção;
- publicação.

Ao cumprir o escopo:
1. reporte arquivos alterados;
2. reporte testes/renders executados;
3. reporte limitações ou pendências reais;
4. pare.
