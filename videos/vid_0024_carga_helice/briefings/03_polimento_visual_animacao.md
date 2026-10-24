# HANDOFF — `vid_0024` — rodada de polimento visual/animação

## Objetivo

Refinar o preview atual do `vid_0024` para aproximá-lo fortemente da versão visual final.

A estrutura física, narrativa e didática está aprovada. **Não reconstruir o vídeo nem trocar sua arquitetura.**

Esta rodada deve melhorar principalmente:

- qualidade e presença visual do campo magnético;
- cores e luminosidade;
- continuidade das animações;
- ritmo das transições;
- álgebra;
- MF-Tools onde trouxer ganho didático;
- sobreposição de variáveis, formas e textos;
- integração entre gráficos e fenômeno;
- comparações de parâmetros;
- fechamento;
- CTA final silencioso somente com `@labparallax`.

O objetivo é sair de uma sequência de bons estados estáticos e chegar a uma **animação contínua, elegante e visualmente viva**.

---

# 1. Estado aprovado que deve ser preservado

Manter:

- Manim 2.5D;
- `solido_3d: nenhum`;
- campo magnético uniforme;
- hélice paramétrica;
- semântica física atual;
- decomposição:
  \[
  \vec v=\vec v_\parallel+\vec v_\perp;
  \]
- projeção circular;
- círculo + translação = hélice;
- derivação do raio;
- período;
- passo;
- comparações de \(B\), \(v_\perp\), \(v_\parallel\);
- inversão de \(q\);
- síntese final.

Não adicionar exemplo numérico.

Não usar Blender ou arsenal.

---

# 2. Diagnóstico do preview atual

O preview está com aproximadamente 168 s.

A estrutura funciona, mas há uma alternância indesejada entre:

1. momentos quase completamente estáticos;
2. transições abruptas para outro estado.

Exemplos observados de pouca atividade visual:

- ~36–39 s;
- ~58–60 s;
- ~70–72 s;
- ~111–113 s;
- ~131 s;
- ~140 s;
- ~153 s;
- ~166 s.

Mudanças visualmente abruptas aparecem especialmente em torno de:

- ~15–16 s;
- ~34–35 s;
- ~39–40 s;
- ~61–63 s;
- ~88–91 s;
- ~114–116 s;
- ~123–125 s;
- ~131–133 s;
- ~141–143 s;
- ~154–155 s;
- ~166–167 s.

Não interpretar esses timestamps como necessidade de corte novo. São pontos para rever a coreografia.

---

# 3. Princípio geral de animação desta rodada

Não deixar o vídeo parecer:

```text
estado A
→ corte/fade
→ estado B
→ pausa
→ estado C
```

Preferir:

```text
estado A
→ objeto existente se transforma
→ perspectiva muda
→ informação nova nasce da anterior
→ estado B
```

A partícula, a trajetória e o sistema físico devem fornecer continuidade entre os blocos sempre que possível.

## Ritmo

Evitar tanto:

- transições de 0,2–0,4 s em que tudo muda simultaneamente;
- quanto pausas de 2–3 s em que nada visualmente relevante acontece.

Como referência geral:

- entrada/saída simples: ~0,4–0,7 s;
- transformação conceitual importante: ~0,8–1,3 s;
- transformação algébrica importante: permitir leitura antes da próxima operação.

Não aplicar esses tempos mecanicamente. Ajustar pelo que precisa ser compreendido.

---

# 4. Campo magnético — elevar bastante o acabamento

O campo atual está correto, mas visualmente apagado e esparso demais.

Aumentar presença sem competir com a partícula.

## Construção sugerida

Usar aproximadamente 8–12 vetores/linhas de campo distribuídos em profundidade, não somente poucos traços longos.

Criar 2–3 camadas de profundidade:

- camada frontal: maior opacidade;
- camada intermediária: média;
- camada traseira: mais discreta.

Manter todos paralelos.

Usar azul elétrico vigente.

## Aparência

Dar aos elementos principais do campo:

- stroke um pouco mais luminoso;
- arrowheads mais reconhecíveis;
- contraste suficiente no celular.

Criar, se funcionar bem no Manim, um efeito de brilho simples por duplicação:

- linha externa mais grossa e baixa opacidade;
- linha principal mais fina e saturada por cima.

Não usar blur externo nem efeitos caros desnecessários.

## Animação de entrada

Na abertura, fazer o campo se montar em cascata curta:

```text
GrowArrow / Create
```

com pequeno `LaggedStart`.

Depois o campo deve permanecer estável.

**Não animar as linhas como se o campo estivesse “fluindo”.**

O campo é uniforme e constante. Movimento decorativo contínuo nas linhas poderia sugerir dinâmica física inexistente.

---

# 5. Campo como variável física

No bloco \(B\uparrow\), fazer o próprio campo participar visualmente.

Quando \(B\) aumenta:

- aumentar moderadamente comprimento das setas e/ou espessura/brilho;
- preservar a quantidade de setas;
- simultaneamente reduzir raio e passo da hélice.

Assim o espectador vê:

```text
B aumenta
→ representação de B fica mais forte
→ hélice fecha
```

Não usar quantidade de linhas como principal representação da intensidade se isso ficar parecendo densidade literal de “linhas físicas”.

---

# 6. Trajetória e partícula — mais vivas

A hélice ciano funciona bem.

Elevar o acabamento com:

- stroke principal mais vivo;
- halo discreto por uma cópia mais espessa/baixa opacidade atrás;
- partícula mantendo o glow atual ou equivalente;
- z-index consistente.

Hierarquia:

```text
partícula
> vetores
> trajetória principal
> projeções/guias
> campo
> trajetória fantasma de comparação
```

A trajetória cinza de referência deve permanecer claramente secundária.

---

# 7. Evitar sensação de “fotografia”

Quando uma fórmula estiver sendo discutida, o sistema físico não precisa congelar completamente.

Usar movimentos sutis e relevantes:

- partícula continua avançando lentamente;
- vetores continuam acompanhando a partícula;
- cursor do gráfico continua acompanhando a fase;
- projeção circular continua girando;
- marcador longitudinal continua avançando.

Não movimentar tudo ao mesmo tempo.

A ideia é manter **vida física**, não criar distração.

Quando o foco exigir concentração total na álgebra, pode congelar a geometria por alguns instantes — mas então a álgebra precisa estar efetivamente se transformando.

---

# 8. Bloco inicial

O gancho atual:

**“Qual é a trajetória de uma carga em um campo magnético?”**

está bom e deve ser preservado.

Melhorar visualmente a sequência:

```text
reta
→ círculo
→ hélice
```

usando o mesmo espaço físico.

Evitar sensação de três exemplos desconectados.

Preferir a mesma partícula reaparecendo/reconfigurando sua condição de entrada.

Campo já deve estar visualmente bonito desde aqui.

Nos três casos, tornar mais clara a relação da direção inicial de \(\vec v\) com \(\vec B\).

---

# 9. Bloco força e direção — manter e elevar

A região ~20–35 s é boa.

Manter:

- \(\vec v\) branco;
- \(\vec F\) magenta;
- \(\vec B\) azul;
- trajetória ciano.

Fazer os vetores acompanharem a partícula com transições suaves.

Evitar qualquer frame em que o vetor parece se soltar da partícula.

---

# 10. Gráficos de velocidade e força

O painel atual de aproximadamente ~28–34 s é uma boa adição. Preservar a ideia e refiná-la.

Hoje há:

- componente de velocidade;
- componente da força;
- cursor vertical.

Tornar essa relação ainda mais visual.

## Sincronização

Usar a **mesma fase** da partícula para:

- movimento sobre a hélice/círculo;
- vetor \(\vec v\);
- vetor \(\vec F\);
- posição do cursor no gráfico;
- ponto destacado sobre cada curva.

Adicionar pequenos pontos móveis nas curvas correspondentes ao instante atual.

Isso transforma o gráfico em outra perspectiva do mesmo fenômeno, e não em gráfico decorativo.

## Física

Se forem componentes:

- rotular explicitamente como \(v_x(t)\), \(F_x(t)\), ou os componentes realmente usados;
- não sugerir que \(|\vec v|\) ou \(|\vec F|\) são senoidais.

Os módulos permanecem constantes neste modelo.

Verificar que as curvas são calculadas a partir da mesma parametrização física da cena e que sua defasagem está correta.

---

# 11. Campo magnético no painel gráfico

Adicionar somente se couber com boa legibilidade.

Pode existir uma terceira faixa bem fina em azul:

\[
B(t)=B_0
\]

como linha horizontal.

Não criar um terceiro gráfico grande.

A mensagem é simplesmente:

```text
componentes de v e F variam
B permanece constante
```

Se tornar o painel poluído, não adicionar. Prioridade continua sendo velocidade + força sincronizadas.

---

# 12. Melhorar a retirada dos gráficos

Atualmente, perto de ~34–35 s, o painel de gráficos desaparece rapidamente e o sistema volta ao espaço 2.5D.

Fazer uma transição mais elegante:

1. desacelerar/finalizar um ciclo do cursor;
2. curvas perdem opacidade;
3. painel se recolhe/fade;
4. partícula/helix recuperam protagonismo;
5. \(\vec F\cdot\vec v=0\) permanece como síntese.

Não apagar gráfico, vetores e textos todos no mesmo frame.

---

# 13. Decomposição da velocidade

Esse continua sendo o bloco mais importante.

Manter a boa ideia atual, mas aumentar:

- separação visual dos componentes;
- espessura;
- saturação;
- clareza dos labels.

Semântica cromática definitiva:

- \(\vec v\): branco;
- \(\vec v_\parallel\): ciano;
- \(\vec v_\perp\): violeta;
- \(\vec F\): magenta;
- \(\vec B\): azul.

Usar as mesmas cores nos termos das equações.

---

# 14. Decomposição deve ser construída, não apenas exibida

Mostrar claramente:

1. \(\vec v\) sozinho;
2. nasce \(\vec v_\parallel\);
3. nasce \(\vec v_\perp\);
4. linhas/guias fecham o triângulo;
5. equação aparece:
   \[
   \vec v=\vec v_\parallel+\vec v_\perp.
   \]

Pode usar:

- guia tracejada;
- tip-to-tail;
- paralelogramo;
- pequeno marcador de perpendicularidade.

Não deixar componentes se sobreporem à trajetória ou ao label da partícula.

---

# 15. Posicionamento de labels e z-order

Há estados no preview em que:

- labels chegam perto de vetores;
- anotações \(r,p,r_0,r_1,p_0,p_1\) competem com a hélice;
- fórmula do bloco anterior permanece durante a entrada do seguinte.

Corrigir sistematicamente.

## Regra

Rótulo matemático nunca deve ficar diretamente sobre:

- partícula;
- arrowhead;
- outra variável;
- trecho importante da curva.

Se necessário, mover labels para overlays fixos de tela e deixar somente a geometria no espaço 3D.

Usar z-index explícito.

Sugestão:

```text
textos/fórmulas overlay: maior z_index
partícula
vetores
trajetória principal
marcadores
trajetórias comparativas
campo
painéis
```

---

# 16. Transição para a vista perpendicular

Atualmente ~61–63 s ocorre uma mudança rápida de hélice 2.5D para o círculo.

Tornar essa transição um momento didático.

Em vez de quase trocar de cena:

1. destacar a projeção transversal violeta;
2. reduzir opacidade da dimensão longitudinal;
3. fazer a hélice “achatar” visualmente / transformar-se na projeção;
4. centralizar o círculo;
5. só então trocar o título.

O espectador deve perceber:

**“Estamos olhando apenas a componente perpendicular.”**

Não parecer que apareceu um novo desenho sem relação com a hélice anterior.

---

# 17. Título desse bloco

Trocar:

**“Vista perpendicular ao campo”**

por:

**“No plano perpendicular a \(\vec B\)”**

ou, se encaixar melhor no layout:

**“A componente transversal faz um círculo”**

Preferência:

**“No plano perpendicular a \(\vec B\)”**

porque descreve exatamente a projeção.

---

# 18. Círculo transversal

Melhorar distinção:

- \(v_\perp\): violeta tangencial;
- \(\vec F\): magenta radial;
- \(r\): linha geométrica branca/cinza fina;
- círculo: violeta luminoso;
- centro: ponto discreto.

Hoje \(r\) e \(\vec F\) ficam próximos cromaticamente em alguns estados.

Corrigir.

---

# 19. Álgebra do raio — problema objetivo atual

Entre aproximadamente ~69–79 s existem frames em que glifos antigos e novos se sobrepõem.

Durante:

\[
|q|v_\perp B=\frac{mv_\perp^2}{r}
\]

→ multiplicação por \(r\);

→ cancelamento de \(v_\perp\);

→ isolamento de \(r\),

aparecem ghostings e formas intermediárias visualmente confusas.

Isso precisa ser corrigido.

---

# 20. Nova coreografia algébrica do raio

Construir claramente:

\[
|q|v_\perp B
=
\frac{mv_\perp^2}{r}
\]

pausa curta.

Depois:

\[
|q|v_\perp Br
=
mv_\perp^2.
\]

Animar o \(r\) saindo do denominador e multiplicando o lado esquerdo.

Depois escrever \(v_\perp^2\) de forma que os dois fatores sejam reconhecíveis:

\[
mv_\perp\cdot v_\perp.
\]

Destacar os dois \(v_\perp\) que serão cancelados.

Risco visual atual: vários glifos atravessam uns aos outros simultaneamente.

Evitar.

---

# 21. Cancelamento com MF-Tools

Aqui `TransformByGlyphMap` faz sentido.

Fazer o cancelamento em uma etapa própria.

Exemplo visual:

1. ambos \(v_\perp\) ficam mais brilhantes;
2. aparecem riscos curtos de cancelamento;
3. breve hold;
4. os termos cancelados desaparecem;
5. restante se reorganiza para:

\[
|q|Br=mv_\perp.
\]

Não mover simultaneamente todos os outros símbolos.

Não usar `auto_morph`.

Usar `auto_fade` ou transformações explícitas quando necessário.

---

# 22. Isolamento de \(r\)

Depois:

\[
|q|Br=mv_\perp
\]

mostrar \(|q|B\) deslocando-se de maneira controlada ao denominador:

\[
r=\frac{mv_\perp}{|q|B}.
\]

Esse movimento é outro bom candidato a `TransformByGlyphMap` com `path_arc` moderado.

Não usar o estado intermediário visualmente confuso atual:

\[
r=mv_\perp\cdot\frac1{|q|B}
\]

a menos que a transformação realmente fique mais clara dessa forma.

Minha preferência é ir diretamente para a fração final.

Final:

\[
\boxed{
r=\frac{mv_\perp}{|q|B}
}
\]

com o círculo ainda se movendo lentamente ao fundo.

---

# 23. Tempo da álgebra

Não acelerar o trecho só para economizar segundos.

Melhor:

- menos estados;
- estados mais claros;
- transições mais lentas.

Eliminar pausas estáticas compensa o tempo adicional das transformações.

---

# 24. \(\omega_c\) e \(T\) — corrigir

No preview atual, perto de ~100 s:

\[
\omega_c=\frac{|q|B}{m}
\]

e:

\[
T=\frac{2\pi m}{|q|B}
\]

entram praticamente prontos e permanecem muito pouco.

Isso é rápido demais.

Construir visualmente:

\[
\omega_c=\frac{v_\perp}{r}.
\]

Usar o resultado anterior:

\[
r=\frac{mv_\perp}{|q|B}.
\]

Então:

\[
\omega_c
=
\frac{v_\perp}
{mv_\perp/(|q|B)}.
\]

Destacar e cancelar \(v_\perp\).

Chegar em:

\[
\boxed{
\omega_c=\frac{|q|B}{m}
}
\]

Depois:

\[
T=\frac{2\pi}{\omega_c}
\]

→

\[
\boxed{
T=\frac{2\pi m}{|q|B}
}.
\]

Não precisa permanecer longamente.

Mas o espectador deve conseguir enxergar **por que \(v_\perp\) desaparece**.

Esse cancelamento é justamente o que prepara o payoff posterior:

**o período não depende de \(v_\perp\).**

---

# 25. Círculo + translação = hélice

Esse bloco continua sendo um dos melhores.

Preservar.

Melhorar apenas a continuidade:

- mesmo phase tracker;
- ponto circular;
- ponto longitudinal;
- partícula na hélice;
- linhas de projeção.

Os três devem se mover simultaneamente.

A relação:

\[
\text{círculo}+\text{translação}=\text{hélice}
\]

deve parecer demonstrada pela animação.

---

# 26. Construção do passo \(p\)

O trecho ~111–113 s fica estático demais.

Em vez de manter a imagem parada enquanto a fórmula final está na tela:

1. marcar posição inicial \(t_0\);
2. partícula realiza uma volta;
3. marca \(t_0+T\);
4. seta/bracket de \(p\) cresce entre as duas posições longitudinais;
5. fórmula acompanha:

\[
p=|v_\parallel|T.
\]

Depois transformar para:

\[
p=\frac{2\pi m|v_\parallel|}{|q|B}.
\]

Assim a geometria continua animada durante a álgebra.

---

# 27. Mudança para os blocos de parâmetros

Atualmente as transições entre:

- campo mais intenso;
- mais velocidade transversal;
- mais velocidade paralela;

ainda parecem em alguns momentos:

```text
limpa cena
→ novo título
→ nova comparação
```

Melhorar continuidade.

Usar **a mesma hélice-base** como estado inicial de todos.

No fim de uma comparação, voltar suavemente ao baseline antes de mudar de variável — ou transformar diretamente usando parâmetros, sem apagar a geometria.

---

# 28. \(B\uparrow\)

Animar simultaneamente:

- setas de \(\vec B\) ficando mais fortes;
- hélice reduzindo raio;
- passo reduzindo;
- trajetória anterior ficando como ghost cinza;
- rótulos \(r_0,r_1,p_0,p_1\) aparecendo somente depois da geometria já estar legível.

Relações:

\[
r\propto\frac1B,
\qquad
p\propto\frac1B.
\]

Evitar rótulos sobrepostos ao início/fim das curvas.

---

# 29. \(v_\perp\uparrow\)

Fazer o vetor violeta \(\vec v_\perp\) crescer visivelmente.

Ao mesmo tempo:

- raio aumenta continuamente;
- passo permanece igual;
- \(T\) permanece igual.

Relações:

\[
r\propto v_\perp
\]

e:

\[
T=\text{constante}.
\]

A comparação deve ser uma transformação contínua, não apenas duas hélices prontas.

---

# 30. \(v_\parallel\uparrow\)

Fazer o vetor ciano \(\vec v_\parallel\) crescer.

Simultaneamente:

- raio permanece exatamente igual;
- hélice alonga;
- passo aumenta.

Mostrar geometricamente:

\[
p\propto|v_\parallel|.
\]

Deixar um marcador de raio constante ajuda.

---

# 31. Corrigir resíduos entre blocos

No preview atual, perto de ~123–125 s e ~131–133 s, relações matemáticas do bloco anterior permanecem durante o início do próximo.

Também acontece novamente na transição ~154–155 s para a síntese.

Regra:

**o título novo não deve entrar enquanto fórmula principal do bloco antigo ainda está ocupando a tela, salvo se ela estiver sendo deliberadamente transformada na nova relação.**

Fazer:

```text
fórmula velha encerra/fade
→ geometria volta ao baseline
→ título muda
→ nova variável entra
```

ou uma transformação explícita entre relações.

---

# 32. Inversão de \(q\)

O bloco funciona conceitualmente, mas pode ficar mais bonito e contínuo.

Evitar reiniciar quase do zero.

Mostrar:

```text
mesma posição
mesma v
mesmo B
```

Primeiro:

\[
q>0.
\]

Mostrar \(\vec F\) magenta.

Depois:

\[
q\rightarrow -q.
\]

A seta \(\vec F\) deve girar/inverter sua direção de forma visível.

Só então o traçado da trajetória muda de handedness/sentido.

Resultado visual:

```text
F inverte
→ curvatura inverte
→ sentido de giro inverte
```

Preservar:

\[
r,\quad T,\quad |p|
\]

iguais.

Pode adicionar um pequeno arco/seta indicando sentido de rotação.

---

# 33. Mais cor sem virar carnaval

Não mudar a paleta.

Aumentar presença das cores existentes.

Usar:

- ciano: trajetória/resultante;
- azul: campo;
- violeta: componente transversal/círculo;
- magenta: força;
- branco: velocidade total/equações estruturais;
- cinza: estado anterior/guias.

Aumentar principalmente:

- saturação;
- opacidade dos elementos principais;
- contraste;
- strokes;
- halo suave.

Não adicionar amarelo, verde, laranja etc.

---

# 34. Fundos/painéis

Os painéis atuais são muito discretos, o que é bom, mas alguns quase desaparecem.

Quando o painel tiver função geométrica real:

- aumentar levemente seu contorno/opacidade;
- manter fundo translúcido;
- não criar cards pesados.

O painel da projeção circular pode ter uma leve borda violeta/azulada de baixa opacidade.

O painel de gráficos pode ter uma borda neutra muito sutil.

---

# 35. Transições de texto e título

Evitar títulos aparecendo como cortes secos.

Usar transições pequenas e elegantes:

- `FadeTransform`;
- deslocamento vertical de poucos pixels/unidades;
- crossfade;
- transform quando palavras se relacionarem.

Não fazer grandes swoops.

O foco continua na física.

---

# 36. Síntese final

Preservar a estrutura:

\[
v_\perp\Rightarrow\text{círculo}
\]

\[
v_\parallel\Rightarrow\text{translação}
\]

\[
v_\perp+v_\parallel\Rightarrow\text{hélice}.
\]

Melhorar a coreografia.

Em vez de mostrar três exemplos como cenas quase independentes:

1. começar com partícula;
2. ativar só \(v_\perp\) → círculo;
3. transformar para só \(v_\parallel\) → reta;
4. juntar visualmente os dois componentes;
5. a reta + círculo reconstruem a hélice.

No estado final:

\[
\vec v=\vec v_\parallel+\vec v_\perp
\]

aparece com cores correspondentes.

Fechar com:

**“Giro transversal + avanço paralelo = hélice.”**

---

# 37. Corrigir transição ~154–155 s

Atualmente o título da síntese começa enquanto ainda há informação residual da comparação de sinal.

Fazer o bloco de \(q\) terminar completamente antes da síntese.

O espectador deve sentir uma pausa de conclusão curta, não uma colisão de dois assuntos.

---

# 38. Encerramento / CTA

Depois da síntese, adicionar um end card silencioso.

Decisão:

**mostrar apenas**

`@labparallax`

Nada além.

Não mostrar:

- “me siga”;
- “siga”;
- “acompanhe”;
- logo + texto adicional;
- chamada falada;
- segunda linha.

## Visual

Fundo escuro limpo.

Centralizar:

**@labparallax**

em Space Grotesk.

Aplicar degradê usando a paleta da marca, preferencialmente:

```text
ciano → violeta → magenta
```

Pode usar:

```python
set_color_by_gradient(...)
```

ou equivalente.

Adicionar no máximo:

- FadeIn suave;
- scale de aproximadamente 0.96 → 1.00;
- glow muito discreto, se ficar elegante.

Não fazer animação chamativa.

## Timing sugerido

Após o fechamento conceitual:

- fade do sistema: ~0,4–0,6 s;
- entrada do `@labparallax`: ~0,4–0,6 s;
- hold limpo: ~1,3–1,8 s;
- fade final: ~0,3–0,5 s.

Sem narração nesse end card.

O watermark de canto deve desaparecer antes ou durante a entrada do handle para não haver `Parallax` duplicado.

---

# 39. Duração

O preview atual tem aproximadamente 168 s.

Não há problema em terminar próximo de 168–172 s após adicionar o end card.

Não estender artificialmente.

Recuperar tempo eliminando:

- holds estáticos;
- redundâncias;
- estados algébricos intermediários pouco úteis.

Investir o tempo recuperado em:

- melhores transforms;
- leitura de \(\omega_c/T\);
- transições mais respiradas.

---

# 40. MF-Tools

Revisar especificamente a álgebra.

Usar seletivamente:

### `TransformMatchingTex`
Padrão para:

- relações simples;
- substituições com correspondência natural.

### `TransformByGlyphMap`
Usar principalmente para:

1. cancelamento de \(v_\perp\) na derivação do raio;
2. movimento de \(|q|B\) para denominador;
3. cancelamento de \(v_\perp\) em \(\omega_c\), se ficar mais claro.

### `FadeOut/FadeIn`
Usar quando um matching seria semanticamente falso.

Não usar `auto_morph`.

Não deixar glifos duplicados/ghosts na meia-transição.

---

# 41. Sobreposição e clipping — revisão obrigatória

Revisar especialmente:

- ~69–79 s: álgebra do raio;
- labels de \(r\) e \(\vec F\) na projeção circular;
- \(r_0/r_1\) e \(p_0/p_1\) nos parâmetros;
- ~123–125 s;
- ~131–133 s;
- ~141–143 s;
- ~154–155 s;
- síntese final.

Nenhuma variável deve:

- atravessar outra variável;
- ficar embaixo de seta;
- ficar sobre a partícula;
- competir com título;
- continuar na tela depois de o assunto ter mudado.

---

# 42. Não fazer

Não:

- mudar física;
- adicionar exemplo numérico;
- adicionar novo bloco conceitual;
- usar Blender;
- investigar arsenal;
- alterar dependências;
- alterar template global;
- voz;
- SRT;
- master final;
- capa;
- publicação;
- commit;
- push.

Esta rodada é somente refinamento do preview Manim.

---

# 43. Validação

Rodar `py_compile`.

Renderizar um preview completo:

```powershell
540×960
15 fps
```

Inspecionar especialmente:

- 0–20 s;
- 20–40 s;
- 40–63 s;
- 63–85 s;
- 88–116 s;
- 116–142 s;
- 142–155 s;
- 155–fim.

Também inspecionar frames intermediários das transformações algébricas, não somente começo/fim.

Isso é importante porque o problema atual está justamente na meia-transição de alguns glifos.

---

# 44. Critério de parada

A rodada termina quando:

1. campo estiver visualmente mais presente;
2. trajetória e vetores tiverem acabamento mais vivo;
3. transições principais estiverem coreografadas;
4. sensação de “slides/fotografias” tiver sido reduzida;
5. álgebra do raio estiver limpa;
6. \(\omega_c\) e \(T\) estiverem visualmente construídos e legíveis;
7. resíduos entre blocos tiverem sido eliminados;
8. parâmetros variarem de maneira contínua;
9. síntese final estiver mais fluida;
10. end card silencioso com somente `@labparallax` estiver implementado.

---

# 45. Relatório de entrega

Reportar:

- arquivos alterados;
- transições refeitas;
- melhorias no campo;
- melhorias de cor/stroke/glow;
- MF-Tools usados e em quais equações;
- gráficos alterados;
- sobreposições corrigidas;
- duração nova;
- caminho do preview;
- timestamps ainda considerados passíveis de refinamento.

Não iniciar etapa posterior.