# vid_0014 — Roteiro (referência para a futura sincronização da voz)

Série: POR TRÁS DA FÓRMULA · EP. 05. Marcos de tempo nominais (preview silencioso); a voz ainda não existe.

## Narração definitiva

É a mesma barra. Mesma massa, mesmo comprimento. Aqui o eixo passa pelo centro. Agora ele vai para a ponta. Só o eixo mudou — mas o momento de inércia ficou quatro vezes maior. De onde veio esse fator quatro?

Pra entender, começa com um pequeno pedaço da barra. Num corpo rígido girando, todo mundo tem a mesma velocidade angular. Mas a velocidade linear depende da distância perpendicular até o eixo.

Quanto mais longe, mais rápido esse pedaço se move.

Se a distância dobra, a velocidade dobra. Só que a energia cinética depende do quadrado da velocidade. Então a contribuição desse pedacinho cresce com o quadrado da distância.

É por isso que, para massas iguais colocadas a uma, duas e três vezes certa distância, as contribuições escalam como um, quatro e nove.

Quando somamos todos os pedacinhos do corpo, aparece naturalmente esta integral: distância ao eixo ao quadrado, vezes massa.

Essa integral é o momento de inércia.

Agora vamos calcular um de verdade.

Para uma barra uniforme com o eixo passando pelo centro, cada pedacinho tem massa proporcional ao seu comprimento. Integrando do menos metade do comprimento até mais metade, encontramos:

momento de inércia pelo centro igual a um doze avos de massa vezes comprimento ao quadrado.

A integral está fazendo exatamente o que vimos: massa perto do eixo contribui pouco para o momento de inércia; massa longe contribui muito mais.

Agora vem a pergunta importante: preciso refazer toda essa integral quando o eixo muda?

Não.

Vamos deslocar o eixo uma distância (d). Um ponto que tinha coordenada (x) em relação ao centro passa a ter coordenada (x-d) em relação ao novo eixo.

Então basta colocar isso na própria definição do momento de inércia.

Quando expandimos o quadrado, aparecem três termos.

O primeiro já é o momento de inércia pelo centro.

O último vira massa total vezes (d) ao quadrado.

E o termo do meio parece atrapalhar tudo.

Só que a integral de (x) vezes massa é a massa total multiplicada pela posição do centro de massa.

E nós escolhemos o centro de massa justamente como (x=0).

Por isso esse termo zera.

Não é a simetria da barra que o teorema exige. É a escolha da origem no centro de massa.

E sobra:

momento de inércia no novo eixo igual ao momento de inércia pelo centro de massa, mais (Md^2).

Esse é o Teorema dos Eixos Paralelos.

Agora leva o eixo até a ponta. A distância é metade do comprimento.

Somando os dois termos, encontramos um terço de massa vezes comprimento ao quadrado.

No centro era um doze avos.

Na ponta, um terço.

Exatamente quatro vezes maior.

O (r^2) nasce da rotação.

O (Md^2) nasce de mudar o eixo.

A fórmula não precisava ser decorada: ela já estava escondida na própria definição.

Se curtiu entender de onde a fórmula vem, segue o Parallax Lab pra mais Física e Matemática assim.

## Storyboard por bloco (V5)

Marcos nominais do preview silencioso (a voz ainda não existe). A V5 é polimento de ritmo e escala: abertura em 15 s com um estado por vez (título → centro→ponta → `I_ponta = 4I_CM ?` → mapa das duas perguntas), hierarquia tipográfica normalizada, comparação final enxuta (sem repetir `1/3 ML²`), síntese sem barra e end card curto.

| # | Tempo (s) | Cena | Relação matemática | Objetivo didático |
| --- | --- | --- | --- | --- |
| 1 | 0–15 | Título "POR QUE O EIXO MUDA O MOMENTO DE INÉRCIA?"; mesma barra (M, L), CM `×`, eixo do centro à ponta ("centro → ponta"); `I_ponta = 4 I_CM ?`; mapa: 1. de onde vem `r_⊥²`? 2. por que mover o eixo adiciona `Md²`? | — | Dizer o assunto e a pergunta antes da derivação |
| 2 | 15–27 | Barra gira; um `dm` se afasta do eixo; cota `r_⊥`, seta `v` | `v = ωr_⊥` | `r_⊥` e `v` ligados |
| 3 | 27–39 | `dK = ½v²dm` → `½(ωr_⊥)²dm` → `½ω²r_⊥²dm` | `dK ∝ r_⊥²` | Origem do `r²` |
| 4 | 39–48 | `r, 2r, 3r`; `v, 2v, 3v`; `1×, 4×, 9×`; "mesmo dm • mesma ω" | `1 : 4 : 9` | Distância ×2 → energia ×4 |
| 5 | 48–65,5 | Barra em 6 → 12 → 24 → 48 pedaços; soma vira integral | `K = ½ω²Σr_i²Δm_i → ½ω²∫r_⊥²dm`; `I = ∫r_⊥²dm`; `K = ½Iω²` | Integral como limite da soma |
| 6 | 65,5–77,5 | Barra para; `r_⊥ = |x|` → `r_⊥² = x²`; `dm = λdx`; `λ = M/L`; `dm = (M/L)dx`; perfil `x²dm` | — | `r²` vira `x²`; massa ∝ comprimento |
| 7 | 77,5–90,5 | `I_CM` em estados completos (box só durante o resultado) | `I_CM = (1/12)ML²` | Integral real |
| 8 | 90,5–102,5 | CM fixo; eixo desliza por `d`; `x'` com sinal e `|x'|` | `x' = x − d` | Geometria |
| 9 | 102,5–121,5 | `∫(x')²dm` → `∫(x−d)²dm` → binômio completo → `∫(x²−2dx+d²)dm` → três integrais → "d é constante" → chaves `I_CM` e `M` → `I' = I_CM − 2d∫x dm + Md²` | expansão e linearidade | Origem dos termos |
| 10 | 121,5–135,5 | Perfil assinado `x·dm`; `∫x dm = Mx_CM = 0`; "origem escolhida no CM"; `−2d·0` | `x_CM = 0` | Por que o termo zera |
| 11 | 135,5–143 | Box | `I' = I_CM + Md²` | Teorema dos Eixos Paralelos |
| 12 | 143–154,5 | Eixo vai à ponta (`d = L/2`, rótulo abaixo da seta); conta | `1/12 + 1/4 → 1/12 + 3/12 → 4/12 = 1/3` | Resolver o exemplo |
| 13 | 154,5–162 | "cada bloco = 1/12 ML²"; `I_CM` com 1 bloco; `I_ponta` com 4 blocos | `I_ponta = 4 I_CM` | Fechar o gancho |
| 14 | 162–166,5 | Síntese limpa, sem barra | `r_⊥²` — a contribuição cresce com a distância ao quadrado; `Md²` — deslocar o eixo adiciona exatamente `Md²` | Mensagem final |
| 15 | 166,5–169 | Só o símbolo oficial e `@labparallax` | — | Assinatura |

Duração nominal do preview V5: ≈169 s. Textos de tela novos (título, "só o eixo mudou", mapa do vídeo, "cada bloco = 1/12 ML²") complementam a narração e podem ser ajustados quando a voz existir.
