# REGRA PERMANENTE · Narração: a tela mostra a álgebra, a voz ensina (Kaio, 2026-11-15)

Vale para todo vídeo novo (curtos e longos) a partir de agora. Vídeos já entregues NÃO são refeitos.

## O que não muda
A TELA continua construindo a álgebra inteira, degrau por degrau (regra CONTA INTEIRA): primitiva com colchete, limites substituídos, frações abertas, MMC, cancelamentos, número final. Nada some da tela.

## O que muda na VOZ
1. A voz NÃO é um leitor de contas. Não ler número por número o que já está escrito ("meio, menos três dezesseis avos, mais cinco oitavos, menos três, igual a doze dezesseis avos"). Isso cansa e alonga o vídeo.
2. Em conta mecânica (aplicar limites, somar frações, MMC, simplificar, potências, substituir valores): a voz anuncia a AÇÃO e dá o RESULTADO. Modelo: "aplica os limites e abre as frações; o MMC é dezesseis, e o resultado é doze dezesseis avos, três quartos."
3. A voz CONTINUA lendo e explicando o que ensina: a definição, a propriedade usada, o porquê do passo, a troca de variável, a ideia do cancelamento, a escolha dos limites, o significado do resultado. Símbolo novo ainda é lido ("lê-se…"), conforme [[feedback-narracao-ler-simbolos]].
4. Não confundir enxugar com pular: o espectador tem de poder pausar e conferir cada degrau na tela; a voz diz onde olhar ("olha a segunda linha") e o que o degrau significa.

## O que a narração passa a ter (didática próxima)
- Tom de conversa com um aluno, 2ª pessoa ("repara", "pensa comigo", "a gente"), rigor matemático intacto.
- Exemplos e aplicações palpáveis: uma imagem do mundo (chapa de metal, prato, pizza, ponte, aro de roda, saco de areia) para cada ideia central.
- A pergunta que o espectador faria ("e se o buraco fosse maior?", "por que o jacobiano tem esse tamanho?") antes da resposta.
- Intuição ANTES da conta, interpretação DEPOIS do resultado ("deu 0,99: menor que um, o centro de massa cai no buraco").
- Narração construída para a teoria e o entendimento, não reprodutora da tela.

## ESCLARECIMENTO DO KAIO (2026-11-15, 21:30) — vale sobre tudo acima
- NÃO é para encurtar a narração nem deixar a tela falando sozinha. O tempo de voz de cada âncora FICA (o mesmo de antes, ou mais). A animação da álgebra também não acelera: a conta aparece com calma, dá tempo de ver.
- O que sai é a LEITURA robótica dos números. O que entra no lugar é CONVERSA: o professor resolve a expressão enquanto fala com o aluno. Ex.: "agora vamos fazer o MMC, que aqui é o menor múltiplo que serve para todo mundo; subtrai um pelo outro; essa fração vocês já conhecem, é aquela de antes; olha como ela simplifica". Verbos de ação (vamos somar, passa para o mesmo denominador, corta o que repete, junta), lembrar o que o aluno já sabe, avisar o que vem, pequenos porquês, aplicação, humor leve.
- Nunca deixar a tela escrevendo em silêncio: toda escrita de degrau é acompanhada de fala, mas fala de professor, não de leitor.
- Meta de QA: a duração da narração NÃO cai em relação à versão anterior; a contagem de números lidos em sequência cai.

## Cadência e orçamento
Cadência continua 3 palavras/s. Duração por âncora NÃO diminui: o tempo antes usado para ler números passa a ser usado para conversar (ação, lembrete do que já sabem, porquê, exemplo, interpretação).

## Como aplicar
- Roteirizar: ao escrever cada âncora, marcar as linhas da coluna como [ensina] ou [mecânica]. [ensina] = lê e explica; [mecânica] = ação + resultado.
- QA da narração: contar quantos números a fala repete que já estão na tela; meta = só resultados e valores-chave. Revisar toda frase com 3 ou mais números seguidos.
- Gatilhos de tela continuam um por degrau (a tela escreve cada degrau; a fala só precisa estar no gatilho do degrau-chave).
- Texto de handoff ao Claude Code: "a coluna escreve todos os degraus; a voz fala a ação e o resultado nas contas mecânicas".

## Texto pronto para docs/decisoes.md (colar no Claude Code quando quiser registrar no Git)
"2026-11-15 · Narração: a tela mostra a álgebra passo a passo; a voz não lê o que já está escrito. Em conta mecânica a voz diz a ação e o resultado; em conceito, propriedade e interpretação a voz explica com exemplos e aplicações, em tom próximo ao espectador, mantendo o rigor. Vale para vídeos novos; os já entregues não são refeitos."
