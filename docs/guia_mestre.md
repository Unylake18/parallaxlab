# Parallax Lab — Física & Matemática com IA + Manim

Guia mestre do Projeto, repositório e produção do canal.

**Versão:** 1.3 · **Referência:** 22 de setembro de 2026 · **Idioma:** português brasileiro.

**Reconciliação operacional — 2026-09-22:** nome oficial Parallax Lab; Instagram @labparallax. A identidade e os oito assets estão aprovados, conforme `docs/identidade_visual.md`; os arquivos já existem localmente, todos untracked, não staged e ainda não commitados. Template básico, cena do piloto e preview com voz já foram produzidos. A aplicação da identidade ao Manim permanece pendente. O piloto atual tem 68,933 s, orientado pela narração aprovada; seu alvo antigo de 45–60 s foi substituído. Exemplos de inicialização e storyboard abaixo são referências históricas, não pendências atuais. Consulte `docs/estado_atual.md` para próximos passos e QA restante.

**Uso:** adicione este arquivo às fontes do Projeto no ChatGPT e mantenha a cópia versionada em `docs/guia_mestre.md`. Para trabalhar hoje, abra primeiro `START_HERE.md`. Para saber a realidade do projeto neste instante, abra `docs/estado_atual.md` — ele é a fonte operacional.

> Princípio do MVP: publicar um bom piloto, depois completar dez vídeos recuperáveis e só então automatizar o gargalo comprovado. O guia orienta; não substitui testes reais nem decisões registradas.

---

## Sumário

1. Direção inicial e resultado esperado
2. Criar o Projeto no ChatGPT
3. Instruções para o Projeto
4. Chats: ordem, função e prompts iniciais
5. Quando usar Chat, Codex, Work, Claude e Gemini
6. Arquitetura de arquivos e convenções
7. Ambiente local no Windows
8. GitHub e uso em outra máquina
9. README e orientações locais ao Codex
10. Identidade visual e template Manim
11. Banco de questões e ficha de produção
12. Pipeline de cada vídeo
13. Piloto `integral_001`
14. Voz, legendas, edição e exportação
15. Publicação nas plataformas
16. QA e definição de pronto
17. Primeiros dez vídeos
18. Métricas e decisões semanais
19. Monetização e produtos futuros
20. Escala e automação
21. Prompts reutilizáveis
22. Ordem de execução
23. Manutenção e recuperação
24. Itens voláteis e fontes

---

## 1. Direção inicial e resultado esperado

Canal educacional faceless para estudantes brasileiros na transição entre ensino médio e início da graduação. Cada vídeo ensina **uma ideia que destrava uma questão**, com solução visual, rigor verificável e leitura confortável no celular.

| Decisão inicial | Padrão |
| --- | --- |
| Formato | Vertical 9:16, Manim, voz em PT-BR e legendas |
| Duração | Normalmente 35–60 s; dividir se a clareza pedir |
| Estrutura | Gancho honesto → ideia → resolução → verificação/conclusão |
| Frequência | Três produções originais por semana, distribuídas onde fizer sentido |
| Prioridade | Correção, legibilidade, compreensão e consistência |
| Marco 1 | Um piloto completo publicado |
| Marco 2 | Dez vídeos publicados, medidos e revisados |

Três vídeos em quatro redes são três produções, não doze. O tablet pode complementar a explicação, mas o piloto pode ser inteiramente Manim.

### Horizonte posterior ao MVP

**Status: PLANEJADA / NÃO IMPLEMENTADA.** Depois do piloto, dos dez vídeos e da análise das métricas, o Parallax Lab poderá ampliar seu escopo para visualizações matemáticas dinâmicas, física animada, conteúdos de intuição e curiosidades. Essa direção não constitui backlog, requisito atual, cronograma ou autorização de implementação. A prioridade permanece: **primeiro piloto → dez vídeos → medir → evoluir e automatizar somente depois**.

## 2. Criar o Projeto no ChatGPT

1. Crie **Canal Física & Matemática — IA + Manim**.
2. Cole as instruções da seção 3.
3. Envie este guia, `START_HERE.md`, `docs/estado_atual.md`, `docs/decisoes.md` e os documentos aprovados.
4. Crie os chats da seção 4 conforme precisar; não é necessário abrir todos antes do piloto.

O Projeto não sincroniza automaticamente com GitHub ou uma pasta local. Após uma decisão duradoura, atualize o arquivo no repositório e substitua/identifique a cópia enviada ao Projeto.

### Fonte operacional: `docs/estado_atual.md`

Este é o primeiro arquivo a atualizar ao terminar uma sessão e o primeiro a ler numa sessão nova:

```markdown
# Estado atual do canal
Atualizado em: AAAA-MM-DD
Guia vigente: 1.3
Ambiente validado: Windows; Python 3.12; uv; Manim Community 0.21.0; MiKTeX/MathTex; MP4 renderizado
Repositório e branch: 
Template vigente: 
Vídeo atual / status: 
Último commit relevante: 
Decisões recentes: 
Pendência concreta: 
Próxima ação: 
```

Não use esse arquivo para ideias longas: elas vão para `decisoes.md`, `banco_ideias.md` ou a pasta do vídeo.

## 3. Instruções para colar no Projeto

```text
Você colabora no “Canal Física & Matemática — IA + Manim”. Responda em português brasileiro, com clareza e proporcionalidade à tarefa.

OBJETIVO: produzir vídeos educacionais autorais, faceless, de física e matemática, sobretudo verticais com Manim, voz e legendas. Uma ideia por vídeo; rigor antes de velocidade.

CONTEXTO ATUAL: Windows, PyCharm, GitHub, ChatGPT, Claude e Gemini, além de Galaxy Tab S6 Lite. O ambiente local JÁ foi validado: Python 3.12, uv funcionando, Manim Community 0.21.0, MiKTeX/MathTex funcionando e primeiro MP4 renderizado. Não recomende reinstalar, recriar ou migrar o ambiente sem uma evidência concreta de necessidade. Preserve o que funciona.

FONTE OPERACIONAL: leia docs/estado_atual.md antes de sugerir próxima ação; ele prevalece sobre descrições antigas do guia. Decisões aprovadas ficam em docs/decisoes.md. Diferencie fatos verificados, decisões e sugestões.

RIGOR: resolva e verifique antes de roteirizar. Para matemática, use uma checagem objetiva como derivar a primitiva; para física, confira hipóteses, unidades, sinais, limites e plausibilidade. Concordância entre IAs não é prova.

PRODUÇÃO: siga questão → solução → verificação → roteiro → Manim → voz → edição → QA → publicar → métricas. Não gere etapas que não foram pedidas. Use transformações visuais para explicar relações, mantenha fórmulas legíveis no celular e não esconda o passo didático central.

FERRAMENTAS: Chat decide e roteiriza; Codex implementa, testa e organiza arquivos; Work serve a pesquisas/entregáveis extensos. Claude e Gemini são revisores independentes, não árbitros por votação.

GIT E AUTOMAÇÃO: nos primeiros dez vídeos, trabalhe em main com commits pequenos e claros. Branch/PR só para mudança maior, arriscada ou compartilhada (template, dependência, automação). Automação é consequência de um processo manual validado e de um gargalo medido.

PUBLICAÇÃO: não afirme regras, formatos, limites ou monetização sem consultar fonte atual e datada. Não publique nem alegue ação externa sem evidência.
```

## 4. Chats: ordem, função e prompts iniciais

| Chat | Função | Registro |
| --- | --- | --- |
| `01 — Master / Estratégia` | Público, promessa, prioridades e decisões | `docs/decisoes.md` |
| `02 — Pipeline Técnico` | Manim, template, render e problemas | `docs/estado_atual.md`, código |
| `03 — Banco de Ideias` | Fila editorial | `docs/banco_ideias.md` |
| `04 — Produção — vid_0001` | Um vídeo do briefing ao QA | `videos/vid_0001_*` |
| `05 — Métricas` | Comparar o primeiro ciclo | `docs/metricas.md` |

Comece apenas com Master, Pipeline e Produção do piloto. Prompt do piloto:

```text
Vamos produzir vid_0001 / integral_001. A questão é ∫ x²eˣ dx. Primeiro apresente a solução com integração por partes duas vezes e confira o resultado final pela derivada. Depois crie roteiro de 45–60 segundos, com fala, tela e animação. Não trate o ambiente como pendente: consulte estado_atual.md e preserve o template existente.
```

## 5. Quando usar cada ferramenta

| Necessidade | Principal |
| --- | --- |
| Escolher conteúdo, resolver, didática e roteiro | Chat no Projeto |
| Editar Manim, renderizar, testar, versionar | Codex na pasta do repositório |
| Pesquisa, calendário ou relatório amplo | Work |
| Revisão independente de solução/clareza | Claude ou Gemini |

Envie ao revisor somente contexto necessário: público, enunciado, hipóteses, solução e pergunta concreta. Compare pelo cálculo ou evidência, nunca por maioria de modelos.

## 6. Arquitetura de arquivos e convenções

```text
manim-fisica/
├── README.md
├── pyproject.toml
├── uv.lock
├── .gitignore
├── docs/
│   ├── guia_mestre.md
│   ├── estado_atual.md
│   ├── decisoes.md
│   ├── banco_ideias.md
│   └── plataformas_2026-09.md
├── template/
│   ├── __init__.py
│   ├── config.py
│   └── helpers.py
├── videos/
│   └── vid_0001_integracao_por_partes/
│       ├── cena.py
│       ├── ficha.md
│       ├── roteiro.md
│       ├── revisao.md
│       ├── legenda.srt
│       └── publicacao.md
├── assets/
└── renders/                 # ignorado pelo Git se pesado
```

Versione código, documentos, roteiros e legendas. Armazene MP4/WAV/projetos pesados em backup externo ou LFS somente se houver necessidade e política definida. Convenção: `vid_0001_integracao_por_partes`, não nomes ambíguos ou datas isoladas.

## 7. Ambiente local no Windows

### Estado validado

- Windows;
- Python 3.12;
- `uv` funcionando;
- Manim Community **0.21.0**;
- MiKTeX e `MathTex` funcionando;
- primeiro MP4 renderizado.

Não rode `uv init`, reinstale Python/Manim ou recrie `.venv` como rotina. Faça isso apenas para um problema diagnosticado e registre motivo, comando, versão e resultado em `estado_atual.md`.

Comandos usuais, executados na raiz do projeto:

```powershell
uv run python -m manim --version

# Preview vertical rápido
uv run python -m manim -p -r 540,960 --fps 15 videos/vid_0001_integracao_por_partes/cena.py Integral001

# Render vertical final
uv run python -m manim -p -r 1080,1920 --fps 30 videos/vid_0001_integracao_por_partes/cena.py Integral001

git status
```

Use o preview em 540×960/15 fps para iterar rápido e o render final em 1080×1920/30 fps. Evite usar `-ql`/`-qh` como atalho padrão do canal, porque esses presets podem aplicar resoluções horizontais. O comando que efetivamente funcionar deve ser registrado no estado atual.

## 8. GitHub e uso em outra máquina

Crie o repositório uma vez, conecte o remoto e use `main` para o MVP. Faça commits pequenos após uma unidade coerente: documentação inicial, template, cena, roteiro/legenda, correção. Exemplo:

```powershell
git add docs/ template/ README.md
git commit -m "docs: registrar estado inicial e guia v1.1"
git push origin main
```

Na outra máquina: clone, instale apenas o que estiver comprovadamente ausente, execute `uv sync` se `pyproject.toml`/`uv.lock` estiverem presentes e renderize uma cena curta de verificação. Atualize `estado_atual.md` com diferenças reais de máquina.

Use branch e PR quando alterar dependências, refatorar o template usado por vídeos existentes, criar automação ou colaborar com outra pessoa. Não crie branch/PR por cena simples nos primeiros dez vídeos.

## 9. README e orientações locais ao Codex

O README precisa de objetivo, estrutura, comando de preview, comando de render, como recuperar o ambiente e local do backup de mídia. `AGENTS.md`, se usado, deve ser curto: ler `docs/estado_atual.md`, preservar mudanças existentes, usar caminhos relativos, renderizar antes de declarar sucesso e nunca publicar sem autorização explícita.

## 10. Identidade visual e template Manim

A direção aprovada é científica, futurista, cósmica, elegante e limpa, com planos translúcidos deslocados e orbe central. Paleta operacional inicial: `#050816`, `#35D9FF`, `#267BFF`, `#745CFF`, `#EA63FF`, `#F5F7FF`; refinamento pelos assets e tipografia oficial ainda pendentes. Cosmos sutil, branding discreto e prioridade de legibilidade. A especificação completa e a distinção entre aprovado, implementado e pendente estão em `docs/identidade_visual.md`.

Padrão inicial: 1080×1920, 30 fps, fundo escuro, alto contraste, paleta curta, equações grandes e zona livre na parte inferior para legendas/interface. Teste sempre um frame em tamanho de celular.

No template/base scene, fixe também a área lógica vertical:

```python
from manim import config

config.frame_width = 9
config.frame_height = 16
```

A resolução em pixels continua definida pela CLI (`-r 540,960` no preview e `-r 1080,1920` no final).

O template deve separar conteúdo de apresentação. Em `template/helpers.py`, comece pequeno e reutilizável:

- `make_title(text)`;
- `make_equation(tex)`;
- `show_step(scene, current, next_step, note=None)`;
- `highlight_term(scene, mob, color)`;
- `show_result(scene, tex)`;
- `add_safe_area_guides(scene, enabled=False)`.

Para evolução algébrica, prefira `TransformMatchingTex` quando termos correspondentes devem permanecer visualmente reconhecíveis. Use `FadeOut`/`FadeIn` quando a transformação seria enganosa. Cada animação deve esclarecer uma relação, não apenas enfeitar.

### Perspectivas complementares

**Status: PLANEJADA / NÃO IMPLEMENTADA.** Como extensão didática do conceito Parallax, um conteúdo poderá mostrar o mesmo fenômeno por representações complementares, simultâneas ou sincronizadas, quando isso melhorar a compreensão. Exemplos possíveis incluem corpo em movimento com \(x(t)\); \(x(t)\), \(v(t)\) e \(a(t)\) sincronizados; círculo unitário gerando uma senoide; projétil com trajetória, vetores e gráficos; carga com vetor de campo; e mola com gráficos de posição, velocidade e aceleração.

Esse princípio expressa **ver o mesmo problema por diferentes perspectivas**. Ele não define agora layout, sistema de câmeras, helper, componente, módulo ou requisito obrigatório para todos os vídeos.

Exemplo conceitual:

```python
next_line = MathTex(r"x^2e^x - 2\int xe^x\,dx")
self.play(TransformMatchingTex(current_line, next_line))
```

Mantenha a cena do vídeo curta; a lógica repetida pertence aos helpers.

## 11. Banco de questões e ficha de produção

Para cada ideia, registre: ID, família (exercício/teoria/aplicação), pergunta, público/pré-requisito, objetivo, erro comum, solução aprovada, checagem, potencial visual, fonte quando aplicável e esforço. A ficha do vídeo deve registrar também versão do roteiro, voz, render e status do QA.

### Taxonomia editorial de longo prazo

**Status: PLANEJADA / NÃO IMPLEMENTADA.** A taxonomia futura possui quatro famílias principais:

1. **Exercícios resolvidos:** matemática e física.
2. **Visualizações dinâmicas:** funções, gráficos, campos, vetores, ondas, trajetórias e sistemas físicos ou matemáticos.
3. **Intuição:** significado visual de fórmulas, relações matemáticas, representações geométricas, fenômenos físicos e conexões entre representações.
4. **Curiosidades:** funções interessantes, caos, infinito, relatividade, paradoxos, fenômenos contraintuitivos e outras visualizações científicas adequadas ao canal.

Essa taxonomia orienta o longo prazo. Ela não substitui as famílias operacionais nem modifica a composição ou a ordem dos dez primeiros vídeos.

### Visualizações matemáticas dinâmicas

Como possibilidades editoriais posteriores ao MVP, o projeto poderá abordar funções variando com parâmetros, gráficos animados, senoides, parábolas, exponenciais, funções polares, curvas paramétricas, círculo unitário, limites, derivadas visualizadas, integrais como acumulação, vetores, séries, Fourier, fractais, sistemas dinâmicos, caos e outras construções matemáticas visualmente interessantes.

Parâmetros poderão variar continuamente para revelar seu papel. Por exemplo, \(y=a\sin(x)\), com \(a\) variando para mostrar a amplitude, e \(y=\sin(kx)\), com \(k\) variando para mostrar a frequência. São possibilidades editoriais futuras, não cenas, testes ou requisitos atuais do template.

### Física animada

A futura frente ampliada de física poderá incluir:

- **Mecânica:** leis de Newton, diagramas de corpo livre, vetores e decomposição de forças, plano inclinado, atrito, lançamento oblíquo, queda livre, movimento circular, trabalho e energia, quantidade de movimento, colisões, molas, pêndulos e movimento harmônico simples.
- **Eletrostática e eletromagnetismo:** cargas, força e campo elétrico, campo resultante, linhas de campo, potencial, superfícies equipotenciais, lei de Gauss, fluxo, campo e força magnética, partículas carregadas e indução.
- **Ondas:** amplitude, frequência, comprimento de onda, fase, interferência, superposição, ondas estacionárias e Fourier.
- **Óptica:** reflexão, refração, lentes, foco e formação de imagens.
- **Gravitação:** órbitas, força gravitacional, velocidade orbital, aceleração centrípeta e energia orbital.

Esses temas delimitam um espaço editorial futuro. Não definem cronograma, backlog, ordem de produção, vídeos aprovados ou prioridade operacional atual.

## 12. Pipeline de cada vídeo

1. Escolher uma questão/foco.
2. Resolver com hipóteses explícitas.
3. Verificar objetivamente.
4. Roteirizar fala, tela e tempo.
5. Implementar/ajustar a cena Manim.
6. Gravar ou gerar a voz aprovada.
7. Editar e inserir legendas.
8. Fazer QA visual, sonoro e matemático.
9. Publicar manualmente com metadados adaptados.
10. Registrar métricas na mesma idade de publicação.

Não automatize uma etapa somente porque ela parece repetitiva; primeiro meça tempo, retrabalho e taxa de erro.

### Modelagem antes da visualização

O Manim será usado como ferramenta de visualização, não como simulador físico automático. O fluxo conceitual é **modelo correto → verificação → representação visual**: a animação representa o modelo aprovado e não o determina. Uma animação convincente não valida a matemática ou a física.

Em matemática, a visualização não substitui demonstração, derivação, cálculo ou outra verificação adequada. Quando a frente ampliada de física for implementada, cálculos, aproximações, hipóteses e condições iniciais deverão ser definidos antes da animação. O pipeline futuro deverá incluir checagem física explícita de unidades, sinais, hipóteses, condições iniciais, leis de conservação, comportamento em limites e plausibilidade, conforme aplicável. Essa exigência metodológica está planejada; ela não acrescenta agora checklist, script, teste ou etapa ao MVP.

## 13. Piloto `integral_001`

### Missão

Publicar o primeiro Short completo para

\[
\int x^2e^x\,dx.
\]

Ele precisa mostrar integração por partes duas vezes, justificar a escolha e verificar a resposta por derivada. É um teste de ritmo, template, legibilidade, narrativa e pipeline — não apenas uma conta.

### Solução-fonte aprovada

Escolha \(u=x^2\), \(dv=e^x\,dx\). Então \(du=2x\,dx\) e \(v=e^x\):

\[
I=\int x^2e^x\,dx=x^2e^x-2\int xe^x\,dx.
\]

Na integral restante, escolha \(u=x\), \(dv=e^x\,dx\):

\[
\int xe^x\,dx=xe^x-\int e^x\,dx=xe^x-e^x.
\]

Logo,

\[
I=x^2e^x-2(xe^x-e^x)+C=e^x(x^2-2x+2)+C.
\]

Verificação:

\[
\frac{d}{dx}\left[e^x(x^2-2x+2)\right]=e^x(x^2-2x+2)+e^x(2x-2)=x^2e^x.
\]

### Storyboard mínimo de referência histórica (45–60 s)

O piloto implementado usa sete blocos de voz e aproximadamente 69 s; não reduzir sua duração para reproduzir a tabela antiga abaixo.

| Tempo | Fala/tela | Objetivo |
| --- | --- | --- |
| 0–4 s | “Como integrar \(x^2e^x\) sem decorar uma fórmula?” | Gancho honesto |
| 4–12 s | Mostre \(u=x^2\), \(dv=e^x\,dx\) | Escolha de partes |
| 12–24 s | Primeiro resultado e destaque \(\int xe^x\,dx\) | Revelar repetição |
| 24–37 s | Segunda integração por partes | Resolver a pendência |
| 37–47 s | Resultado fatorado destacado | Fechamento |
| 47–57 s | Derivada simplificando para \(x^2e^x\) | Verificação |

## 14. Voz, legendas, edição e exportação

A voz define o tempo; não estime duração somente por palavras. Narre o que o aluno precisa ver, sem ler cada símbolo inútil. Legendas devem ser revisadas contra a fala e não cobrir a equação. Guarde roteiro, SRT, áudio aprovado e export final com versão identificada. Verifique resolução vertical, fps, áudio e primeiros/últimos segundos após a exportação.

## 15. Publicação nas plataformas

Prepare um master limpo, sem marca d’água de outra plataforma. Adapte título, descrição, CTA, capa e campos ao destino. Não transforme uma orientação de interface ou regra de uma plataforma em verdade permanente: consulte `docs/plataformas_AAAA-MM.md`, datado, antes de publicar ou decidir monetização.

## 16. QA e definição de pronto

Um vídeo está pronto quando:

- solução e verificação estão corretas;
- texto e fórmulas são legíveis em celular;
- fala, animação e legendas concordam;
- não há salto no passo didático central;
- export tem orientação, duração e áudio corretos;
- fontes/licenças e metadados necessários estão registrados;
- a cópia-fonte é recuperável.

Não é necessário hash, PR, manifesto extenso ou checklist corporativo para o MVP. Registre apenas o que permite corrigir e repetir o vídeo.

## 17. Primeiros dez vídeos

Use o primeiro ciclo para testar três famílias, não para construir um curso linear.

| Nº | Família | Pauta inicial |
| --- | --- | --- |
| 1 | Exercício | \(\int x^2e^x\,dx\): integração por partes duas vezes |
| 2 | Exercício | Integral por substituição simples |
| 3 | Teoria curta | Como escolher \(u\) em integração por partes |
| 4 | Exercício | Derivada pela regra da cadeia |
| 5 | Aplicação | Derivada como velocidade instantânea |
| 6 | Exercício | Limite simples com interpretação visual |
| 7 | Exercício | Outra integração por partes, com estrutura diferente do piloto |
| 8 | Teoria curta | O que uma integral realmente acumula |
| 9 | Aplicação | De \(v(t)\) ao deslocamento usando integral |
| 10 | Exercício | Derivada ou integral aplicada a um problema curto de movimento |

Distribuição: **6 exercícios + 2 teorias curtas + 2 aplicações**. O primeiro ciclo deve parecer uma mini-temporada coerente de **Cálculo + aplicações físicas**, não uma amostra aleatória de todo o currículo. Valide enunciado, nível e solução antes de produzir. Depois do décimo, compare interesse, retenção e tempo de produção por família.

A expansão editorial de longo prazo não reclassifica, remove, substitui ou reorganiza este ciclo. Os dez vídeos e sua distribuição permanecem integralmente aprovados como estão.

## 18. Métricas e decisões semanais

Compare vídeos da mesma plataforma, com idade semelhante e duração próxima. Registre: alcance, retenção/conclusão quando disponível, salvamentos, compartilhamentos, comentários/dúvidas, seguidores atribuídos, tempo de produção e custo incremental. Dados ausentes são `ND`, nunca zero. A cada ciclo, escolha uma hipótese e um experimento; mantenha o restante estável.

## 19. Monetização e produtos futuros

O primeiro ciclo mede aprendizagem e capacidade, não renda. Separe audiência, elegibilidade de plataforma e receita efetiva. Produtos futuros possíveis: listas comentadas, mapas de estudo, revisão paga, aulas ou parcerias compatíveis. Não prometa monetização nem use requisitos de plataformas sem data e fonte atual. Obrigações fiscais/comerciais exigem orientação adequada ao caso.

## 20. Escala e automação

| Nível | Só avance quando… |
| --- | --- |
| Manual | piloto completo existe |
| Padronizado | dez vídeos são recuperáveis e comparáveis |
| Scripts locais | comandos e gargalo estão estáveis/medidos |
| Lotes pequenos | uma falha não afeta os demais |
| Integrações | benefício e custo foram justificados |

Primeiras automações úteis podem criar pasta/ficha, renderizar preview, validar arquivos obrigatórios ou inspecionar metadados do MP4. Não automatize julgamento matemático, didático ou publicação antes de haver processo confiável.

## 21. Prompts reutilizáveis

### Resolver e verificar

```text
Resolva o enunciado para o público indicado. Declare hipóteses e apresente uma checagem objetiva independente. Identifique o erro mais provável e o passo que merece visualização. Não escreva roteiro ainda.

Público: [...]
Enunciado: [...]
```

### Roteirizar a solução aprovada

```text
Converta a solução aprovada em roteiro vertical. Entregue tabela com tempo, fala, tela, animação e objetivo didático. Preserve a matemática, inclua gancho honesto, passo central e verificação. Meta: [...] segundos.
```

### Implementar no Codex

```text
Leia README.md e docs/estado_atual.md, depois o template e a pasta do vídeo. Implemente o storyboard usando Manim Community e uv. Preserve mudanças existentes, use helpers e TransformMatchingTex quando termos correspondentes devem permanecer visíveis. Renderize preview e reporte evidência e limitações reais. Não publique nada.
```

## 22. Ordem de execução

1. Criar Projeto, adicionar este guia e `START_HERE.md`.
2. Criar/atualizar `docs/estado_atual.md` com o ambiente validado.
3. Criar repositório e primeiro commit em `main`.
4. Organizar template mínimo e renderizar preview curto.
5. Produzir `vid_0001` / integral_001 completo.
6. Fazer QA e publicar o piloto.
7. Produzir os outros nove seguindo a distribuição da seção 17.
8. Medir, fazer retrospectiva e automatizar somente o gargalo real.

Visualizações dinâmicas, física animada ampliada e as demais famílias de longo prazo só entram em avaliação operacional depois desse ciclo e de uma decisão explícita de implementação.

## 23. Manutenção e recuperação

Se um erro publicado muda a explicação, corrija de forma visível: solução-fonte → cena → voz/legenda → export → plataformas. Registre a versão corrigida. Mensalmente, confirme que um vídeo pode ser reconstruído a partir do repositório e backup. Atualizações de dependência são mudanças maiores: use branch, renderize cenas representativas e só migre se houver benefício.

## 24. Itens voláteis e fontes

Crie/atualize `docs/plataformas_AAAA-MM.md` para regras de publicação, monetização, limites, elegibilidade, IA, música e disponibilidade regional. Cada afirmação operacional deve ter **data, URL oficial e impacto no canal**. O guia só define a regra: verificar antes de agir.

Referências técnicas úteis: documentação oficial do Manim Community, `uv`, MiKTeX, PyCharm e GitHub. Para plataformas, use as centrais oficiais da plataforma correspondente e registre a data de consulta. Requisitos mudam; uma fonte antiga nunca vence o estado atual.

---

**Próxima ação concreta:** consultar `docs/estado_atual.md` e `docs/identidade_visual.md`, conferir os assets e definir tipografia antes de integrar a identidade ao template. O preview com voz do piloto já existe; preservar matemática e sincronização e concluir o QA pendente.
