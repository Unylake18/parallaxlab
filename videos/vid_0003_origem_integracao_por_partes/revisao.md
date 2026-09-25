# Revisão — vid_0003

O fechamento técnico final está em **Fechamento técnico — 2026-09-25**, ao
final deste arquivo. As seções anteriores registram as rodadas de preview; os
previews, logs e pastas de QA citados nelas foram removidos após o fechamento.

**Primeiro preview conferido em:** 2026-09-24. Entrega desta etapa: dois previews visuais,
com e sem coda. Ainda sujeitos à avaliação editorial antes de voz, legenda
e render final. Nenhuma publicação foi feita.

## Matemática e animação

- A cena começa com `(uv)' = u'v + uv'` e escreve `dx` nos três termos antes
  de apresentar diferenciais. A linha com `dx` foi conferida em frame inteiro
  a 8 s: sinais, fatores e espaçamento ficam legíveis em 540×960.
- `(uv)'dx → d(uv)` é um movimento de grupo. Em `u'v dx`, o `v` muda de
  posição para deixar `u'dx` contíguo; somente essa dupla vira `du`. No
  terceiro termo, `v'dx` vira `dv` enquanto `u` permanece.
- A igualdade é reorganizada para `u dv + v du = d(uv)`. Em seguida,
  `+v du` sobe, atravessa a igualdade e desce como `−v du`. Frames em 29,8,
  30,6, 31,4, 32,4 e 34 s mostram o termo em deslocamento, a troca de sinal
  e a relação final, sem troca abrupta da equação inteira.
- As integrais entram nos três termos. `∫d(uv)` vira `uv`; a fórmula final
  fica em caixa. A observação discreta sobre constantes impede que a
  igualdade entre primitivas seja interpretada como identidade de valores
  fixos sem constante de integração.
- A checagem usa `d/dx[uv − ∫v du] → u'v + uv' − vu' → uv'`.
  Os dois fatores iguais por comutatividade são riscados em ciano;
  o termo restante é o integrando de `u dv`.

## Coda

O plano `(u,v)`, o retângulo `U×V` e a curva crescente da origem ao canto
`(U,V)` aparecem sem fórmula para a curva. Os preenchimentos ciano e magenta
representam respectivamente `∫v du` e `∫u dv` ao longo do arco escolhido.
A síntese `UV = ∫v du + ∫u dv` fica abaixo do desenho. O título
“Uma interpretação geométrica”, a hipótese visual e a legenda
“Acumulações ao longo da curva desenhada” limitam a afirmação; a coda não
é apresentada como prova geral.

A curva é monotônica nas duas coordenadas. Uma verificação numérica
independente, por integração nos pontos amostrados do arco unitário, obteve
`∫v du ≈ 0,39725` e `∫u dv ≈ 0,60275`; a soma é `1,00000 = UV` nesse
desenho. Esta checagem só valida a geometria exibida.

## Render e QA

Comandos executados na raiz, usando o `uv` e Manim existentes:

```powershell
uv run python -m manim -r 540,960 --fps 15 videos/vid_0003_origem_integracao_por_partes/cena.py Integral003
uv run python -m manim -r 540,960 --fps 15 videos/vid_0003_origem_integracao_por_partes/cena.py Integral003SemCoda
```

| Preview local | Resolução | FPS nominal | Frames | Duração | Áudio |
| --- | --- | --- | ---: | ---: | --- |
| `renders/vid_0003_origem_integracao_por_partes_preview_com_coda.mp4` | 540×960 | 15 | 973 | 64,866 s | nenhum |
| `renders/vid_0003_origem_integracao_por_partes_preview_sem_coda.mp4` | 540×960 | 15 | 839 | 55,933 s | nenhum |

A duração adicional medida é **8,933 s**, dentro dos 7–10 s aprovados.
Os **839 frames compartilhados são pixel a pixel idênticos** entre as duas
versões: retirar a coda preserva integralmente derivação, verificação e
fechamento. O último estado da variante sem coda mostra a fórmula em caixa.
Em todos os frames, o pixel de conteúdo mais baixo medido foi `y=758` de
960; cerca de 200 px inferiores permanecem livres. A coda foi conferida
também em frame inteiro. Relatório local: `renders/vid_0003_qa/qa.json`;
contatos e frames amostrados ficam na mesma pasta, fora do Git por padrão.

O primeiro `uv run` restrito encontrou erro 183 no cache externo. Com acesso
adequado, Manim Community 0.21.0 respondeu e os dois renders terminaram.
Não houve alteração de ambiente, template nem dependências.

**Limite desta revisão:** a legibilidade foi avaliada em frames de 540×960;
leitura física em celular ainda não foi confirmada. Não há voz aprovada,
SRT sincronizado, capa nem exportação final nesta etapa. A próxima decisão
editorial é aceitar ou retirar a coda após assistir ao preview.

## Segunda rodada visual — 2026-09-24

O primeiro preview acima foi preservado. Os novos arquivos, também silenciosos,
estão em `renders/` com o sufixo `_preview_rodada2_com_coda.mp4` e
`_preview_rodada2_sem_coda.mp4`. A cena permanece em 540×960/15 fps e não
houve mudança no ambiente, no template, em voz ou em legendas.

| Versão da rodada 2 | Frames | Duração | Áudio |
| --- | ---: | ---: | --- |
| Com coda | 1.018 | 67,864 s | nenhum |
| Sem coda | 843 | 56,199 s | nenhum |

A diferença medida é **11,665 s**, dentro da meta aproximada de 9–12 s.
Os textos da cena continuam **textos-base visuais**, não narração nem SRT.
O título da pergunta sai após a abertura; guias transitórios orientam apenas
as passagens em que atuam. `dx`, `u dv`, `v du` e `uv'` nesses guias usam
MathTex. `du` e `dv` recebem destaque breve no destino, mantendo visíveis
seus fatores de origem. Durante a travessia de `+v du`, os demais termos
perdem contraste; o sinal muda para `−` antes da expressão se estabilizar.

A verificação agora começa com `d/dx(uv − ∫vu' dx)`, passa por
`u'v + uv' − vu'`, mostra brevemente `u'v − vu' = 0` e termina em `uv'`.
Na coda, primeiro aparece uma fatia ciano de altura `v` e largura `du`;
ela percorre o eixo horizontal enquanto a região acumula. Só depois surge
`∫₀ᵁ v du`. O mesmo processo ocorre em magenta com fatia de largura `u`
e espessura `dv`, seguida de `∫₀ⱽ u dv`. A caixa final contém
`UV = ∫₀ᵁ v du + ∫₀ⱽ u dv`, referente apenas ao caso da curva crescente
desenhada. A frase final afirma que as duas regiões completam o retângulo.

Foram inspecionados frames em **8 s** (`dx`), **15,5–17,5 s** (`u'dx → du`),
**22,5 s** (`v'dx → dv`), **29,8–32,5 s** (travessia e sinal), **37 e 41 s**
(integrais e fórmula), **44,8 e 49,5 s** (início da verificação e
cancelamento), **58,1 s** (fatia vertical), **59,7–60,4 s** (região ciano),
**61,1 s** (fatia horizontal), **62,8–63,7 s** (região magenta) e **67 s**
(identidade final). Quadros inteiros e contatos estão em
`renders/vid_0003_qa/rodada2/`. O último pixel de conteúdo detectado nas
amostras foi `y=782` de 960, deixando cerca de 178 px livres embaixo.

`Integral003SemCoda` foi renderizada novamente porque a cena principal
mudou. Ela termina com a síntese e a fórmula em caixa. Os renders independentes
têm pequenas diferenças de tempo durante algumas transformações; portanto,
os frames de índice igual **não são idênticos pixel a pixel** nesta rodada.
Quadros da sequência final em ambos os vídeos confirmam que a coda continua
removível sem retirar nenhum passo matemático. A sincronização precisa de
nova avaliação quando houver narração aprovada. A leitura física em celular
também permanece pendente. Não houve render final nem publicação.

## Ajuste pontual do guia de dx — 2026-09-24

O texto-base “Multiplicando a igualdade por dx” permanece visível após a
entrada dos três `dx` e só começa a sair em **9 s**. A troca para “Cada
derivada agora vira seu diferencial” usa saída e entrada curtas, sem
sobreposição de letras. Frames em **5,7; 6,5; 7,5; 8,5; 9,0; 9,5 e 10,0 s**
foram conferidos em `renders/vid_0003_qa/ajuste_dx/`. A derivação e a coda
não foram reestruturadas.

Os previews silenciosos desta correção são
`renders/vid_0003_origem_integracao_por_partes_preview_ajuste_dx_com_coda.mp4`
(**67,931 s**, 1.019 frames) e
`renders/vid_0003_origem_integracao_por_partes_preview_ajuste_dx_sem_coda.mp4`
(**56,199 s**, 843 frames), ambos em 540×960/15 fps. A diferença de duração
é **11,732 s**. Os previews anteriores permanecem disponíveis. Não houve
voz, SRT, exportação final, push ou publicação.

## Fechamento técnico — 2026-09-25

**Matemática aprovada e preservada:** regra do produto → `dx` nos três termos
→ `d(uv) = v du + u dv` → `+v du` atravessa a igualdade como `−v du` →
integração termo a termo → `∫u dv = uv − ∫v du`, com constante implícita.
Verificação: ponte `du = u'dx`, `dv = v'dx`; `d/dx(uv − ∫vu'dx)` →
`u'v + uv' − vu'`, cancelamento de `u'v` e `vu'`, resta `uv'`. A fórmula em
caixa permanece visível durante a checagem.

**Narração final:** `audio/narracao_final.wav` (PCM 16 bits, 44,1 kHz,
estéreo, 90,48 s), a fonte aprovada sem processamento, recorte, time-stretch
ou ajuste de volume; apenas renomeada de `narracao_original.wav`. A cena a
incorpora com `add_sound`; `Integral003SemCoda` permanece silenciosa.

**SRT final:** `legenda.srt`, 27 cues de 0,08 s a 84,74 s, até duas linhas,
notação escrita (`dx`, `du`, `dv`, `u'dx`, `v'dx`, `d(uv)`, `uv`, `uv'`,
`u dv`, `v du`, `(U,V)`, `U × V`), não a fonetização do áudio. O CTA falado
não tem cue; aparece no elemento visual final.

**Legendas coloridas:** `videos/montar_legendado.py --style solid
--color-module <cena.py>` lê `SUBTITLE_TERM_COLORS` da cena, sem tags no SRT:
termos de `v du` em ciano (`u'dx`, `du`, `v du`), de `u dv` em magenta
(`v'dx`, `dv`, `u dv`, `uv'`) e os demais em branco. O estilo `solid` usa
máscara opaca ampliada; os estilos `standard` e `piloto` mantêm a saída
anterior.

**Coda e CTA:** coda geométrica de 56,5 a 84,7 s (plano, curva crescente,
fatias vertical e horizontal, acumulações, `UV = ∫₀ᵁ v du + ∫₀ⱽ u dv`).
Depois, “Segue o Parallax Lab / @labparallax” até 90,0 s e fade final de
0,3 s com a watermark.

**Finais locais:**

| Arquivo | Tamanho | Vídeo | Frames | Duração vídeo | Áudio |
| --- | ---: | --- | ---: | ---: | --- |
| `renders/vid_0003_origem_integracao_por_partes_final_master_limpo.mp4` | 4.107.917 B | H.264 High, 1080×1920, 30 fps, yuv420p | 2.709 | 90,300 s | AAC 48 kHz estéreo, 90,517 s |
| `renders/vid_0003_origem_integracao_por_partes_final_legendado.mp4` | 4.283.390 B | H.264 High, 1080×1920, 30 fps, yuv420p | 2.709 | 90,300 s | AAC 48 kHz estéreo, 90,517 s |

O master é cópia byte a byte da saída do Manim de
`uv run python -m manim -r 1080,1920 --fps 30 videos/vid_0003_origem_integracao_por_partes/cena.py Integral003`.
O legendado usa o master como fonte; os pacotes de áudio dos dois arquivos
são idênticos.

**QA técnico:** os dois arquivos foram decodificados integralmente, sem erro:
2.709 frames de vídeo e 4.344.832 amostras de áudio cada. O áudio começa em
0 s com narração e termina em 90,50 s com a cauda silenciosa do WAV. Frames
amostrados em 1,5; 5,5; 10,8; 14,5; 18,5; 23,5; 29; 34; 41,5; 50; 53,5;
58,5; 68; 77; 83,5; 88 e 90,2 s cobrem abertura, `dx`, `u'dx → du`,
`v'dx → dv`, `v du → −v du`, integrais, fórmula, cancelamento, início da
coda, fatias vertical e horizontal, retângulo, CTA e último frame.
Resultado: legendas legíveis, cores corretas, sem clipping nem texto além
das bordas; faixa superior e watermark livres. No legendado, em 79,2–84,7 s,
a máscara opaca cobre a frase de tela “As duas regiões completam o retângulo
UV”, que a própria legenda repete; a caixa da identidade permanece visível.
O master não tem legenda queimada.

**Limpeza:** previews, logs e pastas temporárias de QA do vid_0003 em
`renders/`, e caches `Integral003*` em `media/videos/cena/`, foram removidos
após o QA.

## Capa — 2026-09-25

`capa_instagram.png`, 1080×1920 (9:16), RGB. Construída sobre a capa do
`vid_0002`, preservando fundo cósmico, símbolo, divisor, painel com contorno
luminoso, marca `PARALLAX LAB` e horizonte. Foram substituídos somente o
título, a linha de série e o conteúdo do painel:

- série pública: **POR TRÁS DA FÓRMULA · EP. 01**;
- headline: **DE ONDE VEM?** (branco);
- assunto: **INTEGRAÇÃO POR PARTES** (gradiente ciano → azul → violeta → magenta);
- painel: `(uv)′ = u′v + uv′`, seta para baixo, `∫ u dv = uv − ∫ v du`.

A família interna continua **teoria curta** e o ID interno continua
`vid_0003`; a série pública tem contador próprio. Conferidos: dimensões,
ortografia, matemática, ausência de “TEORIA CURTA”, “EP. 03” e “EXERCÍCIO
RESOLVIDO”, e leitura em miniatura de 270×480. Tipografia provisória do
sistema (Century Gothic e Times New Roman), como nas pendências de fonte de
`docs/identidade_visual.md`.

**Pendências:** leitura física em celular (vídeo e capa), backup externo dos
MP4s e publicação não realizados.
