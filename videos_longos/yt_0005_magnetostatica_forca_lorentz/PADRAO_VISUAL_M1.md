# Padrão visual e de construção da série Magnetostática (referência: yt_0005)

Para quem continua a série em outro PC (próximo: yt_0008 = 5.3 de Magnetostática). A fonte da verdade é o código:
`videos_longos/yt_0005_magnetostatica_forca_lorentz/cena.py` (helpers no topo, antes de `class Orbit`). Leia o topo do arquivo e os trechos citados abaixo; não precisa reler o resto.

Formato: `longo_horizontal`, 960×540 / 30 fps para preview (1080p só no final), `template/config_horizontal.py`, sem alterar `template/`.
Fonte: `screen_text` (Space Grotesk) para texto; matemática em `MathTex`. Nunca usar caracteres como `∥ ⊥ ρ λ σ ω ⊗ ⊙` dentro de `Text`/`txt()` (a fonte não tem, vira quadrado branco): usar `eq(r"\rho")` etc.

## Cores por grandeza (constantes no topo do `cena.py`)
| Grandeza | Cor |
|---|---|
| B (campo magnético) | magenta `MAG = #EA63FF` |
| E (campo elétrico), energia/trabalho/potência | ciano `PRIMARY_COLOR` |
| **corrente I, K, J** (setas, pulsos, fluxo, ∇·J) | **verde `GREEN = #3FE08B`** (o mesmo do vid_0009) |
| carga q, dq, ρ, λ, σ, Q | azul `BLUE = #267BFF` / azul-claro `BLUE_L = #7FB2FF` |
| velocidade v, v∥, v⊥, ω, T, t | violeta `VIOLET = #9C8CFF` |
| força (F, F_B, F_E, F_y) | azul-claro `FC = #5AA2FF` |
| geometria auxiliar, eixos, normais | branco/neutro |
| painéis e destaques | azul-escuro `PANEL = #0E2A52` com contorno `BLUE_L` (sem caixa branca sobre preto) |

Carga ≠ corrente: carga azul, corrente verde. Fios em azul-claro; a corrente (pulsos/setas verdes) corre por cima, sempre em movimento.
Operadores matemáticos podem ficar brancos; as grandezas levam a cor semântica (`BASECOL` + `cores_novas`).

## Disposição na tela (16:9, unidades do Manim)
- Cabeçalho "ELETROMAGNETISMO · MAGNETOSTÁTICA" no canto superior esquerdo e marca d'água no direito (já no `construct`).
- **Fenômeno à esquerda (~55–60%), álgebra à direita (coluna centrada em x≈3,9, largura útil ≤ 5,7)**. O desenho continua vivo (órbita girando, fluxo correndo) enquanto a equação aparece.
- Equação grande é exceção curta; depois devolve o foco ao fenômeno.
- Margens seguras: nada além de |x| ≈ 6,9 e |y| ≈ 3,5. Texto de apoio em `T_NOTE = 24` ou menor; texto na tela **não é transcrição da narração**: símbolo + 2–5 palavras.
- Resultado consolidado ganha um **título curto acima da caixa** (`nome("Título", "subtítulo", pos=...)`), em posição reservada, sem acumular legendas.

## Construção da matemática (o que tem de valer em todo trecho)
- Fórmula é transformação do fenômeno vivo, não slide substituindo slide. Um passo por vez; mostrar de onde vem cada termo (determinante por componentes, integral com limites, `+C`, etc.).
- Troca entre expressões: `RT(a, b)` = saída/entrada limpa (padrão). `RT(a, b, match=True)` = `TransformMatchingTex` só quando os tokens casam bem. `morph(...)` mantém os símbolos que sobrevivem (`ReplacementTransform` por token) e faz fade no resto. **Nunca** deformar glifos diferentes uns nos outros (fica amontoado). `TransformByGlyphMap` só onde melhorar muito a leitura.
- `eq(...)` já reduz fontes grandes (`fs()`) e limita a largura (`MAXW = 5.7`); não aumentar fontes para "ocupar espaço".
- Destaques: `box(m)` (painel azul-escuro) em vez de `SurroundingRectangle` branco; `panel(m)` para cards.
- Vetor cuja ponta precisa tocar um ponto exato: `vec(a, b, cor)` (a ponta termina exatamente em b).
- Rótulo que cruza linhas/arcos: `halo(m)`.
- `always_redraw` não faz fade: usar `ValueTracker` de opacidade.
- Em preview: não usar `\textcolor` (o template LaTeX do Manim não carrega xcolor); a cor vem dos tokens (`colors={i: COR}`).
- Objeto que sai de cena sai **por inteiro** (carga, vetores, trilha, rótulos); updaters não devem trazê-lo de volta.

## Física: dois estados, nunca interpolação de sinal
Sinal de q, mudança de caso etc.: troca **discreta** de todo o conjunto coerente (carga, trajetória, vetores, gráficos, fórmula), reiniciando relógio e condição inicial. Nunca animar um multiplicador de +1 a −1.
Conferir a física antes de renderizar: ver `renders/redesign/qa_fisica_rodada_final.py` (RK4 contra solução analítica, |v| constante, R, T, p, geometria do analisador).

## Processo de trabalho (acordado com o usuário)
1. Implementar e rodar `py_compile` + checagem de nomes.
2. Preview local só do trecho alterado: `SEG=<seção> uv run python -m manim -r 960,540 --fps 30 --media_dir <pasta> -o <nome> .../cena.py <Classe>`.
3. **Revisar o vídeo inteiro por folhas de quadros (1 a cada 1–2 s; sequências nos pontos com movimento e transição) antes do render final.** Juntar todos os ajustes numa só rodada. Só então fazer **um** render contínuo (`env -u SEG`), conferir integridade (decodificar tudo, tempos crescentes) e montar o ZIP: vídeo + `cena.py` idêntica ao render + relatório + folhas dos pontos corrigidos (não empacotar milhares de PNG).
4. Render consome 3–5 GB de RAM: um por vez; em falha por memória, tentar de novo.
5. Fases: preview visual → (aprovação) → voz/sync → legenda → master. Não avançar sem pedido.

## Seletores `SEG` do yt_0005 (referência de como segmentar a cena)
`seg("nome")` = `next_section`; `SEG=K` (aprofundamento analítico), `E` (B04), `F/F2` (B05), `G` (B06), `H` (B07), `I` (B08), `J` (B09), `pre` (abertura–M1-06), `R1..R4` (grupos). Reproduza esse padrão no vídeo novo.

## Referência visual
O MP4 de referência (14:44, 960×540/30) não vai para o Git (mídia pesada fica só no PC; ver `.gitignore`). Pegue-o pelo Drive/ZIP enviado ao GPT (`yt0005_rodada_final_para_gpt.zip`) ou re-renderize com a `cena.py` deste commit.

Relatórios: `RELATORIO_REDESIGN.md` (redesign R1–R4) e `RELATORIO_RODADA_FINAL.md` (rodada final, com limitações conhecidas).
