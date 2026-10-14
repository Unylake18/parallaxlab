# V9 — ponte espacial e variáveis ligadas à figura

Rodada limitada à didática e representação visual do `vid_0024`, sobre a V8. Física, modelo equatorial de primeira ordem, torre, gancho, integrações, identidade visual, número público EP.06 e valor aprovado foram preservados. Nenhuma alteração em outra unidade, documentação global, template, assets ou dependências.

## Arquivos

- Alterados: `cena.py` e `ficha.md`.
- Criados: `cena_v8_preservada.py`, `alteracoes_v9.diff`, `revisar_v9.py`, este relatório, logs e artefatos locais V9.
- A V8 e seus renders/quadros continuam disponíveis. Classe Manim mantida: `QuedaCoriolis024`.

## Mudanças

1. **P no equador:** sua posição é calculada pela projeção da latitude zero. P tem marcador acima do preenchimento do globo e rótulo explícito; a torre ilustrativa nasce nesse mesmo ponto.
2. **Raios e leste:** `r_base` e `r_topo` partem da interseção do eixo terrestre com o plano equatorial. O segmento h é radial. Os dois vetores tangenciais azuis e suas expressões são construídos a partir desses objetos e do mesmo omega. Motivação qualitativa, sem derivação de Coriolis.
3. **Ponte espacial:** plano tangente e triedro oblíquo aparecem ainda sobre a Terra. O vetor angular global é copiado para a direção norte, paralela ao eixo. A projeção gira até a vertical radial ficar para cima, o leste à direita e o norte perpendicular à tela. Símbolos geométricos distinguem norte entrando e sul saindo; depois resta a pequena legenda local.
4. **Zoom:** equador → arco → chão; normal radial → eixo z; tangente leste → eixo x; norte projetado → símbolo entrando; torre radial e bola → torre local e bola. Nenhum sistema local desconectado aparece pronto.
5. **Grandezas antes da conta:** chave h nasce logo após o zoom; seta branca para baixo estabelece g; repouso relativo, condições iniciais e relógio aparecem na soltura. A bola e a seta azul se movem antes da expressão `v(t)≈−gt ẑ`.
6. **Coriolis da figura:** retirado o quadro-dicionário de símbolos. Omega e velocidade são copiados dos rótulos físicos para a fórmula. A substituição preserva g, t, y e z separados, passa pela expressão positiva `+2ωgt(ŷ×ẑ)` e somente depois por x̂, junto ao inset do triedro.
7. **Leste sincronizado:** x̂, rótulo LESTE e seta ciano começam na mesma chamada de animação; a seta não existe antes desse evento.
8. **Mesmo t:** posição vertical, deslocamento lateral, trajetória, relógio, velocidade vertical, aceleração lateral e velocidade horizontal acumulada consultam `t_tracker`. Pausas da explicação congelam simultaneamente esse estado. O tempo avança durante a sequência a_x → v_x → x, em vez de a bola atingir o chão antes das integrações.
9. **Distância x(t):** cota horizontal liga a vertical original à posição da bola e acompanha sua altura. Vetores permanecem pequenos; o azul horizontal surge na primeira integral e o ciano continua presente até perto do impacto.
10. **Valores e escala:** h, g e t da figura entram na conta do tempo; omega numérico vem da grandeza trazida da Terra. A ampliação horizontal é identificada e colapsa para escala real antes do payoff de 0,77 cm. Lupa e fechamento preservados.

## Transformações matemáticas

MF-Tools foi preservado no cancelamento explícito dos fatores 2 da primeira integral. Nas passagens vetoriais foi escolhido `TransformMatchingTex`, com tokens separados e estáveis para omega, g, t, ŷ e ẑ: o matching já preserva o percurso desejado. Não se adicionaram glyph maps frágeis, `auto_morph` ou índices de desenvolvimento. Cópias de termos físicos e substituições por slot foram mantidas nos valores numéricos.

## Validação desta rodada

- Diff V8 → V9 registrado e inspecionado; integrações e substituição numérica preservadas, com alterações de origem visual e momento de apresentação.
- `py_compile` da cena e do extrator localizado sem erros.
- Execução estática completa sem vídeo para conferir estados críticos; corrigidas incompatibilidades de objetos dinâmicos, ordem de desenho de P, rótulos próximos e símbolos sem glifo na fonte.
- Um único preview MP4 da variante atual em 540×960 / 15 fps.
- Inspeção localizada prevista: 21 estados críticos e quatro quadros das pontes/nascimento de leste. **Não foi feito QA completo nesta rodada**, conforme o briefing.

Comando do preview:

```powershell
$env:UV_CACHE_DIR = Join-Path $PWD '.uv-cache'
uv run --no-sync python -m manim -r 540,960 --fps 15 --progress_bar none videos/vid_0024_queda_coriolis_leste/cena.py QuedaCoriolis024
```

Preview: `media_v9/videos/cena/960p15/QuedaCoriolis024.mp4`.

## Limites preservados

Projeção oblíqua vetorial da mesma geometria 3D, sem sólido Blender ou novo modelo físico. Raios, altura na Terra e desvio horizontal são ampliados didaticamente. A variação do tempo pode pausar enquanto a álgebra é explicada; não há relógios independentes nem reinício escondido da queda. Mantido o payoff solicitado de 0,77 cm: o intermediário é 0,776 cm; arredondamento convencional a duas casas daria 0,78 cm, observação já registrada na V8.

Esta entrega é preview para revisão. Sem voz, SRT, capa, master, publicação, commit ou push.
