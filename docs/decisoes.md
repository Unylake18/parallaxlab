# Decisões do Parallax Lab

Registro das decisões estáveis do projeto.

## Decisões vigentes

As decisões aprovadas serão registradas aqui conforme o projeto evoluir.

## Uso de agentes de código

Agentes de código devem operar com o menor contexto suficiente para a tarefa. Decisões matemáticas, físicas, didáticas e editoriais aprovadas no chat de Produção são tratadas como especificação de implementação, salvo inconsistência objetiva.

Render, QA, documentação e ações de Git devem ser proporcionais à etapa e ao que realmente mudou. A fonte operacional detalhada desse comportamento é `AGENTS.md`.

## 2026-10-03 — Duas trilhas: curto vertical + longo horizontal

- O Parallax Lab passa a ter duas trilhas: **curto vertical** (`curto_vertical`) e **longo horizontal** (`longo_horizontal`, YouTube long-form). Referência: `docs/formatos.md`.
- Identidade visual única e toolchain único (mesma `.venv`, `pyproject.toml`, `uv.lock`, assets e fontes).
- Longos iniciais: 16:9, frame lógico 16 × 9, preview 960×540/15 fps, final planejado 1920×1080/30 fps, alvo de 8–10 min (até ~12 quando a clareza exigir). Valores de produção interna, não regra de plataforma.
- Longos organizados por macroassunto → módulo → vídeo autossuficiente, sem numeração de aula.
- Três naturezas de longo: `teoria_visual`, `exercicio_resolvido`, `derivacao_aplicada`.
- Curtos e longos podem ser produzidos em paralelo, em worktrees e branches separados.
- Template horizontal aditivo (`template/config_horizontal.py`, `template/layout_horizontal.py`); `template/config.py` e os vídeos históricos não mudam nem são refatorados para a nova arquitetura.
- Mudanças globais (template, assets, dependências, AGENTS, docs) continuam em rodadas próprias.

## 2026-10-01 — MF-Tools

- **MF-Tools 1.4.9** (`MF-Tools[manimce]==1.4.9`) adotado como dependência utilitária **seletiva**. Presente em `pyproject.toml` e `uv.lock`; compatível com Python 3.12.4 + Manim CE 0.21.0. O fluxo de render continua `uv run python -m manim ...`.
- O Manim Community continua sendo a base. Hierarquia nas animações matemáticas:
  1. `TransformMatchingTex` — padrão, quando a correspondência é clara e didaticamente correta;
  2. `TransformByGlyphMap` — quando o controle explícito de termos dá ganho didático real (cancelamentos, reorganização algébrica, termo atravessando a igualdade, cópia deliberada, matching ruim);
  3. `FadeOut`/`FadeIn` — quando qualquer matching visual seria enganoso.
- Glyph maps só depois de estabilizar a expressão/LaTeX (são frágeis a mudanças de LaTeX).
- Os vídeos anteriores não serão refeitos só por causa da biblioteca.
- `show_indices`, `indexx_labels` e `bounding_box` são ferramentas de desenvolvimento e não entram no produto final.
- `auto_morph` não é padrão (deixou borrão no teste); preferir `auto_fade`. `Scene.keep_orientation()` não deve ser usado na versão testada.
- Ressalva conhecida: `SurroundingRectangleUnion` falha em `apply_unbuff` (`np.cross` em vetores 2D, numpy 2.5.3); `unbuff=0` contorna, mas o helper não é padrão.
- MF-Tools deve ser **considerado** nos próximos vídeos, sem obrigatoriedade de uso. Evidência e números em `docs/padroes_producao.md`.

## 2026-10-01 — Pauta do vid_0010

- `vid_0010` passa a ser o **exercício da esfera maciça em looping** (altura mínima 2,5R → 2,7R; I_CM = 2/5 ma²; K = 7/10 mv²).
- Unidade: `videos/vid_0010_looping_esfera/` (classe `LoopingEsfera010`). Série pública: **EXERCÍCIO RESOLVIDO · EP. 04**.
- A antiga pauta genérica “derivada ou integral aplicada a um problema curto de movimento” deixa de ser a pauta vigente do vídeo 10. **Não foi realocada** automaticamente para outro número; segue sem posição aprovada.
- MF-Tools já é usado seletivamente na implementação do vídeo 10 (`TransformByGlyphMap` em três passagens algébricas; ver decisão de MF-Tools acima).
- O vídeo está **em produção** (preview silencioso); o checkpoint da cena foi versionado. Sem voz, SRT, capa, final ou publicação.

## 2026-09-30 — Ordem dos vídeos 8 e 9: espira e solenoide

- O preview combinado “campo magnético do solenoide” (espira + solenoide, 174,7 s) ficou
  comprimido demais e foi **dividido em dois vídeos independentes**, nesta ordem:
  - `vid_0008` = **campo magnético no eixo de uma espira**, série pública
    **POR TRÁS DA FÓRMULA · EP. 03** (Biot-Savart + simetria + integração;
    B_z(z) = μ₀IR²/2(R²+z²)^{3/2}, checagens z = 0 e z ≫ R). Pasta
    `videos/vid_0008_campo_espira/`, classe `CampoEspira008`.
  - `vid_0009` = **campo magnético de um solenoide**, série pública
    **DA EQUAÇÃO AO FENÔMENO · EP. 03** (superposição → simetria → Ampère → B = μ₀nI).
    Pasta `videos/vid_0009_campo_solenoide/`, classe `CampoSolenoide009`. Usa o B_z(z) da
    espira, por isso vem depois do `vid_0008`.
- As pautas 8 (“teoria curta: o que uma integral realmente acumula”) e 9 (“aplicação: de
  v(t) ao deslocamento usando integral”) ficam **sem posição aprovada**; o vídeo 10 não foi
  reordenado. A classificação por família (exercício/teoria/aplicação) dos novos 8 e 9 e a
  contagem por família **não foram decididas**: pendência da Produção.
- Os nomes provisórios “008A/008B” foram descartados; a pasta `vid_0008_campo_solenoide/`
  deixou de existir (o protótipo combinado está em `vid_0009_campo_solenoide/prototipo_combinado.py`).

## 2026-09-28 — Pauta do vid_0007

- `vid_0007` = **Exercício**, série pública **EXERCÍCIO RESOLVIDO · EP. 03**: campo
  elétrico no eixo de um anel uniformemente carregado e posição onde seu módulo é máximo.
- Método aprovado: Lei de Coulomb + simetria + integração (sem Lei de Gauss); passo
  central par oposto → laterais se cancelam → axiais se somam;
  E(z) = kQz/(R² + z²)^{3/2}, máximo em z = R/√2 ≈ 0,71R.
- Headline da capa: “ONDE O CAMPO ELÉTRICO É MAIS FORTE?”.
- “Outra integração por partes, com estrutura diferente” (antiga pauta 7) fica sem
  posição aprovada; vídeos 8–10 não foram reordenados.

## 2026-09-28 — Pauta do vid_0006

- `vid_0006` = **Aplicação**, série pública **DA EQUAÇÃO AO FENÔMENO · EP. 02**:
  interferência de ondas aplicada ao cancelamento ativo de ruído em fones
  (superposição p_total = p₁ + p₂; ANC como aplicação, não aula de engenharia).
- Modelo aprovado: p₂ = A sin(ωt + φ), amplitude 2A|cos(φ/2)|; “= 0” só no caso
  ideal; na aplicação o resíduo nunca chega a zero e a tela compara amplitudes.
- Headline da capa: “O SOM PODE CANCELAR O SOM?”.
- “Limite simples com interpretação visual” (antiga pauta 6) fica sem posição
  aprovada; vídeos 7–10 não foram reordenados.

## 2026-09-27 — Texto na tela em Space Grotesk Medium

- Todo texto na tela das animações fora da matemática (manchetes, rótulos,
  notas, títulos de painel, tag da série) usa **Space Grotesk Medium**, a fonte
  da tag “POR TRÁS DA FÓRMULA”. A matemática continua em **MathTex**.
- Substitui a Inter nos textos auxiliares das animações; a Inter permanece para
  legendas e textos fora da animação.
- Aplicado a partir do `vid_0005`, por escolha do usuário; implementado em
  `screen_text` de `template/fonts.py`.

## 2026-09-27 — Pauta do vid_0005

- `vid_0005` = origem geométrica da aceleração centrípeta (a_c = v²/R), série
  pública **POR TRÁS DA FÓRMULA · EP. 02**.
- Derivação aprovada: instantes simétricos t ± Δt/2, Δv = v₊ − v₋ construído na
  origem comum, triângulos semelhantes de mesmo Δθ, |Δr|/Δt → v e depois
  |Δv|/Δt → a_c; sem aproximação de arco.
- Vídeos 6–10 não foram reordenados.
- “Como escolher u” continua sem posição aprovada.
- “Derivada pela regra da cadeia” continua sem posição aprovada.

## 2026-09-26 — Nova pauta do vid_0004

- `vid_0004` deixa de ser “como escolher u” e passa a ser **Aplicação**, série
  pública **DA EQUAÇÃO AO FENÔMENO · EP. 01**: derivada como velocidade
  instantânea, com a secante virando tangente enquanto Δt → 0.
- Modelo aprovado: x(t) = ½at², a = 2 m/s², x(0) = 0, v(0) = 0, t₀ = 2 s;
  x(2) = 4 m, v(t) = at, v(2) = 4 m/s.
- “Como escolher u” continua aprovada como pauta, sem nova posição.
- Nenhum outro vídeo foi realocado ou reordenado. A colisão temática com a
  pauta 5 e a nova contagem por família exigem decisão posterior.
- Foco da série **DA EQUAÇÃO AO FENÔMENO**: fenômeno físico e representação
  matemática sincronizados.
- Direção visual inicial da série, validada neste piloto: fenômeno físico +
  gráfico/modelo; ciano e azul como base; violeta e magenta como acentos;
  mesma marca Parallax Lab, sem identidade independente.
- Registro factual: textos de apoio e CTA do `vid_0004` usaram o `Text`
  padrão do Manim (estilo do `vid_0003`) e a capa usou Century Gothic, por
  escolha do usuário durante a produção: exceção de transição. A tipografia
  oficial abaixo é a direção vigente para os próximos vídeos.

## 2026-09-26 — Tipografia oficial

- **Space Grotesk** é a fonte de display (headlines, títulos, capas); **Inter** é a fonte de texto (auxiliares, legendas, CTA); a matemática continua em **MathTex**.
- As fontes são versionadas no repositório com suas licenças OFL e carregadas por caminho do repo, sem instalação global.
- Vigente para os próximos vídeos, salvo decisão editorial posterior. O `vid_0004` foi exceção de transição (`Text` padrão do Manim e capa em Century Gothic). Os vídeos 1–3 e suas capas permanecem como identidade pré-tipografia oficial e não serão refeitos.

## 2026-09-23 — Origem da integração por partes e escolha de u

- `vid_0003`: teoria curta — “De onde vem a fórmula da integração por partes?”.
  Mensagem: regra do produto reorganizada e integrada. Mostrar dx antes dos
  diferenciais, conversões termo a termo, travessia de v du com mudança de
  sinal e verificação com cancelamento de u'v e vu'.
- `vid_0004`: trabalhar explicitamente como escolher u em integração por
  partes. Preservar a família de exercício e a distribuição vigente;
  enunciado específico ainda não definido. *(Substituída em 2026-09-26:
  ver “Nova pauta do vid_0004”.)*
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
