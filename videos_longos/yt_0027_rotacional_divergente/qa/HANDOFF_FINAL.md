# yt_0027 · CÁLCULO III · EP. 02 · Rotacional e divergente · HANDOFF FINAL
**Ajustes visuais + voz + sincronização + legenda `.srt` + render 1080p + master + entrega** (arquivo único e autocontido)

2026-11-11. Base: preview v4 (1232,7 s ≈ 20:33, 960×540, 15 fps, sem voz). O visual do v4 **está aprovado como base**; o fechamento é a lista do §2. A narração é a do §3 (v6, a versão final: texto do GPT fundido com a da Produção). Este documento substitui os handoffs v1–v4 do yt_0027 **no que diverge**. Física, números, paleta, caneta, malha, canto, fundo e 3D seguem como estão no v4.

---

## 0. Autorização, fases e modo de execução

**Fases explicitamente abertas pelo Kaio nesta unidade:** fechamento visual (§2), **voz (ElevenLabs v4)**, **sincronização**, **legenda `.srt`**, **render final 1080p**, **master** e **entrega** em `entregas/`.

**Não abertas (não fazer):**
- publicação, capa, `commit`, `push`, `branch`, PR;
- qualquer mudança em `template/`, `assets/`, `pyproject.toml`, `uv.lock`, `AGENTS.md` ou `docs/`.

Só a unidade `videos_longos/yt_0027_rotacional_divergente/` pode ser alterada, além de `renders/` e `entregas/`, que são saída. Pode **copiar** scripts do yt_0026 para dentro da unidade, mas sem alterar o yt_0026.

**Modo de execução (importante):** não encerre a vez entre etapas. Depois de lançar um render ou a geração de voz, espere na mesma vez (comando em primeiro plano com timeout de até 10 min por lote, ou laço `until` que consulta o arquivo de saída) e siga direto para a auditoria. Mensagem de progresso não é entrega.

**Só há duas paradas permitidas:**
1. A variável `ELEVENLABS_API_KEY` não existe na sessão. Peça ao Kaio; **nunca** grave a chave em arquivo, commit, log ou relatório.
2. O WAV gerado passa de **23:30**. Reporte a duração e pare: quem decide cortes é a Produção.

Qualquer outra dúvida: escolha a leitura mais provável, diga qual e siga.

Ordem: **§2 ajustes → §4 voz → §5 sincronização → §6 conferência 540p com voz → §7 render 1080p → §8 QA e entrega → §9 relatório.** Pare só depois do relatório.

---

## 1. Estado de partida
- **Unidade:** `videos_longos/yt_0027_rotacional_divergente/`.
  - Lotes: **PHA, PB1, PB2, PB3, PB4, PB5, PB6 (Three.js), PF, PB7, PS** (`cena.py`).
  - Kit: `kit.py` e `v27.py`.
  - Âncoras: `narracao.md` → `gerar_ancoras.py` → `ancoras.json`.
- **O modelo de pipeline de voz é o yt_0026 v9**, mesmo kit e mesma família, já entregue. Em `videos_longos/yt_0026_funcoes_vetoriais_campos/`, use:
  - `alinhar_voz.py` (alinhamento forçado + STT de conferência);
  - `gerar_ancoras.py` no modo "tempo real da voz";
  - `gerar_srt.py`, `render1080.sh`, `montar_final.py`, `qa_parado.py`, `qa3d_1080.py`;
  - `conferencia_v9.md` como exemplo de relatório de tempo.

  **Copie** esses arquivos para a unidade do yt_0027 e adapte nomes, lotes e caminhos (lotes 3D do yt_0027: só `PB6`).
- **Não reabrir:**
  - física e números (Anexo A);
  - pergunta guia ("duas rodinhas passam pelas mesmas setas; por que só uma gira?");
  - ordem H → A → B1 → B2 → B3 → B4 → B5 → B6 → F → B7 → S;
  - malha no pedacinho de fluido;
  - P e Q definidos no B1-1a e o caso geral em ℝⁿ no B6-0;
  - cores, fundo milimetrado parado e canto;
  - 3D só no B6 (cubo e rodinha);
  - nada de livros na tela nem na fala.
- **A cena segue a voz:** nos longos a voz é um WAV contínuo e a cena se estica. Por isso os tempos do preview v4 **não valem mais**: o Manim e o 3D (por quadro) serão re-renderizados com a linha do tempo da voz.
- **Quadros-alvo:**
  - `referencia_v4/` (alvos 01–17) continua valendo;
  - os novos estão em `referencia_v5/`: copie para lá a pasta `yt_0027_quadros_alvo_v5/` que vem com este handoff (alvos 18–21, prancha `00_problemas_no_v4.jpg` e o `sb27.html` que gerou tudo, com as chaves `b12v5`, `b33v5`, `b44`, `prox5`).

---

## 2. Ajustes de cena (lista fechada)

Prancha dos problemas: `referencia_v5/00_problemas_no_v4.jpg`. Cada item diz a âncora, o que está errado no v4 e como fica.

1. **B1-1a: decomposição pequena.**
   - **Problema:** o triângulo P/Q da seta destacada tem cerca de metade do tamanho do alvo 14.
   - **Como fica:** a seta destacada usa o fator de comprimento `k = 0,7` do alvo (não 0,55). O tracejado e os rótulos P, Q, F e (x, y) acompanham, com placa. A clareira (`skip`) é recalculada para o triângulo maior.
2. **B1-2: a lupa precisa mostrar a derivada parcial (alvo 18).** No v4 só há o zoom (×2, ×8). Novo:
   - **(a)** O zoom ×8 fica como está, dentro de uma lupa (anel GEO).
   - **(b)** Na frase **"pega uma seta e a vizinha"**, duas setas vizinhas na horizontal acendem em `#8CFFD2` (F₁ e F₂, rótulos com placa abaixo dos pés), as outras ficam em contexto, e a cota âmbar `h` aparece entre os pés.
   - **(c)** À direita, o painel `AS DUAS NO MESMO PÉ`: as duas setas desenhadas da mesma origem, escala maior.
   - **(d)** Na frase **"essa setinha coral"**, a diferença ΔF em coral, da ponta de F₁ à ponta de F₂.
   - **(e)** Em **"dividida pela distância"**, CANETA `ΔF/h → ∂F/∂x` (com `h → 0` na seta).
   - **(f)** Embaixo, `∂F/∂x = (∂P/∂x, ∂Q/∂x)` e a legenda `DERIVADA PARCIAL`.

   Campo e ponto: (−y, 2x) perto de (0,8; 0,6), vizinhos na horizontal. A diferença é vertical, porque só o Q muda com x.
3. **B3-3: forte × fraca legível (alvo 19).**
   - **Problema:** no v4 os anéis coral são pequenos, e a comparação não se lê.
   - **Como fica:** na frase **"olha a seta logo ali fora"**, a seta em r = 1,5 sobre o eixo x positivo acende nos dois painéis com **comprimento proporcional ao módulo**: giro 1,5; vórtice 0,667; na circunferência, 1 nos dois. A seta da circunferência fica acesa junto. Anel coral em volta da seta de fora e rótulos `MAIS FORTE` / `MAIS FRACA` com placa, na hora das frases "a seta de fora é mais forte" e "ela é mais fraca". Embaixo, `NA CIRCUNFERÊNCIA: IGUAIS. LOGO FORA: DIFERENTES.` e a CANETA `F irrotacional ⇔ rot F = 0`.
4. **B4-4: faltam as setas que entram (alvo 20).**
   - **Problema:** no v4 só aparecem as setas que saem, nas paredes direita e de cima. A fala diz "pela da esquerda, entra".
   - **Como fica:** nas paredes esquerda e de baixo, setas que **entram**, desenhadas com a componente do campo naquela parede: menores, porque o campo (x, y) vale 0,5 em x₀ e 2 em x₀ + h. Elas aparecem com as frases "pela da esquerda" e "em cima e embaixo".
5. **B5-2: a conclusão por último.**
   - **Problema:** no v4, `div F = 0` é escrito na frase "a área não muda", **antes** das duas derivadas.
   - **Como fica:** na frase "a área não muda", só a legenda `ÁREA DO PEDACINHO: 0,28 → 0,28` e `MAIS LARGO E MAIS FINO`. Depois, as duas derivadas. A caixa com ENTRA/SAI. Por último, na frase **"o divergente é zero em todo ponto"**, CANETA `div F = 0` em `Ω`, na coluna, embaixo do que já está escrito.

   Isso substitui o alvo 13 só na ordem; o layout do alvo continua.
6. **B5-3: setas soltas na borda do furo.** No painel da falsa fonte saem duas setas longas da borda do furo. Use o mesmo `rmin = 0,75` do B5-1 e a mesma compressão de comprimento.
7. **B6-1: painel do B6-0 sobrando.** O painel pequeno `NO ESPAÇO (n = 3)` do B6-0 continua na coluna durante o cubo. Ele sai (FadeOut 0,4 s) na frase "o divergente tem três parcelas".
8. **B7-1 e B7-2: rótulos de nível.** Os rótulos 1, 2, 3 e 4 das curvas de nível ficam sem placa e encostam nas setas do gradiente. Corrija com:
   - placa mínima nos quatro rótulos;
   - clareira de 0,3 u em volta de cada um;
   - rótulos na diagonal de baixo à esquerda (como no alvo 07).
9. **S4: prévia do próximo vídeo e CTA (alvo 21).**
   - Na frase **"no próximo vídeo"**, tudo da terceira coisa sai, e entra a prévia:
     - título `NO PRÓXIMO VÍDEO` e subtítulo `LIMITE, CONTINUIDADE E DERIVADAS PARCIAIS`;
     - painel esquerdo: o quadradinho deformado de (x, −y) com malha e a legenda `A DEFORMAÇÃO`;
     - painel direito: a tabela `(∂P/∂x ∂P/∂y; ∂Q/∂x ∂Q/∂y)` em CANETA e a legenda `TODAS AS DERIVADAS PARCIAIS`.
   - Na frase **"se essa aula te ajudou"**, entra o **CTA padrão** do v4: logo com os dois anéis e `INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS`, até o fim da fala + 3 s.
   - Na tela, sem número de episódio.
10. **B3-5: a pergunta do rio.** Na frase **"esse rio tem giro ou não"**, entra `TEM GIRO?` (Space Grotesk 44, SAIF, placa) no alto do palco, centrado no rio, fora das setas. Ele sai na frase "espalha rodinhas presas". A tela fica parada nesse trecho só com o rio andando, o que é intencional (a pausa da pergunta).
11. **B4-6: fonte do "água:".** O `água: div v ≈ 0` sai em fonte serifada do LaTeX. Troque por `legenda('ÁGUA:')` em Space Grotesk mais `MathTex` de `\operatorname{div}\vec v \approx 0`, com o `v⃗` na cor do campo (`#2EE6A0`), como a velocidade da aula.
12. **B2-2: conferir a transição.** Na troca para `ω_AB = ∂Q/∂x` (`TransformByGlyphMap`), aparece um quadro com glifos amontoados (≈ 4:07 do v4). Tire uma tira de 6 quadros em 1080p. Se o amontoado for visível, troque o trecho do `h` por FadeOut/FadeIn (regra 3 do AGENTS) e mantenha o resto do glyph map.

13. **B3-4: tornado é modelo.** O rótulo `MODELO DE TORNADO` passa a `MODELO IDEALIZADO: VÓRTICE DE RANKINE` (mesmo estilo e posição; se não couber em uma linha, duas). A fala diz que um tornado real é mais complicado.

**Sem mudança de tela, só de tempo** (a fala ficou mais longa; a cena segura): H1, H3, A1 (o logo fica mais tempo), B1-3, B2-1, B2-6 (a rodinha completa as voltas enquanto a fala cita o barquinho do episódio anterior), B3-1, B5-1, B5-3, B6-0, B6-2, S3. Hold só com informação na tela.

**Ficha:**
- atualize `duracao_alvo` (voz real) e `Status`;
- em `3d_threejs`, confirme `cubo` (B6-1) e `roda` (B6-2/3);
- `solido_3d` continua como está;
- inclua `referencia_v5/` na lista de quadros-alvo.

---

## 3. Narração final (texto para gravação)

**Uso:**
- Copie a seção abaixo para `narracao_tags.md` da unidade, com o título exato `## Texto corrido (para gravação)` e **sem mudar uma palavra**.
- Troque o `narracao.md` da unidade pelo `yt_0027_narracao_v6_por_ancora.md` que vem com este handoff. É o mesmo texto, separado por âncora e com os `tela:` atualizados; é a fonte do `ancoras.json`.
- O texto limpo (para legenda e transcrição) é o mesmo sem os `[ ]`. Gere `narracao_limpa.md` e copie os dois para `texto/` na entrega.
- Cada parágrafo é **um trecho contínuo de voz**; não há pausas marcadas.

**Números e tags:**
- **3.843 palavras.** Estimativa a 3 palavras/s (cadência de referência do Kaio): cerca de 21,3 min de fala e 21,7 min de vídeo; a 3,1 palavras/s, 20,7 min. O tamanho foi calculado por âncora para a fala **não ser menor** que o tempo que a animação pede (tabela do Anexo C). A duração real vem do WAV. Não corte nada: acima de 23:30 é a segunda parada permitida (§0).
- **Tags** (docs/roteiro_voz_elevenlabs_v4.md):

  | Tag | Uso |
  |---|---|
  | `[thoughtful]` / `[curious]` | Base (18 e 16 parágrafos) |
  | `[thoughtful, emphatic]` | 5 conceitos |
  | `[excited]` | 3: tornado, física e o gancho final |
  | `[happy]` | Bem-vindos |
  | `[calm, satisfied]` | Resumo |

  Sem `[slowly]` e sem `[pause]`. Se uma tag for lida em voz alta, troque por uma vizinha e regere só o bloco.

**Física conferida:** Anexo A. O texto foi conferido frase a frase contra o v4 e os números da sympy (`verifica_calc3_t2_sympy.py`).

**Gatilhos:** as frases do Anexo B disparam eventos (`gat()` e `falta()`) e estão todas no texto (conferido por script). Se, na regravação, o alinhamento não achar alguma, ligue o evento à frase mais próxima de mesmo sentido e liste no relatório.

## Texto corrido (para gravação)

[curious] Olha esses dois redemoinhos. Nos dois, tudo dá voltas em torno do centro, no mesmo sentido, com a mesma cara. Agora vamos soltar uma rodinha de pás em cada um, exatamente na mesma distância do centro, e deixar a correnteza levar. Fica de olho na pá marcada.

[thoughtful] No primeiro, a rodinha dá a volta e, no caminho, vai girando em torno de si mesma: quando completa a volta, ela também completou um giro. No segundo… olha só: ela faz a mesma trajetória, no mesmo tempo, e chega do mesmo jeito que saiu. A pá marcada fica apontando para cima o tempo todo, igualzinho à cabine de uma roda-gigante.

[curious] E agora vem a parte mais estranha. Em cima dessa circunferência por onde as rodinhas passaram, os dois campos são idênticos: seta por seta, mesmo tamanho, mesma direção. As duas rodinhas foram empurradas exatamente pelas mesmas setas! Então por que uma gira e a outra não? E, afinal, o que quer dizer um campo girar num ponto? Guarda essa pergunta, porque a resposta cabe em duas derivadas… e ela não está nas setas por onde a rodinha passou.

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab. Lembra do barquinho de papel que a gente deixou no redemoinho, no episódio passado? Hoje ele ganha resposta. Hoje a aula é sobre duas medidas que um campo vetorial carrega em cada ponto: o rotacional, que mede o giro, e o divergente, que mede o espalhamento. A gente vai descobrir de onde vêm as fórmulas, o que elas medem de verdade, por que o desenho de longe engana… e onde tudo isso aparece na física. Vai ter rodinha, caixa, rio, tornado e até fio elétrico. Bora?

[thoughtful] Antes da brincadeira, vamos dar nome às peças. Um campo vetorial no plano coloca uma seta em cada ponto de uma região aberta, que a gente chama de ômega. Aberta quer dizer sem a borda: dá para chegar perto de cada ponto por todos os lados, e é isso que deixa a gente derivar. Toda seta se quebra em duas partes. A parte horizontal a gente chama de P, e a vertical, de Q. E as duas mudam de ponto para ponto: P e Q são funções de x e de y. Neste campo, P é menos y, e Q é dois x. Então, daqui para frente, quando aparecer derivada de P ou de Q, é isso: a gente está olhando como uma das partes da seta muda.

[thoughtful] Uma combinação para a aula inteira: a gente vai ler o campo como a velocidade de um fluido. A seta em cada ponto mostra a direção e a rapidez de quem passa por ali, e o escoamento é estacionário: essas velocidades não mudam com o tempo. E P e Q são lisas, de classe cê um, ou seja, com derivadas parciais contínuas. Essas hipóteses deixam a gente estudar o fluido olhando para regiões cada vez menores, e é exatamente isso que vamos fazer.

[curious] Agora pega uma lupa e chega bem pertinho de um ponto. De perto, as setas ficam quase todas iguais. Quase! Se fossem exatamente iguais, um pedacinho de fluido ali só seria carregado: sem girar, sem crescer, sem nada. Toda a graça está nas pequenas diferenças. Pega uma seta e a vizinha, a uma pequena distância, que a gente chama de agá. A diferença entre as duas é essa setinha coral. Essa diferença, dividida pela distância, quando os vizinhos ficam cada vez mais perto, tem nome: derivada parcial. É ela que vai contar toda a história de hoje.

[thoughtful] Então solta um quadradinho de fluido nesse ponto e deixa ele andar um instante. Além de ser carregado, ele pode fazer três coisas. Pode girar. Pode crescer ou encolher, mudando de área. E pode se deformar, esticando para um lado e achatando para o outro, sem mudar de área. Na prática, as três podem acontecer ao mesmo tempo. As duas primeiras ganham nome hoje: o giro é medido pelo rotacional, e a mudança de área, pelo divergente. A terceira, a deformação, tem uma pegadinha, e fica guardada para o fim da aula.

[thoughtful] Vamos começar pelo giro. E o truque é não olhar para a rodinha inteira. Pega só duas partículas de fluido vizinhas, uma ao lado da outra na horizontal, ligadas por um braço. Cada ponta do braço é carregada pela seta do campo no lugar onde ela está.

[curious] Repara só na parte vertical dessas setas. Na ponta da esquerda, bem no centro, ela nem existe; na ponta da direita, ela empurra para cima. Se a ponta da direita sobe mais rápido que a da esquerda, o braço gira no sentido anti-horário. E com que rapidez? A diferença entre as duas velocidades verticais, dividida pelo comprimento do braço. Agora encolhe o braço: essa razão vira a derivada do Q na direção x. Essa é a velocidade angular do braço horizontal. Neste campo, ela vale dois radianos por segundo.

[thoughtful] Agora um braço vertical, com uma partícula embaixo e outra em cima. Para ele, o que importa é a parte horizontal das setas, e aqui tem um detalhe de sinal. Se a ponta de cima anda para a direita mais rápido que a de baixo, o braço tomba para a direita, no sentido horário, que é o sentido negativo. Por isso a velocidade angular dele é menos a derivada do P na direção y. Neste campo, a ponta de cima vai para a esquerda: menos com menos dá mais, e o braço gira no anti-horário, a um radiano por segundo.

[curious] Só que aqui vem uma surpresa: os dois braços não precisam girar juntos. O horizontal gira a dois radianos por segundo, e o vertical, a um só: a cruz abre e fecha como uma tesoura! Então quanto o fluido gira, afinal? Uma rodinha de pás não vira tesoura: aqui ela é uma sonda ideal, bem pequena e rígida, que só mede o giro. E ela gira na média dos dois braços: dois mais um, dividido por dois, dá um radiano e meio por segundo.

[thoughtful, emphatic] E é daí que nasce o rotacional: a derivada do Q na direção x, menos a derivada do P na direção y. Repara que a fórmula não apareceu por mágica: cada termo veio do movimento de um braço de fluido. Essa diferença é o dobro da velocidade angular da rodinha ideal. No plano, o rotacional é um vetor perpendicular à folha: apontando para fora dela, o giro é anti-horário; para dentro, horário. Neste campo, ele vale três, apontando para fora, e a rodinha gira a três meios, ou seja, um radiano e meio por segundo: exatamente o que a média dos braços tinha dado. E o dobro de um e meio é três: tudo fecha.

[thoughtful] Agora a prova dos nove: o primeiro redemoinho do começo, o campo que troca as coordenadas de lugar e põe um sinal de menos na primeira. Aqui, o P é menos y, e o Q é x. Então a derivada do Q em x dá um, e a do P em y dá menos um. Um menos menos um: o rotacional vale dois, em todo ponto. A rodinha gira a um radiano por segundo, exatamente o ritmo com que ela dá a volta no centro. Por isso ela completa um giro a cada volta. E o barquinho de papel do episódio passado? Pequeno o bastante, ele também gira em torno de si mesmo, uma vez a cada volta. Na física, o rotacional da velocidade de um fluido tem nome, vorticidade, e, num corpo rígido girando, ela vale o dobro da velocidade angular. Metade do mistério está resolvida. Agora vem a metade mais estranha.

[curious] E o segundo redemoinho, aquele em que a rodinha não gira? É o mesmo campo de giro, só que dividido pelo quadrado da distância até o centro. Repara no que isso faz com os vizinhos. Pega o braço que aponta para fora: a ponta de dentro está mais perto do centro, onde tudo dá a volta mais rápido, e a ponta de fora vai ficando para trás. Então esse braço tomba no sentido horário.

[thoughtful] Já o braço que acompanha a circunferência é levado pela própria curva e gira no sentido anti-horário. E os dois giram exatamente na mesma rapidez, em sentidos opostos: esse é o segredo. Um cancela o outro. Fazendo as derivadas, as duas parcelas do rotacional dão a mesma expressão: a derivada do Q na direção x e a derivada do P na direção y são iguais. E a diferença é zero. Portanto, o rotacional é zero em todo ponto onde o campo está definido, menos na origem, que nem faz parte do domínio: ali a fórmula não existe.

[thoughtful, emphatic] Então essa é a resposta da pergunta do começo. Na circunferência, os dois campos eram iguais seta por seta, mas o rotacional não olha só a seta do ponto: ele olha como as setas mudam em volta dele. Olha a seta logo ali fora. No primeiro redemoinho, a seta de fora é mais forte; no segundo, ela é mais fraca, na medida exata para o giro desaparecer. Um campo assim, com rotacional zero em todo o domínio, se chama irrotacional. Guarda essa frase: trajetória curva não quer dizer giro. Uma partícula pode dar voltas em torno de um centro sem que o pedacinho de fluido em volta dela tenha rotação local.

[excited] E olha que bonito: cola os dois redemoinhos nessa circunferência, o primeiro por dentro e o segundo por fora. Encaixa certinho, porque ali as setas são iguais. Esse é o modelo clássico de um tornado, o vórtice de Rankine: o miolo gira como um corpo rígido, e em volta dele o ar dá voltas sem girar. Uma rodinha no miolo gira; fora dele, só passeia. É um modelo idealizado: um tornado de verdade é bem mais complicado. Mas ele guarda a lição: dar voltas em torno de um centro não é girar sobre si mesmo.

[curious] E o contrário também engana. Olha um rio: a água anda em linha reta, para a direita, mais rápida no meio e mais devagar perto das margens. Nenhuma partícula faz curva. Então, pergunta rápida, antes de eu mostrar: esse rio tem giro ou não? Pensa aí. Agora espalha rodinhas presas em eixos pelo rio inteiro.

[thoughtful] Na metade de cima, a pá de baixo de cada rodinha está mais perto do meio, onde a água corre mais, e é empurrada mais forte: a rodinha gira no sentido anti-horário. Na metade de baixo, é o contrário, e ela gira no horário. E bem no meio, onde as pás de cima e de baixo são empurradas igual, ela fica parada. A conta confirma: o rotacional é proporcional à altura, positivo em cima, zero no meio e negativo embaixo. Trajetória reta, e mesmo assim tem giro! É por isso que um galho boiando perto da margem vai girando enquanto desce o rio.

[thoughtful] Agora a segunda medida, e ela tem cara de explosão. Volta para o quadradinho de fluido, só que num campo que aponta para fora em todo lugar. Aqui o quadradinho não gira: ele cresce. Os lados vão sendo esticados, e a área aumenta.

[thoughtful] O divergente mede exatamente isso: a taxa com que a área de um pedacinho de fluido aumenta ou diminui, em relação à área que ele tem. A definição é a soma de duas derivadas: a do P na direção x, mais a do Q na direção y. E repara: o resultado é um número, não um vetor. Positivo, o pedacinho se expande; negativo, se contrai; zero, a área se conserva naquele instante. Na explosão, o divergente vale dois em todo ponto, e é por isso que o quadradinho dobra de área no tempo que a gente mostrou.

[curious] Mas de onde saiu essa soma? Ela não caiu do céu. Para enxergar, troca o quadradinho que anda por uma caixa parada, desenhada no chão. O fluido passa por ela. E a pergunta vira: a cada segundo, sai mais fluido do que entra?

[thoughtful] Começa pelas paredes da esquerda e da direita: para elas, só a parte horizontal do campo importa, o P. Pela parede da direita, o fluido sai com o valor do P daquela parede; pela da esquerda, entra com o valor do P de lá. A diferença, vezes a altura da parede, é o saldo na horizontal. E, de novo, diferença entre vizinhos dividida pela distância vira derivada: o saldo horizontal é a derivada do P na direção x, vezes a área da caixa. Em cima e embaixo, a mesma coisa com a parte vertical, o Q: derivada do Q na direção y, vezes a área. Somando e dividindo pela área, sobra… o divergente: o saldo do que sai, por unidade de área.

[curious] Vamos testar num campo de verdade. Nesse aqui, o fluido se espalha perto do centro e se comprime longe dele. Escolhe um ponto e põe uma caixa em volta. Calcula o que sai menos o que entra, dividido pela área: dá uns zero vírgula cinquenta e oito. Agora encolhe a caixa pela metade: zero vírgula setenta e um. E de novo: zero vírgula setenta e quatro. E de novo! Zero vírgula setenta e cinco. Os números vão chegando em três quartos. E três quartos é exatamente o divergente nesse ponto. O divergente é o que sobra desse saldo quando a caixa encolhe até virar o ponto.

[thoughtful] E dá para pintar o plano inteiro com esse número. Dentro de um disco, o divergente é positivo: ali cada pedacinho de fluido se expande. Fora dele, é negativo: ali cada pedacinho se contrai. Na fronteira, um círculo inteiro de divergente zero. Mas cuidado: divergente positivo não quer dizer que fluido esteja sendo criado. Ninguém está criando nem destruindo fluido: o divergente mede o quanto ele se espalha ou se aperta em cada ponto. A água, por exemplo, quase não muda de volume, então num escoamento de água o divergente da velocidade é praticamente zero. Já o ar sendo comprimido numa bomba de bicicleta tem divergente negativo. O que importa é a variação local de volume, e não para onde as setas apontam.

[curious] Só que o divergente também tem a sua pegadinha. Olha esse campo: todas as setas apontam para fora, como uma fonte. Ele é a explosão dividida pelo quadrado da distância, então as setas enfraquecem conforme se afastam. Fonte ou não? Parece óbvio… e não é.

[thoughtful] Solta um pedacinho de fluido. Conforme ele se afasta do centro, ele se alarga para os lados, porque as setas se abrem em leque… mas fica mais fino na direção de fora, porque a parte de trás está mais perto do centro, onde a velocidade é maior, e vai alcançando a da frente. E as duas coisas se compensam exatamente: a área não muda. O pedacinho muda de forma, mas não de tamanho. As derivadas dizem o mesmo: as duas parcelas do divergente têm o mesmo tamanho e sinais trocados, e se cancelam. Coloca uma caixa parada, sem incluir o furo: a gente soma o que entra e o que sai, e o saldo dá zero, porque o que entra é exatamente o que sai. O divergente é zero em todo ponto do domínio.

[thoughtful, emphatic] Então setas apontando para fora não quer dizer fonte. O divergente mede o saldo em cada pedacinho, e aqui, em cada pedacinho, o saldo é zero: as setas enfraquecem na medida exata em que se espalham. Guarda essa falsa fonte, e o furo no centro: daqui a pouco eles aparecem num lugar bem conhecido da física.

[thoughtful] E aí vem uma pergunta justa: isso tudo só vale no plano? A definição do divergente não depende da dimensão. Um campo numa região aberta de um espaço com n dimensões tem n componentes, uma para cada direção, e o divergente é a soma das derivadas de cada componente na sua própria direção. No plano, as duas componentes são o P e o Q; no espaço, chega o R. Já o rotacional é coisa do espaço: o do plano é só o caso em que o R é zero e nada depende de z.

[thoughtful] No espaço, o divergente tem três parcelas, a terceira é a derivada do R na direção z, e a caixa vira um cubo, com seis paredes. O raciocínio é o mesmo: o saldo do que sai, agora por unidade de volume. Dividimos pelo volume e deixamos o cubo encolher. E continua sendo um número.

[curious] Já o rotacional fica ainda mais interessante, porque no espaço a rodinha pode ter o eixo apontando para qualquer lado. Olha um fluido girando como um corpo rígido, em torno de um eixo inclinado. Com o eixo da rodinha alinhado com o eixo do giro, ela gira o mais rápido possível. Inclina a rodinha, e ela gira mais devagar. Deita a rodinha de lado, e ela para. Então qual é o giro desse fluido, afinal?

[thoughtful, emphatic] A resposta é uma seta: no espaço, o rotacional é um vetor de verdade. A direção dele é o eixo em que a rodinha gira mais rápido, com o sentido dado pela regra da mão direita, e o tamanho é o dobro dessa rapidez. As três componentes se organizam num determinante simbólico, com as direções x, y e z numa linha, as derivadas parciais na outra e as componentes P, Q e R do campo na última. Abrindo o determinante, a terceira componente é exatamente a do plano: derivada do Q em x, menos derivada do P em y. Por isso o rotacional também aparece escrito como um produto vetorial do nabla com o campo, e o divergente, como um produto escalar. Agora aquelas duas fórmulas do plano fazem parte de uma estrutura bem maior.

[excited] E aqui vem a parte que eu mais gosto. Lembra da falsa fonte? Ela tem exatamente o formato do campo elétrico em volta de um fio comprido, uniformemente carregado, visto de frente. É a nossa falsa fonte, multiplicada por uma constante. E o furo na origem… é o próprio fio! A lei de Gauss, na forma local, diz que o divergente do campo elétrico é a densidade de carga dividida por uma constante. Fora do fio não tem carga, e o divergente dá zero, igualzinho à nossa conta. A carga mora toda no furo: no fio idealizado, ela está concentrada onde a gente tirou o ponto do desenho.

[curious] E o vórtice? É o formato do campo magnético em volta de um fio com corrente. De novo, o nosso vórtice vezes uma constante. Em situações que não mudam com o tempo, o rotacional do campo magnético é proporcional à densidade de corrente. Fora do fio não passa corrente, e o rotacional dá zero, como a gente calculou: no modelo de um fio fino, a corrente está toda no furo. E tem mais: o divergente do campo magnético é zero sempre, em todo lugar. É o jeito matemático de dizer que ninguém nunca encontrou um polo magnético isolado.

[curious] Antes de fechar, um bônus que vale a pena conhecer desde já. Pega uma função que dá um número em cada ponto, como uma temperatura, e calcula o gradiente dela: um campo de setas apontando para onde ela cresce mais rápido. Agora tira o divergente desse campo. O resultado se chama laplaciano: o divergente do gradiente, o nabla aplicado duas vezes, uma operação feita de derivadas de segunda ordem.

[thoughtful] Por exemplo, a soma dos quadrados das coordenadas no plano. O gradiente dela é uma explosão de setas, o dobro do vetor posição. Agora calcula o divergente dessa explosão: a derivada da primeira componente dá dois, a da segunda também, e a soma dá quatro. No espaço, somando também o quadrado da altura, entra mais uma parcela igual a dois: o laplaciano passa a valer seis.

[thoughtful, emphatic] E o que esse número diz? Ele compara o valor da função num ponto com a média dos vizinhos em volta, numa vizinhança bem pequena. Laplaciano positivo: o ponto está abaixo da média ao redor. Negativo: está acima. Zero: nessa aproximação, a diferença some. E, se o laplaciano for zero numa região inteira, aí sim, cada valor é exatamente a média dos vizinhos em volta.

[curious] Agora olha uma chapa de metal com uma mancha fria no meio. No corte da chapa, a temperatura faz um vale. No fundo do vale, o ponto está abaixo da média dos vizinhos: o laplaciano é positivo, e esse ponto esquenta. O vale vai se enchendo. É assim que o laplaciano entra na equação do calor: num modelo simples, com material uniforme e sem fontes de calor, a temperatura muda na proporção dele. E ele volta nas ondas, no potencial elétrico e em boa parte da física. Mas isso fica para mais à frente.

[calm, satisfied] Então, a pergunta do começo está respondida. As duas rodinhas passavam pelas mesmas setas, mas giro não é coisa de uma seta só: é coisa de como as setas mudam em volta do ponto. O rotacional mede isso com duas derivadas, e vale o dobro da velocidade angular de uma rodinha de pás. O divergente mede, com outras duas, o saldo do que sai de uma caixinha, por unidade de área. Duas medidas locais, feitas num ponto só.

[curious] Mas repara no que sobrou. No vórtice, nenhum ponto gira. Só que, se você der uma volta em torno do furo, o campo empurra o tempo todo no mesmo sentido: essa volta não tem saldo zero. Na falsa fonte, nenhum pedacinho se expande. Só que, se você cercar o furo, tudo atravessa a cerca para fora. Longe do furo, qualquer volta e qualquer cerca dão saldo zero. Em cada ponto, nada; em volta do fio, alguma coisa.

[thoughtful] E aí está a grande pergunta: como ligar o que acontece em cada ponto com o que acontece numa região inteira? Essa ponte entre o local e o global tem nome. A volta em torno do fio é assunto do teorema de Stokes; a cerca, do teorema de Gauss; e, no plano, os dois viram um só: o teorema de Green. Eles chegam mais à frente no Cálculo três, e com hipóteses: a gente não pode atravessar um furo como se o campo existisse ali.

[curious] E a terceira coisa lá do começo, a da pegadinha? Olha este campo: o x com o menos y. Faz a conta: o rotacional dá zero, e o divergente também, em todo ponto. Nenhuma rodinha gira, nenhum pedacinho muda de área… parece que não acontece mais nada, certo? Só que olha o quadradinho: ele estica para um lado e achata para o outro. A área se conserva, mas a forma muda. Isso é a deformação, e nem o rotacional nem o divergente, sozinhos, conseguem enxergá-la. Desafio para os comentários: acha outro campo assim, que não seja constante, com rotacional zero e divergente zero.

[excited] No próximo vídeo, a gente olha de perto as peças que usamos a aula inteira: limite, continuidade e derivadas parciais. E, juntando todas as derivadas parciais de um campo numa tabela só, sai a medida dessa deformação: a gente completa o que começou hoje. Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e ativa o sininho. Até a próxima!
---

## 4. Voz (ElevenLabs v4)
Referência: `docs/roteiro_voz_elevenlabs_v4.md`.
1. Confirme `ELEVENLABS_API_KEY` na sessão (primeira parada permitida, §0).
   - Voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`.
   - Formato `mp3_44100_192`, decodificado para WAV mono 16 bits 44,1 kHz.
2. Rode primeiro com `--seco` (só mostra os blocos, sem gastar crédito):

   ```
   uv run --no-sync python videos/gerar_voz_elevenlabs.py videos_longos/yt_0027_rotacional_divergente/narracao_tags.md videos_longos/yt_0027_rotacional_divergente/audio/narracao_v1.wav --voz qw7jgPZWOKrl10GsjQ82 --secao "## Texto corrido (para gravação)" --seco
   ```

   Depois, a geração de verdade, sem `--seco`.
3. **Uma tomada completa.** Siga com ela. O Kaio ouve em paralelo; se reprovar, regera, e a §5 refaz tudo sozinha. Por isso a sincronização precisa ser **automática e reproduzível**. A tomada aprovada vira `audio/narracao_final.wav` (cópia).
4. **Checagens automáticas do WAV** (relatório `qa/voz.txt`):
   - duração;
   - picos e clipping;
   - silêncio > 1,5 s dentro de um parágrafo;
   - **tag lida em voz alta**: pela transcrição de conferência do `alinhar_voz.py --stt`, procure `curious`, `thoughtful`, `emphatic`, `excited`, `happy`, `calm`, `satisfied`;
   - "ômega", "nabla", "laplaciano", "vorticidade" e "Parallax Lab" pronunciados direito;
   - fronteiras entre blocos sem corte audível.
5. Registre no relatório: modelo, voz, versão do texto, número de blocos, duração e taxa real (palavras ÷ segundos de fala).

---

## 5. Sincronização (a cena segue a voz)
Regras permanentes dos longos:
- **WAV contínuo**;
- **nunca** cortar a voz por âncora nem inserir silêncio;
- **atraso imagem × fala ≤ 0,2 s** (LEAD 0,15 s);
- cena parada esperando a voz, só com informação na tela.

1. **Tempo por palavra:** `alinhar_voz.py` (cópia do yt_0026) → `alinhamento_palavras.json`. É alinhamento forçado do texto limpo com o WAV.
2. **`ancoras.json` gerado por script**, nunca à mão: o `gerar_ancoras.py` no modo do yt_0026 v9 (tempo real da voz). Cada âncora começa no instante da **primeira palavra do seu trecho**, conforme a tabela abaixo, e termina onde a próxima começa. O `t` de cada palavra vem do alinhamento. Assim os `gat()` caem na palavra real.
3. Rode os lotes 540p e confira no log:
   - `[gatilho-sem-frase]` = 0;
   - os `[estouro]`, listados com o motivo (a cena se esticou porque a animação é mais longa que a fala).

   Estouro maior que 1 s numa âncora: encurte a animação dentro da regra de cadência (piso 0,20 s/glifo na caneta) ou deixe a âncora seguinte começar mais tarde. **Nunca** acelere a voz.
4. **Relatório de sincronização** (`qa/sync.txt`): para cada uma das **43 âncoras** e para os gatilhos do Anexo B, o atraso entre a palavra e o evento visual (meta ≤ 0,2 s), com a lista do que passar disso.
5. **Legenda `.srt`:** `gerar_srt.py` (cópia do yt_0026). Regras:
   - até 2 linhas × 42 caracteres;
   - de 2 a 5 s por bloco;
   - "Cálculo três" falado vira "Cálculo III" na legenda;
   - tempo do WAV = tempo do vídeo.

   Longos não têm legendado embutido: o master é o único vídeo final.

| Âncora | Começa em (primeiras palavras) |
|---|---|
| H1 | "Olha esses dois redemoinhos. Nos dois" |
| H2 | "No primeiro, a rodinha dá a" |
| H3 | "E agora vem a parte mais" |
| A1 | "Fala, pessoal! Bem-vindos ao Parallax Lab" |
| B1-1a | "Antes da brincadeira, vamos dar nome" |
| B1-1 | "Uma combinação para a aula inteira" |
| B1-2 | "Agora pega uma lupa e chega" |
| B1-3 | "Então solta um quadradinho de fluido" |
| B2-1 | "Vamos começar pelo giro. E o" |
| B2-2 | "Repara só na parte vertical dessas" |
| B2-3 | "Agora um braço vertical, com uma" |
| B2-4 | "Só que aqui vem uma surpresa" |
| B2-5 | "E é daí que nasce o" |
| B2-6 | "Agora a prova dos nove: o" |
| B3-1 | "E o segundo redemoinho, aquele em" |
| B3-2 | "Já o braço que acompanha a" |
| B3-3 | "Então essa é a resposta da" |
| B3-4 | "E olha que bonito: cola os" |
| B3-5 | "E o contrário também engana. Olha" |
| B3-6 | "Na metade de cima, a pá" |
| B4-1 | "Agora a segunda medida, e ela" |
| B4-2 | "O divergente mede exatamente isso: a" |
| B4-3 | "Mas de onde saiu essa soma" |
| B4-4 | "Começa pelas paredes da esquerda e" |
| B4-5 | "Vamos testar num campo de verdade" |
| B4-6 | "E dá para pintar o plano" |
| B5-1 | "Só que o divergente também tem" |
| B5-2 | "Solta um pedacinho de fluido. Conforme" |
| B5-3 | "Então setas apontando para fora não" |
| B6-0 | "E aí vem uma pergunta justa" |
| B6-1 | "No espaço, o divergente tem três" |
| B6-2 | "Já o rotacional fica ainda mais" |
| B6-3 | "A resposta é uma seta: no" |
| F1 | "E aqui vem a parte que" |
| F2 | "E o vórtice? É o formato" |
| B7-1 | "Antes de fechar, um bônus que" |
| B7-2 | "Por exemplo, a soma dos quadrados" |
| B7-3 | "E o que esse número diz" |
| B7-4 | "Agora olha uma chapa de metal" |
| S1 | "Então, a pergunta do começo está" |
| S2 | "Mas repara no que sobrou. No" |
| S3 | "E aí está a grande pergunta" |
| S4 | "E a terceira coisa lá do" |
---

## 6. Conferência 540p com voz (antes do 1080p)
Render de **todos os lotes** em 540p/15 fps com os tempos da voz, preview com voz (`montar_preview.py` com o WAV). Rode todos os portões e feche o que falhar antes do 1080p:
- `FLASH` = 0 (caneta: nada visível antes da vez);
- **R5 sobreposição** = 0 (`QA_SOBREPOS=1`, `qa_sobrepos_rel.py`);
- **R6 a cada 0,2 s, incluindo transições e duplicatas**. As únicas exceções aceitas são as duplicatas intencionais `0,219` / `0,927` do B5-2;
- quadros vazios ≤ 0,6 s;
- `qa_parado.py`: tela congelada > 2 s **só** onde há informação na tela e a fala segue (liste);
- `[gatilho-sem-frase]` = 0;
- `qa_canto.py` e `qa_fundo.py`;
- `qa3d.py`: alinhamento 3D × Manim ≤ 2 px;
- **SYNC** (atraso ≤ 0,2 s);
- **VOZ** (sem borda abrupta, sem silêncio inserido).

**Lado a lado** (`comparar.py`, `RODADA=v5`): os alvos 18–21 contra o render, mais os alvos 14–17 e 11 para confirmar que nada regrediu. Monte também uma **prancha com um quadro de cada âncora no instante da primeira palavra** (43 quadros), para ver se a imagem certa está na tela quando a fala começa.

---

## 7. Render final 1080p
1. **3D (PB6) por quadro** em 1920×1080 a 30 fps, com os pedidos gerados na linha do tempo da voz (`render1080.sh`, como no yt_0026). Meça de novo o alinhamento 3D × Manim (`qa3d_1080.py`) e informe o erro máximo em px.
2. **Manim em 1080p30** pelo fluxo normal (`uv run python -m manim ...`) com `template/config_horizontal.py`. **Não configure CRF:** o `template/qualidade.py` já troca para **14** nos renders ≥ 1080p. Não use a variável `CRF` e não recodifique.
3. **Emenda:** `montar_final.py` (remux, sem reencodar), na ordem PHA, PB1, PB2, PB3, PB4, PB5, PB6, PF, PB7, PS.
4. **Master:**

   ```
   uv run python videos/montar_master.py <sem_audio_1080p30.mp4> audio/narracao_final.wav renders/yt_0027_master_final_1080p30.mp4
   ```

   A voz é colada **sem recompressão do vídeo**. Confira:
   - 1920×1080, 30 fps;
   - duração do master = WAV (+ os 3 s finais do CTA, se a montagem os mantiver, como no yt_0026);
   - `crf=14.0`, com o comando do AGENTS: `uv run python -c "import av,re;c=av.open('ARQ.mp4');d=b''.join(bytes(p) for _,p in zip(range(4),c.demux(c.streams.video[0])));print(re.search(rb'crf=([0-9.]+)',d).group(1))"`.
5. Se o disco apertar, apague só PNGs e renders 540p **desta** unidade que já foram auditados. Nada de limpeza ampla.

---

## 8. QA final e entrega
- **QA completo no vídeo final** (obrigatório no fechamento):
  - os portões do §6 sobre o 1080p (amostragem por lote, R6 incluído);
  - A/V: voz contínua, sem clipping, sem corte;
  - `.srt` aberto e conferido em 5 pontos: início, meio, fim, uma frase longa e uma de equação;
  - `crf=14.0`;
  - capítulos novos (`renders/capitulos_final.txt`), recalculados com os tempos da voz, nos mesmos 10 títulos do v4.
- **Entrega:** `uv run python videos/entregar.py yt_0027` (cópia; não move nem apaga). Pasta única em `entregas/` com:
  - `master`;
  - `legenda` (`.srt`);
  - `audio/` (WAV final);
  - `texto/` (ficha, `narracao_tags.md`, `narracao_limpa.md`, este handoff, capítulos);
  - `manifesto`.

  O número `0027` vai no fim de cada nome. Sem capa. Série, EP e assunto vêm da `ficha.md` (`CÁLCULO III · EP. 02`, `# Rotacional e divergente`).
- Não rode `entregar.py` com uma versão que reprove um portão do §6. Se algum portão ficar aberto, pare e reporte qual e por quê; a entrega assim mesmo só acontece se o Kaio autorizar.

---

## 9. Relatório de entrega (obrigatório, e depois pare)
1. Arquivos alterados e criados: código, `narracao.md`, `narracao_tags.md`, `narracao_limpa.md`, `ancoras.json`, `.srt`, ficha.
2. Os 13 itens do §2, cada um com o caminho do quadro ou da tira que prova.
3. Verificações e resultados: todos os portões do §6 com números reais, a sincronização das 43 âncoras e o QA de voz.
4. Caminhos: WAV, preview 540p com voz, master 1080p, `.srt`, capítulos e a pasta em `entregas/`.
5. **Relatório 3D:** cenas Three.js, o que foi portado de cada ficha, resolução, custo por quadro, alinhamento em px e o que faltou.
6. Duração final e taxa real da voz (palavras ÷ segundos), comparadas com a estimativa de 3 palavras/s.
7. Pendências reais (estouros de âncora, exceções de portão).

Depois do relatório: **pare**. Sem publicação, capa, commit ou push.

---

## Anexo A · Números congelados (tela e fala)

| Cena | Valores |
|---|---|
| B1-1a | F = (−y, 2x); P = −y, Q = 2x; Ω ⊂ ℝ² aberto, P e Q com derivadas parciais contínuas em Ω |
| B1-2 | Lupa ×8 em (0,8; 0,6); vizinhos na horizontal; ΔF vertical (∂P/∂x = 0, ∂Q/∂x = 2) |
| B2 (campo (−y, 2x)) | ω_AB = ∂Q/∂x = 2 rad/s; ω_AC = −∂P/∂y = −(−1) = 1 rad/s; rodinha = média = 3/2 rad/s; rot F = (2 − (−1)) k = 3 k = 2ω k |
| B2-6 (giro (−y, x)) | ∂Q/∂x = 1, ∂P/∂y = −1, rot F = 2 k em todo ponto, ω = 1 rad/s (um giro por volta); vorticidade = 2ω |
| B3 (vórtice (−y, x)/(x² + y²)) | ∂Q/∂x = ∂P/∂y = (y² − x²)/(x² + y²)²; rot F = 0 em ℝ² − {(0, 0)}; em r = 1 as setas do giro e do vórtice são iguais (módulo 1); em r = 1,5: giro 1,5, vórtice 0,667 |
| B3-4 (tornado) | Giro rígido em r < 1, vórtice em r ≥ 1, colados em r = 1 |
| B3-5/6 (rio) | F = (1 − y²/9, 0) em \|y\| < 3; rot F = (2y/9) k: positivo em cima, zero em y = 0, negativo embaixo |
| B4-1/2 (explosão) | F = (x, y); div F = 1 + 1 = 2; ÁREA 0,49 → 0,99 |
| B4-4 (caixa) | [0,5; 2]²; P(x₀) = 0,5, P(x₀ + h) = 2 (idem Q); [P(x₀ + h) − P(x₀)] k ≈ (∂P/∂x) hk |
| B4-5 (campo-teste) | F = (x − x³/3, y − y³/3); div F = 2 − x² − y²; caixa centrada em (1, ½): 0,583 → 0,708 → 0,740 → 0,747 → div(1, ½) = 0,750 |
| B4-6 (mapa) | div > 0 em r < √2, div = 0 em r = √2, div < 0 fora |
| B5 (falsa fonte (x, y)/(x² + y²)) | Setor: área 0,28 → 0,28; ∂P/∂x = (y² − x²)/(x² + y²)², ∂Q/∂y = (x² − y²)/(x² + y²)²; caixa [1, 2] × [−½, ½]: ENTRA 0,927, SAI 0,490 + 0,219 + 0,219 = 0,927; div F = 0 em Ω |
| B6 | div F = ∂P/∂x + ∂Q/∂y + ∂R/∂z; rot F = (∂R/∂y − ∂Q/∂z, ∂P/∂z − ∂R/∂x, ∂Q/∂x − ∂P/∂y); \|rot\| = 2ω no eixo do giro |
| F | E = λ/(2πε₀) · (x, y)/(x² + y²); ∇·E = ρ/ε₀; ∇×B = μ₀J; ∇·B = 0 |
| B7 | φ = x² + y²: ∇φ = (2x, 2y), ∇²φ = 4; no espaço, 6; ponto (1, ½): valor 1,25, média na circunferência pequena 1,41 (laplaciano > 0 → abaixo da média) |
| S4 | F = (x, −y): rot F = 0, div F = 0; o quadradinho estica em x e achata em y (área constante) |

## Anexo B · Frases-gatilho (precisam estar no texto falado)
Conferidas por script contra o §3: todas presentes. **NOVO** = gatilho que este handoff cria (§2).

| Âncora | Frases que precisam continuar no texto (disparam eventos) |
|---|---|
| H1 | tudo dá voltas em torno do centro · soltar uma rodinha |
| H2 | no primeiro · ela também completou um giro · no segundo |
| H3 | os dois campos são idênticos · então por que uma gira |
| A1 | hoje a aula · duas medidas · o rotacional, que mede o giro · o divergente, que mede o espalhamento · a gente vai descobrir · bora |
| B1-1a | nome às peças · região aberta · duas partes · a parte horizontal · e a vertical, de Q · funções de x e de y · neste campo |
| B1-1 | a gente vai ler o campo como a velocidade |
| B1-2 | pega uma lupa · toda a graça está nas pequenas diferenças · **pega uma seta e a vizinha** (NOVO) · **essa setinha coral** (NOVO) · dividida pela distância |
| B2-1 | pega só duas partículas · ligadas por um braço · cada ponta do braço é carregada |
| B2-2 | repara só na parte vertical · se a ponta da direita sobe · e com que rapidez · essa razão vira a derivada · essa é a velocidade angular |
| B2-3 | agora um braço vertical · o que importa é a parte horizontal · se a ponta de cima anda para a direita · por isso a velocidade angular dele · neste campo, a ponta de cima vai para a esquerda · menos com menos dá mais |
| B2-4 | o horizontal gira a dois · e o vertical, a um só · a cruz abre e fecha · uma rodinha de pás não vira tesoura · na média dos dois braços |
| B2-5 | é daí que nasce o rotacional · um vetor perpendicular à folha · neste campo, ele vale três · a rodinha gira a três meios |
| B2-6 | por isso ela completa um giro · vorticidade |
| B3-1 | o mesmo campo de giro · repara no que isso faz com os vizinhos · pega o braço que aponta para fora · então esse braço tomba |
| B3-2 | gira no sentido anti-horário · e os dois giram exatamente na mesma rapidez · fazendo as derivadas · e a diferença é zero · menos na origem |
| B3-3 | na circunferência, os dois campos · **olha a seta logo ali fora** (NOVO) · a seta de fora é mais forte · ela é mais fraca · se chama irrotacional |
| B3-4 | cola os dois redemoinhos · encaixa certinho · o modelo clássico de um tornado · uma rodinha no miolo gira |
| B3-5 | olha um rio · mais rápida no meio · **esse rio tem giro ou não** (NOVO) · espalha rodinhas presas |
| B3-6 | e ela gira no horário · a conta confirma |
| B4-1 | aqui o quadradinho não gira · ele cresce |
| B4-2 | o divergente mede exatamente isso · o resultado é um número · na explosão, o divergente vale dois |
| B4-3 | uma caixa parada · sai mais fluido do que entra |
| B4-4 | pela parede da direita · pela da esquerda · a diferença, vezes a altura · em cima e embaixo · somando e dividindo pela área |
| B4-5 | vamos testar num campo de verdade · três quartos é exatamente o divergente |
| B4-6 | pintar o plano inteiro · dentro de um disco · fora dele, é negativo · um círculo inteiro de divergente zero · ninguém está criando nem destruindo · a água, por exemplo · bomba de bicicleta |
| B5-1 | é a explosão dividida |
| B5-2 | solta um pedacinho de fluido · a área não muda · as derivadas dizem o mesmo · coloca uma caixa parada · o que entra · é exatamente o que sai · o divergente é zero em todo ponto |
| B5-3 | não quer dizer fonte |
| B6-0 | região aberta de · soma das derivadas · no plano, as duas componentes · no espaço, chega o R · já o rotacional |
| B6-1 | o divergente tem três parcelas · com seis paredes · agora por unidade de volume · continua sendo um número |
| B6-2 | já o rotacional · com o eixo da rodinha alinhado · inclina a rodinha · deita a rodinha de lado |
| B6-3 | o rotacional é um vetor de verdade · o tamanho é o dobro dessa rapidez · se organizam num determinante simbólico · abrindo o determinante · a do plano · um produto vetorial do nabla com o campo · como um produto escalar |
| F1 | o formato do campo elétrico · é a nossa falsa fonte · a lei de Gauss na forma local · fora do fio não tem carga · a carga mora toda no furo |
| F2 | o formato do campo magnético · de novo, o nosso vórtice · o rotacional do campo magnético é proporcional · fora do fio não passa corrente · o divergente do campo magnético é zero sempre |
| B7-1 | uma função que dá um número em cada ponto · calcula o gradiente dela · o resultado se chama laplaciano |
| B7-3 | ele compara o valor da função num ponto · com a média dos vizinhos · laplaciano positivo |
| B7-4 | abaixo da média dos vizinhos · o laplaciano é positivo · esquenta · vai se enchendo · equação do calor · e ele volta nas ondas |
| S1 | o rotacional mede isso com duas derivadas · o divergente mede, com outras duas |
| S2 | se você der uma volta em torno do furo · se você cercar o furo · longe do furo, qualquer volta · em cada ponto, nada · em volta do fio, alguma coisa |
| S4 | o x com o menos y · o rotacional dá zero · o divergente também · nenhuma rodinha gira · nenhum pedacinho muda de área · estica · isso é a deformação · desafio para os comentários · no próximo vídeo · **se essa aula te ajudou** (NOVO) |

## Anexo C · Tempo por âncora (v4 contra a fala a 3 palavras/s)
(A) = a animação manda, e a fala não pode ser menor que a tela. Quem decide a duração final é o WAV.

| Âncora | Tela no v4 (s) | Palavras | Fala a 3 pal/s (s) |
|---|---|---|---|
| H1 | 13 | 47 | 16 |
| H2 | 22 | 62 | 21 |
| H3 | 21 | 78 | 26 |
| A1 | 29 | 93 | 32 |
| B1-1a | 48 | 128 | 43 |
| B1-1 (A) | 25 | 83 | 28 |
| B1-2 | 26 | 97 | 33 |
| B1-3 | 30 | 92 | 31 |
| B2-1 | 16 | 47 | 16 |
| B2-2 | 25 | 90 | 30 |
| B2-3 | 35 | 101 | 34 |
| B2-4 | 26 | 84 | 28 |
| B2-5 (A) | 38 | 116 | 39 |
| B2-6 | 47 | 153 | 52 |
| B3-1 | 25 | 74 | 25 |
| B3-2 (A) | 32 | 98 | 33 |
| B3-3 (A) | 34 | 111 | 38 |
| B3-4 (A) | 31 | 95 | 32 |
| B3-5 | 15 | 55 | 19 |
| B3-6 | 39 | 104 | 35 |
| B4-1 | 15 | 43 | 15 |
| B4-2 (A) | 31 | 97 | 33 |
| B4-3 | 15 | 43 | 15 |
| B4-4 (A) | 41 | 122 | 41 |
| B4-5 (A) | 33 | 106 | 36 |
| B4-6 (A) | 42 | 123 | 42 |
| B5-1 | 15 | 45 | 16 |
| B5-2 (A) | 43 | 134 | 45 |
| B5-3 | 14 | 56 | 19 |
| B6-0 | 32 | 94 | 32 |
| B6-1 | 18 | 54 | 18 |
| B6-2 | 25 | 75 | 26 |
| B6-3 (A) | 45 | 135 | 46 |
| F1 | 38 | 108 | 36 |
| F2 | 33 | 98 | 33 |
| B7-1 | 23 | 69 | 24 |
| B7-2 (A) | 18 | 66 | 22 |
| B7-3 (A) | 17 | 65 | 22 |
| B7-4 | 29 | 94 | 32 |
| S1 | 29 | 78 | 26 |
| S2 | 29 | 77 | 26 |
| S3 | 26 | 85 | 29 |
| S4 (A) | 45 | 168 | 56 |