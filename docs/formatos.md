# Formatos do Parallax Lab

**Criado em:** 2026-10-03 · decisão em `docs/decisoes.md` (2026-10-03 — Duas trilhas).

O Parallax Lab tem duas trilhas, com **uma identidade visual, um toolchain e uma `.venv`**.
São duas apresentações do mesmo laboratório, não dois projetos. Todo vídeo declara o
formato na `ficha.md`; o agente lê a ficha antes de escolher configuração e layout.

| | Curto | Longo |
| --- | --- | --- |
| Identificador | `curto_vertical` | `longo_horizontal` |
| Destino | Reels, Shorts e verticais equivalentes | YouTube long-form |
| Proporção / frame lógico | 9:16 / 9 × 16 | 16:9 / 16 × 9 |
| Preview | 540×960, 15 fps | 960×540, 15 fps |
| Final | 1080×1920, 30 fps | 1920×1080, 30 fps (planejado) |
| Configuração | `template/config.py` | `template/config_horizontal.py` + `template/layout_horizontal.py` |
| Pasta | `videos/vid_NNNN_*` | `videos_longos/yt_NNNN_*` |
| Duração | ~1–3 min | alvo 8–10 min; ~8–12 min quando a clareza exigir |
| Princípio | uma ideia forte → construção visual → payoff | compreensão profunda, Manim-first |

Os valores do longo são **decisão de produção interna inicial**, não regra de plataforma.
Nos dois formatos o final tem 120 px por unidade de cena: o mesmo `font_size` resulta no mesmo
tamanho em pixels.

Nunca converter um formato no outro automaticamente nem usar crop como solução editorial.
A composição 9:16 e a 16:9 são feitas conscientemente para cada formato.

## 1. Curto vertical (`curto_vertical`)

O template vertical existente é a fonte de verdade e não é redesenhado aqui. Os vídeos
históricos continuam importando `template/config.py`.

- **Uma** ideia principal; não alongar para caber mais conteúdo.
- Famílias: EXERCÍCIO RESOLVIDO · POR TRÁS DA FÓRMULA · DA EQUAÇÃO AO FENÔMENO.
- Voz narra a física/matemática conceitual; o Manim carrega a álgebra intermediária; a voz não lê
  todas as fórmulas.
- Tela: poucos elementos simultâneos, fórmulas grandes, prioridade absoluta para celular, espaço
  inferior preservado, uma relação matemática central por estado quando possível.

## 2. Longo horizontal (`longo_horizontal`)

Objetivo: compreensão profunda, biblioteca didática modular, derivação completa quando necessária,
espaço para verificação, limites, comparação e aplicações.

Não é: professor falando sobre slides, dashboard cheio, Reel esticado ou sequência de fórmulas
estáticas. Não alongar um assunto artificialmente para atingir duração.

### Naturezas

**`teoria_visual`** — ensinar um conceito de forma progressiva e visual. Não precisa ser aula
curricular exaustiva.
gancho/pergunta → intuição geométrica ou física → definição formal → desenvolvimento/derivação →
interpretação visual → exemplo → limites/checagem → síntese.

**`exercicio_resolvido`** — resolver um problema universitário forte do começo ao fim.
problema → modelagem → estratégia → conta → resultado → verificação → análise adicional →
interpretação. Não termina quando sai o número: “o que mais conseguimos aprender do resultado?”
(o DNA do vídeo do campo do anel).

**`derivacao_aplicada`** — construir um resultado conhecido e mostrar o que ele significa.
fenômeno/pergunta → hipóteses → modelo → derivação → resultado → aplicação/visualização →
limites de validade. Versão longa de “Por Trás da Fórmula / Da Equação ao Fenômeno”.

### Organização da biblioteca

CURSO/EIXO → MACROASSUNTO → MÓDULO → VÍDEO AUTOSSUFICIENTE. Não estruturar como “Aula 1, Aula 2, Aula 3”;
playlists ordenam depois. Cada vídeo funciona sozinho, pertence a um módulo e tem título baseado
na pergunta real, sem depender de numeração.

Exemplos: Mecânica → Energia e potencial → “Como prever o movimento usando apenas o potencial?”;
Física I → Mecânica → Lançamentos → “Por que o lançamento ótimo de uma altura não é a 45°?”.

Onde cada conteúdo se encaixa (curso/eixo → macroassunto → módulo) está em `docs/mapa_curricular.md`.
Este documento define **como** o vídeo longo é produzido; o mapa define **onde** ele entra na biblioteca.
A publicação pode ocorrer fora da ordem curricular.

### Composição

`mais espaço = mais clareza`, não `mais espaço = mais informação simultânea`. Em geral, uma
representação dominante ou duas sincronizadas; evitar três painéis permanentes. Regiões são
composição, não caixas desenhadas.

| Modo | Uso | Em `layout_horizontal.py` |
| --- | --- | --- |
| **FOCUS** | uma equação, gráfico, objeto ou payoff; muito espaço negativo | `FOCUS` |
| **SPLIT** | o mais importante: fenômeno/geometria à esquerda, equação/gráfico à direita | `split(0.5)` ou `split(0.55)` |
| **COMPARE** | antes/depois, aproximação/exato, caso A/B; no máximo duas ideias | `split(0.5)` |
| **BUILD** | derivação: transformar a relação atual em vez de empilhar 6 linhas históricas | `FOCUS` ou um lado do split |

No SPLIT, quando há relação quantitativa, o **mesmo parâmetro** controla as duas representações
(ex.: órbita + gráfico, projétil + R(θ), circuito + derivação).

**Safe area inicial** (frame 16 × 9; regra interna, ajustar só com evidência): conteúdo crítico em
`|x| ≤ 7,2` e `|y| ≤ 3,8`; faixa de título acima de `y = 2,6`; faixa inferior `y < −3,0` reservada a
legendas, controles e respiro. Tag de série e watermark ficam nos cantos, fora do conteúdo crítico.
`GUIAS=1` desenha as guias em desenvolvimento; elas nunca entram no render normal.

### Visual ao extremo, com propósito

Objetos físicos animados, vetores, diagramas, gráficos sincronizados, parâmetros mudando em tempo
real, curvas construídas progressivamente, transformações de equações, modelo × fenômeno, limites
visíveis, reorganização da composição quando o foco muda. Sempre que possível,
`equação ↔ gráfico ↔ fenômeno` são perspectivas do **mesmo** estado matemático. Nada animado só
porque fica bonito.

### Voz × Manim e ritmo

A voz explica o porquê, hipóteses, interpretação, decisões matemáticas e significado físico. O Manim
explica cancelamentos, substituições, reorganização algébrica, construção de gráficos, evolução de
parâmetros e relações espaciais. Não narrar cada linha já clara na tela.

Sem ritmo de aula gravada: a cada ~30–60 s, algum avanço perceptível (descoberta, resultado
intermediário, mudança de perspectiva, pergunta, teste, comparação, consequência). Não fazer
8 minutos de preparação para um único resultado final.

## Curto × longo

Curto: descoberta, uma ideia, um payoff, alta densidade. Longo: compreensão, construção completa,
análise, biblioteca. Um longo não é um curto esticado; um curto não precisa ser teaser de um longo.
Podem compartilhar tema, diagrama, solução, assets, equações e código matemático realmente genérico.

## Identidade compartilhada

Sem identidade nova para o YouTube. Paleta, tipografia, assets e regras em
`docs/identidade_visual.md`: fundo `#050816`, ciano `#35D9FF`, azul `#267BFF`, violeta `#745CFF`,
magenta `#EA63FF`, branco `#F5F7FF`; Space Grotesk via `screen_text`/`official_text`, MathTex para toda
a matemática. `assets/branding/social/parallax_lab_banner_16x9.png` é referência de branding
horizontal, não fundo obrigatório da aula; o cosmos continua atmosfera sutil.

## Ficha padrão (Markdown, sem automação)

**Curto:** id · série · `formato: curto_vertical` · assunto · pergunta central · solução verificada ·
payoff · duração alvo · storyboard · QA · `solido_3d:` (opcional, ver abaixo).

**Longo:** id · `formato: longo_horizontal` · `natureza:` (`teoria_visual` | `exercicio_resolvido` |
`derivacao_aplicada`) · `macroassunto:` (calculo, mecanica, eletromagnetismo, termodinamica,
ondas_optica, outro) · `modulo:` (texto curto, ex.: energia_e_potencial) · título de trabalho ·
`pergunta_central:` · `pre_requisitos:` · solução/teoria verificada · arquitetura didática ·
`payoff_principal:` · aplicações/exemplos · `duracao_alvo:` · storyboard · QA · `solido_3d:` (opcional,
ver abaixo) · possíveis derivados curtos (opcional).

**`solido_3d:` (curto e longo, opcional).** Ao planejar o vídeo, consulte
`experimentos/blender/arsenal/catalogo.md` (arsenal de sólidos 3D em Blender, com padrão visual em
`experimentos/blender/arsenal/estilo.json`). Registre o `id` do sólido escolhido (só `status: aprovado`) ou
`nenhum`, com uma linha de justificativa pelos critérios "usar quando / não usar quando" da ficha do
sólido. Registrar o campo não autoriza integrar: a integração com o Manim exige handoff explícito.

**Arsenal 3D: funcionalidade nova, a testar nos próximos vídeos.** Desde 2026-10-07 o arsenal tem 90 sólidos
aprovados (Lei de Gauss, eletromagnetismo, mecânica, fluidos, óptica, física moderna, cálculo, álgebra linear e
EDP), vários com movimento (loop ou ciclo único), e a ponte `Solido3D` para o Manim (sandbox, ainda não usada em
vídeo). Nos próximos vídeos **curtos e longos**, ao planejar, confira o `catalogo.md`/`cobertura.md` e, quando um
sólido servir, proponha-o no `solido_3d:` como candidato de teste; depois da produção, anote na ficha se o encaixe
funcionou (legibilidade, peso do render, o que faltou) para ajustarmos o arsenal. Para ver qualquer sólido antes de
decidir, dê dois cliques em `experimentos/blender/arsenal/abrir/<id>.bat` (abre no Blender, em loop).

## Comandos

```powershell
# Curto (preview / final)
uv run python -m manim -r 540,960 --fps 15 videos/vid_NNNN_*/cena.py Classe
uv run python -m manim -r 1080,1920 --fps 30 videos/vid_NNNN_*/cena.py Classe

# Longo (preview / final planejado)
uv run python -m manim -r 960,540 --fps 15 videos_longos/yt_NNNN_*/cena.py Classe
uv run python -m manim -r 1920,1080 --fps 30 videos_longos/yt_NNNN_*/cena.py Classe

# Smoke do horizontal (GUIAS=1 mostra a safe area)
uv run python -m manim -r 960,540 --fps 15 template/smoke_horizontal.py SmokeHorizontal
```

Cena horizontal: importar `template.config_horizontal` (não `template.config`), `template.fonts` e,
se útil, `template.layout_horizontal`. `template/smoke_horizontal.py` é o exemplo mínimo.

## Agentes em paralelo (worktrees)

Quando dois agentes trabalham ao mesmo tempo (ex.: um no curto, outro no longo), cada um usa um
worktree e uma branch próprios, a partir da `main` já com esta infraestrutura:

```powershell
git worktree add ../parallax-short -b video/short-NNNN
git worktree add ../parallax-long  -b video/long-NNNN
```

Os worktrees **compartilham a `.venv` do checkout principal**; não criar `.venv` por worktree. Em cada
shell do worktree:

```powershell
$env:UV_PROJECT_ENVIRONMENT = "<checkout principal>\.venv"
uv run --no-sync python -m manim ...
```

`--no-sync` impede o `uv` de alterar o ambiente compartilhado. Se `uv run` falhar só por restrição
do sandbox do agente, não diagnosticar como ambiente quebrado.

Cada agente trabalha só na própria unidade; pode ler `template/`, `assets/` e `docs/`. Mudanças em
`template/`, `assets/`, `pyproject.toml`, `uv.lock`, `AGENTS.md` ou `docs/` globais são
**compartilhadas** e acontecem em rodada própria, nunca escondidas na produção de um vídeo.
