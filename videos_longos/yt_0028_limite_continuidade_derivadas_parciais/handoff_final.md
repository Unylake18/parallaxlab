# yt_0028 · CÁLCULO III · EP. 03 · Limite, continuidade e derivadas parciais · HANDOFF FINAL
**Ajustes de tela + voz + sincronização + legenda `.srt` + render 1080p + master + entrega** (arquivo único e autocontido; a narração está dentro dele)

2026-11-11. Base: preview v4 (922,5 s ≈ 15:22, 960×540, 15 fps, sem voz), que o Kaio aprovou como base. O fechamento é a lista do §2. A narração é a do §3 (v5: a da Produção com o refino do GPT filtrado). Este documento substitui os handoffs v1 a v4 do yt_0028 **no que diverge**. Matemática, números, paleta, caneta, malha, canto, fundo violeta com grade dos eixos e os 37 alvos v4 seguem como estão.

---

## 0. Autorização, fases e modo de execução

**Fases explicitamente abertas pelo Kaio nesta unidade:** fechamento visual (§2), **voz (ElevenLabs v4)**, **sincronização**, **legenda `.srt`**, **render final 1080p**, **master** e **entrega** em `entregas/`.

**Não abertas (não fazer):**
- publicação, capa, `commit`, `push`, `branch`, PR;
- qualquer mudança em `template/`, `assets/`, `pyproject.toml`, `uv.lock`, `AGENTS.md` ou `docs/`.

Só a unidade `videos_longos/yt_0028_limite_continuidade_derivadas_parciais/` pode ser alterada, além de `renders/` e `entregas/`, que são saída. Pode **copiar** scripts do yt_0026 ou do yt_0027 para dentro da unidade, sem alterar esses vídeos.

**Modo de execução (importante):** não encerre a vez entre etapas. Depois de lançar um render ou a geração de voz, espere na mesma vez (comando em primeiro plano com timeout de até 10 min por lote, ou laço `until` que consulta o arquivo de saída) e siga direto para a auditoria. Mensagem de progresso não é entrega.

**Só há duas paradas permitidas:**
1. A variável `ELEVENLABS_API_KEY` não existe na sessão. Peça ao Kaio; **nunca** grave a chave em arquivo, commit, log ou relatório.
2. O WAV gerado passa de **17:30**. Reporte a duração e pare: quem decide cortes é a Produção.

Qualquer outra dúvida: escolha a leitura mais provável, diga qual e siga.

Ordem: **§2 ajustes → §4 voz → §5 sincronização → §6 conferência 540p com voz → §7 render 1080p → §8 QA e entrega → §9 relatório.** Pare só depois do relatório.

Guarde este arquivo na unidade como `handoff_final.md`.

---

## 1. Estado de partida
- **Unidade:** `videos_longos/yt_0028_limite_continuidade_derivadas_parciais/`.
  - Lotes: **PH, PB1, PB2, PB3, PB4, PB5, PB6, PB7, PS** (`cena.py`). Sem 3D.
  - Kit: `kit.py` e `v28.py`. Âncoras: `narracao.md` → `gerar_ancoras.py` → `ancoras.json`.
  - Fundo: `assets/calculo/papel.py` v2 (violeta liso + grade dos eixos), variante B (`FUNDO_PAINEL = "grade"`). Nada global muda.
- **Pipeline de voz:** o do yt_0026 v9 / yt_0027, mesma família de kit. **Se o yt_0027 já tiver as versões adaptadas, copie de lá** (são mais novas); senão, do yt_0026 (`videos_longos/yt_0026_funcoes_vetoriais_campos/`):
  - `alinhar_voz.py` (alinhamento forçado + STT de conferência);
  - `gerar_ancoras.py` no modo "tempo real da voz";
  - `gerar_srt.py`, `render1080.sh`, `montar_final.py`, `qa_parado.py`, `qa_canto.py`, `qa_fundo.py`;
  - `conferencia_v9.md` como exemplo de relatório de tempo.

  Adapte nomes, lotes e caminhos. O `qa3d*.py` não se aplica (sem 3D).
- **Não reabrir:**
  - matemática e números (Anexo A);
  - o fio do vídeo: o quadradinho do gancho que deforma com rot = 0 e div = 0, respondido no B7;
  - a ordem H → A → B1 → B2 → B3 → B4 → B5 → B6 → B7 → S;
  - pedacinho de fluido (chapa + malha 4×4 + contorno), cores, canto, fundo violeta e grade dos eixos;
  - nada de livros nem do Atlas na tela ou na fala.
- **A cena segue a voz:** nos longos a voz é um WAV contínuo e a cena se estica. Os tempos do preview v4 **não valem mais**: todos os lotes serão re-renderizados com a linha do tempo da voz.
- **Quadros-alvo:** `referencia_v4/` (alvos 01 a 37) continua valendo. Os novos estão em `yt_0028_quadros_alvo_v5/` (alvos **38 a 42**, prancha `00_folha_contato_v5.jpg` e o gerador `sb28v5.html`, chaves `ab1`, `ab2`, `gan`, `b1m`, `b3w`): copie a pasta para `referencia_v5/`.
- **Duração prevista:** 2.861 palavras, cerca de 15,9 min de fala a 3 palavras/s (cadência de referência do Kaio).

---

## 2. Ajustes de cena (lista fechada)

Cada item diz a âncora, o que muda e como fica. **Alvo NN** é o quadro de `referencia_v4/` ou `referencia_v5/`, com ±20 px de posição e ±5 % de tamanho; mesmo texto e mesmas cores.

### 2.1 A1: abertura com a logo clássica (alvos 38 e 39)
- **Problema (Kaio):** no v4 a logo some quando entra o título, e o título fica 16 s sozinho.
- **Como fica:** a logo fica na tela **durante todo o A**.
  - **Bloco da logo:** copie o do A1 do yt_0027 (ou o do CTA do próprio vídeo): mesma imagem, mesmos dois anéis tracejados, mesma posição e tamanho. Nada de brilho, pulso ou rotação nova. O alvo usa o arquivo de logo do projeto só para mostrar a composição.
  - **Etapa 1 (alvo 38):** logo grande, centralizada, e embaixo `BEM-VINDOS AO PARALLAX LAB` (Space Grotesk 46, branco).
  - **Etapa 2 (alvo 39):** a logo sobe e diminui (largura ≈ 380 px, centro em y ≈ 250), em 0,5 s. Entram, nesta ordem, `CÁLCULO III` (SGM 28, GEO, y = 478), o título `LIMITE, CONTINUIDADE E DERIVADAS PARCIAIS` (SG 54, y = 566), `NESTE VÍDEO:` (SG 30, `#2EE6A0`, y = 646) e quatro linhas centradas (SG 36 em branco + SGM 36 em `#8CFFD2`, y = 722, 775, 828 e 881), cada uma com a forma `O LIMITE · CHEGAR PERTO`.
  - **Sem número de episódio na tela.**
- **Gatilhos (frases de A1; a 3 palavras/s, a contar do início do A, como referência):**

  | Frase | Tela |
  |---|---|
  | "Fala, pessoal! Bem-vindos ao Parallax Lab!" | etapa 1 (logo grande e `BEM-VINDOS…`) |
  | "Esse é o terceiro episódio da nossa série de Cálculo três." | a logo sobe e diminui; entra `CÁLCULO III` |
  | "Para isso, entram três ideias" | entra o título; depois `NESTE VÍDEO:` |
  | "Primeiro, o limite" | linha `O LIMITE · CHEGAR PERTO` |
  | "Depois, a continuidade" | linha `A CONTINUIDADE · NÃO PULAR` |
  | "E, por fim, as derivadas parciais" | linha `AS DERIVADAS PARCIAIS · MEDIR A MUDANÇA` |
  | "uma tabela de quatro números" | linha `A TABELA · GIRO, ÁREA E DEFORMAÇÃO` |
  | "Então vamos começar pelo chão" | tudo sai (FadeOut 0,4 s) enquanto o B1 entra; o canto entra aqui (R10) |

  O trecho de A1 tem ≈ 49 s. A tela **não fica parada**: entra algo a cada frase (a tabela acima).

### 2.2 S2: gancho do próximo vídeo e CTA (alvo 40)
- **Problema:** hoje o gancho é só uma frase falada, e o CTA entra direto depois do resumo.
- **Como fica:** na frase **"No próximo vídeo"**, o resumo sai (FadeOut 0,4 s) e entra o cartão:
  - `NO PRÓXIMO VÍDEO` (SGM 34, GEO, y = 215) e `EXERCÍCIOS DO MÓDULO` (SG 72, y = 305);
  - cinco cartões 300×300 em y 410 a 710, x = 120, 465, 810, 1155 e 1500 (grade do eixo dentro, escala 60 px/u, quadradinho 30 px, moldura de 4 px na cor de cada um);
  - nomes embaixo (SG 28, cor do cartão, duas linhas onde precisar): `CAMPO VETORIAL` (GEO), `ROTACIONAL` (`#9C8CFF`), `DIVERGENTE` (`#7FB2FF`), `LIMITE E CONTINUIDADE` (`#8CFFD2`), `DERIVADAS PARCIAIS` (`#FFC24D`);
  - conteúdo das miniaturas, reaproveitando peças do próprio vídeo: o campo (x, −y); o campo `(−y, x)` com o quadradinho girado 0,6 rad; o campo `(x, y)` com o quadradinho 1,3×; o disco ε com a seta L e a seta F(X); `∂F/∂x` (âmbar no x) sobre `∂F/∂y` (magenta no y).
- **Gatilhos:**

  | Frase | Tela |
  |---|---|
  | "No próximo vídeo, é a vez de colocar a mão na massa" | resumo sai; entra o título do cartão |
  | "o integrador do módulo, só com exercícios" | `EXERCÍCIOS DO MÓDULO` |
  | "Campo vetorial" / "rotacional" / "divergente" / "limite e continuidade" / "derivadas parciais" | as cinco miniaturas, uma por expressão (FadeIn 0,3 s) |
  | "Se essa aula te ajudou" | o cartão sai e entra o **CTA padrão** do v4: logo com os dois anéis e `INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS`, até o fim da fala + 3 s |

- Na tela, **sem** o nome "3.1-E1", sem duração e sem Atlas: só o tema.

### 2.3 M1: nascimento dos campos em onda (todas as primeiras entradas)
- **Problema (Kaio):** os campos aparecem inteiros de uma vez e depois ficam parados.
- **Como fica:** na **primeira entrada** de cada campo no vídeo (H1, B1-1, B2-1, B3-1, B4-1, B5-1, B6-1 e os campos dos alvos 18 a 21), as setas nascem em onda a partir do ponto de interesse (P, ou a origem quando não há P), cada seta crescendo de tamanho zero ao comprimento final, com defasagem proporcional à distância (`lag_ratio`), em **0,8 s** no total. Sem updater: animações por seta. Reentradas do mesmo campo (volta de um zoom, troca de cena com o mesmo campo) mantêm o FadeIn atual.
- As regras R1, R5 e R7 valem **durante** a onda (nenhuma seta nasce em cima de texto ou fora da moldura).
- Sem loop, sem pulso, sem brilho: a onda acontece uma vez.

### 2.4 M2: seta em destaque no B1 (alvo 41)
- **Problema:** a seta do ponto X é minúscula; os rótulos `F(X)` e `L` ficam encostados nas hastes (≈ 1:41 do v4).
- **Como fica (B1-1 e B1-2):**
  - A seta de X no painel esquerdo fica **maior** (≈ 2× o comprimento de campo, traço 9, cabeça 28, `#8CFFD2`), com o ponto X laranja de raio 8. A clareira ao redor dela (R1) é recalculada.
  - Na frase **"eu trago essa seta para a mesma origem"**, uma cópia da seta viaja do ponto X até a origem do painel direito em **0,6 s** (sem rastro), e vira o `F(X)` do painel direito. A cópia a meio caminho está no alvo 41.
  - No B1-2, a cada passo da aproximação, a nova seta de X faz o mesmo percurso uma vez.
  - Rótulos do painel direito: `F⃗(X)` na ponta da seta, afastado 14 px, e `L⃗` na ponta da seta-alvo, também afastado 14 px (alvo 41). Placa mínima (R2).
- Legenda `A CÓPIA DA SETA VIAJA PARA A ORIGEM` só no alvo, para mostrar o instante; **não** entra no vídeo.

### 2.5 M3: caminhantes na continuidade (B3-2, alvo 42)
- **Problema:** os três cartões ficam parados por cerca de 50 s.
- **Como fica:** em cada cartão, um ponto X (laranja, raio 8) chega ao ponto especial por uma trilha tracejada curta (GEO), e a seta de X fica em destaque (traço 9, `#8CFFD2`). A trilha **não** persiste depois do movimento. Cada caminhante dura 1,5 a 2,5 s e termina no estado do alvo 42.
  - **Cartão ① (carga):** na frase "No campo elétrico de uma carga", X anda em linha reta até perto da carga (de (−3,1; 1,8) até (−1,7; 1,0) em unidades do cartão). A seta de X **cresce** à medida que X se aproxima (comprimento ∝ 1/r², com teto que caiba no cartão).
  - **Cartão ②:** na frase "dependendo do caminho por onde você chega", três caminhantes em sequência, cada um ~1,2 s: pelo eixo horizontal (seta zero: não há seta), pela diagonal de subida (seta `→` de tamanho 1) e pela outra diagonal (seta `←`). O estado final do alvo mostra o da diagonal de subida.
  - **Cartão ③:** na frase "Chegando de qualquer lado", X anda pelo eixo horizontal desde a esquerda, a seta de X fica `→` o tempo todo; só em cima do ponto a seta do centro (`↑`) é a que vale.
- Os rótulos `① FORA DO DOMÍNIO`, `② SEM LIMITE`, `③ SALTO NO PONTO` e as legendas atuais continuam, entrando nas mesmas frases de hoje.
- R5 e R7 valem: a seta destacada só é desenhada onde cabe na moldura, e as setas de campo na vizinhança dela saem (clareira).

### 2.6 M4: o quadradinho age uma vez no B7-3 (alvos 32 e 34)
- **Problema:** os três quadradinhos já aparecem deformados; o movimento é justamente a mensagem.
- **Como fica:** quando os três cartões entram, cada quadradinho aparece **na posição original** (contorno tracejado mais o quadradinho com malha). Na frase "Olha cada um agindo no quadradinho", cada um faz a sua transformação **uma vez**, em ≈ 1,0 s, e **fica** no estado final do alvo:
  - "o redemoinho gira": gira 0,6 rad;
  - "a explosão cresce": lados ×1,42 (a área dobra);
  - "a deformação estica de um lado e achata do outro": largura ×1,5 e altura ÷1,5.
- O movimento segue o fluxo do campo do cartão; o tracejado original fica como referência.

### 2.7 Tag `ZOOM × 10 · MODELO LINEAR LOCAL`
- **Problema:** nas âncoras B6-1 a B6-4 ela fica empilhada embaixo do título do canto (três linhas no canto), e repete no resumo.
- **Como fica:** a tag vai para **dentro da moldura do palco, no canto inferior esquerdo** (x = 150, y = 878, SGM 26, placa mínima). No resumo (S1) ela **sai**.

### 2.8 Sem mudança de tela, só de tempo
Todas as outras âncoras mantêm a tela do preview v4. A fala nova mexe em algumas frases-gatilho (Anexo D): reconecte cada evento à frase equivalente do texto novo e liste no relatório (§9). A tela do B5-3 (alvo 20) continua com `CLASSE C¹: AS PARCIAIS EXISTEM E SÃO CONTÍNUAS`; a fala acrescenta "numa vizinhança do ponto" e "suficiente para a aproximação linear", sem mudar a tela. Hold só com informação na tela.

### 2.9 Ficha
- Atualize `duracao_alvo` (voz real) e `Status`.
- `quadros_alvo`: inclua `referencia_v5/` (alvos 38 a 42).
- `3d_threejs`: nenhuma cena; `solido_3d` continua `nenhum do arsenal Blender`.
- Mantenha `Série pública: **CÁLCULO III · EP. 03**` e `# Limite, continuidade e derivadas parciais`.

---

## 3. Narração final (texto para gravação)

**Uso:**
- Copie a seção "Texto corrido (para gravação)" abaixo para `narracao_tags.md` da unidade, com o título exato `## Texto corrido (para gravação)` e **sem mudar uma palavra**. (O arquivo pronto, `narracao_tags.md`, vem no zip.)
- Troque o `narracao.md` da unidade pelo `yt_0028_narracao_v5_por_ancora.md` do zip (Anexo E tem o mesmo conteúdo). É o mesmo texto, separado por âncora, com os `tela:` atualizados; é a fonte do `ancoras.json`.
- O texto limpo (para legenda e transcrição) é o mesmo sem os `[ ]`. Gere `narracao_limpa.md` e copie os dois para `texto/` na entrega.
- Cada parágrafo é **um trecho contínuo de voz**; não há pausas marcadas.

**Números e tags:**
- **2.861 palavras.** A 3 palavras/s: cerca de 15,9 min de fala. A duração real vem do WAV. Não corte nada: acima de 17:30 é a segunda parada permitida (§0).
- **Tags** (`docs/roteiro_voz_elevenlabs_v4.md`): `[thoughtful]` e `[curious]` na base; `[thoughtful, emphatic]` nos conceitos; `[happy]` no Bem-vindos e na chamada de inscrição; `[excited]` no gancho do próximo vídeo. Sem `[slowly]` e sem `[pause]`. Se uma tag for lida em voz alta, troque por uma vizinha e regere só o bloco.
- Variáveis pelo nome e pronúncia: "cê um" é C¹ e "cê erre" é Cʳ (já escritos assim no texto).

**Física conferida:** Anexo A. O texto foi conferido frase a frase contra o v4 e os números da sympy (`verifica_calc3_t3_sympy.py`: 63 checagens, todas `True`, no zip).

## Texto corrido (para gravação)

[curious] Lembra do campo que fechou o episódio passado? A componente horizontal é o próprio x, e a vertical é menos y. Coloca um quadradinho de fluido no meio e faz as contas que a gente já conhece. O rotacional dá zero, em todo ponto: nenhuma rodinha gira. O divergente também dá zero: nenhum pedacinho muda de área. Então, pelas duas medidas, não era para acontecer nada, certo?

[thoughtful] Só que agora deixa o fluido andar… e olha o que acontece: o quadradinho estica para os lados e achata na vertical. A área continua a mesma, e ele não girou nem um grau. Mas a forma mudou completamente.

[curious] Então tem alguma coisa nesse campo que o rotacional e o divergente não enxergam. Que número mede isso? E de onde ele sai? A resposta está nas derivadas parciais do campo. Só que, para usar essas derivadas com segurança, a gente precisa começar pelo chão: o que quer dizer chegar perto de um ponto.

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab! Esse é o terceiro episódio da nossa série de Cálculo três. Hoje a gente olha um campo vetorial bem de pertinho. [thoughtful] Porque a seta de um ponto não basta: é preciso entender as setas vizinhas. Para isso, entram três ideias, uma apoiada na outra. Primeiro, o limite: o que quer dizer chegar perto de um ponto, com o épsilon e o delta desenhados, e não só escritos. Depois, a continuidade: quando a seta não dá pulo, e três jeitos de ela falhar. E, por fim, as derivadas parciais, que medem como a seta muda em cada direção. [curious] No meio do caminho tem um engano, em que as derivadas parciais mentem sobre o campo. E, no final, a gente junta tudo numa tabela de quatro números, que revela o giro, a mudança de área e aquela deformação do quadradinho que ficou sem explicação. [happy] Então vamos começar pelo chão: o que é chegar perto?

[thoughtful] Vamos usar duas telas. Na da esquerda está o campo, e é ali que você anda: tem um ponto fixo, e você vai se aproximando dele. A seta do lugar onde você está fica em destaque. Na da direita, eu trago essa seta para a mesma origem, para comparar só onde a ponta dela chega. Uma tela mostra por onde você anda; a outra, onde a seta chega.

[curious] Conforme você chega perto do ponto, a ponta da seta vai chegando perto de uma seta-alvo. Essa seta-alvo é a candidata a limite. Os dois números de baixo contam a história: a distância até o ponto encolhe, e a distância da ponta até o alvo encolhe junto. Só que "encolhe junto" ainda é vago. Perto quanto? Então a definição vira um desafio.

[thoughtful] Primeiro, alguém escolhe uma tolerância na chegada: um disquinho de raio épsilon em volta da ponta do alvo. É como se dissesse: quero todas as respostas aqui dentro. Qualquer épsilon pode ser escolhido, por isso a definição começa com "para todo épsilon". Depois é a sua vez: você responde com um disquinho de raio delta em volta do ponto. E olha o que acontece do outro lado: cada ponto do seu disco manda a ponta da seta para algum lugar, e todas essas pontas juntas formam uma mancha. A pergunta é uma só: a mancha cabe no disco épsilon?

[curious] Com delta igual a zero vírgula sete, não cabe: um monte de pontas escapa. Diminui o delta… e a mancha encolhe junto. Em zero vírgula quatro um, ela fica inteira por dentro. Achou: é isso que "existe delta" quer dizer. Se o desafio aperta para meio, você aperta para zero vírgula dois um. Para um quarto, zero vírgula um zero. O delta depende do épsilon, e o limite existe quando você sempre consegue responder.

[thoughtful] E tem um detalhe no seu disco: o próprio ponto fica de fora. É o "maior que zero" da definição. O limite só olha para quem está chegando, nunca para o que acontece em cima do ponto. Aliás, o ponto nem precisa estar no domínio: basta ter pontos do domínio tão perto dele quanto você quiser. O nome disso é ponto de acumulação. Já um ponto do domínio sozinho, sem vizinhos, não serve: ninguém chega perto dele. Agora sim, escrito: a seta-alvo é o limite quando, para todo épsilon positivo, existe um delta positivo tal que, para todo ponto do domínio a uma distância maior que zero e menor que delta, a seta fica a menos de épsilon do alvo. A metade da esquerda fala de onde você anda. A da direita, de onde a seta chega.

[curious] E tem um atalho. Se a ponta está no disco épsilon, as duas sombras dela, a horizontal e a vertical, ficam a menos de épsilon das sombras do alvo. E o contrário também vale: se as duas sombras estão perto, a ponta cai num quadrado, que cabe num disco só um pouquinho maior. Então o limite de um campo existe exatamente quando o limite de cada componente existe, e aí é o limite de funções de várias variáveis que você já conhece. Mas guarda uma coisa: com várias variáveis, o caminho pelo qual você chega pode mudar completamente a resposta.

[curious] E é justamente isso que acontece com este campo encrenqueiro. Todas as setas são horizontais. Nos eixos, não tem seta nenhuma; nas diagonais, as setas têm tamanho um: numa delas apontam para a direita, na outra, para a esquerda. Só que a resposta muda com a direção por onde a gente chega.

[thoughtful] Vem andando até a origem pelo eixo horizontal: a seta é zero o caminho todo. Pela diagonal de subida: um, para a direita. Pela outra: um, para a esquerda. Numa reta qualquer pela origem, o campo vale o dobro da inclinação, dividido por um mais a inclinação ao quadrado. Três caminhos, três resultados diferentes. Muda a reta, muda o valor.

[curious] E dá para ver isso de um jeito mais bonito. Em coordenadas polares, a componente horizontal vira o seno do dobro do ângulo. O campo não depende da distância, só da direção. Então dá uma volta num círculo minúsculo em volta da origem: a ponta da seta varre o segmento inteiro, de menos um até um. Diminui o raio… e diminui de novo: acontece exatamente a mesma coisa, por menor que seja o círculo.

[thoughtful, emphatic] Agora joga o desafio. Escolhe um alvo qualquer e um épsilon de meio. O disco tem largura um, e o segmento tem largura dois: não cabe, seja qual for o alvo. Então não existe limite na origem. E fica um cuidado: dois caminhos com valores diferentes provam que o limite não existe. Mas todas as retas darem o mesmo valor ainda não provam que ele existe, porque dá para chegar por uma curva. Olha este campo: por qualquer reta, a seta vai para zero. Mas, pela parábola, ela fica em meio o caminho todo. Também não tem limite.

[thoughtful] Agora a continuidade. A definição tem três pedaços, e cada um pode falhar. Um: o ponto está no domínio, então a seta do ponto existe. Dois: o limite ali existe. Três: o limite é igual à própria seta do ponto. Na figura, é o mesmo desafio de antes, só que agora o disco épsilon fica em volta da ponta da seta do próprio ponto. No nosso campo, a mancha cabe. Contínuo.

[curious] Agora, três jeitos de dar errado, e em cada um você vai chegando no ponto para ver o que a seta faz. No campo elétrico de uma carga, o ponto da carga nem está no domínio, e quanto mais você chega perto, mais a seta cresce. Falha o primeiro pedaço, e a pergunta nem se faz; em todo o resto, ele é contínuo. No campo encrenqueiro, definido como zero na origem, a seta existe, mas o limite não: dependendo do caminho por onde você chega, a seta vai para a direita, para a esquerda ou para zero. Falha o segundo. E neste aqui todas as setas apontam para a direita, menos a do centro, que aponta para cima. Chegando de qualquer lado, a seta é para a direita; só em cima do ponto ela vira para cima. O limite existe e é a seta para a direita, mas a seta do ponto é outra. Falha o terceiro: um salto bem em cima do ponto.

[thoughtful] E, de novo, por componentes: o campo é contínuo exatamente quando cada componente é contínua. Por isso quase todo campo que vem de fórmula é contínuo onde está definido: somas, produtos, quocientes com denominador diferente de zero e composições de funções contínuas continuam contínuas. A primeira componente do nosso campo é uma constante mais senos: contínua. E o campo da carga é um quociente: contínuo em todo lugar, menos em cima da carga.

[thoughtful] Agora sim: medir como a seta muda. Fica no ponto e anda só na horizontal, um passo. A seta muda de uma para outra, e a diferença entre as duas é um vetor, que liga a ponta velha à ponta nova. Divide esse vetor pelo tamanho do passo e encolhe o passo. Esse limite é a derivada parcial do campo na direção horizontal.

[curious] Com passo um, o quociente vale zero vírgula oito quatro e dois vírgula um quatro. Com meio, zero vírgula nove seis e dois vírgula um seis. Com passo cada vez menor, ele vai chegando em um e dois. E olha a tela da chegada: andando na horizontal, a ponta da seta desenha uma curva. A diferença é uma corda dessa curva, e, dividida pelo passo, ela vira a seta tangente. Então a derivada parcial é a velocidade da ponta, quando você anda na horizontal com velocidade um.

[thoughtful] E essa velocidade tem duas sombras. A horizontal diz quanto muda a componente horizontal do campo: um. A vertical diz quanto muda a componente vertical: dois. Por isso a conta é por componentes: a derivada do campo é a derivada de cada componente.

[curious] Agora na vertical. Andando para cima, a ponta anda num círculo, e o quociente vai chegando em menos um e zero: a derivada na direção vertical aponta para a esquerda, tangente ao círculo.

[thoughtful, emphatic] Então a derivada parcial de um campo não é um número: é um vetor, que diz como a seta muda quando você anda numa direção. Na conta, a derivada na horizontal dá cosseno e dois cossenos mais seno, da coordenada horizontal; no ponto, um e dois. A derivada na vertical dá menos cosseno e seno da coordenada vertical; no ponto, menos um e zero. A conta bate com o desenho. E, num campo no espaço, aparece uma terceira, na direção da profundidade, com a mesma ideia.

[curious] Só que tem uma armadilha. Volta no campo encrenqueiro e calcula as derivadas parciais na origem. Pelo eixo horizontal, a seta é zero o tempo todo: derivada zero. Pelo vertical, mesma coisa. As duas existem, e as duas são zero.

[thoughtful] Se você confiasse só nelas, ia prever que, perto da origem, tudo vai para perto do zero: um quadradinho em volta da origem iria parar num ponto só. Mas olha a imagem de verdade: a ponta varre o segmento inteiro, de menos um até um. A previsão errou feio. As parciais só olham duas retas, e esse campo esconde tudo nas diagonais. Ele nem é contínuo na origem.

[thoughtful, emphatic] O que faltou? Olha as próprias derivadas, andando pelo eixo vertical. No nosso campo, a derivada na horizontal vale um o caminho todo, sem salto nenhum. No encrenqueiro, ela vale dois dividido pela altura: explode perto da origem, e na origem vale zero. Essa é a condição de classe cê um: as derivadas parciais existem e são contínuas, numa vizinhança do ponto. Ela é suficiente para a aproximação linear funcionar. Classe cê erre é o mesmo, até as derivadas de ordem erre.

[curious] E com ela vem a promessa. Pega uma malhinha em volta do ponto e manda para a tela da chegada. As linhas horizontais viram curvas na direção da derivada horizontal, e as verticais, curvas na direção da derivada vertical. Cada quadradinho da malha vira quase um paralelogramo, com lados de passo vezes derivada. Escrito: a seta num ponto vizinho é a seta do ponto, mais o passo horizontal vezes a derivada na horizontal, mais o passo vertical vezes a derivada na vertical, com um erro que some mais rápido que o passo. O nosso campo, feito de senos e cossenos, é cê um. O encrenqueiro, não. E dá para ver isso dividindo o erro pelo passo. No nosso campo, quando o passo cai pela metade, essa conta cai pela metade também, e vai para zero. No encrenqueiro, ela dobra. É a diferença entre ter duas derivadas parciais e ter uma aproximação linear de verdade.

[curious] Então vamos usar isso. Pega o campo da aula e chega dez vezes mais perto do ponto: essa janelinha vira o palco inteiro. De perto, todas as setas ficam parecidas com a seta do centro. Cada uma é a seta do centro, mais um restinho. Tira a seta do centro de todas… e sobra só a mudança. Olha que campo arrumadinho.

[thoughtful] Bem de perto, essa mudança é escrita com as duas derivadas. Então coloca as duas lado a lado, como colunas: a derivada na horizontal na primeira, a derivada na vertical na segunda. Fica uma tabela de quatro números, com as derivadas das duas componentes nas duas direções. Ela tem nome: matriz jacobiana. No nosso ponto, um e menos um em cima, dois e zero embaixo.

[curious] E ela funciona assim: um passo com uma parte horizontal e uma vertical vira a parte horizontal vezes a primeira coluna, mais a parte vertical vezes a segunda. A seta do modelo é a soma das duas. É a primeira aproximação do campo perto do ponto.

[thoughtful] Agora coloca um quadradinho com a quina no ponto. A quina da direita é empurrada pela primeira coluna; a de cima, pela segunda. Cada coluna empurra uma aresta. Solta o fluido no modelo… e o quadradinho gira, cresce e entorta, tudo ao mesmo tempo. Tudo isso, no modelo linear, estava nos quatro números.

[thoughtful] E dá para separar essa bagunça, lendo cada número da tabela como um movimento de aresta. Em cima, à esquerda: quanto a aresta horizontal estica. Aqui, um. Embaixo, à esquerda: quanto ela gira. Dois. Em cima, à direita: quanto a aresta vertical tomba para o lado. Menos um, para a esquerda. Embaixo, à direita: quanto ela estica. Zero.

[curious] Agora junta. Os dois giros no mesmo sentido, somados, dão o rotacional: dois mais um, três. Os dois estiramentos somados dão o divergente: um mais zero, um. E sobram duas comparações. Estiramento horizontal menos vertical: um. Essa é a primeira deformação, quanto o pedacinho estica mais numa direção do que na outra. E a diferença entre os dois giros: dois menos um, um. Essa é a segunda, quanto o ângulo reto do quadradinho fecha, como uma tesoura.

[thoughtful, emphatic] Quatro números entram, quatro medidas saem, e nada se perde no caminho. Bem de perto e sem a seta do centro, a variação de primeira ordem de todo campo cê um é uma mistura de quatro campos simples: um redemoinho, uma explosão e duas deformações. Olha cada um agindo no quadradinho: o redemoinho gira, a explosão cresce, a deformação estica de um lado e achata do outro. E isso não é só matemática: num fluido newtoniano, o atrito viscoso vem da deformação. Um bloco de fluido girando inteiro, rígido, não tem atrito viscoso nenhum por dentro.

[curious] Agora volta lá no começo. No campo que esticava o quadradinho, a tabela é um e zero em cima, zero e menos um embaixo. A aresta horizontal estica, a vertical encolhe na mesma medida, e ninguém gira. Rotacional zero, divergente zero, e a primeira deformação vale dois. É tudo deformação.

[happy] E lá no episódio passado ficou um desafio: achar outro campo, que não fosse constante, com rotacional e divergente zero. Um deles é este, que troca as coordenadas de lugar. As duas arestas giram uma contra a outra: a segunda deformação vale dois, e o quadradinho vira losango. É o mesmo campo de antes, girado quarenta e cinco graus. E quem achou um de segundo grau, como o da tela, também acertou. Rotacional e divergente, sozinhos, não dizem tudo sobre como um campo varia.

[thoughtful] Resumindo: limite é ganhar o desafio do épsilon com um delta. Continuidade é o limite igual à seta do ponto, sem salto. A derivada parcial é a velocidade da ponta numa direção. E, quando essas derivadas são contínuas, a tabela delas descreve o campo bem perto do ponto: giro, área e deformação. E uma curiosidade: no espaço, a tabela tem nove números, que se separam em três de giro, um de volume e cinco de deformação.

[excited] No próximo vídeo, é a vez de colocar a mão na massa: o integrador do módulo, só com exercícios. Campo vetorial, rotacional, divergente, limite e continuidade, derivadas parciais, tudo junto. E vai ser a sua hora de pegar um campo, montar a tabela e descobrir se o quadradinho vai girar, mudar de área ou deformar. [happy] Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e conta nos comentários: qual dessas medidas, giro, expansão ou deformação, você acha que aparece mais na física? Até a próxima!
---

## 4. Voz (ElevenLabs v4)
Referência: `docs/roteiro_voz_elevenlabs_v4.md`.
1. Confirme `ELEVENLABS_API_KEY` na sessão (primeira parada permitida, §0).
   - Voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`.
   - Formato `mp3_44100_192`, decodificado para WAV mono 16 bits 44,1 kHz.
2. Rode primeiro com `--seco` (só mostra os blocos, sem gastar crédito):

   ```
   uv run --no-sync python videos/gerar_voz_elevenlabs.py videos_longos/yt_0028_limite_continuidade_derivadas_parciais/narracao_tags.md videos_longos/yt_0028_limite_continuidade_derivadas_parciais/audio/narracao_v1.wav --voz qw7jgPZWOKrl10GsjQ82 --secao "## Texto corrido (para gravação)" --seco
   ```

   Depois, a geração de verdade, sem `--seco`.
3. **Uma tomada completa.** Siga com ela. O Kaio ouve em paralelo; se reprovar, regera, e a §5 refaz tudo sozinha. Por isso a sincronização precisa ser **automática e reproduzível**. A tomada aprovada vira `audio/narracao_final.wav` (cópia).
4. **Checagens automáticas do WAV** (relatório `qa/voz.txt`):
   - duração;
   - picos e clipping;
   - silêncio > 1,5 s dentro de um parágrafo;
   - **tag lida em voz alta**: pela transcrição de conferência do `alinhar_voz.py --stt`, procure `curious`, `thoughtful`, `emphatic`, `excited`, `happy`;
   - "épsilon", "delta", "jacobiana", "cê um", "cê erre", "newtoniano" e "Parallax Lab" pronunciados direito;
   - fronteiras entre blocos sem corte audível.
5. Registre no relatório: modelo, voz, versão do texto, número de blocos, duração e taxa real (palavras ÷ segundos de fala).

---

## 5. Sincronização (a cena segue a voz)
Regras permanentes dos longos:
- **WAV contínuo**;
- **nunca** cortar a voz por âncora nem inserir silêncio;
- **atraso imagem × fala ≤ 0,2 s** (LEAD 0,15 s);
- cena parada esperando a voz, só com informação na tela.

1. **Tempo por palavra:** `alinhar_voz.py` → `alinhamento_palavras.json` (alinhamento forçado do texto limpo com o WAV).
2. **`ancoras.json` gerado por script**, nunca à mão: `gerar_ancoras.py` no modo do yt_0026 v9 (tempo real da voz). Cada âncora começa no instante da **primeira palavra do seu trecho**, conforme a tabela abaixo, e termina onde a próxima começa. O `t` de cada palavra vem do alinhamento.
3. Rode os lotes 540p e confira no log:
   - `[gatilho-sem-frase]` = 0;
   - os `[estouro]`, listados com o motivo (a cena se esticou porque a animação é mais longa que a fala).

   Estouro maior que 1 s numa âncora: encurte a animação dentro da regra de cadência (piso 0,20 s/glifo na caneta) ou deixe a âncora seguinte começar mais tarde. **Nunca** acelere a voz.
4. **Relatório de sincronização** (`qa/sync.txt`): para cada uma das **37 âncoras** e para os gatilhos do §2 e do Anexo B, o atraso entre a palavra e o evento visual (meta ≤ 0,2 s), com a lista do que passar disso.
5. **Legenda `.srt`:** `gerar_srt.py`. Regras:
   - até 2 linhas × 42 caracteres;
   - de 2 a 5 s por bloco;
   - "Cálculo três" falado vira "Cálculo III", "cê um" vira "C¹" e "cê erre" vira "Cʳ" na legenda;
   - tempo do WAV = tempo do vídeo.

   Longos não têm legendado embutido: o master é o único vídeo final.

| Âncora | Começa em (primeiras palavras) |
|---|---|
| H1 | "Lembra do campo que fechou o" |
| H2 | "Só que agora deixa o fluido" |
| H3 | "Então tem alguma coisa nesse campo" |
| A1 | "Fala, pessoal! Bem-vindos ao Parallax Lab!" |
| B1-1 | "Vamos usar duas telas. Na da" |
| B1-2 | "Conforme você chega perto do ponto," |
| B1-3 | "Primeiro, alguém escolhe uma tolerância na" |
| B1-4 | "Com delta igual a zero vírgula" |
| B1-5 | "E tem um detalhe no seu" |
| B1-6 | "E tem um atalho. Se a" |
| B2-1 | "E é justamente isso que acontece" |
| B2-2 | "Vem andando até a origem pelo" |
| B2-3 | "E dá para ver isso de" |
| B2-4 | "Agora joga o desafio. Escolhe um" |
| B3-1 | "Agora a continuidade. A definição tem" |
| B3-2 | "Agora, três jeitos de dar errado," |
| B3-3 | "E, de novo, por componentes: o" |
| B4-1 | "Agora sim: medir como a seta" |
| B4-2 | "Com passo um, o quociente vale" |
| B4-3 | "E essa velocidade tem duas sombras." |
| B4-4 | "Agora na vertical. Andando para cima," |
| B4-5 | "Então a derivada parcial de um" |
| B5-1 | "Só que tem uma armadilha. Volta" |
| B5-2 | "Se você confiasse só nelas, ia" |
| B5-3 | "O que faltou? Olha as próprias" |
| B5-4 | "E com ela vem a promessa." |
| B6-1 | "Então vamos usar isso. Pega o" |
| B6-2 | "Bem de perto, essa mudança é" |
| B6-3 | "E ela funciona assim: um passo" |
| B6-4 | "Agora coloca um quadradinho com a" |
| B7-1 | "E dá para separar essa bagunça," |
| B7-2 | "Agora junta. Os dois giros no" |
| B7-3 | "Quatro números entram, quatro medidas saem," |
| B7-4 | "Agora volta lá no começo. No" |
| B7-5 | "E lá no episódio passado ficou" |
| S1 | "Resumindo: limite é ganhar o desafio" |
| S2 | "No próximo vídeo, é a vez" |

---

## 6. Conferência 540p com voz (antes do 1080p)
Render de **todos os lotes** em 540p/15 fps com os tempos da voz e preview com voz (`montar_preview.py` com o WAV). Rode todos os portões e feche o que falhar antes do 1080p:
- `FLASH` = 0 (caneta: nada visível antes da vez);
- **R5 sobreposição** = 0 (`qa_sobrepos_rel.py`, seta inteira, também **durante** a onda do M1 e os caminhantes do M3);
- **R7 seta na moldura** = 0, e nenhum texto, rótulo ou placa cruza a moldura do seu painel;
- **R10 transições** = 0 (nenhum quadro com menos de um objeto além do canto e do logo por mais de 0,8 s; `transicoes.py`), incluindo a saída do A para o B1 e do resumo para o cartão de gancho;
- **alinhamento (R9)**: grade, moldura, origem e redes de setas com resíduo ≤ 1 px em stills 1080p;
- `qa_parado.py`: tela congelada > 2 s **só** onde há informação na tela e a fala segue (liste);
- `[gatilho-sem-frase]` = 0;
- `qa_canto.py` e `qa_fundo.py`;
- **logo presente em todos os quadros do A1** (do primeiro ao último);
- **SYNC** (atraso ≤ 0,2 s);
- **VOZ** (sem borda abrupta, sem silêncio inserido).

**Lado a lado** (`comparar.py`, `RODADA=final`): os alvos 38 a 42 contra o render, mais os alvos 01, 03, 12, 22, 32 e 37 para confirmar que nada regrediu. Monte também uma **prancha com um quadro de cada âncora no instante da primeira palavra** (37 quadros), para ver se a imagem certa está na tela quando a fala começa.

---

## 7. Render final 1080p
1. **Manim em 1080p30** pelo fluxo normal (`uv run python -m manim ...`) com `template/config_horizontal.py`. **Não configure CRF:** o `template/qualidade.py` já troca para **14** nos renders ≥ 1080p. Não use a variável `CRF` e não recodifique. Sem modo leve: não há teto de tempo de render.
2. **Emenda:** `montar_final.py` (remux, sem reencodar), na ordem PH, PB1, PB2, PB3, PB4, PB5, PB6, PB7, PS.
3. **Master:**

   ```
   uv run python videos/montar_master.py <sem_audio_1080p30.mp4> audio/narracao_final.wav renders/yt_0028_master_final_1080p30.mp4
   ```

   A voz é colada **sem recompressão do vídeo**. Confira:
   - 1920×1080, 30 fps;
   - duração do master = WAV (+ os 3 s finais do CTA, se a montagem os mantiver, como no yt_0026);
   - `crf=14.0`, com o comando do AGENTS: `uv run python -c "import av,re;c=av.open('ARQ.mp4');d=b''.join(bytes(p) for _,p in zip(range(4),c.demux(c.streams.video[0])));print(re.search(rb'crf=([0-9.]+)',d).group(1))"`.
4. Se o disco apertar, apague só PNGs e renders 540p **desta** unidade que já foram auditados. Nada de limpeza ampla.

---

## 8. QA final e entrega
- **QA completo no vídeo final** (obrigatório no fechamento):
  - os portões do §6 sobre o 1080p (amostragem por lote);
  - A/V: voz contínua, sem clipping, sem corte;
  - `.srt` aberto e conferido em 5 pontos: início, meio, fim, uma frase longa e uma de equação;
  - `crf=14.0`;
  - capítulos (`renders/capitulos_final.txt`) recalculados com os tempos da voz, nos mesmos 9 títulos do v4 (`O QUADRADINHO QUE DEFORMA`, `CHEGAR PERTO`, `QUANDO O LIMITE NÃO EXISTE`, `CONTINUIDADE`, `DERIVADA PARCIAL`, `O ENGANO`, `A TABELA`, `QUATRO NÚMEROS, QUATRO MEDIDAS`, `RESUMO`).
- **Entrega:** `uv run python videos/entregar.py yt_0028` (cópia; não move nem apaga). Pasta única em `entregas/` com:
  - `master`;
  - `legenda` (`.srt`);
  - `audio/` (WAV final);
  - `texto/` (ficha, `narracao_tags.md`, `narracao_limpa.md`, este handoff, capítulos);
  - `manifesto`.

  O número `0028` vai no fim de cada nome. Sem capa. Série, EP e assunto vêm da `ficha.md` (`CÁLCULO III · EP. 03`, `# Limite, continuidade e derivadas parciais`).
- Não rode `entregar.py` com uma versão que reprove um portão do §6. Se algum portão ficar aberto, pare e reporte qual e por quê; a entrega assim mesmo só acontece se o Kaio autorizar.

---

## 9. Relatório de entrega (obrigatório, e depois pare)
1. Arquivos alterados e criados: código, `narracao.md`, `narracao_tags.md`, `narracao_limpa.md`, `ancoras.json`, `.srt`, ficha.
2. Os itens 2.1 a 2.7 do §2, cada um com o caminho do quadro ou da tira que prova. Lista dos gatilhos reconectados por causa do Anexo D (frase antiga → frase nova).
3. Verificações e resultados: todos os portões do §6 com números reais, a sincronização das 37 âncoras e o QA de voz.
4. Caminhos: WAV, preview 540p com voz, master 1080p, `.srt`, capítulos e a pasta em `entregas/`.
5. Custo de render por lote no 1080p e o que faltou (sem 3D nesta unidade).
6. Duração final e taxa real da voz (palavras ÷ segundos), comparadas com a estimativa de 3 palavras/s.
7. Pendências reais (estouros de âncora, exceções de portão).

Depois do relatório: **pare**. Sem publicação, capa, commit ou push.

---

## Anexo A · Números congelados (tela e fala)
- **Gancho:** `F⃗ = (x, −y)`; `rot = 0`, `div = 0`; o quadradinho de lado 1,2 vira `ÁREA 1,44 → 1,44` (estica ×eᵗ na horizontal, ÷eᵗ na vertical, t = 0,55). Jacobiana `diag(1, −1)`, primeira deformação 2.
- **Campo da aula:** `F⃗ = (1 + sen x − sen y, 2 sen x + 2 − cos x − cos y)`; no ponto (0, 0): `F⃗ = (1, 0)`, `J = [[1, −1], [2, 0]]`, `rot = 3`, `div = 1`, deformações 1 e 1. Derivadas: `∂F⃗/∂x = (cos x, 2 cos x + sen x)` → (1, 2); `∂F⃗/∂y = (−cos y, sen y)` → (−1, 0).
- **Quocientes (B4):** passo em x: 1 → (0,84; 2,14), 0,5 → (0,96; 2,16), 0,1 → (1,00; 2,05) → (1, 2). Passo em y: 1 → (−0,84; 0,46), 0,5 → (−0,96; 0,25), 0,1 → (−1,00; 0,05) → (−1, 0).
- **ε e δ (B1):** ε = 1 → δ = 0,41; ε = 0,5 → δ = 0,21; ε = 0,25 → δ = 0,10; δ = 0,7 não cabe. Atalho: o quadrado das sombras cabe no disco de raio √2·ε.
- **Campo encrenqueiro:** `G⃗ = (2xy/(x² + y²), 0)`; em coordenadas polares `(sen 2θ, 0)`; na reta y = mx vale `2m/(1 + m²)`; eixos: 0; diagonais: ±1. Com ε = 1/2 o disco tem diâmetro 1 e o segmento tem comprimento 2: não cabe. Contra-exemplo: `K = x²y/(x⁴ + y²)` vale 0 por toda reta e 1/2 pela parábola y = x².
- **Parciais do encrenqueiro na origem:** ambas 0; sobre o eixo vertical, a derivada em x vale 2/y (explode) e a do nosso campo vale 1.
- **Erro ÷ passo:** nosso campo 0,07 / 0,15 / 0,33 para passo 0,125 / 0,25 / 0,5; encrenqueiro 8 / 4 / 2 (cresce como 1/passo).
- **Giros e estiramentos (B7):** estica_H = 1, giro_H = 2, giro_V = 1 (a aresta vertical tomba para a esquerda), estica_V = 0. `rot = 2 + 1 = 3`, `div = 1 + 0 = 1`, deformações `1 − 0 = 1` e `2 − 1 = 1`.
- **Desafio do episódio passado:** `F⃗ = (y, x)`: `J = [[0, 1], [1, 0]]`, `rot = 0`, `div = 0`, deformações 0 e 2 (o mesmo campo do gancho girado 45°).
- **No espaço:** 9 números = 3 de giro + 1 de volume + 5 de deformação.

---

## Anexo B · Frases-gatilho novas (precisam estar no texto falado)

Além das frases dos §2.1 e §2.2:

| Âncora | Frase | Evento |
|---|---|---|
| H1 | "O rotacional dá zero, em todo ponto" / "O divergente também dá zero" | `rot F⃗ = 0` / `div F⃗ = 0` (como hoje) |
| H2 | "olha o que acontece" | o fluido começa a andar |
| B1-1 | "A seta do lugar onde você está fica em destaque" | seta de X em destaque (M2) |
| B1-1 | "eu trago essa seta para a mesma origem" | a cópia viaja (M2) |
| B1-1 | "por onde você anda" / "onde a seta chega" | os nomes dos painéis (como hoje) |
| B3-2 | "No campo elétrico de uma carga" | caminhante do cartão ① (M3) |
| B3-2 | "dependendo do caminho por onde você chega" | três caminhantes do cartão ② |
| B3-2 | "Chegando de qualquer lado" | caminhante do cartão ③ |
| B7-3 | "Olha cada um agindo no quadradinho" | os três quadradinhos aparecem na posição original (M4) |
| B7-3 | "o redemoinho gira" / "a explosão cresce" / "a deformação estica de um lado" | cada quadradinho faz sua transformação (M4) |
| B6-1 | "chega dez vezes mais perto" | zoom ×10; a tag do zoom entra no canto inferior esquerdo da moldura |
| S1 | "Resumindo" | resumo; a tag do zoom sai |

Os demais gatilhos continuam os do preview v4 (conferidos no log do `gerar_ancoras.py`).

---

## Anexo C · Tamanho por âncora (v5, 3 palavras/s)

| Âncora | Palavras | Fala (s) |
|---|---|---|
| H1 | 67 | 22 |
| H2 | 39 | 13 |
| H3 | 54 | 18 |
| A1 | 158 | 53 |
| B1-1 | 68 | 23 |
| B1-2 | 62 | 21 |
| B1-3 | 99 | 33 |
| B1-4 | 74 | 25 |
| B1-5 | 137 | 46 |
| B1-6 | 100 | 33 |
| B2-1 | 52 | 17 |
| B2-2 | 60 | 20 |
| B2-3 | 74 | 25 |
| B2-4 | 98 | 33 |
| B3-1 | 71 | 24 |
| B3-2 | 164 | 55 |
| B3-3 | 73 | 24 |
| B4-1 | 63 | 21 |
| B4-2 | 87 | 29 |
| B4-3 | 43 | 14 |
| B4-4 | 33 | 11 |
| B4-5 | 86 | 29 |
| B5-1 | 40 | 13 |
| B5-2 | 68 | 23 |
| B5-3 | 82 | 27 |
| B5-4 | 154 | 51 |
| B6-1 | 61 | 20 |
| B6-2 | 65 | 22 |
| B6-3 | 46 | 15 |
| B6-4 | 53 | 18 |
| B7-1 | 58 | 19 |
| B7-2 | 77 | 26 |
| B7-3 | 96 | 32 |
| B7-4 | 50 | 17 |
| B7-5 | 84 | 28 |
| S1 | 76 | 25 |
| S2 | 89 | 30 |
| **Total** | **2861** | **≈ 954 s (15.9 min)** |

---

## Anexo D · O que mudou de texto em relação ao preview v4 (para reconectar gatilhos)

O texto do preview v4 era a narração v3. Só os parágrafos abaixo mudaram; o resto é idêntico. Para cada evento do código que dependia de uma frase "tirou", reaponte para a frase "entrou" equivalente e liste no relatório.

**H1**
- tirou: "A componente horizontal é a própria coordenada horizontal, e a vertical é menos a coordenada vertical."
- entrou: "A componente horizontal é o próprio x, e a vertical é menos y."
- entrou: "Então, pelas duas medidas, não era para acontecer nada, certo?"

**H2**
- tirou: "Então, pelas duas medidas, não acontece nada."
- tirou: "e o quadradinho estica para os lados e achata na vertical."
- tirou: "Mas virou outra coisa."
- entrou: "e olha o que acontece: o quadradinho estica para os lados e achata na vertical."
- entrou: "Mas a forma mudou completamente."

**A1**
- tirou: "Bem-vindos ao Parallax Lab."
- tirou: "Hoje são três ideias que se apoiam uma na outra: limite, continuidade e derivadas parciais de um campo vetorial."
- tirou: "E, no fim, a gente vai juntar tudo numa tabela de quatro números que mostra, bem de perto, como o campo muda em volta de um ponto."
- entrou: "Bem-vindos ao Parallax Lab!"
- entrou: "Esse é o terceiro episódio da nossa série de Cálculo três."
- entrou: "Hoje a gente olha um campo vetorial bem de pertinho."
- entrou: "Porque a seta de um ponto não basta: é preciso entender as setas vizinhas."
- entrou: "Para isso, entram três ideias, uma apoiada na outra."
- entrou: "Primeiro, o limite: o que quer dizer chegar perto de um ponto, com o épsilon e o delta desenhados, e não só escritos."
- entrou: "Depois, a continuidade: quando a seta não dá pulo, e três jeitos de ela falhar."
- entrou: "E, por fim, as derivadas parciais, que medem como a seta muda em cada direção."
- entrou: "No meio do caminho tem um engano, em que as derivadas parciais mentem sobre o campo."
- entrou: "E, no final, a gente junta tudo numa tabela de quatro números, que revela o giro, a mudança de área e aquela deformação do quadradinho que ficou sem explicação."
- entrou: "Então vamos começar pelo chão: o que é chegar perto?"

**B1-1**
- tirou: "Na da direita, eu trago cada seta para a mesma origem, para comparar só onde a ponta dela chega."
- entrou: "A seta do lugar onde você está fica em destaque."
- entrou: "Na da direita, eu trago essa seta para a mesma origem, para comparar só onde a ponta dela chega."
- entrou: "Uma tela mostra por onde você anda; a outra, onde a seta chega."

**B1-2**
- entrou: "Perto quanto?"

**B1-3**
- entrou: "É como se dissesse: quero todas as respostas aqui dentro."

**B1-6**
- entrou: "Mas guarda uma coisa: com várias variáveis, o caminho pelo qual você chega pode mudar completamente a resposta."

**B2-1**
- tirou: "Agora um campo encrenqueiro."
- entrou: "E é justamente isso que acontece com este campo encrenqueiro."
- entrou: "Só que a resposta muda com a direção por onde a gente chega."

**B2-2**
- entrou: "Três caminhos, três resultados diferentes."

**B2-3**
- tirou: "E isso acontece em qualquer círculo, por menor que seja."
- entrou: "Diminui o raio…"
- entrou: "e diminui de novo: acontece exatamente a mesma coisa, por menor que seja o círculo."

**B3-2**
- tirou: "Agora, três jeitos de dar errado."
- tirou: "No campo elétrico de uma carga, o ponto da carga nem está no domínio."
- tirou: "No campo encrenqueiro, definido como zero na origem, a seta existe, mas o limite não: falha o segundo."
- entrou: "Agora, três jeitos de dar errado, e em cada um você vai chegando no ponto para ver o que a seta faz."
- entrou: "No campo elétrico de uma carga, o ponto da carga nem está no domínio, e quanto mais você chega perto, mais a seta cresce."
- entrou: "No campo encrenqueiro, definido como zero na origem, a seta existe, mas o limite não: dependendo do caminho por onde você chega, a seta vai para a direita, para a esquerda ou para zero."
- entrou: "Falha o segundo."
- entrou: "Chegando de qualquer lado, a seta é para a direita; só em cima do ponto ela vira para cima."

**B5-3**
- tirou: "Essa é a condição de classe cê um: as derivadas parciais existem e são contínuas."
- entrou: "Essa é a condição de classe cê um: as derivadas parciais existem e são contínuas, numa vizinhança do ponto."
- entrou: "Ela é suficiente para a aproximação linear funcionar."

**B5-4**
- entrou: "É a diferença entre ter duas derivadas parciais e ter uma aproximação linear de verdade."

**B6-3**
- entrou: "É a primeira aproximação do campo perto do ponto."

**B6-4**
- tirou: "Tudo isso estava nos quatro números."
- entrou: "Tudo isso, no modelo linear, estava nos quatro números."

**B7-3**
- tirou: "Bem de perto e sem a seta do centro, todo campo cê um se comporta como uma mistura de quatro campos simples: um redemoinho, uma explosão e duas deformações."
- tirou: "E isso não é só matemática: num fluido, o atrito viscoso vem da deformação."
- entrou: "Bem de perto e sem a seta do centro, a variação de primeira ordem de todo campo cê um é uma mistura de quatro campos simples: um redemoinho, uma explosão e duas deformações."
- entrou: "Olha cada um agindo no quadradinho: o redemoinho gira, a explosão cresce, a deformação estica de um lado e achata do outro."
- entrou: "E isso não é só matemática: num fluido newtoniano, o atrito viscoso vem da deformação."

**B7-5**
- entrou: "Rotacional e divergente, sozinhos, não dizem tudo sobre como um campo varia."

**S2**
- tirou: "No próximo vídeo, a gente coloca o módulo inteiro para trabalhar em exercícios: campo vetorial, rotacional, divergente, limite e derivadas parciais, tudo junto."
- tirou: "Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e conta nos comentários: qual dessas quatro medidas você acha que aparece mais na física?"
- entrou: "No próximo vídeo, é a vez de colocar a mão na massa: o integrador do módulo, só com exercícios."
- entrou: "Campo vetorial, rotacional, divergente, limite e continuidade, derivadas parciais, tudo junto."
- entrou: "E vai ser a sua hora de pegar um campo, montar a tabela e descobrir se o quadradinho vai girar, mudar de área ou deformar."
- entrou: "Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e conta nos comentários: qual dessas medidas, giro, expansão ou deformação, você acha que aparece mais na física?"


---

## Anexo E · Narração por âncora (conteúdo de `narracao.md`)

### H1 · tela: campo (x, −y) nasce em onda a partir do centro (M1); `F⃗ = (x, −y)`; o quadradinho com malha entra; `rot F⃗ = 0`, `div F⃗ = 0` (alvo 01)
[curious] Lembra do campo que fechou o episódio passado? A componente horizontal é o próprio x, e a vertical é menos y. Coloca um quadradinho de fluido no meio e faz as contas que a gente já conhece. O rotacional dá zero, em todo ponto: nenhuma rodinha gira. O divergente também dá zero: nenhum pedacinho muda de área. Então, pelas duas medidas, não era para acontecer nada, certo?

### H2 · tela: o fluido anda: o quadradinho estica e achata; `ÁREA 1,44 → 1,44`; `MAS DEFORMA`
[thoughtful] Só que agora deixa o fluido andar… e olha o que acontece: o quadradinho estica para os lados e achata na vertical. A área continua a mesma, e ele não girou nem um grau. Mas a forma mudou completamente.

### H3 · tela: `QUE NÚMERO MEDE ISSO?`; `A RESPOSTA: AS DERIVADAS PARCIAIS`; `∂F/∂x`, `∂F/∂y`; `MAS ANTES, O CHÃO:` (alvo 02)
[curious] Então tem alguma coisa nesse campo que o rotacional e o divergente não enxergam. Que número mede isso? E de onde ele sai? A resposta está nas derivadas parciais do campo. Só que, para usar essas derivadas com segurança, a gente precisa começar pelo chão: o que quer dizer chegar perto de um ponto.

### A1 · tela: logo com os dois anéis e `BEM-VINDOS AO PARALLAX LAB`; depois título e a lista `NESTE VÍDEO` (§2.1, alvos 38 e 39); o canto entra no fim
[happy] Fala, pessoal! Bem-vindos ao Parallax Lab! Esse é o terceiro episódio da nossa série de Cálculo três. Hoje a gente olha um campo vetorial bem de pertinho. [thoughtful] Porque a seta de um ponto não basta: é preciso entender as setas vizinhas. Para isso, entram três ideias, uma apoiada na outra. Primeiro, o limite: o que quer dizer chegar perto de um ponto, com o épsilon e o delta desenhados, e não só escritos. Depois, a continuidade: quando a seta não dá pulo, e três jeitos de ela falhar. E, por fim, as derivadas parciais, que medem como a seta muda em cada direção. [curious] No meio do caminho tem um engano, em que as derivadas parciais mentem sobre o campo. E, no final, a gente junta tudo numa tabela de quatro números, que revela o giro, a mudança de área e aquela deformação do quadradinho que ficou sem explicação. [happy] Então vamos começar pelo chão: o que é chegar perto?

### B1-1 · tela: layout B, dois painéis; a seta de X em destaque e a cópia que viaja para a origem (§2.4, alvo 41)
[thoughtful] Vamos usar duas telas. Na da esquerda está o campo, e é ali que você anda: tem um ponto fixo, e você vai se aproximando dele. A seta do lugar onde você está fica em destaque. Na da direita, eu trago essa seta para a mesma origem, para comparar só onde a ponta dela chega. Uma tela mostra por onde você anda; a outra, onde a seta chega.

### B1-2 · tela: os dois números (‖X − P‖ e ‖F(X) − L‖) encolhendo juntos; `∀ε`/`∃δ` ainda não
[curious] Conforme você chega perto do ponto, a ponta da seta vai chegando perto de uma seta-alvo. Essa seta-alvo é a candidata a limite. Os dois números de baixo contam a história: a distância até o ponto encolhe, e a distância da ponta até o alvo encolhe junto. Só que "encolhe junto" ainda é vago. Perto quanto? Então a definição vira um desafio.

### B1-3 · tela: o disco ε, o disco δ e a mancha das pontas (alvo 03)
[thoughtful] Primeiro, alguém escolhe uma tolerância na chegada: um disquinho de raio épsilon em volta da ponta do alvo. É como se dissesse: quero todas as respostas aqui dentro. Qualquer épsilon pode ser escolhido, por isso a definição começa com "para todo épsilon". Depois é a sua vez: você responde com um disquinho de raio delta em volta do ponto. E olha o que acontece do outro lado: cada ponto do seu disco manda a ponta da seta para algum lugar, e todas essas pontas juntas formam uma mancha. A pergunta é uma só: a mancha cabe no disco épsilon?

### B1-4 · tela: δ = 0,7 vaza em vermelho; δ = 0,41 cabe; tabela ε → δ (alvo 04)
[curious] Com delta igual a zero vírgula sete, não cabe: um monte de pontas escapa. Diminui o delta… e a mancha encolhe junto. Em zero vírgula quatro um, ela fica inteira por dentro. Achou: é isso que "existe delta" quer dizer. Se o desafio aperta para meio, você aperta para zero vírgula dois um. Para um quarto, zero vírgula um zero. O delta depende do épsilon, e o limite existe quando você sempre consegue responder.

### B1-5 · tela: ponto de acumulação, ponto isolado e a definição escrita (alvos 05 e 06)
[thoughtful] E tem um detalhe no seu disco: o próprio ponto fica de fora. É o "maior que zero" da definição. O limite só olha para quem está chegando, nunca para o que acontece em cima do ponto. Aliás, o ponto nem precisa estar no domínio: basta ter pontos do domínio tão perto dele quanto você quiser. O nome disso é ponto de acumulação. Já um ponto do domínio sozinho, sem vizinhos, não serve: ninguém chega perto dele. Agora sim, escrito: a seta-alvo é o limite quando, para todo épsilon positivo, existe um delta positivo tal que, para todo ponto do domínio a uma distância maior que zero e menor que delta, a seta fica a menos de épsilon do alvo. A metade da esquerda fala de onde você anda. A da direita, de onde a seta chega.

### B1-6 · tela: as sombras na grade e o quadrado que cabe no disco (alvo 07)
[curious] E tem um atalho. Se a ponta está no disco épsilon, as duas sombras dela, a horizontal e a vertical, ficam a menos de épsilon das sombras do alvo. E o contrário também vale: se as duas sombras estão perto, a ponta cai num quadrado, que cabe num disco só um pouquinho maior. Então o limite de um campo existe exatamente quando o limite de cada componente existe, e aí é o limite de funções de várias variáveis que você já conhece. Mas guarda uma coisa: com várias variáveis, o caminho pelo qual você chega pode mudar completamente a resposta.

### B2-1 · tela: o campo G, os três caminhos (alvo 08)
[curious] E é justamente isso que acontece com este campo encrenqueiro. Todas as setas são horizontais. Nos eixos, não tem seta nenhuma; nas diagonais, as setas têm tamanho um: numa delas apontam para a direita, na outra, para a esquerda. Só que a resposta muda com a direção por onde a gente chega.

### B2-2 · tela: a reta de inclinação m e `2m/(1+m²)`
[thoughtful] Vem andando até a origem pelo eixo horizontal: a seta é zero o caminho todo. Pela diagonal de subida: um, para a direita. Pela outra: um, para a esquerda. Numa reta qualquer pela origem, o campo vale o dobro da inclinação, dividido por um mais a inclinação ao quadrado. Três caminhos, três resultados diferentes. Muda a reta, muda o valor.

### B2-3 · tela: `G = (sen 2θ, 0)`, a volta no círculo e a ponta varrendo o segmento (alvo 09)
[curious] E dá para ver isso de um jeito mais bonito. Em coordenadas polares, a componente horizontal vira o seno do dobro do ângulo. O campo não depende da distância, só da direção. Então dá uma volta num círculo minúsculo em volta da origem: a ponta da seta varre o segmento inteiro, de menos um até um. Diminui o raio… e diminui de novo: acontece exatamente a mesma coisa, por menor que seja o círculo.

### B2-4 · tela: o desafio ε = 1/2 não cabe; o campo K e a parábola (alvo 10)
[thoughtful, emphatic] Agora joga o desafio. Escolhe um alvo qualquer e um épsilon de meio. O disco tem largura um, e o segmento tem largura dois: não cabe, seja qual for o alvo. Então não existe limite na origem. E fica um cuidado: dois caminhos com valores diferentes provam que o limite não existe. Mas todas as retas darem o mesmo valor ainda não provam que ele existe, porque dá para chegar por uma curva. Olha este campo: por qualquer reta, a seta vai para zero. Mas, pela parábola, ela fica em meio o caminho todo. Também não tem limite.

### B3-1 · tela: os três pedaços ①②③ (alvo 11)
[thoughtful] Agora a continuidade. A definição tem três pedaços, e cada um pode falhar. Um: o ponto está no domínio, então a seta do ponto existe. Dois: o limite ali existe. Três: o limite é igual à própria seta do ponto. Na figura, é o mesmo desafio de antes, só que agora o disco épsilon fica em volta da ponta da seta do próprio ponto. No nosso campo, a mancha cabe. Contínuo.

### B3-2 · tela: três cartões com os caminhantes (§2.5, alvos 42 e 12)
[curious] Agora, três jeitos de dar errado, e em cada um você vai chegando no ponto para ver o que a seta faz. No campo elétrico de uma carga, o ponto da carga nem está no domínio, e quanto mais você chega perto, mais a seta cresce. Falha o primeiro pedaço, e a pergunta nem se faz; em todo o resto, ele é contínuo. No campo encrenqueiro, definido como zero na origem, a seta existe, mas o limite não: dependendo do caminho por onde você chega, a seta vai para a direita, para a esquerda ou para zero. Falha o segundo. E neste aqui todas as setas apontam para a direita, menos a do centro, que aponta para cima. Chegando de qualquer lado, a seta é para a direita; só em cima do ponto ela vira para cima. O limite existe e é a seta para a direita, mas a seta do ponto é outra. Falha o terceiro: um salto bem em cima do ponto.

### B3-3 · tela: componentes e operações (alvo 13)
[thoughtful] E, de novo, por componentes: o campo é contínuo exatamente quando cada componente é contínua. Por isso quase todo campo que vem de fórmula é contínuo onde está definido: somas, produtos, quocientes com denominador diferente de zero e composições de funções contínuas continuam contínuas. A primeira componente do nosso campo é uma constante mais senos: contínua. E o campo da carga é um quociente: contínuo em todo lugar, menos em cima da carga.

### B4-1 · tela: a corda em x e o quociente (alvo 14)
[thoughtful] Agora sim: medir como a seta muda. Fica no ponto e anda só na horizontal, um passo. A seta muda de uma para outra, e a diferença entre as duas é um vetor, que liga a ponta velha à ponta nova. Divide esse vetor pelo tamanho do passo e encolhe o passo. Esse limite é a derivada parcial do campo na direção horizontal.

### B4-2 · tela: a velocidade da ponta e as sombras (alvo 15)
[curious] Com passo um, o quociente vale zero vírgula oito quatro e dois vírgula um quatro. Com meio, zero vírgula nove seis e dois vírgula um seis. Com passo cada vez menor, ele vai chegando em um e dois. E olha a tela da chegada: andando na horizontal, a ponta da seta desenha uma curva. A diferença é uma corda dessa curva, e, dividida pelo passo, ela vira a seta tangente. Então a derivada parcial é a velocidade da ponta, quando você anda na horizontal com velocidade um.

### B4-3 · tela: as duas sombras: `∂P/∂x = 1`, `∂Q/∂x = 2`
[thoughtful] E essa velocidade tem duas sombras. A horizontal diz quanto muda a componente horizontal do campo: um. A vertical diz quanto muda a componente vertical: dois. Por isso a conta é por componentes: a derivada do campo é a derivada de cada componente.

### B4-4 · tela: a derivada em y (alvo 16)
[curious] Agora na vertical. Andando para cima, a ponta anda num círculo, e o quociente vai chegando em menos um e zero: a derivada na direção vertical aponta para a esquerda, tangente ao círculo.

### B4-5 · tela: as derivadas no palco e as fórmulas (alvo 17)
[thoughtful, emphatic] Então a derivada parcial de um campo não é um número: é um vetor, que diz como a seta muda quando você anda numa direção. Na conta, a derivada na horizontal dá cosseno e dois cossenos mais seno, da coordenada horizontal; no ponto, um e dois. A derivada na vertical dá menos cosseno e seno da coordenada vertical; no ponto, menos um e zero. A conta bate com o desenho. E, num campo no espaço, aparece uma terceira, na direção da profundidade, com a mesma ideia.

### B5-1 · tela: o campo G: as duas parciais valem zero (alvo 18)
[curious] Só que tem uma armadilha. Volta no campo encrenqueiro e calcula as derivadas parciais na origem. Pelo eixo horizontal, a seta é zero o tempo todo: derivada zero. Pelo vertical, mesma coisa. As duas existem, e as duas são zero.

### B5-2 · tela: previsão × imagem de verdade (alvo 19)
[thoughtful] Se você confiasse só nelas, ia prever que, perto da origem, tudo vai para perto do zero: um quadradinho em volta da origem iria parar num ponto só. Mas olha a imagem de verdade: a ponta varre o segmento inteiro, de menos um até um. A previsão errou feio. As parciais só olham duas retas, e esse campo esconde tudo nas diagonais. Ele nem é contínuo na origem.

### B5-3 · tela: gráficos da derivada: sempre 1 × 2/y; classe C¹ (alvo 20)
[thoughtful, emphatic] O que faltou? Olha as próprias derivadas, andando pelo eixo vertical. No nosso campo, a derivada na horizontal vale um o caminho todo, sem salto nenhum. No encrenqueiro, ela vale dois dividido pela altura: explode perto da origem, e na origem vale zero. Essa é a condição de classe cê um: as derivadas parciais existem e são contínuas, numa vizinhança do ponto. Ela é suficiente para a aproximação linear funcionar. Classe cê erre é o mesmo, até as derivadas de ordem erre.

### B5-4 · tela: a malha vira quase paralelogramo (alvo 21) e o gráfico erro ÷ passo (alvo 22)
[curious] E com ela vem a promessa. Pega uma malhinha em volta do ponto e manda para a tela da chegada. As linhas horizontais viram curvas na direção da derivada horizontal, e as verticais, curvas na direção da derivada vertical. Cada quadradinho da malha vira quase um paralelogramo, com lados de passo vezes derivada. Escrito: a seta num ponto vizinho é a seta do ponto, mais o passo horizontal vezes a derivada na horizontal, mais o passo vertical vezes a derivada na vertical, com um erro que some mais rápido que o passo. O nosso campo, feito de senos e cossenos, é cê um. O encrenqueiro, não. E dá para ver isso dividindo o erro pelo passo. No nosso campo, quando o passo cai pela metade, essa conta cai pela metade também, e vai para zero. No encrenqueiro, ela dobra. É a diferença entre ter duas derivadas parciais e ter uma aproximação linear de verdade.

### B6-1 · tela: janela com zoom ×10, a seta do centro e o resto (alvos 23 a 25)
[curious] Então vamos usar isso. Pega o campo da aula e chega dez vezes mais perto do ponto: essa janelinha vira o palco inteiro. De perto, todas as setas ficam parecidas com a seta do centro. Cada uma é a seta do centro, mais um restinho. Tira a seta do centro de todas… e sobra só a mudança. Olha que campo arrumadinho.

### B6-2 · tela: a matriz jacobiana (alvo 26)
[thoughtful] Bem de perto, essa mudança é escrita com as duas derivadas. Então coloca as duas lado a lado, como colunas: a derivada na horizontal na primeira, a derivada na vertical na segunda. Fica uma tabela de quatro números, com as derivadas das duas componentes nas duas direções. Ela tem nome: matriz jacobiana. No nosso ponto, um e menos um em cima, dois e zero embaixo.

### B6-3 · tela: `J·H` como combinação das colunas (alvo 27)
[curious] E ela funciona assim: um passo com uma parte horizontal e uma vertical vira a parte horizontal vezes a primeira coluna, mais a parte vertical vezes a segunda. A seta do modelo é a soma das duas. É a primeira aproximação do campo perto do ponto.

### B6-4 · tela: as colunas empurram as arestas e o fluxo do modelo (alvos 28 e 29)
[thoughtful] Agora coloca um quadradinho com a quina no ponto. A quina da direita é empurrada pela primeira coluna; a de cima, pela segunda. Cada coluna empurra uma aresta. Solta o fluido no modelo… e o quadradinho gira, cresce e entorta, tudo ao mesmo tempo. Tudo isso, no modelo linear, estava nos quatro números.

### B7-1 · tela: a matriz de movimentos de aresta (alvo 30)
[thoughtful] E dá para separar essa bagunça, lendo cada número da tabela como um movimento de aresta. Em cima, à esquerda: quanto a aresta horizontal estica. Aqui, um. Embaixo, à esquerda: quanto ela gira. Dois. Em cima, à direita: quanto a aresta vertical tomba para o lado. Menos um, para a esquerda. Embaixo, à direita: quanto ela estica. Zero.

### B7-2 · tela: as combinações: rot, div, deformações (alvos 31 e 33)
[curious] Agora junta. Os dois giros no mesmo sentido, somados, dão o rotacional: dois mais um, três. Os dois estiramentos somados dão o divergente: um mais zero, um. E sobram duas comparações. Estiramento horizontal menos vertical: um. Essa é a primeira deformação, quanto o pedacinho estica mais numa direção do que na outra. E a diferença entre os dois giros: dois menos um, um. Essa é a segunda, quanto o ângulo reto do quadradinho fecha, como uma tesoura.

### B7-3 · tela: os três cartões, com o quadradinho agindo (§2.6, alvos 32 e 34)
[thoughtful, emphatic] Quatro números entram, quatro medidas saem, e nada se perde no caminho. Bem de perto e sem a seta do centro, a variação de primeira ordem de todo campo cê um é uma mistura de quatro campos simples: um redemoinho, uma explosão e duas deformações. Olha cada um agindo no quadradinho: o redemoinho gira, a explosão cresce, a deformação estica de um lado e achata do outro. E isso não é só matemática: num fluido newtoniano, o atrito viscoso vem da deformação. Um bloco de fluido girando inteiro, rígido, não tem atrito viscoso nenhum por dentro.

### B7-4 · tela: volta ao gancho: tudo é deformação (alvo 35)
[curious] Agora volta lá no começo. No campo que esticava o quadradinho, a tabela é um e zero em cima, zero e menos um embaixo. A aresta horizontal estica, a vertical encolhe na mesma medida, e ninguém gira. Rotacional zero, divergente zero, e a primeira deformação vale dois. É tudo deformação.

### B7-5 · tela: o desafio do episódio passado (alvo 36)
[happy] E lá no episódio passado ficou um desafio: achar outro campo, que não fosse constante, com rotacional e divergente zero. Um deles é este, que troca as coordenadas de lugar. As duas arestas giram uma contra a outra: a segunda deformação vale dois, e o quadradinho vira losango. É o mesmo campo de antes, girado quarenta e cinco graus. E quem achou um de segundo grau, como o da tela, também acertou. Rotacional e divergente, sozinhos, não dizem tudo sobre como um campo varia.

### S1 · tela: o resumo (alvo 37); a tag do zoom não aparece aqui (§2.7)
[thoughtful] Resumindo: limite é ganhar o desafio do épsilon com um delta. Continuidade é o limite igual à seta do ponto, sem salto. A derivada parcial é a velocidade da ponta numa direção. E, quando essas derivadas são contínuas, a tabela delas descreve o campo bem perto do ponto: giro, área e deformação. E uma curiosidade: no espaço, a tabela tem nove números, que se separam em três de giro, um de volume e cinco de deformação.

### S2 · tela: o cartão do próximo vídeo (§2.2, alvo 40), depois o CTA padrão
[excited] No próximo vídeo, é a vez de colocar a mão na massa: o integrador do módulo, só com exercícios. Campo vetorial, rotacional, divergente, limite e continuidade, derivadas parciais, tudo junto. E vai ser a sua hora de pegar um campo, montar a tabela e descobrir se o quadradinho vai girar, mudar de área ou deformar. [happy] Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e conta nos comentários: qual dessas medidas, giro, expansão ou deformação, você acha que aparece mais na física? Até a próxima!
