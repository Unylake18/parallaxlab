# V7 — revisão do vídeo inteiro

Preview silencioso da unidade 0024, EP. 06. Mantidos Equador, 50 m, repouso inicial relativo à Terra, gravidade uniforme, ausência de arrasto e primeira ordem na rotação terrestre.

## Análise ponto a ponto

| Parte | Oportunidade encontrada | Melhoria implementada |
|---|---|---|
| Gancho | O ponto do chão precisava receber atenção no instante da pergunta | Pulso sincronizado com “AQUI?”, dentro do tempo existente |
| Globo | Tempo de observação podia ser redistribuído | Rotação real preservada, 0,8 s redistribuído para matemática e comparação |
| Globo → corte | Direção da observação estava implícita | Texto transitório “olhando ao longo do eixo terrestre” acompanha a projeção |
| Geometria | Diagrama relativamente pequeno | Raio visual ampliado de 2,35 para 2,55; rótulos dos raios seguem a geometria |
| Arcos → velocidade | A genealogia já funcionava após corrigir o ghost na V6 | Preservadas cópias físicas; rótulos R, R+h e r ancorados, sem duplicar fórmulas |
| Topo e chão | Ciano era usado também para velocidade da referência | Bola azul, malha neutra, rotação violeta e excesso/Coriolis ciano |
| Repouso relativo | Distinção Terra/espaço já estava explícita | Preservados movimento da Terra e os dois textos curtos |
| Momento angular | L_z podia ser confundido com o z vertical posterior | L_eixo e texto “sem torque → momento angular conservado” |
| Motivação da álgebra | Entrada na regra do produto tinha pouca orientação | Pergunta “de onde vem a aceleração relativa?” antecede a derivação |
| Contribuição da bola | Aproximação aparecia dentro de uma cadeia de igualdades | Nota “perto da soltura”; símbolo de aproximação preservado após usar vphi ≈ omega r |
| Contribuição da malha | “Mais lento” podia sugerir mudança de velocidade angular | Texto especifica menor velocidade linear perto do eixo |
| Comparação | Vetores no planeta tinham origens/direções diferentes | Novo comparador com caudas alinhadas no mesmo raio; delta-v ciano mostra o excesso |
| Fator 2 | Cores se perdiam nas strings únicas | Fusão mantém omega_T violeta e u azul; duas origens convergem ao resultado |
| Referencial | Contrarrotação e marcas externas já funcionavam | Preservada continuidade; comparador acompanha a dinâmica e sai antes da fórmula |
| Sinal negativo | Duas setas simultâneas enfraqueciam a explicação do sinal | Seta do produto vetorial transforma-se na seta oposta de Coriolis quando o sinal entra |
| Zoom local | Geometria já produzia os eixos | Preservada superfície → chão, raio → z, tangente → x, eixo → norte |
| Soltura e gravidade | Tracker e limites locais corretos; seta radial do corte tinha módulo fixo | Seta radial cresce com o tempo e é limitada; preservados velocidade relativa nula na soltura e vetores sem atravessar o chão |
| Exagero visual | Selo muito pequeno | Selo maior em área livre, com cor secundária |
| Primeira integral | Cancelamento era apenas marcado antes de uma transformação genérica | Glyph map elimina os dois fatores 2 e a barra, preservando os demais glifos |
| Segunda integral | Condições iniciais e cópias já existiam | Preservadas; vx azul e x ciano reforçam o significado |
| Altura e tempo | Valor pequeno e sobre a chave | h = 50 m ampliado e colocado acima da chave; números ainda entram nos slots do radical |
| Substituição numérica | Construção sequencial já funcionava | Preservadas entradas de omega, g e tf; deslocamento recebe ciano |
| Escala real | Aviso desaparecia enquanto a curva mudava | Selo transforma-se em “ESCALA REAL” durante S → 1 |
| Ampliação | Pontos ideal e real não tinham nomes | Rótulos “vertical” e “impacto”; valor em cm reorganizado no círculo |
| Fechamento | Hierarquia já estava adequada | Preservados fundo discreto, conclusão curta e resposta à pergunta inicial |

## Matemática e animação

MF-Tools é usado em dois pontos: fusão omega_T u + omega_T u → 2 omega_T u e cancelamento 2 omega_T g t²/2 → omega_T g t². Ambos usam strings únicas estabilizadas, asserts de topologia e mapas explícitos. TransformMatchingTex permanece o padrão; cópias físicas têm updaters congelados.

O comparador usa comprimentos proporcionais às velocidades do modelo de motivação: vbola ∝ Rt/r e vref ∝ r/Rt. Delta-v é a diferença, não uma terceira velocidade absoluta. A altura exagerada permanece sinalizada.

## Arquivos

- cena.py: V7.
- cena_v6_preservada.py: snapshot integral da V6.
- ficha.md: fase e descrição atualizadas.
- revisar_v7.py: checkpoints, amostras temporais, 19 frames e auditoria de decodificação.
- relatorio_v7.md: análise e entrega.
- media_v7/, qa_v7/, qa_v7_timestamps.json e logs: artefatos locais.

Nenhum arquivo global, dependência ou configuração do ambiente alterado.

## Render e QA

Comando: `uv run --no-sync python -m manim -r 540,960 --fps 15 videos/vid_0024_queda_coriolis_leste/cena.py QuedaCoriolis024`.

Ambiente validado, UV_CACHE_DIR local e MiKTeX existente. MP4: media_v7/videos/cena/960p15/QuedaCoriolis024.mp4.

- py_compile aprovado.
- Construção completa com manim -s aprovada, incluindo os dois glyph maps.
- Render entregue: 178,863 s (2min58,9s), 540×960, nominal 15 fps; 2.683 frames decodificados sem erro e com timestamps crescentes.
- Revisão temporal após o último render: 23 checkpoints e 90 amostras de transições inspecionadas; nenhum novo ghost ou sobreposição indevida identificado nesses quadros.
- Seleção final: 19 PNGs, painel 19_frames_01.jpg e pacote 19_frames_v7.zip.
- Ajustes de QA: rótulos dos raios ancorados, nota afastada da borda, altura retirada da chave, labels do inset ampliados e seta radial sincronizada; renders repetidos para conferir.
- Modelo do comparador verificado: r vphi constante, vbola crescente, vref decrescente e delta-v não negativo.
- Reprodução contínua: o controle do VLC continua retornando “foreground window did not report a process id”, inclusive após ativar a janela. A revisão foi por quadros extraídos; reprodução contínua não declarada aprovada.

## Limites preservados

O cálculo permanece de primeira ordem na rotação. O corte equatorial tem altura exagerada; o cálculo local usa 50 m. Teste do arsenal: nenhum sólido Blender, conforme briefing; geometria Manim 2D/2.5D.

Mantido 0,77 cm conforme briefing. O valor interno é cerca de 0,776 cm; o payoff é uma aproximação truncada, enquanto arredondar a duas casas daria 0,78 cm.

Sem voz, SRT, capa, master, commit, push ou publicação.
