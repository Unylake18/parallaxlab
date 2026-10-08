# Lei de Gauss na prática — fechamento de Produção

Data: 2026-10-06. Escopo: somente pré-produção editorial. Identificação definitiva aprovada: **`yt_0002_lei_gauss_casos_classicos`**. A pauta anterior de energia potencial foi descartada editorialmente; sua pasta foi removida por autorização explícita do usuário. O pacote do Work foi transferido da pasta provisória para esta unidade definitiva.

Este documento segue a ordem de entrega do briefing. Narração integral em `narracao.md`, storyboard em `storyboard.md` e consolidação em `ficha.md`. Nenhum código de cena, áudio, legenda ou imagem é parte desta rodada.

**Aprovação registrada em 2026-10-06:** o usuário aprovou os quatro documentos do Work como fonte canônica de Produção. Prevalecem `Q_env` / carga envolvida, estimativa de 18:42 sem compressão artificial, B4 de ~56 s, revisão da esfera maciça de ~66 s e ressalva de simetria + carga envolvida fixa no payoff geométrico. Registro completo em `ficha.md`, seção Estado. Identificação administrativa resolvida; a implementação só começa com handoff específico, primeiro N01–N03.

## 1. Auditoria da seleção

Manter as onze configurações solicitadas. São dez aplicações e uma consequência local (B4), não onze derivações independentes. A1 ensina a superfície cilíndrica; B1 ensina o cilindro gaussiano curto/pillbox; C1 reapresenta a superfície esférica com derivação completa, porém curta, pois o primeiro longo já a desenvolveu. Variações conservam a superfície e atualizam carga envolvida/região.

| Caso | Função editorial | Decisão |
| --- | --- | --- |
| A1 Linha infinita | Ensinar simetria, lateral e tampas | Completo |
| A2 Casca cilíndrica | Distinguir carga existente e carga envolvida; salto | Manter |
| A3 Cilindro maciço | Carga volumétrica por região, continuidade e gráfico | Manter |
| A4 Coaxial | Condutores e confinamento radial | Manter sem capacitância |
| B1 Chapa não condutora | Duas tampas, fator 2 e campo constante | Completo |
| B2 Slab | Espessura, coordenada assinada e gráfico | Manter |
| B3 Duas chapas opostas | Soma vetorial e confinamento | Manter por superposição |
| B4 Face de condutor | Uma tampa ativa, densidade local | Consequência de 56 s |
| C1 Casca esférica | Esfera reutilizada e interior nulo | Completo em versão curta |
| C2 Esfera maciça | Retomada e contraste de gráficos | Revisão de 65 s |
| C3 Capacitor esférico | Terceira geometria de confinamento | Manter |

## 2. Redundâncias e ausências

C2 é redundante cientificamente com o vídeo 1, mas necessário aqui como revisão/comparação, sem reconstruir coordenadas esféricas ou integrais de volume. A2 e C1 repetem carga envolvida zero, mas a repetição evidencia a mesma estratégia em outra geometria. A4/B3/C3 são necessários ao payoff comparativo e não serão reduzidos a menções.

Nenhuma ausência essencial entre os clássicos da seleção. Carga pontual aparece como equivalência externa da casca, não como um décimo segundo caso. A esfera condutora isolada pode ser reconhecida como variante de C1: interior nulo e exterior pontual; não abrir outro bloco. Placa condutora inteira, cilindro com espessura e esferas condutoras espessas ficam cobertos pelas hipóteses/QA, sem novos casos públicos.

Não incluir densidades variáveis, cargas excêntricas, objetos finitos, potencial ou capacitâncias. A passagem entre desenhos representa comparação de modelos, não transformação física que conserve a carga durante todo o morph.

## 3. Solução e verificação matemática de todos os casos

### Convenções comuns

Eletrostática no vácuo, permissividade `ε₀`, fontes isoladas sem campo externo imposto. Nos desenhos, `λ>0`, `σ>0`, `ρ>0`, `Q>0`; os sinais negativos explícitos dos capacitores são mantidos. Para outras polaridades, inverter vetores; módulos usam valores absolutos. Nas fórmulas radiais abaixo, `E_r` é a componente assinada para fora. Sob a polaridade positiva exibida, coincide com o módulo `E`.

Usar publicamente **carga envolvida**, `Q_{\mathrm{env}}`, como no `yt_0001`. É exatamente a carga encerrada do briefing, `Q_{\rm enc}`; registrar esta equivalência aqui, sem introduzir duas notações concorrentes na tela.

$$\Phi_E=\oint_S\vec E\cdot d\vec A=\frac{Q_{\mathrm{env}}}{\varepsilon_0},\qquad d\vec A=\hat n\,dA.$$

`r` é distância ao eixo nos casos cilíndricos e ao centro nos esféricos; `R` é raio físico fixo. `L` é comprimento arbitrário FINITO da superfície gaussiana, não comprimento da fonte infinita. `A` é área de cada tampa; `x` é coordenada normal assinada nos casos planares. Não integrar exatamente sobre uma camada superficial singular: dar limites laterais.

### A1 — Linha infinita

Translações ao longo do eixo e rotações em torno dele eliminam dependências em `z` e azimute. Reflexões eliminam componentes axial e azimutal. Resta `\vec E=E_r(r)\hat r`. Cilindro fechado coaxial de raio `r>0`, comprimento `L>0`: normal radial na lateral, axial nas tampas.

$$\Phi_{\rm lateral}=E_r\,2\pi rL,\qquad\Phi_{\rm tampas}=0,\qquad Q_{\mathrm{env}}=\lambda L.$$
$$E_r\,2\pi rL=\frac{\lambda L}{\varepsilon_0}\quad\Rightarrow\quad E_r(r)=\frac{\lambda}{2\pi\varepsilon_0r}.$$

Verificação independente por Coulomb, somente QA: no ponto a distância `r`, pares de elementos em `±z` cancelam a componente axial.
$$E_r=\frac{\lambda}{4\pi\varepsilon_0}\int_{-\infty}^{\infty}\frac{r\,dz}{(r^2+z^2)^{3/2}}=\frac{\lambda}{4\pi\varepsilon_0}\frac2r.$$
`L` cancela, unidades `N/C`, sinal acompanha `λ`, limite `∞` nulo; `r→0⁺` diverge. Não mostrar valor finito no eixo da linha ideal.

### A2 — Casca cilíndrica

Camada não condutora ideal de raio `R`, espessura desprezível, uniforme ao longo do eixo e do azimute. Escolha pública: `λ` = carga total por unidade de comprimento; não mostrar `σ` redundante.

$$Q_{\mathrm{env}}(r)=\begin{cases}0,&r<R,\\\lambda L,&r>R,\end{cases}\qquad E_r(r)=\begin{cases}0,&r<R,\\\dfrac{\lambda}{2\pi\varepsilon_0r},&r>R.\end{cases}$$

Para `0<r<R`, a simetria dá um único `E_r` na lateral, então `E_r2πrL=0` implica `E_r=0`; no eixo, a simetria/regularidade completa o resultado. Não deduzir zero apenas da ausência de carga.

QA: `σ_R=λ/(2πR)`; salto radial `E_r(R⁺)−E_r(R⁻)=λ/(2πε₀R)=σ_R/ε₀`. Exterior decai; interior regular. Em `r=R`, não atribuir valor único ao campo ideal.

### A3 — Cilindro maciço

Fonte NÃO condutora, raio `R`, uniforme no volume com `ρ`; infinita ao longo do eixo. Sem camada superficial adicional.

$$Q_{\mathrm{env}}=\rho\pi L\min(r^2,R^2).$$
$$E_r(r)=\begin{cases}\dfrac{\rho r}{2\varepsilon_0},&0\le r<R,\\\dfrac{\rho R^2}{2\varepsilon_0r},&r>R.\end{cases}$$

Derivação interior: `E_r2πrL=ρπr²L/ε₀`, cancelar `πL`, dividir por `2r`. Exterior: substituir apenas `r²` por `R²` na carga; área gaussiana continua dependendo de `r`.

$$E_r(R^-)=E_r(R^+)=\frac{\rho R}{2\varepsilon_0},\qquad E_r(0)=0,\qquad E_r(\infty)=0.$$

QA independente local: `(1/r)d(rE_r)/dr=ρ/ε₀` dentro e zero fora; a ausência de camada garante continuidade, mas as derivadas em `R` são opostas. `λ_total=ρπR²` reproduz o campo exterior A1. Não prolongar o ramo linear para fora.

### A4 — Capacitor coaxial

Modelo público fechado: condutor interno MACIÇO de raio `a`; condutor externo em casca ideal delgada de raio `b>a`; ambos infinitos, coaxiais, separados por vácuo, em equilíbrio eletrostático. Cargas totais por comprimento `+λ` e `−λ`. Sem cavidade no condutor interno, sem fontes externas. A casca fina evita um terceiro raio público.

$$Q_{\mathrm{env}}=\begin{cases}0,&r<a,\\+\lambda L,&a<r<b,\\(+\lambda-\lambda)L=0,&r>b,\end{cases}$$
$$E_r(r)=\begin{cases}0,&r<a,\\\dfrac{\lambda}{2\pi\varepsilon_0r},&a<r<b,\\0,&r>b.\end{cases}$$

O zero dentro do material vem do equilíbrio eletrostático. O zero externo vem da carga líquida por comprimento nula MAIS simetria cilíndrica e ausência de campo externo. Vetores saem do interno positivo e terminam no externo negativo.

QA: `σ_a=λ/(2πa)`, `σ_b=−λ/(2πb)`. Saltos, tomando `\hat r` como direção crescente: em `a`, `+λ/(2πε₀a)`; em `b`, `−λ/(2πε₀b)`. Não unir curvas através desses saltos. Para condutor externo espesso `b<r<c`, o material tem `E=0`, a face em `b` leva `−λ`, a face em `c` fica sem excesso e o exterior continua nulo; `c` é QA, sem novo caso público.

### B1 — Chapa infinita não condutora

Folha ideal uniforme em `x=0`, densidade `σ`, sem outra fonte. Translações/rotações no plano eliminam dependência lateral e componentes paralelas. Reflexão pelo plano dá módulos iguais e sentidos opostos. Pillbox fechado simétrico, área `A` de cada tampa.

$$\Phi_E=EA+EA=2EA,\quad\Phi_{\rm lateral}=0,\quad Q_{\mathrm{env}}=\sigma A.$$
$$2EA=\frac{\sigma A}{\varepsilon_0}\quad\Rightarrow\quad E=\frac{\sigma}{2\varepsilon_0}\quad(\sigma>0).$$
$$E_x(x)=\frac{\sigma}{2\varepsilon_0}\operatorname{sgn}(x),\qquad x\ne0.$$

As duas contribuições do fluxo são positivas para `σ>0`, pois campo e normal exterior se invertem juntos. Campo não diminui com a distância no modelo infinito. QA independente por Coulomb: `E_x=σx/(2ε₀)∫₀^∞ s ds/(s²+x²)^{3/2}=σ sgn(x)/(2ε₀)`. Salto `E_x(0⁺)−E_x(0⁻)=σ/ε₀`. Não exigir campo zero no infinito para essa fonte infinita; valor na folha ideal não é definido por estes ramos.

### B2 — Slab uniforme

Distribuição NÃO condutora, infinita em `y,z`, ocupando `−a<x<a`, densidade volumétrica `ρ`, sem folha singular nas faces. Superfície gaussiana simétrica com tampas em `±u`, onde `u=|x|>0`.

$$Q_{\mathrm{env}}=2\rho A\min(u,a),\qquad 2E(u)A=\frac{Q_{\mathrm{env}}}{\varepsilon_0}.$$
$$E_x(x)=\begin{cases}-\rho a/\varepsilon_0,&x<-a,\\\rho x/\varepsilon_0,&|x|\le a,\\+\rho a/\varepsilon_0,&x>a.\end{cases}$$

Público: derivar para `x>0`: dentro `Q_env=2ρxA`, fora `Q_env=2ρaA`; depois espelhar vetores e apresentar o gráfico ASSINADO `E_x(x)`. O volume nunca é negativo. QA: `E_x(−x)=−E_x(x)`, `E_x(0)=0`, continuidade nas duas faces, derivada interior `ρ/ε₀`, exterior zero; limites em `±∞` são constantes opostas.

Verificação por superposição de folhas infinitesimais, somente QA:
$$E_x(x)=\frac{\rho}{2\varepsilon_0}\int_{-a}^{a}\operatorname{sgn}(x-x')\,dx'.$$
Dentro a integral vale `2x`; fora vale `±2a`. A função módulo seria um V com patamares, não a reta ímpar escolhida para a tela.

### B3 — Duas chapas opostas / capacitor plano

Folhas infinitas paralelas em `x=0` (`+σ`) e `x=d` (`−σ`), `d>0`; vácuo entre elas; sem campo externo. O campo de cada folha já foi derivado em B1.

$$E_x(x)=\frac{\sigma}{2\varepsilon_0}\left[\operatorname{sgn}(x)-\operatorname{sgn}(x-d)\right]=\begin{cases}0,&x<0,\\\sigma/\varepsilon_0,&0<x<d,\\0,&x>d.\end{cases}$$

Entre as chapas os dois vetores apontam da positiva para a negativa e somam; fora, cancelam. Descrição como capacitor de placas condutoras: `±σ` são densidades nas FACES voltadas para o vão, no modelo ideal; campo zero nos materiais e nas regiões externas. Folhas fontes e material condutor não são confundidos.

QA: salto `+σ/ε₀` na folha positiva e `−σ/ε₀` na negativa. Não usar `Q_env=0` sozinho como prova do campo externo planar: a soma vetorial, sem fundo externo, é a justificativa pública. Não calcular `C` ou potencial.

### B4 — Superfície de condutor

Condição LOCAL, que não exige simetria planar global. Região da superfície suave, vácuo imediatamente fora, equilíbrio eletrostático. `\hat n` sai do material para o vácuo; `σ_face` é densidade algébrica local nesta face, não carga por área de uma lâmina inteira.

Pillbox infinitesimal atravessando a face: tampa no metal tem fluxo zero; contribuição lateral desaparece no limite de altura; `Q_env=σ_face A`.
$$EA=\frac{\sigma_{\rm face} A}{\varepsilon_0},\qquad\vec E_{\rm fora}=\frac{\sigma_{\rm face}}{\varepsilon_0}\hat n,\qquad E_{\parallel,\rm fora}=0.$$

QA: componente normal assinada `E_{n,fora}=σ_face/ε₀`; módulo `|σ_face|/ε₀`. Para face negativa, campo aponta para o metal. A diferença entre uma e duas tampas ativas explica o fator 2. Se uma lâmina condutora isolada e simétrica tiver carga TOTAL por área `Σ`, cada face terá `σ_face=Σ/2`, resultando em `E=Σ/(2ε₀)`; isso fica apenas em QA.

### C1 — Casca esférica

Casca NÃO condutora ideal, raio `R`, carga `Q` uniforme na superfície; sem campo externo. Rotações ao redor do centro e reflexões dão `\vec E=E_r(r)\hat r`. Esfera gaussiana concêntrica fechada.

$$\Phi_E=E_r\,4\pi r^2,\qquad Q_{\mathrm{env}}=\begin{cases}0,&r<R,\\Q,&r>R.\end{cases}$$
$$E_r(r)=\begin{cases}0,&r<R,\\\dfrac{Q}{4\pi\varepsilon_0r^2},&r>R.\end{cases}$$

`0<r<R` implica zero com simetria; centro zero por isotropia. Exterior equivalente ao campo de carga pontual CENTRAL apenas fora da casca. QA: `σ_R=Q/(4πR²)` e salto `Q/(4πε₀R²)=σ_R/ε₀`; limite no infinito zero. Casca fina tem salto; não extrapolar exterior ao centro.

### C2 — Esfera maciça

Fonte NÃO condutora, densidade `ρ` uniforme, raio `R`, sem camada superficial singular.
$$Q=\frac43\pi\rho R^3,\qquad Q_{\mathrm{env}}=\frac43\pi\rho\min(r^3,R^3).$$
$$E_r(r)=\begin{cases}\dfrac{\rho r}{3\varepsilon_0},&0\le r<R,\\\dfrac{\rho R^3}{3\varepsilon_0r^2}=\dfrac{Q}{4\pi\varepsilon_0r^2},&r>R.\end{cases}$$

QA: `E_r4πr²=Q_env/ε₀` nos dois ramos; continuidade `E(R)=ρR/(3ε₀)`; centro zero; infinito zero; dentro `(1/r²)d(r²E_r)/dr=ρ/ε₀`, fora zero. Declives em `R`: `ρ/(3ε₀)` e `−2ρ/(3ε₀)`. A expressão equivalente `Qr/(4πε₀R³)` fica em QA para evitar parâmetros públicos redundantes.

### C3 — Capacitor esférico

Modelo público: esfera condutora MACIÇA de raio `a`, carga `+Q`; casca condutora ideal delgada concêntrica de raio `b>a`, carga total `−Q`; vácuo no vão e ausência de fontes externas. Assim `r<a` significa material do condutor interno, não uma cavidade ambígua.

$$Q_{\mathrm{env}}=\begin{cases}0,&r<a,\\Q,&a<r<b,\\Q-Q=0,&r>b,\end{cases}\qquad E_r(r)=\begin{cases}0,&r<a,\\\dfrac{Q}{4\pi\varepsilon_0r^2},&a<r<b,\\0,&r>b.\end{cases}$$

Interior zero por equilíbrio, exterior zero por carga líquida + simetria esférica; campo radial do positivo para o negativo no vão. QA: `σ_a=Q/(4πa²)`, `σ_b=−Q/(4πb²)`; saltos `+Q/(4πε₀a²)` e `−Q/(4πε₀b²)`. Se a casca externa tiver espessura até `c`, metal `b<r<c` tem campo zero; face interna leva `−Q`, face externa zero; não adicionar `c` à tela.

## 4. Hipóteses de cada configuração

As definições completas estão nas subseções anteriores e são parte da especificação, não decisões futuras de implementação.

| Casos | Hipótese que deve ser falada | Rótulo recorrente |
| --- | --- | --- |
| A1–A3 | Fonte infinita e uniforme; campo próprio sem fontes externas | Modelo infinito ideal |
| A2/C1 | Carga em camada superficial ideal de espessura desprezível | Casca uniforme |
| A3/B2/C2 | Carga distribuída no volume de um isolante; sem folha extra na fronteira | Densidade volumétrica constante |
| A4 | Dois condutores coaxiais infinitos em equilíbrio; núcleo maciço | Vácuo; cargas opostas |
| B1 | Chapa não condutora infinita, isolada | Sem efeitos de borda |
| B2 | Slab infinito paralelamente ao plano, espessura finita `2a` | Plano médio `x=0` |
| B3 | Duas folhas infinitas opostas; interpretação em faces condutoras | Campo de `+` para `−` |
| B4 | Face local de condutor em equilíbrio; pillbox infinitesimal | `σ_face`: nesta face |
| C1/C2 | Distribuição esfericamente uniforme, sem fontes externas | Esfera concêntrica |
| C3 | Núcleo condutor maciço + casca concêntrica delgada | Vácuo; cargas opostas |

Uma vista lateral finita representa apenas um trecho da fonte infinita. Não desenhar cargas nas tampas fictícias da fonte. O cilindro gaussiano sempre tem tampas fechando a superfície matemática.

## 5. Decisão público × QA

Público: justificativa das superfícies, `Q_env` por região, fórmulas finais com domínio, cancelamentos relevantes, continuidade dos maciços/slab, leitura de saltos nas cascas, direção/sinal e idealizações. B4 ocupa só 56 s. Não usar a condição de salto formal como mais um assunto; mencionar que uma camada superficial pode produzir salto.

QA: integral de Coulomb da linha/chapa, superposição integral do slab, divergência local, densidades equivalentes das cascas, espessura dos condutores externos, fórmula geral do salto, limites completos e identidades dimensionais. Estas verificações sustentam a aula, mas não são narradas como onze listas.

## 6. Títulos/headlines candidatos

1. **As 3 simetrias que resolvem a Lei de Gauss** — recomendação editorial.
2. Lei de Gauss sem decorar: o guia das três simetrias.
3. Lei de Gauss na prática: os casos clássicos.
4. Como escolher a superfície gaussiana certa.
5. Lei de Gauss: esfera, cilindro, plano e capacitores.
6. Um método, três simetrias: Lei de Gauss na prática.
7. Da fonte ao campo: como usar a Lei de Gauss.
8. Esfera, cilindro ou plano? O método da Lei de Gauss.

Título de tela: **LEI DE GAUSS** (mesmo sistema do primeiro longo). Subtítulo: **Três simetrias, um método**. Headline editorial possível: **ESFERA · CILINDRO · PLANO**. São propostas de texto, sem produzir thumbnail. Evitar “todos” como promessa absoluta: o vídeo cobre os clássicos selecionados, não toda aplicação possível.

## 7. Pergunta central definitiva

Como reconhecer a superfície gaussiana certa e resolver os casos clássicos da Lei de Gauss sem decorar uma fórmula diferente para cada geometria?

## 8. Payoff definitivo

**Identifique a simetria da fonte, escolha uma superfície onde o fluxo simplifique e calcule a carga envolvida na região. Esfera, cilindro e plano são três versões do mesmo raciocínio.**

Algoritmo recorrente, construído progressivamente: fonte → simetria → direção/dependência de `E` → superfície gaussiana → fluxo → carga envolvida → campo. O formato longo permite mostrá-lo em duas linhas, sem reduzir a fonte para caber sete etapas.

## 9. Arquitetura final

Cold open científico → intro humana curta no sistema existente → recap/algoritmo → capítulo cilíndrico (A1→A4) → capítulo planar (B1→B4) → capítulo esférico (C1→C3) → três capacitores → áreas/potências → checklist aplicado → payoff → pausa → CTA.

A primeira fonte de cada família explica o aparato; as fontes seguintes substituem apenas o que mudou. Há transições contínuas entre modelos, com rótulo de material quando o isolante vira condutor. Não sugerir que adicionar uma casca negativa transforma automaticamente uma esfera com carga volumétrica uniforme num capacitor: antes, trocar explicitamente o modelo para condutor e redistribuir a carga na superfície.

## 10. Tempos estimados por bloco

| Bloco | Janela editorial | Duração |
| --- | --- | --- |
| Abertura, intro, recap e método | 0:00–1:17 | 77 s |
| Cilíndrico, incluindo transição | 1:17–6:32 | 315 s |
| Planar, incluindo transição | 6:32–12:03 | 331 s |
| Esférico | 12:03–15:27 | 204 s |
| Comparação, método e encerramento | 15:27–18:42 | 195 s |
| Total de referência | 0:00–18:42 | 1122 s |

Tempos são orçamento editorial, não sincronia medida. A narração integral contém **2551 palavras faladas**, excluindo ganchos alternativos, cabeçalhos e cues. A referência usa 150 palavras/min e **93 s de leitura/demonstração/pausa**, com arredondamento por beat: 18:42. A 145 palavras/min, a estimativa é cerca de 19:09 antes dos arredondamentos. O intervalo de planejamento é aproximadamente 18:40–19:20, próximo da tolerância aberta no briefing e abaixo do teto de 20 min. A velocidade efetiva precisa ser medida na etapa de voz. Se a leitura pedir mais tempo, retirar redundâncias antes de acelerar explicações ou cortar casos. Não fabricar duração de áudio ausente.

## 11. Narração completa

Texto integral, falável e dividido por âncoras em **`narracao.md`**. Três ganchos opcionais, um selecionado, sem ler todos no vídeo. Notas entre colchetes não são faladas.

## 12. Storyboard detalhado

Em **`storyboard.md`**: tempo estimado, fala vinculada à íntegra, tela/equações, animação, modo e objetivo por beat; também mapa de retenção.

## 13. Equações públicas

IDs abaixo servem ao storyboard; as linhas intermediárias são estados sucessivos, nunca um mural inteiro. `E` radial assume carga positiva; `E_x` é componente assinada planar. Casos por região podem aparecer em dois/três cartões sucessivos antes de uma expressão compacta final.

| ID | Estados públicos |
| --- | --- |
| P0 | `∮ E⃗·dA⃗ = Q_env/ε₀`; método em palavras |
| P1 | `E⃗=E(r) r̂`; `Φ_lateral=E2πrL`; `Φ_tampas=0`; `Q_env=λL`; `E2πrL=λL/ε₀`; `E=λ/(2πε₀r)` |
| P2 | `Q_env=0` / `λL`; `E=0 (r<R)` / `λ/(2πε₀r) (r>R)` |
| P3 | `Q_env=ρπr²L` / `ρπR²L`; `E2πrL=Q_env/ε₀`; `E=ρr/(2ε₀)` / `ρR²/(2ε₀r)`; `E(R⁻)=E(R⁺)` |
| P4 | `Q_env=0`, `λL`, `(λ−λ)L`; `E=0`, `λ/(2πε₀r)`, `0`, com `r<a`, `a<r<b`, `r>b` |
| P5 | `Q_env=σA`; `Φ=EA+EA=2EA`; `2EA=σA/ε₀`; `E=σ/(2ε₀)`; domínio `x≠0` |
| P6 | para `x>0`: `Q_env=2ρxA` / `2ρaA`; `E=ρx/ε₀` / `ρa/ε₀`; depois `E_x=ρx/ε₀ (|x|≤a)` / `±ρa/ε₀ (x≷±a)`; `E_x(0)=0` |
| P7 | `E_entre=σ/(2ε₀)+σ/(2ε₀)=σ/ε₀`; `E_fora=0`; setas de superposição; `0<x<d` |
| P8 | `E_dentro=0`; `EA=σ_face A/ε₀`; `E_{n,fora}=σ_face/ε₀`; normal para fora do material |
| P9 | `Φ=E4πr²`; `Q_env=0` / `Q`; `E=0` / `Q/(4πε₀r²)`; `r<R` / `r>R` |
| P10 | `Q_env=(4/3)πρr³` / `Q=(4/3)πρR³`; `E=ρr/(3ε₀)` / `Q/(4πε₀r²)`; continuidade e `E(0)=0` |
| P11 | `Q_env=0`, `Q`, `Q−Q`; `E=0`, `Q/(4πε₀r²)`, `0`, nos três domínios |
| P12 | No vão: plano `constante`, coaxial `1/r`, esférico `1/r²` |
| P13 | Com `Q_env` fixo: `4πr²→1/r²`, `2πrL→1/r`, tampas `A`/`2A` não crescem com distância `→constante` |
| P14 | Checklist progressivo, com fórmula de Gauss e `Q_env(região)`; domínio explícito |

## 14. Equações apenas de QA

Além das verificações locais da seção 3: salto normal geral `E_n^+−E_n^−=σ/ε₀`, normal da região “−” para a “+”; lei diferencial `∇·E⃗=ρ/ε₀`; equivalências `λ=2πRσ` e `Q=4πR²σ`; densidades das faces de capacitores; extensões a condutores espessos. Não usar `1/r`, `1/r²` como afirmação de campo EXTERIOR aos capacitores: os três têm campo externo zero no modelo selecionado; as potências se referem ao VÃO.

Dimensional: `[ε₀]=C²/(N m²)`, `[λ]=C/m`, `[σ]=C/m²`, `[ρ]=C/m³`. Portanto `[λ/(ε₀r)]=[σ/ε₀]=[ρr/ε₀]=[Q/(ε₀r²)]=N/C`. Fluxo tem unidade `N m²/C`, carga envolvida tem `C`. Verificado em todos os ramos, inclusive `ρR²/(ε₀r)` e `ρR³/(ε₀r²)`.

## 15. Gráficos necessários

Obrigatórios, apenas três gráficos completos. Marcador de posição sincronizado à gaussiana; coordenada da fonte fixa e da superfície móvel inequívocas.

1. A3: `u=r/R`, `E/E_R`, `E_R=ρR/(2ε₀)`: `u` dentro, `1/u` fora. Centro `(0,0)`, encontro `(1,1)`, cauda decrescente. Eixo radial começa em zero.
2. B2: `v=x/a`, `E_x/E_a`, `E_a=ρa/ε₀`: `−1` para `v<−1`, `v` para `−1≤v≤1`, `+1` para `v>1`. Eixo assinado de ambos os lados. A gaussiana tem tampas `±|x|`; o ponto de observação pode ser à esquerda. Contínuo nas faces.
3. C2: `u=r/R`, `E/E_R`, `E_R=ρR/(3ε₀)`: `u` dentro, `1/u²` fora. Comparar sequencialmente ao A3 com mesma normalização; não comparar amplitudes físicas sem informar densidades/raios.

Mini-indicação de salto para A2/C1: dois níveis/limites laterais junto ao diagrama, sem quarto gráfico de longa duração. Campos dos capacitores são demonstrados por vetores e regiões; nenhum gráfico extra é necessário. Se futuramente se desenhar um gráfico por regiões, o salto deve ter pontos abertos/fechados convencionados e não uma curva contínua inventada.

## 16. QA físico/matemático auditado nesta rodada

Derivações algébricas e verificações analíticas concluídas nesta seção e na seção 3; ainda não são QA de uma animação inexistente.

| Caso | Carga/fluxo | Direção, sinal e unidades | Fronteira | Limites |
| --- | --- | --- | --- | --- |
| A1 | `λL`, lateral `2πrL` | Radial; sinal `λ`; N/C | Eixo singular | Diverge em 0; zero em ∞ |
| A2 | 0 / `λL` | Radial; sinal `λ`; N/C | Salto `σ_R/ε₀` | Centro zero; exterior zero em ∞ |
| A3 | `ρπr²L` / `ρπR²L` | Radial; sinal `ρ`; N/C | Contínuo, declive muda | Zero em 0 e ∞ |
| A4 | 0 / `λL` / 0 | `+` para `−`; N/C | Saltos nas faces | Material e exterior zero |
| B1 | `σA`, duas tampas | Normal; oposto nos lados; N/C | Salto `σ/ε₀` | Patamares não nulos em ±∞ |
| B2 | `2ρA min(|x|,a)` | `E_x` ímpar; N/C | Contínuo em ±a | Centro zero; constantes em ±∞ |
| B3 | Soma dos campos B1 | Da placa `+` para a `−`; N/C | Saltos opostos | Exterior zero |
| B4 | `σ_face A`, uma tampa | Normal exterior assinada; N/C | Salto local, tangente zero | Condição local; ∞ não aplicável |
| C1 | 0 / Q, `4πr²` | Radial; sinal Q; N/C | Salto `σ_R/ε₀` | Centro zero; exterior zero em ∞ |
| C2 | `(4/3)πρ min(r³,R³)` | Radial; sinal ρ; N/C | Contínuo, declive muda | Zero em 0 e ∞ |
| C3 | 0 / Q / 0 | `+` para `−`; N/C | Saltos nas faces | Material e exterior zero |

Pontos conceituais fechados: a lei vale para qualquer superfície fechada; a fonte fornece a simetria; carga externa pode produzir campo local, embora não entre em `Q_env`; fluxo/carga envolvida zero não bastam para concluir campo zero em geral; a condição local de condutor não equivale a uma fonte globalmente planar; o argumento das áreas requer simetria e carga envolvida fixa, não é regra universal para maciços por dentro.

Conferência bibliográfica: materiais universitários primários, consultados em 06/10/2026. Os textos, derivações e diagramas propostos são originais; nenhum exercício numerado foi adaptado. Não foi verificada uma edição específica de Griffiths ou Sears, portanto não lhes atribuir seções/exercícios.

- Samuel J. Ling, William Moebs, Jeff Sanny — *University Physics Volume 2*, OpenStax (2016), [§6.3 Applying Gauss’s Law](https://openstax.org/books/university-physics-volume-2/pages/6-3-applying-gausss-law): confirmação das três simetrias e superfícies. As substituições por região acima foram derivadas diretamente de Gauss.
- Mesmos autores, [§6.4 Conductors in Electrostatic Equilibrium](https://openstax.org/books/university-physics-volume-2/pages/6-4-conductors-in-electrostatic-equilibrium): confirmação do campo nulo no material em equilíbrio e da condição normal na face.
- MIT OCW, *8.02 Physics II: Electricity and Magnetism*, Spring 2007, [Class Slides, presentati_w02d2.pdf](https://ocw.mit.edu/courses/8-02-physics-ii-electricity-and-magnetism-spring-2007/ae0d9b601b83812b25ed6a4fb0c19a03_presentati_w02d2.pdf): texto do PDF conferido; slides 23–25 (método/superfícies), 27–31 (esfera uniforme), 33–35 (cilíndrico), 36–38 (planar), 40 (enunciado de slab com espessura 2d). Nenhuma figura ou enunciado será copiado; aqui a meia-espessura é `a`. Potencial nos slides posteriores não integra esta unidade.

## 17. QA visual — critérios para a futura implementação

Não declarar estes testes como executados: nesta rodada só foram auditadas as instruções do storyboard.

- Ler em 960×540; verificar domínios junto das fórmulas, acentos e hierarquia do sistema do `yt_0001`.
- Fonte azul contínua/preenchida; gaussiana violeta tracejada; regiões que contribuem em traço contínuo; volume envolvido violeta translúcido com rótulo. Nenhuma superfície matemática vira peça física.
- A1: nas tampas `E⃗` está no plano, perpendicular à normal, não “campo zero”; B1: campo sai de ambas as tampas para σ positivo; lateral tem campo tangente.
- A2/C1: campo aparece de modo descontínuo ao cruzar a casca; não passar a gaussiana exatamente sobre a camada ao avaliar Gauss.
- A3/B2/C2: posição, carga envolvida, fórmula e ponto do gráfico correspondem ao mesmo estado. Não prolongar linearidade além da fonte.
- A4/C3: nenhuma seta dentro do metal ou fora do sistema; sinais das faces identificados por símbolos, não só cor; mudanças de modelo/material ditas e rotuladas.
- B2: campo à esquerda negativo em `E_x`; volume da gaussiana positivo; centro sem vetor com direção definida.
- B3: setas auxiliares identificadas por placa; só a resultante ciano opaca tem hierarquia principal. Fora, cancelamento vetorial visível.
- B4: normal sai do metal; tampa inferior dentro do material; `σ_face` junto da face, não da lâmina inteira.
- Não usar painéis rígidos permanentes. Nunca três derivações completas simultâneas. Comparação final de três capacitores: apenas diagramas pequenos e uma lei por caso, com leitura sequencial.
- Transformações: uma operação por estado; cancelamentos permanecem apontáveis; textos não migram para a geometria por matching enganoso; sem índices ou guias no final.
- Payoff sem CTA na mesma tela; pausa de 2 s; outro segue a marca existente. Sem data prometida.

## 18. Continuidade visual explícita com yt_0001

Referências efetivamente consultadas: `videos_longos/yt_0001_lei_gauss/ficha.md` (identidade, arquitetura, semântica, tipografia e QA); trechos de `cena.py` (paleta/composição/helpers, `b02_intro`, `b12_retorno_payoff_outro`); `template/config_horizontal.py`, `template/layout_horizontal.py`; `docs/formatos.md` e `docs/mapa_curricular.md` §6.3. Não foi necessário rever os vídeos ou ler toda a cena.

| Item | Especificação de continuidade |
| --- | --- |
| Abertura | Ciência primeiro, sem watermark/tag antes do cold open terminar. Intro humana curta; manter diagramas residuais embaixo, menores e com 30% de opacidade |
| Marca na intro | `PARALLAX LAB`, Space Grotesk 22, opacidade 0,8, centro lógico `(0,2.05)`; primeiro longo não usa logo grande na intro |
| Título | Mesmo sistema `LEI DE GAUSS`, Space Grotesk Bold 58, centro `(0,1.25)`; subtítulo 26, 85%, `(0,0.45)`; mudar só o texto do subtítulo |
| Watermark | Asset vigente de `template/config_horizontal.py`/config reexportado; largura lógica 1,92, opacidade 0,45, canto superior direito, margem 0,30 |
| Header | `ELETROMAGNETISMO · LEI DE GAUSS`, 18, opacidade 0,6, canto superior esquerdo, margem 0,38; persistente depois da intro |
| Frame/margens | 16×9; conteúdo crítico em `|x|≤7.2`, `|y|≤3.8`; corpo entre `y=−3.0` e `2.6`; faixa inferior livre para controles/legendas/respiro |
| SPLIT | `split(0.5)`, gap 0,6; centros derivados do helper: aproximadamente `x=−3.75,+3.75`, `y=−0.2`; diagrama à esquerda e análise à direita |
| FOCUS/BUILD | Região ampla, sem contornos de dashboard. Texto normal 24–36; equação ativa 42–52; caso 20 e domínio 26, cerca de 70–75%; usar mesma hierarquia e não reduzir fórmulas só para caber |
| Fontes | Space Grotesk em texto via helpers vigentes; MathTex em matemática. Não usar uma nova família de headline |
| Cores | Fundo #050816; campo/E #35D9FF; fonte preenchida #267BFF e contorno/R/Q #7FB2FF; gaussiana/r #9C8CFF; normal #267BFF; dA⃗/patch #745CFF; neutro #F5F7FF; magenta #EA63FF só para conflito hipotético |
| Ângulos | Âmbar #FFC24D apenas se necessário nas relações campo-normal; não adicionar uma seção de ângulos |
| Setas | Estilo `vec` da cena de referência: buff 0, stroke 5 como base, tip limitado a 0,2, sem setas decorativas. Normal fina/curta; vetor área mais grosso |
| Boxes | Borda fina, stroke 2, buff 0,26, canto 0,1; resultado domina rótulo de caso e nota auxiliar |
| Transformações | Entradas 0,8–1,4 s; matching usual 1,0–1,3 s por operação; varreduras geométricas 2–4 s. Valores de referência, voz futura manda. Preferir TransformMatchingTex; glyph map apenas se houver ganho didático após estabilizar LaTeX; fade para mudança de significado |
| Saídas | Fade com ~0,8–1,2 s; reter watermark/header no corpo; preservar gaussiana na passagem entre casos; manter respiro de leitura após resultados |
| Payoff | Headline 40 e linha secundária 36, tela limpa, sem tag competindo; watermark discreto até a troca para outro; pausa de 2 s |
| Outro | Logo horizontal oficial `assets/branding/overlays/parallax_lab_logo_horizontal.png`, largura lógica 6, centro `(0,0.6)`; mensagem 28 em `(0,−1.0)`; anéis tracejados discretos; sem links/destinos inventados |

Exceção explícita do briefing ao padrão inicial de `docs/formatos.md`: duração 15–18 min, com tolerância até 19 e teto 20; não atualizar o documento global por essa unidade.

## 19. Briefing consolidado pronto para ficha

**`ficha.md`** consolida classificação curricular, decisão editorial, modelos físicos, arquitetura e portas de implementação por bloco. Fechamento científico/editorial auditado e identificação definitiva resolvida; QA renderizado e sincronização real dependem das etapas indicadas. Este fechamento não autoriza iniciar Manim.
