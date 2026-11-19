# Contexto do projeto: "Novelinha da Física" (história da ciência em 2D)

Você vai me ajudar a criar roteiros e ideias para uma série de vídeos curtos de comédia/novelinha sobre história da ciência e física. Eu já tenho um canal de física (Parallax Lab) com vídeos didáticos em Manim; esta série é um formato alternativo, com personagens. Abaixo está tudo o que já foi construído, o que o sistema consegue fazer hoje, o que ainda não consegue, e como um roteiro precisa ser escrito para virar cena.

## 1. O que é a série
- Cientistas históricos convivem numa **sala "fora do tempo"** (parede bege, lambri de madeira, quadro-negro verde, dois retratos na parede, piso de tábuas).
- **Motor da graça:** cada personagem só conhece quem veio antes dele. Galileu não sabe quem é Newton, Newton não sabe quem é Einstein, e nenhum dos dois sabe quem é Maxwell. Os anacronismos são assumidos, mas os fatos ditos em cena precisam ser verdadeiros.
- **Tom:** novelinha cômica e leve, com física correta. Cada episódio ensina uma ideia de verdade.
- **Formato:** horizontal 1920×1080, 30 fps. Episódios de ~2 a 3 min (dá para fazer cortes verticais depois).
- **Título da série:** "Novelinha da Física" é provisório.

## 2. Elenco pronto (desenho 2D ilustrado, estilo flat com contorno)
- **Galileu Galilei (1564–1642):** calvo com brilho na cabeça, cabelo grisalho dos lados, barba cheia grisalha, olhos meio cerrados de velho sábio. Toga preta abotoada, gola branca caída, punhos brancos. Voz provisória: Piper "faber".
- **Isaac Newton (1643–1727; 1642 pelo calendário inglês):** peruca longa e cacheada até os ombros, rosto fino e nariz comprido. Casaca bordô com punhos largos, colete creme com botões dourados, jabot de renda, calção, meias brancas e sapato com fivela dourada. Voz provisória: Piper "cadu".
- **Albert Einstein (1879–1955):** cabeleira branca arrepiada, bigodão. Suéter/cardigã marrom-acinzentado, camisa branca, calça escura. Voz provisória: Piper "jeff".
- **Personagem novo** (ex.: Maxwell, Marie Curie, Faraday, Kepler, Tesla, Noether, Feynman, Aristóteles): custa só o desenho (cabeça, roupa e cores). Rig, rosto, boca, emoções e movimento já são reaproveitados. Leva poucas horas por personagem.

## 3. O que os personagens já fazem
**Rosto**
- Olhos com pálpebra de cima e de baixo, abertura do olho, tamanho da pupila e direção do olhar, com saltinhos naturais.
- Piscadas variadas: às vezes duplas, junto com a virada de cabeça, e mudando com a emoção.
- Sobrancelhas que sobem, descem, inclinam (preocupado ou bravo) e assimétricas (cético, confuso).
- A cabeça vira para os lados e para cima/baixo com efeito 2.5D.
- Rubor e cor do rosto: vermelho de raiva, verde de nojo, pálido de medo.

**Boca e fala**
- A boca é sincronizada com a voz por fonema (Rhubarb Lip Sync): fecha no M/B/P, faz bico no U/O, mostra os dentes no S/F e desliza entre as formas.
- A emoção continua por baixo da fala: dá para falar sorrindo, bravo, chorando.
- A cabeça acompanha a fala com balanço leve e acenos.

**13 emoções prontas** (cada uma muda rosto, postura, jeito de se mexer parado e efeito visual)
| Emoção | Rosto, corpo e jeito | Efeito |
|---|---|---|
| alegria | sorriso com dentes, quique leve | bochecha rosada |
| empolgado | braços para cima, pulinhos | estrelinhas |
| tristeza | sobrancelha caída, olhar baixo, ombros caídos | lágrimas, palidez |
| raiva | sobrancelhas em V, dentes cerrados, punhos, tremor | rosto vermelho, veia pulsando |
| medo | olhos enormes, pupila pequena, mãos no rosto, tremedeira | suor, palidez |
| nojo | sobrancelhas assimétricas, olhar de canto, cabeça virada, mão de "para" | rosto verde |
| ansiedade | mãos se esfregando, olhos para todo lado | piscadas rápidas, suor |
| tédio | olhos meio fechados, corpo pendendo | "zzz" |
| vergonha | olhar para baixo, sorriso sem graça, mãos juntas | rubor forte |
| fome | língua para fora, mão na barriga | baba, ronco na barriga, balão pensando numa maçã |
| surpresa | olhos arregalados, boca em "O", braços abertos | — |
| confuso | uma sobrancelha só | — |
| cético | sobrancelha torta, meio sorriso de lado | — |

Toda emoção aceita intensidade (ex.: "raiva 0.4" = irritado; "raiva 1" = furioso), e as transições são suaves.

**Gestos prontos:** apontar, dedo para cima ("eureka"), mão aberta apresentando, braços abertos, dar de ombros, coçar a cabeça ou mão na testa, mãos para o alto, mão de "para", mão na barriga, mãos juntas, mãos no rosto, punhos. Pose nova se cria com facilidade (é só uma lista de ângulos).

**Movimento:** articulações com mola (acelera, passa um pouco e assenta), antebraço e mão chegando depois do braço (efeito chicote), leve recuo antes de gestos grandes e cabelo/peruca/barba balançando atrasados. Parados, eles respiram, fazem micro-movimentos e trocam o peso entre as pernas.

**Cena:**
- Quem escuta vira para quem fala.
- A câmera aproxima suavemente de quem fala.
- Legenda com o nome do falante em dourado, sobre tarja escura.
- Cartela de nome e datas na apresentação.
- O quadro-negro mostra textos e desenhos de giz.

## 4. O que ainda NÃO existe (dá para fazer, mas é implementação nova; avise no roteiro quando precisar)
- Andar, entrar ou sair de cena andando. Hoje se resolve com corte, fade ou a câmera revelando quem já estava lá.
- Personagem sentado, de perfil ou de costas (hoje são sempre de frente, com virada de cabeça 2.5D).
- Segurar objetos (ex.: a maçã do Newton). Planejado e simples.
- Giz que se desenha traço a traço e apagador. Planejado e simples.
- Planos de câmera com corte seco: close, dupla, geral. Planejado.
- Fala em coro (dois falando juntos). Planejado.
- Cenários novos (laboratório, jardim, Lua, espaço…). Cada um é um desenho novo.
- Trilha sonora e efeitos sonoros (crunch, risada). A definir.
- Contato físico entre personagens (abraço, empurrão). Mais difícil.

## 5. Como é produzido (para você entender os custos)
- **Ferramentas:** tudo roda no meu PC. O vídeo é montado em HTML/SVG + GSAP e renderizado pelo HyperFrames (do projeto open-source OpenMontage) em ~1 min por cena. O 3D só entra se for necessário (Three.js).
- **Voz provisória:** Piper, offline e grátis, robótica, usada só para marcar ritmo e boca.
- **Voz final:** ElevenLabs, com audio tags de emoção, **somente quando a cena estiver fechada**.
- **Sincronia:** gestos, emoções, olhares, câmera e legenda ficam ancorados no início e na duração de cada fala. Trocar a voz re-sincroniza sozinho.
- **Fluxo de um episódio:** roteiro aprovado → cena com voz provisória → iteração visual → voz ElevenLabs → render final.

## 6. Como um roteiro precisa vir para virar cena
Tabela por cena, uma linha por fala, com estas colunas:
`# | Quem | Fala | Emoção (de quem fala, com intensidade) | Gesto | Reação (dos outros) | Quadro-negro / câmera (CLOSE, DUPLA, GERAL) | Tom (para a voz)`

Regras de escrita:
- Falas curtas e faladas (1 a 2 frases), no jeito de falar do Brasil, sem texto de livro.
- Uma ideia de física por episódio, explicada por conflito entre os personagens, não por aula.
- O quadro-negro ajuda a explicar: fórmulas curtas, desenhos simples.
- Toda afirmação histórica ou física precisa ser verdadeira. Lendas são tratadas como lenda (ex.: a torre de Pisa é provavelmente lenda; a maçã não caiu na cabeça do Newton). Liste no fim uma "checagem de fatos" com a fonte de cada afirmação.
- Terminar com um gancho para o próximo episódio.

## 7. Episódio 1 já roteirizado: "Quem cai primeiro?" (~2:15, 35 falas, 6 cenas)
1. **Frio:** Galileu no quadro com a pedra pesada e a leve. Newton, comendo maçã: "E não chega."
2. **Experimento de pensamento** (Duas Novas Ciências, 1638): as pedras amarradas cairiam "mais devagar e mais rápido ao mesmo tempo". Conclusão: sem o ar, tudo cai igual. Newton: "Mas você não disse por quê."
3. **A maçã:** "Caiu na sua cabeça?" — "Não! Isso é invenção." A mesma força segura a Lua; F = GMm/r² e a massa se cancela, a = GM/r².
4. **Einstein:** a câmera revela que ele estava lá. Fala da ideia de 1907, do homem que cai e não sente o próprio peso. Galileu: "Era sobre comida?" Depois, a massa curva o espaço-tempo.
5. **O tempo:** "No meu universo, o tempo é absoluto!" — "Era."
6. **Gancho:** "Nasci no ano em que você morreu" / "No calendário inglês, né?" / "…Detalhes." Depois, "Quem é Maxwell?" em coro → EP. 2.

## 8. Possibilidades para discutir
- **Próximos episódios:** Maxwell (luz é eletromagnetismo), Faraday × Maxwell (intuição × matemática), Marie Curie (radioatividade), Kepler × Galileu (órbitas e cartas), Aristóteles chegando para se defender, Noether (simetria e conservação), Feynman, Tesla × Edison (com cuidado com os mitos).
- **Formatos:** episódio de 2–3 min; cortes verticais curtos de 30–60 s com uma piada cada; "fofoca científica" (rivalidades reais, como Newton × Leibniz ou Newton × Hooke); "reagindo a mitos" (maçã, Pisa, Einstein reprovado em matemática, que é falso).
- **Integração com o canal:** um episódio da novelinha pode chamar para o vídeo didático completo do mesmo tema (ex.: queda livre, gravitação, relatividade).
- **Recursos visuais que podem virar marca:** o quadro-negro que "entra na conversa", o balão de pensamento, a cartela de datas, a fala em coro.

O que eu quero de você: discutir ideias de episódios, escrever roteiros nesse formato de tabela, sugerir piadas que nasçam da física e da história reais, apontar fatos duvidosos e dizer quando uma ideia exige recurso novo (seção 4).
