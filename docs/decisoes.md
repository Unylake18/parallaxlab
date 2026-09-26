# Decisões do Parallax Lab

Registro das decisões estáveis do projeto.

## Decisões vigentes

As decisões aprovadas serão registradas aqui conforme o projeto evoluir.

## Uso de agentes de código

Agentes de código devem operar com o menor contexto suficiente para a tarefa. Decisões matemáticas, físicas, didáticas e editoriais aprovadas no chat de Produção são tratadas como especificação de implementação, salvo inconsistência objetiva.

Render, QA, documentação e ações de Git devem ser proporcionais à etapa e ao que realmente mudou. A fonte operacional detalhada desse comportamento é `AGENTS.md`.

## 2026-09-26 — Tipografia oficial

- **Space Grotesk** é a fonte de display (headlines, títulos, capas); **Inter** é a fonte de texto (auxiliares, legendas, CTA); a matemática continua em **MathTex**.
- As fontes são versionadas no repositório com suas licenças OFL e carregadas por caminho do repo, sem instalação global.
- Aplicação a partir do `vid_0004`. Os vídeos 1–3 e suas capas permanecem como identidade pré-tipografia oficial e não serão refeitos.

## 2026-09-23 — Origem da integração por partes e escolha de u

- `vid_0003`: teoria curta — “De onde vem a fórmula da integração por partes?”.
  Mensagem: regra do produto reorganizada e integrada. Mostrar dx antes dos
  diferenciais, conversões termo a termo, travessia de v du com mudança de
  sinal e verificação com cancelamento de u'v e vu'.
- `vid_0004`: trabalhar explicitamente como escolher u em integração por
  partes. Preservar a família de exercício e a distribuição vigente;
  enunciado específico ainda não definido.
- A pauta “derivada pela regra da cadeia”, antes no vídeo 4, fica sem posição
  aprovada. Registrar essa inconsistência pendente; não inventar posição,
  exclusão definitiva, reordenação de outros vídeos ou nova distribuição.
- Preservar vídeos 1, 2 e 5–10 e a composição 6 exercícios + 2 teorias curtas
  + 2 aplicações nas partes não afetadas por essas decisões.
- Primeiro preview do vídeo 3 com coda geométrica de 7–10 s, complementar e
  removível. Retângulo U×V e curva crescente desde (0,0) até (U,V), sem equação
  específica atribuída. Regiões ∫v du e ∫u dv e síntese UV = ∫v du + ∫u dv
  referem-se às acumulações ao longo desse arco. Não é prova geral.
- Etapa autorizada: implementação, preview vertical e QA; não publicação.
  Trabalhar em main com commits pequenos; nenhum push sem autorização explícita.

## 2026-09-22 — Marca, identidade e estratégia

- Marca oficial: Parallax Lab. Instagram: @labparallax.
- Conceito: ensinar física e matemática por perspectivas que tornam os problemas mais compreensíveis.
- Símbolo aprovado: planos geométricos translúcidos e deslocados, com orbe central e sensação de paralaxe.
- Direção visual: científica, futurista, cósmica, elegante e limpa; influência psicodélica leve. Evitar estética infantil, escolar genérica ou gamer.
- Paleta operacional inicial, variantes de assets e organização aprovadas conforme `docs/identidade_visual.md`. Refinamento das cores permanece pendente; a tipografia oficial foi decidida em 2026-09-26.
- Nos vídeos: branding discreto, cosmos sutil e faixa inferior livre. Prioridade: legibilidade, compreensão, matemática/física e identidade visual.
- Primeiro ciclo: dez vídeos de Cálculo + aplicações físicas — seis exercícios, duas teorias curtas e duas aplicações. Não estruturar ainda um curso linear.
- Ampliar automação após o primeiro ciclo, com base em gargalos medidos.

## 2026-09-22 — Expansão editorial de longo prazo

**Status: PLANEJADA / NÃO IMPLEMENTADA.**

- Direção futura aprovada: visualizações matemáticas dinâmicas, frente ampliada de física animada e conteúdos de intuição e curiosidades.
- Taxonomia editorial de longo prazo: exercícios resolvidos, visualizações dinâmicas, intuição e curiosidades.
- Princípio Parallax: mostrar o mesmo problema por perspectivas complementares, simultâneas ou sincronizadas, quando isso melhorar a compreensão.
- O Manim é ferramenta de visualização, não simulador físico automático. O fluxo obrigatório é modelo correto → verificação → representação visual.
- A visualização não substitui validação matemática ou física. A futura frente de física exigirá checagem explícita de unidades, sinais, hipóteses, condições iniciais, leis de conservação, comportamento em limites e plausibilidade, conforme aplicável.
- O MVP, o piloto `vid_0001` e os dez primeiros vídeos permanecem integralmente preservados. A expansão não é pendência atual, backlog, cronograma, requisito técnico nem autorização de implementação imediata.
- A ordem estratégica permanece: primeiro piloto → dez vídeos → métricas → evolução posterior.
