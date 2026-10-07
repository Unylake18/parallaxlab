# Arsenal de sólidos 3D (Blender)

> Arquivo **gerado** por `gerar_catalogo.py` a partir de `solidos/*.json`. Não edite à mão: edite a ficha e regere.

Cada sólido tem uma ficha com "usar quando / não usar quando". Consulte o índice, abra a ficha do que parecer
servir e confira os critérios antes de decidir. Status: `planejado` (só ideia), `estudo` (funciona, aparência
não aprovada), `aprovado` (pode entrar em vídeo).

| id | Nome | Status | Áreas |
|---|---|---|---|
| `amperiano_circular` | Contorno amperiano circular | aprovado | eletromagnetismo/lei_de_ampere |
| `amperiano_retangular` | Contorno amperiano retangular | aprovado | eletromagnetismo/lei_de_ampere |
| `anel_carregado` | Anel carregado (aro) | aprovado | eletromagnetismo/campo_eletrico, mecanica/momento_de_inercia |
| `anteparo_fenda_dupla` | Anteparo de fenda dupla | aprovado | otica/interferencia, otica/difracao |
| `aro_rolando` | Aro rolando sem deslizar | aprovado | mecanica/rolamento, mecanica/momento_de_inercia |
| `caixa_gas_cinetica` | Gás ideal em recipiente com êmbolo (teoria cinética) | aprovado | termodinamica/teoria_cinetica, termodinamica/processos_em_gases |
| `campo_vetorial` | Campo vetorial (setas) | aprovado | calculo/campos_vetoriais, eletromagnetismo/campo_eletrico |
| `capacitor_esferico` | Capacitor esférico (esferas concêntricas, em corte) | aprovado | eletromagnetismo/condutores_e_capacitores |
| `capacitor_placas_paralelas` | Capacitor de placas paralelas | aprovado | eletromagnetismo/condutores_e_capacitores |
| `casca_cilindrica_oca` | Casca cilíndrica oca | aprovado | eletromagnetismo/lei_de_gauss, eletromagnetismo/campo_eletrico |
| `casca_esferica_oca` | Casca esférica oca (com corte em octante) | aprovado | eletromagnetismo/lei_de_gauss, eletromagnetismo/campo_eletrico |
| `cilindro_coaxial` | Cilindro coaxial (condutor maciço + casca externa, em corte) | aprovado | eletromagnetismo/lei_de_gauss, eletromagnetismo/campo_eletrico |
| `cilindro_macico_isolante` | Cilindro maciço isolante com cargas no volume | aprovado | eletromagnetismo/lei_de_gauss, eletromagnetismo/campo_eletrico |
| `cilindro_rolando` | Cilindro rolando sem deslizar | aprovado | mecanica/rolamento, mecanica/momento_de_inercia |
| `colisao_1d` | Colisão unidimensional entre dois blocos | estudo | mecanica/colisoes |
| `disco_carregado` | Disco carregado | aprovado | eletromagnetismo/campo_eletrico, mecanica/momento_de_inercia |
| `esfera_macica_isolante` | Esfera maciça isolante com cargas no volume | aprovado | eletromagnetismo/lei_de_gauss, eletromagnetismo/campo_eletrico |
| `esfera_rolando` | Esfera rolando sem deslizar | aprovado | mecanica/rolamento, mecanica/momento_de_inercia |
| `fio_infinito` | Fio infinito (retilíneo) | aprovado | eletromagnetismo/lei_de_ampere |
| `gaussiana_caixa` | Superfície gaussiana em caixa (pillbox) | aprovado | eletromagnetismo/lei_de_gauss |
| `gaussiana_cilindrica` | Superfície gaussiana cilíndrica (fechada) | aprovado | eletromagnetismo/lei_de_gauss |
| `gaussiana_esferica` | Superfície gaussiana esférica | aprovado | eletromagnetismo/lei_de_gauss |
| `gradiente_colina` | Gradiente numa colina (curvas de nível) | aprovado | calculo/gradiente, calculo/funcoes_de_varias_variaveis |
| `haste_carregada` | Haste carregada | aprovado | eletromagnetismo/campo_eletrico, mecanica/momento_de_inercia |
| `lente_delgada` | Lente delgada (biconvexa ou biconcava) | aprovado | otica/otica_geometrica |
| `massa_mola` | Sistema massa-mola horizontal (MHS) | estudo | fisica2/mhs |
| `onda_corda` | Onda numa corda (progressiva e estacionária) | estudo | fisica2/ondas_mecanicas, fisica2/ondas_estacionarias |
| `ondas_duas_fontes` | Ondas na superfície com duas fontes (interferência) | estudo | fisica2/superposicao_e_interferencia, otica/interferencia |
| `orbita_kepleriana` | Órbita kepleriana com setores de áreas iguais | estudo | mecanica/gravitacao |
| `pendulo_simples` | Pêndulo simples (pequenas oscilações) | estudo | fisica2/mhs |
| `placa_infinita_carregada` | Placa infinita carregada (plano com cargas na superfície) | aprovado | eletromagnetismo/lei_de_gauss, eletromagnetismo/campo_eletrico |
| `poco_gravitacional` | Poço gravitacional (potencial) | aprovado | mecanica/gravitacao |
| `prisma_triangular` | Prisma triangular | aprovado | otica/otica_geometrica |
| `solenoide_corrente` | Solenoide (hélice de fio) | aprovado | eletromagnetismo/lei_de_ampere |
| `solido_revolucao_arruela` | Sólido de revolução: método das arruelas | aprovado | calculo/volumes_de_revolucao |
| `solido_revolucao_cascas` | Sólido de revolução: método das cascas | aprovado | calculo/volumes_de_revolucao |
| `solido_revolucao_disco` | Sólido de revolução: método dos discos | aprovado | calculo/volumes_de_revolucao |
| `superficie_parametrizada` | Superfície parametrizada com remendo dS | aprovado | calculo/superficies_parametrizadas, calculo/integrais_de_superficie |
| `teorema_stokes` | Teorema de Stokes (hemisfério e contorno) | aprovado | calculo/stokes, eletromagnetismo/lei_de_ampere |
| `toroide_corrente` | Toroide (fio enrolado em anel) | aprovado | eletromagnetismo/lei_de_ampere |
| `tubo_escoamento` | Tubo com estrangulamento (continuidade) | aprovado | fluidos/fluidos_em_movimento |

## Padrão visual

Fonte única: `estilo.json`. Identidade: docs/identidade_visual.md. Gramática visual da série Lei de Gauss: constantes de cor em videos_longos/yt_0001_lei_gauss/cena.py e yt_0002_lei_gauss_casos_classicos/cena.py (o 3D segue o 2D, não o contrário).

| Cor | Hex | Papel |
|---|---|---|
| `fundo` | `#050816` | fundo da cena (muito escuro, bastante espaço negativo) |
| `texto_neutro` | `#F5F7FF` | matemática neutra; luz principal |
| `campo_eletrico` | `#35D9FF` | E⃗ e linhas de campo. RESERVADA ao campo: nunca em fontes, cargas ou superfícies |
| `fonte_fisica` | `#267BFF` | distribuição física: preenchimento do corpo, n̂ |
| `fonte_contorno` | `#7FB2FF` | contorno/aro da distribuição física, cargas próximas, R, Q; luz de contorno |
| `gaussiana` | `#9C8CFF` | superfície gaussiana, contorno amperiano e r: construção matemática, tracejada ou translúcida, nunca sólida |
| `area_vetor` | `#745CFF` | vetor área d⃗A e seleção matemática translúcida |
| `apoio_magenta` | `#EA63FF` | apoio pontual de identidade; sem uso 3D definido |
| `fonte_escura` | `#0B2A7A` | DERIVADA de fonte_fisica, escurecida à mão: interior de cascas (profundidade) |

**Regras**
- Ciano é só do campo elétrico: cargas e fontes são azul (#267BFF preenchimento, #7FB2FF contorno).
- Superfície gaussiana é violeta #9C8CFF, tracejada ou translúcida; nunca preenchimento sólido (não pode esconder a fonte).
- Sem bloom e sem estética gamer: a emissão máxima do arsenal é 2,2 (borda do vidro); nenhum sólido compete com texto e equações.
- Fundo #050816 e view transform Standard: as cores renderizadas têm de bater com a paleta do 2D.
- Legibilidade antes de efeito: ao desenhar um sólido novo, a distinção entre sólidos vizinhos (ex.: casca x maciço) deve valer sem rótulo.
- Nenhum hexadecimal ou parâmetro de material solto no código: tudo vem deste arquivo (gerar_catalogo.py recusa literais).

**Render:** Eevee, 64 amostras, view transform Standard; preview
960×540 a 15 fps; final
1920×1080 a 30 fps.

## Sólidos

### `amperiano_circular` — Contorno amperiano circular

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Círculo violeta (#9C8CFF), tracejado por padrão, no plano YZ, em torno do eixo X. Por padrão envolve um fio infinito de referência.

![Contorno amperiano circular](previews/amperiano_circular.png)

**Como se lê:** Círculo tracejado violeta em torno do fio azul. Tracejado = construção; contínuo (`continua=1`) = circulação calculada.

**Usar quando**
- campo B de um fio infinito (circulação em torno do fio, B tangente ao círculo)
- campo B dentro/fora de um toroide (círculo concêntrico)
- delimitar regiões por raio (dentro/fora do condutor)

**Não usar quando**
- o contorno atravessa a parede de um solenoide (use amperiano_retangular)
- superfície fechada de fluxo (use as gaussianas)

**Limitações**
- construção matemática (violeta, tracejada ou contínua), nunca preenchimento sólido: as faces opcionais são vidro violeta muito translúcido
- com_fonte=1 desenha uma fonte de referência só para contexto e teste de leitura; em vídeo use com_fonte=0 e componha com a fonte da cena
- o contorno é uma curva fechada (sem preenchimento); o sentido de percurso não é indicado: usar seta/rótulo no Manim

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `raio` | 1.4 | u | raio do círculo |
| `continua` | 0 | 0/1 | 0 = tracejado (construção); 1 = contínuo (circulação) |
| `faces` | 0 | 0/1 | 1 = disco de vidro violeta translúcido dentro do contorno |
| `com_fonte` | 1 | 0/1 | 1 = desenha um fio infinito de referência |
| `comprimento_fonte` | 10.0 | u | comprimento do fio de referência |
| `raio_fonte` | 0.06 | u | raio do fio de referência |

**Integração:** `png_seq_alpha` · custo 0.71 s/frame (1080p, Eevee)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- amperiano_circular --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("amperiano_circular").mobject(altura=5)   # estático: um quadro PNG com alpha
```

Ficha: `solidos/amperiano_circular.json`

### `amperiano_retangular` — Contorno amperiano retangular

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Retângulo violeta (#9C8CFF), tracejado por padrão, no plano XY (contém o eixo X): lados `comprimento` (em X) e `altura` (em Y), centrado na parede do solenoide de referência.

![Contorno amperiano retangular](previews/amperiano_retangular.png)

**Como se lê:** Retângulo tracejado violeta atravessando a parede do solenoide: metade dentro, metade fora. Lê-se como 'só o lado de dentro contribui'.

**Usar quando**
- campo B no interior de um solenoide longo (retângulo amperiano atravessando a parede)
- mostrar a corrente envolvida (n·l·I) pelos fios que o retângulo atravessa
- mostrar que os lados transversais e o lado de fora não contribuem

**Não usar quando**
- fio ou toroide (use amperiano_circular)
- contorno que deve ficar inteiramente fora do solenoide

**Limitações**
- construção matemática (violeta, tracejada ou contínua), nunca preenchimento sólido: as faces opcionais são vidro violeta muito translúcido
- com_fonte=1 desenha uma fonte de referência só para contexto e teste de leitura; em vídeo use com_fonte=0 e componha com a fonte da cena
- plano fixo XY e centrado em y = raio da fonte: outro posicionamento exige alterar `centro_y` no código
- o sentido de percurso não é indicado: usar seta/rótulo no Manim

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `comprimento` | 2.4 | u | lado do retângulo ao longo de X |
| `altura` | 1.8 | u | lado do retângulo ao longo de Y |
| `continua` | 0 | 0/1 | 0 = tracejado; 1 = contínuo |
| `faces` | 0 | 0/1 | 1 = face de vidro violeta translúcido |
| `com_fonte` | 1 | 0/1 | 1 = desenha um solenoide de referência |
| `raio_fonte` | 1.0 | u | raio do solenoide de referência (o retângulo é centrado na parede, em y = raio) |
| `comprimento_fonte` | 4.0 | u | comprimento do solenoide de referência |
| `n_espiras_fonte` | 12 | n | número de espiras do solenoide de referência |

**Integração:** `png_seq_alpha` · custo 0.45 s/frame (1080p, Eevee)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- amperiano_retangular --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("amperiano_retangular").mobject(altura=5)   # estático: um quadro PNG com alpha
```

Ficha: `solidos/amperiano_retangular.json`

### `anel_carregado` — Anel carregado (aro)

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Anel fino de vidro azulado no plano YZ, com eixo de simetria em X, e cargas espaçadas ao longo do aro (espaçamento regular com pequeno jitter). Eixo de simetria opcional (tracejado neutro).

![Anel carregado (aro)](previews/anel_carregado.png)

**Como se lê:** Aro de vidro fino com pontos azuis alinhados e, opcionalmente, o eixo tracejado atravessando o centro. Lê-se como 'carga distribuída numa linha circular; o campo no eixo se calcula somando dq'.

**Usar quando**
- campo elétrico no eixo de um anel carregado (integração de elementos de carga dq, simetria, análise de máximo e limites)
- momento de inércia de um aro (com_cargas=0), com o eixo de simetria desenhado
- contraste com o disco (superfície) e com a haste (linha reta)
- espira com corrente: cargas circulando pelo aro (cargas_moveis=1)

**Não usar quando**
- a carga está numa superfície (use disco_carregado) ou numa linha reta (use haste_carregada)
- a espessura real do anel importa para o problema (o tubo aqui é só visual)

**Limitações**
- o campo e a gaussiana não são desenhados: o ciano é reservado ao campo (animação 2D/Manim)
- em contexto de mecânica (com_cargas=0) o azul de 'fonte física' vem da gramática de Eletromagnetismo; a gramática de cor da Mecânica não foi verificada aqui
- espessura/raio do corpo exagerados em relação ao ideal (o corpo de vidro é visível); as cargas ficam dentro dele
- as cargas têm espaçamento quase regular (jitter 0,12): uma distribuição contínua é aproximada por pontos
- o movimento não codifica a corrente: a convenção (corrente convencional ou elétrons, que vão ao contrário) e o sinal vão por seta e rótulo no Manim; o movimento é didático, não em escala
- com cargas_moveis=1 as cargas estáticas (com_cargas) são substituídas pelas móveis

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `raio` | 1.5 | u | raio do anel |
| `raio_tubo` | 0.07 | u | raio do tubo do anel (visual) |
| `n_cargas` | 60 | n | número de cargas ao longo do aro |
| `com_cargas` | 1 | 0/1 | 1 = cargas pontuais (campo elétrico); 0 = só o corpo de vidro (ex.: momento de inércia) |
| `eixo` | 0 | 0/1 | 1 = eixo de simetria tracejado em cor neutra |
| `comprimento_eixo` | 4.0 | u | comprimento do eixo de simetria, se desenhado |
| `semente` | 7 | n | semente do sorteio/jitter (mesma semente = mesma distribuição) |
| `cargas_moveis` | 0 | 0/1 | 1 = cargas em movimento (animação em loop); use com animar.py ou a ponte com o Manim |
| `fase` | 0.0 | 0-1 | fase do movimento; fase=1 repete o quadro da fase 0 (loop perfeito) |
| `espaco_cargas` | 0.4 | u | distância entre cargas ao longo do aro (ajustada para fechar a volta) |
| `tamanho_carga_movel` | 0.07 | u | raio de cada carga móvel |

**Integração:** `png_seq_alpha` · custo 0.63 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `circulacao` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 0.62 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- anel_carregado --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("anel_carregado").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/anel_carregado.json`

### `anteparo_fenda_dupla` — Anteparo de fenda dupla

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Anteparo opaco azul (normal X) com duas fendas verticais (ao longo de Z) de largura `fenda`, separadas de `separacao` entre centros; as bordas das fendas em azul-claro. Nada atrás dele: a onda, as frentes e a figura de interferência são do Manim.

![Anteparo de fenda dupla](previews/anteparo_fenda_dupla.png)

**Como se lê:** Placa azul com duas frestas escuras e bordas claras: lê-se como 'duas fontes coerentes'.

**Usar quando**
- experimento de Young: interferência em fenda dupla, d sen θ = mλ
- difração por fenda simples (com separacao grande ou uma só fenda no Manim)
- mostrar a geometria (a, d) antes das frentes de onda

**Não usar quando**
- redes de difração com muitas fendas
- fenda simples: este sólido sempre tem duas

**Limitações**
- só o objeto: raios, frentes de onda, ângulos e a figura de interferência são do Manim
- vidro translúcido azul-claro (padrão do arsenal): não representa cor, dispersão nem índice de refração
- as fendas se leem como frestas escuras: sem fundo, o espaço atrás aparece vazio (preto)

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `largura` | 4.0 | u | largura do anteparo (eixo Y) |
| `altura` | 3.0 | u | altura do anteparo (eixo Z) |
| `espessura` | 0.12 | u | espessura (eixo X) |
| `fenda` | 0.2 | u | largura a de cada fenda |
| `separacao` | 1.0 | u | distância d entre os centros das fendas |

**Integração:** `png_seq_alpha` · custo 0.6 s/frame (1080p, Eevee)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- anteparo_fenda_dupla --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("anteparo_fenda_dupla").mobject(altura=5)   # estático: um quadro PNG com alpha
```

Ficha: `solidos/anteparo_fenda_dupla.json`

### `aro_rolando` — Aro rolando sem deslizar

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Aro (toro fino de vidro azulado, eixo ao longo de Y) com 3 marcas a 120° e a do centro de massa, sobre o chão que corre. Eixo instantâneo violeta tracejado no contato.

![Aro rolando sem deslizar](previews/aro_rolando.png)

**Como se lê:** Aro girando parado no centro, com 3 marcas que mostram a rotação sem rótulo; o chão corre. Lê-se como 'aro rolando sem deslizar'.

**Usar quando**
- rolamento sem deslizar: v_cm = ωR, energia cinética de translação + rotação
- mostrar o eixo instantâneo de rotação (no ponto de contato) como construção violeta
- comparar corpos de momentos de inércia diferentes (esfera, cilindro, aro) pela forma, em vídeos separados ou composição no Manim
- aro ou argola rolando (I = M R²)

**Não usar quando**
- o corpo desliza (rolamento com escorregamento): as marcas do chão não acompanham o giro
- problemas com rampa e corrida de corpos: aqui só chão plano
- disco ou cilindro cheio: use cilindro_rolando

**Limitações**
- câmera acompanha o corpo: ele gira parado no centro do quadro e é o chão que corre (é o que torna o loop perfeito); para mostrar o corpo avançando no quadro, ou corridas entre corpos, é preciso compor no Manim
- chão horizontal: não há rampa nem inclinação
- só a cinemática visual: velocidades (v_cm = ωR), energia, atrito e o sentido de rotação em vetores/rótulos ficam para o Manim
- a gramática de cor de Mecânica segue o padrão do arsenal (estilo.json): azul para o corpo, branco neutro para as marcas, violeta tracejado para a construção (eixo instantâneo)
- o aro é um toro fino: a espessura é só visual (0,07)
- o loop fecha com ruído de amostragem: 95% dos pixels diferem em até 2/255 entre a fase 0 e a fase 1 (só 2 a 301 pixels chegam a 3-7), invisível a olho nu

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `raio` | 1.0 | u | raio do corpo |
| `voltas` | 1 | n | voltas completas por loop (o chão avança 2πR por volta) |
| `eixo_instantaneo` | 1 | 0/1 | 1 = eixo instantâneo de rotação tracejado violeta no ponto de contato |
| `marca_centro` | 1 | 0/1 | 1 = marca do centro de massa |
| `movimento` | 0 | 0/1 | 1 = animação do rolamento (use animar.py ou a ponte com o Manim) |
| `fase` | 0.0 | 0-1 | fase do rolamento; fase=1 repete o quadro da fase 0 (loop perfeito) |

**Integração:** `png_seq_alpha` · custo 0.88 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `rolamento` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 0.88 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- aro_rolando --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("aro_rolando").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/aro_rolando.json`

### `caixa_gas_cinetica` — Gás ideal em recipiente com êmbolo (teoria cinética)

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Recipiente de vidro (arestas azul-claro) com um êmbolo e moléculas neutras (brancas perto, azul-claro longe) ricocheteando nas paredes e no êmbolo. `pistao` = fração do comprimento ocupada pelo gás; `temperatura` multiplica a velocidade das moléculas; `amplitude_pistao` faz o êmbolo oscilar (compressão e expansão) ao longo do loop.

![Gás ideal em recipiente com êmbolo (teoria cinética)](previews/caixa_gas_cinetica.png)

**Como se lê:** Caixa de vidro com um êmbolo e pontos brancos em movimento; com o êmbolo oscilando, o volume muda e as moléculas ficam mais densas. Lê-se como 'gás ideal: pressão = colisões, T = velocidade média'.

**Usar quando**
- teoria cinética: pressão como colisões com as paredes, temperatura como energia cinética média
- processos em gases ideais: compressão e expansão pelo êmbolo (isotérmica, adiabática no Manim)
- primeira lei: trabalho realizado pelo êmbolo

**Não usar quando**
- o ponto é o gráfico P×V (é do Manim; este sólido dá a imagem microscópica)
- gás real ou interações entre moléculas (as moléculas não colidem entre si)

**Limitações**
- as moléculas não colidem entre si e a velocidade de cada uma é fixa (ciclos inteiros por loop): não há distribuição de Maxwell nem troca de energia
- ao oscilar o êmbolo, as posições são escaladas com o volume (aproximação visual): a velocidade não muda como numa compressão adiabática real; temperatura/pressão ficam para o Manim
- moléculas e cargas têm aspectos parecidos (pontos): moléculas são brancas, cargas azuis
- a velocidade é o número de ciclos por loop: o loop precisa ser longo o bastante (60 quadros) para as mais rápidas não parecerem tremer

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `comprimento` | 4.0 | u | comprimento do recipiente (eixo X) |
| `largura` | 2.0 | u | lado da seção quadrada |
| `n_moleculas` | 40 | n | número de moléculas |
| `temperatura` | 1.0 | x | fator de velocidade das moléculas (inteiro de ciclos por loop) |
| `pistao` | 0.8 | 0-1 | fração do comprimento ocupada pelo gás |
| `amplitude_pistao` | 0.0 | 0-1 | oscilação do êmbolo (fração do comprimento); 0 = fixo |
| `semente` | 7 | n | semente do sorteio |
| `movimento` | 0 | 0/1 | 1 = animação em loop (use animar.py ou a ponte com o Manim) |
| `fase` | 0.0 | 0-1 | fase do loop; fase=1 repete o quadro da fase 0 (loop perfeito) |

**Integração:** `png_seq_alpha` · custo 1.12 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `colisoes` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 1.12 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- caixa_gas_cinetica --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("caixa_gas_cinetica").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/caixa_gas_cinetica.json`

### `campo_vetorial` — Campo vetorial (setas)

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Campo vetorial como setas ciano numa grade (plano z = 0 com `dim=2`; cubo com `dim=3`). `tipo`: radial (fonte), rotacional (circulação), sela ou espiral (fonte + circulação). O comprimento da seta cresce com o módulo do campo.

![Campo vetorial (setas)](previews/campo_vetorial.png)

**Como se lê:** Grade de setas ciano: para fora (radial), em círculos (rotacional), ao longo de eixos (sela) ou em espiral. Lê-se como 'campo de vetores'; a divergência e o rotacional se leem na forma.

**Usar quando**
- visualizar campos escalares e vetoriais, linhas e padrões (Cálculo IV 11.1)
- divergência (fonte/sumidouro) e rotacional (circulação) pela forma do campo
- campo elétrico ou de velocidades de fluido como setas (o ciano é reservado ao campo)

**Não usar quando**
- campos que variam no tempo ou com singularidades (o preview não evita o centro)
- linhas de campo contínuas (as setas são amostras)

**Limitações**
- a gramática de cor segue o padrão do arsenal: campo vetorial = ciano (reservado ao campo), normal n̂ = azul, tangentes = branco, construções (remendo, contorno) = violeta, nunca sólidas
- só o objeto geométrico: integrais, fórmulas e o sinal da circulação/fluxo são do Manim
- campo amostrado numa grade de n×n (ou n×n×4 em 3D); o comprimento é normalizado entre 28% e 100% do máximo, então não é proporcional ao módulo absoluto
- só 4 campos prontos (radial, rotacional, sela, espiral); outro exige alterar CAMPOS em calc_vetorial.py

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `tipo` | rotacional | texto | radial, rotacional, sela ou espiral |
| `dim` | 2 | n | 2 = plano; 3 = cubo (mais setas) |
| `n` | 7 | n | setas por lado da grade |
| `extensao` | 3.0 | u | meia largura da região |

**Integração:** `png_seq_alpha` · custo 0.41 s/frame (1080p, Eevee)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- campo_vetorial --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("campo_vetorial").mobject(altura=5)   # estático: um quadro PNG com alpha
```

Ficha: `solidos/campo_vetorial.json`

### `capacitor_esferico` — Capacitor esférico (esferas concêntricas, em corte)

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Esfera condutora interna de raio `raio_a` (vidro, cargas na superfície) dentro de uma casca esférica externa de raio `raio_b`, com um octante removido voltado para a câmera (como a casca esférica do arsenal). O mesmo número de cargas nas duas superfícies.

![Capacitor esférico (esferas concêntricas, em corte)](previews/capacitor_esferico.png)

**Como se lê:** Esfera de vidro com pontos azuis dentro de uma casca azul aberta em corte, também com pontos na face interna: lê-se como 'duas superfícies esféricas concêntricas carregadas, com um vão entre elas'.

**Usar quando**
- capacitor esférico: C = 4πε₀ ab/(b−a), campo ∝ 1/r² no vão
- Gauss em simetria esférica com condutores
- contraste com placas paralelas e com o coaxial

**Não usar quando**
- isolante com carga em volume (use esfera_macica_isolante)
- casca única (use casca_esferica_oca)

**Limitações**
- o sinal da carga não é codificado em cor: +Q e −Q vão por rótulo no Manim; o campo (ciano) também
- o mesmo número de cargas em cada armadura (carga igual e oposta)
- o corte em octante é convenção de leitura; as cargas da região removida não são desenhadas
- o corte aponta para a câmera padrão (azimute -23, elevação 17)

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `raio_a` | 0.8 | u | raio da esfera interna |
| `raio_b` | 1.6 | u | raio externo da casca |
| `espessura` | 0.06 | u | espessura da parede da casca |
| `n_cargas` | 70 | n | cargas por superfície |
| `corte` | 1 | 0/1 | 1 = remove o octante voltado para a câmera |

**Integração:** `png_seq_alpha` · custo 0.81 s/frame (1080p, Eevee)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- capacitor_esferico --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("capacitor_esferico").mobject(altura=5)   # estático: um quadro PNG com alpha
```

Ficha: `solidos/capacitor_esferico.json`

### `capacitor_placas_paralelas` — Capacitor de placas paralelas

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Duas placas de vidro azulado quadradas e paralelas (normal X) separadas por `distancia`, com o mesmo número de cargas pontuais nas faces internas. Dielétrico opcional (vidro azul-claro enchendo o vão).

![Capacitor de placas paralelas](previews/capacitor_placas_paralelas.png)

**Como se lê:** Duas folhas de vidro paralelas com pontos azuis voltados um para o outro: lê-se como 'duas armaduras com cargas iguais e opostas e um vão entre elas'.

**Usar quando**
- capacitor de placas paralelas: C = ε₀A/d, campo uniforme no vão, energia armazenada
- inserir um dielétrico (dieletrico=1) e comparar com o vão vazio
- contraste com o capacitor cilíndrico (cilindro_coaxial) e o esférico

**Não usar quando**
- o ponto é o plano infinito sem borda (use placa_infinita_carregada)
- efeitos de borda do campo: aqui as placas são desenhadas sem campo

**Limitações**
- o sinal da carga não é codificado em cor: +Q e −Q vão por rótulo no Manim; o campo (ciano) também
- o mesmo número de cargas em cada armadura (carga igual e oposta)
- as placas são quadradas e finitas; o campo uniforme 'ideal' é uma aproximação feita no Manim

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `lado` | 3.0 | u | lado das placas quadradas |
| `distancia` | 1.0 | u | distância d entre as placas |
| `espessura` | 0.06 | u | espessura das placas (visual) |
| `n_cargas` | 36 | n | cargas por placa |
| `dist_min` | 0.42 | u | distância mínima entre cargas |
| `dieletrico` | 0 | 0/1 | 1 = dielétrico (vidro claro) no vão |
| `semente` | 7 | n | semente do sorteio |

**Integração:** `png_seq_alpha` · custo 0.92 s/frame (1080p, Eevee)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- capacitor_placas_paralelas --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("capacitor_placas_paralelas").mobject(altura=5)   # estático: um quadro PNG com alpha
```

Ficha: `solidos/capacitor_placas_paralelas.json`

### `casca_cilindrica_oca` — Casca cilíndrica oca

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Tubo oco de parede fina, aberto nas duas pontas, com eixo ao longo de X. O raio externo é `raio`; a espessura cresce para dentro.

![Casca cilíndrica oca](previews/casca_cilindrica_oca.png)

**Como se lê:** Aro claro (#7FB2FF) marca a parede fina; interior escuro e vazio; exterior azul (#267BFF). Lê-se como 'só há material na superfície'.

**Usar quando**
- a carga ou o material está só na superfície de um cilindro (casca cilíndrica, condutor oco)
- contraste casca x maciço (par com cilindro_macico_isolante)
- mostrar que o interior é vazio, por exemplo campo nulo dentro via Lei de Gauss

**Não usar quando**
- precisa mostrar cargas individuais no volume (use cilindro_macico_isolante)
- é preciso um cilindro finito com tampas fechadas: esta casca é aberta nas pontas

**Limitações**
- não desenha cargas individuais sobre a superfície
- eixo fixo em X; para outra orientação, girar a câmera/pivô na cena
- espessura de parede exagerada em relação a uma casca ideal (padrão 0,10)

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `raio` | 1.0 | u | raio externo |
| `comprimento` | 4.0 | u | comprimento ao longo do eixo X |
| `espessura` | 0.1 | u | espessura da parede (cresce para dentro) |
| `lados` | 96 | n | segmentos da circunferência |

**Integração:** `png_seq_alpha` · custo 0.56 s/frame (1080p, Eevee)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- casca_cilindrica_oca --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("casca_cilindrica_oca").mobject(altura=5)   # estático: um quadro PNG com alpha
```

Ficha: `solidos/casca_cilindrica_oca.json`

### `casca_esferica_oca` — Casca esférica oca (com corte em octante)

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Esfera oca de parede fina com um octante removido (x>0, y<0, z>0), voltado para a câmera padrão, que expõe a parede e o interior vazio. O raio externo é `raio`; a espessura cresce para dentro. Com `corte=0` a esfera fica fechada.

![Casca esférica oca (com corte em octante)](previews/casca_esferica_oca.png)

**Como se lê:** Exterior azul (#267BFF) opaco; o contorno do corte tem um aro claro (#7FB2FF) que mostra a parede fina; dentro, escuro e vazio. Lê-se como 'só há material na superfície; o interior é vazio'.

**Usar quando**
- a carga ou o material está só na superfície de uma esfera (casca esférica, condutor oco)
- contraste casca x maciço (par com esfera_macica_isolante)
- mostrar que o interior é vazio, por exemplo campo nulo dentro via Lei de Gauss

**Não usar quando**
- precisa mostrar cargas individuais no volume (use esfera_macica_isolante)
- o ponto do vídeo é a esfera inteira e fechada: o corte em octante existe só para mostrar o interior
- densidade de carga não uniforme em volume (ex.: rho(r)): este sólido não representa perfil radial

**Limitações**
- o octante removido é uma convenção de leitura, não parte da física: a casca real é fechada
- o corte aponta para a câmera padrão (azimute -23, elevação 17); com outro ângulo de câmera o corte pode ficar de costas
- não desenha cargas individuais sobre a superfície
- espessura de parede exagerada em relação a uma casca ideal (padrão 0,08)

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `raio` | 1.0 | u | raio externo |
| `espessura` | 0.08 | u | espessura da parede (cresce para dentro) |
| `segmentos` | 96 | n | segmentos de longitude (múltiplo de 4, para o corte cair sobre linhas da malha) |
| `aneis` | 48 | n | anéis de latitude (par, pelo mesmo motivo) |
| `corte` | 1 | 0/1 | 1 = remove o octante voltado para a câmera; 0 = esfera fechada |

**Integração:** `png_seq_alpha` · custo 0.45 s/frame (1080p, Eevee)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- casca_esferica_oca --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("casca_esferica_oca").mobject(altura=5)   # estático: um quadro PNG com alpha
```

Ficha: `solidos/casca_esferica_oca.json`

### `cilindro_coaxial` — Cilindro coaxial (condutor maciço + casca externa, em corte)

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Modelo do capacitor coaxial (yt_0002, A4): condutor interno maciço de raio `raio_a` (vidro translúcido) dentro de uma casca externa delgada de raio `raio_b` > `raio_a`, coaxiais, com eixo ao longo de X. A casca tem uma faixa longitudinal removida (voltada para a câmera) para o condutor aparecer. O condutor tem cargas só na superfície; a casca tem o MESMO número de cargas na face interna (lambda igual e oposto), logo mais esparsas.

![Cilindro coaxial (condutor maciço + casca externa, em corte)](previews/cilindro_coaxial.png)

**Como se lê:** Casca azul opaca aberta, com aro claro (#7FB2FF) marcando a parede e o corte; dentro, um cilindro de vidro com pontos azuis só na superfície. O vão entre os dois é vazio. Lê-se como 'duas superfícies carregadas, coaxiais, com um vão entre elas'.

**Usar quando**
- capacitor coaxial / cabo coaxial: condutor interno maciço e condutor externo em casca delgada, em equilíbrio eletrostático
- mostrar que a carga do condutor interno fica na sua superfície (e não no volume) e que as cargas por comprimento são iguais e opostas
- delimitar as regiões r < a, a < r < b e r > b para a superfície gaussiana coaxial

**Não usar quando**
- o interno é isolante com carga em volume (use cilindro_macico_isolante)
- o condutor externo é espesso com três raios públicos (a, b, c): este sólido tem casca delgada de propósito
- o ponto do vídeo exige distinguir o sinal das cargas (+ e −) em cor: aqui o sinal não é codificado (use rótulos no Manim)
- um cilindro isolado sem condutor externo (use casca_cilindrica_oca ou cilindro_macico_isolante)

**Limitações**
- o sinal da carga não é codificado em cor (o padrão visual não define cores de polaridade); +λ e −λ têm de ser indicados por rótulos no Manim
- o corte longitudinal é convenção de leitura: a casca real é fechada; as cargas da faixa removida não são desenhadas, então aparecem menos cargas visíveis na casca do que o número nominal
- o condutor interno usa o mesmo vidro do isolante maciço: o que o distingue é a carga só na superfície
- espessura de parede exagerada em relação a uma casca ideal delgada (padrão 0,08)
- o corte aponta para a câmera padrão (azimute -23, elevação 17); com outro ângulo pode ficar de costas

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `raio_a` | 0.5 | u | raio do condutor interno |
| `raio_b` | 1.5 | u | raio externo da casca (deve ser maior que raio_a) |
| `comprimento` | 5.0 | u | comprimento ao longo do eixo X (igual nos dois cilindros) |
| `espessura` | 0.08 | u | espessura da parede da casca (cresce para dentro) |
| `n_cargas` | 70 | n | cargas por superfície, iguais nas duas (lambda igual e oposto) |
| `dist_min` | 0.35 | u | distância mínima entre cargas |
| `tamanho_carga` | 0.04 | u | raio de cada esfera de carga |
| `semente` | 7 | n | semente do sorteio (mesma semente = mesma distribuição) |
| `corte` | 1 | 0/1 | 1 = remove a faixa da casca voltada para a câmera; 0 = casca inteira (o condutor só aparece pela ponta aberta) |

**Integração:** `png_seq_alpha` · custo 0.95 s/frame (1080p, Eevee)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- cilindro_coaxial --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("cilindro_coaxial").mobject(altura=5)   # estático: um quadro PNG com alpha
```

Ficha: `solidos/cilindro_coaxial.json`

### `cilindro_macico_isolante` — Cilindro maciço isolante com cargas no volume

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Cilindro preenchido, de vidro azulado translúcido, com tampas, eixo ao longo de X e cargas pontuais distribuídas uniformemente no volume (distância mínima entre elas, semente fixa).

![Cilindro maciço isolante com cargas no volume](previews/cilindro_macico_isolante.png)

**Como se lê:** Vidro translúcido de borda luminosa cheio de pontos. Cargas próximas da câmera são azul-claro (#7FB2FF) e brilhantes; as distantes, azul (#267BFF) e fracas (pista de profundidade). O ciano fica livre para o campo E⃗. Lê-se como 'há material e carga em todo o volume'.

**Usar quando**
- a carga está distribuída no volume de um cilindro isolante (densidade volumétrica)
- contraste casca x maciço (par com casca_cilindrica_oca)
- mostrar que existe carga no interior, por exemplo campo crescendo com r dentro do cilindro

**Não usar quando**
- o material só existe na superfície (use casca_cilindrica_oca)
- a densidade de carga é não uniforme e isso é o ponto do vídeo: as cargas aqui são distribuídas uniformemente

**Limitações**
- distribuição uniforme apenas; não há perfil radial rho(r)
- material translúcido exige culling de faces de trás (já embutido); ângulos muito rasantes não foram testados
- eixo fixo em X

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `raio` | 1.0 | u | raio do cilindro |
| `comprimento` | 4.0 | u | comprimento ao longo do eixo X |
| `n_cargas` | 110 | n | número de cargas desejado (pode sair menos se a distância mínima não couber) |
| `dist_min` | 0.26 | u | distância mínima entre cargas |
| `tamanho_carga` | 0.04 | u | raio de cada esfera de carga |
| `semente` | 7 | n | semente do sorteio (mesma semente = mesma distribuição) |

**Integração:** `png_seq_alpha` · custo não medido

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- cilindro_macico_isolante --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("cilindro_macico_isolante").mobject(altura=5)   # estático: um quadro PNG com alpha
```

Ficha: `solidos/cilindro_macico_isolante.json`

### `cilindro_rolando` — Cilindro rolando sem deslizar

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Cilindro de vidro azulado (eixo ao longo de Y) com bordas circulares e 4 geratrizes em azul-claro, uma marca na borda e a do centro de massa, sobre o chão que corre. Eixo instantâneo violeta tracejado no contato.

![Cilindro rolando sem deslizar](previews/cilindro_rolando.png)

**Como se lê:** Tambor de vidro girando parado no centro, com geratrizes e uma marca na borda que mostram a rotação; o chão corre. Lê-se como 'cilindro rolando sem deslizar'.

**Usar quando**
- rolamento sem deslizar: v_cm = ωR, energia cinética de translação + rotação
- mostrar o eixo instantâneo de rotação (no ponto de contato) como construção violeta
- comparar corpos de momentos de inércia diferentes (esfera, cilindro, aro) pela forma, em vídeos separados ou composição no Manim
- cilindro maciço rolando (I = 1/2 M R²)

**Não usar quando**
- o corpo desliza (rolamento com escorregamento): as marcas do chão não acompanham o giro
- problemas com rampa e corrida de corpos: aqui só chão plano
- casca cilíndrica oca (I = M R²): este cilindro é de vidro cheio

**Limitações**
- câmera acompanha o corpo: ele gira parado no centro do quadro e é o chão que corre (é o que torna o loop perfeito); para mostrar o corpo avançando no quadro, ou corridas entre corpos, é preciso compor no Manim
- chão horizontal: não há rampa nem inclinação
- só a cinemática visual: velocidades (v_cm = ωR), energia, atrito e o sentido de rotação em vetores/rótulos ficam para o Manim
- a gramática de cor de Mecânica segue o padrão do arsenal (estilo.json): azul para o corpo, branco neutro para as marcas, violeta tracejado para a construção (eixo instantâneo)
- a distribuição de massa (maciço ou oco) não é codificada visualmente: dizer por rótulo
- o loop fecha com ruído de amostragem: 95% dos pixels diferem em até 2/255 entre a fase 0 e a fase 1 (só 2 a 301 pixels chegam a 3-7), invisível a olho nu

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `largura` | 2.0 | u | comprimento do cilindro ao longo do eixo Y |
| `raio` | 1.0 | u | raio do corpo |
| `voltas` | 1 | n | voltas completas por loop (o chão avança 2πR por volta) |
| `eixo_instantaneo` | 1 | 0/1 | 1 = eixo instantâneo de rotação tracejado violeta no ponto de contato |
| `marca_centro` | 1 | 0/1 | 1 = marca do centro de massa |
| `movimento` | 0 | 0/1 | 1 = animação do rolamento (use animar.py ou a ponte com o Manim) |
| `fase` | 0.0 | 0-1 | fase do rolamento; fase=1 repete o quadro da fase 0 (loop perfeito) |

**Integração:** `png_seq_alpha` · custo 1.22 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `rolamento` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 1.22 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- cilindro_rolando --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("cilindro_rolando").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/cilindro_rolando.json`

### `colisao_1d` — Colisão unidimensional entre dois blocos

**Status:** estudo · Tecnicamente validado (render 960x540); aparência aguardando aprovação do usuário.

Dois blocos de vidro sobre um trilho (bloco 1 azul, bloco 2 azul-claro; o tamanho cresce com a massa) que colidem em x = 0 no instante `instante`. `restituicao` e = 1 elástica, e = 0 totalmente inelástica (grudam). Uma esfera neutra marca o centro de massa, que não muda de velocidade. Animação de CICLO ÚNICO (a fase 1 é o estado final, diferente da fase 0).

![Colisão unidimensional entre dois blocos](previews/colisao_1d.png)

**Como se lê:** Dois blocos se aproximam, colidem e se afastam (ou seguem juntos); a marca do CM anda em linha reta o tempo todo.

**Usar quando**
- colisões elásticas e inelásticas: conservação do momento linear
- mostrar que o centro de massa não é afetado pela colisão
- comparar massas diferentes (o tamanho do bloco acompanha a massa)

**Não usar quando**
- colisões em duas dimensões
- colisão com perda de massa ou explosões

**Limitações**
- só o objeto em movimento: velocidades, energia, gráficos x(t) e as fórmulas são do Manim
- movimento didático calculado por fórmula (não é uma simulação física de verdade)
- ciclo único: não há loop (a fase 1 não repete a fase 0); a ponte renderiza quadros de 0 a 1 incluindo o final, e o Manim congela no fim
- só 1D, sem atrito (os blocos deslizam a velocidade constante); o tamanho do bloco é proporcional a m^(1/3)
- os blocos não se deformam e o contato é instantâneo

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `m1` | 2.0 | u | massa do bloco 1 (azul) |
| `m2` | 1.0 | u | massa do bloco 2 (azul-claro) |
| `v1` | 3.0 | u | velocidade inicial do bloco 1 (deve ser maior que v2) |
| `v2` | 0.0 | u | velocidade inicial do bloco 2 |
| `restituicao` | 1.0 | 0-1 | coeficiente de restituição e (1 elástica, 0 inelástica) |
| `instante` | 0.45 | 0-1 | instante da colisão (fração da duração) |
| `mostrar_cm` | 1 | 0/1 | 1 = marca do centro de massa |
| `movimento` | 0 | 0/1 | 1 = animação (use animar.py ou a ponte com o Manim) |
| `fase` | 0.0 | 0-1 | fase da animação |

**Integração:** `png_seq_alpha` · custo 0.75 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `colisao` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 0.75 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- colisao_1d --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("colisao_1d").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/colisao_1d.json`

### `disco_carregado` — Disco carregado

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Disco fino de vidro azulado no plano YZ, com eixo de simetria em X, e cargas uniformes sobre a superfície (distância mínima entre elas, semente fixa). Eixo de simetria opcional (tracejado neutro).

![Disco carregado](previews/disco_carregado.png)

**Como se lê:** Disco translúcido de borda luminosa, cheio de pontos uniformes e, opcionalmente, o eixo tracejado atravessando o centro. Lê-se como 'carga distribuída numa superfície circular'.

**Usar quando**
- campo elétrico no eixo de um disco carregado (anéis concêntricos somados; no limite de raio grande recupera o plano infinito)
- momento de inércia de um disco (com_cargas=0), com o eixo de simetria desenhado
- contraste com o anel (linha circular) e com a placa infinita (plano ilimitado)
- disco carregado girando (corrente de rotação; cargas_moveis=1)

**Não usar quando**
- o ponto do vídeo é um plano ilimitado sem borda (use placa_infinita_carregada)
- a carga está só no aro (use anel_carregado)

**Limitações**
- o campo e a gaussiana não são desenhados: o ciano é reservado ao campo (animação 2D/Manim)
- em contexto de mecânica (com_cargas=0) o azul de 'fonte física' vem da gramática de Eletromagnetismo; a gramática de cor da Mecânica não foi verificada aqui
- espessura/raio do corpo exagerados em relação ao ideal (o corpo de vidro é visível); as cargas ficam dentro dele
- cargas apenas sobre o plano médio do disco (visíveis através do vidro): uma só camada
- a densidade é uniforme: perfil radial não uniforme não está representado
- o movimento não codifica a corrente: a convenção (corrente convencional ou elétrons, que vão ao contrário) e o sinal vão por seta e rótulo no Manim; o movimento é didático, não em escala
- rotação rígida: as cargas mantêm a distribuição e giram em torno do eixo X

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `raio` | 1.8 | u | raio do disco |
| `espessura` | 0.06 | u | espessura do disco (visual) |
| `n_cargas` | 110 | n | número de cargas desejado (pode sair menos se a distância mínima não couber) |
| `dist_min` | 0.28 | u | distância mínima entre cargas |
| `com_cargas` | 1 | 0/1 | 1 = cargas pontuais (campo elétrico); 0 = só o corpo de vidro (ex.: momento de inércia) |
| `eixo` | 0 | 0/1 | 1 = eixo de simetria tracejado em cor neutra |
| `comprimento_eixo` | 4.0 | u | comprimento do eixo de simetria, se desenhado |
| `semente` | 7 | n | semente do sorteio/jitter (mesma semente = mesma distribuição) |
| `cargas_moveis` | 0 | 0/1 | 1 = cargas em movimento (animação em loop); use com animar.py ou a ponte com o Manim |
| `fase` | 0.0 | 0-1 | fase do movimento; fase=1 repete o quadro da fase 0 (loop perfeito) |
| `voltas` | 1 | n | voltas completas por loop (rotação rígida em torno do eixo) |

**Integração:** `png_seq_alpha` · custo 0.71 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `rotacao` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 0.72 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- disco_carregado --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("disco_carregado").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/disco_carregado.json`

### `esfera_macica_isolante` — Esfera maciça isolante com cargas no volume

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Orbe de vidro azulado translúcido, preenchido, com cargas pontuais distribuídas uniformemente no volume da bola (distância mínima entre elas, semente fixa).

![Esfera maciça isolante com cargas no volume](previews/esfera_macica_isolante.png)

**Como se lê:** Vidro translúcido de borda luminosa cheio de pontos. Cargas próximas da câmera são azul-claro (#7FB2FF) e brilhantes; as distantes, azul (#267BFF) e fracas (pista de profundidade). O ciano fica livre para o campo E⃗. Lê-se como 'há material e carga em todo o volume'.

**Usar quando**
- a carga está distribuída no volume de uma esfera isolante com densidade uniforme
- contraste casca x maciço (par com casca_esferica_oca)
- mostrar que existe carga no interior, por exemplo campo crescendo com r dentro da esfera

**Não usar quando**
- o material só existe na superfície (use casca_esferica_oca)
- a densidade de carga é não uniforme e isso é o ponto do vídeo: as cargas aqui são uniformes (para rho(r) seria preciso outro sólido)
- é preciso um condutor: num condutor a carga fica na superfície

**Limitações**
- distribuição uniforme apenas; não há perfil radial rho(r)
- o brilho do vidro mostra um reflexo retangular suave da luz principal; é cosmético
- o número de cargas desejado pode não caber com a distância mínima escolhida (sai menos)

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `raio` | 1.0 | u | raio da esfera |
| `n_cargas` | 70 | n | número de cargas desejado (pode sair menos se a distância mínima não couber) |
| `dist_min` | 0.3 | u | distância mínima entre cargas |
| `tamanho_carga` | 0.04 | u | raio de cada esfera de carga |
| `semente` | 7 | n | semente do sorteio (mesma semente = mesma distribuição) |

**Integração:** `png_seq_alpha` · custo 0.71 s/frame (1080p, Eevee)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- esfera_macica_isolante --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("esfera_macica_isolante").mobject(altura=5)   # estático: um quadro PNG com alpha
```

Ficha: `solidos/esfera_macica_isolante.json`

### `esfera_rolando` — Esfera rolando sem deslizar

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Esfera de vidro azulado com 3 meridianos e o equador em azul-claro, uma marca de superfície e a marca do centro de massa, sobre um chão de vidro com marcas transversais que corre sob ela (câmera acompanha). Eixo instantâneo de rotação tracejado violeta no contato.

![Esfera rolando sem deslizar](previews/esfera_rolando.png)

**Como se lê:** Esfera de vidro girando parada no centro, com riscos que mostram a rotação e um ponto de superfície que descreve uma ciclóide; o chão corre e o eixo violeta fica no contato. Lê-se como 'rolar sem deslizar'.

**Usar quando**
- rolamento sem deslizar: v_cm = ωR, energia cinética de translação + rotação
- mostrar o eixo instantâneo de rotação (no ponto de contato) como construção violeta
- comparar corpos de momentos de inércia diferentes (esfera, cilindro, aro) pela forma, em vídeos separados ou composição no Manim
- esfera maciça rolando (I = 2/5 M R²)

**Não usar quando**
- o corpo desliza (rolamento com escorregamento): as marcas do chão não acompanham o giro
- problemas com rampa e corrida de corpos: aqui só chão plano
- casca esférica oca (I = 2/3 M R²): esta esfera é de vidro cheio, sem distinção de distribuição de massa

**Limitações**
- câmera acompanha o corpo: ele gira parado no centro do quadro e é o chão que corre (é o que torna o loop perfeito); para mostrar o corpo avançando no quadro, ou corridas entre corpos, é preciso compor no Manim
- chão horizontal: não há rampa nem inclinação
- só a cinemática visual: velocidades (v_cm = ωR), energia, atrito e o sentido de rotação em vetores/rótulos ficam para o Manim
- a gramática de cor de Mecânica segue o padrão do arsenal (estilo.json): azul para o corpo, branco neutro para as marcas, violeta tracejado para a construção (eixo instantâneo)
- a distribuição de massa (maciça ou oca) não é codificada visualmente: dizer por rótulo
- o loop fecha com ruído de amostragem: 95% dos pixels diferem em até 2/255 entre a fase 0 e a fase 1 (só 2 a 301 pixels chegam a 3-7), invisível a olho nu

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `raio` | 1.0 | u | raio do corpo |
| `voltas` | 1 | n | voltas completas por loop (o chão avança 2πR por volta) |
| `eixo_instantaneo` | 1 | 0/1 | 1 = eixo instantâneo de rotação tracejado violeta no ponto de contato |
| `marca_centro` | 1 | 0/1 | 1 = marca do centro de massa |
| `movimento` | 0 | 0/1 | 1 = animação do rolamento (use animar.py ou a ponte com o Manim) |
| `fase` | 0.0 | 0-1 | fase do rolamento; fase=1 repete o quadro da fase 0 (loop perfeito) |

**Integração:** `png_seq_alpha` · custo 1.17 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `rolamento` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 1.17 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- esfera_rolando --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("esfera_rolando").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/esfera_rolando.json`

### `fio_infinito` — Fio infinito (retilíneo)

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Fio retilíneo azul (#267BFF) ao longo de X, brilhante, com um halo de vidro fino em volta, cuja opacidade se dissolve nas duas pontas para sugerir comprimento infinito. Eixo de simetria opcional.

![Fio infinito (retilíneo)](previews/fio_infinito.png)

**Como se lê:** Linha azul luminosa com halo suave que some nas pontas: lê-se como 'fio muito longo, sem fim visível'.

**Usar quando**
- campo B de um fio longo (circulação amperiana circular em torno dele)
- linha de carga/corrente infinita como fonte
- contraste com solenoide e toroide (outras fontes de Ampère)
- corrente num fio: cargas em movimento ao longo dele (cargas_moveis=1, animar.py)
- corrente num fio: cargas em movimento ao longo dele (cargas_moveis=1)

**Não usar quando**
- o fio é finito e o efeito de pontas importa: aqui as pontas se dissolvem de propósito
- um condutor espesso com corrente distribuída na seção: este fio é fino

**Limitações**
- só a fonte física (fio/enrolamento, azul): o campo B (ciano) e o sentido da corrente são desenhados no 2D/Manim
- sem noção de sentido: a hélice tem um sentido de enrolamento, mas ele não representa a corrente de forma legível; indicar I por rótulo/seta no Manim
- fisicamente finito (10 por padrão): o 'infinito' é só visual; se o enquadramento incluir as pontas, o efeito se perde
- é um cilindro opaco-translúcido fino; não representa a densidade de corrente na seção
- o sentido do movimento não codifica a corrente: a convenção (corrente convencional ou elétrons, que vão ao contrário) e o sinal vão por seta e rótulo no Manim
- o movimento não codifica a corrente: a convenção (corrente convencional ou elétrons, que vão ao contrário) e o sinal vão por seta e rótulo no Manim; o movimento é didático, não em escala

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `comprimento` | 10.0 | u | comprimento do fio (eixo X) |
| `raio` | 0.06 | u | raio do fio (visual) |
| `eixo` | 0 | 0/1 | 1 = eixo tracejado neutro (coincide com o fio; útil só como guia) |
| `comprimento_eixo` | 6.0 | u | comprimento do eixo, se desenhado |
| `cargas_moveis` | 0 | 0/1 | 1 = cargas azul-claro deslizando ao longo do fio (corrente); o movimento é didático, não em escala |
| `fase` | 0.0 | 0-1 | fase do movimento: desloca as cargas de 0 a 1 espaçamento; fase=1 repete o quadro da fase 0 (loop perfeito) |
| `espaco_cargas` | 0.6 | u | distância entre cargas consecutivas ao longo do fio |
| `tamanho_carga_movel` | 0.09 | u | raio de cada carga móvel |

**Integração:** `png_seq_alpha` · custo 0.5 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `deslizamento` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 0.67 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- fio_infinito --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("fio_infinito").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/fio_infinito.json`

### `gaussiana_caixa` — Superfície gaussiana em caixa (pillbox)

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Caixa gaussiana curta (pillbox) de arestas violeta (#9C8CFF), com a normal do plano ao longo de X: `altura` em X e `lado` em Y e Z, centrada no plano. Faces de vidro violeta muito translúcido. Por padrão atravessa uma placa carregada de referência.

![Superfície gaussiana em caixa (pillbox)](previews/gaussiana_caixa.png)

**Como se lê:** Caixa de arestas violeta tracejadas atravessando o plano azul: metade de cada lado. Lê-se como 'a gaussiana envolve um pedaço do plano'; o fluxo sai pelas duas faces paralelas ao plano.

**Usar quando**
- simetria planar: plano infinito carregado, placa não condutora
- mostrar a caixa curta atravessando o plano e que só as faces paralelas ao plano contribuem
- contraste com as gaussianas esférica e cilíndrica na mesma unidade

**Não usar quando**
- simetria esférica ou cilíndrica (use gaussiana_esferica ou gaussiana_cilindrica)
- placa condutora com a caixa de um lado só: esta caixa é simétrica em torno do plano

**Limitações**
- a gaussiana é uma construção matemática, não um objeto físico: nunca preenchimento sólido (as faces são vidro violeta muito translúcido, só para dar volume)
- com_fonte=1 desenha também uma fonte de referência (aprovada do arsenal) só para contexto e teste de leitura; em vídeo use com_fonte=0 e componha com a fonte da cena
- a caixa é centrada no plano x=0 e simétrica; caixa assimétrica não é suportada
- no preview a placa de referência é menor (8 x 5) que a do sólido placa_infinita_carregada, para a caixa ficar legível
- o enquadramento padrão (azimute -40, elevação 16) segue o da placa

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `lado` | 2.4 | u | lado das faces paralelas ao plano (Y e Z) |
| `altura` | 1.4 | u | espessura da caixa ao longo de X (a normal do plano) |
| `continua` | 0 | 0/1 | 0 = arestas tracejadas; 1 = contínuas |
| `faces` | 1 | 0/1 | 1 = vidro violeta translúcido; 0 = só as arestas |
| `com_fonte` | 1 | 0/1 | 1 = desenha uma placa carregada de referência |

**Integração:** `png_seq_alpha` · custo 1.38 s/frame (1080p, Eevee)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- gaussiana_caixa --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("gaussiana_caixa").mobject(altura=5)   # estático: um quadro PNG com alpha
```

Ficha: `solidos/gaussiana_caixa.json`

### `gaussiana_cilindrica` — Superfície gaussiana cilíndrica (fechada)

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Cilindro gaussiano fechado (eixo X) de raio `raio` e comprimento `comprimento`: duas tampas circulares e linhas longitudinais em violeta (#9C8CFF), sobre vidro violeta muito translúcido. Lateral e tampas têm estilo independente (tracejado ou contínuo). Por padrão envolve um cilindro maciço de referência.

![Superfície gaussiana cilíndrica (fechada)](previews/gaussiana_cilindrica.png)

**Como se lê:** Cilindro de traços violeta sobre a fonte azul. Na gramática da série: lateral contínua = parte que contribui ao fluxo; tampas tracejadas = fluxo nulo (campo radial). O preview mostra esse estado (lateral contínua).

**Usar quando**
- simetria cilíndrica: linha infinita, cilindro maciço, casca cilíndrica, cabo coaxial
- mostrar que o fluxo vem só da lateral (2πrL) e as tampas não contribuem
- delimitar r < a, a < r < b e r > b com raios diferentes de gaussiana

**Não usar quando**
- simetria esférica ou planar (use gaussiana_esferica ou gaussiana_caixa)
- o campo não é radial ao eixo: o argumento das tampas nulas deixa de valer

**Limitações**
- a gaussiana é uma construção matemática, não um objeto físico: nunca preenchimento sólido (as faces são vidro violeta muito translúcido, só para dar volume)
- com_fonte=1 desenha também uma fonte de referência (aprovada do arsenal) só para contexto e teste de leitura; em vídeo use com_fonte=0 e componha com a fonte da cena
- comprimento finito: a gaussiana tem tampas, a fonte é idealmente infinita
- as linhas longitudinais (4 por padrão) são só guias de leitura da superfície
- eixo fixo em X; o enquadramento padrão (azimute -45, elevação 20) foi escolhido para a lateral ler bem

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `raio` | 1.5 | u | raio do cilindro gaussiano |
| `comprimento` | 3.0 | u | comprimento ao longo do eixo X |
| `lateral_continua` | 0 | 0/1 | 0 = lateral tracejada; 1 = contínua (contribui) |
| `tampas_continuas` | 0 | 0/1 | 0 = tampas tracejadas; 1 = contínuas |
| `n_linhas` | 4 | n | linhas longitudinais de guia |
| `faces` | 1 | 0/1 | 1 = vidro violeta translúcido; 0 = só os traços |
| `com_fonte` | 1 | 0/1 | 1 = desenha um cilindro maciço de referência dentro |
| `raio_fonte` | 1.0 | u | raio do cilindro de referência |
| `comprimento_fonte` | 4.0 | u | comprimento do cilindro de referência |

**Integração:** `png_seq_alpha` · custo 1.21 s/frame (1080p, Eevee)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- gaussiana_cilindrica --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("gaussiana_cilindrica").mobject(altura=5)   # estático: um quadro PNG com alpha
```

Ficha: `solidos/gaussiana_cilindrica.json`

### `gaussiana_esferica` — Superfície gaussiana esférica

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Esfera gaussiana de raio `raio`: equador e dois meridianos em violeta (#9C8CFF), tracejados por padrão, sobre um orbe de vidro violeta muito translúcido. Por padrão envolve uma esfera maciça de referência (`com_fonte`).

![Superfície gaussiana esférica](previews/gaussiana_esferica.png)

**Como se lê:** Três círculos violeta tracejados sobre uma esfera quase transparente, envolvendo a fonte azul. Tracejado = construção; contínuo (`continua=1`) = a superfície inteira contribui ao fluxo.

**Usar quando**
- simetria esférica: carga pontual, esfera maciça, casca esférica (campo radial)
- delimitar as regiões r < R e r > R ao escolher o raio da gaussiana
- mostrar o estado de construção (tracejada) e o de cálculo do fluxo (contínua)

**Não usar quando**
- simetria cilíndrica ou planar (use gaussiana_cilindrica ou gaussiana_caixa)
- qualquer superfície não fechada: esta é fechada por construção

**Limitações**
- a gaussiana é uma construção matemática, não um objeto físico: nunca preenchimento sólido (as faces são vidro violeta muito translúcido, só para dar volume)
- com_fonte=1 desenha também uma fonte de referência (aprovada do arsenal) só para contexto e teste de leitura; em vídeo use com_fonte=0 e componha com a fonte da cena
- a esfera inteira contribui: não há parte tracejada e parte contínua dentro de uma mesma esfera
- representada por três círculos (equador e dois meridianos), não por malha completa

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `raio` | 1.5 | u | raio da esfera gaussiana |
| `continua` | 0 | 0/1 | 0 = tracejada (construção); 1 = contínua (contribui ao fluxo) |
| `faces` | 1 | 0/1 | 1 = orbe de vidro violeta translúcido; 0 = só os traços |
| `com_fonte` | 1 | 0/1 | 1 = desenha uma esfera maciça de referência dentro |
| `raio_fonte` | 1.0 | u | raio da esfera de referência (menor que `raio`) |

**Integração:** `png_seq_alpha` · custo 1.01 s/frame (1080p, Eevee)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- gaussiana_esferica --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("gaussiana_esferica").mobject(altura=5)   # estático: um quadro PNG com alpha
```

Ficha: `solidos/gaussiana_esferica.json`

### `gradiente_colina` — Gradiente numa colina (curvas de nível)

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Colina gaussiana f(x, y) = h e^(−r²/2σ²) (vidro azul) com curvas de nível em azul-claro, um ponto P (branco) sobre a superfície, o vetor gradiente ∇f (ciano, horizontal, apontando para o topo) e a projeção vertical de P no plano (violeta tracejada). Com `movimento=1` o ponto circunda a colina e o gradiente gira com ele.

![Gradiente numa colina (curvas de nível)](previews/gradiente_colina.png)

**Como se lê:** Colina de vidro com anéis e um ponto com uma seta ciano perpendicular ao anel, apontando para o topo. Lê-se como 'o gradiente é perpendicular às curvas de nível e aponta para a maior subida'.

**Usar quando**
- gradiente e derivada direcional (Cálculo III 10.5): ∇f ⟂ curvas de nível
- extremos em várias variáveis (o topo da colina)
- relação do gradiente com o campo conservativo (potencial)

**Não usar quando**
- funções com pontos de sela (use superficie_parametrizada, tipo sela)
- mais de uma colina

**Limitações**
- a gramática de cor segue o padrão do arsenal: campo vetorial = ciano (reservado ao campo), normal n̂ = azul, tangentes = branco, construções (remendo, contorno) = violeta, nunca sólidas
- só o objeto geométrico: integrais, fórmulas e o sinal da circulação/fluxo são do Manim
- a seta do gradiente é horizontal (no plano xy) e normalizada em comprimento (0,35 + 0,9|∇f|, no máximo 1,6)
- a colina é fixa (gaussiana), só altura e abertura mudam

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `altura` | 2.0 | u | altura h do topo |
| `abertura` | 1.0 | u | largura σ da colina |
| `extensao` | 3.0 | u | meia largura da região |
| `n_niveis` | 5 | n | curvas de nível |
| `raio_ponto` | 1.4 | u | distância de P ao eixo da colina |
| `movimento` | 0 | 0/1 | 1 = animação em loop (use animar.py ou a ponte com o Manim) |
| `fase` | 0.0 | 0-1 | fase do loop; fase=1 repete o quadro da fase 0 (loop perfeito) |

**Integração:** `png_seq_alpha` · custo 1.03 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `percurso` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 1.03 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- gradiente_colina --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("gradiente_colina").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/gradiente_colina.json`

### `haste_carregada` — Haste carregada

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Haste fina de vidro azulado ao longo de Y, com eixo de simetria (mediatriz) em X, e cargas espaçadas ao longo dela. Eixo de simetria opcional (tracejado neutro).

![Haste carregada](previews/haste_carregada.png)

**Como se lê:** Bastão de vidro fino com uma fileira de pontos azuis e, opcionalmente, o eixo tracejado cruzando-o ao meio. Lê-se como 'carga distribuída numa linha reta finita'.

**Usar quando**
- campo elétrico de uma haste finita carregada (integração de dq, ponto na mediatriz, limite de haste longa)
- momento de inércia de uma haste (com_cargas=0), com o eixo de simetria desenhado
- contraste com o anel (linha curva) e com o disco (superfície)
- corrente numa haste: cargas deslizando ao longo dela (cargas_moveis=1)

**Não usar quando**
- a haste deve ser infinita: o objeto é finito (para linha infinita use gaussiana_cilindrica com a fonte da cena)
- a espessura da haste importa para o problema

**Limitações**
- o campo e a gaussiana não são desenhados: o ciano é reservado ao campo (animação 2D/Manim)
- em contexto de mecânica (com_cargas=0) o azul de 'fonte física' vem da gramática de Eletromagnetismo; a gramática de cor da Mecânica não foi verificada aqui
- espessura/raio do corpo exagerados em relação ao ideal (o corpo de vidro é visível); as cargas ficam dentro dele
- haste ao longo de Y fixa; em outra orientação, girar a câmera
- as cargas têm espaçamento quase regular (jitter 0,12)
- o movimento não codifica a corrente: a convenção (corrente convencional ou elétrons, que vão ao contrário) e o sinal vão por seta e rótulo no Manim; o movimento é didático, não em escala
- com cargas_moveis=1 as cargas estáticas (com_cargas) são substituídas pelas móveis

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `comprimento` | 4.0 | u | comprimento da haste (eixo Y) |
| `raio` | 0.1 | u | raio da haste (visual) |
| `n_cargas` | 36 | n | número de cargas ao longo da haste |
| `com_cargas` | 1 | 0/1 | 1 = cargas pontuais (campo elétrico); 0 = só o corpo de vidro (ex.: momento de inércia) |
| `eixo` | 0 | 0/1 | 1 = eixo de simetria tracejado em cor neutra |
| `comprimento_eixo` | 3.0 | u | comprimento do eixo de simetria, se desenhado |
| `semente` | 7 | n | semente do sorteio/jitter (mesma semente = mesma distribuição) |
| `cargas_moveis` | 0 | 0/1 | 1 = cargas em movimento (animação em loop); use com animar.py ou a ponte com o Manim |
| `fase` | 0.0 | 0-1 | fase do movimento; fase=1 repete o quadro da fase 0 (loop perfeito) |
| `espaco_cargas` | 0.45 | u | distância entre cargas ao longo da haste |
| `tamanho_carga_movel` | 0.07 | u | raio de cada carga móvel |

**Integração:** `png_seq_alpha` · custo 0.62 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `deslizamento` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 0.62 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- haste_carregada --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("haste_carregada").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/haste_carregada.json`

### `lente_delgada` — Lente delgada (biconvexa ou biconcava)

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Lente de vidro azul-claro de revolução em torno do eixo óptico X, com faces esféricas de raios `raio1` e `raio2`. `forma` = biconvexa (converge) ou biconcava (diverge). Eixo óptico tracejado neutro e os dois focos (marcas neutras) pela equação dos fabricantes de lentes, 1/f = (n−1)(1/R₁+1/R₂).

![Lente delgada (biconvexa ou biconcava)](previews/lente_delgada.png)

**Como se lê:** Lente de vidro com o eixo tracejado e duas marcas nos focos: lê-se como 'lente delgada com seus focos'. A biconcava tem as marcas nos focos virtuais, do mesmo lado.

**Usar quando**
- lente delgada: foco, formação de imagem, equação de Gauss das lentes
- contraste converge/diverge (biconvexa × biconcava)
- ponto de partida para os raios desenhados no Manim

**Não usar quando**
- lentes espessas ou aberração (esta é delgada, de faces esféricas ideais)
- espelhos (não há espelhos no arsenal)

**Limitações**
- só o objeto: raios, frentes de onda, ângulos e a figura de interferência são do Manim
- vidro translúcido azul-claro (padrão do arsenal): não representa cor, dispersão nem índice de refração
- foco pela equação das lentes delgadas, não por traçado de raios
- o raio de curvatura deve ser maior que o semi-diâmetro
- vista lateral (azimute -78): o perfil da lente aparece de lado, com o eixo óptico na horizontal, como nos esquemas de óptica

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `forma` | biconvexa | texto | biconvexa ou biconcava |
| `diametro` | 2.4 | u | diâmetro da lente |
| `raio1` | 2.2 | u | raio de curvatura da face da frente |
| `raio2` | 2.2 | u | raio de curvatura da face de trás |
| `espessura_borda` | 0.08 | u | espessura na borda (convexa) ou no centro (côncava) |
| `indice` | 1.5 | n | índice de refração (só para posicionar os focos) |
| `focos` | 1 | 0/1 | 1 = marcas nos focos |
| `eixo` | 1 | 0/1 | 1 = eixo óptico tracejado |

**Integração:** `png_seq_alpha` · custo 0.65 s/frame (1080p, Eevee)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- lente_delgada --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("lente_delgada").mobject(altura=5)   # estático: um quadro PNG com alpha
```

Ficha: `solidos/lente_delgada.json`

### `massa_mola` — Sistema massa-mola horizontal (MHS)

**Status:** estudo · Tecnicamente validado (render 960x540); aparência aguardando aprovação do usuário.

Bloco de vidro azul preso a uma mola helicoidal (fio azul) na parede, sobre um trilho, com três marcas violeta tracejadas: equilíbrio e os extremos ±A. Com `movimento=1` o bloco oscila x = x_eq + A cos(2π fase) e a mola se comprime e se estica.

![Sistema massa-mola horizontal (MHS)](previews/massa_mola.png)

**Como se lê:** Bloco entre duas marcas pontilhadas, com a mola mudando de comprimento: lê-se como 'oscilador harmônico simples'.

**Usar quando**
- MHS: período, amplitude e a posição de equilíbrio
- energia no oscilador: a energia da mola é do Manim
- contraste com o pêndulo e com as oscilações amortecidas (o amortecimento é do Manim)

**Não usar quando**
- movimento vertical com gravidade (a mola é horizontal, sem atrito)
- oscilações amortecidas ou forçadas

**Limitações**
- só o objeto em movimento: velocidades, energia, gráficos x(t) e as fórmulas são do Manim
- movimento didático calculado por fórmula (não é uma simulação física de verdade)
- a mola é uma hélice de passo uniforme com espiras que mudam de espaçamento: a espessura do fio é visual
- sem atrito: a amplitude é constante

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `amplitude` | 1.0 | u | amplitude A |
| `equilibrio` | 0.5 | u | posição de equilíbrio do centro do bloco |
| `parede` | -3.0 | u | posição da parede |
| `lado` | 0.9 | u | lado do bloco |
| `n_espiras` | 12 | n | espiras da mola |
| `raio_mola` | 0.26 | u | raio da hélice |
| `marcas` | 1 | 0/1 | 1 = marcas do equilíbrio e dos extremos |
| `movimento` | 0 | 0/1 | 1 = animação (use animar.py ou a ponte com o Manim) |
| `fase` | 0.0 | 0-1 | fase da animação |

**Integração:** `png_seq_alpha` · custo 0.87 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `oscilacao` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 0.87 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- massa_mola --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("massa_mola").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/massa_mola.json`

### `onda_corda` — Onda numa corda (progressiva e estacionária)

**Status:** estudo · Tecnicamente validado (render 960x540); aparência aguardando aprovação do usuário.

Corda como curva azul-claro y(x, t) com contas neutras que só sobem e descem. `tipo` = progressiva (y = A sen(kx − 2π fase), anda para +X) ou estacionaria (y = A sen(kx) cos(2π fase), extremos fixos, com nós em violeta e envoltória pontilhada violeta).

![Onda numa corda (progressiva e estacionária)](previews/onda_corda.png)

**Como se lê:** Onda com contas brancas que oscilam na vertical enquanto a forma anda (progressiva) ou fica parada com nós (estacionária).

**Usar quando**
- ondas transversais: comprimento de onda, amplitude, frequência e velocidade (v = λf, no Manim)
- partículas oscilando na vertical enquanto a onda se propaga
- ondas estacionárias: nós, ventres e harmônicos (n_ondas = número de comprimentos de onda)

**Não usar quando**
- ondas longitudinais (som): aqui só transversais
- superposição de pulsos ou reflexões: a onda é senoidal e infinita

**Limitações**
- só o objeto em movimento: velocidades, energia, gráficos x(t) e as fórmulas são do Manim
- movimento didático calculado por fórmula (não é uma simulação física de verdade)
- para a estacionária `n_ondas` deve ser inteiro (nós nas pontas)
- a onda progressiva é senoidal e preenche toda a corda: não há pulso nem reflexão

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `tipo` | progressiva | texto | progressiva ou estacionaria |
| `comprimento` | 8.0 | u | comprimento da corda |
| `n_ondas` | 2 | n | número de comprimentos de onda na corda |
| `amplitude` | 0.9 | u | amplitude A |
| `n_contas` | 9 | n | contas indicadoras |
| `nos` | 1 | 0/1 | 1 = nós marcados (só estacionária) |
| `movimento` | 0 | 0/1 | 1 = animação (use animar.py ou a ponte com o Manim) |
| `fase` | 0.0 | 0-1 | fase da animação |

**Integração:** `png_seq_alpha` · custo 0.39 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `onda` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 0.39 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- onda_corda --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("onda_corda").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/onda_corda.json`

### `ondas_duas_fontes` — Ondas na superfície com duas fontes (interferência)

**Status:** estudo · Tecnicamente validado (render 960x540); aparência aguardando aprovação do usuário.

Superfície de vidro azul com malha azul-claro e duas fontes neutras (esferas brancas) que emitem ondas circulares coerentes; a altura é a soma das duas, amortecida até zero na borda. Com `movimento=1` as ondas se propagam (fase = um período).

![Ondas na superfície com duas fontes (interferência)](previews/ondas_duas_fontes.png)

**Como se lê:** Superfície ondulada com dois pontos brancos e um padrão de cristas e vales cruzados: lê-se como 'interferência de duas fontes'.

**Usar quando**
- interferência construtiva e destrutiva de duas fontes coerentes (cuba de ondas)
- experimento de Young em ondas na água, antes da luz
- mostrar a diferença de caminho: as linhas nodais vêm da soma das ondas

**Não usar quando**
- uma única fonte ou ondas estacionárias (use onda_corda)
- fontes incoerentes

**Limitações**
- só o objeto em movimento: velocidades, energia, gráficos x(t) e as fórmulas são do Manim
- movimento didático calculado por fórmula (não é uma simulação física de verdade)
- a amplitude cai como 1/√(1 + 0,5 r) e é zerada na borda (apenas visual)
- malha de 64×64: dá um aspecto de grade fina e as cristas são lisas, mas o detalhe fino some a distância

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `extensao` | 5.0 | u | meia largura da superfície |
| `separacao` | 3.0 | u | distância entre as fontes |
| `comprimento_onda` | 1.8 | u | comprimento de onda |
| `amplitude` | 0.42 | u | amplitude de cada onda |
| `resolucao` | 64 | n | divisões por lado da malha |
| `movimento` | 0 | 0/1 | 1 = animação (use animar.py ou a ponte com o Manim) |
| `fase` | 0.0 | 0-1 | fase da animação |

**Integração:** `png_seq_alpha` · custo 1.65 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `onda` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 1.65 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- ondas_duas_fontes --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("ondas_duas_fontes").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/ondas_duas_fontes.json`

### `orbita_kepleriana` — Órbita kepleriana com setores de áreas iguais

**Status:** estudo · Corpo central ajustado com degradê a pedido do usuário; aguardando nova aprovação da aparência.

Órbita elíptica num plano: corpo central branco no foco, corpo orbitante azul-claro, trajetória tracejada violeta, vetor posição e `setores` fatias violeta translúcidas varridas em intervalos de tempo iguais (fração `fracao_setor` do período). Com `movimento=1` o corpo percorre a órbita (fase = um período, velocidade de Kepler).

![Órbita kepleriana com setores de áreas iguais](previews/orbita_kepleriana.png)

**Como se lê:** Elipse tracejada com o corpo central num foco e fatias violeta: a do periélio é larga e curta, a do afélio fina e longa, mas de mesma área. Lê-se como 'áreas iguais em tempos iguais'.

**Usar quando**
- leis de Kepler: 1ª (elipse com o Sol no foco), 2ª (áreas iguais) e 3ª (T² ∝ a³ no Manim)
- energia orbital e velocidade maior no periélio (a velocidade é do Manim)
- órbitas circulares (excentricidade 0) como caso particular

**Não usar quando**
- problemas de dois corpos com massas comparáveis (o centro é fixo)
- órbitas abertas (parábola, hipérbole): só elipses (0 ≤ e < 1)
- precessão ou perturbações

**Limitações**
- o corpo central é fixo no foco: não há movimento do centro de massa
- o plano da órbita é XY; a câmera padrão olha de cima (elevação 34)
- a equação de Kepler é resolvida por Newton para cada quadro: a velocidade é a real (variável) ao longo do loop
- o setor é uma fatia plana colorida com bordas retas, aproximando o setor elíptico com 24 pontos

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `semi_eixo` | 2.6 | u | semi-eixo maior a |
| `excentricidade` | 0.55 | 0-1 | excentricidade e (0 = círculo) |
| `setores` | 2 | n | número de setores de áreas iguais (distribuídos em fase) |
| `fracao_setor` | 0.125 | 0-1 | fração do período varrida por cada setor |
| `vetor` | 1 | 0/1 | 1 = vetor posição (do centro ao corpo) |
| `movimento` | 0 | 0/1 | 1 = animação em loop (use animar.py ou a ponte com o Manim) |
| `fase` | 0.0 | 0-1 | fase do loop; fase=1 repete o quadro da fase 0 (loop perfeito) |

**Integração:** `png_seq_alpha` · custo 0.67 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `orbita` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 0.67 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- orbita_kepleriana --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("orbita_kepleriana").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/orbita_kepleriana.json`

### `pendulo_simples` — Pêndulo simples (pequenas oscilações)

**Status:** estudo · Tecnicamente validado (render 960x540); aparência aguardando aprovação do usuário.

Pêndulo no plano XZ: suporte de vidro, fio azul-claro, massa esférica com degradê, arco tracejado violeta entre ±θ0 e a vertical de referência. Com `movimento=1` θ(t) = θ0 cos(2π fase) (aproximação de pequenas oscilações, MHS).

![Pêndulo simples (pequenas oscilações)](previews/pendulo_simples.png)

**Como se lê:** Massa balançando num fio, com o arco pontilhado do percurso e a vertical: lê-se como 'pêndulo'.

**Usar quando**
- pêndulo simples e a aproximação de pequenos ângulos (T = 2π√(L/g))
- contraste com massa-mola (também MHS)
- energia: troca entre potencial e cinética (as setas e gráficos são do Manim)

**Não usar quando**
- grandes amplitudes (o movimento real não é senoidal)
- pêndulo físico ou duplo

**Limitações**
- só o objeto em movimento: velocidades, energia, gráficos x(t) e as fórmulas são do Manim
- movimento didático calculado por fórmula (não é uma simulação física de verdade)
- θ(t) é cosseno puro (MHS): para amplitudes grandes (>30°) a diferença do pêndulo real é visível
- fio inextensível e sem atrito

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `comprimento` | 3.0 | u | comprimento L do fio |
| `amplitude_graus` | 24.0 | graus | amplitude angular θ0 |
| `raio_corpo` | 0.24 | u | raio da massa |
| `arco` | 1 | 0/1 | 1 = arco e vertical de referência |
| `movimento` | 0 | 0/1 | 1 = animação (use animar.py ou a ponte com o Manim) |
| `fase` | 0.0 | 0-1 | fase da animação |

**Integração:** `png_seq_alpha` · custo 0.53 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `oscilacao` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 0.53 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- pendulo_simples --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("pendulo_simples").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/pendulo_simples.json`

### `placa_infinita_carregada` — Placa infinita carregada (plano com cargas na superfície)

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Folha de vidro azulado muito fina (normal ao longo de X) com grade sutil e cargas pontuais distribuídas sobre o plano. A opacidade da folha, a grade e o tamanho das cargas se dissolvem com a distância ao centro, para sugerir que o plano continua além do quadro. Fisicamente finita (14 x 6,5 por padrão).

![Placa infinita carregada (plano com cargas na superfície)](previews/placa_infinita_carregada.png)

**Como se lê:** Plano azul translúcido de grade discreta, cheio de pontos e sumindo nas bordas. Cargas próximas da câmera são azul-claro (#7FB2FF); as distantes, azul (#267BFF). Lê-se como 'plano contínuo de carga, sem limites visíveis'.

**Usar quando**
- simetria planar: plano infinito com densidade superficial de carga uniforme (isolante fino ou plano de carga)
- mostrar que o plano é ilimitado e que o campo não depende da distância (par com os sólidos de simetria cilíndrica e esférica)
- contraste com as simetrias cilíndrica e esférica na mesma unidade (casca, maciço, plano)
- corrente superficial: cargas deslizando sobre o plano na direção Y (cargas_moveis=1)

**Não usar quando**
- o vídeo precisa mostrar as bordas ou efeitos de borda: a placa aqui se dissolve de propósito
- placa condutora de espessura finita (carga em duas faces) ou capacitor de duas placas: este sólido é um único plano
- placa espessa isolante com densidade volumétrica de carga: aqui as cargas estão só no plano

**Limitações**
- o plano é fisicamente finito e o 'infinito' é só visual (dissolve nas bordas); se o enquadramento incluir as bordas, o efeito se perde
- cargas só sobre o plano x=0; a normal do plano é fixa em X
- a visualização depende do ângulo: muito de frente (olhando ao longo de X) a placa vira um retângulo chapado; o padrão usa azimute -40
- não desenha campo elétrico: o ciano é reservado ao campo e fica para a animação 2D/Manim
- o movimento não codifica a corrente: a convenção (corrente convencional ou elétrons, que vão ao contrário) e o sinal vão por seta e rótulo no Manim; o movimento é didático, não em escala
- as cargas somem por escala nas bordas (como o fade da placa); a direção do deslizamento é fixa em Y

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `largura` | 14.0 | u | largura da folha (eixo Y) |
| `altura` | 6.5 | u | altura da folha (eixo Z) |
| `espessura` | 0.05 | u | espessura da folha (eixo X) |
| `n_cargas` | 220 | n | número de cargas desejado (pode sair menos se a distância mínima não couber) |
| `dist_min` | 0.5 | u | distância mínima entre cargas |
| `tamanho_carga` | 0.06 | u | raio de cada esfera de carga |
| `semente` | 7 | n | semente do sorteio (mesma semente = mesma distribuição) |
| `grade` | 1 | 0/1 | 1 = grade sutil sobre o plano; 0 = só o vidro |
| `fade_inicio` | 0.5 | 0-1 | fração da meia largura/altura onde a folha começa a se dissolver |
| `cargas_moveis` | 0 | 0/1 | 1 = cargas em movimento (animação em loop); use com animar.py ou a ponte com o Manim |
| `fase` | 0.0 | 0-1 | fase do movimento; fase=1 repete o quadro da fase 0 (loop perfeito) |
| `periodos` | 4 | n | o padrão de cargas se repete esta vez ao longo da largura; o loop desloca 1 período |

**Integração:** `png_seq_alpha` · custo 1.31 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `deslizamento` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 1.3 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- placa_infinita_carregada --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("placa_infinita_carregada").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/placa_infinita_carregada.json`

### `poco_gravitacional` — Poço gravitacional (potencial)

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Superfície de vidro azulado de revolução z = −P·s/√(r²+s²) com anéis e raios em azul-claro e uma bola azul-claro em órbita circular sobre ela. Representa o poço de potencial gravitacional (o mais fundo no centro).

![Poço gravitacional (potencial)](previews/poco_gravitacional.png)

**Como se lê:** Funil de vidro com grade e uma bola circulando: lê-se como 'potencial gravitacional: a bola orbita no poço'.

**Usar quando**
- potencial gravitacional e energia potencial negativa (o poço é mais profundo perto do corpo)
- velocidade de escape: sair do poço (a escala de energia é do Manim)
- satélites e órbitas circulares como bolas no poço (analogia)

**Não usar quando**
- curvatura do espaço-tempo da relatividade geral (é só uma analogia de potencial)
- órbitas elípticas (use orbita_kepleriana)

**Limitações**
- é uma analogia visual: a bola gira sobre uma superfície, mas a força real é central no plano, não gravidade vertical sobre o funil
- a profundidade do poço é um parâmetro visual, não uma escala de energia
- o poço é suavizado pelo raio do núcleo `raio_nucleo` (evita a singularidade em r = 0)
- só a órbita circular é animada

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `raio_max` | 3.2 | u | raio da borda do poço |
| `profundidade` | 1.8 | u | profundidade no centro |
| `raio_nucleo` | 0.9 | u | raio de suavização do centro |
| `bola` | 1 | 0/1 | 1 = bola orbitando sobre a superfície |
| `raio_bola` | 1.9 | u | raio da órbita circular da bola |
| `movimento` | 0 | 0/1 | 1 = animação em loop (use animar.py ou a ponte com o Manim) |
| `fase` | 0.0 | 0-1 | fase do loop; fase=1 repete o quadro da fase 0 (loop perfeito) |

**Integração:** `png_seq_alpha` · custo 1.15 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `orbita` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 1.15 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- poco_gravitacional --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("poco_gravitacional").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/poco_gravitacional.json`

### `prisma_triangular` — Prisma triangular

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Prisma de vidro azul-claro de seção triangular isósceles (ângulo de ápice `angulo_apice`), com a seção no plano XY e extrusão ao longo de Z, apoiado na base. As nove arestas em azul-claro.

![Prisma triangular](previews/prisma_triangular.png)

**Como se lê:** Prisma de vidro com arestas claras: lê-se como 'prisma óptico'. A direção dos raios, o desvio e a dispersão são do Manim.

**Usar quando**
- refração em um prisma, ângulo de desvio mínimo
- dispersão (as cores vêm do Manim)
- reflexão interna total

**Não usar quando**
- lentes (use lente_delgada)
- prismas não triangulares

**Limitações**
- só o objeto: raios, frentes de onda, ângulos e a figura de interferência são do Manim
- vidro translúcido azul-claro (padrão do arsenal): não representa cor, dispersão nem índice de refração
- os raios entrariam no plano da seção (XY); a extrusão em Z é só para dar volume

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `angulo_apice` | 60.0 | graus | ângulo de ápice |
| `base` | 2.0 | u | comprimento da base |
| `comprimento` | 2.0 | u | comprimento da extrusão (eixo Z) |
| `eixo` | 0 | 0/1 | 1 = eixo tracejado neutro ao longo de X |

**Integração:** `png_seq_alpha` · custo 0.76 s/frame (1080p, Eevee)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- prisma_triangular --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("prisma_triangular").mobject(altura=5)   # estático: um quadro PNG com alpha
```

Ficha: `solidos/prisma_triangular.json`

### `solenoide_corrente` — Solenoide (hélice de fio)

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Solenoide: fio azul (#267BFF) enrolado em hélice de passo constante ao longo do eixo X. Terminais retos nas pontas. Núcleo de vidro opcional e eixo de simetria opcional.

![Solenoide (hélice de fio)](previews/solenoide_corrente.png)

**Como se lê:** Hélice azul luminosa de espiras abertas em volta de um núcleo de vidro translúcido: lê-se como 'fio enrolado'. Sem núcleo (nucleo=0) o interior fica visível e vazio.

**Usar quando**
- campo B no interior de um solenoide longo (n espiras por comprimento, retângulo amperiano atravessando a parede)
- mostrar a densidade de espiras n e o efeito de enrolar o fio
- contraste com o toroide (enrolamento fechado) e com o fio reto
- corrente seguindo as espiras: cargas em movimento ao longo da hélice (cargas_moveis=1, animar.py)
- corrente seguindo as espiras: cargas em movimento ao longo da hélice (cargas_moveis=1)

**Não usar quando**
- o enrolamento é fechado em anel (use toroide_corrente)
- uma única espira (use anel_carregado como aro, ou espira no 2D)

**Limitações**
- só a fonte física (fio/enrolamento, azul): o campo B (ciano) e o sentido da corrente são desenhados no 2D/Manim
- sem noção de sentido: a hélice tem um sentido de enrolamento, mas ele não representa a corrente de forma legível; indicar I por rótulo/seta no Manim
- hélice ideal: espiras muito próximas aproximam o solenoide infinito, mas a hélice é finita (4 de comprimento)
- o fio é grosso para ser visível; o passo e o número de espiras são estilizados (12 por padrão)
- o sentido do movimento não codifica a corrente: a convenção (corrente convencional ou elétrons, que vão ao contrário) e o sinal vão por seta e rótulo no Manim
- o movimento não codifica a corrente: a convenção (corrente convencional ou elétrons, que vão ao contrário) e o sinal vão por seta e rótulo no Manim; o movimento é didático, não em escala

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `raio` | 1.0 | u | raio do solenoide |
| `comprimento` | 4.0 | u | comprimento ao longo do eixo X |
| `n_espiras` | 12 | n | número de espiras |
| `raio_fio` | 0.035 | u | raio do fio (visual) |
| `nucleo` | 1 | 0/1 | 1 = núcleo de vidro dentro (só visual, dá corpo ao solenoide; não representa um material magnético); 0 = só o fio |
| `eixo` | 0 | 0/1 | 1 = eixo de simetria tracejado neutro |
| `comprimento_eixo` | 6.0 | u | comprimento do eixo, se desenhado |
| `terminal` | 0.7 | u | comprimento dos terminais retos de fio nas duas pontas |
| `cargas_moveis` | 0 | 0/1 | 1 = cargas azul-claro deslizando ao longo do fio (corrente); o movimento é didático, não em escala |
| `fase` | 0.0 | 0-1 | fase do movimento: desloca as cargas de 0 a 1 espaçamento; fase=1 repete o quadro da fase 0 (loop perfeito) |
| `espaco_cargas` | 0.8 | u | distância entre cargas consecutivas ao longo do fio |
| `tamanho_carga_movel` | 0.08 | u | raio de cada carga móvel |

**Integração:** `png_seq_alpha` · custo 0.53 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `deslizamento` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 0.55 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- solenoide_corrente --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("solenoide_corrente").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/solenoide_corrente.json`

### `solido_revolucao_arruela` — Sólido de revolução: método das arruelas

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Sólido de vidro azulado gerado pela rotação, em torno do eixo X, da região entre y = √x e y = x² (as duas curvas em azul-claro; o corpo fica oco por dentro), com o eixo tracejado e a fatia elementar (uma arruela, de raio externo f e interno g, espessura dx) em violeta com arestas tracejadas. Com movimento, a arruela varre o sólido e volta.

![Sólido de revolução: método das arruelas](previews/solido_revolucao_arruela.png)

**Como se lê:** Corpo de vidro azul em forma de taça aberta, com uma arruela violeta de arestas tracejadas. Lê-se como 'o volume é a soma de arruelas: π (f² − g²) dx'.

**Usar quando**
- volume por arruelas: V = ∫ π (f(x)² − g(x)²) dx (região entre duas curvas girada em torno do eixo x)
- mostrar a arruela elementar varrendo o sólido (movimento=1)
- contraste com o método dos discos (sem furo)

**Não usar quando**
- a região vai até o eixo (use solido_revolucao_disco)
- eixo de rotação deslocado ou outras duas curvas: aqui a região é fixa (√x e x²)

**Limitações**
- a fatia mostra UM elemento dx exagerado, não a soma de Riemann: o limite dx→0 e a integral ficam para o Manim
- o violeta da fatia segue a gramática do arsenal (construção matemática, translúcida, nunca sólida): ela fica dentro do vidro azul e perde contraste em ângulos muito rasantes
- o sólido é vidro translúcido (culling de faces de trás já embutido); o interior de uma arruela só aparece pelo lado aberto
- a gramática de cor de Cálculo segue o padrão do arsenal (estilo.json)
- região fixa entre y = √x e y = x² normalizada em [0, comprimento]

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `comprimento` | 4.0 | u | extensão ao longo do eixo X |
| `raio_max` | 1.6 | u | raio onde as duas curvas se encontram (em x = comprimento) |
| `fatia` | 1 | 0/1 | 1 = desenha a fatia elementar (violeta, arestas tracejadas); 0 = só o sólido |
| `posicao_fatia` | 0.5 | 0-1 | posição da fatia ao longo do sólido (fração da extensão); ignorada com movimento=1 |
| `espessura_fatia` | 0.14 | u | espessura dx da fatia (exagerada para ser visível) |
| `perfil_visivel` | 1 | 0/1 | 1 = curva geratriz em azul-claro |
| `eixo` | 1 | 0/1 | 1 = eixo de revolução tracejado em cor neutra |
| `movimento` | 0 | 0/1 | 1 = a fatia varre o sólido em vaivém suave (use animar.py ou a ponte com o Manim) |
| `fase` | 0.0 | 0-1 | fase do vaivém; fase=1 repete o quadro da fase 0 (loop perfeito) |

**Integração:** `png_seq_alpha` · custo 0.91 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `varredura` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 0.91 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- solido_revolucao_arruela --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("solido_revolucao_arruela").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/solido_revolucao_arruela.json`

### `solido_revolucao_cascas` — Sólido de revolução: método das cascas

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Sólido de vidro azulado (uma tigela) gerado pela rotação da região sob y = H (1 − (x/a)²) em torno do eixo Z (vertical), com a curva geratriz em azul-claro, o eixo tracejado e a fatia elementar (uma casca cilíndrica de raio r, altura f(r) e espessura dr) em violeta com arestas tracejadas. Com movimento, a casca cresce de dentro para fora e volta.

![Sólido de revolução: método das cascas](previews/solido_revolucao_cascas.png)

**Como se lê:** Tigela de vidro azul com uma casca cilíndrica violeta de arestas tracejadas, concêntrica ao eixo vertical. Lê-se como 'o volume é a soma de cascas: 2π r f(r) dr'.

**Usar quando**
- volume por cascas: V = ∫ 2π x f(x) dx (região sob a curva girada em torno do eixo y)
- mostrar a casca elementar varrendo o sólido (movimento=1)
- contraste com discos e arruelas (fatias perpendiculares ao eixo)

**Não usar quando**
- rotação em torno do eixo x com a região sob a curva (use solido_revolucao_disco)
- outra curva ou eixo deslocado: a parábola invertida é fixa

**Limitações**
- a fatia mostra UM elemento dx exagerado, não a soma de Riemann: o limite dx→0 e a integral ficam para o Manim
- o violeta da fatia segue a gramática do arsenal (construção matemática, translúcida, nunca sólida): ela fica dentro do vidro azul e perde contraste em ângulos muito rasantes
- o sólido é vidro translúcido (culling de faces de trás já embutido); o interior de uma arruela só aparece pelo lado aberto
- a gramática de cor de Cálculo segue o padrão do arsenal (estilo.json)
- perfil fixo: parábola invertida y = H (1 − (x/a)²) em [0, a]
- o eixo de rotação é Z (vertical), diferente dos outros dois métodos (eixo X)

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `raio_base` | 2.0 | u | raio a da base da tigela |
| `altura` | 3.0 | u | altura H da tigela (no eixo) |
| `fatia` | 1 | 0/1 | 1 = desenha a fatia elementar (violeta, arestas tracejadas); 0 = só o sólido |
| `posicao_fatia` | 0.5 | 0-1 | posição da fatia ao longo do sólido (fração da extensão); ignorada com movimento=1 |
| `espessura_fatia` | 0.14 | u | espessura dx da fatia (exagerada para ser visível) |
| `perfil_visivel` | 1 | 0/1 | 1 = curva geratriz em azul-claro |
| `eixo` | 1 | 0/1 | 1 = eixo de revolução tracejado em cor neutra |
| `movimento` | 0 | 0/1 | 1 = a fatia varre o sólido em vaivém suave (use animar.py ou a ponte com o Manim) |
| `fase` | 0.0 | 0-1 | fase do vaivém; fase=1 repete o quadro da fase 0 (loop perfeito) |

**Integração:** `png_seq_alpha` · custo 0.96 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `varredura` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 0.96 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- solido_revolucao_cascas --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("solido_revolucao_cascas").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/solido_revolucao_cascas.json`

### `solido_revolucao_disco` — Sólido de revolução: método dos discos

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Sólido de vidro azulado gerado pela rotação de uma curva y = f(x) em torno do eixo X (4 perfis: raiz, parábola, cone, elipsoide), com a curva geratriz em azul-claro, o eixo tracejado e a fatia elementar (um disco de espessura dx) em violeta com arestas tracejadas. Com movimento, o disco varre o sólido de uma ponta à outra e volta.

![Sólido de revolução: método dos discos](previews/solido_revolucao_disco.png)

**Como se lê:** Corpo de vidro azul atravessado por um disco violeta de arestas tracejadas. Lê-se como 'o volume é a soma de discos de raio f(x) e espessura dx'.

**Usar quando**
- volume por discos: V = ∫ π f(x)² dx (região sob a curva girada em torno do eixo x)
- mostrar a fatia elementar varrendo o sólido (movimento=1)
- contraste com arruelas (região entre duas curvas) e cascas (eixo vertical)

**Não usar quando**
- a região é limitada por duas curvas (use solido_revolucao_arruela)
- o eixo de rotação é vertical e as fatias são paralelas a ele (use solido_revolucao_cascas)
- eixo de rotação deslocado (ex.: y = −1): só o eixo X é suportado

**Limitações**
- a fatia mostra UM elemento dx exagerado, não a soma de Riemann: o limite dx→0 e a integral ficam para o Manim
- o violeta da fatia segue a gramática do arsenal (construção matemática, translúcida, nunca sólida): ela fica dentro do vidro azul e perde contraste em ângulos muito rasantes
- o sólido é vidro translúcido (culling de faces de trás já embutido); o interior de uma arruela só aparece pelo lado aberto
- a gramática de cor de Cálculo segue o padrão do arsenal (estilo.json)
- só 4 perfis normalizados (parâmetro perfil); outra curva exige alterar PERFIS em revolucao.py

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `perfil` | raiz | texto | raiz (y=√x), parabola (y=x²), cone (y=x) ou elipsoide (semi-elipse) |
| `comprimento` | 4.0 | u | extensão ao longo do eixo X |
| `raio_max` | 1.6 | u | raio máximo do sólido |
| `fatia` | 1 | 0/1 | 1 = desenha a fatia elementar (violeta, arestas tracejadas); 0 = só o sólido |
| `posicao_fatia` | 0.5 | 0-1 | posição da fatia ao longo do sólido (fração da extensão); ignorada com movimento=1 |
| `espessura_fatia` | 0.14 | u | espessura dx da fatia (exagerada para ser visível) |
| `perfil_visivel` | 1 | 0/1 | 1 = curva geratriz em azul-claro |
| `eixo` | 1 | 0/1 | 1 = eixo de revolução tracejado em cor neutra |
| `movimento` | 0 | 0/1 | 1 = a fatia varre o sólido em vaivém suave (use animar.py ou a ponte com o Manim) |
| `fase` | 0.0 | 0-1 | fase do vaivém; fase=1 repete o quadro da fase 0 (loop perfeito) |

**Integração:** `png_seq_alpha` · custo 0.86 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `varredura` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 0.86 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- solido_revolucao_disco --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("solido_revolucao_disco").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/solido_revolucao_disco.json`

### `superficie_parametrizada` — Superfície parametrizada com remendo dS

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Superfície de vidro azul (`tipo`: onda, sela ou esfera) com as curvas coordenadas u = cte e v = cte em azul-claro, um remendo elementar dS em violeta tracejado, os vetores tangentes r_u e r_v (brancos) e a normal n̂ = r_u × r_v (azul) no ponto (`u0`, `v0`). Com `movimento=1` o ponto percorre uma pequena volta.

![Superfície parametrizada com remendo dS](previews/superficie_parametrizada.png)

**Como se lê:** Superfície de vidro com malha, um quadrilátero violeta e três setas (duas brancas no plano tangente, uma azul normal). Lê-se como 'parametrização: elemento de área e orientação'.

**Usar quando**
- superfícies parametrizadas: vetores tangentes, elemento de área |r_u × r_v| du dv e orientação (Cálculo IV 11.6)
- integral de superfície e fluxo (o remendo é o dS)
- contraste entre onda, sela e esfera

**Não usar quando**
- superfícies de revolução com fatias (use solido_revolucao_*)
- superfícies fechadas com gaussianas (use as gaussianas)

**Limitações**
- a gramática de cor segue o padrão do arsenal: campo vetorial = ciano (reservado ao campo), normal n̂ = azul, tangentes = branco, construções (remendo, contorno) = violeta, nunca sólidas
- só o objeto geométrico: integrais, fórmulas e o sinal da circulação/fluxo são do Manim
- superfície fina de vidro com Solidify (espessura 0,03): vista de lado o vidro quase some
- sobre a esfera os vetores tangentes e a normal dependem do ponto: perto dos polos a parametrização é degenerada (domínio cortado em 5%)
- o remendo é plano (quadrilátero); a curvatura dentro dele não aparece

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `tipo` | onda | texto | onda, sela ou esfera |
| `u0` | 0.5 | 0-1 | posição de u no domínio |
| `v0` | 0.5 | 0-1 | posição de v no domínio |
| `tamanho_remendo` | 1.0 | x | tamanho relativo do remendo dS |
| `vetores` | 1 | 0/1 | 1 = r_u, r_v e n̂ |
| `linhas` | 1 | 0/1 | 1 = curvas coordenadas |
| `movimento` | 0 | 0/1 | 1 = animação em loop (use animar.py ou a ponte com o Manim) |
| `fase` | 0.0 | 0-1 | fase do loop; fase=1 repete o quadro da fase 0 (loop perfeito) |

**Integração:** `png_seq_alpha` · custo 1.06 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `percurso` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 1.06 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- superficie_parametrizada --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("superficie_parametrizada").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/superficie_parametrizada.json`

### `teorema_stokes` — Teorema de Stokes (hemisfério e contorno)

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Hemisfério de vidro azul (a superfície S) com o contorno ∂S no plano z = 0 em violeta contínuo, normais n̂ para fora (azuis), setas do campo rotacional (ciano) e uma seta branca percorrendo ∂S no sentido anti-horário (regra da mão direita com n̂ para cima). Com `movimento=1` a seta percorre o contorno.

![Teorema de Stokes (hemisfério e contorno)](previews/teorema_stokes.png)

**Como se lê:** Cúpula de vidro com anel violeta na base, normais azuis para fora e setas ciano girando: lê-se como 'circulação no contorno = fluxo do rotacional pela superfície'.

**Usar quando**
- teorema de Stokes: ∮ F·dr = ∬ (∇×F)·dS (circulação e fluxo do rotacional)
- orientação: sentido do percurso × normal (regra da mão direita)
- relação com a lei de Ampère (superfície que apoia o contorno amperiano)

**Não usar quando**
- superfícies fechadas (use o teorema da divergência com as gaussianas)
- superfícies com buracos ou mais de um contorno

**Limitações**
- a gramática de cor segue o padrão do arsenal: campo vetorial = ciano (reservado ao campo), normal n̂ = azul, tangentes = branco, construções (remendo, contorno) = violeta, nunca sólidas
- só o objeto geométrico: integrais, fórmulas e o sinal da circulação/fluxo são do Manim
- a superfície é um hemisfério fixo (z ≥ 0) e o contorno é o equador; outra superfície com o mesmo contorno (um disco) não está no arsenal
- o campo desenhado é o rotacional (−y, x, 0) em 6 pontos: é ilustrativo, não é o ∇×F

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `raio` | 1.8 | u | raio do hemisfério |
| `com_campo` | 1 | 0/1 | 1 = setas ciano do campo rotacional |
| `normais` | 1 | 0/1 | 1 = normais n̂ para fora |
| `contorno_continuo` | 1 | 0/1 | 1 = contorno contínuo (circulação calculada); 0 = tracejado |
| `movimento` | 0 | 0/1 | 1 = animação em loop (use animar.py ou a ponte com o Manim) |
| `fase` | 0.0 | 0-1 | fase do loop; fase=1 repete o quadro da fase 0 (loop perfeito) |

**Integração:** `png_seq_alpha` · custo 1.02 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `circulacao` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 1.02 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- teorema_stokes --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("teorema_stokes").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/teorema_stokes.json`

### `toroide_corrente` — Toroide (fio enrolado em anel)

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Toroide: fio azul (#267BFF) enrolado em torno da seção de um toro cujo eixo é X. Núcleo de vidro opcional e eixo de simetria opcional.

![Toroide (fio enrolado em anel)](previews/toroide_corrente.png)

**Como se lê:** Anel formado por espiras azuis apertadas, com o buraco central visível. Lê-se como 'solenoide fechado sobre si mesmo'.

**Usar quando**
- campo B de um toroide (circulação amperiana circular dentro do núcleo; campo fora é nulo)
- contraste com o solenoide reto (enrolamento aberto)
- mostrar que o campo fica confinado ao interior do enrolamento
- corrente circulando pelas espiras do toroide (cargas_moveis=1)

**Não usar quando**
- enrolamento reto (use solenoide_corrente)
- toroide com seção retangular: aqui a seção é circular

**Limitações**
- só a fonte física (fio/enrolamento, azul): o campo B (ciano) e o sentido da corrente são desenhados no 2D/Manim
- sem noção de sentido: a hélice tem um sentido de enrolamento, mas ele não representa a corrente de forma legível; indicar I por rótulo/seta no Manim
- N espiras fixas e uniformes; o espaçamento interno é mais apertado que o externo, como num toroide real
- o fio é grosso para ser visível
- o movimento não codifica a corrente: a convenção (corrente convencional ou elétrons, que vão ao contrário) e o sinal vão por seta e rótulo no Manim; o movimento é didático, não em escala
- as cargas seguem o fio em volta do toroide; o campo B (ciano) circular no interior não é desenhado

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `raio_maior` | 1.6 | u | raio do círculo central do toro |
| `raio_menor` | 0.5 | u | raio da seção do toro |
| `n_espiras` | 40 | n | número de espiras |
| `raio_fio` | 0.04 | u | raio do fio (visual) |
| `nucleo` | 0 | 0/1 | 1 = núcleo de vidro (toro) dentro do enrolamento |
| `eixo` | 0 | 0/1 | 1 = eixo de simetria tracejado neutro |
| `comprimento_eixo` | 4.5 | u | comprimento do eixo, se desenhado |
| `cargas_moveis` | 0 | 0/1 | 1 = cargas em movimento (animação em loop); use com animar.py ou a ponte com o Manim |
| `fase` | 0.0 | 0-1 | fase do movimento; fase=1 repete o quadro da fase 0 (loop perfeito) |
| `espaco_cargas` | 0.9 | u | distância entre cargas ao longo do fio (ajustada para fechar a volta) |
| `tamanho_carga_movel` | 0.07 | u | raio de cada carga móvel |

**Integração:** `png_seq_alpha` · custo 0.45 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `circulacao` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 0.5 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- toroide_corrente --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("toroide_corrente").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/toroide_corrente.json`

### `tubo_escoamento` — Tubo com estrangulamento (continuidade)

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Tubo de vidro azulado (eixo X) que se estreita no meio até `razao` do raio, com partículas marcadoras (brancas perto, azul-claro longe) fluindo em +X com v ∝ 1/r². As partículas são igualmente espaçadas no tempo, então ficam mais afastadas e mais rápidas no gargalo.

![Tubo com estrangulamento (continuidade)](previews/tubo_escoamento.png)

**Como se lê:** Tubo com um gargalo e pontos que aceleram ao passar por ele e ficam mais espaçados. Lê-se como 'A v = constante'.

**Usar quando**
- equação da continuidade: A₁v₁ = A₂v₂
- Bernoulli e efeito Venturi (a diferença de pressão é do Manim)
- mostrar que a velocidade cresce onde a seção diminui

**Não usar quando**
- escoamento turbulento ou viscoso (o campo de velocidades é uniforme na seção)
- fluido compressível

**Limitações**
- o campo de velocidade é uniforme na seção (escoamento ideal): não há perfil parabólico
- as partículas são marcadores, não representam a densidade do fluido nem a pressão
- o estrangulamento é fixo (suave, de 1,5 u de transição); só `razao` e o raio mudam

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `comprimento` | 6.0 | u | comprimento do tubo (eixo X) |
| `raio` | 1.0 | u | raio nas pontas |
| `razao` | 0.5 | 0-1 | raio do gargalo / raio nas pontas |
| `n_particulas` | 36 | n | número de partículas marcadoras |
| `semente` | 7 | n | semente do sorteio |
| `movimento` | 0 | 0/1 | 1 = animação em loop (use animar.py ou a ponte com o Manim) |
| `fase` | 0.0 | 0-1 | fase do loop; fase=1 repete o quadro da fase 0 (loop perfeito) |

**Integração:** `png_seq_alpha` · custo 1.15 s/frame (1080p, Eevee)

**Animação (cargas em movimento):** `escoamento` · loop sem emenda (`fase` de 0 a 1) · 60 quadros sugeridos · custo 1.15 s/frame (1080p, com alpha)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- tubo_escoamento --res 1920x1080 --alpha
```

**No Manim:**

```python
from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal
img = Solido3D("tubo_escoamento").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()
```

Ficha: `solidos/tubo_escoamento.json`
