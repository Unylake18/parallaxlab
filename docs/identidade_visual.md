# Identidade visual — Parallax Lab

**Consolidada em:** 2026-09-22

**Marca oficial:** Parallax Lab

**Instagram aprovado:** @labparallax

## Posicionamento e conceito

Parallax remete à mudança aparente de posição causada por diferentes pontos de observação. A marca conecta esse fenômeno à proposta de ensinar física e matemática por perspectivas que tornam os problemas mais compreensíveis.

A identidade deve transmitir ciência, perspectiva, profundidade, curiosidade, universo/cosmos, tecnologia e inteligência. A influência psicodélica é leve e sofisticada. A direção aprovada é **premium, futurista, científica, cósmica, elegante e limpa**; não está em fase de escolha de um novo conceito.

### Perspectivas complementares

**Status: PLANEJADA / NÃO IMPLEMENTADA.** Parallax representa a possibilidade de compreender o mesmo problema por perspectivas complementares. Futuramente, essa ideia poderá aparecer didaticamente em representações simultâneas ou sincronizadas, como objeto físico com vetores e gráficos, representação geométrica com representação analítica, movimento com gráficos associados ou fenômeno físico com seu modelo matemático.

Qualquer aplicação concreta desse princípio depende de decisão posterior. Ele não define agora novo layout, transição, elemento gráfico ou regra visual obrigatória para todos os conteúdos.

## Símbolo oficial

Planos geométricos translúcidos e deslocados envolvem um orbe/esfera central. A composição comunica profundidade e paralaxe por geometria limpa, vidro e luz, com linguagem futurista e inspiração cósmica. Preservar esse símbolo nas aplicações; não redesenhar a marca para cada vídeo.

## Paleta operacional inicial

| Papel | Cor | Valor |
| --- | --- | --- |
| Fundo | Quase preto / azul-marinho muito escuro | `#050816` |
| Destaque primário | Ciano | `#35D9FF` |
| Destaque secundário | Azul elétrico | `#267BFF` |
| Destaque secundário | Violeta | `#745CFF` |
| Destaque secundário | Magenta suave | `#EA63FF` |
| Texto principal e equações | Branco | `#F5F7FF` |

A direção cromática está aprovada. Os valores hexadecimais são a paleta operacional inicial, ainda passível de refinamento por extração direta dos assets oficiais. Não registrar essa extração como realizada.

Usar ciano para o destaque principal; azul, violeta e magenta como apoios pontuais. O contraste e a leitura dos sinais matemáticos têm precedência sobre efeitos de cor.

## Diretrizes tipográficas

Linguagem sans-serif geométrica, futurista, limpa, legível e premium, sem aparência gamer.

**Tipografia oficial (implementada em 2026-09-26; aplicação a partir do `vid_0004`):**

| Papel | Fonte | Pesos iniciais |
| --- | --- | --- |
| Display: headlines, títulos, capas, linhas de série | **Space Grotesk** 2.0.0 | Medium, Bold |
| Texto: auxiliares, legendas, CTA | **Inter** 4.1 | Regular, Medium, SemiBold, Bold |
| Matemática | **MathTex** (LaTeX), sem alteração | — |

Arquivos estáticos oficiais, sem modificação, versionados em `assets/fonts/`:
Space Grotesk da release 2.0.0 de `github.com/floriankarsten/space-grotesk`
(`ttf/static/`) e Inter da release v4.1 de `github.com/rsms/inter`
(`extras/ttf/`). Ambas sob SIL Open Font License 1.1, com licença junto aos
arquivos (`OFL.txt`, `LICENSE.txt`).

Carregamento pelo repositório, sem instalação global: `template/fonts.py`
registra os arquivos no Pango ao ser importado e expõe `official_text(...)`,
que gera o texto em 4× e reduz a escala para evitar o espaçamento irregular do
Pango em corpos pequenos. Para Pillow, os caminhos estão em `SPACE_GROTESK` e
`INTER`. Teste isolado: `template/teste_tipografia.py`.

Os vídeos 1–3 e suas capas permanecem com a identidade pré-tipografia
oficial e não serão refeitos.

## Assets aprovados, funções e organização

A estrutura abaixo é a organização aprovada. Os oito arquivos estão presentes nesses caminhos, são rastreados pelo Git e já foram versionados no repositório. Aprovação visual, versionamento e aplicação no vídeo continuam sendo estados distintos; a presença do arquivo não certifica sua adequação a todo recorte ou contexto.

Caminhos relativos a `assets/branding/`:

| Arquivo | Função aprovada |
| --- | --- |
| `master/parallax_lab_logo_master.png` | Logo principal: símbolo + texto PARALLAX LAB sobre fundo cósmico escuro. |
| `master/parallax_lab_icon_profile.png` | Símbolo isolado sobre fundo cósmico para Instagram, YouTube, TikTok e avatar. |
| `master/parallax_lab_icon_transparent.png` | Símbolo isolado com fundo realmente transparente para overlays, vídeos, thumbnails e Manim. Transparência efetiva ainda deve ser conferida. |
| `master/parallax_lab_logo_monochrome.png` | Versão branca/cinza para uso institucional ou quando a versão colorida não for adequada. |
| `social/parallax_lab_banner_16x9.png` | Banner horizontal para YouTube e outras capas; conferir recortes da aplicação antes do uso. |
| `social/parallax_lab_cover_template_9x16.png` | Referência inicial para capas de Reels e Shorts. |
| `overlays/parallax_lab_watermark.png` | Marca pequena para canto dos vídeos. |
| `overlays/parallax_lab_logo_horizontal.png` | Símbolo à esquerda + PARALLAX LAB horizontalmente, para sites, cabeçalhos e overlays. |

Esses nomes e formatos indicam a aplicação pretendida; não comprovam que o asset foi publicado em qualquer plataforma.

## Fundos e atmosfera

Conteúdo didático sobre fundo muito escuro, com bastante espaço negativo. Cosmos como atmosfera extremamente sutil, sem competir com texto e equações. Os fundos cósmicos dos assets de marca não precisam ocupar o fundo de toda aula. Efeitos de vidro/luz pertencem à linguagem do símbolo e não devem prejudicar a leitura das fórmulas.

## Aplicação em vídeos e no Manim

Padrão final pretendido: vertical 1080×1920, 30 fps. Preview: 540×960, 15 fps. Área lógica: `config.frame_width = 9` e `config.frame_height = 16`.

Equações claras, resultado destacado, branding discreto e espaço inferior livre para futuras legendas/interface. O logo não deve dominar as aulas. Prioridade aprovada:

1. Legibilidade.
2. Compreensão.
3. Matemática/física.
4. Identidade visual.

O template vertical e os helpers básicos já existem. A paleta e o watermark
foram aplicados ao piloto e ao `vid_0002`; os dois finais passaram por QA
técnico em 1080×1920/30 fps. A leitura física em celular ainda não foi
comprovada. O estado atual e os caminhos finais estão em `docs/estado_atual.md`.

## Uso de logo, avatar e watermark

- **Logo:** usar a variante adequada ao contexto, preservar proporção e reservar espaço ao redor. Dimensões mínimas e área de proteção ainda precisam ser definidas; não há medidas oficiais aprovadas.
- **Avatar:** usar o ícone de perfil; validar leitura em tamanho pequeno e recorte circular antes de aplicar. Não tratar presença do arquivo como confirmação de perfil atualizado.
- **Watermark:** pequeno e discreto, sem disputar atenção com a conta, cobrir sinais ou ocupar a faixa segura inferior. Canto, tamanho e opacidade serão definidos ao integrar e testar o template.
- **Logo horizontal e monocromático:** usar conforme as funções acima, sem substituir ou redesenhar o símbolo oficial.

## Thumbnails e capas

Usar o template vertical aprovado como referência inicial para Reels e Shorts, mantendo foco claro no tema, contraste e leitura em tamanho pequeno. O banner horizontal tem aplicação própria; não assumir que um único arquivo atende a todos os recortes das plataformas. A identidade deve ser reconhecível sem que o logo ou a atmosfera cósmica dominem o conteúdo.

## O que evitar

Estética infantil, escolar genérica, gamer ou excessivamente carregada; psicodelia intensa; excesso de estrelas, brilhos, gradientes e efeitos; baixo contraste; fórmulas pequenas; logos dominantes; marcas sobre equações; escolhas tipográficas apresentadas como finais antes de seleção e licença.

## Decisões finais e pendências

**Aprovado:** nome Parallax Lab; @labparallax; conceito de perspectiva; símbolo com planos e orbe; direção visual; famílias de cor; oito variantes e suas funções; organização de pastas; branding discreto e prioridade de leitura.

**Implementado/versionado:** oito PNGs de marca rastreados na estrutura aprovada; template vertical básico, helpers e piloto com voz existentes no histórico. Capas dos vídeos 1 a 3 estão nas respectivas unidades de produção. Tipografia oficial (Space Grotesk + Inter) e licenças em `assets/fonts/`, com carregamento em `template/fonts.py`.

**Pendente:** refinar padrões de tipografia (tamanhos, entrelinhas) e área de
proteção apenas com mais evidência; validar a nova tipografia e revisar os
finais e capas em celular. A aprovação técnica dos renders não comprova publicação.
