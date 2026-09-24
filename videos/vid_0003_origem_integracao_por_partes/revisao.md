# Revisão do primeiro preview — vid_0003

**Conferido em:** 2026-09-24. Entrega desta etapa: dois previews visuais,
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
