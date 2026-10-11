# Preview silencioso V5 — POR TRÁS DA FÓRMULA · EP. 07

Unidade: vid_0020_integral_dupla_volume. Revisão didática da integração e limite;
f(x,y)=4−x²−y² e R=[−1,1]² preservados. Apenas roteiro visual, sem voz.

1. **A superfície nasce nos eixos.** Cabeçalho e logo no padrão de vid_0011.
   Construir x/y/z e a região; traçar a superfície ciano. Gancho temporário
   e integral dupla. Rótulo z=f(x,y)=4−x²−y² aponta para a malha. Uma
   vertical central associa z à altura. A referência permanece visível.
2. **A base gera ΔA.** Dividir em 4×4. Destacar a célula sem deslocá-la.
   “Fixe uma célula” → “A base vale ΔA”. Cópia ampliada permite ler Δx e Δy;
   os rótulos geram ΔA=ΔxΔy.
   A ampliação sai; a célula original permanece no mesmo domínio.
3. **A função determina a altura.** Marcar o ponto médio (x_i,y_j).
   “A altura vem da função f”. Vertical magenta alcança a superfície e marca
   a interseção. A seta de
   altura e f(x_i,y_j) nascem desse encontro. Só então a célula extruda.
   Volume violeta gera ΔV, altura copia f(x_i,y_j), base copia ΔA.
   Fórmula: ΔV≈f(x_i,y_j)ΔA, com as mesmas cores da geometria.
4. **Repetir a regra.** “Repita em cada célula”. Outras quinze colunas crescem em onda até suas
   alturas de pontos médios. A inicial conserva destaque durante a
   repetição, depois assume estilo comum. A expressão de uma coluna
   transforma-se em Σ_{i,j}f(x_i,y_j)ΔA.
5. **Refinar sob a mesma função.** Superfície, eixos, domínio e projeção
   fixos. Cruzar os topos marca a divisão de cada mãe em quatro filhas,
   primeiro coplanares ao topo antigo. Seus topos movem-se para f nos
   novos pontos médios. Repetir 4→8→16→32, com durações decrescentes.
   Acrescentar brevemente 64×64: 4.096 topos de altura exata agrupados,
   com faces de fronteira e degraus expostos; omitir faces internas ocultas.
   Mostrar n crescente, Δx/Δy decrescentes, Δx=Δy=2/n e ΔA=4/n².
   Em 64×64, ΔA=4/4096=1/1024.
   Fechar com n→∞ e ΔA=ΔxΔy→0. MF-Tools transporta operador, função e
   medida do somatório para a integral; os indicadores explicitam o limite.
6. **A seção produz uma área.** Reduzir opacidade das colunas. Inserir
   x=x_0, traçar z=4−x_0²−y². “Primeiro, integramos em y”: marcador e
   vertical magenta percorrem y de −1 a 1 enquanto a área ciano-claro se
   preenche. A seção gera A(x_0)=∫ de −1 a 1 f(x_0,y)dy; destacar dy.
   “Uma área para cada x”: generalizar A(x), mantendo a fórmula visível.
   “Depois, acumulamos em x”: o plano avança, deixando seções suaves,
   enquanto V=∫A(x)dx entra em violeta-claro. Destacar dx. Copiar o bloco
   interno diretamente da expressão de A(x) para o lugar correspondente
   na integral externa. Limpar as fontes após a cópia, sem fórmulas residuais.
7. **Conta construída em duas etapas.** Diminuir e atenuar temporariamente
   a geometria; manter a integral externa como contexto discreto.
   Isolar ∫(4−x²−y²)dy. “x fica constante”. Separar em
   (4−x²)∫dy−∫y²dy, mantendo os limites −1 e 1.
   Revelar os apoios ∫dy=y e ∫y²dy=y³/3 por cópias dos termos ativos.
   Montar (4−x²)y−y³/3 a partir desses apoios; acrescentar colchetes e limites.
   Mostrar separadamente a substituição y=1 e y=−1. Simplificar cada linha,
   subtrair os dois valores, agrupar em 2(4−x²)−2/3, expandir para
   8−2x²−2/3 e obter A(x)=22/3−2x² por transformação.
   Retomar a seção destacada: “Agora temos a área da seção para cada x”.
   “Depois, integramos em x”: copiar A(x) para V=∫A(x)dx e depois seus
   termos para V=∫(22/3−2x²)dx. Separar os termos da integral.
   Mostrar ∫(22/3)dx=22x/3 e ∫2x²dx=2x³/3; montar a primitiva por cópias,
   depois acrescentar limites. Mostrar x=1: 22/3−2/3=20/3 e
   x=−1: −22/3+2/3=−20/3. Copiar os resultados para
   V=20/3−(−20/3) → (20+20)/3 → 40/3≈13,33.
   MF-Tools preserva fatores na separação, avaliação e simplificação;
   TransformFromCopy monta regras/primitivas e transporta o resultado A(x).
8. **Payoff em movimento.** Colunas refinadas crescem sob a referência
   fixa. Destacar a superfície. A geometria gera V=∬_R f(x,y)dA.
   Retomar ΔV→ΣΔV→∬_R f dA. “Somar pequenas contribuições sobre toda a área.”
   Registrar f>0 em R.

O sistema não muda de projeção entre célula, coluna, refinamento e seção.
Na seção, a casca curva exata substitui as colunas densas para revelar a área.
O payoff usa 16×16 para leitura das colunas; o limite já foi apresentado em 64×64.
Base/região/ΔA são ciano; função local, magenta; volume, violeta;
integração em y, ciano-claro; integração em x, violeta-claro.
Pausas curtas; cada movimento explica uma relação. Não descrever dA como
infinitésimo literal nem justificar a integral iterada contando variáveis.
