# Padrão visual e de construção — Magnetostática (yt_0005 + yt_0006)

Leitura obrigatória para quem constrói o **5.3 (vid_0008 / magnetostática)** em outro computador. O código de referência é este
diretório: `kit.py`, `base.py`, `sec1.py`–`sec7.py`, `fisica.py`. Copie `kit.py` e `base.py` para a nova unidade e escreva as seções
em módulos `secN.py` (um mixin por bloco), como em `cena.py`. Não altere `template/`.

## 1. Cores (as mesmas do yt_0005)
| Grandeza | Cor | Constante |
|---|---|---|
| Campo B | magenta `#EA63FF` | `MAG` |
| Corrente (I, K, J, dℓ, t̂, dI) | verde `#3FE08B` | `GREEN` (nunca ciano) |
| Força | azul claro `#5AA2FF` | `FC` |
| Fios / densidade de carga | azul claro `#7FB2FF` | `BLUE_L` |
| Geometria (R, r, s, a, x, z, dw, da, dτ, dA⊥) | violeta `#9C8CFF` | `VIOLET` |
| Ângulos auxiliares (α, γ), componente perpendicular | ciano | `CYAN` |
| Cartões | `#0E2A52` translúcido, borda azul-clara | `PANEL` |
Cor por token: tabela `TOKCOL` em `kit.py`. Ao criar um símbolo novo, registre-o ali.

## 2. Tipografia e tamanhos
Texto na tela: Space Grotesk via `txt()/screen_text`. Matemática: `MathTex`. Título de seção 36, legenda 28 (`T_CAP`), nota 26,
fórmula principal `M_XL=54` / `M_L=48`, secundária `M_M=40`, `M_S=32`. Gregos e símbolos dentro de legenda: `$...$` (`rich()`).
Legenda ocupa só a faixa y≈-3,2; descrições de objetos ficam perto do objeto.

## 3. Disposição da tela (frame 16×9, safe |x|≤7,2, |y|≤3,8)
- Cabeçalho da série (canto sup. esq.) + marca (sup. dir.) + título da seção em y=3,3 (sai e entra em sequência, sem morph).
- **Layouts** (`LAYOUTS`, `relayout()`): `split` (desenho à esquerda, cartões à direita), `geo` (geometria dominante, cartões pequenos
  à direita), `alg` (álgebra dominante: cartões mais largos, desenho reduzido à esquerda). Use `geo` ao construir triângulos/vetores
  e `alg` quando a operação é algébrica.
- **Cartões** (`HERO` = equação ativa, `AUX` = apoio/definição): altura proporcional à expressão (`_need_h`), vazios saem (`drop`).
  Unidades e notas curtas podem ficar sem caixa.
- Corrente sempre em movimento (relógio `clock` + `flow()`), mesmo durante a álgebra; o elemento selecionado pode ficar fixo.

## 4. Construção de equações (MF-Tools com proveniência)
Regra central: **nenhum termo surge do nada**.
1. Equação = `E(tex, *tokens, size=, colors=)` (MathTex único com tokens isolados). Evite tokens de uma letra que apareçam dentro de
   comandos TeX (`a` em `\hat`, `x`, `s` em `\cos`). Prefira tokens compostos (`a\,dx`, `\frac{x}{a}`).
2. `self.show(nova, *pares, slot="H"|"A", src={(token,occ): rótulo_do_desenho}, auto=, structure=)`:
   - com equação anterior → `TransformByGlyphMap` (`gmap`); pares `(tokA, tokB[,occA,occB])`, `(tokA, None)` remove;
   - `src` → o termo voa de uma **cópia congelada** do rótulo do desenho (ou de glifos de outra equação); os glifos de destino ficam
     reservados;
   - **um proprietário por glifo de destino** (erro explícito se repetir). Fusões (R·R→R², s²·s→s³): primeiro mostre o produto
     (`R\cdot R`), só depois transforme (`R^2`), removendo o segundo fator.
   - sem termos em comum → fade simples (nunca deixe o MF-Tools mostrar índices de depuração).
3. Antes de substituir, destaque a parcela: `self.hl(token)`. Separe substituição, agrupamento e simplificação em passos.
4. Nunca mapear grandezas diferentes entre si (`sinθ`→`R̂`, `R²`→`s²`). Se a grandeza muda, mostre a definição no cartão auxiliar e traga
   o termo de lá.
5. `structure=False` em passos densos para não parear glifos de estrutura por assinatura.

## 5. Desenho (2.5D e 2D)
- Projeção `W(p)` com `ox, oy, gs, beta, tau` (`ValueTracker`); `vec()`, `tube()` (fio com brilho), `out_symbol()` (⊙/⊗ só em vista
  frontal; em vista oblíqua use a seta projetada). Objetos que dependem da vista precisam ser `always_redraw`/`cached`, senão ficam
  para trás ao mudar `view_to()`.
- Rótulos de diagrama: `lab()` (halo), com `add_updater` quando o objeto se move; eles são as **origens** dos termos das equações.
- Física em `fisica.py` (np.cross): a animação lê estados, não desenha por tentativa.

## 6. Notas na tela
Nomeie a operação ("Reescreva x em função de α", "Use s²=R²+z² no denominador"); não repita o que já está visível; saída e entrada
em sequência (`caption()`); retire a nota antiga antes de mudar o estado (`delcap()`).

## 7. Render e armadilhas (Windows, 16 GB)
- Preview 960×540 / 15 fps, por trechos: `SEG=<seção,...>` + `_grupo.sh NOME SEÇÕES` (um processo por vez; copie `Tex/` de uma rodada de
  fumaça para acelerar), junção com `juntar.py` (recodifica H.264 CRF 16). **Render completo numa só passada estoura a memória.**
- Rodada de fumaça sem quadros: `SEG=nenhuma` — pega erros de token/mapa em minutos.
- `DecimalNumber` em grupos: o cartão precisa remover os filhos (já tratado em `drop()`).
- Seções puladas por `SEG` ainda executam o código: objetos criados nelas persistem; comece cada seção com `clear()`.
- Em scripts de edição, cuidado com `\f`, `\t`, `\r` em strings Python (use `chr(92)` ou a ferramenta de edição).
- **Nunca** `taskkill /IM python.exe`: pode derrubar render de outro vídeo.
- Sem voz/SRT/master nesta fase; relatório de entrega e zip para avaliação conforme `AGENTS.md`.

## 8. Checklist para o 5.3
1. Ler `AGENTS.md`, `docs/estado_atual.md` (só o necessário), a `ficha.md` do vídeo e este arquivo.
2. Definir os estados físicos em `fisica.py` e conferir com um QA numérico.
3. Para cada seção: desenho primeiro, rótulos-origem, equação construída com `src`, nota curta, estado limpo para leitura.
4. Layout por operação (`geo` / `split` / `alg`); cartões proporcionais; nada vazio.
5. Fumaça (`SEG=nenhuma`) → trechos sentinela → preview completo por trechos → folhas de contato e zip para avaliação.
