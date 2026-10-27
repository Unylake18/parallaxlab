# Storyboard — Gauss + superposição (yt_0004)

Versão: 2026-10-13. 16 blocos (N01–N16). Fala completa em `narracao.md`, mesmos IDs; abaixo, âncoras. Janelas são orçamento de montagem (soma 10:15); estimativa realista 9:30–10:00 (ver `ficha.md`). Sem código, voz ou render.

Notação em tela: `Q_{\mathrm{env}}` / carga envolvida (como em yt_0001/yt_0002); `\vec r_+`, `\vec r_-`, `\vec d`, `C=\rho/3\varepsilon_0`. Cores: fonte positiva azul, negativa/fictícia magenta tracejado translúcido, campo ciano, gaussiana violeta, vetores posição brancos (gramática do yt_0001/yt_0002). Nenhum sólido 3D: 2D/2.5D em Manim, circunferências com sombreamento leve.

Modos: FOCUS (um objeto), BUILD (equação/construção em passos), SPLIT (geometria + equação, mesmo estado matemático). Nunca três painéis permanentes.

---

**N01 · 0:00–0:30 · Pergunta**
- Objetivo: abrir com o desconforto — configuração sem simetria útil.
- Fala: “Duas esferas do mesmo tamanho se sobrepõem…” → “…o campo muda?”
- Visual: duas esferas (+ρ azul, −ρ magenta), sobreposição em lente; pontos candidatos na lente aparecem um a um.
- Texto: `+ρ`, `−ρ`, “E = ?”, “E muda com P?”. Sem header/marca.
- Movimento: esferas deslizam até a sobreposição; pergunta 2 com marcador de P saltando entre posições.
- Estado final: configuração das duas esferas, P marcado, sem resposta. Fonte: Griffiths 2.18.

**N02 · 0:30–0:42 · Intro**
- Objetivo: marca, sem prolongar. Visual: título LEI DE GAUSS, subtítulo “Superposição”; esferas reduzidas à faixa inferior (opacidade 0,3); entram watermark/header.
- Estado final: header ativo; esferas em segundo plano.

**N03 · 0:42–1:25 · Gauss não dá E direto**
- Objetivo: separar “lei válida” de “simetria utilizável”.
- Fala: “Você acabou de aprender…” → “…descobrir o campo diretamente.”
- Visual (FOCUS→COMPARE): configuração à esquerda ampliada; três tentativas de gaussiana: (1) esfera em O₊, (2) esfera em O₋, (3) superfície envolvendo tudo. Cada uma recebe um ✗ discreto e etiqueta “simetria quebrada”; na (3), vetores amostrados com módulo/ângulo variados.
- Texto final (BUILD): `Gauss: sempre verdadeira` / `simetria total ⇒ E direto: não`. Nunca escrever “Gauss não funciona”.
- Estado final: as duas linhas de texto; configuração ao fundo.

**N04 · 1:25–2:00 · Superposição**
- Objetivo: mudar de perspectiva — partes simétricas.
- Fala: “Mas e se não olharmos a configuração inteira?…” → “Falta uma ferramenta.”
- Visual (BUILD): configuração = esfera(+ρ) + esfera(−ρ) (separação em dois painéis breves, SPLIT temporário, recolhido ao fim). `ρ_total = ρ₁ + ρ₂ ⇒ E_total = E₁ + E₂`.
- Selo: `sempre válido ≠ sempre útil`.
- Estado final: selo + `E_total = E₁ + E₂`; pergunta aberta: “campo de uma esfera uniforme por dentro?”.

**N05 · 2:00–3:20 · Ferramenta: E⃗ = C r⃗ (bloco enxuto)**
- Objetivo: obter a ferramenta sem virar aula de Gauss.
- Fala: “Considere uma esfera maciça isolante…” → “…daqui a pouco.”
- Visual (SPLIT): esquerda, esfera isolante azul, ponto a distância r, gaussiana violeta concêntrica, setas radiais; direita, passos:
  1. `Q_env = ρ·(4/3)πr³`
  2. `E·4πr² = Q_env/ε₀`
  3. `E = ρr/3ε₀`
  4. selo de intuição `Q_env ∝ r³, área ∝ r² ⇒ E ∝ r`
  5. `E⃗ = E r̂`, `r⃗ = r r̂` ⇒ `E⃗ = (ρ/3ε₀) r⃗`
  6. `C = ρ/3ε₀` ⇒ `E⃗ = C r⃗` (caixa).
- Movimento: gaussiana cresce e encolhe, vetores acompanham e crescem proporcionalmente a r (mostra linearidade). Sem exibir integral de volume nem coordenadas esféricas.
- Estado final: caixa `E⃗ = C r⃗` + legenda “linear no vetor posição, origem no centro”. Duração ~80 s: não ampliar.

**N06 · 3:20–3:55 · Retorno e vetores posição**
- Objetivo: nomear objetos; origem importa.
- Fala: “Voltemos às duas esferas…” → “Cada esfera usa a sua.”
- Visual (FOCUS): sobreposição ampliada; rótulos `O₊`, `O₋`, `d⃗` (seta de O₊ a O₋), `P` na lente. Apresentar `r⃗₊` (de O₊ a P) e `r⃗₋` (de O₋ a P) nessa ordem, cada um com sua cor de origem.
- Texto: “Mesmo ponto, duas origens”.
- Estado final: construção completa dos três vetores sobre a figura, sem a relação.

**N07 · 3:55–4:50 · r⃗₊ = d⃗ + r⃗₋ (não comprimir)**
- Objetivo: nascer a relação da geometria.
- Fala: “Esta é a relação em que tudo se apoia…” → “…o que liga os centros.”
- Visual (BUILD, geometria antes da álgebra):
  1. destacar o caminho direto `r⃗₊` (O₊→P);
  2. mostrar o caminho em dois trechos: `d⃗` (O₊→O₋), depois `r⃗₋` (O₋→P), ponta com cauda;
  3. sobrepor os dois caminhos, mesmo ponto final;
  4. só então: `r⃗₊ = d⃗ + r⃗₋` ⇒ `r⃗₊ − r⃗₋ = d⃗` (caixa).
- Movimento: leitura de 4 s ao final; sem mover P ainda.
- Estado final: triângulo O₊O₋P + as duas equações.

**N08 · 4:50–5:25 · Campos e sinais**
- Objetivo: sinal tem origem física.
- Fala: “A esfera positiva produz…” → “…o contrário do vetor posição.”
- Visual (SPLIT): em P, `E⃗₊ = C r⃗₊` (para fora de O₊, ciano) e `E⃗₋ = −C r⃗₋` (para O₋, ciano); setas de reforço “sai da positiva” / “chega à negativa”. Equações aparecem junto da seta correspondente.
- Estado final: ambas as setas em P + equações; triângulo recuado.

**N09 · 5:25–5:55 · Soma**
- Objetivo: payoff algébrico.
- Fala: “Superponha…” → “…e mesmo assim há campo.”
- Visual (BUILD): `E⃗ = E⃗₊ + E⃗₋` → `C r⃗₊ − C r⃗₋` → `C(r⃗₊ − r⃗₋)` → `C d⃗` → `(ρ/3ε₀) d⃗`. Transformação preferencial `TransformMatchingTex`; glyph map só se a fatoração do C exigir. Soma vetorial das duas setas de P resulta numa seta paralela a `d⃗`.
- Nota em tela: “aqui, ρ_total = 0 — e E ≠ 0”.
- Estado final: caixa `E⃗ = (ρ/3ε₀) d⃗`; seta total desenhada ao lado de `d⃗`.

**N10 · 5:55–6:40 · Mover P (momento central)**
- Objetivo: perceber a uniformidade.
- Fala: “Olhe a resposta. Onde está o ponto P?…” → “…não se move.”
- Visual (SPLIT): equação final à direita com `P` riscado/esmaecido (“sumiu”); geometria à esquerda: P percorre ao menos 4 posições da lente em trajetória lenta contínua. Atualização simultânea de `r⃗₊`, `r⃗₋`, `E⃗₊`, `E⃗₋` (variam); `E⃗_total` em cor de destaque, fixa, com seta-referência fantasma ao lado para mostrar que é idêntica.
- Movimento: sem aceleração brusca; pausa de ~2 s em cada posição-chave.
- Estado final: P na posição inicial, E_total destacado; equação visível.

**N11 · 6:40–7:15 · ΔE⃗ = 0**
- Objetivo: explicação física da uniformidade.
- Fala: “Por que isso acontece, além da álgebra?…” → “…É a soma que não muda.”
- Visual (BUILD): P→P′ com Δ pequeno; Δr⃗₊ e Δr⃗₋ desenhados lado a lado, idênticos (paralelogramo). `Δr⃗₊ = Δr⃗₋` ⇒ `ΔE⃗ = C Δr⃗₊ − C Δr⃗₋ = 0`.
- Texto final: “Cada campo muda. A soma não.”
- Estado final: o texto e `ΔE⃗ = 0`.

**N12 · 7:15–7:50 · −ρ como carga removida**
- Objetivo: reinterpretar o problema.
- Fala: “Agora uma pergunta nova…” → “…reproduz a configuração.”
- Visual (FOCUS→BUILD): título “E se −ρ for a região que queremos retirar?”; esfera maciça `+ρ` isolante; esfera fictícia `−ρ` tracejada entra; na sobreposição `+ρ + (−ρ) = 0`, a região esmaece até “vazio” (cavidade). Texto: `remover carga = somar a distribuição oposta`; ressalva `decomposição matemática, não carga negativa física`.
- Estado final: esfera com cavidade ao lado da decomposição `maciça + fictícia`.

**N13 · 7:50–8:25 · Cavidade deslocada**
- Objetivo: definir a nova configuração.
- Fala: “Defina a esfera maciça isolante…” → “…esfera correspondente.”
- Visual (SPLIT): corte 2D; raio `R`, raio `a`, `d⃗` do centro grande ao centro da cavidade; condição `a + |d⃗| < R` (estritamente interna); nota: `a ≠ R`, e `E⃗ = (ρ/3ε₀) r⃗` não contém R.
- Estado final: figura com R, a, d⃗ e a desigualdade.

**N14 · 8:25–9:10 · Campo na cavidade**
- Objetivo: reaproveitar a construção.
- Fala: “Pegue um ponto P na cavidade…” → “…tem campo constante.”
- Visual (BUILD→SPLIT): `r⃗` (centro grande→P), `r⃗'` (centro da cavidade→P), `r⃗ = d⃗ + r⃗'` desenhado como o triângulo da N07, mesma cor/gramática. `E⃗₁ = C r⃗`, `E⃗₂ = −C r⃗'`, `E⃗ = C(r⃗ − r⃗') = C d⃗`. Mover P rapidamente na cavidade (≈6 s) com total fixo.
- Equação final: `E⃗_cav = (ρ/3ε₀) d⃗` (caixa).
- Estado final: caixa e figura da cavidade.

**N15 · 9:10–9:35 · Limites**
- Objetivo: bloquear generalizações falsas.
- Fala: “Cuidado com o que isso não diz…” → “…produza campo uniforme.”
- Visual (FOCUS): `superposição: sempre válida` / `útil: porque sabemos resolver as partes`; cinco condições aparecem em sequência: densidade uniforme; cavidade esférica; E linear em r⃗; mesmo |C| nas duas; `r⃗ − r⃗' = d⃗` fixo. Selo `✗ toda cavidade`.
- Estado final: lista; sem cenas novas.

**N16 · 9:35–10:15 · Checagens e estratégia**
- Objetivo: confiança no resultado e payoff conceitual.
- Fala: “Teste se o resultado faz sentido…” → “…use a superposição.”
- Visual (BUILD): quatro checagens rápidas, cada uma com mini-ilustração: `d⃗ = 0 ⇒ E⃗ = 0`; `ρ → 0 ⇒ E⃗ → 0`; trocar sinais ⇒ seta inverte; `[ρ d/ε₀] = N/C`. Depois, cadeia final:
  `geometria difícil → decomposição → problemas simétricos → superposição`.
- Estado final: cadeia centralizada; pausa antes do CTA/encerramento da série.

---

## Mapa de retenção (avanço a cada 30–60 s)

pergunta (N01) → conflito (N03) → mudança de perspectiva (N04) → ferramenta (N05) → mapa vetorial (N06–N07) → resultado (N09) → P móvel (N10) → explicação física (N11) → nova pergunta (N12) → generalização (N14) → limites (N15) → checagens/estratégia (N16).

---

## Direção visual V3 (preview silencioso, 2026-10-13) — substitui a seção V2 e as janelas antigas acima

Janelas de planejamento (referência 14:15): N01 0:00–0:35 · N02 –0:45 · N03 –1:50 · N04 –2:35 · N05 –4:45 · N06 –5:40 · N07 –6:55 · N08 –7:45 · N09 –8:35 · N10 –9:30 · N11 –10:15 · N12 –11:20 · N13 –12:05 · N14 –13:10 · N15 –13:40 · N16 –14:15. A fala está em `narracao.md` (V3); os trechos "fala" das tabelas anteriores valem só como histórico.

- **Rótulos:** tipografia matemática normal, sem contorno, sombra ou negrito; afastados de linhas e pontas; sinais de carga ausentes nas figuras vetoriais.
- **Vista com zoom (N07–N11, N14):** a figura dos objetos conserva identidade e é ampliada (esferas recuadas); P é um ponto cheio rotulado; o **anel** é o marcador de percurso e nunca é P.
- **N01–N04:** P definido como "o lugar onde calculamos o campo"; condição para tirar E da integral; uma gaussiana que muda de centro e raio com campo real e pontos A e B; decomposição com ρ₁, ρ₂ ↔ E⃗₁, E⃗₂.
- **N05 (≈ 2:10):** esfera com equador 2.5D → ρ = Q/V e [ρ] → P e gaussiana imaginária (R × r) → V_env → Q_env → fluxo com n̂ → Gauss, substituição e cancelamentos (`\cancel`) → E = ρr/3ε₀ → r → 2r (×8, ×4, ×2) → r̂ unitário, r r̂ = r⃗ → C → E⃗ = C r⃗.
- **N06:** legenda compacta construída uma linha por vez (O₊, O₋, d⃗, P, r⃗₊, r⃗₋) com o elemento correspondente; anatomia (início, ponta).
- **N07:** zoom; marcador percorre O₊→P e O₊→O₋→P; soma ponta com cauda; vetor oposto por rotação da cópia de r⃗₋; O₊→P→O₋ = d⃗.
- **N08–N09:** distância × intensidade (escalas distintas); campos ancorados em P com guias; C = ρ/3ε₀ (abreviação); soma por cópia deslizante; fatoração; ρ_tot = 0 na lente.
- **N10–N11:** primeira passagem com parciais, segunda só com a resultante, setas totais iguais na lente; Δ = depois − antes, ΔP = Δr⃗₊ = Δr⃗₋, CΔr⃗₊ e −CΔr⃗₋ se cancelam.
- **N12:** segundo problema; esfera com buraco → pergunta → esfera cheia + fictícia tracejada → densidades fora/dentro → pares +ρ/−ρ se cancelam → miniaturas.
- **N13–N14:** R, a, d⃗ (um por vez); |d⃗| + a comparado a R na mesma direção; a varia; r⃗ e r⃗′ (apóstrofo = outra origem); mesma gramática de N07; P percorre a cavidade; d⃗ muda de direção e E⃗ acompanha.
- **N15–N16:** |d⃗| cresce e E⃗ cresce; hipóteses do resultado uniforme; outro formato "sem garantia"; checagens uma por vez (d⃗ = 0, troca de sinal, unidades); síntese com os próprios objetos.
- **Ritmo:** esperas até cada marco limitadas a 6 s; nenhum trecho parado ≥ 8 s no preview.

---

## Direção visual V4 (2026-10-13) — composição, textos de tela e álgebra

- **Áreas fixas:** título/pergunta na faixa superior (abaixo da marca); geometria à esquerda (≈55%); legenda compacta no canto superior direito (uma definição por vez, a ativa em destaque); álgebra no slot central da coluna direita (o resultado substitui o desenvolvimento); observação curta abaixo da equação.
- **Zoom (N07–N11, N14):** contornos das distribuições recuados (N07–N11) ou retirados antes de entrar na coluna de leitura; ícone do par de esferas no canto da geometria preserva o vínculo com o problema original. Nenhuma fórmula ou frase sobre contornos.
- **Rótulos:** tipografia matemática normal, sem contorno; símbolos na tela (ρ, O₊, O₋, r⃗, r⃗′, E⃗); grafias de pronúncia só na voz; frases com inicial maiúscula.
- **Transições:** texto que sai e texto que entra no mesmo lugar não se sobrepõem (saída antes da entrada).
- **Glyph maps (MF-Tools `TransformByGlyphMap`):** N05 — cancelamento de 4πr² (mostrando o r restante), r·r̂ → r⃗, ρ/(3ε₀) → C; N09 — C r⃗₊ − C r⃗₋ → C(r⃗₊ − r⃗₋), grupo (r⃗₊ − r⃗₋) → d⃗, C → ρ/(3ε₀); N14 — C r⃗ − C r⃗′ → C(r⃗ − r⃗′) → C d⃗.
- **N10:** três passagens (posições; contribuições; resultante), cada uma com sua legenda e sem rótulos móveis além de P.
