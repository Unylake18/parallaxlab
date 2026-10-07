# Arsenal de sólidos 3D (Blender)

> Arquivo **gerado** por `gerar_catalogo.py` a partir de `solidos/*.json`. Não edite à mão: edite a ficha e regere.

Cada sólido tem uma ficha com "usar quando / não usar quando". Consulte o índice, abra a ficha do que parecer
servir e confira os critérios antes de decidir. Status: `planejado` (só ideia), `estudo` (funciona, aparência
não aprovada), `aprovado` (pode entrar em vídeo).

| id | Nome | Status | Áreas |
|---|---|---|---|
| `anel_carregado` | Anel carregado (aro) | aprovado | eletromagnetismo/campo_eletrico, mecanica/momento_de_inercia |
| `casca_cilindrica_oca` | Casca cilíndrica oca | aprovado | eletromagnetismo/lei_de_gauss, eletromagnetismo/campo_eletrico |
| `casca_esferica_oca` | Casca esférica oca (com corte em octante) | aprovado | eletromagnetismo/lei_de_gauss, eletromagnetismo/campo_eletrico |
| `cilindro_coaxial` | Cilindro coaxial (condutor maciço + casca externa, em corte) | aprovado | eletromagnetismo/lei_de_gauss, eletromagnetismo/campo_eletrico |
| `cilindro_macico_isolante` | Cilindro maciço isolante com cargas no volume | aprovado | eletromagnetismo/lei_de_gauss, eletromagnetismo/campo_eletrico |
| `disco_carregado` | Disco carregado | aprovado | eletromagnetismo/campo_eletrico, mecanica/momento_de_inercia |
| `esfera_macica_isolante` | Esfera maciça isolante com cargas no volume | aprovado | eletromagnetismo/lei_de_gauss, eletromagnetismo/campo_eletrico |
| `gaussiana_caixa` | Superfície gaussiana em caixa (pillbox) | aprovado | eletromagnetismo/lei_de_gauss |
| `gaussiana_cilindrica` | Superfície gaussiana cilíndrica (fechada) | aprovado | eletromagnetismo/lei_de_gauss |
| `gaussiana_esferica` | Superfície gaussiana esférica | aprovado | eletromagnetismo/lei_de_gauss |
| `haste_carregada` | Haste carregada | aprovado | eletromagnetismo/campo_eletrico, mecanica/momento_de_inercia |
| `placa_infinita_carregada` | Placa infinita carregada (plano com cargas na superfície) | aprovado | eletromagnetismo/lei_de_gauss, eletromagnetismo/campo_eletrico |

## Padrão visual

Fonte única: `estilo.json`. Identidade: docs/identidade_visual.md. Gramática visual da série Lei de Gauss: constantes de cor em videos_longos/yt_0001_lei_gauss/cena.py e yt_0002_lei_gauss_casos_classicos/cena.py (o 3D segue o 2D, não o contrário).

| Cor | Hex | Papel |
|---|---|---|
| `fundo` | `#050816` | fundo da cena (muito escuro, bastante espaço negativo) |
| `texto_neutro` | `#F5F7FF` | matemática neutra; luz principal |
| `campo_eletrico` | `#35D9FF` | E⃗ e linhas de campo. RESERVADA ao campo: nunca em fontes, cargas ou superfícies |
| `fonte_fisica` | `#267BFF` | distribuição física: preenchimento do corpo, n̂ |
| `fonte_contorno` | `#7FB2FF` | contorno/aro da distribuição física, cargas próximas, R, Q; luz de contorno |
| `gaussiana` | `#9C8CFF` | superfície gaussiana e r: construção matemática, tracejada ou translúcida, nunca sólida |
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

### `anel_carregado` — Anel carregado (aro)

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Anel fino de vidro azulado no plano YZ, com eixo de simetria em X, e cargas espaçadas ao longo do aro (espaçamento regular com pequeno jitter). Eixo de simetria opcional (tracejado neutro).

![Anel carregado (aro)](previews/anel_carregado.png)

**Como se lê:** Aro de vidro fino com pontos azuis alinhados e, opcionalmente, o eixo tracejado atravessando o centro. Lê-se como 'carga distribuída numa linha circular; o campo no eixo se calcula somando dq'.

**Usar quando**
- campo elétrico no eixo de um anel carregado (integração de elementos de carga dq, simetria, análise de máximo e limites)
- momento de inércia de um aro (com_cargas=0), com o eixo de simetria desenhado
- contraste com o disco (superfície) e com a haste (linha reta)

**Não usar quando**
- a carga está numa superfície (use disco_carregado) ou numa linha reta (use haste_carregada)
- a espessura real do anel importa para o problema (o tubo aqui é só visual)

**Limitações**
- o campo e a gaussiana não são desenhados: o ciano é reservado ao campo (animação 2D/Manim)
- em contexto de mecânica (com_cargas=0) o azul de 'fonte física' vem da gramática de Eletromagnetismo; a gramática de cor da Mecânica não foi verificada aqui
- espessura/raio do corpo exagerados em relação ao ideal (o corpo de vidro é visível); as cargas ficam dentro dele
- as cargas têm espaçamento quase regular (jitter 0,12): uma distribuição contínua é aproximada por pontos

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `raio` | 1.5 | u | raio do anel |
| `raio_tubo` | 0.07 | u | raio do tubo do anel (visual) |
| `n_cargas` | 60 | n | número de cargas ao longo do aro |
| `com_cargas` | 1 | 0/1 | 1 = cargas pontuais (campo elétrico); 0 = só o corpo de vidro (ex.: momento de inércia) |
| `eixo` | 0 | 0/1 | 1 = eixo de simetria tracejado em cor neutra |
| `comprimento_eixo` | 4.0 | u | comprimento do eixo de simetria, se desenhado |
| `semente` | 7 | n | semente do sorteio/jitter (mesma semente = mesma distribuição) |

**Integração:** `png_seq_alpha` · custo 0.63 s/frame (1080p, Eevee)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- anel_carregado --res 1920x1080 --alpha
```

Ficha: `solidos/anel_carregado.json`

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

Ficha: `solidos/cilindro_macico_isolante.json`

### `disco_carregado` — Disco carregado

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Disco fino de vidro azulado no plano YZ, com eixo de simetria em X, e cargas uniformes sobre a superfície (distância mínima entre elas, semente fixa). Eixo de simetria opcional (tracejado neutro).

![Disco carregado](previews/disco_carregado.png)

**Como se lê:** Disco translúcido de borda luminosa, cheio de pontos uniformes e, opcionalmente, o eixo tracejado atravessando o centro. Lê-se como 'carga distribuída numa superfície circular'.

**Usar quando**
- campo elétrico no eixo de um disco carregado (anéis concêntricos somados; no limite de raio grande recupera o plano infinito)
- momento de inércia de um disco (com_cargas=0), com o eixo de simetria desenhado
- contraste com o anel (linha circular) e com a placa infinita (plano ilimitado)

**Não usar quando**
- o ponto do vídeo é um plano ilimitado sem borda (use placa_infinita_carregada)
- a carga está só no aro (use anel_carregado)

**Limitações**
- o campo e a gaussiana não são desenhados: o ciano é reservado ao campo (animação 2D/Manim)
- em contexto de mecânica (com_cargas=0) o azul de 'fonte física' vem da gramática de Eletromagnetismo; a gramática de cor da Mecânica não foi verificada aqui
- espessura/raio do corpo exagerados em relação ao ideal (o corpo de vidro é visível); as cargas ficam dentro dele
- cargas apenas sobre o plano médio do disco (visíveis através do vidro): uma só camada
- a densidade é uniforme: perfil radial não uniforme não está representado

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

**Integração:** `png_seq_alpha` · custo 0.71 s/frame (1080p, Eevee)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- disco_carregado --res 1920x1080 --alpha
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

Ficha: `solidos/esfera_macica_isolante.json`

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

Ficha: `solidos/gaussiana_esferica.json`

### `haste_carregada` — Haste carregada

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Haste fina de vidro azulado ao longo de Y, com eixo de simetria (mediatriz) em X, e cargas espaçadas ao longo dela. Eixo de simetria opcional (tracejado neutro).

![Haste carregada](previews/haste_carregada.png)

**Como se lê:** Bastão de vidro fino com uma fileira de pontos azuis e, opcionalmente, o eixo tracejado cruzando-o ao meio. Lê-se como 'carga distribuída numa linha reta finita'.

**Usar quando**
- campo elétrico de uma haste finita carregada (integração de dq, ponto na mediatriz, limite de haste longa)
- momento de inércia de uma haste (com_cargas=0), com o eixo de simetria desenhado
- contraste com o anel (linha curva) e com o disco (superfície)

**Não usar quando**
- a haste deve ser infinita: o objeto é finito (para linha infinita use gaussiana_cilindrica com a fonte da cena)
- a espessura da haste importa para o problema

**Limitações**
- o campo e a gaussiana não são desenhados: o ciano é reservado ao campo (animação 2D/Manim)
- em contexto de mecânica (com_cargas=0) o azul de 'fonte física' vem da gramática de Eletromagnetismo; a gramática de cor da Mecânica não foi verificada aqui
- espessura/raio do corpo exagerados em relação ao ideal (o corpo de vidro é visível); as cargas ficam dentro dele
- haste ao longo de Y fixa; em outra orientação, girar a câmera
- as cargas têm espaçamento quase regular (jitter 0,12)

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
| `comprimento` | 4.0 | u | comprimento da haste (eixo Y) |
| `raio` | 0.1 | u | raio da haste (visual) |
| `n_cargas` | 36 | n | número de cargas ao longo da haste |
| `com_cargas` | 1 | 0/1 | 1 = cargas pontuais (campo elétrico); 0 = só o corpo de vidro (ex.: momento de inércia) |
| `eixo` | 0 | 0/1 | 1 = eixo de simetria tracejado em cor neutra |
| `comprimento_eixo` | 3.0 | u | comprimento do eixo de simetria, se desenhado |
| `semente` | 7 | n | semente do sorteio/jitter (mesma semente = mesma distribuição) |

**Integração:** `png_seq_alpha` · custo 0.62 s/frame (1080p, Eevee)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- haste_carregada --res 1920x1080 --alpha
```

Ficha: `solidos/haste_carregada.json`

### `placa_infinita_carregada` — Placa infinita carregada (plano com cargas na superfície)

**Status:** aprovado · Aparência aprovada pelo usuário em 2026-10-07 (padrão visual de estilo.json); validado em 960x540 e 1080p.

Folha de vidro azulado muito fina (normal ao longo de X) com grade sutil e cargas pontuais distribuídas sobre o plano. A opacidade da folha, a grade e o tamanho das cargas se dissolvem com a distância ao centro, para sugerir que o plano continua além do quadro. Fisicamente finita (14 x 6,5 por padrão).

![Placa infinita carregada (plano com cargas na superfície)](previews/placa_infinita_carregada.png)

**Como se lê:** Plano azul translúcido de grade discreta, cheio de pontos e sumindo nas bordas. Cargas próximas da câmera são azul-claro (#7FB2FF); as distantes, azul (#267BFF). Lê-se como 'plano contínuo de carga, sem limites visíveis'.

**Usar quando**
- simetria planar: plano infinito com densidade superficial de carga uniforme (isolante fino ou plano de carga)
- mostrar que o plano é ilimitado e que o campo não depende da distância (par com os sólidos de simetria cilíndrica e esférica)
- contraste com as simetrias cilíndrica e esférica na mesma unidade (casca, maciço, plano)

**Não usar quando**
- o vídeo precisa mostrar as bordas ou efeitos de borda: a placa aqui se dissolve de propósito
- placa condutora de espessura finita (carga em duas faces) ou capacitor de duas placas: este sólido é um único plano
- placa espessa isolante com densidade volumétrica de carga: aqui as cargas estão só no plano

**Limitações**
- o plano é fisicamente finito e o 'infinito' é só visual (dissolve nas bordas); se o enquadramento incluir as bordas, o efeito se perde
- cargas só sobre o plano x=0; a normal do plano é fixa em X
- a visualização depende do ângulo: muito de frente (olhando ao longo de X) a placa vira um retângulo chapado; o padrão usa azimute -40
- não desenha campo elétrico: o ciano é reservado ao campo e fica para a animação 2D/Manim

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

**Integração:** `png_seq_alpha` · custo 1.31 s/frame (1080p, Eevee)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- placa_infinita_carregada --res 1920x1080 --alpha
```

Ficha: `solidos/placa_infinita_carregada.json`
