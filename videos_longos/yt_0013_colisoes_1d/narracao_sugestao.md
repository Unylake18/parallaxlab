# COLISÕES EM 1D — sugestão de narração (v2.1, sobre o preview v6)

Fonte da cena: `cena.py` v6 (preview `renders/v6/yt_0013_v6_preview_960x540_15fps.mp4`). Padrão: `docs/padrao_video_longo.md` §5 e
`docs/roteiro_voz_elevenlabs_v4.md`. Professor de cursinho, conversado, "a gente"/"você", nunca a letra solta.

**Como ler:** cada `###` é uma **âncora** (evento visual). A linha `tela:` diz o que aparece; a fala que vem embaixo começa ~0,15 s
depois desse evento. A fala manda: nada aqui deve ser cortado para caber na animação. Na sincronização, a cena acompanha a voz por
**retiming das próprias animações, revelações progressivas e pausas curtas**; `hold` só onde a tela já tem algo para ler ou contemplar
(marcado **(segurar)**), nunca um quadro congelado enquanto a voz explica.

**Notação falada** (definida na tela em C01 e no pêndulo): velocidade inicial do corpo um / do corpo dois (v₁ᵢ, v₂ᵢ); velocidade final do
corpo um / do corpo dois (v₁f, v₂f); velocidade final comum (v_f); no pêndulo, velocidade inicial do projétil (vᵢ) e velocidade do
conjunto (V_t). Momento = "momento linear" ou "quantidade de movimento" na primeira vez; depois só "momento".

---

## HOOK

### H1 — tela: dois blocos no trilho, mesma situação inicial; colidem e REBATEM
Olha essa colisão. Dois blocos num trilho, um vindo de cada lado. Eles batem... e rebatem.

### H2 — tela: reset, mesmo começo; SE SEPARAM
Agora o mesmo começo: as mesmas massas, as mesmas velocidades. E dessa vez eles se separam de outro jeito.

### H3 — tela: reset; FICAM JUNTOS
Mais uma vez: mesmas massas, mesmas velocidades iniciais... e agora eles grudam e seguem juntos.

### H4 — tela: três miniaturas; MESMO COMEÇO. TRÊS FINAIS. POR QUÊ?
Mesmo começo, três finais completamente diferentes. Por quê? É isso que a gente vai responder hoje.

## ABERTURA

### A1 — tela: logo; BEM-VINDOS AO PARALLAX LAB
Fala, pessoal! Bem-vindos ao Parallax Lab!

### A2 — tela: COLISÕES EM 1D · NESTE VÍDEO: COMO SABER O QUE ACONTECE DEPOIS
Vamos para a mecânica, começando por colisões em uma dimensão. A ideia é sair daqui sabendo, diante de qualquer colisão, o que você precisa saber para prever o que acontece depois.

## C01 — MOMENTO LINEAR

### C01-1 — tela: um bloco com a seta de velocidade (violeta) e a seta de momento (magenta); p⃗ = m v⃗ no painel
Primeiro, uma ferramenta. O momento linear, que também aparece como quantidade de movimento, é a massa vezes a velocidade. Por isso o momento aponta para o mesmo lado que a velocidade: a massa é sempre positiva.

### C01-2 — tela: MAIS MASSA (o bloco cresce, o momento cresce)
Com a mesma velocidade, mais massa significa mais momento.

### C01-3 — tela: MAIS VELOCIDADE (a seta violeta cresce, o momento acompanha)
E com a mesma massa, mais velocidade também significa mais momento.

### C01-4 — tela: dois corpos, cada um com seu momento magenta embaixo
Agora voltamos aos nossos dois blocos. Cada um tem o seu momento: o momento do corpo um e o momento do corpo dois.

### C01-5 — tela: o eixo +x pisca; v₁ᵢ > 0 e v₂ᵢ < 0; selo DEFINA O EIXO · RESPEITE OS SINAIS
E aqui entra um detalhe que derruba muita gente em prova: o sinal. A gente combina que para a direita é positivo. Então a velocidade inicial do corpo um é positiva, e a velocidade inicial do corpo dois, que vem para a esquerda, é negativa. Defina o eixo antes de qualquer conta e respeite os sinais.

### C01-6 — tela: soma ponta com cauda; a seta do corpo dois começa onde termina a do corpo um; nasce o momento total
Para somar os momentos, a gente soma com sinal: a seta do corpo dois começa onde termina a do corpo um. O que sobra é o momento total do sistema.

### C01-7 — tela: ANTES (miniatura) e DEPOIS (com interrogações); definições v₁ᵢ, v₂ᵢ iniciais e v₁f, v₂f finais
Daqui para frente, uma convenção de nomes. O índice i quer dizer inicial, antes da colisão; o índice f quer dizer final, depois. Então temos a velocidade inicial e a velocidade final de cada corpo.

### C01-8 — tela: m₁v₁ᵢ + m₂v₂ᵢ = m₁v₁f + m₂v₂f, ligada ao ANTES e ao DEPOIS
Se o momento total se conserva na colisão, e a gente já vai ver por quê, o momento total antes é igual ao momento total depois.

### C01-9 — tela: caixas nas velocidades finais; 1 EQUAÇÃO. 2 INCÓGNITAS.
Só que repara: as massas e as velocidades iniciais a gente conhece. As incógnitas são as duas velocidades finais. Uma equação, duas incógnitas.

### C01-10 — tela: O QUE FALTA? (segurar)
Com uma equação só, não dá para achar duas coisas. Então... o que está faltando?

## C02 — MOMENTO E IMPULSO

### C02-1 — tela: Δp⃗ = J⃗ e J⃗ = ∫F⃗ dt no topo; blocos se aproximando; ANTES → CONTATO → DEPOIS
Antes de responder, vamos entender por que o momento total se conserva. Lembrando: a variação do momento de um corpo é o impulso que ele recebe, e o impulso é a força acumulada ao longo do tempo, a área sob o gráfico da força.

### C02-2 — tela: painel F × t (CASO: REBATEM) e painel com p₁, p₂ e P TOTAL
Em cima, a força de contato ao longo do tempo; embaixo, o momento de cada bloco e o total, no caso em que eles rebatem. A forma da curva é um esquema; o que importa é a área.

### C02-3 — tela: contato; setas de força (azul-claro) iguais e opostas; a área (impulso) se preenche; p₁ e p₂ mudam; P TOTAL parado
No contato, o bloco um empurra o bloco dois e o bloco dois empurra de volta: forças iguais e opostas, ação e reação. Enquanto a área cresce, o momento do corpo um diminui e o do corpo dois aumenta. Mas olha o total... não se mexe.

### C02-4 — tela: Δp₁ = −Δp₂ ; área = J
As variações de momento dos dois blocos são iguais em módulo e opostas: a variação do corpo um é menos a variação do corpo dois.

### C02-5 — tela: AS FORÇAS INTERNAS TROCAM MOMENTO. → O TOTAL NÃO MUDA.
As forças internas trocam momento entre os corpos... mas o total não muda.

### C02-6 — tela: os blocos se afastam (DEPOIS); contorno SISTEMA; selo ESCOLHA O SISTEMA
Por isso é tão importante escolher o sistema. Aqui, o sistema são os dois blocos juntos: as forças entre eles ficam do lado de dentro.

### C02-7 — tela: J_ext ≈ 0 ; ΔP ≈ 0
E as forças de fora? Atrito com o trilho, resistência do ar... Na direção do trilho, durante um contato tão curto, o impulso externo é desprezível. Então a variação do momento total nessa direção é praticamente zero.

### C02-8 — tela: MODELO IDEAL ; P_i = P_f em caixa magenta (segurar)
No modelo ideal, a gente toma esse impulso externo como zero. E aí sim escreve a igualdade: momento total inicial igual a momento total final.

## C03 — TIPOS DE COLISÃO

### C03-1 — tela: colisão 1 (rebatem) com o painel P TOTAL e K TOTAL
Agora vamos rever os três finais com dois medidores: o momento total e a energia cinética total. Lembrando que a energia cinética é meio vezes a massa vezes a velocidade ao quadrado, e nunca é negativa.

### C03-2 — tela: depois do contato; os dois medidores iguais; ELÁSTICA ; P_i = P_f ; K_i = K_f
No primeiro caso, o momento total fica igual, e a energia cinética total também. Isso tem nome: colisão elástica. Momento conservado e energia cinética conservada.

### C03-3 — tela: colisão 2 (se separam); K diminui; a parte laranja aparece: ENERGIA INTERNA
No segundo, o momento total continua o mesmo. Só que a energia cinética diminui. Para onde ela foi? Virou energia interna: deformação, aquecimento, vibração dos blocos. Ela não some; muda de forma.

### C03-4 — tela: INELÁSTICA ; P_i = P_f ; K_f < K_i
Essa é uma colisão inelástica: o momento se conserva e, nas colisões que estamos estudando, a energia cinética diminui.

### C03-5 — tela: colisão 3 (ficam juntos); K cai mais; COMPLETAMENTE INELÁSTICA ; v₁f = v₂f = v_f
E no terceiro, os blocos grudam. O momento continua conservado, e a energia cinética cai ainda mais. É a colisão completamente inelástica, e a marca dela é que os dois saem com a mesma velocidade final.

### C03-6 — tela: resumo das três; P_i = P_f NAS TRÊS; NÃO FECHA SOZINHA ao lado de K_f < K_i
Resumindo: o momento se conserva nas três. O que muda é a informação extra. Na elástica, a energia cinética se conserva: é uma segunda equação. Na que gruda, as velocidades finais são iguais: também é uma segunda equação. Mas repara na inelástica comum: dizer só que a energia diminuiu é uma desigualdade. Ela restringe, mas não fecha a conta sozinha. Aí o problema precisa dar algum dado a mais.

### C03-7 — tela: MOMENTO + TIPO DE COLISÃO (segurar)
O estado inicial é o mesmo; o que mudou foi a interação durante o contato. Então, respondendo à pergunta lá do começo: o que falta é o tipo de colisão. Momento mais tipo de colisão.

## C04 — COMPLETAMENTE INELÁSTICA

### C04-1 — tela: os blocos voltam ao ANTES, se aproximam e grudam; as duas setas se fundem numa só
Vamos começar pelo caso mais simples: quando os blocos ficam juntos. Repara nas velocidades: no contato, as duas viram uma só.

### C04-2 — tela: v₁f = v₂f = v_f
Ficar junto quer dizer exatamente isto: a velocidade final do corpo um é igual à do corpo dois. Vamos chamar de velocidade final comum.

### C04-3 — tela: ANTES m₁v₁ᵢ + m₂v₂ᵢ ; DEPOIS (m₁+m₂)v_f
Antes, o momento total é a soma dos dois momentos. Depois, é como um bloco só, com a massa total, andando com a velocidade final comum.

### C04-4 — tela: as duas expressões se unem numa equação; ÷(m₁+m₂); v_f = (m₁v₁ᵢ + m₂v₂ᵢ)/(m₁+m₂)
Igualando os dois, sai a velocidade final comum: o momento total dividido pela massa total.

### C04-5 — tela: título MÉDIA PONDERADA; a fórmula reescrita com os pesos m₁/(m₁+m₂) e m₂/(m₁+m₂); o eixo de velocidades
E dá para ler essa fórmula de um jeito bonito. Separando os termos, ela vira uma média ponderada das velocidades iniciais: cada velocidade pesa conforme a fração da massa. Esse eixo aqui embaixo é um eixo de velocidades, não é o trilho.

### C04-6 — tela: as massas mudam; o ponto da velocidade final comum desliza entre as velocidades iniciais
Olha o ponto da velocidade final. Quando a massa um aumenta, ele vai para perto da velocidade inicial do corpo um; quando a massa dois aumenta, para perto da do corpo dois. E ele nunca sai do intervalo entre as duas, podendo até ser negativo.

### C04-7 — tela: A MASSA MAIOR PESA MAIS NO RESULTADO. (segurar)
A massa maior pesa mais no resultado.

## C05 — ENERGIA CINÉTICA

### C05-1 — tela: METADE DA VELOCIDADE = METADE DA ENERGIA? ; m₁ = m₂ = m, v₂ᵢ = 0 ; barras K_i e K cheias
Agora uma pergunta que parece fácil. Dois blocos de massas iguais, o segundo parado. Eles batem e grudam. Se a velocidade cair pela metade, a energia cinética também cai pela metade?

### C05-2 — tela: o bloco um chega com v₁ᵢ; no contato, a barra K encolhe e a energia interna cresce; saem juntos com v_f = v₁ᵢ/2
Olha a barra. No contato, a energia cinética cai, e o que sai dela vira energia interna. Pelo momento, os dois saem juntos com metade da velocidade inicial: o dobro da massa com metade da velocidade dá o mesmo momento.

### C05-3 — tela: K_i = ½ m v₁ᵢ²
Vamos fazer a conta. Antes, a energia cinética é meio vezes a massa vezes a velocidade inicial ao quadrado.

### C05-4 — tela: K_f = ½(2m)(v₁ᵢ/2)² ; chaves MASSA ×2 e VELOCIDADE ÷2
Depois, a massa que se move dobrou... e a velocidade caiu pela metade.

### C05-5 — tela: QUADRADO ÷4 ; K_f = ¼ m v₁ᵢ²
Só que a velocidade entra ao quadrado: metade ao quadrado é um quarto. Dobro da massa vezes um quarto... dá metade.

### C05-6 — tela: K_f = ½ K_i em caixa ciano; a barra final tem metade do tamanho
Então a energia cinética final é metade da inicial. A outra metade virou energia interna.

### C05-7 — tela: P CONSERVADO / NÃO IMPLICA / K CONSERVADA (segurar)
E fica a lição: momento conservado não implica energia cinética conservada. São duas conservações diferentes; uma não garante a outra.

## C06 — COLISÃO ELÁSTICA

### C06-1 — tela: novo exemplo; o bloco um vem, o dois parado; medidores P TOTAL e K TOTAL constantes; ANTES → CONTATO → DEPOIS
Agora a colisão elástica, num exemplo novo: o bloco dois começa parado. Repara nos medidores: momento total e energia cinética total ficam iguais. Por isso temos duas equações.

### C06-2 — tela: a colisão e os medidores sobem para a faixa de cima; nasce a equação do momento
A primeira vem do momento.

### C06-3 — tela: m₁v₁ᵢ − m₁v₁f = m₂v₂f − m₂v₂ᵢ → m₁(v₁ᵢ − v₁f) = m₂(v₂f − v₂ᵢ)  (1)
Separando o que é de cada corpo, fica: a massa um vezes a diferença entre a velocidade inicial e a final do corpo um é igual à massa dois vezes a diferença entre a velocidade final e a inicial do corpo dois. Essa é a equação um.

### C06-4 — tela: nasce a equação da energia; ×2 nos dois lados
A segunda vem da energia cinética. E aqui está a ideia: queremos fazer a equação da energia conversar com a do momento.

### C06-5 — tela: m₁(v₁ᵢ² − v₁f²) = m₂(v₂f² − v₂ᵢ²)
Por isso a gente reorganiza do mesmo jeito, separando os corpos, até aparecerem diferenças de quadrados.

### C06-6 — tela: caixa no lado esquerdo; lembrete a² − b² = (a − b)(a + b); depois o lado direito
Fatorando essas diferenças, surgem exatamente os mesmos fatores da primeira equação.

### C06-7 — tela: m₁(v₁ᵢ − v₁f)(v₁ᵢ + v₁f) = m₂(v₂f − v₂ᵢ)(v₂f + v₂ᵢ)  (2)
Essa é a equação dois, e agora as duas falam a mesma língua.

### C06-8 — tela: contorno no fator m₁(v₁ᵢ − v₁f)
Agora, cuidado. A tentação é dividir uma equação pela outra. Mas esse fator pode ser zero, e dividir por zero não pode. Então a gente faz diferente.

### C06-9 — tela: caixas magenta em m₂(v₂f − v₂ᵢ) nas duas equações; a substituição
Repara: esse bloco da equação dois é o mesmo que aparece na equação um. Então a gente usa uma equação dentro da outra.

### C06-10 — tela: m₁(…)(…) − m₁(…)(…) = 0 → m₁(v₁ᵢ − v₁f)[(v₁ᵢ + v₁f) − (v₂f + v₂ᵢ)] = 0
Organizando, aparece um produto igual a zero. A massa não é zero. Então ou o primeiro fator é zero, ou o colchete é zero.

### C06-11 — tela: ramo da esquerda: v₁ᵢ = v₁f e v₂ᵢ = v₂f ; ANTES = DEPOIS ; SEM TROCA LÍQUIDA
Se o primeiro fator for zero, as velocidades finais são iguais às iniciais. Nada mudou: não houve mudança líquida nos momentos dos corpos. Não é o encontro com interação que a gente quer resolver.

### C06-12 — tela: ramo da direita: v₁ᵢ + v₁f = v₂f + v₂ᵢ → v₁ᵢ − v₂ᵢ = −(v₁f − v₂f) em caixa ciano (segurar)
Então fica o outro: o colchete é zero. Rearrumando, a diferença entre as velocidades iniciais é igual a menos a diferença entre as velocidades finais. Guarda essa relação, porque ela tem um significado físico muito bonito.

## C06b — VELOCIDADE RELATIVA

### C06b-1 — tela: os blocos com a régua da distância entre os centros; o gráfico distância × tempo vazio
Olha a distância entre os centros dos dois blocos. Vamos acompanhar essa distância ao longo do tempo, no gráfico da direita.

### C06b-2 — tela: os blocos se aproximam; a reta desce; APROXIMAÇÃO ; Δd/Δt = v₂ᵢ − v₁ᵢ = −3 m/s
Antes do contato, a distância diminui. A inclinação dessa reta é quanto a distância muda por segundo: aqui, a distância diminui a três metros por segundo. É a rapidez com que os blocos se aproximam.

### C06b-3 — tela: contato no mínimo; os blocos se afastam; a reta sobe; AFASTAMENTO ; Δd/Δt = v₂f − v₁f = +3 m/s
Depois do contato, a distância volta a crescer, e repara na inclinação: agora ela aumenta a três metros por segundo.

### C06b-4 — tela: |v₂ᵢ − v₁ᵢ| = |v₂f − v₁f|
Os blocos se afastam com a mesma rapidez com que se aproximaram.

### C06b-5 — tela: A VELOCIDADE RELATIVA INVERTE. ; v₁ᵢ − v₂ᵢ = −(v₁f − v₂f) (segurar)
Essa é a relação que saiu da álgebra: numa colisão elástica, a velocidade relativa inverte. Cada bloco não precisa inverter a própria velocidade; o que inverte é a velocidade de um em relação ao outro.

## C07 — FÓRMULAS GERAIS

### C07-1 — tela: miniatura antes → depois; P_i = P_f e v₁ᵢ − v₂ᵢ = v₂f − v₁f
Com o momento e a velocidade relativa, dá para achar as duas velocidades finais de qualquer colisão elástica em uma dimensão.

### C07-2 — tela: isolar v₂f; o bloco inteiro entra na equação do momento
O caminho é simples: substituímos uma relação na outra e isolamos cada velocidade final.

### C07-3 — tela: DISTRIBUTIVA + AGRUPAR → (m₁ − m₂)v₁ᵢ + 2m₂v₂ᵢ = (m₁ + m₂)v₁f
(deixar a tela trabalhar; sem fala ou só um curto "organizando...")

### C07-4 — tela: ÷(m₁+m₂) → v₁f = (m₁ − m₂)/(m₁ + m₂)·v₁ᵢ + 2m₂/(m₁ + m₂)·v₂ᵢ
Aí está a velocidade final do corpo um.

### C07-5 — tela: v₂f = 2m₁/(m₁ + m₂)·v₁ᵢ + (m₂ − m₁)/(m₁ + m₂)·v₂ᵢ
E, pela velocidade relativa, sai a do corpo dois.

### C07-6 — tela: as fórmulas encolhem; RESULTADO ≠ MÉTODO ; MÉTODO: MOMENTO + CONDIÇÃO DA COLISÃO (segurar)
Agora, uma coisa importante: essas fórmulas são um resultado, não o método. Elas valem para colisão elástica em uma dimensão, e só. O método é sempre o mesmo: momento mais a condição da colisão. Se você entende isso, nem precisa decorar as fórmulas.

## C08 — CASOS-LIMITE

### C08-1 — tela: v₂ᵢ = 0 e as duas fórmulas no topo
Mas vamos testar se elas fazem sentido. Com o segundo bloco parado, as fórmulas ficam mais simples. E a gente vai olhar três casos extremos.

### C08-2 — tela: MASSAS IGUAIS ; m₁ = m₂ ; O QUE VOCÊ ESPERA?
Primeiro: massas iguais. Pensa um pouco... o que você espera que aconteça?

### C08-3 — tela: a colisão; o um para e o dois sai; v₁f = 0, v₂f = v₁ᵢ ; CONFERE
O primeiro para, e o segundo sai com a velocidade que o primeiro tinha. É a famosa troca de velocidades da sinuca. As fórmulas dão exatamente isso: confere.

### C08-4 — tela: LEVE CONTRA PESADO ; m₁ ≪ m₂ ; O QUE VOCÊ ESPERA?
Agora um bloco leve batendo num muito pesado. Na animação, o pesado tem trinta vezes a massa do leve. O tamanho dos blocos só ajuda a ver; não é a escala da massa.

### C08-5 — tela: o leve volta; o pesado anda um pouquinho (marca Δx₂ > 0); v₁f ≈ −v₁ᵢ, v₂f ≈ 0 ; REBATE.
O leve volta praticamente com a mesma velocidade, e o pesado mal se mexe. Mal, mas se mexe: repara na marquinha embaixo dele. Por isso está escrito "aproximadamente zero", e não zero. É como uma bolinha batendo numa parede: rebate.

### C08-6 — tela: PESADO CONTRA LEVE ; m₁ ≫ m₂
E o contrário: um bloco pesado batendo num leve parado.

### C08-7 — tela: o pesado quase não perde velocidade; o leve dispara; v₁f ≈ v₁ᵢ, v₂f ≈ 2v₁ᵢ ; O LEVE PODE SAIR MAIS RÁPIDO QUE O INCIDENTE.
O pesado segue quase como se nada tivesse acontecido, e o leve sai com quase o dobro da velocidade do pesado. Parece estranho, mas não cria energia nenhuma: a energia que o leve ganha sai do pesado.

### C08-8 — tela: CASOS-LIMITE = TESTES DE PLAUSIBILIDADE ; TESTE SUA RESPOSTA. (segurar)
Esse é o valor dos casos-limite: são testes de plausibilidade. Achou uma fórmula numa prova? Testa massas iguais, testa uma massa muito maior que a outra. Se não der o que você espera, alguma coisa está errada.

## C09 — PÊNDULO BALÍSTICO

### C09-1 — tela: bloco suspenso por dois fios; o projétil chega com a seta da velocidade inicial; definição de vᵢ
Agora um problema clássico, que mistura tudo isso: o pêndulo balístico. Um projétil, com uma velocidade inicial que a gente quer descobrir, vai bater num bloco pendurado.

### C09-2 — tela: o projétil entra no bloco; o conjunto sai com V_t; definição de V_t
Ele entra no bloco e fica preso. Logo depois, o conjunto, projétil mais bloco, sai com uma velocidade que a gente vai chamar de velocidade do conjunto.

### C09-3 — tela: o conjunto sobe; a altura h marcada com a chave
E aí o conjunto sobe, até parar por um instante a uma certa altura. A altura é fácil de medir. A pergunta é: dá para descobrir a velocidade do projétil só medindo essa altura?

### C09-4 — tela: UMA ÚNICA LEI NÃO VALE DO COMEÇO AO FIM.; linha do tempo A → B → C (segurar)
O segredo é perceber que uma única lei não vale do começo ao fim. Vamos dividir em três instantes: A, antes do impacto; B, logo depois; e C, na altura máxima.

## C10 — PÊNDULO · IMPACTO

### C10-1 — tela: o trecho A → B acende em magenta; MOMENTO HORIZONTAL
Primeiro, do instante A para o B: o impacto.

### C10-2 — tela: peso e tensões verticais (azul-claro); FORÇAS EXTERNAS VERTICAIS; eixo +x
As forças externas aqui, o peso e as tensões nos fios, são verticais naquele instante. Na horizontal, o impulso externo é desprezível. Então, no impacto, o que se conserva é o momento horizontal.

### C10-3 — tela: P_x,A = m vᵢ
Antes, só o projétil se move: momento horizontal igual à massa do projétil vezes a velocidade inicial dele.

### C10-4 — tela: o projétil entra; P_x,B = (m + M)V_t
Logo depois, projétil e bloco andam juntos: a massa total vezes a velocidade do conjunto. É uma colisão completamente inelástica, igual à que a gente viu antes.

### C10-5 — tela: m vᵢ = (m + M)V_t em caixa magenta
Igualando: massa do projétil vezes a velocidade inicial é igual à massa total vezes a velocidade do conjunto.

### C10-6 — tela: barras K_A e K_B; 2 %
E a energia cinética? Despenca. Com um projétil de vinte gramas e um bloco de novecentos e oitenta, sobram só dois por cento. Por isso, no impacto, não dá para conservar a energia cinética.

## C11 — PÊNDULO · SUBIDA

### C11-1 — tela: o trecho B → C acende em ciano; ENERGIA MECÂNICA; U_g = 0 em B; barras K e U_g
Agora, do B para o C: a subida. Aqui é outra história. Desprezando o ar e o atrito nos suportes, e com fios ideais, a tensão é sempre perpendicular ao movimento e não realiza trabalho. Então a energia mecânica se conserva. Vamos tomar a energia potencial como zero lá embaixo, no ponto B.

### C11-2 — tela: o conjunto sobe; K diminui e U_g aumenta, sincronizados; a altura h
Repara nas barras: conforme o conjunto sobe, a energia cinética vai virando energia potencial gravitacional. No topo, a velocidade é zero, e tudo virou energia potencial. E repara que aqui o momento linear do conjunto não se conserva: durante a subida existe impulso externo.

### C11-3 — tela: ½(m + M)V_t² = (m + M)g h
Então a energia cinética lá embaixo é igual à energia potencial lá em cima.

### C11-4 — tela: a massa total cortada dos dois lados → V_t = √(2gh)
A massa total cancela, e a velocidade do conjunto fica a raiz quadrada de duas vezes a gravidade vezes a altura. A raiz positiva, porque é o módulo da velocidade.

### C11-5 — tela: a equação do impacto pisca; vᵢ = (m + M)/m · V_t → vᵢ = (m + M)/m · √(2gh)
Agora a gente volta para o impacto e substitui. Chegamos lá: dá para descobrir a velocidade do projétil medindo só as massas e a altura.

### C11-6 — tela: a linha do tempo inteira; MOMENTO em A → B, ENERGIA em B → C; LEIS DIFERENTES PARA INTERVALOS DIFERENTES. (segurar)
Mas o mais importante não é a fórmula. É o caminho: no impacto, momento; na subida, energia. Leis diferentes para intervalos diferentes. Misturar as duas é o erro mais comum nesse problema.

## C12 — MÉTODO

### C12-1 — tela: SISTEMA + INTERVALO (o marcador ciano no primeiro nó)
Então vamos juntar tudo num método. Primeiro: qual é o sistema e qual é o intervalo de tempo que você está olhando?

### C12-2 — tela: o marcador anda; EIXO + SINAIS
Segundo: defina o eixo e cuide dos sinais.

### C12-3 — tela: J_ext ≈ 0 ? → P_i = P_f
Terceiro: o impulso externo é desprezível nesse intervalo? Se for, o momento total se conserva.

### C12-4 — tela: CONDIÇÃO EXTRA? ; ELÁSTICA → K_i = K_f ; GRUDAM → v₁f = v₂f ; OUTRA → DADO
Quarto: qual é a condição extra? Se é elástica, conserva a energia cinética. Se gruda, as velocidades finais são iguais. Se for outra, alguma informação física adicional precisa ser fornecida.

### C12-5 — tela: NOVO PROCESSO? → SEPARE
E quinto: começou outro processo depois da colisão? Então separe os intervalos, como no pêndulo.

### C12-6 — tela: as três miniaturas do começo; MESMO COMEÇO; REBATEM K_i = K_f · SE SEPARAM DADO EXTRA · FICAM JUNTOS v₁f = v₂f (segurar)
E agora a pergunta lá do começo está respondida. Mesmo começo, três finais, porque cada colisão tem uma condição diferente: na elástica, a energia cinética se conserva; quando se separam perdendo energia, precisa de um dado extra; quando grudam, as velocidades finais são iguais. O momento é o mesmo nas três; quem decide o final é o tipo de colisão.

### C12-7 — tela: MODELE O PROCESSO. / NÃO PROCURE UMA FÓRMULA. (segurar)
Então, na próxima vez que você encontrar uma colisão: modele o processo. Não procure uma fórmula.

## PONTE 2D

### P1 — tela: P⃗_i = P⃗_f ; dois discos com as velocidades na mesma linha; as velocidades finais se inclinam e o triângulo magenta mostra o momento total fixo
E repara num detalhe que a gente escondeu até aqui: o momento é um vetor. Em uma dimensão, tudo acontece numa linha só. Mas se os corpos puderem sair em direções diferentes, o momento total continua o mesmo... só que agora como vetor.

## CTA

### E1 — tela: logo com os anéis; INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS
Hoje a gente ligou momento, energia e o tipo de colisão para prever o que acontece depois de um choque. Se essas ideias ajudaram você, se inscreve no Parallax Lab para acompanhar os próximos vídeos.

### E2 — tela: E SE A COLISÃO NÃO ACONTECER EM UMA LINHA?
E fica a pergunta: e se a colisão não acontecer em uma linha?

### E3 — tela: PRÓXIMO VÍDEO: COLISÕES EM 2D ; onda dos anéis
É isso que a gente vai ver no próximo vídeo: colisões em duas dimensões. Me conta aqui nos comentários: qual foi o caso-limite que mais te surpreendeu? Valeu demais por assistir, e até a próxima!

---

## Notas para a sincronização (fase seguinte)

- Estratégia: **retiming das próprias animações + revelações progressivas + pausas curtas**. `hold` só quando a tela já tem algo para
  ler ou contemplar (âncoras **(segurar)**); nada de quadro congelado por 15 s enquanto a voz explica. Onde a fala é mais longa que a
  animação (C01, C02, C06, pêndulo), esticar os movimentos e escalonar a entrada dos elementos.
- Pontos onde a fala pede mais tempo de tela do que a animação tem hoje: H4, A2, C01-5, C01-8, C02-3, C03-6, C04-6, C05-2, C06-8 a
  C06-12, C06b-5, C07-6, C08-5, C08-8, C11-1, C11-5, C12-6.
- A cena ainda não tem as âncoras `an(n, k)` do padrão; elas entram na fase de voz, uma por `###` deste arquivo.
- Números falados: "três metros por segundo", "trinta vezes", "vinte gramas", "novecentos e oitenta gramas", "dois por cento".
