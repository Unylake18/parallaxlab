# HANDOFF — `vid_0024` — implementação Manim 2.5D

## Objetivo desta rodada

Implementar uma **primeira versão completa, visualmente bem resolvida e próxima da versão final** do `vid_0024`, sobre movimento helicoidal de uma carga em campo magnético uniforme.

Não fazer um protótipo mínimo ou uma coleção de cenas provisórias.

A intenção desta rodada é chegar a um **preview completo de ponta a ponta**, já com:

- composição vertical consistente com os vídeos recentes;
- linguagem visual atual do Parallax Lab;
- geometria 2.5D bem resolvida;
- vetores sincronizados com o movimento;
- decomposição visual da velocidade;
- projeção circular;
- avanço longitudinal;
- derivação do raio;
- construção da hélice;
- comparação visual dos parâmetros;
- transições de equações adequadas;
- ritmo visual coerente;
- textos e fórmulas em posições próximas das definitivas.

Depois desta rodada devem restar preferencialmente apenas ajustes pontuais de exposição, ritmo, tamanho, posição, matching de fórmulas ou escolha de alguma transformação MF-Tools.

---

# 1. Contexto já aprovado

## Unidade

- ID: `vid_0024`
- série: `DA EQUAÇÃO AO FENÔMENO`
- episódio público: `EP. 06` ainda provisório
- formato: `curto_vertical`
- título de trabalho: **POR QUE UMA CARGA FAZ UMA HÉLICE?**
- subtítulo: **campo magnético uniforme**
- duração alvo editorial: aproximadamente **2:10–2:50**
- tema: movimento de uma partícula carregada entrando obliquamente em um campo magnético uniforme

## Decisão operacional desta implementação

**`solido_3d: nenhum — Manim 2.5D aprovado para esta implementação.`**

Não investigar nem utilizar:

- Blender;
- `particula_em_campo_magnetico`;
- catálogo do arsenal;
- `Solido3D`;
- `ponte.py`;
- caches do arsenal;
- sequências PNG;
- `.blend`;
- qualquer pipeline Blender → Manim.

Essa é uma decisão específica desta unidade e desta implementação.

Toda a profundidade espacial será construída diretamente no Manim.

---

# 2. Antes de editar

Executar primeiro:

```powershell
git status --short
```

Preservar qualquer modificação já existente.

Depois localizar a unidade do `vid_0024`.

Se ela já existir, usar sua estrutura.

Se ainda não existir, criar uma unidade coerente com a convenção atual, preferencialmente:

```text
videos/vid_0024_carga_helice/
```

com classe de cena:

```python
CargaHelice024
```

Se o repositório já tiver definido outro nome para a unidade, preservar o nome existente em vez de renomear.

---

# 3. Referências visuais obrigatórias antes da implementação

Antes de desenhar a cena do zero, localizar e inspecionar os vídeos recentes:

- `vid_0019`;
- `vid_0020`;
- `vid_0021`.

Usar principalmente:

- `cena.py`;
- `ficha.md`, somente se ajudar a entender decisões visuais;
- helpers locais da unidade, se houver.

Localizar também a unidade recente que contém a parte visual de **“calor absorvido”**, mencionada como referência aprovada.

Não reler todos os vídeos anteriores.

## O que extrair dessas referências

Observar concretamente:

- escala dos textos;
- escala das fórmulas;
- margens;
- respiro vertical;
- posicionamento de títulos e subtítulos;
- linguagem dos painéis;
- caixas ou superfícies translúcidas;
- destaque de resultados;
- largura de traços;
- glow, opacidade e hierarquia visual;
- ritmo de entrada e saída;
- duração aproximada das transformações;
- uso de trackers;
- continuidade entre estados;
- como elementos antigos são apagados antes do próximo foco;
- uso atual de Space Grotesk;
- watermark;
- tratamento do fundo;
- uso recente da paleta;
- densidade visual máxima aceitável no celular.

A intenção não é copiar cenas específicas.

É usar os últimos vídeos como **baseline de qualidade atual do canal**, para que o `vid_0024` não pareça regredir visualmente.

Em especial, aproveitar o que funcionou bem:

- na exposição visual do `vid_0019`;
- nos vídeos `0019–0021` como padrão recente;
- na representação do trecho de “calor absorvido”.

Se esses elementos estiverem implementados por helpers locais úteis e reutilizáveis sem criar dependência estranha, considerar reaproveitar a ideia ou padrão.

Não refatorar vídeos antigos.

---

# 4. Arquivos permitidos nesta rodada

Pode ler:

- `AGENTS.md`;
- arquivos da unidade `vid_0024`;
- `template/config.py`;
- `template/fonts.py`;
- helpers do template necessários;
- `vid_0019`, `vid_0020`, `vid_0021`;
- unidade recente que contenha “calor absorvido”;
- outros arquivos específicos somente se houver uma dependência concreta descoberta durante a implementação.

Pode criar/alterar:

- `videos/vid_0024_*/cena.py`;
- `videos/vid_0024_*/ficha.md`, se necessário para registrar a decisão congelada;
- helpers **locais da própria unidade**, caso realmente reduzam repetição.

Não alterar nesta rodada:

- `template/`;
- `assets/`;
- `pyproject.toml`;
- `uv.lock`;
- `AGENTS.md`;
- documentação global;
- outros vídeos.

---

# 5. Física congelada

Não rediscutir ou substituir o modelo abaixo salvo se encontrar inconsistência objetiva.

Lei de Lorentz magnética:

\[
\vec F=q\,\vec v\times\vec B.
\]

Decomposição:

\[
\vec v=\vec v_\parallel+\vec v_\perp.
\]

Como:

\[
\vec v_\parallel\times\vec B=0,
\]

então:

\[
\boxed{
\vec F=q\,\vec v_\perp\times\vec B
}
\]

Para o movimento transversal:

\[
|q|v_\perp B
=
\frac{mv_\perp^2}{r}
\]

e:

\[
\boxed{
r=\frac{mv_\perp}{|q|B}
}
\]

Frequência angular:

\[
\boxed{
\omega_c=\frac{|q|B}{m}
}
\]

Período:

\[
\boxed{
T=\frac{2\pi m}{|q|B}
}
\]

Passo geométrico da hélice:

\[
\boxed{
p=|v_\parallel|T
=
\frac{2\pi m|v_\parallel|}{|q|B}
}
\]

Energia/rapidez:

\[
\boxed{
\vec F\cdot\vec v=0
}
\]

Não usar a frase “a partícula não acelera”.

Ela possui aceleração quando a direção de \(\vec v\) muda.

A rapidez permanece constante.

---

# 6. Núcleo visual obrigatório

Todo o vídeo deve convergir para esta transformação conceitual:

\[
\boxed{
\vec v
\rightarrow
\vec v_\parallel+\vec v_\perp
\rightarrow
\text{círculo}+\text{translação}
\rightarrow
\text{hélice}
}
\]

Esse é o centro didático da unidade.

A animação não é decoração da álgebra.

O espectador deve literalmente **ver** a hélice surgindo da combinação dos dois movimentos.

---

# 7. Arquitetura Manim 2.5D

## Representação principal

Construir uma cena espacial diretamente no Manim.

Preferência:

- geometria realmente definida em coordenadas 3D;
- câmera fixa levemente inclinada;
- projeção resultante com aparência 2.5D;
- textos e fórmulas críticos fixados no frame;
- sem rotação contínua de câmera.

Pode usar `ThreeDScene`/recursos 3D nativos do Manim se isso produzir o resultado de forma robusta.

A câmera não deve ser protagonista.

Ela serve apenas para tornar simultaneamente perceptíveis:

- profundidade;
- raio;
- avanço longitudinal;
- hélice.

Evitar câmera girando ao redor do fenômeno apenas por estética.

---

# 8. Sistema geométrico recomendado

Para manter a física transparente e permitir trackers, usar preferencialmente:

\[
\vec B=B\,\hat z.
\]

Ou seja, o eixo longitudinal da hélice é o eixo \(z\) da construção matemática.

O enquadramento da câmera pode fazer esse eixo aparecer levemente inclinado na tela.

Não inclinar a física só para inclinar o desenho.

## Modelo normalizado interno

Não mostrar números ao espectador.

É permitido usar internamente valores normalizados, por exemplo:

```python
m = 1
abs_q = 1
```

e controlar:

- `B`;
- `v_perp`;
- `v_parallel`;
- `charge_sign`.

Então:

```python
omega = abs_q * B / m
r = m * v_perp / (abs_q * B)
```

e:

```python
pitch = 2 * PI * abs(v_parallel) / omega
```

---

# 9. Parametrização recomendada da hélice

Usar uma parametrização cuja orientação seja fisicamente consistente com o sinal da carga.

Definir:

\[
s=\operatorname{sgn}(q).
\]

Para fase \(\phi\):

\[
x(\phi)=r\cos\phi,
\]

\[
y(\phi)=-s\,r\sin\phi,
\]

\[
z(\phi)=\frac{v_\parallel}{\omega_c}\phi.
\]

Assim:

- \(q>0\) produz um sentido;
- \(q<0\) produz o sentido oposto;
- inverter `charge_sign` deve inverter a rotação;
- raio e passo não mudam só pela inversão do sinal.

Não desenhar simplesmente uma hélice bonita independente das variáveis físicas.

A geometria deve derivar dos parâmetros.

---

# 10. Vetores sincronizados

Na posição atual da partícula, construir e atualizar:

\[
\vec v_\parallel
\]

na direção de \(\vec B\);

\[
\vec v_\perp
\]

tangente ao círculo transversal;

\[
\vec v
=
\vec v_\parallel+\vec v_\perp;
\]

e, quando didaticamente relevante,

\[
\vec F.
\]

Para a parametrização acima:

\[
\vec v_\perp
\propto
(-\sin\phi,\,-s\cos\phi,\,0)
\]

e:

\[
\vec v_\parallel
=
(0,0,v_\parallel).
\]

A força deve apontar radialmente para o eixo da hélice no caso circular/helicoidal.

Não aproximar visualmente a direção de \(\vec F\) de forma inconsistente.

## Comprimento visual dos vetores

Os vetores devem ter comprimento legível, não necessariamente escala física literal.

Porém:

- direção precisa estar correta;
- decomposição precisa fechar geometricamente;
- mudanças comparativas devem ser coerentes.

Se necessário, usar fator de escala visual explícito no código.

---

# 11. Gramática de cores

Não inventar uma paleta nova.

Usar somente a paleta vigente e, antes de fixar a semântica, verificar como `vid_0019–0021` tratam campos, vetores e destaques.

Objetivo:

- \(\vec v\) total claramente dominante;
- \(\vec v_\parallel\) e \(\vec v_\perp\) claramente distinguíveis;
- \(\vec B\) distinguível das velocidades;
- \(\vec F\) distinguível do campo e da velocidade;
- trajetória visível sem competir com os vetores.

Preferir consistência com os vídeos recentes a inventar uma convenção nova nesta unidade.

Sem novas cores fora da identidade oficial.

---

# 12. Campo magnético visual

Representar \(\vec B\) como conjunto **esparso** de elementos paralelos no espaço.

Pode usar:

- setas;
- linhas com ponta;
- ou outra solução já comprovada nos vídeos recentes.

Objetivos:

1. tornar clara a direção uniforme do campo;
2. criar profundidade;
3. não poluir a tela.

Não desenhar dezenas de setas.

Algo como uma pequena grade espacial, com opacidade baixa e alguns elementos mais evidentes, é preferível.

A partícula, trajetória e vetores devem permanecer hierarquicamente acima do campo.

---

# 13. Recurso visual de projeção — obrigatório

A projeção circular deve ser uma parte real da explicação.

Construir preferencialmente duas leituras sincronizadas da mesma partícula:

## Movimento real

Partícula na hélice.

## Projeção transversal

Criar uma “sombra” ou marcador projetado no plano perpendicular a \(\vec B\).

Esse ponto projetado percorre:

\[
\text{círculo}.
\]

Pode haver:

- plano transversal discreto;
- círculo fantasma;
- marcador projetado;
- linha de projeção de baixa opacidade ligando a partícula ao marcador.

## Avanço longitudinal

Em paralelo, mostrar a coordenada longitudinal avançando ao longo do eixo do campo.

Pode haver:

- linha-eixo central;
- marcador longitudinal;
- projeção da partícula no eixo;
- conector discreto.

O objetivo é o espectador conseguir enxergar simultaneamente:

\[
\text{movimento transversal circular}
\]

e:

\[
\text{movimento longitudinal uniforme}.
\]

Depois recombinar visualmente:

\[
\boxed{
\text{círculo}+\text{translação}=\text{hélice}
}
\]

Esse momento deve ser um dos melhores visuais do vídeo.

---

# 14. Estrutura completa da cena

## BLOCO A — abertura: três trajetórias

Meta aproximada:

```text
0:00–0:18
```

Mostrar no mesmo campo uniforme, de forma rápida e limpa:

### Entrada paralela

\[
\vec v\parallel\vec B
\]

\[
\vec F=0
\]

trajetória reta.

### Entrada perpendicular

\[
\vec v\perp\vec B
\]

trajetória circular.

### Entrada oblíqua

\[
v_\parallel\neq0,
\qquad
v_\perp\neq0
\]

trajetória helicoidal.

Preferência visual:

usar o **mesmo palco/campo**, mudando apenas a condição de entrada, em vez de criar três mini-aulas independentes.

Pode mostrar rótulos curtos:

```text
paralela
perpendicular
oblíqua
```

Terminar mantendo a hélice na tela.

Pergunta:

**“O mesmo campo magnético pode produzir três trajetórias diferentes. Por quê?”**

Evitar layout abarrotado de três painéis permanentes.

---

# 15. BLOCO B — Lei de Lorentz e trabalho nulo

Meta:

```text
0:18–0:35
```

Apresentar:

\[
\vec F=q\,\vec v\times\vec B
\]

com o estado espacial ainda visível.

Depois destacar:

\[
\boxed{
\vec F\cdot\vec v=0
}
\]

Texto/ideia:

**“A força magnética nunca tem componente na direção instantânea do movimento.”**

Quando \(\vec F\neq0\):

- mostrar \(\vec v\);
- mostrar \(\vec F\);
- evidenciar ortogonalidade.

Não usar visual que sugira que \(\vec F=0\) possui direção.

Não transformar essa parte em aula de produto vetorial ou regra da mão direita.

---

# 16. BLOCO C — decomposição da velocidade

Meta:

```text
0:35–1:00
```

Este é o **ponto visual mais importante do vídeo**.

Congelar ou desacelerar a partícula em um ponto visualmente bom da hélice.

Mostrar inicialmente apenas:

\[
\vec v.
\]

Depois decompor geometricamente:

\[
\boxed{
\vec v
=
\vec v_\parallel+\vec v_\perp
}
\]

A decomposição deve ser visível no próprio espaço, não somente como MathTex.

Idealmente:

1. \(\vec v\) aparece tangente à hélice;
2. surge a componente paralela ao campo;
3. surge a componente transversal;
4. as duas compõem exatamente o vetor original;
5. rótulos aparecem próximos dos vetores sem cobrir a geometria.

Depois mostrar:

\[
\vec v_\parallel\times\vec B=0.
\]

Pode visualmente reduzir/destacar essa componente.

Então chegar a:

\[
\boxed{
\vec F
=
q\,\vec v_\perp\times\vec B
}
\]

A mensagem precisa ser visual:

- \(v_\parallel\) → avanço;
- \(v_\perp\) → curvatura.

Não resolver isso apenas com textos.

---

# 17. BLOCO D — nascimento do círculo

Meta:

```text
1:00–1:28
```

Dar destaque temporário à projeção transversal.

A hélice pode perder opacidade enquanto o círculo projetado ganha prioridade.

Mostrar no círculo:

- partícula;
- velocidade tangencial;
- força radial para o centro;
- raio \(r\).

Construir:

\[
|q|v_\perp B
=
\frac{mv_\perp^2}{r}
\]

e transformar em:

\[
\boxed{
r=\frac{mv_\perp}{|q|B}
}
\]

## Transformação matemática

Usar primeiro a solução mais robusta:

- `TransformMatchingTex`, se a correspondência estiver clara;
- `TransformByGlyphMap`, somente se trouxer ganho didático real e o LaTeX já estiver estabilizado;
- `FadeOut/FadeIn`, se matching induzir movimento enganoso.

Não usar MF-Tools só para deixar bonito.

A conta deve parecer limpa e atual, no nível dos vídeos recentes.

---

# 18. BLOCO E — reconstrução da hélice

Meta:

```text
1:28–1:52
```

Essa é a recompensa da explicação.

Reintroduzir simultaneamente:

- círculo projetado;
- avanço longitudinal;
- partícula real.

Fazer os três estados compartilharem **a mesma fase**.

Mostrar claramente que, enquanto:

- a projeção gira;
- a coordenada longitudinal avança;

a partícula real percorre a hélice.

Construir visualmente a frase:

\[
\boxed{
\text{círculo}+\text{translação}=\text{hélice}
}
\]

Não simplesmente escrever a frase sobre uma hélice já pronta.

A composição deve demonstrá-la.

Depois introduzir o período:

\[
T=\frac{2\pi m}{|q|B}
\]

e o passo:

\[
p=|v_\parallel|T.
\]

## Marcação do passo

Mostrar duas posições da partícula separadas por uma volta completa.

Marcar a distância longitudinal entre elas:

\[
p.
\]

Não confundir o passo com comprimento de arco da hélice.

---

# 19. BLOCO F — parâmetros

Meta:

```text
1:52–2:25
```

Esse bloco deve ter qualidade visual alta.

Usar trackers e manter a mesma composição.

Alterar **uma variável por vez**.

## 19.1 Aumentar \(B\)

Visual:

- raio reduz;
- passo reduz;
- hélice fica mais “fechada”.

Matemática de apoio:

\[
r\propto\frac1B,
\qquad
p\propto\frac1B.
\]

Evitar impressão de que apenas o raio muda.

---

## 19.2 Aumentar \(v_\perp\)

Visual:

- raio aumenta;
- distância longitudinal por volta permanece a mesma se \(v_\parallel,B,q,m\) não mudarem.

Destacar:

\[
r\propto v_\perp
\]

e:

\[
T=\frac{2\pi m}{|q|B}
\]

portanto:

**“o período não muda.”**

Esse é um payoff importante.

---

## 19.3 Aumentar \(v_\parallel\)

Visual:

- raio permanece igual;
- passo aumenta;
- hélice alonga no eixo do campo.

Mostrar:

\[
p\propto|v_\parallel|.
\]

---

## 19.4 Inverter o sinal de \(q\)

Fazer a comparação visual mais limpa possível.

O sentido de rotação deve inverter.

Não alterar:

- raio;
- período;
- módulo do passo.

Pode usar:

```text
q > 0
```

→

```text
q < 0
```

com mudança do sentido da trajetória.

Não é necessário explicar regra da mão direita.

---

# 20. Implementação dos trackers

A arquitetura deve permitir controlar, idealmente:

```python
B_tracker
v_perp_tracker
v_parallel_tracker
charge_sign
phase_tracker
```

Não é obrigatório que `charge_sign` seja `ValueTracker` contínuo, porque fisicamente queremos dois estados discretos \(+1\) e \(-1\).

Pode fazer a inversão por transformação entre duas geometrias se isso for visualmente mais estável.

## Performance

Não criar dezenas de `always_redraw` pesados sem necessidade.

Priorizar:

- uma curva principal;
- partícula;
- poucos vetores;
- poucas projeções;
- campo esparso.

Se reconstruir uma `ParametricFunction` a cada frame ficar pesado:

1. reduzir densidade de pontos;
2. limitar quantidade de elementos dependentes de tracker;
3. usar curvas pré-computadas para estados comparativos;
4. transformar entre estados.

Qualidade visual > virtuosismo técnico.

---

# 21. BLOCO G — síntese final

Meta:

```text
2:25–2:45
```

Limpar progressivamente a tela.

Construir:

\[
\boxed{
v_\perp\Rightarrow\text{círculo}
}
\]

depois:

\[
\boxed{
v_\parallel\Rightarrow\text{translação}
}
\]

e finalmente:

\[
\boxed{
v_\perp+v_\parallel
\Rightarrow
\text{hélice}
}
\]

Sempre que possível, cada linha deve estar acompanhada da representação visual correspondente.

Fechar na hélice completa.

Frase conceitual final prevista:

**“A hélice é a geometria da força de Lorentz virando movimento.”**

Não implementar CTA novo se a unidade ainda não tiver CTA aprovado.

---

# 22. Layout vertical

Formato:

```text
9:16
```

Preview:

```text
540×960 / 15 fps
```

Usar `template/config.py`.

Preservar faixa inferior para legendas futuras.

Evitar colocar conteúdo crítico muito próximo:

- da borda inferior;
- do topo;
- das laterais.

## Hierarquia sugerida

Durante os estados espaciais:

- zona superior: pergunta, frase curta ou equação principal;
- região central: fenômeno 2.5D;
- região inferior-média: fórmula secundária ou interpretação;
- faixa inferior real: livre.

Não deixar simultaneamente:

- título;
- quatro vetores;
- fórmula longa;
- legenda conceitual;
- painel comparativo;
- labels de todos os parâmetros.

Fazer limpeza entre estados.

---

# 23. Tipografia

Texto não matemático:

- Space Grotesk Medium via solução vigente do template/repositório.

Matemática:

- `MathTex`.

Usar os vídeos recentes para calibrar os tamanhos reais.

Não reduzir uma equação importante só para caber.

Se necessário:

- quebrar em dois estados;
- ocultar elementos espaciais;
- reposicionar a geometria.

---

# 24. Acabamento visual esperado

A primeira versão já deve buscar:

- fundo consistente;
- watermark correto;
- hierarquia clara;
- ausência de elementos default crus;
- opacidades refinadas;
- espessuras coerentes;
- labels bem ancorados;
- equações centralizadas;
- transições suaves;
- ausência de objetos “pulando” entre posições;
- ausência de vetores atravessando textos;
- ausência de trajetória passando sobre fórmulas;
- continuidade espacial entre os blocos.

A hélice deve parecer parte do design do Parallax Lab, não um gráfico 3D padrão do Manim.

---

# 25. Uso do 2.5D

Não tentar produzir realismo.

Queremos:

**profundidade matemática legível.**

Preferir:

- linhas limpas;
- baixo número de objetos;
- plano transversal discreto;
- guias com opacidade reduzida;
- trilha principal luminosa;
- partícula clara;
- vetores muito legíveis.

Evitar:

- malhas 3D;
- eixos cartesianos completos;
- grids 3D;
- perspectiva exagerada;
- câmera muito inclinada;
- elementos escondidos atrás uns dos outros;
- profundidade que dificulte ler \(r\) ou \(p\).

---

# 26. Continuidade visual

Não recriar a hélice do zero em cada bloco se for possível manter o mesmo objeto conceitual.

Preferir continuidade:

```text
entrada oblíqua
→ congelamento
→ vetores
→ projeção
→ círculo
→ hélice recomposta
→ parâmetros
→ síntese
```

O espectador deve sentir que está examinando **o mesmo sistema físico por perspectivas diferentes**.

Isso é melhor do que sete slides animados independentes.

---

# 27. MF-Tools

MF-Tools 1.4.9 está disponível, mas é seletivo.

Nesta unidade:

### Considere para

- derivação do raio;
- reorganização de alguma expressão;
- cancelamento ou movimentação de termos se realmente ficar melhor.

### Não usar por obrigação

Para:

\[
\vec F=q\vec v\times\vec B
\]

→

\[
\vec F\cdot\vec v=0
\]

não fingir que uma expressão “vira” a outra por matching se isso não representa uma transformação algébrica real.

Nesse caso, usar mudança de foco/Fade.

Para a decomposição:

\[
\vec v
=
\vec v_\parallel+\vec v_\perp
\]

o principal deve ser a **decomposição geométrica dos vetores**, e o MathTex entra como síntese.

Não substituir o recurso visual por morph de símbolos.

---

# 28. Sem exemplo numérico

Decisão congelada:

**não adicionar exemplo numérico.**

Não usar:

- elétron com valor de carga;
- massa do elétron;
- campo de `0,x T`;
- raio em metros;
- frequência em Hz;
- valores arbitrários como parte do conteúdo.

Valores internos de implementação podem existir, mas não devem aparecer como exercício.

---

# 29. QA físico específico durante a implementação

Antes de renderizar o preview completo, conferir no código e visualmente:

### Caso paralelo

\[
v_\perp=0
\Rightarrow
\vec F=0
\]

e trajetória reta.

### Caso perpendicular

\[
v_\parallel=0
\]

e trajetória circular.

### Caso oblíquo

ambas não nulas → hélice.

### Força

No círculo/hélice:

- \(\vec F\) perpendicular a \(\vec v\);
- componente radial para dentro.

### \(B\uparrow\)

- \(r\downarrow\);
- \(p\downarrow\).

### \(v_\perp\uparrow\)

- \(r\uparrow\);
- \(T\) não muda.

### \(v_\parallel\uparrow\)

- \(p\uparrow\);
- \(r\) não muda.

### \(q\to-q\)

- rotação inverte;
- \(r\) não muda;
- \(T\) não muda;
- passo geométrico não muda.

### Passo

Medir longitudinalmente uma volta completa, não ao longo da curva.

---

# 30. QA visual específico

No preview completo verificar especialmente:

1. abertura com três casos;
2. primeiro frame da hélice;
3. frame da ortogonalidade;
4. decomposição de \(\vec v\);
5. estado com os três vetores;
6. projeção circular;
7. força centrípeta;
8. fórmula do raio;
9. círculo + translação simultâneos;
10. marcação de \(p\);
11. estado antes/depois de aumentar \(B\);
12. estado antes/depois de aumentar \(v_\perp\);
13. estado antes/depois de aumentar \(v_\parallel\);
14. inversão de \(q\);
15. síntese final.

Checar:

- clipping;
- labels;
- sobreposição;
- perspectiva;
- tamanho em celular;
- legibilidade de fórmulas;
- profundidade;
- se a hélice parece efetivamente uma hélice e não uma senoide 2D;
- se o círculo projetado é compreensível;
- se \(r\) e \(p\) parecem grandezas diferentes;
- se os vetores permanecem presos à partícula.

---

# 31. Validação técnica mínima

Primeiro:

```powershell
uv run python -m py_compile videos/vid_0024_*/cena.py
```

ou equivalente robusto para o caminho real.

Depois fazer **um preview completo**:

```powershell
uv run python -m manim -r 540,960 --fps 15 videos/vid_0024_*/cena.py CargaHelice024
```

Ajustar o comando se a unidade/classe já possuir nome aprovado diferente.

Não renderizar 1080×1920 nesta rodada.

O objetivo é um preview 540×960/15 fps suficientemente acabado para revisão editorial/visual.

---

# 32. Pode corrigir antes de entregar

Se o primeiro preview revelar um problema objetivo evidente, por exemplo:

- clipping;
- vetor no sentido errado;
- câmera ruim;
- rótulo ilegível;
- equação sobreposta;
- hélice achatada demais;
- campo poluído;
- trackers quebrando geometria;

corrigir e rerenderizar o **mesmo preview afetado** antes de entregar.

Não entregar um erro óbvio só porque “é primeira versão”.

Ao mesmo tempo, não entrar em um ciclo infinito de refinamento cosmético.

---

# 33. Não fazer

Nesta rodada não:

- gerar voz;
- gerar SRT;
- montar master;
- montar legendado;
- produzir capa;
- publicar;
- renderizar final 1080×1920;
- alterar dependências;
- alterar template global;
- alterar identidade visual;
- usar Blender;
- consultar/integrar arsenal 3D;
- criar automação;
- criar branch por conta própria;
- fazer PR;
- commit;
- push;
- refatorar vídeos antigos;
- atualizar documentação global;
- introduzir exemplo numérico;
- mudar a física ou narrativa aprovada por preferência própria.

---

# 34. Critério de qualidade desta rodada

Não considerar a tarefa concluída apenas porque “a cena renderiza”.

A rodada só está concluída quando houver um preview completo em que já seja possível avaliar seriamente o vídeo como produto.

A primeira versão deve permitir responder:

- a decomposição vetorial ficou clara?
- o 2.5D realmente ajuda?
- dá para perceber círculo + translação simultaneamente?
- o raio é entendido?
- o passo é entendido?
- os parâmetros modificam a geometria corretamente?
- a composição está no nível visual dos vídeos recentes?
- o resultado parece um vídeo atual do Parallax Lab?

A intenção é que a revisão seguinte seja de **refinamento**, não de reconstrução.

---

# 35. Condição de parada

Pare quando:

1. `cena.py` estiver implementada de ponta a ponta;
2. a decisão `solido_3d: nenhum` estiver respeitada;
3. o preview vertical completo tiver sido renderizado;
4. os estados críticos acima tiverem sido inspecionados;
5. erros objetivos encontrados nessa inspeção tiverem sido corrigidos;
6. nenhuma etapa posterior de produção tiver sido iniciada.

---

# 36. Relatório obrigatório de entrega

Ao terminar, reportar de forma objetiva:

### Arquivos alterados
Listar caminhos.

### Referências recentes consultadas
Dizer quais partes de `vid_0019`, `vid_0020`, `vid_0021` e/ou da unidade de “calor absorvido” serviram de referência visual.

Não dizer apenas “usei como referência”; informar brevemente o que foi reaproveitado como linguagem:

- composição;
- painel;
- trackers;
- equações;
- transições;
- tipografia;
- etc.

### Implementação
Resumir:

- geometria da hélice;
- campo;
- partícula;
- vetores;
- projeções;
- trackers;
- parâmetros;
- transições matemáticas.

### Validações
Informar:

- `py_compile`;
- render realizado;
- duração do preview;
- resolução/fps;
- estados visuais inspecionados.

### Caminho do preview
Informar caminho exato.

### Pontos ainda passíveis de refinamento
Somente pendências reais observadas.

Não iniciar outra fase.