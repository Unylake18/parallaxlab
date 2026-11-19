# yt_0041 · EP. 16 · Coordenadas esféricas · avaliação do preview v1

Data: 2026-11-15. Base: `yt0041_v1_para_gpt.zip` (preview 540p15, 19:48,8, QA e stills). Vi o vídeo inteiro em quadros a cada 4 s e conferi em resolução cheia os trechos com problema. A prancha de prova está ao lado: `prova_v1_quadros.jpg` (15 quadros numerados, citados abaixo como [P01]…[P15]).

## 0. Veredito

O preview é fiel ao que foi pedido: o 3D bate com os alvos, as contas estão certas, a caneta não pisca e o QA automático está limpo. Os problemas que sobram são de três tipos:

1. **Leitura.** As fórmulas estão pequenas demais. Na escala 1080p, a coluna fica em ≈ 24–30 px de altura de glifo, quando o pedido era 40–48. Além disso, um terço da tela fica vazio em quase todo bloco.
2. **Perspectiva.** A cunha de 90° vista de frente transforma a bola e as cascas num "coração" (H1, B4, B5, B7). A região da receita (B3-2) não aparece. A casquinha e a lata leem mal só em 3D.
3. **Sobreposições e contas.** Há rótulos em cima de arestas, voos que pousam no lugar errado e três degraus de conta que faltam.

Parte disso vem dos meus próprios alvos e não do Claude Code: o tamanho da coluna, a cunha de frente, os menores 2×2 marcados como "opcionais" e o "MASSA ATÉ c" sem a integral. Esses itens corrijo na especificação, não cobro como erro de execução.

## 1. Sobreposições e falhas visuais (com tempo)

| # | Tempo | Bloco | Problema | Correção |
|---|---|---|---|---|
| 1 | 0:00–0:03 | H1 | O rótulo `y` do eixo escondido atrás da bola é pintado na superfície [P01] | Rótulo de eixo só aparece se a ponta do eixo estiver visível (oclusão no `pontos.json`), ou o eixo y sai pela frente da bola |
| 2 | 0:04–0:52 | H1 | A seta do eixo x atravessa a placa `PESADA NA CASCA` [P02] | Mover a legenda para dentro da cunha (no degradê) ou encurtar o eixo x |
| 3 | 1:38–1:47 | A1 | O chip `o r² sen φ` pousa no topo, ao lado do logo, e o 2º chip fica vazio [P03] | O texto nasce dentro do 2º chip (caneta), sem voo |
| 4 | 1:56–3:15 | B1-1 | Os rótulos `r` e `s` ficam em cima dos próprios segmentos, e o `s` cruza o tracejado [P04] | Deslocamento normal ao segmento ≥ 14 px (1080p), do lado de fora do triângulo |
| 5 | 2:12–3:12 | B1-1 | As legendas `φ: DO POLO NORTE…` e `θ: A LONGITUDE…` nascem no meio da coluna e depois a coluna as alcança | Nascem já no lugar final, abaixo das fórmulas |
| 6 | 4:10–4:18 | B1-3 | A seta `T` e a bola aparecem antes da caixa: a seta aponta para o nada [P05] | Ordem: caixa → célula na caixa → seta T → bola |
| 7 | 4:30–4:36 | B1-3 | A célula sai da caixa como uma lasca de poucos pixels, e na bola ela fica atravessada pela seta `T` [P06] | Ver §3.3: a célula fica 2 s acesa na caixa; uma cópia viaja e se deforma; a original fica apagada (contorno) na caixa |
| 8 | 5:12–6:36 | B2-1 | `r Δφ` e `r sen φ Δθ` ficam em cima das arestas da célula; `r sen φ Δθ` encosta no `Δr` [P07] | Placas fora da célula, com fio-guia fino até a aresta |
| 9 | 6:16–6:36 | B2-1 | As duas miniaturas de célula do painel ficam sobrepostas [P07] | Uma miniatura por linha (POLO, EQUADOR), alinhadas à direita |
| 10 | 6:24–6:36 | B2-1 | A fração da `RAZÃO` passa da borda de baixo do painel [P07] | O painel cresce 40 px ou a RAZÃO vira uma linha fora do painel |
| 11 | 6:40–7:35 | B2-2 | O determinante 2×2 e o `FATOR s` ficam minúsculos no rodapé (y ≈ 1035 em 1080p), com 2/3 da tela vazios [P08] | Ver §2: os dois painéis ocupam a tela inteira; o 2×2 fica no painel da página |
| 12 | 7:22–7:26 | B2-2 | O voo do `s = r sen φ` cruza o rótulo parado (`s = r sesenφ`) | O rótulo de origem fica parado; a cópia sobe por cima, em arco |
| 13 | 9:12–10:30 | B2-4 | O `2π` fica em cima da página vermelha e do eixo; o `π` fica longe do meridiano; a célula lima cobre o meridiano violeta [P10] | Célula menor (esc 0,6) ou no hemisfério de trás; `2π` fora do equador, com placa; `π` colado ao arco |
| 14 | 10:24–10:30 | B2-4 | `UNIDADE CERTA, NÚMERO ERRADO…` encosta na borda de baixo do painel de erros | Painel +30 px |
| 15 | 10:36–11:52 | B3-1 | A caixa aparece sem a célula lima, só a bola tem (quebra a imagem-mãe) | A célula fica na caixa e na bola, ligadas pela seta T |
| 16 | 11:08 | B3-1 | O chip `dV = r² sen φ…` aparece pequeno, no canto do painel, e não voa do B2-3 | Voo do chip para o lugar do módulo do jacobiano (glyph map 9) |
| 17 | 11:50–11:58 | B3-1→B3-2 | No dissolve, a bola da receita aparece por cima da caixa, e `O CORTE: VOLUME ZERO` fica solto à direita, sem apontar para nada [P11] | Corte seco entre as cenas; `O CORTE…` com fio até a costura |
| 18 | 12:00–12:30 | B3-2 | A região entre duas cascas e dois cones é só arame: não se vê o sólido [P12] | Ver §3.5 |
| 19 | 12:12 | B3-2 | `ENTRA` fica sobre as linhas da esfera | Placa ou deslocamento para fora |
| 20 | 12:32–13:35 | B4 | `CASCA DE RAIO r` fica sobre os contornos das cascas; as cascas aparecem como corações [P13] | Ver §3.1 |
| 21 | 13:36 | B5 | O chip `x² + y² + z² = r²` aparece no topo, centralizado, longe da coluna | O chip nasce na coluna, acima de ρ |
| 22 | 15:44–17:58 | B6 | Os rótulos `φ = π/4` e `r = 2 cos φ` ficam longe da peça; as placas `1`, `φ`, `π/3` e `2π/3` ficam em cima de arestas e da sonda [P14] | Ver §3.6 (corte 2D) |
| 23 | 17:12–17:20 | B6-2 | A linha `= 8/3 ∫ u³ du` nasce acima das linhas `u = cos φ` e dos limites, que a justificam | Ordem: u, du, limites e só depois a integral nova |
| 24 | 17:40 | B6-2 | Quando a coluna renova, `= 8/3 · 3/16 = 1/2` fica sozinha a meia altura (linha órfã começando por `=`) | A linha sobe junto com o `V =`, numa só animação |
| 25 | 19:20–19:40 | S2 | O rótulo `r = 1/cos φ` fica na borda da tampa; `RACHA EM φ = π/4` fica longe da diagonal [P15] | Ver §3.7 (corte 2D) |
| 26 | 18:04–18:08 | B7 | Miniatura 2 sem ✓ por 4 s, enquanto a voz já fala dela | ✓ entra no gatilho |
| 27 | H1, B4, B5, B7 | — | Cunha de frente = "coração" (quatro blocos) [P02][P13] | Ver §3.1 |

As 13 entradas `R5V` do relatório (glifo em voo cruzando texto parado) são trânsito e não reprovam. Mas três delas (B2-2 135 s, B6-1 33 s) cruzam a própria linha de origem: dá para resolver com o voo em arco por cima.

## 2. Tamanho e ocupação da tela

**Medido (escala 1080p):**
- coluna do B1, B2-4, B5 e B6: glifo maiúsculo ≈ 24–28 px;
- matriz do B2-3: ≈ 28 px;
- legendas Space Grotesk: ≈ 16–18 px;
- pedido: fórmula principal 40–48 px, secundária 32–38 px, legenda ≥ 26 px.

**Regra para a v2:**
- coluna com escala ×1,4 sobre o v1 (fórmula principal ≈ 40 px);
- coluna começando em x ≈ 1000 e indo até a margem direita (48 px);
- o 3D cresce para ocupar x de 48 a 960;
- máximo de 5 linhas por etapa: renovar a coluna mais vezes, com o chip do resultado no topo.

**Os blocos 2D (B2-2, B2-3) ocupam a tela inteira:**
- B2-2: dois painéis lado a lado de 900 × 760, o 2×2 dentro do painel da página e o cartão `OS FATORES SE MULTIPLICAM` embaixo, centralizado;
- B2-3: matriz a 44 px, centralizada.

## 3. Perspectiva, câmera e vistas (o que muda na v2)

### 3.1 Cortar a bola por um octante, não por uma cunha de frente
Hoje a cunha de 90° fica centrada na direção da câmera. As duas faces do corte são vistas de quina, e o contorno vira um coração (H1, B4, B5, B7).

Proposta: tirar **um oitavo** da bola (x > 0, y > 0, z > 0), com a câmera olhando para dentro do vão (azimute no meio do octante, elevação ≈ 30°). Assim aparecem **três faces planas de quarto de disco**:
- no H1 e no B5, o degradê radial lê como anéis concêntricos (centro escuro, borda ciano);
- no B4, as cascas viram **arcos concêntricos de quarto de círculo**, que é a imagem clássica da cebola.

É uma troca de geometria no `c41.js`. Não é efeito novo.

### 3.2 Duas vistas no endereço (B1-1, B1-2)
O 3D fica à esquerda. A coluna **ganha dois desenhos 2D pequenos** antes das fórmulas, os mesmos do B2-2:
- **página** (vista de lado): z para cima, s para o lado, o triângulo com r, φ, z = r cos φ e s = r sen φ;
- **chão** (vista de cima): o s com o θ, x = s cos θ e y = s sen θ.

Cada fórmula voa do desenho 2D correspondente. As polares no chão o aluno já conhece. Isso responde ao "diferentes ângulos e visões" sem girar câmera.

### 3.3 A caixa vira a bola (B1-3)
- A caixa entra primeiro, com eixos e rótulos.
- A célula lima acende na caixa (2 s).
- A seta `T` entra.
- **Uma cópia** da célula viaja ao longo da seta e se deforma até a casca curva na bola. A original fica na caixa só em contorno lima.
- As bordas ruins acendem nas duas peças ao mesmo tempo, como já está.

Isso refaz o alvo 05 (a guia tracejada lima volta).

### 3.4 A caixinha curva (B2-1)
- Uma única órbita de **~35° em 4 s**, logo depois da célula ampliada, para revelar a profundidade das três arestas. Hoje a aresta Δr fica escondida embaixo.
- A câmera para antes da primeira aresta.
- As arestas acendem uma por vez, com placa fora da peça e fio-guia.

### 3.5 A receita (B3-2)
- A região entre duas cascas e dois cones vira um **sólido opaco** (a mesma "célula" grande, em lima escuro). Hoje é só arame.
- A sonda sai da origem, fura a casca de dentro (ponto azul-claro `ENTRA`) e sai pela de fora (ponto coral `SAI`).
- As duas cascas ficam pintadas nas cores da entrada e da saída.

### 3.6 A casquinha (B6) com o corte 2D
Os limites da casquinha se leem num **corte meridiano** (a página θ = cte), em 2D:
- o eixo z;
- a reta do cone a 45° (violeta);
- o círculo r = 2 cos φ de centro (0, 1) (coral);
- a sonda saindo da origem;
- o encontro em (s, z) = (1, 1).

Composição:
- B6-1: o 3D fica no topo à esquerda (esc 0,6) e o corte 2D à esquerda, embaixo;
- os rótulos `φ = π/4`, `r = 2 cos φ` e `(1, 1)` ficam no 2D, com espaço.

A conferência π/3 + 2π/3 também fica no corte 2D: o triângulo (cone) e o semicírculo de cima (meia bola) pintados.

### 3.7 A lata (S2) com o corte 2D
O corte meridiano é um retângulo 1 × 1 com a diagonal da quina em φ = π/4:
- a sonda da parede para em r = 1/sen φ;
- a da tampa para em r = 1/cos φ.

Isso deixa a "racha" evidente. O 3D da lata continua pequeno, ao lado.

### 3.8 Movimento de câmera (regra)
Uma órbita curta só onde ela revela profundidade:
- H1: já existe;
- B2-1: §3.4;
- B6-1: já existe.

Nunca durante a escrita. O resto fica parado.

## 4. Conta inteira e MF-Tools

| # | Bloco | Falta | Linha nova (texto exato) | Animação |
|---|---|---|---|---|
| A1 | B2-3 | Os dois menores 2×2 (os meus alvos deixavam opcional) | `M₃₁ = r cos φ cos θ · r sen φ cos θ − (−r sen φ sen θ) · r cos φ sen θ` → `= r² sen φ cos φ cos²θ + r² sen φ cos φ sen²θ` → `= r² sen φ cos φ (cos²θ + sen²θ)`; o mesmo para `M₃₂ = sen φ cos θ · r sen φ cos θ − (−r sen φ sen θ) · sen φ sen θ = r sen²φ (cos²θ + sen²θ)` | Os quatro fatores voam da matriz (sublinhado no menor); evidência por glyph map; `= 1` sob o parêntese |
| A2 | B5 | `MASSA ATÉ c` sem a integral | `M(c) = ∫₀^{2π}∫₀^π∫₀^c r³ sen φ dr dφ dθ` → `= [r⁴/4]₀^c · 2 · 2π` → `= (c⁴/4 − 0) · 2 · 2π` → `= πc⁴` | O 2 e o 2π voam da linha do M = π; a primitiva entra pela caneta |
| A3 | B5 | `V = 4π/3` sem origem na média | `V = 4π/3 (R = 1)` | Chip voa do resultado do B2-4 (a cena guarda o chip) |
| A4 | B6-1 | Cone e esfera sem a equação cartesiana de partida | `CONE z = √(x² + y²)` → `r cos φ = r sen φ` → `tg φ = 1` → `φ = π/4`; `ESFERA x² + y² + z² = 2z` → `r² = 2r cos φ` → `r = 2 cos φ (r > 0)` | Glyph map com x² + y² + z² → r² e z → r cos φ voando das chaves do B1 |
| A5 | B6-2 | Ordem das linhas da substituição | `u = cos φ, du = −sen φ dφ` → `φ = 0 → u = 1; φ = π/4 → u = √2/2` → `= (8/3) ∫₁^{√2/2} u³ (−du)` → `= (8/3) ∫_{√2/2}^{1} u³ du` | Os limites voam da linha dos limites; o `−` e a troca dos limites num glyph map (os dois limites trocam de lugar em arco, o `−` some junto) |
| A6 | B4 | Notação misturada `4/3 πR³` × `4πR³/3` | Sempre `\dfrac{4\pi R^3}{3}` | — |

**MF-Tools.** As 17 famílias existem, mas várias são uma chamada só. Na v2, cada degrau das linhas acima é um `TransformByGlyphMap` com mapa explícito:
- A1: 3 por menor;
- A2: 3;
- A4: 2 + 2;
- A5: 2.

Cancelamento em dois tempos: o par acende e some junto.

## 5. O que fica como está

- 3D em Three.js, alinhamento de 0,01 px e IoU de 0,996.
- Caneta, flash zero, sem pulso nem palco vivo.
- Grade de borda a borda no 2D.
- Cores das grandezas.
- Os três caminhos do fator.
- Duração ≈ 19:49: o corte para ≈ 16:00 continua opcional (§5 da proposta).

## 6. Próximo passo
HANDOFF v2 com:
- as 27 correções da §1;
- as regras de tamanho da §2;
- as trocas de vista da §3, com **quadros-alvo novos só das cenas que mudam**: H1/B4/B5 com o octante, B1-1 com as duas vistas, B1-3, B2-2, B3-2, B6 e S2 com os cortes 2D;
- as linhas A1–A6 da §4.
