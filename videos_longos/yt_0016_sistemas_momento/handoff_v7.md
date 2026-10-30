# yt_0016 — avaliação do preview v6 e HANDOFF v7 (rodada visual: 3D moderno)

Base: zip `v6_para_gpt 2.zip` (preview 960×540/15 fps, 22:46,8; voz com pausas, 3,01 palavras/s). Revisei o vídeo inteiro por folhas de
contato, com um quadro a cada 3 s e a fala embaixo.
Pedido do Kaio: "algumas animações bem porcas, tipo a do disco… seguir um padrão moderno de 3D Three.js; 2D só se for realmente
melhor, e aí tem que caprichar; 2,5D também".

---

## Parte 1 — Avaliação do v6

### 1.0 Veredito
O áudio e a sincronia estão fechados: a voz respira, os eventos acontecem na frase em que são ditos e os resultados entram no número
falado. **Esta rodada não mexe na voz nem nos tempos.**
O que falta agora é aparência. Metade do vídeo é 3D de verdade (cavalo, esferas, manequim, vela). A outra metade é 2D chapado, com
formas cinzentas num fundo quase preto:
- o disco do T7-8, um círculo cinza com uma barra branca, visto de cima, num quadrado azul;
- a bola e a "Terra" do T9 (uma cúpula cinza);
- os blocos e as molas do T9/T10;
- o rifle do E8 (cinza, em dois postes);
- o Cyrano;
- os discos do A3/A4.
Ao lado do cavalo e da vela, essas cenas parecem de outro vídeo. Somam-se a isso dois problemas globais: o chão 3D termina numa
aresta no meio do quadro (o degradê do v6 ainda deixa uma faixa escura vertical) e o fundo #050816 está preto demais. No yt_0017 o
Kaio já aprovou o fundo espacial azul (§1.3).

### 1.1 Resíduos de acabamento do v6
| Tempo v6 | Âncora | Problema |
|---|---|---|
| 0:50–0:52 | A3 | Ainda sobra um glifo solto voando perto de `dp⃗/dt` (resto do morph antigo) |
| 1:32–1:34 | A5 | Na entrada, `UM CORPO: TODA FORÇA CONTA` encosta em `→ SISTEMA: INTERNAS × EXTERNAS` (as letras se cobrem por ~1 s) |
| 10:47–10:49 | T9-5→T9-6 | As linhas ATRITO NO LEVE, RESULTANTE e ATRITO NO PESADO se cobrem na troca |
| 13:05–13:07 | T10-4 | A DICA entra por cima de `QUANTO MAIOR A DIFERENÇA… / GUARDA PARA O CAÇADOR` antes de esse texto sair |
| 17:06–17:56 | E8-2/3/4 | `EM RELAÇÃO AO CANO · 601 m/s` encosta em `v_bala,chão = …` (os dois quase se tocam) |
| 22:39–22:46 | EN2 | Um pedaço da granada fica parado na borda de cima, acima da pergunta |

### 1.2 O plano cena por cena
Legenda:
- **3D** = Three.js na pipeline da unidade (`threejs/cena3d/*.js` + `r3d.js`), com rótulos e setas no Manim presos por `pontos.json`.
- **2,5D** = Manim com profundidade: sombra, brilho, camadas em paralaxe, gradientes e objetos com volume.
- **2D+** = continua 2D, mas caprichado.

| Cena | Hoje | v7 | Prioridade |
|---|---|---|---|
| **T7-8 disco com binário** | Círculo cinza com barra branca, visto de cima num quadrado azul | **3D.** Disco de aço escovado (tipo hóquei, com borda chanfrada e uma faixa magenta na lateral para ler a rotação) sobre uma pista de gelo, câmera 3/4 baixa. Duas setas de força, iguais e opostas, nas bordas. O disco gira com 3–4 "fantasmas" estroboscópicos esmaecendo. No centro, um ponto magenta fixo e uma cruz gravada no gelo, que mostram que o centro não sai do lugar. A câmera orbita devagar ~15° enquanto a CONTA monta | A |
| **T9-3 a T9-7, T10 blocos e mola** | Quadrados cinza, mola em zigue-zague, palco nos 45% de cima | **3D.** Blocos de 1 kg e 2 kg com volume (aço claro e grafite, cantos arredondados), mola 3D helicoidal comprimida, chão de concreto com textura no T9 (com atrito; poeira fina saindo de baixo dos blocos enquanto deslizam) e gelo polido com reflexo no T10 (sem atrito), com batentes de aço. **Câmera lateral** (as setas de momento são comparadas por comprimento), um pouco elevada (~12°), para dar volume sem distorcer. O gráfico P(t) continua no Manim (2D+): linha com brilho, área sob a curva com degradê e ponto do mínimo pulsando | A |
| **E8 rifle** | Silhueta cinza em dois postes | **3D.** Rifle low-poly (coronha de madeira escura, cano metálico) num **apoio frouxo** (bipé com articulação solta). O rifle desliza para trás de verdade, a bala é um traço metálico, e os gases são uma nuvem de partículas (cinza-azulada, com expansão e dissipação; nunca cobrem rótulo). Câmera lateral | A |
| **T8-7 Cyrano** | Bonequinho 2D cinza, ímã em "U" e lua crescente plana | **3D.** O manequim do E6/E7 sentado numa placa de ferro, com um ímã em ferradura (vermelho/prata) na mão. Céu com a Lua 3D (esfera com relevo, terminador suave) ao fundo, e o lançamento do ímã com arco. A seta do peso do conjunto fica no Manim. Tom de humor: a câmera sobe até a Lua no "chegar à Lua" e desce no "Pena que não funciona" | A |
| **T9-1/T9-2 bola e Terra** | Bola 2D caindo numa cúpula cinza | **3D.** A bola de 1 kg cai de uma plataforma (10 m, com cota no Manim) sobre um chão com grade. No "Agora aumenta o sistema: bola mais Terra", **a câmera faz um dolly-out** até o planeta (Terra estilizada: oceanos azul-escuros, continentes dessaturados, atmosfera fina), e a fronteira cresce junto até englobar a Terra. O replay com p⃗ e −p⃗ vem nessa vista, com a seta da Terra minúscula | A |
| **Global: fundo e chão** | #050816 quase preto; chão 3D cortado no meio do quadro | **Fundo espacial do yt_0017** em todo o vídeo (§1.3). O 3D renderiza a **largura toda**: o chão vai até a borda direita e some no fundo por névoa (fog), e a coluna da CONTA fica sobre a parte escura do mesmo céu. Nada de painel 3D recortado | A |
| **A3/A4 discos do vídeo anterior** | Círculos cinza num trilho pontilhado | **3D.** Os discos de aço do yt_0015 (mesma geometria, se existir na unidade do yt_0015; senão, o disco do T7-8) sobre uma mesa de ar/gelo, câmera lateral baixa. O gráfico F(t) fica no Manim (2D+), com área de J⃗ em degradê | B |
| **T7-9 parábola + cargas** | Bola 2D sobre linha tracejada | **3D.** Bola lançada sobre o chão com grade e rastro estroboscópico (7–9 cópias esmaecendo). As setas pₓ (constante) e p_y (mudando) ficam no Manim pela bola. Para as duas cargas e o campo: 2,5D, duas esferas brilhantes (cores de carga do canal) e linhas de campo animadas com brilho, em vez da "nuvem" de elipses | B |
| **C-1 placas e luz** | Dois painéis azuis com placas suspensas | **3D.** Duas placas penduradas por fios finos dentro de uma campânula de vácuo de vidro. Um laser em LUZ (#FFD25A, feixe com brilho volumétrico) bate **de frente**. A placa preta esquenta (brilho laranja); o espelho reflete o feixe de volta. As placas se deslocam (pêndulo) sem girar. A câmera vai de 3/4 para frontal no "Olha as duas placas". Setas F⃗ e 2F⃗ no Manim | B |
| **A6 mapa** | Ícones 2D pequenos | **2,5D.** Miniaturas dos objetos 3D reais (o disco e as três esferas), renderizadas como sprites com sombra. O disco vira as esferas no "vira uma ferramenta" | C |
| **E9 corpúsculos** | Diagramas 2D (espelho e água) limpos, mas pobres | **2D+, porque aqui o 2D é melhor:** ângulos, normal e decomposição pedem geometria plana e exata. Água com degradê, linha de superfície com brilho e cáustica suave; espelho metálico com reflexo em degradê; corpúsculos LUZ com brilho e rastro curto; setas de decomposição em caixas próprias, afastadas do raio. Cartão do Newton: trocar a silhueta borrada por um retrato estilizado em gravura (linha fina, tom sépia frio), sem nome de livro | C |
| **Barras (T10, E6, E7)** | Retângulos chapados | **2D+.** Barras com cantos arredondados, degradê vertical, brilho no topo, valor que conta de 0 até o número (contador) e eixo fino | C |
| **EN2 granada** | Ponto e arco 2D | **2,5D**, ou reaproveitar a explosão 3D do yt_0017, se já existir no repositório (só a geometria; nada de Blender). Pedaços com rastro e o CM em degradê ciano→magenta, como no v6. Corrigir o pedaço parado (1.1) | C |
| Cavalo, esferas do T7, manequim, vela | 3D bons | Só herdam o fundo e o chão novos (§1.3). Não remodelar | — |

### 1.3 Padrão visual moderno (vale para todas as cenas 3D)
- **Fundo:** o mesmo do yt_0017, num `fundo_lab.png` único na unidade e no clear do Three.js:
  - gradiente azul-noite #0B1A3A → #08122B → #0A1030;
  - estrelas estáticas fracas, mais rarefeitas atrás da coluna da CONTA;
  - brilho magenta baixo no horizonte.
- **Chão:** só onde há chão e gravidade, com grade ciano fina que esmaece com a distância e fog para o fundo. Gelo e concreto são
  materiais sobre esse chão, nunca um "tapete" retangular solto.
- **Luz:** key light quente suave, rim light ciano fria nos contornos, sombras de contato macias e environment map simples para os
  metais. Nada de luz chapada.
- **Materiais:** PBR, com metalness e roughness coerentes (aço escovado, grafite, madeira escura, vidro).
- **Câmera:**
  - movimento sempre com easing;
  - **câmera lateral** quando a tela compara comprimentos de setas (T9, T10, E7-2, E8);
  - 3/4 quando o objetivo é volume (disco, Cyrano, placas);
  - deriva lenta ("palco vivo"): órbita ≤ 2°/s ou dolly ≤ 3%/s enquanto a CONTA monta. Esta é a resposta ao "palco congelado" que o
    Claude Code deixou para decidir: **aprovado**.
- **Movimento:** estroboscópio (fantasmas esmaecendo) nos voos e giros; partículas só onde há física (poeira de atrito, gases).
  Motion blur leve só em objetos rápidos (bala, disco girando).
- **Rótulos e setas:** continuam no Manim, presos por `pontos.json`, com as regras de sempre:
  - nada escrito sobre corpo 3D;
  - `buff ≥ 0,15`;
  - folga ≥ 0,25;
  - margem ≥ 0,3.
- **Cores de grandeza** inalteradas: velocidade violeta, força #5AA2FF, momento magenta, impulso ~#9CC7FF, energia interna laranja,
  luz #FFD25A.
- **Legibilidade antes de beleza:** nenhum efeito (fog, glow, partícula, profundidade) pode reduzir o contraste de um rótulo ou de uma
  seta. Na dúvida, menos efeito.

---

## Parte 2 — HANDOFF v7 (rodada visual)

### 0. Rodada
- Unidade `videos_longos/yt_0016_sistemas_momento/` (preview v6). Rode `git status --short`. Copie a unidade para `_v6/` (código,
  ficha, âncoras e `threejs/`; sem renders). Salve este handoff como `handoff_v7.md`.
- **Congelado:**
  - a voz `audio/narracao_v4_pausas.wav`;
  - as 64 âncoras e os tempos de `diz()`;
  - a duração (22:46,8);
  - o texto da narração;
  - a física e a sincronia do v6.
  Esta rodada troca só a aparência. Cada evento continua acontecendo na mesma palavra.
- 3D só em Three.js, na pipeline da unidade. Nada de Blender, `ponte.py` nem arsenal: as fichas servem, no máximo, de referência de
  geometria.
- Sem SRT, master, legendado, `entregar.py`, commit ou push. Não alterar `template/`, `docs/`, `assets/`, `experimentos/threejs/` nem
  o yt_0015. Os modelos novos ficam em `threejs/cena3d/` da unidade.

### 1. Ordem de trabalho
1. **Look primeiro:** fundo e chão globais (§1.3), mais três cenas A: T7-8 (disco), T9-5 (blocos com gráfico) e E8-1 (rifle). Gere
   stills 960×540 de 2 quadros de cada e uma prancha `look_v7.png`. Siga sem esperar aprovação, mas coloque a prancha no zip e no topo
   do relatório.
2. As outras cenas A: T8-7 (Cyrano), T9-1/T9-2 (bola e Terra, com dolly-out), T9-3 a T9-7 e T10 (blocos).
3. As cenas B: A3/A4, T7-9 (com as cargas e as linhas de campo) e C-1.
4. As cenas C: A6, E9, barras, EN2.
5. Os resíduos da tabela 1.1.
6. Aplicar fundo e chão novos às cenas 3D que já existiam (cavalo, esferas, manequim, vela), sem remodelar.

Se o tempo apertar, entregue A e B completas e liste o que de C ficou de fora. A ordem acima é a prioridade.

### 2. Regras de implementação
- Cada cena 3D nova tem uma câmera definida por estado, com ponto de vista e easing no código, e um `pontos.json` com os pontos onde o
  Manim prende setas e rótulos. Alinhamento 3D × Manim ≤ 2 px.
- Mantenha o mesmo número de eventos e replays do v6 (no máximo um replay por evento). A deriva de câmera não é replay nem loop.
- Gases, poeira e fantasmas são determinísticos (seed fixa), para que o preview e o render final batam quadro a quadro.
- Render 3D: primeiro em 960×540. Custo por quadro anotado por cena no relatório, para estimar o 1080p depois.

### 3. QA
- Sobreposição: auditoria completa, conferindo V1–V18 e N1–N8 (sem regressão) e os itens da tabela 1.1.
- **Palco congelado** (a mesma métrica do v6): meta de nenhum trecho ≥ 8 s, com a deriva de câmera e as cenas novas. Listar os
  trechos ≥ 6 s.
- Sincronia: a mesma tabela de eventos do v6, com o tempo da palavra-gatilho e o tempo do evento (desvio ≤ 0,15 s). Nada pode ter
  mudado de lugar.
- Contraste: para cada cena nova, medir o contraste mínimo entre os rótulos e o fundo atrás deles (meta ≥ 4,5:1) e confirmar que fog e
  glow não ficaram atrás de texto.
- Alinhamento 3D × Manim ≤ 2 px em todas as cenas 3D (as novas incluídas).

### 4. Parada e relatório
Pare com o preview v7 com voz, 960×540 / 15 fps, completo. O relatório (AGENTS.md) leva:
- a prancha `look_v7.png` no topo;
- arquivos e modelos novos;
- cada linha da tabela 1.2 (feito / não feito e por quê);
- os resíduos 1.1;
- o QA;
- o custo de render por cena;
- as pendências.

Zip para avaliação: preview, quadros a 5 fps, `look_v7.png`, stills antes/depois de cada cena da tabela 1.2 e os logs. Sem 1080p,
SRT, master, commit nem push.
