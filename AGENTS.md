# AGENTS.md — Parallax Lab

Instruções operacionais para agentes de código que trabalham neste repositório.

## Idioma

Responda sempre em português do Brasil (pt-BR), incluindo explicações, planos, dúvidas e relatórios de entrega.
Preserve comandos, nomes de arquivos e identificadores de código quando necessário.

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
- `docs/guia_mestre.md` — estratégia ampla;
- `docs/formatos.md` — formatos curto vertical e longo horizontal, campos da ficha (inclui `solido_3d:`) e relatório "Teste do arsenal";
- `docs/mapa_curricular.md` — arquitetura curricular/editorial; usar para localizar uma pauta dentro de Física/Cálculo e entender como ela se conecta à biblioteca futura;
- `experimentos/blender/arsenal/catalogo.md` — arsenal de sólidos 3D (Blender) e seu padrão visual. Ao planejar um vídeo que precise de um sólido 3D (cilindro, casca, esfera etc.), consulte o catálogo ANTES de modelar algo novo: confira "usar quando / não usar quando" e o status (só `aprovado` serve); `experimentos/blender/arsenal/cobertura.md` mostra, por capítulo do mapa curricular, o que existe e o que falta. Ponte com o Manim pronta (sandbox): `Solido3D` em `experimentos/blender/arsenal/manim_solido3d.py` (uso e cuidados no `README.md` do arsenal); prepare as sequências antes do render final com `ponte.py`. Usar um sólido num vídeo continua exigindo handoff explícito. Para ver um sólido no Blender: `experimentos/blender/arsenal/abrir/<id>.bat`. O arsenal deve ser testado nos próximos vídeos (curtos e longos): ver `docs/formatos.md`.

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

## Qualidade de render e codificação (padrão único, desde 2026-10-09)

Um padrão só para master e legendado: **H.264, yuv420p, CRF 14**. Medido num trecho denso (linhas finas): abaixo de 14 o ganho é desprezível e o
arquivo cresce 12–25%; acima de 14 as linhas finas degradam (pior bloco SSIM: 0,88 em 14 · 0,78 em 16 · 0,56 em 20 · 0,48 em 23). Vale para Codex, Claude Code e qualquer CLI.

- **Render final do Manim (1080p ou maior):** não precisa configurar nada. `template/config.py` chama `template/qualidade.py`, que troca o CRF 23 do Manim por 14
  automaticamente (todo `cena.py` importa o template). Preview 540p fica no padrão do Manim (CRF 23, mais rápido).
  Sobrescrever só com a variável `CRF` (`CRF=0` fonte sem perdas; `CRF=18` teste). O número mora em `template/qualidade.py` (`CRF_PADRAO`).
- **Conferir um arquivo:** o x264 grava `crf=` no stream (`uv run python -c "import av,re;c=av.open('ARQ.mp4');d=b''.join(bytes(p) for _,p in zip(range(4),c.demux(c.streams.video[0])));print(re.search(rb'crf=([0-9.]+)',d).group(1))"`). Master final esperado: `14.0`.
- **Master:** é o render do Manim com a voz colada sem recompressão (`videos/montar_master.py`, `montar_final.py`). A qualidade do master é a do render: master em CRF 23 não melhora recodificando; só re-renderizando.
- **Legendado (`videos/montar_legendado.py`):** recodifica com `--crf auto` (padrão) = `max(14, CRF do master − 5)`: master em 14 → legendado em 14; master antigo em 23 → 18 (14 só incharia o arquivo). Preset `medium`. `--crf N` força.
- **Encoders próprios de montagem/postagem:** CRF 14, preset `medium` ou `slow`, nunca abaixo de 14 sem motivo. Fonte arquivística sem perdas (CRF 0) só quando pedida.
- **Vídeos longos com legenda `.srt` separada:** não há legendado embutido; o master em CRF 14 é o único vídeo final.
- Não "melhorar" qualidade acima do necessário: CRF menor que 14 só com evidência medida.

## Entregas finais (pasta única)

Toda versão final de vídeo vai para `entregas/`, uma pasta por vídeo: `Série - EP NN - Assunto - NNNN`, com `master`,
`legendado`, `legenda`, `capa` (só a escolhida), `audio/`, `texto/` e `manifesto`; o número do vídeo (`0016`) vai no fim de todo nome de
arquivo (`master - 0016.mp4`). Vale para qualquer agente.

- Ao fechar uma versão final: `uv run python videos/entregar.py vid_NNNN` (cópia; não move nem apaga origens) e informar no
  relatório o caminho da pasta em `entregas/`.
- Não deixar finais soltos em `renders/` nem em `videos/vid_NNNN/renders/` como destino definitivo; previews e
  intermediários podem continuar lá.
- Série, EP e assunto vêm da `ficha.md` (`Série pública: **NOME · EP. N**` e `# Assunto`) ou de
  `videos/entregas_registro.json`. Detalhes em `docs/entregas.md`.

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

## Arsenal 3D em vídeos novos (teste em andamento)

O arsenal de sólidos 3D (90 sólidos aprovados) está em fase de **teste em vídeos reais**, curtos e longos. Ao receber o briefing de um vídeo novo:

0. Índice enxuto de consulta rápida: `experimentos/blender/arsenal/indice_producao.md` (gerado por `gerar_indice.py`; regerar ao criar ou editar sólidos). O briefing de Produção também o consulta para preencher `solido_3d:`.
1. Leia o campo `solido_3d:` da `ficha.md`/briefing. Se houver um `id`, ele é a especificação: integre só nessa unidade.
2. Se o campo faltar ou for `nenhum` sem justificativa, **avalie antes de implementar**: consulte `experimentos/blender/arsenal/catalogo.md` e `cobertura.md` (usar quando / não usar quando; só `aprovado`) e **reporte** o candidato (ou "nenhum, porque ...") sem integrar por conta própria. O briefing de Produção continua soberano. O 3D só dá a geometria: valores, fórmulas, rótulos, sinais e setas de sentido são do Manim; não force 3D onde o 2D explica melhor.
3. Com o `id` definido, siga o checklist de `experimentos/blender/arsenal/README.md` (seção "Uso no Manim"): `Solido3D` na `cena.py` da unidade, sequências preparadas com `ponte.py` antes do render final, quadros conferidos no preview, e nada em `template/`. Não invente sólido nem parâmetro fora do catálogo: se faltar algo, registre como "ajuste desejado" no relatório em vez de improvisar.
4. No relatório de entrega, inclua o **"Teste do arsenal"**: sólido usado, resolução, custo/peso, o que funcionou e o que faltou (formato em `docs/formatos.md`). Isso alimenta os ajustes do arsenal.

## Formatos e paralelismo

Referência: `docs/formatos.md`.

- Identifique o formato lendo `formato:` na `ficha.md` da unidade: `curto_vertical` ou `longo_horizontal`.
- Curto (`videos/vid_NNNN_*`) usa `template/config.py`, sem mudança. Longo (`videos_longos/yt_NNNN_*`) usa `template/config_horizontal.py` e, se útil, `template/layout_horizontal.py`.
- Nunca converta um formato no outro automaticamente nem use crop como solução.
- Produção de vídeo altera apenas a própria unidade por padrão.
- `template/`, `assets/`, `pyproject.toml`, `uv.lock`, `AGENTS.md` e `docs/` globais são compartilhados: não altere no meio de uma unidade sem handoff explícito. Dois agentes nunca editam arquivos globais ao mesmo tempo.
- Dois agentes em paralelo: um worktree e uma branch por agente (ex.: `video/short-NNNN`, `video/long-NNNN`), sem mexer na pasta do outro vídeo.
- Não crie ambientes Python separados: worktrees usam a `.venv` do checkout principal via `UV_PROJECT_ENVIRONMENT` e `uv run --no-sync`.
- Para escolher ou posicionar conteúdo longo, consulte `docs/mapa_curricular.md`. Ordem de publicação não é ordem curricular; não invente posição curricular que o mapa não sustente.
- O briefing de Produção (matemática, física, roteiro) continua soberano sobre a implementação.

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
2. reporte verificações, testes e renders executados, com seus resultados;
3. informe o caminho do preview e dos demais artefatos gerados, quando houver;
4. reporte limitações ou pendências reais, incluindo verificações que não puderam ser concluídas;
5. pare, sem iniciar outra fase da produção.

Esse relatório de entrega é obrigatório ao concluir qualquer briefing ou handoff, mesmo quando o pedido não repetir o formato.
