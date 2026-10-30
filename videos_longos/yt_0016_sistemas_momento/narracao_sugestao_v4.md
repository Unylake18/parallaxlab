# yt_0016 — MOMENTO EM SISTEMAS · sugestão de narração v4 (Parte 2 de 2 do yt_0015)

Data: 2026-10-29. Base: a física e os números do `handoff_v1.md` (§3 congelada: g = 9,8 m/s², +x à direita, +y para cima), as âncoras
do preview v4 (`mapa_ancoras_v4.txt`) e a análise do v4 quadro a quadro (3 quadros por âncora). A fala foi reescrita inteira a partir da
`narracao_v3.md`: mesmas 64 âncoras, mesma ordem, mesma física; mais conectivos, mais explicação (a animação se molda à voz), tom de
professor de cursinho, brincadeiras curtas, boas-vindas e encerramento.

**Regras aplicadas** (`docs/roteiro_voz_elevenlabs_v4.md` e `docs/padrao_video_longo.md` §5):
- variável sempre pelo nome inteiro ("a massa do cavalo", "a velocidade na água"), nunca a letra; números e unidades por extenso;
  operações faladas ("vezes", "dividido por", "ao quadrado");
- tags `[ ]` em inglês, uma por trecho, valendo até a próxima; base `[thoughtful]`/`[curious]`; `[thoughtful, emphatic]` só no conceito-chave;
  `[excited]` duas vezes; `[happy]` nas boas-vindas; `[calm, satisfied]` no fechamento; pausa com `[short pause]` ou reticências;
  nada de `[slowly]`, `[pause]` ou tags de postura;
- estrutura de cada bloco: pergunta → ideia → conta → significado → conferência; o fechamento responde o hook.

**Como ler:** cada `###` é uma âncora (evento visual) com o mesmo ID do v4. A linha `tela:` descreve o que o v4 mostra; a fala começa
~0,15 s depois e manda: a cena se estica ou encolhe. Para gerar o `ancoras.json` com este texto, basta apontar o `gerar_ancoras.py`
para este arquivo (o formato é o mesmo).

---

## HOOK

### H1 — tela: (3D) o cavalo já andando, puxando a pedra pela corda presa no balancim; setas T⃗ (na pedra, para a frente) e −T⃗ (no balancim, para trás), do mesmo tamanho
[curious] A corda puxa a pedra para a frente. E, pela terceira lei de Newton, ela puxa o cavalo para trás... com uma força do mesmo tamanho.

### H2 — tela: (3D) sinal de igual entre os rótulos; push-in até a corda; interrogação sobre o cavalo
Forças iguais e opostas: era para dar empate. Então como é que o cavalo anda, e ainda leva a pedra junto?

### H3 — tela: (3D) a câmera recua; o cavalo apaga; SE A CORDA PUXA O CAVALO PARA TRÁS COM A MESMA FORÇA, COMO ELE ANDA?
A resposta cabe em duas ideias: o que é um sistema, e o que muda o momento dele.

## ABERTURA

### A1 — tela: logo; BEM-VINDOS AO PARALLAX LAB
[happy] Fala, pessoal! Bem-vindos ao Parallax Lab!

### A2 — tela: miniatura parada do hook com a pergunta embaixo; MOMENTO EM SISTEMAS · NESTE VÍDEO: O QUE MUDA O MOMENTO DE VÁRIOS CORPOS
[thoughtful] Hoje o assunto é o momento de vários corpos juntos. E a gente começa exatamente onde o vídeo anterior parou: com esse cavalo teimoso e essa pergunta. Fica tranquilo que, até o final, ela vai estar respondida.

### A3 — tela: O VÍDEO ANTERIOR: UM CORPO; disco empurrado uma vez; a curva da força no tempo se desenha com a área do impulso; CONTA: F⃗_res = dp⃗/dt → J⃗ = ∫F⃗_res dt = Δp⃗
[thoughtful] Primeiro, uma lembrança rápida. No vídeo anterior, a gente olhou para um corpo só e perguntou: o que uma força faz com o momento dele? A resposta foi a segunda lei na forma com o momento: a força resultante é a taxa de variação do momento. E, somando essa força ao longo do tempo, aparece o impulso resultante, que é exatamente a variação do momento. No gráfico, o impulso é a área embaixo da curva da força.

### A4 — tela: O VÍDEO ANTERIOR: DOIS CORPOS; dois discos colidem uma vez; CONTA: Δp⃗₁ = −Δp⃗₂ → P⃗ = CONSTANTE (DOIS CORPOS SOZINHOS)
Depois, a gente colocou dois discos para bater. Durante o choque, um empurra o outro com forças iguais e opostas. Por isso, a variação do momento do primeiro disco é exatamente o contrário da variação do momento do segundo. O que um ganha, o outro perde. Ou seja: dois corpos sozinhos, sem ninguém de fora mexendo, têm momento total constante.

### A5 — tela: A DIFERENÇA DE HOJE; volta o cavalo; fronteira só no cavalo (CAVALO), com −T⃗ azul; a fronteira cresce até CAVALO + CORDA + PEDRA e a seta vira cinza INTERNA; legenda UM CORPO: TODA FORÇA CONTA → SISTEMA: INTERNAS × EXTERNAS
[curious] Só que o mundo real quase nunca é tão limpinho. O cavalo pisa no chão, a pedra raspa no chão, e a corda liga os dois. E aqui está a grande diferença entre os dois vídeos. Repara na caixa tracejada. Se você olha só para o cavalo, a força da corda é uma força como outra qualquer: ela puxa o cavalo para trás e entra na força resultante dele. Mas agora a caixa cresce e engole o cavalo, a corda e a pedra. Essa mesma força passa a ser uma força de dentro, uma força interna. Então a pergunta de hoje é: as forças de dentro conseguem mudar o momento do conjunto, ou não?

### A6 — tela: ONDE A GENTE ESTÁ; VÍDEO ANTERIOR · UM CORPO (disco, F⃗_res = dp⃗/dt, RESOLVIDO) → HOJE · MUITOS CORPOS (três esferas, ?); o ? vai para o canto da CONTA
[thoughtful] Então o mapa é este. A parte de um corpo só já está resolvida. Hoje a gente passa para muitos corpos, e aquela interrogação ali no canto vai virar uma equação. No caminho, a conservação do momento deixa de ser um fato sobre dois discos isolados e vira uma ferramenta para qualquer sistema, mesmo com forças de fora agindo.

## T7 — SISTEMAS DE PARTÍCULAS

### T7-1 — tela: (3D) três esferas de aço ligadas por molas dentro da fronteira SISTEMA; legenda INTERNAS · FORÇAS ENTRE OS CORPOS DE DENTRO; depois EXTERNAS · VÊM DE FORA DA FRONTEIRA, com o peso de cada esfera
[thoughtful] Vamos começar combinando as palavras. Um sistema é o grupo de corpos que a gente escolhe acompanhar, dentro de uma fronteira que a gente mesmo desenha, como essa caixa tracejada. As forças que os corpos de dentro fazem uns nos outros, como as molas, são as forças internas. E as forças que vêm de fora da fronteira, como o peso de cada esfera, são as forças externas. Guarda isso: quem escolhe a fronteira é você. E essa escolha vai decidir o problema inteiro.

### T7-2 — tela: SISTEMA: 1 + 2; duas esferas e uma mola, com a força da mola em cada uma e o peso de cada uma; CONTA: dp⃗₁/dt = F⃗₁₍₂₎ + F⃗₁^ext, depois dp⃗₂/dt = F⃗₂₍₁₎ + F⃗₂^ext
[curious] E como a gente descobre o que muda o momento do sistema? Vamos por partes, começando pelo caso mais simples: só duas esferas, ligadas por uma mola. Sobre a primeira esfera agem duas coisas: a força da mola, que vem da segunda esfera, e a força externa, o peso. Pela segunda lei, a taxa de variação do momento da primeira esfera é a soma dessas duas forças. Para a segunda esfera é a mesma história: a força da mola, que agora vem da primeira, mais a força externa sobre ela.

### T7-3 — tela: as duas equações somadas; F⃗₁₍₂₎ e F⃗₂₍₁₎ se cancelam (TERCEIRA LEI: IGUAIS E OPOSTAS) → dP⃗/dt = F⃗^ext; A MOLA TRABALHA; O TOTAL SÓ OUVE O DE FORA
Agora vem o truque: soma as duas equações. Do lado esquerdo, aparece a taxa de variação do momento total, que é a soma dos dois momentos. Do lado direito, aparecem as duas forças da mola. Só que, pela terceira lei, a força que a primeira esfera recebe da segunda é igual e oposta à força que a segunda recebe da primeira. Somadas, elas dão zero e somem da conta. Sobra só a força externa. Ou seja: a mola trabalha bastante, estica, encolhe, sacode as esferas... mas o momento total só escuta o que vem de fora.

### T7-4 — tela: volta a terceira esfera; uma esfera acende; CONTA: dp⃗ᵢ/dt = Σⱼ F⃗ᵢ₍ⱼ₎ + F⃗ᵢ^ext; legenda i RECEBE DE j
[thoughtful] Beleza, com dois funcionou. E com muitos corpos? Pega uma esfera qualquer do sistema, essa que acendeu. A taxa de variação do momento dela é a soma das forças que todas as outras esferas fazem nela, mais a força externa que age sobre ela. É a mesma ideia de antes, só que agora a esfera escolhida recebe força de cada uma das outras.

### T7-5 — tela: CONTA: dP⃗/dt = ΣᵢΣⱼ F⃗ᵢ₍ⱼ₎ + F⃗^ext, com P⃗ = Σp⃗ᵢ; chaves SOMA DUPLA DAS INTERNAS e EXTERNA TOTAL; a seta magenta do momento total no meio das esferas
Agora a gente escreve essa equação para cada esfera e soma tudo. Do lado esquerdo, a soma dos momentos de todas as esferas é o momento total do sistema, essa seta magenta no meio delas. Do lado direito, sobram duas partes: uma soma dupla, com todas as forças internas, e a força externa total.

### T7-6 — tela: matriz de pares, LINHA: QUEM RECEBE × COLUNA: QUEM FAZ; as células (1, 2) e (2, 1) acendem junto com a mola entre as esferas um e dois, depois os outros pares; as células se apagam duas a duas; a diagonal é vazia
[curious] E essa soma dupla, assusta? Calma, ela é só uma tabela. Cada linha é quem recebe a força, e cada coluna é quem faz a força. Olha aqui: a força que a esfera um recebe da esfera dois, e, do outro lado da diagonal, a força que a esfera dois recebe da esfera um. É o mesmo par da mola que a gente acabou de ver, e pela terceira lei a soma dele dá zero. Com o par da um com a três acontece a mesma coisa, e com o par da dois com a três também. A diagonal fica vazia, porque ninguém empurra a si mesmo. No fim, as células se apagam duas a duas, e a soma dupla inteira vale zero.

### T7-7 — tela: dP⃗/dt = F⃗^ext em destaque (a interrogação do A6 vira essa equação); AS INTERNAS NÃO APARECEM; DICA: PRIMEIRO DEFINA O SISTEMA. SÓ FORÇA EXTERNA ENTRA NA VARIAÇÃO DO MOMENTO TOTAL
[thoughtful, emphatic] E sobra só isto: a taxa de variação do momento total é igual à força externa resultante. As forças internas, por maiores que sejam, não aparecem. Então, só uma força de fora muda o momento total de um sistema. Lembra da interrogação lá do canto? Virou esta equação.

### T7-8 — tela: (3D) disco sobre o gelo com um binário (duas forças externas iguais e opostas em pontos diferentes); o disco gira; O CENTRO NÃO SAI DO LUGAR; CONTA: SE A FORÇA EXTERNA RESULTANTE = 0 ⇒ P⃗ CONSTANTE; MAS O DISCO GIRA; GIRAR: MÓDULO DE ROTAÇÃO
[thoughtful] Agora repara numa sutileza importante. Para o momento total ficar constante, o sistema não precisa estar isolado do mundo. Basta a força externa resultante ser zero. Olha esse disco no gelo: duas forças externas, iguais e opostas, puxando em pontos diferentes. A soma delas é zero, então o momento total não muda, e o centro do disco não sai do lugar. Mas o disco gira! E esse giro é assunto para o módulo de rotação. Hoje a gente só anota: momento constante não quer dizer que nada está acontecendo.

### T7-9 — tela: bola em parábola, PESO SÓ NA VERTICAL; CONTA: dPₓ/dt = Fₓ^ext = 0; dP_y/dt = F_y^ext; COMPONENTE POR COMPONENTE; no fim, duas cargas e uma nuvem de campo: MOMENTO DAS PARTÍCULAS + MOMENTO DO CAMPO = CONSTANTE
[curious] E tem mais: essa equação vale componente por componente. Olha a bola em parábola. O peso só puxa na vertical, então, na horizontal, a força externa é zero, e o momento horizontal fica constante o tempo todo. Já o momento vertical muda, porque na vertical tem força. Uma direção pode conservar e a outra não. E um detalhe para os curiosos: quando a terceira lei falha, como entre cargas elétricas em movimento, a conservação continua valendo, desde que a gente conte também o momento do campo.

## T8 — FORÇA INTERNA NÃO MOVE O SISTEMA

### T8-1 — tela: (3D, lateral) o cavalo arrasta a pedra; fronteira SISTEMA: CAVALO + CORDA + PEDRA; setas da corda em cinza (INTERNA: A CORDA · PUXA A PEDRA E O CAVALO; SOME DA CONTA); em azul-claro, CHÃO NA PEDRA (para trás) e CHÃO NAS PATAS (para a frente) (EXTERNAS NA HORIZONTAL); CONTA: massa do cavalo 600 kg, massa da pedra 800 kg
[thoughtful] Agora sim, de volta ao cavalo, com a ferramenta nova na mão. Primeiro passo, sempre: definir o sistema. A gente desenha a fronteira em volta do cavalo, da corda e da pedra. A corda puxa a pedra para a frente e o cavalo para trás, mas as duas pontas estão dentro da caixa. Então a força da corda é interna e sai da conta. E quem sobra? As forças externas na horizontal: o chão empurrando as patas do cavalo para a frente, e o chão raspando na pedra, para trás. O peso e a normal ficam na vertical e se cancelam.

### T8-2 — tela: CONTA: f_pedra = 0,3 · 800 · 9,8 = 2.352 N (CINÉTICO: A PEDRA JÁ DESLIZA); F_chão = 2.800 N; os valores aparecem nas setas do chão
Vamos colocar números. O cavalo tem seiscentos quilogramas, e a pedra tem oitocentos. Como a pedra já está deslizando, vale o coeficiente de atrito cinético, que é zero vírgula três. Então o atrito do chão na pedra é zero vírgula três, vezes oitocentos, vezes nove vírgula oito: dois mil trezentos e cinquenta e dois newtons, para trás. E vamos supor que o chão empurre o cavalo para a frente com dois mil e oitocentos newtons.

### T8-3 — tela: (3D, câmera 3/4) o conjunto acelera, com o mostrador da velocidade subindo e as setas da velocidade e da aceleração; CONTA: (2.800 − 2.352) = (600 + 800) · a; A CORDA NEM APARECE; a = 0,32 m/s²
[curious] E a corda? Repara: ela nem aparece na conta! Para o sistema inteiro, a força externa resultante é dois mil e oitocentos menos dois mil trezentos e cinquenta e dois, ou seja, quatrocentos e quarenta e oito newtons. E essa força acelera a massa total, que é mil e quatrocentos quilogramas. Dividindo uma pela outra, a aceleração do conjunto dá zero vírgula trinta e dois metros por segundo ao quadrado. Dá para ver no mostrador: a velocidade vai subindo devagarinho.

### T8-4 — tela: (3D, lateral) PEDRA: T − 2.352 = 800 · 0,32 ⇒ T = 2.608 N; CAVALO: 2.800 − T = 600 · 0,32 ⇒ 192 N = 192 N; FECHA: MESMA TENSÃO NAS DUAS PONTAS
Agora, só para desconfiar da gente mesmo, vamos conferir separando os corpos. Na pedra: a tensão da corda menos o atrito tem que dar a massa da pedra vezes a aceleração. Então a corda puxa a pedra com dois mil seiscentos e oito newtons. No cavalo: o empurrão do chão menos essa mesma tensão sobra cento e noventa e dois newtons. E a massa do cavalo vezes a aceleração dá... cento e noventa e dois newtons. Fecha certinho. A corda tem a mesma tensão nas duas pontas.

### T8-5 — tela: no cavalo, a seta do chão (2.800 N) maior que a seta da corda (2.608 N); CONTA: 2.800 N > 2.608 N; O CAVALO ANDA PORQUE O CHÃO O EMPURRA; A CORDA SÓ TRANSMITE
[excited] E aqui está a resposta da pergunta do começo. Sim, a corda puxa o cavalo para trás com dois mil seiscentos e oito newtons. Só que o chão empurra o cavalo para a frente com dois mil e oitocentos. O cavalo não anda porque ganha a briga com a pedra: ele anda porque ganha a briga com o chão. A corda só transmite o esforço de um para o outro.

### T8-6 — tela: (3D, 3/4) o chão sob as patas vira gelo; CÂMERA LENTA; a velocidade cai até zero e as patas escorregam; CONTA: coeficiente estático ≈ 0,1; f_máx = 0,1 · 600 · 9,8 = 588 N; 588 < 2.352; a ≈ −1,26 m/s²; barras CHÃO FIRME 2.800 N × GELO 588 N, cada uma contra os 2.352 N da pedra: ANDA / PARA
[curious] E se o chão embaixo das patas virasse gelo? Vira um cavalo de patins. No gelo, o coeficiente de atrito estático cai para uns zero vírgula um. Então o máximo que o chão consegue empurrar o cavalo é zero vírgula um, vezes seiscentos, vezes nove vírgula oito: quinhentos e oitenta e oito newtons. Só que a pedra continua raspando com dois mil trezentos e cinquenta e dois. A força externa resultante fica para trás, e o conjunto freia, com uns um vírgula vinte e seis metros por segundo ao quadrado, até parar. Olha as barras: no chão firme, o empurrão ganha da pedra, e o cavalo anda. No gelo, perde, e o cavalo para. O cavalo é o mesmo, a corda é a mesma. O que mudou foi só a força externa.

### T8-7 — tela: Cyrano sentado numa placa de ferro, a Lua no alto; ele joga um ímã para cima (um lançamento + REPLAY); fronteira PESSOA + PLACA + ÍMÃ; CORDA E ÍMÃ: SÓ FORÇAS INTERNAS · NÃO MUDAM O MOMENTO DO CONJUNTO
[thoughtful] Tem uma ideia clássica, do Cyrano de Bergerac, para chegar até a Lua: sentar numa placa de ferro e jogar um ímã para cima. O ímã puxa a placa, você joga o ímã de novo, e assim vai subindo. Genial, né? Pena que não funciona. Desenha a fronteira em volta da pessoa, da placa e do ímã: todas as forças entre eles são internas. E força interna não muda o momento do conjunto. A viagem para a Lua vai ter que esperar.

### T8-8 — tela: (3D) pessoa andando; PÉ EMPURRA O CHÃO (para trás) e ATRITO DO CHÃO (para a frente); A GENTE EMPURRA A TERRA PARA TRÁS; O ATRITO EMPURRA A GENTE PARA A FRENTE; NO GELO, QUASE NÃO HÁ ATRITO; DICA: QUEM ACELERA O CONJUNTO É A FORÇA EXTERNA. A CORDA SÓ TRANSMITE
Até o jeito como você anda é exatamente isso. A cada passo, o seu pé empurra o chão para trás, e o atrito do chão empurra você para a frente. Quem acelera você é o chão, uma força externa. Por isso andar no gelo é tão difícil: quase não tem atrito para te empurrar. Guarda essa ideia, que daqui a pouco ela volta.

## T9 — ESCOLHER O SISTEMA

### T9-1 — tela: SISTEMA: SÓ A BOLA; bola cai 10 m até a Terra, com a seta do peso; CONTA: v = √(2gh) = 14,0 m/s; p⃗ MUDA O TEMPO TODO; O PESO É EXTERNO
[thoughtful] Agora a segunda grande ideia: a escolha do sistema. Uma bola de um quilograma cai de dez metros de altura. A velocidade de chegada é a raiz quadrada de duas vezes a gravidade vezes a altura, e dá catorze metros por segundo. Se o sistema é só a bola, o momento dela cresce o tempo todo durante a queda. E está tudo certo: o peso vem da Terra, que está fora da fronteira, então é uma força externa. E força externa muda o momento.

### T9-2 — tela: REPLAY · CÂMERA LENTA; a fronteira cresce: SISTEMA: BOLA + TERRA; A FORÇA ENTRE ELAS FICA INTERNA; P⃗_total = 0 EM TODO INSTANTE; v_Terra = 1 · 14 / 5,97 × 10²⁴ ≈ 2,3 × 10⁻²⁴ m/s; IMPOSSÍVEL DE PERCEBER
[curious] Agora a gente aumenta o sistema: bola mais Terra. A atração entre as duas fica dentro da fronteira, então vira força interna. E aí o momento total fica zero a todo instante. Enquanto a bola ganha momento para baixo, a Terra ganha o mesmo tanto para cima, vindo ao encontro da bola. Só que a Terra tem uns seis vezes dez elevado a vinte e quatro quilogramas. Dividindo o momento da bola pela massa da Terra, a velocidade dela fica em uns dois vírgula três vezes dez elevado a menos vinte e quatro metros por segundo. Ninguém percebe, nem a Terra. Mas a conta fecha.

### T9-3 — tela: chão com atrito; bloco LEVE de 1 kg à esquerda e PESADO de 2 kg à direita, com uma mola entre eles; eixo +x para a direita; logo após o disparo, as setas das velocidades; CONTA: v₁ = −2 m/s; v₂ = +1 m/s; p₁ = −2, p₂ = +2 kg·m/s; P = 0 LOGO DEPOIS DO DISPARO
[thoughtful] Agora um exemplo mais esperto. Dois blocos num chão com atrito, com uma mola comprimida entre eles: o leve, de um quilograma, e o pesado, de dois. Marca o sentido positivo para a direita. A mola dispara os dois num instante tão curto que o atrito nem tem tempo de agir. O bloco leve sai para a esquerda a dois metros por segundo, e o pesado sai para a direita a um metro por segundo. Logo depois do disparo, o momento total continua zero: menos dois quilogramas metro por segundo de um lado, mais dois do outro.

### T9-4 — tela: MASSAS IGUAIS; dois blocos iguais com atritos iguais e opostos; ATRITOS IGUAIS E OPOSTOS; o gráfico P(t) = 0; PARAM JUNTOS
[curious] Antes, um caso para comparar: e se as massas fossem iguais? Os dois blocos sairiam com a mesma velocidade, em sentidos opostos, e o atrito em cada um teria o mesmo tamanho, também em sentidos opostos. A força externa resultante é zero. Então o momento total fica zero o tempo todo, e os dois param juntos. Sem graça, né? Agora vem a parte interessante.

### T9-5 — tela: o disparo principal uma vez em CÂMERA LENTA, com o gráfico P(t) se desenhando; CONTA: m₁ = 1 kg, m₂ = 2 kg, μ = 0,2; ATRITO NO LEVE +1,96 N; ATRITO NO PESADO −3,92 N; RESULTANTE −1,96 N; O MOMENTO TOTAL DESCE
Com massas diferentes, o atrito não se cancela. O coeficiente de atrito é zero vírgula dois. O bloco leve está indo para a esquerda, então o atrito nele aponta para a direita: zero vírgula dois, vezes um, vezes nove vírgula oito, um vírgula noventa e seis newtons. O pesado vai para a direita, então o atrito nele aponta para a esquerda, e como ele tem o dobro da massa, o atrito é o dobro: três vírgula noventa e dois newtons. Somando, a força externa resultante fica em um vírgula noventa e seis newtons para a esquerda. Por isso o momento total, que começou em zero, começa a descer no gráfico.

### T9-6 — tela: o pesado parado; o ponto (0,51 s; −1,0) acende; depois (1,02 s; 0); CONTA: PESADO PARA: t = 0,51 s, P = −1,0; LEVE PARA: t = 1,02 s, P = 0
[thoughtful] O bloco pesado para primeiro, depois de uns cinquenta e um centésimos de segundo. Nesse instante, só o leve ainda está andando, e o momento total chega a menos um quilograma metro por segundo: o ponto mais baixo do gráfico. A partir daí, só sobra o atrito no leve, que aponta para a direita, e o momento total sobe de volta. Quando o leve também para, em um vírgula zero dois segundo, o momento total volta a ser zero.

### T9-7 — tela: REPLAY desenha P_Terra(t) embaixo, espelhado; O CHÃO GANHA, DEPOIS DEVOLVE; CONTA: P + P_Terra = 0 A TODO INSTANTE; DICA: NÃO CONSERVA? PERGUNTE QUEM FICOU DE FORA DO SISTEMA
[curious] Mas espera aí: o momento total foi até menos um e voltou. Para onde ele foi nesse meio-tempo? Para a Terra! O atrito é a força entre os blocos e o chão. Se você coloca a Terra dentro do sistema, o atrito vira força interna, e o momento total volta a ser zero a todo instante. Olha o gráfico de baixo: é o espelho do de cima. O chão ganha momento, e depois devolve. Então fica a dica de ouro: quando a conta do momento não fecha, a primeira pergunta é sempre... quem eu deixei de fora do sistema?

## T10 — COMO A ENERGIA SE DIVIDE

### T10-1 — tela: os dois blocos, SEM ATRITO AGORA, disparam pela mola uma vez e param nos batentes; barras MOMENTO (iguais) e ENERGIA (diferentes) ficam; CONTA: SÓ FORÇA INTERNA (A MOLA); P⃗ = 0; m₁v₁ = m₂v₂ (MÓDULOS)
[thoughtful] Agora uma consequência que vai ser muito útil nos exercícios. Pega os mesmos dois blocos, só que agora sem atrito. A mola dispara os dois a partir do repouso, e a única força que age na horizontal é a da mola, uma força interna. Então o momento total continua zero, e os momentos dos dois blocos têm o mesmo tamanho, em sentidos opostos. Ou seja, a massa do primeiro bloco vezes a velocidade dele é igual à massa do segundo bloco vezes a velocidade dele. Repara nas barras: as de momento são iguais. Mas as de energia... não.

### T10-2 — tela: CONTA: K = p²/2m (DO VÍDEO ANTERIOR; MESMO MOMENTO: ENERGIA INVERSA À MASSA); m₁v₁ = m₂v₂ → v₁/v₂ = m₂/m₁ → K₁/K₂ = (m₁/m₂)(v₁/v₂)² = m₂/m₁
[curious] Por que as energias ficam diferentes? Do vídeo anterior, a gente sabe que a energia cinética é o momento ao quadrado dividido por duas vezes a massa. Se o momento é o mesmo nos dois, a energia fica inversamente proporcional à massa. Vamos passo a passo. A razão entre as velocidades é a razão inversa das massas: o bloco mais leve anda mais rápido. E, quando a gente coloca isso na razão das energias cinéticas, a velocidade entra ao quadrado, e sobra uma coisa bem simples: a energia do primeiro dividida pela energia do segundo é a massa do segundo dividida pela massa do primeiro.

### T10-3 — tela: REPLAY; CONTA: MOMENTO SE DIVIDE IGUAL; ENERGIA, NÃO; K₁ = 2 J, K₂ = 1 J; FRAÇÃO DO MAIS LEVE: 2/3 (67%); MASSAS IGUAIS: 50%; QUANTO MAIOR A DIFERENÇA DE MASSAS, MAIOR A FRAÇÃO DA ENERGIA CINÉTICA QUE FICA COM O MAIS LEVE
[thoughtful, emphatic] Ou seja: o momento se divide igualmente, mas a energia, não. Com os nossos blocos, o leve sai a dois metros por segundo e fica com dois joules. O pesado sai a um metro por segundo e fica com um joule. Dois terços da energia, uns sessenta e sete por cento, vão para o mais leve. Se as massas fossem iguais, seria meio a meio. E quanto maior a diferença entre as massas, maior a fração da energia que fica com o mais leve. Guarda esse resultado, que ele vai explicar por que levar um tiro é bem pior do que dar um.

### T10-4 — tela: DICA: MESMO MOMENTO: QUANTO MAIS LEVE, MAIOR A FRAÇÃO DA ENERGIA
Com a teoria na mão, bora para os exercícios!

## E6 — AGARRAR OU REBATER

### E6-1 — tela: EXERCÍCIO 6 · AGARRAR OU REBATER · SISTEMA: VOCÊ + A BOLA; (3D) o manequim parado no gelo dentro da fronteira VOCÊ + A BOLA; CONTA: M = 70,0 kg; m = 0,600 kg; v = 10,0 m/s; NA HORIZONTAL: SEM FORÇA EXTERNA; a bola chega em câmera lenta
[thoughtful] Primeiro exercício. Você está parado sobre um gelo sem atrito, e tem setenta quilogramas. Um amigo joga em você uma bola de seiscentos gramas, a dez metros por segundo. Primeiro passo, como sempre: o sistema é você mais a bola. E, na horizontal, não tem nenhuma força externa. Então o momento total na horizontal se conserva.

### E6-2 — tela: o manequim agarra a bola e desliza; AGARRA: 0,600 · 10,0 = (70,0 + 0,600) V; V = 6,0 / 70,6 = 0,085 m/s; UNS 8,5 CENTÍMETROS POR SEGUNDO
Primeiro caso: você agarra a bola. Antes, só a bola tinha momento: zero vírgula seis vezes dez, seis quilogramas metro por segundo. Depois, você e a bola seguem juntos, então esse momento se divide pela massa total, setenta vírgula seis quilogramas. A sua velocidade fica em uns oito centímetros e meio por segundo. Bem devagarinho.

### E6-3 — tela: virada para o rebate: a bola volta a 8,0 m/s; CONTA: AGARRA: V = 0,085 m/s; REBATE: 70,0 · V = 0,600 · (10,0 + 8,0); V = 0,154 m/s · QUASE O DOBRO; chip COMO A PAREDE DO VÍDEO ANTERIOR: REBATER TRANSFERE MAIS QUE AGARRAR
[curious] E se, em vez de agarrar, a bola bate no seu peito e volta a oito metros por segundo? Agora a bola não só perde todo o momento que tinha, como ainda ganha momento para o outro lado. E todo esse momento vai para você. Na conta, a sua massa vezes a sua velocidade é a massa da bola vezes dez mais oito. Dá uns quinze centímetros por segundo: quase o dobro de quando você agarrou. É o mesmo efeito da parede do vídeo anterior: rebater transfere mais momento do que agarrar.

### E6-4 — tela: barras de energia: AGARRAR: antes 30 J, depois 0,25 J (≈ 29,7 J em CALOR E DEFORMAÇÃO); REBATER: antes 30 J, depois ≈ 20 J (≈ 10 J perdidos); MOMENTO: CONSERVADO NOS DOIS; ENERGIA: EM NENHUM; DICA: NO MOMENTO O SISTEMA É VOCÊ + A BOLA. REBATER TRANSFERE MAIS QUE AGARRAR
[thoughtful, emphatic] E a energia? Antes do choque, a bola tinha trinta joules. Quando você agarra, sobram só uns zero vírgula vinte e cinco joules: quase trinta joules viram calor e deformação, na bola e nas suas mãos. Quando você rebate, sobram uns vinte, e uns dez se perdem. Ou seja: o momento se conservou nos dois casos, e a energia cinética, em nenhum. O momento se conserva em qualquer colisão. A energia cinética só se conserva se a colisão for elástica.

## E7 — O CAÇADOR NO LAGO

### E7-1 — tela: EXERCÍCIO 7 · O CAÇADOR NO LAGO · MOMENTO POR COMPONENTE; (3D) o caçador com a arma, LAGO CONGELADO · SEM ATRITO, fronteira CAÇADOR + ARMA + BALA; CONTA: M = 72,5 kg; m = 4,20 g; v = 965 m/s
[thoughtful] Segundo exercício. Um caçador está parado num lago congelado, sem atrito. Não me pergunte o que ele está caçando num lago congelado, mas tudo bem. Ele e a arma têm, juntos, setenta e dois vírgula cinco quilogramas. A bala tem quatro vírgula dois gramas e sai a novecentos e sessenta e cinco metros por segundo. O sistema é caçador, arma e bala.

### E7-2 — tela: TIRO HORIZONTAL; o caçador recua; CONTA: 0 = m v − M V; V = 0,00420 · 965 / 72,5 = 0,0559 m/s; UNS 5,6 CENTÍMETROS POR SEGUNDO: DÁ PARA VER
Primeiro, o tiro na horizontal. Antes do disparo, tudo parado: o momento total é zero. Depois, ele continua zero. Então o momento da bala para a frente é igual ao momento do caçador para trás. A velocidade de recuo é o momento da bala dividido pela massa do caçador: uns cinco vírgula seis centímetros por segundo. Pouquinho, mas dá para ver ele escorregando.

### E7-3 — tela: CÂMERA LENTA; o tiro sai a 56° acima da horizontal; aparece a normal do gelo (EXTERNA, IMPULSIVA) empurrando para cima durante o disparo; QUEM SEGUROU ELE?
[curious] Agora ele atira para cima, a cinquenta e seis graus da horizontal. A bala leva momento para cima... e, pela conservação, o caçador deveria ganhar momento para baixo. Só que ele não afunda no gelo. Então quem segurou ele?

### E7-4 — tela: p⃗_bala decomposto em pₓ e p_y (um X na parte vertical); cópia da parte horizontal volta no recuo; CONTA: N⃗ DO GELO: EXTERNA E IMPULSIVA; P_y NÃO SE CONSERVA; Pₓ SE CONSERVA; M V = m v cos 56°; V = 0,0559 · cos 56° = 0,031 m/s; UNS 3 CENTÍMETROS POR SEGUNDO
[thoughtful, emphatic] Foi o gelo! Durante o disparo, a força normal do gelo cresce de repente e segura o momento vertical. Ela é externa, e é impulsiva: grande, e bem rápida. Então, na vertical, o sistema não está isolado, e o momento vertical não se conserva. Mas na horizontal não tem atrito, então o momento horizontal se conserva. Por isso, só a parte horizontal do momento da bala volta para o caçador. A massa do caçador vezes a velocidade de recuo é a massa da bala vezes a velocidade dela vezes o cosseno de cinquenta e seis graus. O recuo cai para uns três centímetros por segundo.

### E7-5 — tela: REPLAY do tiro horizontal; barras de MOMENTO iguais (4,05 kg·m/s) e ENERGIA em escala log: bala ≈ 1.956 J, caçador ≈ 0,11 J; CONTA: K_bala/K_caçador ≈ 17.262 = 72,5 / 0,0042; ≈ 99,994% NA BALA; DICA: ISOLADO NA HORIZONTAL NÃO É ISOLADO NA VERTICAL
[curious] E a energia? Lembra do resultado da teoria: momentos iguais, e quem tem menos massa fica com mais energia. Olha as barras. Os momentos são iguais. Mas a bala sai com quase dois mil joules, e o caçador recua com uns onze centésimos de joule. A energia da bala é umas dezessete mil vezes maior, que é exatamente a massa do caçador dividida pela massa da bala. Praticamente toda a energia cinética, mais de noventa e nove vírgula nove por cento, fica na bala. Por isso o recuo não machuca ninguém... e a bala, sim.

## E8 — OS GASES DO RIFLE

### E8-1 — tela: EXERCÍCIO 8 · OS GASES DO RIFLE · QUEM ESTÁ NO SISTEMA?; rifle num APOIO FROUXO; o tiro uma vez + REPLAY; 601 m/s EM RELAÇÃO AO CANO; 1,85 m/s EM RELAÇÃO AO CHÃO; CONTA: m_rifle = 2,80 kg; m_bala = 7,20 g; OS GASES CARREGAM MOMENTO?
[curious] Mais um tiro, agora com uma pegadinha. Um rifle de dois vírgula oito quilogramas, solto num apoio frouxo, dispara uma bala de sete vírgula dois gramas. A bala sai a seiscentos e um metros por segundo... em relação ao cano. E o rifle recua a um vírgula oitenta e cinco metros por segundo, em relação ao chão. A pergunta é: os gases da explosão, que saem junto com a bala, carregam algum momento?

### E8-2 — tela: CONTA: v_bala,chão = 601 − 1,85 = 599,15 m/s (O CANO ANDA PARA TRÁS); setas: p_bala = +4,31 kg·m/s e p_rifle = −5,18 kg·m/s
[thoughtful] Primeiro, cuidado com a velocidade da bala. Os seiscentos e um metros por segundo são medidos em relação ao cano, e o cano está andando para trás. Então, em relação ao chão, a bala anda seiscentos e um menos um vírgula oitenta e cinco: quinhentos e noventa e nove vírgula quinze metros por segundo. Com isso, o momento da bala fica em quatro vírgula trinta e um quilogramas metro por segundo, para a frente. E o momento do rifle, massa vezes velocidade, dá cinco vírgula dezoito, para trás.

### E8-3 — tela: NÃO FECHA; a nuvem de GASES aparece com p_gases = +0,866 kg·m/s; Σp = 0
Só que, antes do tiro, estava tudo parado, e o momento total era zero. E essas duas setas não se cancelam: a do rifle é maior. Falta alguém na conta. São os gases! Eles são aqueles convidados que ninguém chamou, mas que aparecem na foto. E carregam uns zero vírgula oitenta e sete quilogramas metro por segundo para a frente. Agora, sim, a soma dá zero.

### E8-4 — tela: SISTEMA = BALA + RIFLE + GASES (a fronteira inclui os gases); DICA: VELOCIDADE EM RELAÇÃO AO CANO NÃO É EM RELAÇÃO AO CHÃO. A CONTA FECHA COM OS GASES
[thoughtful, emphatic] A lição é a mesma dos blocos com a Terra: a conservação vale para o sistema inteiro. O sistema certo aqui é bala, rifle e gases. Se a conta do momento não fecha, quase sempre tem alguém escondido que você deixou de fora.

## E9 — NEWTON E A LUZ

### E9-1 — tela: EXERCÍCIO 9 · NEWTON E A LUZ · IMPULSO NORMAL; retrato estilizado SÉCULO XVII; RAIO DE LUZ = FLUXO DE CORPÚSCULOS; O IMPULSO EXPLICA REFLEXÃO E REFRAÇÃO?
[curious] Para fechar os exercícios, um problema que mistura física e história. No século dezessete, o Newton defendia que a luz era feita de corpúsculos: bolinhas minúsculas e muito rápidas. Então um raio de luz seria um fluxo dessas bolinhas. E a pergunta é: será que o impulso consegue explicar a reflexão e a refração da luz nesse modelo?

### E9-2 — tela: ESPELHO; um corpúsculo bate e volta; o impulso J⃗ NORMAL, perpendicular à superfície; ANTES e DEPOIS com as componentes; TANGENCIAL: IGUAL; NORMAL: INVERTIDA; θ₁′ = θ₁
[thoughtful] Vamos começar pela reflexão. O espelho só consegue empurrar na direção perpendicular à superfície, a direção normal. Então o impulso que o corpúsculo recebe é todo normal. E o que esse impulso faz? Inverte a parte normal da velocidade, e não mexe na parte paralela ao espelho. Repara nas setinhas: antes e depois, a parte paralela é igual, e a parte normal trocou de sentido. Resultado: o ângulo de reflexão é igual ao ângulo de incidência. Até aqui, o Newton está mandando bem.

### E9-3 — tela: AR → ÁGUA; o impulso J⃗ NORMAL puxa o corpúsculo para dentro da água; A TANGENCIAL SE CONSERVA; ÂNGULOS MEDIDOS DA NORMAL; v₁ sen θ₁ = v₂ sen θ₂
Agora a passagem do ar para a água. No modelo de Newton, a superfície da água também dá um impulso só normal, puxando o corpúsculo para dentro. Então, de novo, a parte da velocidade paralela à superfície se conserva. Escrevendo isso com os ângulos medidos a partir da normal: a velocidade no ar vezes o seno do ângulo no ar é igual à velocidade na água vezes o seno do ângulo na água.

### E9-4 — tela: CONTA: sen θ₁ / sen θ₂ = CONSTANTE (A FORMA DA LEI DE SNELL) → no modelo de Newton: = v₂/v₁
[curious] Arrumando essa igualdade, aparece uma coisa conhecida: o seno do ângulo no ar dividido pelo seno do ângulo na água é uma constante. Essa é a forma da lei de Snell! Só que, no modelo de Newton, essa constante é a velocidade na água dividida pela velocidade no ar. Guarda essa ordem, porque é aqui que mora o problema.

### E9-5 — tela: o raio SE APROXIMA DA NORMAL na água; CONTA: θ₂ < θ₁ ⇒ v₂/v₁ > 1; NEWTON: LUZ MAIS RÁPIDA NA ÁGUA
[thoughtful] Agora olha o que acontece de verdade: ao entrar na água, a luz se aproxima da normal. O ângulo na água é menor que o ângulo no ar. Então o seno do ângulo no ar dividido pelo seno do ângulo na água é maior que um. E, pelo modelo, isso quer dizer que a velocidade na água teria que ser maior que a velocidade no ar. Os corpúsculos acelerariam ao entrar na água.

### E9-6 — tela: 1850 · FOUCAULT · A LUZ É MAIS LENTA NA ÁGUA; a PREVISÃO DE NEWTON v₂ > v₁ é riscada; ao lado, na DESCRIÇÃO ONDULATÓRIA: sen θ₁ / sen θ₂ = v₁/v₂
[excited] E durante quase dois séculos ninguém conseguiu medir isso. Até que, em mil oitocentos e cinquenta, o Foucault mediu a velocidade da luz na água... e ela era mais lenta! A previsão do modelo corpuscular caiu. Na descrição ondulatória, a relação aparece invertida: o seno do ângulo no ar dividido pelo seno do ângulo na água é a velocidade no ar dividida pela velocidade na água. E é essa que a natureza segue.

### E9-7 — tela: os corpúsculos apagados; CONTA: IMPULSO CERTO + MODELO ERRADO = PREVISÃO TESTÁVEL; DICA: O IMPULSO É NORMAL: SÓ A COMPONENTE NORMAL DA VELOCIDADE MUDA
[thoughtful] E repara numa coisa bonita: o teorema do impulso estava certo o tempo todo. O que estava errado era o modelo da luz. Uma física correta, aplicada com cuidado num modelo errado, fez uma previsão que dava para medir. E a natureza decidiu. Até o Newton errou, o que, convenhamos, é um alívio para todo mundo.

## CODA — A LUZ TAMBÉM TEM MOMENTO

### C-1 — tela: dois painéis: SUPERFÍCIE PRETA · ABSORVE e ESPELHO · REFLETE; feixe amarelo com fótons-pacote e seta p⃗; flash laranja na preta, retorno no espelho; Δp_placa = p − (−p) = 2p; placas penduradas inclinando 1:2, F⃗ e 2F⃗; CONTA: p = E/c; Δp/Δt = F · MOMENTO POR SEGUNDO É FORÇA
[curious] Só que a história tem uma virada. O modelo do Newton errou a velocidade da luz na água, mas a luz carrega momento de verdade. O momento de um pulso de luz é a energia dele dividida pela velocidade da luz. Olha as duas placas. Na preta, a luz é absorvida: a placa recebe o momento da luz e pronto. No espelho, a luz volta: a placa recebe o momento de ida e ainda o de volta, ou seja, o dobro. E, como a luz chega o tempo todo, a placa recebe momento a cada segundo. E momento por segundo é força. Por isso o espelho é empurrado com o dobro da força da superfície preta.

### C-2 — tela: (3D) vela solar refletora no espaço, com fótons em riscos amarelos e a seta FORÇA DA LUZ NA VELA; CONTA: LUZ DO SOL 1.361 W/m²; 4,5 μPa ABSORVIDA; 9,1 μPa REFLETIDA; VELA SOLAR DE 100 M² REFLETORA ≈ 0,9 mN; NO VÁCUO, EMPURRANDO O TEMPO TODO; laser de 1 W: 3,3 nN
[thoughtful] Só que é uma força pequenininha. A luz do Sol chega aqui com mil trezentos e sessenta e um watts por metro quadrado. Isso empurra com uns quatro vírgula cinco micropascais, se a luz for absorvida, e com o dobro, uns nove micropascais, se for refletida. Uma vela solar refletora de cem metros quadrados recebe uns nove décimos de milinewton. É mais ou menos o peso de uns três grãozinhos de arroz. Parece nada... mas no vácuo não tem atrito, e a luz empurra o tempo todo, sem parar. Com paciência, dá para navegar no espaço. E um laser de um watt empurra com uns três vírgula três nanonewtons.

### C-3 — tela: a vela se afasta (a câmera acompanha); O MODELO DO NEWTON CAIU. · A CONSERVAÇÃO DO MOMENTO FICOU. · VALE PARA A LUZ, NA FÍSICA QUÂNTICA E EM TUDO O QUE A GENTE SABE MEDIR
[thoughtful, emphatic] Então, o modelo do Newton caiu. Mas a conservação do momento ficou. Ela vale para a luz, vale na física quântica, onde o momento nem é mais massa vezes velocidade, e vale em tudo o que a gente sabe medir.

## SÍNTESE

### S1 — tela: RESUMO; o cavalo e a pedra com a fronteira SISTEMA, a corda em cinza (INTERNA), CHÃO NA PEDRA e CHÃO NAS PATAS em azul-claro; QUEM ACELERA O CAVALO E A PEDRA É O CHÃO
[calm, satisfied] Então, voltando à pergunta do começo. A corda puxa, sim, o cavalo para trás. Mas, no sistema cavalo, corda e pedra, ela é uma força interna, e força interna não muda o momento do sistema. Quem acelera o cavalo e a pedra é o chão, uma força externa. A pergunta inicial está respondida.

### S2 — tela: o cavalo no PALCO + três ideias com ícones: dP⃗/dt = F⃗^ext · COMPONENTE POR COMPONENTE; MOMENTO SE DIVIDE IGUAL; ENERGIA, NÃO; NÃO CONSERVA? AUMENTE O SISTEMA; a fronteira cresce até + TERRA
[thoughtful] Resumindo em três ideias. Primeira: a taxa de variação do momento total só depende da força externa resultante, e isso vale componente por componente. Segunda: quando um sistema se separa por forças internas, o momento se divide igualmente, mas a energia cinética vai principalmente para o mais leve. E terceira: quando a conta do momento não fecha, aumenta o sistema até ela fechar.

## ENCERRAMENTO

### EN1 — tela: logo com anéis; INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS
Se essas conexões ajudaram você, se inscreve no Parallax Lab para acompanhar os próximos vídeos.

### EN2 — tela: granada explodindo no ar, um ponto seguindo a parábola; SE A GRANADA EXPLODE NO AR, O QUE CONTINUA NA PARÁBOLA? → PRÓXIMO VÍDEO: CENTRO DE MASSA
[curious] E fica a pergunta para o próximo: se uma granada explode no meio do voo, os pedaços voam para todo lado... mas uma coisa continua exatamente na mesma parábola. O quê? No próximo vídeo: centro de massa. Até a próxima!

---

## Números de conferência (handoff v1; g = 9,8 m/s²)

| Bloco | Valor falado | Exato |
|---|---|---|
| T8 | 2.352 N; 2.800 N; 448 N; 1.400 kg; 0,32 m/s²; 2.608 N; 192 N; μe 0,1 → 588 N; −1,26 m/s² | 2352; 2800; 448; 1400; 0,32; 2608; 192; 588; −1,26 |
| T9 | 14 m/s; Terra ≈ 6×10²⁴ kg; 2,3×10⁻²⁴ m/s; ±2 kg·m/s; μ 0,2; 1,96 N; 3,92 N; 0,51 s; −1,0; 1,02 s | 14,0; 5,97e24; 2,35e-24; 2; 0,2; 1,96; 3,92; 0,510; −1,0; 1,020 |
| T10 | 2 m/s e 1 m/s; 2 J e 1 J; 2/3 (67%); 50% (iguais) | 2; 1; 2; 1; 66,7%; 50% |
| E6 | 6 kg·m/s; 70,6 kg; 8,5 cm/s; 15 cm/s; 30 J → 0,25 J (≈ 29,7 J); ≈ 20 J (≈ 10 J perdidos) | 6,0; 70,6; 0,0850; 0,1543; 30; 0,255; 20,03 |
| E7 | 5,6 cm/s; 56°; 3 cm/s; ≈ 1.956 J e ≈ 0,11 J; ≈ 17 mil; 99,99% | 0,0559; 0,0313; 1955,6 e 0,113; 17.262; 99,994% |
| E8 | 599,15 m/s; 4,31; 5,18; 0,87 kg·m/s | 599,15; 4,314; 5,18; 0,866 |
| Coda | 1.361 W/m²; 4,5 e 9,1 μPa; 0,9 mN; 3,3 nN | 1361; 4,54; 9,08; 0,908; 3,34 |

## O que mudou em relação à narracao_v3.md

- **Tom:** conectivos variados em todos os blocos ("Vamos por partes", "Repara", "Ou seja", "Então", "Só que", "Agora sim"), perguntas
  retóricas antes de cada conta e brincadeiras curtas (cavalo teimoso, cavalo de patins, viagem à Lua do Cyrano, caçador no lago,
  gases "convidados que ninguém chamou", "até o Newton errou").
- **Mais explicação onde a tela já mostra mais:** T7-6 (por que a diagonal é vazia), T8-3 (mostrador da velocidade), T8-6 (a
  desaceleração de 1,26 m/s² que a CONTA mostra), T9-5 (o coeficiente 0,2 e por que o atrito no pesado é o dobro), T9-6 (por que o
  momento sobe depois que o pesado para), T10-3 (as velocidades 2 e 1 m/s antes das energias), E6-4 (os ≈ 10 J perdidos no rebate,
  que as barras mostram), E7-4 (o que é força impulsiva), E8-1 (o apoio frouxo e a massa do rifle e da bala, que estão na CONTA),
  C-1 (por que o espelho recebe o dobro).
- **Hook:** mesmas três ideias, com "era para dar empate"; fica em ~60 palavras (~22 s nominais, contra 24,8 s da v3).
- **Tags:** `[emphatic]` sozinho virou `[thoughtful, emphatic]` (descritor recomendado no guia); `[calm]` do S1 virou `[calm, satisfied]`; o segundo `[excited]` entrou na resposta do hook (T8-5).
- **CTA:** "Se essas conexões ajudaram você…" (frase padrão do guia).

## Pontos a confirmar antes da voz

1. **C-2, laser de 1 W (3,3 nN):** a análise do v4 não mostrou o valor na tela nos quadros conferidos (o painel termina em "NO VÁCUO,
   EMPURRANDO O TEMPO TODO"). Se ele não aparece no fim do bloco, cortar a última frase do C-2 ou acrescentar o valor na tela.
2. **C-2, "o peso de um grãozinho de arroz":** 0,9 mN ≈ 0,09 g-força; um grão de arroz cru tem ~0,02–0,03 g. A comparação é da ordem de
   grandeza de "uns três ou quatro grãos de arroz". Se quiser exatidão, trocar por "o peso de uns três grãos de arroz" ou tirar.
3. **T9-2, massa da Terra:** a fala diz "uns seis vezes dez elevado a vinte e quatro"; a tela mostra 5,97 × 10²⁴. Arredondamento só na fala.
4. **E9-6:** Foucault, 1850, luz mais lenta na água — fato bem estabelecido; conferir a fonte só se for para a descrição.
5. **T7-9:** a observação sobre cargas em movimento e momento do campo é qualitativa, sem esquema de forças (como no handoff v1).
6. **E7-1, brincadeira do lago:** se soar como crítica à caça, trocar por "Não me pergunte por que alguém atira em cima de um lago
   congelado, mas a física agradece".
