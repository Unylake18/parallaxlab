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
