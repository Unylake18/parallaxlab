# Handoff para o 5.3 — corrente em traços e dℓ em branco (convenção do 5.2)

Escopo: só a unidade do 5.3. Sem commit, push, voz, master. Não alterar `template/`, 5.1 nem 5.2.
O 5.3 foi montado a partir de `kit.py`/`base.py` do 5.2 (ver `PADRAO_VISUAL_E_CONSTRUCAO.md`); se a cópia local ainda for a antiga, aplicar o abaixo.

## Convenção
| Objeto | Cor | Representação |
|---|---|---|
| Matéria condutora (fio, espira, bobina, solenoide, toroide, lâmina) | `STEEL = "#7A8696"` | corpo neutro (nunca azul-claro) |
| Corrente `I`, `K`, `J`, `dI` | `GREEN` | **traços alongados** no sentido convencional; não bolinhas (bolinha lê como carga) |
| Elemento de caminho `dℓ`, `dx`, `x̂`, `t̂`, `L` (vetor, rótulo, arco destacado, ⊙/⊗ de dℓ) | **branco** | geometria, não corrente |
| Campo B | magenta | — |
| Força | azul atual | — |
| Painéis/bordas/construção auxiliar | `BLUE_L` | **manter** (não é matéria) |

Não fazer `replace all` de `BLUE_L`: decidir ocorrência por ocorrência (só o que é matéria condutora vira `STEEL`).

## 1. kit.py
```python
STEEL = "#7A8696"   # matéria condutora

# depois dos loops que preenchem TOKCOL:
for _t in (r"d\boldsymbol\ell", r"d\ell", r"\boldsymbol\ell", r"\ell", "dx", r"dx\,\hat x", r"\hat x",
           r"\mathbf L", "L", r"\hat{\mathbf t}"):
    TOKCOL[_t] = WHITE      # elementos de caminho: branco. I, K, J, dI continuam GREEN
```
(`tube()` deve ter `color=STEEL` como padrão; espiras/arcos/lâminas desenhados à mão: `color=STEEL`.)

## 2. base.py — trocar `flow()` por traços
Importar `CapStyleType` de `manim`. Substituir a função:
```python
def flow(self, paths, count=7, direction=1, color=GREEN, dash=0.30, width=8):
    """Marcas convencionais de corrente: traços alongados (cabeça mais clara que a cauda). Não são cargas."""
    g = VGroup()
    for path in paths:
        pts = np.array([path(t) for t in np.linspace(0, 1, 41)])
        length = float(np.linalg.norm(np.diff(pts, axis=0), axis=1).sum()) + 1e-6
        du = dash / 2 / length
        for k in range(count):
            tail = Line(LEFT, RIGHT, color=color, stroke_width=width, cap_style=CapStyleType.ROUND).set_opacity(0.5)
            head = Line(LEFT, RIGHT, color=color, stroke_width=width, cap_style=CapStyleType.ROUND)
            for ln in (tail, head):
                ln.set_stroke(BACKGROUND_COLOR, width + 3.5, background=True)
            mark = VGroup(tail, head).set_z_index(8)

            def move(m, p=path, phase=k / count, du=du):
                s = direction() if callable(direction) else direction
                u = (phase + s * self.clock.get_value()) % 1
                back = p(min(max(u - s * du, 0.0), 1.0))
                front = p(min(max(u + s * du, 0.0), 1.0))
                m[0].set_points_as_corners([back, front])
                m[1].set_points_as_corners([p(u), front])
            mark.add_updater(move)
            mark.update(0)
            g.add(mark)
    return g
```
Usar `set_points_as_corners` (e não `put_start_and_end_on`): este falha quando o traço chega a comprimento zero nas pontas do fio.
Os chamadores (`self.flow([...], count=N)`) não mudam. Se algum passava `radius=`, remover.

## 3. Desenhos a trocar para branco
Seta/rótulo de `dℓ`, arco destacado do elemento, o `L` (colchete e seta de comprimento), `t̂`, e símbolos ⊙/⊗ que representem `dℓ` saindo/entrando da tela. Ficam verdes: setas de `I`, `K`, `J`, os traços de corrente e o ponto-fonte.

## 4. Conferir (preview 960×540 / 15 fps, só as cenas afetadas)
- fio/matéria cinza-aço, sem azul residual forte nos corpos;
- traços verdes visíveis sobre o aço, em reta e em curva (espira/solenoide), sem sumir dentro do traço do condutor;
- `dℓ` e `L` brancos; `I`, `K`, `J` verdes; painéis azuis intactos;
- nenhum traço esticado atravessando o fio no fim do caminho.
