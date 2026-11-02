# yt_0018 — roteiro com narração v2.2

> v2.2 (2026-10-30, handoff v4 §9): sem citar outro vídeo e sem prometer dois vídeos seguidos. Trocas no A2, X0-3, X3-8, X5-8 e EP2; tag do X5-5 vira `[emphatic]`. O texto com as tags para gravação está em `narracao_tags_v1.md`.

> v2.1 (2026-10-30, handoff v3 §8): nunca citar outro vídeo como já existente (a ordem de publicação pode mudar). Trocas só no A2, X0-1, X4-5 e EN2; na tela, o X0-1 perde o selo DESAFIO DO VÍDEO ANTERIOR e o EN2 mostra O FOGUETE (ciano) embaixo da pergunta.

> v2 (2026-10-30, depois do preview v1): o rojão saiu (repetia o hook, o T2-7/T2-8 e o T3 do yt_0017) e entrou **a balança da máquina de Atwood** (M A⃗_cm = F⃗_ext usado ao contrário). O gafanhoto fecha no próprio problema (X3-10; sem S1). Os dados nascem no desenho, sincronizados com a fala. Hook e X3 viram cena Three.js. Fonte do `ancoras.json` (`gerar_ancoras.py`): cada `###` é uma âncora; a fala começa ~0,15 s depois da linha `tela:` e manda. Tags `[ ]` não entram na contagem nem na legenda. Texto integral do handoff v2 (Anexo A); a v1 só existe no handoff v1 (as âncoras v1 estão em `_v1/ancoras_v1.json`).

---

## HOOK

### H1 — tela: Three.js, lago à noite; câmera baixa, quase rente à água, aproximando; folha de verdade boiando; gafanhoto detalhado na ponta, olhando para a outra ponta; a cota L = 30 cm nasce ao longo da folha em "trinta centímetros"
[curious] Olha esse gafanhoto, parado na ponta de uma folha que boia num lago. Ele quer pular para a outra ponta, que está a só trinta centímetros dele.

### H2 — tela: ele agacha, estica as pernas e salta a ~30°; a folha recua e deixa esteira; rastro violeta fino com 4–5 poses fantasma; cai na água (respingo e anéis); replay 0,5× de lado com a posição inicial da folha em tracejado
Ele salta… e passa direto. Cai na água, bem longe da folha. Agora, olha de novo o instante do salto, em câmera lenta. Repara que a folha não fica parada: ela escorrega para trás.

### H3 — tela: congela com o gafanhoto no ar sobre a água e a folha deslocada; pergunta EM QUE ÂNGULO ELE PRECISA PULAR PARA CAIR DE VOLTA NA FOLHA?, acima da cena
[curious] Então, em que ângulo ele precisa pular para cair de volta na folha? Parece que falta informação. Mas o centro de massa resolve isso, e mais cinco problemas que parecem impossíveis.

## ABERTURA

### A1 — tela: logo; BEM-VINDOS AO PARALLAX LAB
[happy] Fala, pessoal! Bem-vindos ao Parallax Lab!

### A2 — tela: CENTRO DE MASSA · 6 PROBLEMAS QUE PARECEM IMPOSSÍVEIS; NESTE VÍDEO: cinco ícones (TIRAR MASSA · MONTAR POR PARTES · ⊕ PARADO, DOIS REFERENCIAIS · REFERENCIAL DO CM · ⊕ ACELERA → FORÇA EXTERNA)
[thoughtful] Hoje é dia de problema difícil de centro de massa. Seis deles, e cada um pede uma ferramenta diferente da teoria.

### A3 — tela: os ícones viram uma faixa no rodapé; PALCO: a granada do yt_0017 pequena, com o ⊕ seguindo a parábola; CONTA: R⃗_cm = Σ mᵢ r⃗ᵢ / M e M A⃗_cm = F⃗_ext acendendo token a token com a fala
Lembrando: o centro de massa é a média das posições, pesada pelas massas. E ele se move como uma partícula com toda a massa do sistema, empurrada só pelas forças de fora. Se não tem força externa e tudo começa parado, ele não sai do lugar. É só isso que a gente vai usar hoje, do jeito certo.

### A4 — tela: três perguntas entram uma a uma como checklist; o checklist sai de cena (nos problemas, só a pergunta que decide aparece como chip, ~4 s)
[thoughtful] E antes de qualquer conta, três perguntas. Qual é o sistema? Tem força externa, e em que direção? E de qual referencial eu estou olhando? Em quase todo problema difícil de centro de massa, o difícil é responder bem essas três. A conta que vem depois é curta.

## X0 — O DISCO FURADO (RESPOSTA DO DESAFIO)

### X0-1 — tela: PROBLEMA 1 · O DISCO FURADO; a miniatura do disco (nascida no fim do A4) cresce até o disco; nascem R = 1 m, r = 0,5 m (dentro do furo) e a cota 0,25 m abaixo do eixo; selo O QUE ESTE PEDE: TIRAR MASSA
[curious] Primeiro, um clássico: o disco com um furo fora do centro. Onde fica o centro de massa?

### X0-2 — tela: o furo se preenche (massa 1 em 0) e reaparece como fantasma MASSA −¼ em +0,25; CONTA: A_furo = ¼ A_disco; X = (1·0 + (−¼)·0,25)/(1 − ¼) → (−1/16)/(¾) → −1/12 m ≈ −8,3 cm; ⊕ em −8,3 cm
[thoughtful] O raio do furo é metade do raio do disco, então a área dele é um quarto. A gente conta o disco inteiro, com o centro de massa no centro, e soma o furo com massa negativa: menos um quarto, sentado a vinte e cinco centímetros. Dá menos um doze avos de metro, uns oito centímetros e pouco, do lado oposto ao furo. E atenção: ninguém tem massa negativa. É só a conta de tirar um material que não está lá.

### X0-3 — tela: CONFERE: o furo desliza até o centro e o ⊕ volta para 0; DICA: O CENTRO DE MASSA FOGE DO FURO
Confere: se o furo estivesse no meio, o centro de massa ficaria no meio, e a conta dá zero mesmo. E a dica: o centro de massa foge do furo.

## X1 — A PLACA QUADRADA COM FURO

### X1-1 — tela: PROBLEMA 2 · A PLACA COM FURO; placa de 40 cm, furo r = 10 cm em (8; 8) cm; cotas nascem uma por vez, fora da placa; O QUE ESTE PEDE: TIRAR MASSA + SIMETRIA; HIPÓTESE: ESPESSURA UNIFORME → MASSA ∝ ÁREA
[curious] Agora em duas dimensões. Uma placa quadrada, com um furo redondo fora do centro, deslocado na diagonal. A placa tem espessura uniforme, então a massa de cada pedaço é proporcional à área dele.

### X1-2 — tela: a diagonal y = x acende; a placa reflete em torno dela; CONTA: SIMETRIA → X = Y
[thoughtful] Antes de qualquer conta, procura a simetria. A diagonal que passa pelo centro da placa e pelo centro do furo divide tudo em duas metades iguais, espelhadas. Então o centro de massa está nessa diagonal, e as duas coordenadas são iguais. Basta calcular uma.

### X1-3 — tela: o furo vira fantasma MASSA ∝ −100π, a placa MASSA ∝ 1600; CONTA: A□ = 40² = 1600 cm², A○ = π·10² = 100π ≈ 314 cm² → X = (1600·0 + (−100π)·8)/(1600 − 100π) → −2513/1286 → X = Y ≈ −1,95 cm; ⊕ em (−1,95; −1,95); d = √2·1,95 ≈ 2,76 cm
De novo, placa inteira mais furo com massa negativa. A placa tem mil e seiscentos centímetros quadrados, com o centro de massa no meio. O furo tem cem pi, uns trezentos e catorze centímetros quadrados, com o centro oito centímetros para a direita e oito para cima. Fazendo a conta, a coordenada horizontal dá menos um vírgula noventa e cinco centímetros. E a vertical é igual, pela simetria. O centro de massa fica a quase três centímetros do centro, na diagonal, do lado oposto ao furo.

### X1-4 — tela: CONFERE: o furo encolhe até 0 e o ⊕ volta ao centro; DICA: ACHE A SIMETRIA PRIMEIRO: ELA CORTA A CONTA PELA METADE E JÁ DÁ O SINAL
[thoughtful] Confere: se o furo encolhe até sumir, o centro de massa volta para o meio. E repara por que aqui ele andou pouco: o furo tira só um quinto da placa, e ainda está perto do centro. E a dica: procura a simetria antes de calcular. Ela corta a conta pela metade e ainda diz para que lado a resposta vai.

## X2 — O FIO NAS ARESTAS DO CUBO

### X2-1 — tela: PROBLEMA 3 · O FIO NO CUBO; Three.js: cubo de 1 m em arame fantasma girando; o fio se desenha aresta a aresta com "comprimento", "largura", "altura"; a cota 1 m nasce na primeira aresta; O QUE ESTE PEDE: MONTAR POR PARTES; HIPÓTESE: FIO UNIFORME → MASSA ∝ COMPRIMENTO
[curious] Agora em três dimensões. Um fio uniforme, dobrado ao longo de três arestas seguidas de um cubo de um metro: primeiro no comprimento, depois na largura, depois na altura. Onde fica o centro de massa desse fio?

### X2-2 — tela: o cubo para numa vista fixa; cada aresta acende e encolhe até uma partícula M/3 no ponto médio; CONTA: CADA ARESTA → M/3 NO MEIO DELA
[thoughtful] A ferramenta aqui é a de montar por partes. Cada aresta é um pedaço reto e uniforme, então, por simetria, o centro de massa de cada uma está no meio dela. E cada pedaço tem um terço da massa. Então a gente troca o fio por três partículas iguais, uma no meio de cada aresta.

### X2-3 — tela: projeções em cada eixo; X = (½ + 1 + 1)/3 = 5/6 m · Y = ½ m · Z = 1/6 m; o ⊕ nasce em (5/6; ½; 1/6) m
Como as três massas são iguais, cada coordenada do centro de massa é uma média simples, e cada uma é uma conta de uma dimensão só. Na direção do comprimento: meio, um e um, média cinco sextos de metro. Na largura: zero, meio e um, média meio metro. Na altura: zero, zero e meio, média um sexto de metro.

### X2-3b — tela: MÉDIA DOS 4 CANTOS = (3/4; 1/2; 1/4) riscada em laranja; ponto fantasma laranja; PEGADINHA: A MASSA ESTÁ NAS ARESTAS, NÃO NOS CANTOS
[curious] E cuidado com uma pegadinha. Muita gente pega os quatro cantos do fio e tira a média. Dá três quartos, meio e um quarto, que é outro ponto. Está errado, porque a massa não está nos cantos: está espalhada ao longo das arestas. Quem representa cada pedaço é o meio dele, não as pontas.

### X2-4 — tela: o cubo volta a girar; o ⊕ dentro do cubo, fora do fio; cota √2/6 ≈ 24 cm; CONFERE: AS TRÊS COORDENADAS ENTRE 0 E 1 → DENTRO DO CUBO; DICA: EM 3D, CADA COORDENADA É UMA CONTA DE UMA DIMENSÃO
[curious] E olha onde ele foi parar: dentro do cubo, no ar, a uns vinte e quatro centímetros do pedaço de fio mais próximo. O centro de massa não precisa estar em cima do material. Confere: as três coordenadas estão entre zero e um, então ele está dentro do cubo. E a dica: em três dimensões, separa as coordenadas. Cada uma é um problema de uma dimensão.

## X3 — O GAFANHOTO NA FOLHA (RESPOSTA DO HOOK)

### X3-1 — tela: PROBLEMA 4 · O GAFANHOTO; o lago em Three.js de lado, folha ~60% do ESQUEMA; nascem m = 1 g, M = 4 g, L = 30 cm, v = 4 m/s EM RELAÇÃO À ÁGUA e o arco de θ; O QUE ESTE PEDE: ⊕ PARADO, DOIS REFERENCIAIS; HIPÓTESES: ÁGUA SEM RESISTÊNCIA HORIZONTAL · FOLHA RÍGIDA · DECOLAGEM RÁPIDA
[curious] Agora, a resposta do começo. A folha tem quatro vezes a massa do gafanhoto. Ele salta a quatro metros por segundo, e repara: essa velocidade é em relação à água, não em relação à folha. E a gente supõe que a água não segura a folha na horizontal, que a folha é rígida, e que a decolagem é rápida.

### X3-2 — tela: pesos e EMPUXO (FC); nenhuma seta horizontal; SÓ A COMPONENTE HORIZONTAL SE CONSERVA; CONTA: F_ext,x = 0 → P_x = 0
[thoughtful] Primeiro, que momento se conserva? Na vertical, tem força externa: os pesos e o empuxo da água, que segura a folha quando ele empurra para baixo. Então o momento vertical não se conserva. Mas na horizontal, nenhuma força de fora. Por isso, só a componente horizontal do momento total fica igual a zero do começo ao fim.

### X3-3 — tela: componentes da velocidade; V da folha para a esquerda; momentos iguais e opostos; CONTA: m v cos θ = M V → V = (m/M) v cos θ = v cos θ / 4
Então, se o gafanhoto ganha momento horizontal para a frente, a folha ganha o mesmo momento para trás. A massa do gafanhoto vezes a parte horizontal da velocidade dele é igual à massa da folha vezes a velocidade da folha. Como a folha tem quatro vezes a massa, ela recua com um quarto da velocidade horizontal do gafanhoto.

### X3-4 — tela: a parábola do salto aparece fina; CONTA: T = 2 v sen θ / g (2 v sen θ sai da componente vertical; g da seta g)
[thoughtful] E quanto tempo ele fica no ar? Isso só depende da parte vertical da velocidade: o tempo de voo é duas vezes a parte vertical da velocidade, dividido pela aceleração da gravidade. É o mesmo de qualquer lançamento.

### X3-5 — tela: duas réguas (água e folha); VISTO DA ÁGUA → VISTO DA FOLHA; CONTA: v_rel = v cos θ + V = 1,25 v cos θ
[curious] Só que a pergunta é sobre a folha, e a folha está andando. Então troca de régua. Vista da água, o gafanhoto vai para a frente e a folha para trás. Agora, vista da folha, as duas coisas se somam: em relação à folha, o gafanhoto anda com a parte horizontal da velocidade dele mais a velocidade de recuo da folha. Ou seja, um vírgula vinte e cinco vezes a parte horizontal da velocidade.

### X3-5b — tela: o ⊕ do sistema sobe e desce na linha vertical, sem sair dela; CONTA: m Δx_g + M Δx_f = 0 → Δx_f = −Δx_g/4 → Δx_rel = 1,25 Δx_g; miniatura do remador
[thoughtful] Dá para ver isso também pelo centro de massa do sistema, gafanhoto mais folha. Ele sobe e desce durante o voo, porque na vertical tem força externa. Mas ele nunca sai dessa linha vertical. Então a massa do gafanhoto vezes o deslocamento dele, mais a massa da folha vezes o dela, dá zero. A folha anda para trás um quarto do que o gafanhoto anda para a frente, e, em relação à folha, ele anda um vírgula vinte e cinco vezes mais. É o mesmo um vírgula vinte e cinco, por outro caminho.

### X3-6 — tela: CONTA: Δx_rel = 1,25 v cos θ · 2 v sen θ / g → 1,25 v² sen 2θ / g → 2,04 sen 2θ ≤ 0,30 → sen 2θ ≤ 0,147 → 2θ ≤ 8,45° ou 2θ ≥ 171,55° → 0° < θ ≤ 4,23° ou 85,77° ≤ θ < 90°
[thoughtful] Multiplicando essa velocidade relativa pelo tempo de voo, sai o quanto ele anda em relação à folha. E aparece o seno do dobro do ângulo. Com os números, dá dois vírgula zero quatro metros vezes o seno do dobro do ângulo, e isso não pode passar dos trinta centímetros da folha. Então o seno do dobro do ângulo tem que ser no máximo zero vírgula um quatro sete. [short pause] E aí vem a surpresa: dá duas faixas. Ou ele pula quase rasante, com no máximo quatro vírgula dois graus, ou quase na vertical, com pelo menos oitenta e cinco vírgula oito graus.

### X3-7 — tela: os dois saltos-limite (rasante com inset AMPLIADO ×20; quase vertical com a câmera recuando); réguas: 24 cm e 6 cm; CONFERE: 24 + 6 = 30 cm
[excited] Olha os dois saltos-limite. No rasante, ele voa seis centésimos de segundo, a quatro milímetros da folha. No quase vertical, sobe oitenta centímetros e fica oito décimos de segundo no ar. E os dois terminam no mesmo lugar: a ponta oposta da folha. Confere nas réguas: em relação à água, ele anda vinte e quatro centímetros e a folha recua seis. Vinte e quatro mais seis, os trinta da folha.

### X3-8 — tela: CONFERE: folha pesadíssima → 1,25 vira 1; miniatura do remador; DICA: ÂNGULOS COMPLEMENTARES DÃO O MESMO ALCANCE. AQUI ISSO VIRA A RESPOSTA
[thoughtful] Mais uma conferência: se a folha fosse pesadíssima, o recuo sumiria, o um vírgula vinte e cinco viraria um, e voltaria o alcance de qualquer lançamento. E repara que é o mesmo problema do remador na canoa, só que voando. A dica: ângulos complementares dão o mesmo alcance, e aqui isso vira a resposta.

### X3-9 — tela: só a régua da folha; u = 4 m/s EM RELAÇÃO À FOLHA; painel: u² sen 2θ / g ≤ 0,30 → sen 2θ ≤ 0,184 → θ ≤ 5,29° ou θ ≥ 84,71°; O REFERENCIAL DO ENUNCIADO MUDA A RESPOSTA
[curious] E repara como o enunciado importa. Se os quatro metros por segundo fossem em relação à folha, o recuo já estaria embutido, o fator um vírgula vinte e cinco sumiria, e o ângulo rasante máximo subiria para uns cinco vírgula três graus. Mesmo gafanhoto, outra resposta. Por isso a primeira coisa é perguntar: velocidade em relação a quê?

### X3-10 — tela: as duas trajetórias-limite juntas sobre a folha e o transferidor com as faixas 0°–4,23° e 85,77°–90°; o gafanhoto pousa na ponta da folha; fecho do gafanhoto
[calm] E a pergunta do começo está respondida: só o salto quase rasante, ou quase na vertical, cai de volta na folha. Qualquer coisa no meio passa direto, porque a folha foge dele.

## X4 — AS NAVES QUE SE SEPARAM

### X4-1 — tela: PROBLEMA 5 · AS NAVES; naves acopladas; nascem 1.000 kg, 2.000 kg e 3.000 J (ciano) na carga; ⊕ a 1/3 da maior; O QUE ESTE PEDE: REFERENCIAL DO CENTRO DE MASSA → HIPÓTESES: SEM FORÇA EXTERNA · PARADAS NO REFERENCIAL DO CM
[curious] Agora, no espaço. Duas naves acopladas, uma de mil quilos e outra com o dobro da massa, dois mil, paradas no referencial do centro de massa. Entre elas, uma carga que, ao disparar, dá energia cinética ao conjunto: três mil joules. Com que velocidade cada uma sai?

### X4-2 — tela: a carga dispara; as naves se afastam, o ⊕ fica; momentos iguais e opostos; CONTA: P = 0 → p⃗₁ + p⃗₂ = 0⃗ → |p₁| = |p₂| = p
[thoughtful] Primeiro, o momento. O momento total era zero, e a carga é interna. Então, depois, os momentos das duas naves têm que ser iguais e opostos. Mesmo tamanho, sentidos contrários. E o centro de massa continua parado.

### X4-3 — tela: barras ciano com alturas diferentes (a da leve com o dobro); SE OS MOMENTOS SÃO IGUAIS, POR QUE AS ENERGIAS NÃO SÃO?
[curious] Só que olha as energias: elas não saem iguais. Se os momentos são iguais, por que as energias não são?

### X4-4 — tela: K = ½mv² → K = p²/2m (linha nova, glyph map) → p²/2·1000 + p²/2·2000 = 3000 → p² · 3/4000 = 3000 → p = 2000 kg·m/s → v₁ = 2 m/s, v₂ = 1 m/s; K₁ = 2000 J, K₂ = 1000 J; SE AFASTAM A 3 m/s
[thoughtful] Porque a energia cinética escrita com o momento é o momento ao quadrado, dividido por duas vezes a massa. Com o mesmo momento, quem tem menos massa leva mais energia. Somando as duas e igualando a três mil joules, o momento de cada uma dá dois mil quilogramas metro por segundo. Então a nave leve sai a dois metros por segundo e a pesada a um. Elas se afastam a três metros por segundo. E a energia fica dividida: dois mil joules para a leve e mil para a pesada.

### X4-5 — tela: CONFERE: massas iguais → barras iguais; nave muito pesada (→ ∞) → a outra leva quase tudo; DICA; painel VISTO DE UMA NAVE-MÃE A −10 m/s: 150.000 J → 153.000 J; diferença 3.000 J
Confere: com massas iguais, seria meio a meio; com uma nave pesadíssima, a outra levaria quase tudo. A dica: no referencial do centro de massa, a energia se divide na razão inversa das massas. Mas o total que a carga libera não depende de onde você olha. Imagina que as naves já viajassem juntas a dez metros por segundo. Antes, cento e cinquenta mil joules. Depois, a leve sai a doze e a pesada a nove, e a soma dá cento e cinquenta e três mil. A diferença continua sendo três mil joules: é a parte relativa, e essa nenhum referencial muda.

## X5 — A BALANÇA QUE MARCA MENOS

### X5-1 — tela: PROBLEMA 6 · A BALANÇA; balança de plataforma com mostrador; suporte em ∏ com polia; blocos travados; nascem 2 kg, 3 kg, 1 kg; o mostrador acende em 6,0 kg; O QUE ESTE PEDE: ⊕ ACELERA → FORÇA EXTERNA
[curious] Último problema. Uma balança, um suporte de dois quilos com uma polia, e dois blocos, de três e de um quilo, pendurados por um fio, travados. Parada, ela marca a soma de tudo: seis quilos. Agora a gente solta a trava.

### X5-2 — tela: a trava se abre; 3 kg desce, 1 kg sobe; no mesmo quadro o mostrador cai de 6,0 para 5,0 kg e pisca; POR QUE A BALANÇA MARCA MENOS?
[curious] Os blocos começam a se mover, mas nenhuma massa saiu de cima da balança. E mesmo assim ela passa a marcar cinco quilos. Por quê?

### X5-3 — tela: HIPÓTESES: FIO E POLIA IDEAIS · BALANÇA MEDE A FORÇA QUE FAZ PARA CIMA; fronteira do sistema; fio e trações em cinza INTERNA; M g⃗ no ⊕ e N⃗ na base (FC); CONTA: N − M g = M A_cm
[thoughtful] Primeiro, qual é o sistema? Tudo que está em cima da balança: suporte, polia, fio e os dois blocos. O fio puxa os blocos e a polia, mas isso é força interna. De fora, só duas: o peso de tudo, para baixo, e a força da balança, para cima. Então a força da balança menos o peso é a massa total vezes a aceleração do centro de massa.

### X5-4 — tela: peso e tração em cada bloco; CONTA: 3 g − T = 3 a e T − 1 g = 1 a → somando, T e −T riscam → (3 − 1) g = (3 + 1) a → a = g/2 = 4,9 m/s²
[thoughtful] Mas quanto acelera esse centro de massa? Antes, a aceleração dos blocos. No bloco pesado, o peso menos a tração; no leve, a tração menos o peso. Somando as duas, a tração some, como toda força interna. Sobra a diferença dos pesos acelerando as duas massas juntas: metade da aceleração da gravidade, quatro vírgula nove metros por segundo ao quadrado.

### X5-5 — tela: o ⊕ do sistema desce acelerando, com estroboscopia a cada 0,25 s; o suporte não se mexe; CONTA: 6 A_cm = 3·(−4,9) + 1·(+4,9) + 2·0 → A_cm = −1,63 m/s²
[emphatic] Agora repara no centro de massa. O suporte fica parado. O bloco pesado desce e o leve sobe, com a mesma aceleração. Só que o pesado conta mais na média: o centro de massa do sistema desce, acelerando. Um vírgula sessenta e três metros por segundo ao quadrado, para baixo.

### X5-6 — tela: CONTA: N = M (g + A_cm) → 6·(9,8 − 1,63) → 49 N → 5,0 kg; o 5,0 desce até o mostrador; caixa N = 49 N
[excited] E aí sai a balança. A força dela é o peso total menos a massa vezes essa aceleração para baixo: quarenta e nove newtons. A balança mostra isso como cinco quilos. Um quilo a menos, sem nenhuma massa ir embora, só porque o centro de massa está acelerando para baixo.

### X5-7 — tela: CONFERE em três linhas: pela tração (T = 14,7 N; 2T = 29,4 N; N = 2·9,8 + 29,4 = 49 N); massas iguais → 6,0 kg; bloco leve → 0 → 2,0 kg
[thoughtful] Confere por outro caminho: a tração no fio dá catorze vírgula sete newtons, a polia é puxada para baixo pelos dois lados do fio, e a balança tem que segurar o suporte mais essas duas trações. Quarenta e nove newtons de novo. E os casos-limite: com blocos iguais, nada acelera, e a balança volta aos seis quilos. Se o bloco leve fosse sumindo, o pesado cairia livre, e a balança marcaria só o suporte.

### X5-8 — tela: miniatura do cavalo puxando a pedra e de uma pessoa num elevador descendo; DICA: SE O CENTRO DE MASSA ACELERA PARA BAIXO, O APOIO EMPURRA MENOS
[thoughtful] A dica: quem está de fora só enxerga o centro de massa. Se ele acelera para baixo, o apoio empurra menos; se acelera para cima, empurra mais. É o mesmo do elevador, e do cavalo puxando a pedra: a força externa sai da aceleração do centro de massa, sem precisar olhar para dentro.

## EPÍLOGO — A LUZ TAMBÉM EMPURRA

### EP1 — tela: caixa longa no espaço; ⊕ no meio com linha tracejada; pulso de luz da parede esquerda à direita; a caixa recua (FORA DE ESCALA); seta E/c
[curious] Uma última ideia, para levar para casa. Uma caixa parada no espaço. De uma parede, sai um pulso de luz, que atravessa a caixa e é absorvido na outra parede. Só que a luz carrega momento. Então, quando ela sai, a caixa recua, e quando ela chega do outro lado, a caixa para.

### EP2 — tela: a caixa parou à esquerda; a linha do ⊕ antigo pisca; O QUE ATRAVESSOU A CAIXA PARA O CENTRO DE MASSA NÃO ANDAR?; m = E/c² com PISTA, NÃO DEMONSTRAÇÃO
[thoughtful] Mas só houve forças internas, então o centro de massa não podia ter andado. A caixa foi para a esquerda… o que foi para a direita? Einstein fez exatamente essa pergunta, em mil novecentos e seis, e a resposta exige que a própria energia carregue inércia. Isso não é uma demonstração: é uma pista, e a porta de entrada da relatividade.

## SÍNTESE

### S2 — tela: o checklist volta ao centro por 2 s e sobe; cinco cartões (TIRAR MASSA · MONTAR POR PARTES · ⊕ PARADO, DOIS REFERENCIAIS · NO REFERENCIAL DO CM · ⊕ ACELERA → FORÇA EXTERNA)
[calm] Resumindo as ferramentas. Um buraco é massa negativa. Um corpo complicado vira algumas partículas, uma no centro de massa de cada pedaço. Sem força externa, o centro de massa fica parado, e aí vale trocar de régua. No referencial do centro de massa, os momentos se cancelam e a energia que sobra é a relativa. E, quando o centro de massa acelera, ele entrega a força externa. E as três perguntas do começo valem para qualquer um: qual é o sistema, tem força externa e em que direção, e de qual referencial eu olho. Em todos os seis, o mais difícil sumiu quando a gente escolheu bem o sistema e o referencial.

## ENCERRAMENTO

### EN1 — tela: logo com anéis; INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS
Se esses problemas mudaram o jeito como você enxerga o centro de massa, se inscreve no Parallax Lab para acompanhar os próximos vídeos.

### EN2 — tela: Three.js: foguete cuspindo gás; ⊕ do conjunto reto a velocidade constante; COMO ACELERAR SEM TER NADA PARA EMPURRAR?; O FOGUETE (ciano), embaixo da pergunta
[curious] E até aqui, a massa de cada corpo nunca mudou. E quando ela muda? Um foguete no espaço acelera sem ter nada para empurrar. Esse problema pede um vídeo só dele: o foguete. Até a próxima!

---

**Palavras faladas:** ~2530 (≈ 16 min a 2,7 palavras/s).

## Números de conferência (g = 9,8 m/s²)

| Bloco | Valor | Exato |
|---|---|---|
| X0 | X = −1/12 m ≈ −8,3 cm | −0,08333 |
| X1 | X = Y = −1,95 cm; 2,76 cm | −1,9546; 2,7642 |
| X2 | (5/6; 1/2; 1/6) m; 24 cm | 0,2357 |
| X3 | 2,04 sen 2θ ≤ 0,30; θ ≤ 4,23° ou ≥ 85,77° | 2,0408; 4,2266° |
| X3 limites | 0,060 s / 0,814 s; 4,4 mm / 81 cm; 24 cm e 6 cm | 0,0602; 0,8141; 0,00443; 0,8119 |
| X3-9 | θ ≤ 5,29° ou ≥ 84,71° | 0,18375 |
| X4 | p = 2.000 kg·m/s; 2 e 1 m/s; 2.000 J e 1.000 J | ✓ |
| X4-5 | 150.000 J → 153.000 J | ✓ |
| X5 | a = 4,9 m/s²; A_cm = −1,633 m/s²; N = 49,0 N → 5,0 kg; T = 14,7 N | ✓ |
