# Handoff para o 5.1 (yt_0005) — convenção de corrente e dℓ (vinda do 5.2)

Escopo: só `videos_longos/yt_0005_magnetostatica_forca_lorentz/`. Sem commit, push, voz, master. Não tocar em `template/`.

## Convenção adotada no 5.2
| Objeto | Cor | Representação |
|---|---|---|
| Matéria condutora (fio, espira, lâmina, volume) | `STEEL #7A8696` | corpo neutro |
| Corrente `I`, `K`, `J`, `dI` | `GREEN` | traços alongados que correm no sentido convencional; **não** bolinhas (bolinha lê como carga) |
| Elemento de caminho `dℓ`, `dx`, `x̂`, `t̂`, `L` (vetores e rótulos) | **branco** | geometria, não corrente |
| Carga (λ, q, ρ) | azul `BLUE_L` | só quando o assunto é a carga |

## Estado atual do 5.1 (verificado no código)
- Já usa `STEEL` nos fios (`cena.py` linhas ~352, 2334–2342, 2539, 3364, 3420).
- Já representa a corrente como pulsos alongados (`dots()` ~linha 354: `Line(... color=GREEN, stroke_width=5)`, comprimento 0,32, com fade nas pontas). Não há `Dot` verde.
- `dℓ` e `dℓ⃗` (`"dl"`, `"dlv"`) **não estão em `BASECOL`** → saem brancos. `I`, `Kv`, `Jv`, `div` já são verdes (linha ~198).

Ou seja: **o 5.1 já segue a convenção; nada é obrigatório.**

## Opcional (só se quiser o mesmo acabamento do 5.2)
1. Nos pulsos de corrente (`dots()`, `flow()`, `flow9()`): arredondar as pontas (`cap_style=CapStyleType.ROUND`), subir `stroke_width` de 5 para ~7–8 e dar um contorno na cor do fundo (`.set_stroke(BACKGROUND_COLOR, width+3.5, background=True)`) para a corrente destacar do aço.
2. Cabeça mais clara que a cauda: desenhar dois traços sobrepostos (cauda com opacidade 0,5, cabeça — metade da frente — com opacidade 1).
3. Se algum desenho tiver seta/rótulo de `dℓ` ou `L` em verde, trocar para branco; `I`, `K`, `J` continuam verdes.

Conferir em preview 960×540 / 15 fps só as cenas que desenham corrente. Não re-renderizar o resto.
