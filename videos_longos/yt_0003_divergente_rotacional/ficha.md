# yt_0003 — Divergente e rotacional do campo eletrostático

- id: `yt_0003`
- formato: `longo_horizontal`
- natureza: `derivacao_aplicada`
- macroassunto: `eletromagnetismo`
- módulo: Lei de Gauss / eletrostática
- tema: divergente e rotacional do campo eletrostático
- duração-alvo: aproximadamente 11:15
- status: preview visual silencioso V1.5 concluído para avaliação, 960×540 / 15 fps
- solido_3d: nenhum na V1.5; geometria em Manim conforme autorização explícita do handoff V1.5

## Rodada atual — V1.5

A V1.4 não foi aprovada. O handoff V1.5 substitui a direção visual anterior; física, narração e ordem conceitual V1.2 permanecem congeladas. Os registros V1.4 abaixo são históricos e não constituem aprovação da rodada atual.

Reconstrução: intervalo centrado antes do cubo; faces, normais e fluxos separados; interface geométrica compartilhada; matching sem dupla exposição de fórmulas; campos e sonda com movimento funcional; circulação em caminhos sucessivos com acumulador; patches orientados de Stokes e inferência local na mesma superfície; mapa progressivo e coda com B variável e equipotenciais.

Gates solicitados: A (0–70 s), B (70–155 s), C (155–245 s), D (270–395 s), E (395–590 s), F (590–675 s). O exemplo de 245–270 s recebe também uma verificação localizada K, pois fica fora das janelas A–F do handoff.

### Referência local conferida

- `yt_0001`: paleta em `cena.py`, construção do vetor área e produto escalar, folha visual final 03 (1:20–1:59).
- `yt_0002`: implementação local existente em `cena.py`, mesmo que a ficha antiga diga “sem implementação”; fórmulas ativas 50, secundárias 40, rótulos 30; parâmetros vivos, fonte azul, campo ciano e gaussiana violeta. Frames locais de 145, 185 e 540 s extraídos do MP4 existente.
- Uma representação dominante e uma operação por transformação. Rótulos separados da geometria, matemática ativa tipicamente 46–56 pontos e payoffs 74–76; nenhuma dependência global alterada.

### Verificações atuais

- `python -m py_compile videos_longos/yt_0003_divergente_rotacional/cena.py`: passou após a reconstrução.
- `renders/conferir_fisica_v1_5.py`: passou; integrais numéricas 0,379247489581 e 0,379247489364, contra 0,379247489754 analítico; distâncias mínimas dos caminhos à carga 1,62688 e 1,74929.
- Superfície de Stokes: x ≥ −5,35, carga em x = −6,2; margem horizontal 0,85. Cubo de teste: distância mínima do centro 1,74805, raio projetado máximo 0,48836; não alcança a singularidade.
- `QA_LAYOUT=1`: checagem auxiliar dos textos contra traços e safe area em estados estáveis; não substitui inspeção dos frames intermediários.
- Preview completo concluído; relatório da rodada abaixo. A conclusão técnica não representa aprovação editorial do usuário.

### Arsenal na V1.5

`divergencia_local` e `rotacional_roda_de_pas` foram avaliados na V1.4 (registro histórico abaixo). A V1.5 usa Manim na explicação principal: o cubo mantém P fixo e a roda acompanha Ω continuamente. O handoff autoriza retirar os assets quando prejudicam clareza ou controle. Nenhum sólido, parâmetro ou cache do arsenal foi modificado/preparado nesta rodada.

## Entrega da V1.5 — 13/10/2026

### Arquivos e artefatos

- Alterados nesta unidade: `cena.py` e `ficha.md`.
- Criados para a verificação desta rodada: `renders/inspecionar_v1_5.py`, `renders/conferir_fisica_v1_5.py` e `renders/empacotar_preview_v1_5.py`.
- Preview: `renders/videos/cena/540p15/preview_v1_5.mp4`.
- Imagens para avaliação: `renders/yt_0003_v1_5_19_imagens.zip`, contendo exatamente 19 PNGs, com quatro frames reais e timestamps por imagem (76 frames). PNGs também em `renders/qa_preview_v1_5/`.
- Diagnóstico visual adicional: 24 frames em seis pranchas, em `renders/qa_denso_v1_5/`.
- Comparação visual local: `renders/referencias_v1_5/comparacao_lado_a_lado.png`; usa preview local V2 de yt_0001 e MP4s locais de yt_0002. A folha final 03 de yt_0001 também foi consultada; não se afirma comparação com um MP4 final de yt_0001.
- Metadados e timestamps exatos: `renders/entrega_preview_v1_5.json`. Resultados: `renders/qa_layout_completo_v1_5.json` e `renders/qa_fisica_v1_5.json`. Log completo: `renders/render_completo_v1_5.log`.

### Comandos e resultados

`git status --short` foi executado antes das alterações e na conferência final. Alterações preexistentes em outros vídeos e no arsenal foram preservadas.

```powershell
python -m py_compile videos_longos/yt_0003_divergente_rotacional/cena.py
$env:UV_CACHE_DIR=(Join-Path (Get-Location) 'renders\uv_cache')
uv run --no-sync python videos_longos/yt_0003_divergente_rotacional/renders/conferir_fisica_v1_5.py
```

Ambas as verificações passaram. Os gates A–F e o exemplo K foram renderizados separadamente antes do completo, usando a seleção `TRECHO` na mesma cena; erros locais foram corrigidos e os trechos afetados verificados novamente.

Comando exato do preview completo:

```powershell
$env:UV_CACHE_DIR=(Join-Path (Get-Location) 'renders\uv_cache')
$env:TRECHO=''
$env:QA_LAYOUT='1'
uv run --no-sync python -m manim -r 960,540 --fps 15 --media_dir videos_longos/yt_0003_divergente_rotacional/renders -o preview_v1_5.mp4 videos_longos/yt_0003_divergente_rotacional/cena.py DivergenteRotacional
```

Resultado: saída 0, 553 animações, 674,985352 segundos (aproximadamente 11:15), 10.125 quadros, 960×540, 15 fps nominal, H.264/yuv420p, CRF 23, sem áudio, 13.534.494 bytes. Todos os quadros foram decodificados sem erro.

```powershell
uv run --no-sync python videos_longos/yt_0003_divergente_rotacional/renders/empacotar_preview_v1_5.py
uv run --no-sync python videos_longos/yt_0003_divergente_rotacional/renders/empacotar_preview_v1_5.py --imagens
```

Empacotamento passou, ZIP íntegro. Os cortes abaixo foram sincronizados com o arquivo completo por cópia dos pacotes, sem recompressão, e decodificados integralmente. As fronteiras são keyframes efetivos.

| Corte | Intervalo no completo (s) | Quadros |
|---|---:|---:|
| `trecho_A_v1_5.mp4` | 0–69,999349 | 1.050 |
| `trecho_B_v1_5.mp4` | 69,999349–155,064388 | 1.276 |
| `trecho_C_v1_5.mp4` | 155,064388–245,060807 | 1.350 |
| `exemplo_K_v1_5.mp4` | 245,060807–270,058854 | 375 |
| `trecho_D_v1_5.mp4` | 270,058854–395,058203 | 1.875 |
| `trecho_E_v1_5.mp4` | 395,058203–589,986328 | 2.924 |
| `trecho_F_v1_5.mp4` | 589,986328–674,985352 | 1.275 |

Todos ficam em `renders/videos/cena/540p15/`. SHA256 de `cena.py` correspondente ao render: `eca4b6eb0786245ed7c40ff9ee7a30baf085309e91444671cbae6e0be668c721`.

### Inspeção e correções

Foram inspecionadas manualmente as 19 pranchas finais (76 timestamps registrados no JSON), as seis pranchas de diagnóstico (11, 50, 77, 80, 88, 89, 95, 96, 108, 122, 135, 142, 160, 192, 210, 230, 330, 390, 450, 510, 540, 570, 630 e 660 s), a comparação de referências e frames intermediários locais das transições do cubo e de Stokes durante a iteração.

Pontos conferidos: intervalo simétrico e P fixo; normais opostas; mesma interface compartilhada; campo não nulo com divergente zero; ligação Gauss/teorema; campo kappa r; delta com origem estritamente no interior para integral 1; F1 uniforme e F2 anti-horário com rotacional +z; sonda geométrica; caminhos regulares com mesmo valor de integral; Stokes inteiro fora da singularidade; inferência com pequenas superfícies em posições/orientações diferentes; dois payoffs, síntese e coda legíveis; faixa inferior livre.

O verificador auxiliar examinou 75 estados estáveis e reportou zero problemas de layout. Isso complementa a inspeção amostral e não equivale a uma prova de ausência de colisões em todos os frames intermediários.

Correções durante a reconstrução: compatibilidade do matching com as partes reais de MathTex no Manim 0.21; preservação dos termos correspondentes durante a entrada dos novos; retirada da dupla exposição de fórmulas; trajetórias de rótulos por áreas livres; ajuste da malha F2 para não alcançar o texto inferior; redução da opacidade dos patches de fundo na inferência de Stokes; retirada do rodapé de conteúdo e ajuste dos tempos de leitura. As correções locais precederam o render completo entregue.

### Teste do arsenal — decisão V1.5

| Sólido | Uso nesta versão | Cache/custo/peso novos | Resultado |
|---|---|---|---|
| `divergencia_local` | Não integrado; cubo centrado e faces controlados em Manim | Nenhum cache preparado; custo/peso de sequência 3D novos: zero | Substituição autorizada pelo handoff V1.5; geometria e rótulos legíveis no preview 960×540 |
| `rotacional_roda_de_pas` | Não integrado; sonda geométrica animada em Manim, com Ω contínuo | Nenhum cache preparado; custo/peso de sequência 3D novos: zero | Substituição autorizada pelo handoff V1.5; repouso, aceleração e sentido +z conferidos |

Não se apresenta um novo teste de integração dos assets Blender nesta versão: os resultados da V1.4 permanecem no histórico. O arsenal e seus caches preexistentes foram preservados.

### Limites e encerramento

Preview técnico concluído para avaliação visual, sem pendências técnicas identificadas nos checks executados. Inspeção visual amostral, sem QA de fechamento final da unidade. A projeção dos cubos e patches é geométrica em Manim; não há novos renders Blender. Não foram produzidos voz, TTS, SRT, master, final, versão legendada ou render 1080p. Não houve alteração global, commit, push, branch, PR ou publicação. Rodada encerrada no preview.

## Histórico técnico — V1.4 não aprovada

## Especificação congelada

Física, narração, ordem conceitual e arquitetura didática: Narração + Storyboard V1.2, recebida no chat. A rodada V1.4 reconstrói exclusivamente a implementação visual conforme o handoff anexado em 12/10/2026. Sem voz, SRT, master, final 1080p ou publicação. Os previews V1.2/V1.3 anteriores foram preservados.

## Referências concretas adotadas

- `videos_longos/yt_0001_lei_gauss/cena.py`: paleta semântica de `E`, cargas, gaussianas, normais e área; `MathTex` com termos isolados; fonte oficial com oversampling e contexto Pango amplo; marca d'água oficial.
- `videos_longos/yt_0002_lei_gauss_casos_classicos/cena.py`: superfícies translúcidas, campo ciano com hierarquia de intensidade, setas com comprimento significativo, revelações graduais e correspondência entre objetos e termos algébricos.
- Implementação local: três planos discretos de fundo, aproximações por transformação dos objetos, anotações ancoradas, traçadores, memória compacta das contribuições x/y/z e continuidade entre curva, membrana e pequena superfície.

## Mapa semântico

| Elemento | Cor |
|---|---|
| Campo E e componentes | ciano `#35D9FF` |
| Cargas q, Q e densidade rho | azul claro `#7FB2FF` |
| Superfícies gaussianas, volume e divergente | violeta `#9C8CFF` |
| Fluxo e suas contribuições | lavanda `#D6CCFF` |
| Normal orientada | azul `#267BFF` |
| Rotacional e circulação | âmbar `#FFC24D` |
| B | magenta `#EA63FF` |
| Potencial V, somente na coda | âmbar; distinto do volume V |
| Operações neutras e campo genérico F | branco |

Textos: Space Grotesk oficial. Matemática: MathTex. Conteúdo crítico acima da faixa inferior, com fórmulas dimensionadas para 960×540.

## Transformações matemáticas

| Passagem | Recurso e motivo |
|---|---|
| Faces → fluxo em x | cópias geométricas das faces/setas para os termos; o sinal menos nasce da normal oposta |
| Diferença finita → derivada parcial | MF-Tools `TransformByGlyphMap`, mapa explícito dos seis glifos; preserva E e troca Delta por parcial |
| Contribuições x/y/z → divergente | memória compacta, cópia da soma e `TransformMatchingTex` com identidades isoladas |
| Gauss integral → local | cópias do mesmo fluxo, `TransformMatchingTex` e volume encolhendo; não transformar uma inferência em identidade algébrica falsa |
| kappa+kappa+kappa → 3kappa | MF-Tools, mapa explícito 5→2 glifos, contagens conferidas |
| rho → q delta³ | `TransformMatchingTex`, substituição identificável após rho=q delta³; MF não acrescentaria clareza à substituição |
| Stokes → resultado local | matching mantém o zero da circulação na integral; seleção, mudança de orientação e redução da superfície antecedem a revelação local |
| Faraday → eletrostática | `TransformMatchingTex`; B estacionário é mostrado antes do caso eletrostático |

Não há determinante-mnemônico do rotacional. Fades separam inferências conceituais de igualdades operacionais. Nenhuma transformação de PNG em glifos.

## Mapa temporal do preview

| Tempo aproximado | Bloco |
|---|---|
| 0:00–0:35 | Superfície gaussiana → ponto P → cubo |
| 0:35–1:10 | Gauss integral, carga envolvida → densidade |
| 1:10–2:35 | Sólido introdutório, cubo centrado, divergente e seus três estados |
| 2:35–3:25 | Faces internas cancelam; fronteira externa |
| 3:25–4:05 | Mesmo fluxo → Gauss diferencial |
| 4:05–4:30 | Campo kappa r; sonda deslocada nos três eixos |
| 4:30–5:45 | Carga pontual, volumes regulares e superfície encolhendo |
| 5:45–6:35 | Delta por integrais de volumes de teste |
| 6:35–7:00 | F1 uniforme versus F2 giratório |
| 7:00–7:45 | Roda como sonda geométrica de F; transição F→E |
| 7:45–8:35 | Caminhos distintos, acumulação e circulação fechada |
| 8:35–9:20 | Curva, membrana, orientação e Stokes |
| 9:20–9:55 | Qualquer pequena superfície regular → rotacional zero |
| 9:55–10:35 | Síntese progressiva; relações global/local |
| 10:35–11:15 | Faraday, caso eletrostático e porta para potencial |

## Checkpoints

Todos em `renders/videos/cena/540p15/` nesta unidade:

- A: `trecho_A_v1_4.mp4`, 155,063 s, 2.326 quadros.
- B: `trecho_B_v1_4.mp4`, 90,000 s, 1.350 quadros.
- C: `trecho_C_v1_4.mp4`, 194,997 s, 2.925 quadros.
- D: `trecho_D_v1_4.mp4`, 129,999 s, 1.950 quadros.

A/B/C/D foram renderizados e inspecionados antes do preview completo; C foi atualizado para corrigir o trajeto do cubo. Ao concluir, os quatro MP4 foram sincronizados com o preview completo por cópia dos pacotes H.264 entre keyframes, sem recompressão. Assim, os checkpoints entregues incluem também os últimos ajustes de contorno, opacidade, marca e cadência. Todos os quatro foram decodificados integralmente após o recorte. Os contatos em `renders/qa_trecho_*_v1_4/` registram as provas das iterações anteriores.

Intervalos efetivos no arquivo completo: A 0–155,063; B 155,063–245,063; C 270,063–465,060; D 465,060–595,060 segundos. A diferença de centésimos corresponde às fronteiras de quadros/keyframes; não há sincronização de áudio nesta rodada.

## Verificações e comandos

- `git status --short` antes das alterações: mudanças de outros vídeos/arsenal preservadas.
- `python -m py_compile videos_longos/yt_0003_divergente_rotacional/cena.py`: passou.
- Import localizado da cena: passou; fontes e MF-Tools disponíveis.
- Caches carregados com `render="nunca"`: a cena não modela nem altera o arsenal.
- PNGs dos dois sólidos: 960×540, alpha 0–255; diferenças RGB entre quadros 1/8 confirmam movimento. Estado parado não muda.
- Trajeto do cubo da carga pontual: distância mínima amostrada do centro à origem 1,624; raio conservador da projeção do cubo 0,488; folga superior a 1,13 unidade de cena. O segundo deslocamento permanece abaixo da carga, com separação vertical de 1,45.
- Stokes: fonte em x=-5,7; curva e membrana inteiras em x≥-4,15, separação horizontal mínima 1,55. Nenhuma superfície cruza a carga.

Ambiente de execução em PowerShell:

```powershell
$env:UV_CACHE_DIR=(Join-Path (Get-Location) 'renders\uv_cache')
$env:TRECHO=''
uv run --no-sync python -m manim -r 960,540 --fps 15 --media_dir videos_longos/yt_0003_divergente_rotacional/renders -o preview_v1_4.mp4 videos_longos/yt_0003_divergente_rotacional/cena.py DivergenteRotacional
```

Checkpoints: mesmo comando, com `$env:TRECHO='A'` (ou B/C/D) e `-o trecho_A_v1_4.mp4` (ou B/C/D).

## Resultado do preview completo

- Caminho: `renders/videos/cena/540p15/preview_v1_4.mp4`.
- Resultado: render concluído, 362 animações; 675,058984 s (aproximadamente 11:15), 10.126 quadros, 960×540, taxa nominal e de decodificação 15 fps, H.264/yuv420p, nenhum stream de áudio.
- Peso: 12.100.731 bytes (aproximadamente 11,54 MiB).
- A conferência de duração admite arredondamento de um quadro em torno de 675 s; uma expectativa inicial de exatamente 10.125 quadros foi substituída pela verificação da resolução, taxa nominal, ausência de áudio e tolerância temporal inferior a 0,1 s.
- 76 quadros reais extraídos; 19 imagens compostas, quatro quadros de 960×540 com timestamps por imagem: `renders/qa_preview_v1_4/yt_0003_v1_4_01.png` a `yt_0003_v1_4_19.png`.
- Pacote para avaliação: `renders/yt_0003_v1_4_19_imagens.zip`, somente as 19 imagens compostas.
- Quadros finais inspecionados incluem: 1:13, 1:20, 1:27, 1:35; 2:50, 2:58, 3:05, 3:18; 3:30, 3:38, 3:46, 3:58; 4:09, 4:16, 4:23, 4:28; 5:33, 5:42, 5:50, 6:00, 6:11, 6:22, 6:32; 6:40, 6:49, 6:56; 7:07, 7:19, 7:29; 7:53, 8:02; 8:52, 9:04, 9:13, 9:23, 9:33, 9:45, 9:52; 10:03, 10:14, 10:24, 10:33; 10:41, 10:49, 10:57, 11:06, 11:14.
- QA conferido: cubo centrado em P fixo; faces simétricas; campo não nulo com divergente zero; passagem explícita entre as duas integrais de Gauss; delta por ação em volumes, com origem interior para resultado 1; campos F1/F2 e sentido anti-horário corretos; trajetos e Stokes regulares; qualquer pequena superfície e orientação antes do segundo payoff; nenhuma equivalência entre irrotacional e linhas retas; coda curta, sem derivação de potencial. Fórmulas críticas legíveis a 960×540 e faixa inferior preservada.
- Os últimos ajustes foram reavaliados no arquivo completo. O cache de animações do Manim invalidou mais trechos por causa dos updaters; não houve novo render Blender. Essa limitação aumentou o tempo de iteração, sem alterar o preview entregue.

Extração das 19 imagens:

```powershell
uv run --no-sync python videos_longos/yt_0003_divergente_rotacional/renders/inspecionar_v1_4.py videos_longos/yt_0003_divergente_rotacional/renders/videos/cena/540p15/preview_v1_4.mp4 5,12,20,29,39,48,57,66,73,80,87,95,100,106,112,117,122,127,133,140,144,149,153,161,170,178,185,198,210,218,226,238,249,256,263,268,278,290,307,321,333,342,350,360,371,382,392,400,409,416,427,439.1,449.4,459,473,482,492,504,512,522,532,544,553,563,573,585,592,603,614,624,633,641,649,657,666,674 4
```

## Correções feitas durante a rodada

- Argumentos de índices/frações protegidos antes de isolar símbolos no MathTex; retirada de comandos de espaçamento que conflitavam com a letra q isolada.
- Abertura centrada na geometria, com integral abaixo da superfície.
- Memória x/y/z antes da soma; P fixo durante a construção diferencial.
- Cancelamentos de faces repetidos, fronteira destacada e fluxo comum explícito antes da igualdade entre integrais.
- Removida sobreposição entre divergente fora da origem e equações da delta.
- Anotações do cubo móvel e da superfície encolhendo agora seguem os objetos.
- Trajeto do cubo desviado da singularidade; um render completo foi interrompido para corrigir esse problema.
- Rótulo genérico F afastado das setas 3D; valores e orientação ficam em Manim.
- Caminhos já percorridos mudam de intensidade; barras acumulam a expressão coulombiana pelos extremos instantâneos.
- Sondas orientadas de Stokes passam a zeros explícitos antes da inferência; nenhuma aparência de giro não nulo permanece no resultado eletrostático.
- Contorno externo alinhado exatamente à envoltória das células; interior da membrana reduzido em opacidade durante o foco local; espaçamento final de divergente=3kappa corrigido.
- Ciclos 3D de 30 quadros reproduzidos em 2 s, aproveitando a cadência de 15 fps; rampa de fase da roda dura 2 s e termina com a mesma velocidade do ciclo seguinte.

## Teste do arsenal

### divergencia_local — encaixou com ajustes

- Resolução: 960×540, 32 amostras, 30 quadros animados.
- Cache: preparado anteriormente e reutilizado, `renders/arsenal3d/divergencia_local/390b9d6c7df3/`.
- Custo nesta rodada: sem novo render Blender; leitura de cache. Preparo anterior registrado: aproximadamente 20,2 s.
- Peso: 6.188.120 bytes, aproximadamente 5,90 MiB.
- Funcionou: campo e faces legíveis como apresentação espacial de fluxo, durante cerca de 4 s.
- Ciclo de 2 s: 30 estados do cache correspondem aos 15 quadros/s do preview.
- Limitação: o cubo do sólido move seu centro e possui tamanho fixo; não representa o limite diferencial. A construção precisa usa depois um cubo Manim 2.5D centrado em P fixo.

### rotacional_roda_de_pas — encaixou com ajustes

- Resolução: 960×540, 32 amostras; 1 quadro parado e 30 quadros giratórios.
- Caches: `374edf6cf81c/` (parado) e `4bc2a90d746a/` (giro), sob `renders/arsenal3d/rotacional_roda_de_pas/`.
- Custo nesta rodada: sem novo render Blender; leitura dos caches. Preparo giratório anterior registrado: aproximadamente 9,2 s.
- Peso: 178.083 bytes parado (0,17 MiB) + 5.652.970 bytes animado (5,39 MiB).
- Funcionou: pá ampliada, estado sem giro, rampa inicial por fase, giro anti-horário e anotação de 2 Omega z em Manim. Alpha preservado nos fades.
- Após a rampa, ciclo de 2 s com 30 quadros: cadência compatível com 15 fps, mantendo a rapidez explicitamente ilustrativa.
- Limitações: estado parado é um campo radial regularizado e irrotacional, não F1 uniforme; por isso é identificado como F genérico. A rapidez e os 30 estados de fase são ilustrativos, não uma medição de Omega. A troca de campos usa caches discretos, sem interpolação geométrica de campo. Nenhum sólido ou parâmetro do catálogo foi alterado.

## Escopo de arquivos e parada

- Fontes alteradas: `cena.py`, `ficha.md` desta unidade.
- Artefatos locais: checkpoints, preview, logs e imagens de inspeção; auxiliar `renders/inspecionar_v1_4.py` extrai quadros reais com PyAV/Pillow.
- Manim 2.5D: cubo diferencial, faces internas, volumes de teste, caminhos, Stokes e síntese. Blender somente nos dois sólidos aprovados.
- Nenhuma voz, SRT, master, final 1080p, publicação, branch, PR, commit ou push. Template, dependências e documentação global preservados.
- Condição de parada cumprida: preview completo e funcional, dois sólidos integrados, QA específico inspecionado e 19 imagens disponíveis. Nenhuma etapa posterior iniciada.
