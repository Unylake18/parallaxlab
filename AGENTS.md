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
