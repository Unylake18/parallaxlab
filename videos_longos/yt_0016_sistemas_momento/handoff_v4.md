# yt_0016 — avaliação do preview v3 e HANDOFF v4 (último preview antes da narração)

Data: 2026-10-29. Base: zip do preview v3 (960×540 / 15 fps, 20:09, 18.141 quadros), relatório do Claude Code e pedido do Kaio (2026-10-29, 02:35).
Método: quadros a cada 0,2 s, folhas de contato a cada 7 s em todo o vídeo, quadros em resolução cheia nos pontos suspeitos e diferença quadro a quadro (ffmpeg) para achar travadas.

(Cópia salva na unidade pelo Claude Code, 2026-10-29, conforme o §0. A narração completa do Anexo A está em `narracao_v3.md`.)

---

## Parte 1 — Avaliação do v3

**Veredito:** o v3 está perto do fechamento. O tempo morto sumiu (a única pausa ≥ 4 s é o cartão final), o resumo tem as três ideias, o E7 tem a normal e a decomposição, o gelo ficou certo e o T9 tem os gráficos empilhados. Faltam quatro famílias de problema: **(1)** sobreposições pontuais de texto, quase todas em viradas de cena; **(2)** travadas de quadro no cavalo; **(3)** cavalo demais, no começo e ao longo do vídeo; **(4)** a luz da coda, que está fraca. Mais os loops do T9 e do T10, que reiniciam demais.

### 1.1 Sobreposições (tempos do v3)

| # | Tempo | Bloco | O que acontece | Correção (§ do handoff) |
|---|---|---|---|---|
| S1 | 0:42 | A1 | A pergunta do hook e o cavalo ainda aparecem, fantasmas, atrás do logo "BEM-VINDOS" | 2.1 |
| S2 | 3:09 | T7-3 | Soma das duas equações encavalada: o `dt` de `d(p⃗₁+p⃗₂)/dt` encosta na 2ª linha, a 2ª linha sai espremida, e "TERCEIRA LEI: IGUAIS E OPOSTAS" quase some sobre o chão 3D | 2.4 |
| S3 | 5:17–7:56 | T8 | `−T⃗` e seu rótulo desenhados sobre o tronco do cavalo; "600 kg" escrito no corpo | 2.2 |
| S4 | 8:12 | T8-7 → T8-8 | Crossfade: o diagrama do Cyrano (texto e fronteira) aparece fantasma sobre o manequim andando | 1.3 |
| S5 | 9:18,8–9:19,2 | T9-2 → T9-3 | Os blocos de 1 kg e 2 kg, "LEVE/PESADO" e "CHÃO COM ATRITO" entram **por cima** da cena bola + Terra, ainda inteira | 1.3 |
| S6 | 9:18 e 10:20–11:08 | T9 | Chip "CÂMERA LENTA" sobre o arco da Terra e, depois, colado no começo do eixo de P_Terra | 2.6 |
| S7 | 11:10 e 11:37 | T10 | Resíduo apagado do capítulo anterior no canto direito (11:10); no reinício do loop, os blocos aparecem **duplicados** (os do fim e os do começo ao mesmo tempo, 11:37,6) | 2.7 |
| S8 | 12:15 | T10-4 | "QUANTO MAIOR A DIFERENÇA…" em corpo minúsculo, ilegível | 2.7 |
| S9 | 13:11 | E6-3 | "COMO A PAREDE DO VÍDEO ANTERIOR: REBATER TRANSFERE…" escrito por cima do bloco "AGARRA" (apagado, mas legível) | 2.8 |
| S10 | 13:18–13:32 | E6-4 | Rótulo "0,25 J" encostado na base das barras e na coluna vizinha | 2.8 |
| S11 | 14:07–14:28 | E7-3/4 | Arco tracejado de p_x até o recuo atravessa o corpo do caçador; rótulo `N⃗ (EXTERNA, IMPULSIVA)` encostado em "LAGO CONGELADO · SEM ATRITO" | 2.9 |
| S12 | 15:45–15:59 | E8-3/4 | A linha tracejada do zero corta os rótulos `p_rifle` e `p_gases`; a DICA entra colada em `p_gases = +0,866` | 2.10 |
| S13 | 16:34 | E9-2 → E9-3 | Crossfade: "TANGENCIAL: IGUAL / NORMAL: INVERTIDA", `θ₁′ = θ₁` e o espelho aparecem fantasmas sobre o tanque de água | 1.3 |
| S14 | 17:58 | E9-7 | O selo DICA do E9-7 só aparece como um retângulo apagado no fim e não chega a ser lido | 2.11 |
| S15 | 19:22 | S1 | Rótulo "INTERNA" escrito na barriga do cavalo | 2.2 |
| S16 | 19:45–19:50 | S2 | Ideia 3 fica só ~5 s; a faixa do chão 3D continua atravessando atrás do texto da CONTA; o ícone da Terra (arco) encosta no texto "NÃO CONSERVA?" | 2.13 |

Os de 6:32 (rótulos `v = …` no canto do PALCO) estão aceitáveis.

### 1.2 Travadas de quadro (o "pipocado" que o Kaio viu)

Medição: diferença média entre quadros consecutivos. Quando o cavalo está andando, dois quadros quase idênticos seguidos mostram um **quadro repetido**. Um salto isolado muito acima da média mostra um **pulo de posição**.

- **Quadro repetido a cada ~1,1 s** no hook (0:15,5 · 0:16,6 · 0:17,7 · 0:23,0 · 0:24,3 · 0:32,1) e em 0:44,1 (o cavalo ao fundo do A2). O período é o do ciclo de passo. Causa provável: o ciclo de caminhada foi renderizado com o último quadro igual ao primeiro (t de 0 a T **inclusive**). Ao emendar os ciclos, esse quadro aparece duas vezes e o cavalo "engasga" a cada passada.
- **Pulos de posição nas emendas entre tomadas:** 1:14,7–1:15,2 e 1:28,4 (abertura), 6:30,7–6:31,2, 7:23,9 e 7:52,0 (T8). Causa provável: o crossfade junta duas tomadas do mesmo enquadramento com o cavalo em posições diferentes, e durante 0,5 s aparecem dois cavalos meio transparentes que "pulam".
- O corte em 8:12 e o de 19:49 são viradas de cena normais (o problema do 8:12 é o fantasma do texto, S4).

### 1.3 O cavalo: quanto tempo e quantas vezes

Hoje ele aparece em: **hook** (0:01–0:42, ~34 s andando antes da pergunta), **A2** (ao fundo, apagado), **A5** (1:31–2:13), **A6** (ao lado do mapa), **T8** (5:17–7:56) e **resumo** (19:12–19:50). São seis entradas.

O que cada uma faz pela física:
- **Hook: precisa, mas curto.** Mostra a pergunta. Bastam ~18 s, com a fala enxuta (Anexo A) e a câmera fazendo alguma coisa (push-in até a corda, recuo para a pergunta).
- **A2: não precisa.** Ele só fica andando ao fundo. Vira uma miniatura parada do hook, com a pergunta.
- **A5: precisa.** É a virada da série: a mesma força da corda muda de papel quando a fronteira cresce. Fica.
- **A6: não precisa.** O mapa dos dois vídeos vai para o CENTRO, sem cavalo.
- **T8: precisa.** É a resposta da pergunta e o exercício resolvido com números. Fica, com as travadas e o trecho parado no gelo corrigidos e duas câmeras alternando, para não ser o mesmo plano por 2:39.
- **Resumo: precisa, curto.** Fecha o arco do vídeo (a fronteira cresce até "+ TERRA").

Resultado: o cavalo cai de seis entradas para **quatro** (hook, A5, T8, resumo) e de ~4:50 de tela para ~3:40.

O T8-6 (gelo) tem um problema próprio. A física está certa: a −1,26 m/s², o conjunto para em ~3 s. Mas depois o cavalo fica ~25 s parado, só com os cascos girando (7:28–7:53). A correção (§2.3) mostra a desaceleração em câmera lenta e enche o resto com o que a fala diz: patas escorregando e a comparação firme × gelo.

### 1.4 Luz da coda (C-1, 18:05–18:30)

Hoje são dois traços cinza tracejados batendo num retângulo preto e num retângulo cinza, com as setas F e 2F. Não parece luz, e não mostra o que a fala diz: a luz carrega momento, entrega esse momento e, no espelho, entrega o dobro. O redesenho está no §2.12. A luz passa a ser **amarela com brilho**, com fótons como pacotes de onda e uma seta de momento magenta em cada um. A placa preta absorve e esquenta (flash laranja de calor). O espelho devolve o fóton e a placa recebe o dobro. As duas placas ficam penduradas por fios e balançam, uma o dobro da outra.

**Cor nova:** `LUZ = #FFD25A`, com brilho `#FFE9A8`. Vale só para luz (coda, os corpúsculos do E9 e os fótons da vela). Não conflita com nenhuma grandeza da paleta (o verde continua proibido). Registrar no `padrao_video_longo.md` quando o vídeo fechar.

### 1.5 Loops do T9 e do T10

- **T9 (10:18–11:08):** o evento inteiro (1,02 s) é reproduzido em câmera lenta e **recomeça a cada ~2,6 s por quase um minuto**. O contador `t` e os gráficos voltam a zero a cada volta. Nos quadros soltos parece que o tempo corre para trás (t = 0,89 → 0,49 → 0,89 → 0,14). Cansa e confunde exatamente no gráfico que precisa ser lido com calma.
- **T10 (11:10–12:15):** a cada volta (~7,5 s) as barras de energia somem e voltam a crescer, e o reinício dos blocos é um crossfade que mostra os blocos em dobro.

### 1.6 Pendências do relatório do v3 (todas entram no v4)
E7: arco atravessando o corpo (S11). T9: chip CÂMERA LENTA (S6). T8: ~25 s parado no gelo (§1.3). Headers: resíduo na virada (§1.1 e regra 1.3). Handoff não salvo na unidade (§0).

---

## Parte 2 — HANDOFF v4

### 0. Rodada
- Unidade `videos_longos/yt_0016_sistemas_momento/` (preview v3). Rode `git status --short`. Copie a unidade para `_v3/` (código, ficha e âncoras; sem renders) antes de editar. **Salve este handoff na unidade como `handoff_v4.md`** (e o v3 como `handoff_v3.md`, se ainda tiver o texto).
- **Objetivo:** preview silencioso **v4** 960×540 / 15 fps, completo, mais os stills da §5. **Este é o último preview antes da narração.** Depois dele vêm a voz e a sincronização. Por isso as âncoras, a ordem e os capítulos do v4 têm de ser os definitivos, seguindo a **narração v3** do Anexo A.
- Re-renderize só os lotes afetados: provavelmente hook/abertura, T7, T8, T9, T10, E6, E7, E8, E9, coda e resumo.
- Sem voz, SRT, master, entrega, commit ou push. Não alterar `template/`, `docs/`, `assets/`, `experimentos/threejs/` nem o yt_0015.

### 1. Regras gerais novas (valem para o vídeo todo)

**1.1 Sem quadro repetido nem pulo no 3D.**
- Ciclos de caminhada (cavalo e manequim) renderizados com `t` de 0 a T **exclusivo**: o quadro N do ciclo é o quadro 0 do seguinte e não pode ser gravado duas vezes. Melhor ainda: renderize cada tomada como **uma sequência contínua** do Three.js, com o deslocamento contínuo do corpo, sem emendar ciclos depois.
- Renderize o Three.js **na mesma taxa do vídeo** (15 fps no preview; a taxa do final no render final) ou num múltiplo inteiro dela. Nada de reamostrar a taxa com o ffmpeg, que duplica ou pula quadros.
- **Mesmo enquadramento → uma tomada contínua**, sem emenda. **Enquadramento diferente → corte seco**, no começo de uma frase da fala. Nunca crossfade entre duas tomadas do mesmo plano com o cavalo em posições diferentes.

**1.2 Loops com no máximo uma repetição.** Uma animação de evento (bloco disparando, tiro, bola) roda **uma vez** sincronizada com a fala. Se a fala precisar revê-la, faça **um** replay sempre para a frente, com o chip `REPLAY` no PALCO. Depois disso, o estado final **fica** e o "algo acontecendo" vem dos realces (o termo da conta acende junto com o objeto no desenho). Gráficos e barras nunca são apagados para recomeçar. Loops contínuos só onde o objeto é o "palco vivo" de fundo (cavalo andando, esferas vibrando, vela girando).

**1.3 Viradas de cena em sequência, nunca em crossfade de layouts.** Sai tudo o que é da cena anterior (texto, fronteira, rótulos e 3D) em 0,3 s. Depois entra o novo em 0,3 s. Header junto: sai em 0,25 s, entra em 0,25 s. Crossfade só quando o **mesmo** objeto continua no PALCO. Isso resolve S1, S4, S5, S7, S13 e o resíduo dos headers.

**1.4 Nada escrito sobre corpo 3D.** Nenhum rótulo ou massa sobre o cavalo, a pedra, o manequim ou a vela. Massas vão como dado na CONTA (`m_cavalo = 600 kg`) ou numa etiqueta abaixo da linha do chão, sob o corpo. Rótulos de seta pelo lado livre, `buff ≥ 0,15`, folga ≥ 0,25 de qualquer outro texto (regra do v3, agora cobrando também 3D × texto).

**1.5 Tamanho mínimo de texto.** Nenhum texto lido em voz menor que o corpo `BODY` da CONTA. Legendas pequenas (`CAPTION`) só para notas que a fala não lê.

**1.6 Fundo da CONTA escuro.** Onde o 3D tem chão (T7, T8, E6, E7, resumo), o chão não atravessa a zona CONTA. Ou o render 3D é cortado/escurecido em x > 0,6 (degradê de 0,6 a 1,0 para o fundo `#05070D`), ou a CONTA fica sobre o painel `PANEL`.

### 2. Correções por bloco

**2.1 Hook e abertura (0:00–2:18). Prioridade.**
- **Hook com ~18 s**, seguindo a fala nova do Anexo A (H1–H3). O cavalo já está andando no primeiro quadro: nada de entrada lenta.
  - H1 (~6 s): câmera lateral baixa. As setas `T⃗` (na pedra, para a frente) e `−T⃗` (no balancim, para trás; ver 2.2) entram juntas em 0,5 s.
  - H2 (~6 s): as duas setas pulsam juntas. Um `=` pequeno aparece entre os dois rótulos de módulo (`|T⃗| = |−T⃗|`). Push-in lento da câmera até a corda e um "?" suave sobre o cavalo.
  - H3 (~6 s): a câmera recua. O cavalo baixa para 40% e a pergunta central entra: `SE A CORDA PUXA O CAVALO PARA TRÁS COM A MESMA FORÇA, COMO ELE ANDA?`.
- **A1 (logo):** fundo limpo. O cavalo e a pergunta saem inteiros antes de o logo entrar (S1).
- **A2:** **sem o cavalo andando.** No PALCO entra uma **miniatura parada** do último quadro do hook (moldura fina, zoom lento de 1,00 a 1,05) com a pergunta embaixo, em `CAPTION`. Na CONTA, `MOMENTO EM SISTEMAS · NESTE VÍDEO: O QUE MUDA O MOMENTO DE VÁRIOS CORPOS`.
- A3 e A4 como no v3.
- **A5: o cavalo fica** (é a virada um corpo → sistema), com uma tomada contínua só (1.1). A seta azul que vira cinza é a `−T⃗` do balancim.
- **A6: sem o cavalo.** O mapa dos dois vídeos fica no CENTRO, em duas colunas: `VÍDEO ANTERIOR · UM CORPO → F⃗_res = dp⃗/dt` (apagado, com um ícone do disco) e `HOJE · MUITOS CORPOS → ?` (com um ícone das três esferas). O "?" migra para o canto da CONTA, como já era.

**2.2 Setas da corda e o balancim (hook, A5, T8, resumo).**
- Na vista lateral, uma seta que nasce no arreio do peito e aponta para trás, ao longo da corda, **sempre cai sobre o tronco do cavalo**. A solução é a de um cavalo de tração de verdade: a corda prende num **balancim** atrás da anca, uma barra curta horizontal (~0,35 da largura do corpo, aço `#B8C4DA`) logo atrás das patas traseiras, na altura do jarrete. Do balancim, dois **tirantes** finos sobem pelos lados do corpo até o peitoral. A pedra é puxada pela corda presa no balancim.
- Faça isso **na cópia do asset dentro da unidade** (não no yt_0015 nem em `experimentos/threejs/`). Exporte o ponto do balancim em `pontos.json`, como o arreio.
- `−T⃗` (no hook, `−F⃗` vira `−T⃗`; padronize): cauda **no balancim**, apontando para trás ao longo da corda, deslocada ~0,15 acima dela. Fica inteira atrás do cavalo. `T⃗`: cauda na amarração da pedra, para a frente. Mesmo comprimento na tela. Rótulos acima da corda, no vão entre a pedra e o cavalo, nunca na barriga.
- O valor `2.608 N` vai junto da seta, acima da corda. As setas do chão (2.352 N na pedra, 2.800 N nas patas) e os rótulos delas ficam abaixo da linha do chão.
- Tirar "600 kg" e "800 kg" de cima dos corpos (1.4): `m_cavalo = 600 kg` e `m_pedra = 800 kg` entram como dados na CONTA (T8-1).
- No resumo (S1), o rótulo "INTERNA" vai acima da corda, no vão, nunca no corpo (S15).

**2.3 T8: cavalo e pedra (5:17–8:30).**
- Travadas: aplicar 1.1 (pulos em 6:30,7–6:31,2, 7:23,9 e 7:52,0).
- **Duas câmeras, alternando por corte seco** no começo das frases: (a) **lateral** com as setas, para T8-1, T8-2, T8-4 e T8-5; (b) **3/4 baixa, perto das patas**, para T8-3 (a aceleração) e para a entrada do gelo. Assim o bloco deixa de ser o mesmo plano por 2:39.
- **T8-6, gelo (sem os 25 s parado):**
  1. (~2 s) o gelo surge sob as patas (placa translúcida do v3) e os cascos começam a escorregar.
  2. (~6 s) **desaceleração em câmera lenta** (chip `CÂMERA LENTA` no canto superior esquerdo do PALCO): o mostrador `v = … m/s` desce de ~3,5 até 0,00 com a seta violeta encolhendo, a −1,26 m/s² na escala do tempo real.
  3. (~resto da fala, ~8–10 s) o cavalo **não fica parado**: as patas escorregam no lugar (as traseiras derrapando para trás, com um spray fino de gelo `#9CC7FF` a 50%), e o corpo balança ±2 cm.
  - Na CONTA, quando a fala diz "o cavalo é o mesmo, a corda é a mesma": comparação lado a lado com duas barras horizontais de força externa nas patas, `CHÃO FIRME: 2.800 N` × `GELO: 588 N`, cada uma ao lado de `2.352 N` (atrito da pedra) e o veredito `ANDA` / `PARA`.
  - Corte para o T8-7 (Cyrano) no fim da frase. Nada de cavalo parado esperando.
- T8-7 → T8-8: virada em sequência (1.3). O diagrama do Cyrano sai inteiro antes de o manequim entrar (S4).

**2.4 T7-3, a soma (3:05–3:20) (S2).** Layout fixo, em três linhas na CONTA, tudo em `Math` normal (não espremer com `scale_to_fit_width` abaixo do `Math S`):
- linha 1 e linha 2: as duas equações (como no v3), com o `+` à esquerda da linha 2;
- traço de soma;
- linha 3: `d(p⃗₁ + p⃗₂)/dt = F⃗₁₍₂₎ + F⃗₂₍₁₎ + F⃗^ext` numa linha só. Se não couber, quebre **depois do `=`** e alinhe a continuação pelo `=`, com 0,3 de espaço vertical entre as linhas (a fração não pode encostar na linha de baixo).
- `TERCEIRA LEI: IGUAIS E OPOSTAS` em `CAPTION` branco 80%, abaixo da linha 3, com folga ≥ 0,25, sobre o fundo escuro da CONTA (1.6). Nada de texto sobre o chão 3D.

**2.5 T9-2 → T9-3 (9:18) (S5).** Virada em sequência: a bola, a Terra, a fronteira e a conta saem inteiras. Depois entram os blocos, "LEVE/PESADO" e "CHÃO COM ATRITO".

**2.6 T9-3 a T9-7, os blocos com atrito (S6 e §1.5).**
- O evento (1,02 s) roda em **câmera lenta 4×** (≈ 4,1 s na tela), **uma vez**, sincronizado com T9-5/T9-6. O contador `t` só sobe. O ponto de P(t) desenha a curva enquanto anda, desce até `(0,51 s; −1,0)` quando o pesado para e sobe até `(1,02 s; 0)`.
- Em T9-6, com o estado final na tela, o ponto `(0,51 s; −1,0)` acende junto com o bloco pesado parado (realce, não replay).
- Em T9-7, **um** replay (chip `REPLAY`, 1.2) desenha o gráfico de P_Terra(t) embaixo, espelhado, com os dois pontos correndo juntos. Depois disso tudo fica: blocos parados, gráficos completos e a reta `P + P_Terra = 0` na CONTA.
- Chip `CÂMERA LENTA` no canto superior esquerdo do PALCO, acima dos blocos, longe dos eixos. No T9-2 (bola + Terra), longe do arco da Terra.

**2.7 T10 (S7, S8 e §1.5).**
- A mola dispara **uma vez** em T10-1. As setas de momento e as barras crescem junto com o movimento. Os blocos param em batentes nas bordas do PALCO (pequenas paredes cinza, sem rebote) e **ficam**.
- Em T10-3, quando entram `2 J` e `1 J`, **um** replay para a frente (chip `REPLAY`): os blocos somem em 0,25 s, reaparecem juntos com a mola comprimida em 0,25 s (em sequência, nunca dois pares ao mesmo tempo) e disparam de novo. **As barras não somem**: ficam no valor final; durante o replay só acendem.
- `QUANTO MAIOR A DIFERENÇA DE MASSAS, MAIOR A FRAÇÃO DA ENERGIA CINÉTICA QUE FICA COM O MAIS LEVE` no corpo `BODY` (o mesmo de "MOMENTO SE DIVIDE IGUAL; ENERGIA, NÃO"), em duas linhas.
- Resíduo do 11:10: aplicar 1.3.

**2.8 E6 (S9, S10).**
- No E6-3, o bloco "AGARRA" sai inteiro (ou sobe e encolhe para uma linha-resumo `AGARRA: V = 0,085 m/s` no topo da CONTA) **antes** de "REBATE" entrar.
- `COMO A PAREDE DO VÍDEO ANTERIOR: REBATER TRANSFERE MAIS QUE AGARRAR` vira um chip no rodapé da CONTA, depois de `V = 0,154 m/s · QUASE O DOBRO`, sem tocar em nada.
- Barras do E6-4: `0,25 J` acima da barra minúscula, com um fio-guia curto. Nunca na base nem na coluna vizinha.

**2.9 E7 (S11).**
- **Tirar o arco tracejado.** A ligação de p_x com o recuo vira um `TransformFromCopy`: uma cópia da seta p_x sai da bala, viaja **por cima da cabeça do caçador** (caminho em arco acima do corpo, nunca através dele), gira 180° e pousa como a seta do recuo nos pés. Ao mesmo tempo entra o rótulo `M V = m v cos 56°` na CONTA.
- `N⃗ (EXTERNA, IMPULSIVA)`: rótulo à esquerda da seta da normal, na altura do joelho. `LAGO CONGELADO · SEM ATRITO` vai para o canto superior direito, dentro da fronteira. Folga ≥ 0,25 entre os dois.

**2.10 E8 (S12).** Diagrama de setas do momento na CONTA:
- A linha do zero (tracejada) **para antes** dos rótulos. Cada rótulo fica na ponta livre da sua seta, com `buff 0,15`: `p_bala = +4,31` à direita da ponta, `p_rifle = −5,18` à esquerda da ponta, `p_gases = +0,866` à direita da ponta.
- Setas com a escala de 1 kg·m/s ≈ 0,35 unidades, para a de 0,866 ser legível.
- A DICA entra no rodapé da CONTA, abaixo de `Σp = 0`, com folga ≥ 0,25 de tudo.

**2.11 E9 (S13, S14).**
- E9-2 → E9-3: virada em sequência (1.3). O espelho e o texto dele saem inteiros antes do tanque.
- **Corpúsculos em amarelo** `LUZ #FFD25A` com brilho (os pontos brancos de hoje), para a luz ser sempre a mesma cor no vídeo.
- Selo DICA do E9-7 (`O IMPULSO É NORMAL: SÓ A COMPONENTE NORMAL DA VELOCIDADE MUDA`) entra logo depois de `= PREVISÃO TESTÁVEL` e fica legível ≥ 4 s antes da virada para a coda.

**2.12 Coda C-1: a luz absorvida e refletida (redesenho completo, Manim 2D).**
- **Layout:** PALCO com duas raias empilhadas (como hoje), cada uma num painel `PANEL` com rótulo no topo: `SUPERFÍCIE PRETA · ABSORVE` (em cima) e `ESPELHO · REFLETE` (embaixo). CONTA à direita.
- **Fonte:** à esquerda de cada raia, um emissor pequeno (retângulo arredondado aço `#7A8696`, com a abertura acesa em `#FFE9A8`).
- **Feixe:** faixa amarela suave da fonte até a placa. Brilho por camadas de traço sobrepostas, do mais largo e transparente ao mais fino e opaco: largura 18 / 10 / 4, opacidade 0,08 / 0,18 / 0,9, cores `#FFD25A` / `#FFD25A` / `#FFE9A8`. Nada de traço cinza tracejado.
- **Fótons:** pacotes de onda que correm pelo feixe, com espaçamento regular. Cada um é um trecho de senoide de 3 ciclos com envelope gaussiano, em `#FFE9A8` com o mesmo brilho em camadas. Um fóton em destaque por raia leva uma seta magenta pequena `p⃗` acima dele (o momento que ele carrega).
- **Placas penduradas:** cada placa fica pendurada num fio fino do teto do painel, como um pêndulo, para a força **aparecer** no movimento.
  - **Preta:** fosca (preenchimento `#0B0D12`, borda `#2A2F3A`). Cada fóton que chega **some dentro dela** e deixa um flash laranja `#FF7A3D` (calor) no ponto de impacto. A placa vai ficando com um leve brilho laranja. A seta `p⃗` do fóton destacado passa para a placa.
  - **Espelho:** gradiente metálico `#7A8696 → #B8C4DA` com uma linha de reflexo branca. Cada fóton que chega **volta** pelo mesmo feixe (um feixe de volta, mais fraco, a 60%). A seta do fóton destacado vira de `+p⃗` para `−p⃗`, e ao lado da placa aparece o mini-diagrama `Δp⃗_placa = p⃗ − (−p⃗) = 2p⃗`.
  - Com os fótons chegando sem parar, a placa preta se inclina um ângulo pequeno e a do espelho **o dobro**. As setas de força `F⃗` e `2F⃗` (azul-claro `#5AA2FF`) ficam atrás das placas, com comprimentos exatamente na razão 1 : 2.
- **CONTA**, sincronizada com a fala do C-1: `p = E / c` (p magenta, E amarelo `LUZ`, c branco) → `Δp / Δt = F` com `MOMENTO POR SEGUNDO É FORÇA` (CAPTION). Por último, `ABSORVE: F` e `REFLETE: 2F`, cada um acendendo junto com a sua placa.
- **C-2 (vela 3D):** os fótons que batem na vela passam a ser riscos curtos amarelo `LUZ`, que voltam depois de bater (refletora), em vez dos pontos brancos. O resto da vela como no v3.

**2.13 Resumo (S16).**
- O fundo do texto fica escuro (1.6): o chão 3D não passa por trás da CONTA.
- A ideia 3 (`NÃO CONSERVA? AUMENTE O SISTEMA`, com a fronteira crescendo até `+ TERRA`) entra no começo da frase dela e fica **≥ 4 s inteira** antes do encerramento. Os ícones ficam alinhados à esquerda das três linhas, sem encostar no texto.
- Rótulo "INTERNA" fora do corpo (2.2).

### 3. O que não muda
Narração (exceto o hook e as linhas `tela:` do Anexo A), âncoras, os 11 capítulos e seus títulos, cores (mais a cor nova `LUZ`), todos os números da física, o 3D já aprovado (esferas, disco, manequim, vela), a grade PALCO/CONTA, os selos de ligação e as DICAs.

### 4. QA (obrigatório antes de mandar o zip)
- **Travadas:** diferença quadro a quadro em todas as tomadas 3D. Liste (a) pares de quadros quase iguais (diferença < 15% da mediana do trecho) durante movimento e (b) saltos > 3× a mediana fora das viradas de cena. **Meta: zero** no hook, A5, T8 e resumo. Reporte a lista.
- **Sobreposição:** auditoria completa, incluindo 3D × texto (caixas projetadas do cavalo, do balancim, da pedra, do manequim e da vela) e **as viradas de cena**: em cada virada, nenhum quadro com elementos das duas cenas ao mesmo tempo, exceto o objeto 3D que continua. Confira um por um os 16 pontos da tabela 1.1.
- **Pausas:** nenhuma ≥ 4 s, exceto o cartão final.
- **Loops:** liste cada loop e quantas repetições tem. Os eventos (T9, T10, E6, E7) têm no máximo um replay.
- **Alinhamento 3D × Manim ≤ 2 px**, agora também no balancim.
- **Duração do hook ≤ 20 s.** Cavalo só no hook, A5, T8 e resumo.
- Nenhuma referência de livro e nenhum header sobreposto.

### 5. Stills 1920×1080
H2 (balancim com `T⃗` e `−T⃗` fora do corpo) · A2 (miniatura parada) · T7-3 (soma em três linhas) · T8-4 (conta + 2.608 N) · T8-6 (comparação firme × gelo) · T9-7 (gráficos completos, sem chip em cima) · T10 fim (texto em BODY) · E6-3 (rebate sem sobreposição) · E7-4 (cópia de p_x por cima da cabeça) · E8-4 (setas e DICA) · C-1 (luz: as duas placas inclinadas, fótons e flash) · RESUMO com a ideia 3.

### 6. Parada e relatório
Pare com o preview v4 completo. Relatório (AGENTS.md): arquivos alterados; lotes re-renderizados; caminhos; resultado de cada item do QA (travadas, sobreposição com os 16 pontos, pausas, loops, alinhamento, duração do hook); arquivos de teste apagados; pendências. Inclua também **o mapa de âncoras do v4** (tempo de início de cada `###`). Ele vai ser a base da sincronização com a voz na próxima rodada. Zip para avaliação como no v3. Sem commit nem push.

---

## Anexo A — Narração v3

Salva na unidade como `narracao_v3.md` (a v2 com o hook reescrito e as linhas `tela:` de A2, A6, T8-6, T9-5 a T9-7, T10-1, C-1 e C-2 atualizadas; o resto da fala igual à v2, palavra por palavra).
Estimativa do handoff: a fala do hook cai de ~110 para ~60 palavras (≈ −18 s) e o hook fica com ~18 s na tela, em vez de ~40 s. Sem o cavalo no A2 e no A6, o total previsto fica em ≈ 19:40.
