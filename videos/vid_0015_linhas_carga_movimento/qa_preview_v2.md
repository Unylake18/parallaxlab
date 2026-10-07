# QA — vid_0015, reconstrução visual V2

Rodada de 2026-10-06. Escopo: preview silencioso, sem avançar para voz ou final.
A V1 permanece preservada como referência histórica, sem aprovação visual.

## Arquivos da unidade

- `cena.py`: segunda implementação, classe `LinhasCarga015`.
- `ficha.md`: briefing e geometria horizontal registrados.
- `inspecionar_preview.py`: decoder, extração de estados e folhas de contato.
- `qa_preview.md`: este relatório.
- `cena_v1.py`, `qa_preview_v1.md`: cópias da implementação e relatório anteriores.
- `qa_estados_v2.json`: timestamps e 13 transformações com MF-Tools.
- `qa_tecnico_v2.json`: medidas do MP4 e associação de cada estado ao PNG.
- `frames_preview_v2/`: 37 estados, 10 frames de transição, 10 folhas de contato
  dos estados e três das transições.
- `render_preview_v2.log`: saída do render.
- `media/videos/cena/960p15/vid_0015_preview_v2_silencioso.mp4`: preview entregue.

Nenhum arquivo global nem arquivo de outra unidade foi alterado nesta rodada.
As alterações preexistentes do vid_0014 e os arquivos de outras unidades foram preservados.

## Reconstrução

As duas linhas agora são horizontais, com cargas em movimento para a direita.
O topo reproduz tag, fonte, margens e watermark de `vid_0014/build_stage`.
Gauss usa cilindro coaxial em perspectiva, E radial em vários pontos, normal lateral
paralela ao campo e normais axiais nas duas tampas, com ângulos de 90°.
O cilindro encurta até uma seção; a superfície preenchida dá lugar à curva
amperiana sem preenchimento. Curva de integração e campo tangente usam códigos distintos.
A regra da mão direita combina corrente/polegar, campo/dedos e enrolamento animado.
O marcador ⊗ fica separado da linha, com halo e guia até o ponto de avaliação.
O produto vetorial nasce dos elementos geométricos e exibe a orientação calculada.

O mesmo ValueTracker controla velocidade ilustrativa das cargas, ponto do gráfico,
valores numéricos, seta magnética, resultante e posições fantasma de afastamento.
A curva y=(v/c)² é revelada progressivamente. F_E é a referência constante;
F_B=F_E(v/c)² e F_liq=F_E[1−(v/c)²]. As posições fantasma são qualitativas:
não há massa, aceleração, tempo físico ou integração de dinâmica supostos.
A faixa y<−5,7 fica livre para legendas futuras.

## Matemática e MF-Tools

`TransformMatchingTex` permanece nas passagens com correspondência simples.
`TransformByGlyphMap` controla cancelamentos e reorganizações: ℓ em Gauss,
2πd nos campos e na igualdade das forças, isolar I²/λ², raiz e módulos,
identificar c, substituir |I|=|λ|v, cancelar |λ| e derivar F_B/F_E=v²/c².
Os mapas usam MathTex de string única com spans calculados e verificados;
nenhum índice ou debug aparece no vídeo. O uso seletivo evita perder os termos
sobreviventes nos cancelamentos. As 13 passagens estão registradas no JSON.

## Comandos de validação e render

```powershell
uv run --no-sync python -m py_compile videos/vid_0015_linhas_carga_movimento/cena.py
uv run --no-sync python -m manim -r 540,960 --fps 15 --media_dir videos/vid_0015_linhas_carga_movimento/media -o vid_0015_preview_v2_silencioso videos/vid_0015_linhas_carga_movimento/cena.py LinhasCarga015
uv run --no-sync python videos/vid_0015_linhas_carga_movimento/inspecionar_preview.py
```

O render teve saída redirecionada para `render_preview_v2.log`.
Os três comandos terminaram com código de saída 0 na versão entregue.
O runtime validado exigiu execução fora do sandbox; ambiente e dependências preservados.
As iterações renderizaram somente esta variante e reutilizaram o cache do Manim.

## Resultado técnico

540×960, H.264, 15 fps nominal, aproximadamente **198,46 s** (3 min 18,46 s),
**2.977 quadros**, nenhum stream de áudio. Os valores exatos estão no JSON técnico.
O decoder verifica resolução, ausência de áudio, todos os quadros e intervalos
compatíveis com 15 fps. A concatenação do Manim arredonda PTS nas fronteiras
em menos de 1 ms; por isso a taxa média do container difere minimamente de 15.

## Estados e QA físico

| Grupo inspecionado | Estados e tempos aproximados |
| --- | --- |
| Enunciado, repulsão e atração coexistindo | 01–03, 2,8–12,9 s |
| Cilindro, campo radial e lateral | 04–06, 18,9–25,7 s |
| Cada tampa perpendicular e fluxo zero individual | 07–08, 30,3–34,2 s |
| Fluxo lateral, cancelamento de ℓ e E(d) | 09–11, 41,6–52,2 s |
| Campo externo, trecho q=λℓ e F_E/ℓ | 12–13, 57,3–62,8 s |
| Seção, superfície → curva e B tangente | 14–16, 68,9–78,6 s |
| Regra da mão direita e B(d) | 17–18, 84,6–90,0 s |
| ⊗ separado, produto vetorial e F_B/ℓ | 19–21, 95,6–109,4 s |
| Forças opostas, fatores comuns e reorganização | 22–25, 113,9–126,5 s |
| Primeiro payoff: \|I\|/\|λ\|=c | 26, 133,9 s |
| Retorno ao movimento, \|I\|=\|λ\|v, segundo payoff v=c | 27–29, 140,6–152,6 s |
| Gráfico em 0; 0,2; 0,6; 0,85; 0,97; 0,995 | 30–35, 165,2–186,3 s |
| Partículas massivas e repulsão líquida final | 36–37, 189,4–196,0 s |

- E radial e para fora; E paralelo a dA na lateral.
- Nas duas tampas, E perpendicular ao vetor área axial: cada integral de fluxo
  é zero individualmente, sem depender de cancelamento entre tampas.
- Gauss usa superfície fechada. Ampère usa curva fechada e circulação de B.
- Corrente +x na linha superior: B=−z na linha inferior, marcado por ⊗.
- +x × (−z)=+y: atração magnética para cima, repulsão elétrica para baixo.
- Campos produzidos pela linha 1; forças avaliadas na linha 2, sem auto-força.
- Comparação das forças com origem comum e sentidos opostos.
- |I|/|λ|=c precede |I|=|λ|v. v=c surge após recuperar o movimento do enunciado.
- Texto de retorno aprovado preservado integralmente.
- Modelo ideal identificado durante a exploração; nota curta distingue o parâmetro
  de uma aceleração de elétrons num fio real.
- Tracker limitado a 0≤v/c≤0,995. F_B nunca ultrapassa F_E para v<c.
  O limite v=c é uma fronteira marcada, não um estado atravessado pelo tracker.
- Fechamento retorna a v/c=0,6: razão 0,36 e resultante repulsiva inequívoca.

Também foram extraídos dez quadros durante o colapso do cilindro, a transformação
superfície → curva, o enrolamento magnético, a reorganização algébrica e a variação
contínua do gráfico. A inspeção não se limita aos estados parados.
Os 37 estados e os dez quadros adicionais foram inspecionados visualmente;
os estados 12 e 28 foram novamente vistos em resolução integral após a correção.

## Correções e limites

Corrigidos durante a implementação: incompatibilidade de key_map com famílias
geométricas de tamanhos diferentes no Manim 0.21; sobreposição da equação B com o
produto vetorial; rótulos do gráfico próximos dos readouts e do limite; nota v<c
próxima dos ticks; ghosts atravessando nomes; ℓ encostando na seta E; relação
|I|=|λ|v encostando na caixa do primeiro payoff. Frames finais foram extraídos
do MP4, evitando capturas de câmera desatualizadas ao reutilizar animações em cache.

A movimentação relativa é deliberadamente qualitativa, conforme o briefing.
Não houve inconsistência física objetiva que exigisse reabrir decisões aprovadas.
Não ficou pendência técnica ou sobreposição identificada nos estados inspecionados.
Voz, SRT, master, legendado, capa, publicação e render final não foram iniciados.
