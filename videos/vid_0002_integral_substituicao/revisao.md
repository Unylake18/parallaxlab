# Revisão final — vid_0002

## Solução e checagem

A substituição é u = x², du = 2x dx. Assim,
∫2x cos(x²) dx = ∫cos(u) du = sin(u) + C = sin(x²) + C.
Pela regra da cadeia, d/dx[sin(x²) + C] = cos(x²)·2x.
Diferenças centrais em 101 pontos de [−2, 2] tiveram erro máximo de
1,01×10⁻⁹. Na coda, F(x) = sin(x²) e F′(x) = 2x cos(x²); F cresce até
x = √(π/2), para no máximo e desce no intervalo restante mostrado.

## Áudio aprovado

- Fonte audio/narracao_final.wav: PCM estéreo 44,1 kHz/16 bits,
  71,023991 s, SHA-256
  ff352adf1f48dd84ce1ab1a06bb0ef1ec6794ae11e700265321a360ff94516e1.
- A primeira fala começa perto de 2,14 s no original; não há silêncio
  excessivo no fim. Pausas internas, incluindo uma de cerca de 2,22 s,
  são naturais e foram mantidas.
- preparar_audio.py remove 1,8 s do silêncio inicial e aplica +1,2 dB
  somente em 26,12–29,44 s, com fades de 140 ms. Recriou byte a byte
  audio/narracao_montagem.wav: 69,223991 s, SHA-256
  f7151cc60dcddc4e997d7e7be70e09e24d128ec4a48b6b66bda276b122747c8e.

## Exportação e QA final

O master limpo e o legendado em renders/ são H.264 vertical,
1080×1920/30 fps, 2.083 frames e cerca de 69,433 s. O AAC estéreo termina
em 69,224 s; primeira e última atividade foram medidas perto de 0,3 e
69,2 s. A trilha AAC é idêntica entre os dois MP4s, com hash de pacotes
397e6687daa1ec62e3411dfbc2fbb24796733399a69cbda35726e6da3ca2ac96.
O log do render final não continha warning, erro ou traceback. Na
compilação de fórmulas de uma revisão antiga, MiKTeX havia avisado sobre
atualizações não verificadas; nenhuma atualização foi feita.

legenda.srt tem 25 entradas sequenciais, sem sobreposição, de 0,270 a
69,100 s, em até duas linhas. No final legendado, a faixa fica
aproximadamente entre y = 1558 e 1720; não cobre fórmulas nem o CTA.
Foram inspecionados abertura, substituição, retorno, regra da cadeia
concreta, verificação, síntese, coda, CTA e último quadro.

Na transformação central, a estrutura ∫cos( ) aparece antes e as cópias
de u e du percorrem um trajeto curto sem cruzar as chaves. A verificação
usa somente a expressão concreta do exercício, sem f(g(x)). A coda é
complementar à solução: Integral002SemCoda a remove sem afetar a conta.
Os cursores, pontos e tangente usam a mesma abscissa. O QA anterior
conferiu 244 frames consecutivos da coda: 145 com F′>0, 17 com F′=0 e
82 com F′<0, sem inversões. Na versão final, o zero cobre a parada no
máximo e o sinal negativo só aparece na descida. O CTA entra em 68,07 s.

## Histórico condensado e limites

A primeira transformação teve sobreposição de chaves/rótulos; uma
revisão seguinte mandou u e du longe demais; a versão final preparou o
destino e encurtou os percursos. A fórmula geral f(g(x)) foi removida
para manter o foco na substituição. A sincronização foi refinada pela
fala aprovada, e a redação do SRT trocou formas fonéticas por du e dx.
Previews, capturas e logs anteriores foram substituídos pelos finais e
pelas medições acima.

A matemática, exportação, áudio, sincronização amostrada e legendas
passaram no QA técnico. A reprodução física em celular, a aprovação
final da capa, o backup externo dos MP4s e a publicação não foram
comprovados. A reconstrução com as fontes preservadas mantém conteúdo
e formato; nova codificação não garante bytes idênticos ao MP4 aprovado.
