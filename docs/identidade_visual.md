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

Linguagem sans-serif geométrica, futurista, limpa, legível e premium, sem aparência gamer. **Nenhuma fonte específica foi oficialmente escolhida ou licenciada.**

Pendência: escolher tipografia oficial compatível com uso comercial e disponível no Windows/Manim. Definir separadamente fonte de títulos, fonte de texto/legendas e comportamento das fórmulas via LaTeX/MathTex. A aparência atual das cenas não constitui uma decisão tipográfica final.

## Assets aprovados, funções e organização

A estrutura abaixo é a organização aprovada. Na inspeção local de 2026-09-22, os oito arquivos estavam presentes nesses caminhos. Todos aparecem como untracked (`?? assets/branding/`), nenhum está staged, nenhum é retornado por `git ls-files assets/branding` e, portanto, nenhum está commitado. Aprovação visual, presença local e versionamento são estados distintos. A inspeção de existência não certifica dimensões, transparência ou qualidade de exportação.

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

O template vertical e os helpers básicos já existem. **A aplicação desta identidade ao template e ao piloto permanece pendente.** O piloto atual usa fundo `#101820` e destaques YELLOW/TEAL/GREEN; esse estado técnico não substitui a paleta aprovada nem deve ser descrito como integração de branding concluída. Esta consolidação documental não altera cenas, cores ou assets.

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

**Implementado/verificado:** oito PNGs presentes localmente na estrutura aprovada; template vertical básico e piloto com voz existentes. Assets ainda não versionados; branding ainda não integrado ao Manim.

**Pendente:** conferir exportações, transparência e dimensões; extrair/refinar cores dos assets; escolher e verificar licença das fontes; definir títulos, legendas e MathTex; definir área de proteção, tamanhos e watermark; integrar a identidade ao template preservando didática e sincronização; revisar em celular; revisar e versionar os assets em uma etapa autorizada.
