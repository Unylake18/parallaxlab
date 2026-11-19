# BRIEFING vid_0029 — Por que o campo não escapa do toroide? (teste Three.js + Manim)

Documento autocontido para o Claude Code. Responda em pt-BR. Não é preciso reler o repositório inteiro.
Este é o **primeiro vídeo de teste do pipeline Three.js (3D dinâmico) + Manim (passo a passo 2D e álgebra)**. A física e o
roteiro abaixo são especificação; o pipeline técnico (seção 6) é proposta de implementação e pode ser ajustado se houver motivo
concreto, desde que o relatório explique.

---

## 0. A ideia em uma frase

Um solenoide dobrado até fechar em anel prende o campo magnético dentro do enrolamento: pela Lei de Ampère, **B = μ₀NI/(2πr)
dentro e zero fora (e no buraco)**, e o campo lá dentro **nem é uniforme**: é mais forte perto do buraco.

**Como o vídeo funciona:** o toroide 3D "canta solto" o tempo todo na metade de cima da tela (gira devagar, a corrente corre
pelo fio, o campo pulsa dentro do anel). O Manim faz o raciocínio, um passo por vez, na metade de baixo. Nos momentos de
contagem de corrente, a câmera 3D pousa na **vista de cima, alinhada ao Manim**, e o Manim desenha por cima dela (círculo
amperiano, ⊙/⊗, gráfico de B(r)), como no demo do solenoide aprovado pelo Kaio em 2026-10-26.

---

## 1. Unidade e rodada

- **Unidade:** `videos/vid_0029_campo_toroide/` (criar). Classe Manim sugerida: `CampoToroide029`.
- **ID e série:** `vid_0029` · **POR TRÁS DA FÓRMULA · EP. 09** (aprovados pelo Kaio em 2026-10-26, condicionados a:) rode `ls videos` e confira que `vid_0025`–`vid_0028`
  não colidem e que o EP. 09 está livre (o último visto no clone da nuvem é o EP. 08). Se colidir, **pare e reporte**.
- **Formato:** `curto_vertical` (1080×1920), `template/config.py`, sem mudar o template. Nada em `template/`, `docs/`, `assets/`.
- **Fase aberta:** **preview visual silencioso**, 540×960 / 15 fps (3D e Manim nessa resolução). **Não** gerar voz, SRT, master,
  legendado, entrega ou publicação. A narração da seção 9 é para orientar ritmo e conteúdo; a voz vem depois.
- **Duração-alvo:** animação-base ≈ 170 s; final com voz entre **175 e 200 s** (o Kaio pediu "uns 3 min").
- **solido_3d:** `toroide_corrente` (aprovado no arsenal), **portado para Three.js** neste vídeo. Parâmetros da ficha:
  `raio_maior = 1.6`, `raio_menor = 0.5`, `raio_fio = 0.04`, `nucleo = 0`, `eixo = 0`; **exceção aprovada pelo Kaio: `n_espiras = 24`**
  (a ficha usa 40; com 24 os ⊙/⊗ da vista de cima ficam legíveis no celular). É decisão de visualização, não de física: o N da conta
  continua simbólico. O Blender **não** é usado nesta unidade.
- Não commit, não push, não branch (salvo pedido do Kaio).

---

## 2. Arquivos

- **Ler:** `AGENTS.md` (já lido); `videos/vid_0024_carga_helice/cena.py` (padrão de curto: `LAYOUT`, `screen_text`, glyph maps,
  end card); `template/config.py`; `template/fonts.py`; a ficha `experimentos/blender/arsenal/solidos/toroide_corrente.json`.
  Só o necessário.
- **Referência do demo aprovado** (fonte entregue pelo Kaio a partir da pasta do projeto `threejs_demo/fonte/`):
  `cena3d.html` (cena 3D por frame, `window.setFrame(f)`), `render3d.js` (Playwright → PNG) e `cena_manim.py` (Manim abrindo
  no último quadro do 3D). Reaproveite as ideias, não os caminhos.
- **Criar na unidade:** `ficha.md`, `timeline.json`, `cena3d/` (HTML + JS do toroide, com `three.min.js` r128 local e
  `RoomEnvironment.js`), `render3d.js`, `cena.py` (Manim), `compor.py` (ou `.sh`) para a composição final do preview.
- **Dependência:** Node + Playwright só para renderizar o 3D. **Não** alterar `pyproject.toml`/`uv.lock`. Se precisar de
  `package.json`, deixe-o **dentro da unidade** e reporte. Se Node/Playwright não estiverem disponíveis na máquina, pare e reporte.

---

## 3. A física (resolvida e verificada; não redesenhar)

**Sistema:** toroide ideal de seção circular, N espiras bem apertadas, corrente I, raio médio R, raio da seção a, núcleo de ar.
Eixo de simetria = z. Coordenada r = distância ao eixo.

**Simetria (formulação fechada pelo Kaio):** "No toroide ideal, a simetria faz o campo acompanhar círculos em torno do eixo e ter o
mesmo módulo ao longo de cada círculo." Não dizer que a invariância por rotação, sozinha, prova que B é tangente; não abrir a prova
das componentes radial/axial.

**Ampère num círculo de raio r:** ∮ B⃗·dℓ⃗ = B · 2πr = μ₀ I_enc.

| Região | O que fura o disco do círculo | I_enc | B |
|---|---|---|---|
| Buraco: r < R − a | nada | 0 | **0** |
| Dentro do enrolamento: R − a < r < R + a | o lado de dentro de cada espira, uma vez, todas no mesmo sentido | N I | **μ₀ N I / (2π r)** |
| Fora: r > R + a | cada espira duas vezes: lado de dentro (subindo) e lado de fora (descendo) | N I − N I = 0 | **0** |

**Consequências que o vídeo mostra:**
- B dentro **não é uniforme**: cai com 1/r. Razão entre a borda de dentro e a de fora: (R + a)/(R − a).
  Com os parâmetros da ficha (1,6 e 0,5): 2,1/1,1 ≈ **1,9** ("quase o dobro").
- **Caso-limite (conferência):** se a ≪ R, então r ≈ R no enrolamento e B ≈ μ₀ (N/2πR) I = **μ₀ n I**, com n = N/(2πR)
  espiras por unidade de comprimento: o campo do solenoide (vid_0009).
- **Unidades:** μ₀ N I/(2πr): (T·m/A)·A/m = T. ✔
- **Conferência numérica (só QA, não vai ao vídeo):** N = 1000, I = 1 A, R = 10 cm, a = 2 cm ⇒ B(8 cm) = 2,50 mT,
  B(10 cm) = 2,00 mT, B(12 cm) = 1,67 mT.

**Cuidados de formulação (valem para tela e fala):**
- "Zero fora" vale para o **toroide ideal**. Num enrolamento real, o avanço da hélice ao longo do anel equivale a uma espira a mais
  e deixa um campo pequeno fora. Não dizer "exatamente zero na vida real"; dizer "num toroide ideal" uma vez, no começo.
- No gráfico, os saltos em R − a e R + a são do modelo ideal (fio de espessura desprezível). Não comentar além disso.
- Não usar a palavra "polo": o toroide não tem polos. Pode ser dito como curiosidade ("um ímã sem polo nenhum") só se couber.
- Sem exemplo numérico em tela.

---

## 4. Notação e cores (padrão dos longos, o mesmo do demo do solenoide que o Kaio aprovou)

| Elemento | Cor |
|---|---|
| Corrente I e tudo que a representa (tracinhos e flash no fio, ⊙/⊗, I_enc) | verde `#3FE08B` |
| Campo B (anéis de campo no 3D, setas, B na equação, curva B(r) no gráfico) | magenta `#EA63FF` |
| Geometria: r, R, a, círculo amperiano, dℓ do caminho, 2πr, eixos do gráfico, n | GEO `#B8C4DA` |
| Fio / enrolamento (matéria condutora) | aço `#7A8696` |
| N, μ₀, operadores, números | branco `#F5F7FF` |
| Texto secundário e chips | `#8FA3C4` |
| Painel do resultado final | `#0E2A52` com borda `#7FB2FF` |
| Fundo | `#050816` |

- **Diferença em relação à ficha do arsenal:** a ficha pinta o fio de azul `#267BFF` e reserva o ciano para o campo (gramática antiga
  da Lei de Gauss). Aqui vale o padrão dos longos acima: fio em aço, corrente verde, B magenta. **Não usar azul nem ciano.**
  Registre no "Teste do arsenal" como ajuste desejado para a ficha.
- Violeta é só de velocidade: **não usar**. Amarelo não existe na paleta. Corrente convencional (cargas positivas), nunca elétrons.
- Texto de tela em MAIÚSCULAS, Space Grotesk (`screen_text`). Pouca escrita: no máximo ~3 elementos novos por vez.

---

## 5. Convenções geométricas e sentidos (conferir no QA)

- Eixo do toroide = z, apontando **para a câmera na vista de cima**.
- Sentido da corrente escolhido: no **lado de dentro** de cada espira (r = R − a) a corrente **sobe** (+z, sai da tela na vista de
  cima: **⊙**); no **lado de fora** (r = R + a) ela **desce** (−z, entra na tela: **⊗**).
- Círculo amperiano percorrido no sentido **anti-horário visto de cima** (normal +z). Então I_enc = +N I dentro do enrolamento.
- Logo, **B dentro do enrolamento circula no sentido anti-horário visto de cima** (regra da mão direita: polegar no sentido das
  correntes ⊙ do lado de dentro). Setas magenta no 3D e no Manim nesse sentido.
- A circulação do círculo amperiano é desenhada com duas pontas de seta GEO pequenas, sempre anti-horário.
- O mesmo sentido tem que valer na hélice 3D: confira que os tracinhos verdes **sobem no lado de dentro** e que os anéis magenta
  giram anti-horário vistos de cima (regra da mão direita). **Não** usar Biot–Savart da hélice para isso (ver seção 7).

---

## 6. Pipeline técnico (Three.js + Manim)

**Princípio:** o 3D e o Manim são dois vídeos do mesmo tamanho e da mesma duração, sincronizados por um arquivo de tempos, e
compostos no final. O 3D é o fundo opaco; o Manim é uma camada transparente por cima.

1. **`timeline.json`** (fonte única de tempos): lista de beats `{id, inicio_s, fim_s}` e eventos com tempo absoluto
   (`corrente_liga`, `camera_topo`, `amperiano_r`, `camera_livre` etc.). O Manim lê os tempos para os `run_time`/`wait`; o 3D lê
   os mesmos tempos para a câmera e os efeitos. Depois da voz, só esse arquivo muda e os dois são re-renderizados.
2. **3D:** `cena3d/index.html` com `window.setFrame(f)` determinístico (tudo é função do frame, sem relógio; mesmo esquema do
   demo). `render3d.js` (Playwright) salva `frames3d/f%05d.png` na resolução pedida (preview 540×960; final 1080×1920) e
   `ffmpeg` gera `parte3d.mp4`. Sem `requestAnimationFrame` no render.
3. **Manim:** `cena.py` renderizado com fundo transparente (`--transparent`, saída `.mov` com alpha) e **sem** imagem do 3D dentro
   dele. No preview, se o `.mov` transparente pesar, pode renderizar com fundo `#050816` só para conferir layout, mas a composição
   usa a versão transparente.
4. **Composição:** `ffmpeg -i parte3d.mp4 -i manim.mov -filter_complex overlay` → preview H.264. No final valerá CRF 14 (AGENTS.md).
5. **Alinhamento 3D ↔ Manim (crítico):** na vista de cima, o plano z = 0 do toroide tem que cair exatamente nas coordenadas
   do Manim abaixo. Use, nesses trechos, uma câmera **ortográfica** (ou perspectiva com dolly-zoom até fov ≤ 14°, como no demo) e
   confira a sobreposição: erro ≤ 2 px no preview 540×960.

**Escala e posição na vista de cima (unidades do Manim, frame 9 × 16):**
fator 3D → Manim = 3,6/2,1 ≈ 1,714 · centro do toroide em **(0, 2,2)** · R − a → **1,886** · R → **2,743** · R + a → **3,600**.
O anel ocupa y de −1,4 a 5,8. Topo (y > 6,2) fica para a manchete/tag; a faixa y < −1,8 é a área da álgebra.

**Fora da vista de cima,** o toroide fica livre na metade de cima (centro em torno de y = 2,5), em órbita lenta, levemente
inclinado (elevação ~25°, como o enquadramento da ficha), sem invadir a área da álgebra. O Manim não depende da posição exata
dele nesses trechos.

---

## 7. O que o 3D faz (o toroide "cantando solto")

- **Fio:** tubo de aço em hélice toroidal (24 espiras, raio do fio 0,04 × escala), material metálico com reflexo suave, mesma luz
  do demo (chave branca, contraluz magenta, preenchimento leve). Sem núcleo de vidro, para o campo dentro ficar visível.
- **Corrente = tracinhos verdes** (como nos longos): segmentos curtos e brilhantes **alinhados à tangente do fio**, correndo pelo
  enrolamento no sentido da seção 5, com velocidade constante. Nada de bolinhas.
  **Flash verde:** quando a corrente liga (B01), um pulso verde largo percorre o enrolamento inteiro uma vez (~1,5 s), e só
  então os tracinhos aparecem e ficam. Nas contagens (B06, B07), um flash curto acende **só os trechos que furam o disco do
  amperiano** (lado de dentro em B06; lado de dentro e lado de fora, em sentidos opostos, em B07).
- **Campo B = visualização do campo do MODELO IDEAL**, não uma reconstrução Biot–Savart das 24 espiras discretas. **Não calcular
  o campo da hélice**: com 24 voltas ele tem fuga externa e contradiz a aula (decisão do Kaio). Anéis magenta **concêntricos ao eixo**, dentro da seção do toro (por exemplo raios R + a·{−0,7; −0,35; 0; 0,35; 0,7}
  e algumas alturas dentro da seção), com pontas de seta pequenas no sentido anti-horário visto de cima. **Brilho e tamanho das
  setas ∝ 1/r** (mais forte perto do buraco). O campo nasce em B01 junto com a corrente e pulsa de leve o vídeo todo.
  **Nada de campo no buraco nem fora do anel.**
- **Círculo amperiano em 3D:** anel GEO tracejado no plano z = 0, que aparece e muda de raio conforme os beats B05–B08 (o raio é
  um evento do `timeline.json`, o mesmo que o Manim usa para o círculo 2D).
- **Câmera por beat:** órbita lenta (B01, B02, B09, B10); vista de cima alinhada (B03 a B08); em B09, aproximação de um trecho
  pequeno do anel, que parece um solenoide reto (o caso-limite), e volta.
- **Estrelas** discretas ao fundo, determinísticas. Sem música, sem efeitos.

---

## 8. Storyboard por beat (tempos-alvo da animação-base; a voz depois estica)

Coordenadas do Manim: área de álgebra centrada em y ≈ −4,2 (de −1,8 a −6,8). Manchete no topo (y ≈ 6,9). Rodapé livre abaixo
de y = −7,2 (legendas futuras).

| Beat | t (s) | 3D | Manim | Fala (resumo) |
|---|---|---|---|---|
| **B01 Gancho** | 0–12 | toroide surge em órbita; **flash verde** percorre o fio; anéis de campo acendem por dentro | tag `POR TRÁS DA FÓRMULA · EP. 09` + manchete **"POR QUE O CAMPO NÃO ESCAPA?"**; depois chip `E FORA DO ANEL?` | o campo fica preso dentro; fora, nada. Por quê? |
| **B02 O objeto** | 12–28 | órbita lenta; tracinhos correndo | chip `MODELO IDEAL` (DIM) primeiro; depois quatro chips com cor: `N ESPIRAS` (branco), `CORRENTE I` (verde), `RAIO MÉDIO R` e `RAIO DA SEÇÃO a` (GEO); um esboço 2D pequeno ao lado ligando R e a a um corte do anel | solenoide dobrado até fechar; toroide ideal; nomes das grandezas |
| **B03 Simetria** | 28–48 | câmera desce para a **vista de cima alinhada** | contorno do anel (GEO fino) por cima do 3D; círculo de raio r (GEO tracejado) dentro do enrolamento; 6–8 setinhas magenta tangentes **do mesmo tamanho** no círculo; chip `MESMO B NO CÍRCULO TODO` | no toroide ideal, a simetria faz o campo acompanhar círculos em torno do eixo, com o mesmo módulo em cada círculo |
| **B04 Ampère** | 48–64 | vista de cima; campo pulsando | `∮ B⃗·dℓ⃗ = μ₀ I_enc` → `B ∮ dℓ = μ₀ I_enc` → `B (2πr) = μ₀ I_enc` (glyph maps, seção 10) | B sai da integral; sobra o comprimento do círculo |
| **B05 Buraco** | 64–79 | amperiano 3D encolhe para r ≈ 1,2 (Manim) | círculo 2D no buraco + disco translúcido GEO 12 %; contador `I_enc = 0` (verde); `B = 0` (magenta) | nenhum fio fura o disco ⇒ campo zero |
| **B06 Dentro** | 79–104 | amperiano 3D em r ≈ 2,74 (meio do enrolamento); **flash só nos trechos de dentro** | 24 marcas **⊙** verdes no círculo R − a (uma por espira); o disco do amperiano as engloba; contador sobe de 0 a 24 rápido e vira `I_enc = N I`; `B (2πr) = μ₀ N I` → **`B = μ₀ N I / (2πr)`** | cada espira fura o disco uma vez, mesmo sentido ⇒ N I; r no denominador: não é uniforme |
| **B07 Fora** | 104–122 | amperiano 3D em r ≈ 4,1; **flash dentro (subindo) e fora (descendo)** | aparecem 24 marcas **⊗** no círculo R + a; contador `N I − N I = 0`; `B = 0` | cada espira fura duas vezes, em sentidos opostos ⇒ cancela; por isso não escapa |
| **B08 Gráfico B(r)** | 122–146 | amperiano 3D **varre** de r = 0 até ~4,3 em ~8 s; setas de campo maiores perto do buraco | eixos r (GEO) e B (magenta) na área de baixo; cursor sincronizado com o raio do amperiano desenhando: 0 até R − a, salto, curva 1/r, queda a 0 em R + a; tracejados GEO verticais em R − a e R + a; chip `QUASE O DOBRO` entre os dois valores das bordas | três regiões num gráfico; dentro cai com 1/r; borda de dentro ≈ 2× a de fora |
| **B09 Conferência** | 146–160 | câmera aproxima de um trecho do anel: parece um solenoide reto; depois volta | `r ≈ R` (GEO) → `B ≈ μ₀ (N / 2πR) I` → `n = N / 2πR` → **`B ≈ μ₀ n I`** com chip `SOLENOIDE` | anel grande perto da seção ⇒ volta o campo do solenoide |
| **B10 Fechamento** | 160–172 | órbita lenta; campo brilhando só dentro | painel final: `B = μ₀ N I / (2πr)` **DENTRO** · `B = 0` **FORA**; depois end card silencioso `@labparallax` (padrão dos curtos) | dentro cai com 1/r; no buraco e fora, zero no modelo ideal; o solenoide fechado em anel confina o próprio campo |

**Regras de tela:** na vista de cima, os ⊙/⊗ do Manim precisam coincidir com os trechos verticais do fio 3D (mesma posição
angular das espiras: a k-ésima espira em φ_k = 2πk/24 + φ₀; use o mesmo φ₀ no 3D e no Manim). Raio dos marcadores ≈ 0,13.
Enquanto a álgebra roda, o 3D nunca congela: tracinhos e pulsação continuam.

---

## 9. Narração (proposta; orienta o ritmo do preview. A voz só será gerada quando pedida)

Tom de professor de cursinho, variáveis pelo nome, conectivos. Ritmo de referência 2,7 palavras/s ⇒ ~540 palavras ≈ 200 s.
Tags do ElevenLabs v4 em inglês, **uma por trecho**, sem `[slowly]` nem `[slow, measured pace]`.

**B01** [curious] Olha esse anel de fio. Liga a corrente... e aparece um campo magnético. Só que tem um detalhe estranho: esse campo fica preso dentro do enrolamento. Fora dele, nada. Por quê?

**B02** [thoughtful] Isso aqui é um toroide: pensa num solenoide que a gente dobrou até as duas pontas se encontrarem. Vamos tratar o toroide ideal, com as espiras bem apertadinhas. Ele tem um número de espiras, que na tela aparece como N, todas levando a mesma corrente. O raio médio do anel aparece como R, e o raio da seção, a parte grossinha do anel, aparece como a.

**B03** [thoughtful] Agora, vamos olhar de cima. No toroide ideal, a simetria faz o campo magnético acompanhar círculos em volta do eixo, com o mesmo valor ao longo de cada círculo. É só disso que a gente precisa pra usar a Lei de Ampère.

**B04** [thoughtful] Lembrando: a Lei de Ampère diz que a circulação do campo magnético num caminho fechado é mi zero vezes a corrente que atravessa esse caminho. Como o campo tem o mesmo valor no círculo todo, ele sai da integral. E o que sobra é só o comprimento do círculo: dois pi vezes o raio.

**B05** [curious] Primeira região: um círculo dentro do buraco do anel. Quantos fios furam esse disco? Nenhum. [short pause] A corrente envolvida é zero... então o campo ali é zero.

**B06** [thoughtful] Agora o círculo passa por dentro do enrolamento. Olha só: cada espira fura o disco uma vez, sempre pelo lado de dentro, e todas no mesmo sentido. São N espiras, então a corrente envolvida é o número de espiras vezes a corrente. Logo, o campo é mi zero vezes o número de espiras vezes a corrente, dividido por dois pi vezes o raio. [excited] E repara: o raio está embaixo. O campo dentro do toroide não é uniforme. Ele é mais forte perto do buraco e mais fraco na parte de fora.

**B07** [curious] E fora do anel? Agora cada espira fura o disco duas vezes: uma pelo lado de dentro, subindo, e outra pelo lado de fora, descendo. O número de espiras vezes a corrente pra um lado, e o mesmo tanto pro outro. Se cancelam. [short pause] Corrente envolvida zero... campo zero. É por isso que o campo não escapa.

**B08** [thoughtful] Juntando tudo num gráfico: zero no buraco, um salto quando a gente entra no enrolamento, uma queda com um sobre o raio lá dentro, e zero de novo do lado de fora. Com as medidas desse toroide, o campo na borda de dentro é quase o dobro do campo na borda de fora.

**B09** [thoughtful] E dá pra conferir com o que a gente já sabe. Se o anel for muito grande comparado com a seção, o raio quase não muda lá dentro e fica igual ao raio médio. Aí, o número de espiras dividido por dois pi vezes o raio médio é o número de espiras por unidade de comprimento... e voltamos ao campo do solenoide: mi zero vezes as espiras por metro vezes a corrente.

**B10** [calm, satisfied] Resumindo: dentro do enrolamento, o campo é mi zero vezes o número de espiras vezes a corrente, dividido por dois pi vezes o raio. Dentro, o campo cai como um sobre o raio. No buraco e fora, zero no modelo ideal. É assim que um solenoide fechado em anel confina seu próprio campo.

(~540 palavras ≈ 190–200 s de voz a 2,7 palavras/s. Se a voz passar de 200 s, ver seção 13; o primeiro corte de fala é a frase "Vamos tratar o toroide ideal..." virar só "num toroide ideal" dentro da frase seguinte, e o B09 perder a frase do raio médio.)

---

## 10. Álgebra e transformações (Manim + MF-Tools)

- **B04:** `∮ B⃗·dℓ⃗` → `B ∮ dℓ`: `TransformByGlyphMap` (o B atravessa para fora da integral; o vetor some porque B ∥ dℓ — o chip
  `B ∥ dℓ` pode aparecer por 1 s). `∮ dℓ` → `2πr`: FadeOut/FadeIn localizado (não há correspondência honesta de glifos).
- **B06:** `B (2πr) = μ₀ N I` → `B = μ₀ N I / (2πr)`: `TransformByGlyphMap` com o `2πr` atravessando a igualdade para o
  denominador. Destaque o r do denominador (Indicate GEO) no "o raio está embaixo".
- **B09:** `μ₀ N I / (2πR)` → `μ₀ (N / 2πR) I` → `μ₀ n I`: `TransformMatchingTex` para o reagrupamento, glyph map para o
  colapso `N/2πR → n`.
- Contadores de I_enc: `DecimalNumber`/`Integer` verdes, só no B06 (0 → 24 → "N I"). Sem índices de debug no vídeo final.
- Fórmulas legíveis no celular: `font_size` ≥ 56 nas equações principais, ≥ 72 no resultado final.

---

## 11. QA do preview (só o necessário)

1. `py_compile` da `cena.py`; render do 3D e do Manim em 540×960 / 15 fps; composição. Sem renders extras.
2. Quadros de conferência: B01 (flash e campo nascendo), B03 (alinhamento 3D ↔ Manim na vista de cima, ≤ 2 px), B06 (⊙ sobre
   os trechos de dentro, contador, glyph map do 2πr), B07 (⊗ e cancelamento), B08 (cursor do gráfico sincronizado com o raio do
   amperiano 3D; razão das bordas ≈ 1,9 medida na própria curva), B09 (μ₀ n I), B10 (painel e end card).
3. Conferir sentidos da seção 5 nos dois mundos (3D e Manim): ⊙ dentro, ⊗ fora, B anti-horário visto de cima.
4. Conferir cores por token (seção 4), nada de azul/ciano/violeta; texto em MAIÚSCULAS; ≤ ~3 elementos novos por vez.
5. Duração total e por beat (frames/fps), comparada com a tabela da seção 8.
6. Custo: tempo de render do 3D por quadro e total, tempo do Manim, tempo da composição.

---

## 12. O que NÃO fazer

- Voz, SRT, master, legendado, entrega, publicação, commit, push.
- Bolinhas como corrente (são tracinhos ou flash); elétrons; azul/ciano/violeta; campo desenhado no buraco ou fora do anel.
- Pôr o 3D dentro do Manim como imagem estática nos trechos em que ele deve continuar animado.
- Alterar `template/`, `docs/` globais, `AGENTS.md`, `pyproject.toml`, `uv.lock` ou o arsenal do Blender.
- Prova formal das componentes radial/axial de B; exemplo numérico em tela; teaser de outro vídeo.
- Remotion (não entra neste teste: `timeline.json` + render determinístico + ffmpeg bastam); tokamak ou outra aplicação no fechamento;
  campo da hélice calculado por Biot–Savart.
- Refatorar, limpar ou iniciar outra fase.

---

## 13. Se passar do tempo

Cortar nesta ordem: (1) o esboço 2D de R e a no B02 (fica só nos chips); (2) a aproximação do 3D no B09 (fica só a álgebra);
(3) o chip `QUASE O DOBRO`. **Nunca** cortar as três regiões (B05–B07) nem o gráfico B(r) (B08).

---

## 14. Relatório de entrega (obrigatório)

Arquivos criados; verificações e renders com resultados; caminho do preview composto; duração total e por beat; limitações e
pendências; e os dois testes:

- **Teste do arsenal** (formato de `docs/formatos.md`): sólido `toroide_corrente`, portado para Three.js; resolução; custo/peso;
  o que funcionou; o que faltou; ajustes desejados (cores da ficha: fio aço, corrente verde, B magenta; `n_espiras = 24` para curtos).
- **Teste do pipeline Three.js + Manim:** como ficou o `timeline.json`; precisão do alinhamento na vista de cima; tempo de render;
  o que seria preciso mudar para o render final 1080×1920 e para re-sincronizar depois da voz.

Pare após o preview, sem iniciar voz.

---

## 15. Decisões do Kaio (2026-10-26)

1. **Série e ID:** `vid_0029` · POR TRÁS DA FÓRMULA · EP. 09, desde que o `ls videos` confirme o slot.
2. **Fechamento sem tokamak:** termina no payoff ("É assim que um solenoide fechado em anel confina seu próprio campo").
3. **24 espiras** aprovadas para este curto (decisão de visualização).
4. **Simetria** com a formulação suave do B03.
5. **Campo desenhado = modelo ideal**, com chip `MODELO IDEAL` no B02.
6. **Arquitetura do teste:** Three.js = objeto e fenômeno 3D; Manim = vetores, construções, equações e transformações. Remotion só
   entra depois, e só se a composição por `timeline.json` + ffmpeg virar gargalo.
7. **O que o teste precisa provar:** se o 3D carrega a intuição espacial enquanto o Manim carrega o raciocínio matemático, sem
   os dois competirem pela tela. Comente isso no relatório (seção 14).
