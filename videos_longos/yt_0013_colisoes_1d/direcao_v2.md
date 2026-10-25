# yt_0013 — direção v2 (decisões locais e notas para a futura voz)

Fonte: `HANDOFF_CLAUDE_CODE_V2.md` + `REVISAO_CRITICA.md` (24/10/2026). A v2 reabre didática e direção visual por
pedido do usuário; a progressão C01–C12 e o escopo físico ficam. Preview v1 (Blender em C01/C03) preservado em
`renders/yt_0013_preview_960x540_15fps.mp4`; código v1 em `cena_v1_backup.py`.

## Decisões locais
- **Sem Blender nesta unidade.** Corpos 2.5D em Manim: face frontal (referência de contato e medidas) + faces
  superior/lateral decorativas. Massas por rótulo, nunca pelo tamanho.
- **Paleta:** corpo 1 azul `#267BFF` (símbolos `#4D93FF`), corpo 2 violeta `#745CFF` (símbolos `#9C8CFF`), K e
  resultado ativo ciano, energia convertida em interna magenta `#EA63FF`, U_g violeta claro com rótulo. Sem laranja/amarelo.
- **Um estado físico por cena:** posição, setas, barras e gráficos leem o mesmo relógio (`ValueTracker`).
  Contato instantâneo; em C02 o intervalo do contato é ampliado no tempo com força F ∝ sen(πs), e as setas de momento
  integram a mesma lei (área do gráfico = impulso trocado = 16/3 kg·m/s).
- **Pêndulo bifilar** (bloco não gira). Subida integrada (RK4, sem dissipação) com m = 20 g, M = 980 g, L = 1,0 m,
  h = 0,20 m → V ≈ 1,980 m/s, u ≈ 99,0 m/s, θ_max = 36,87°, K_B/K_A = 2 % (barra real, sem fator gráfico).
- **Teaser 2D:** plano sem trilho, discos de massas iguais, contato oblíquo a 45°: u₁ = (2,0), u₂ = 0 →
  v₁ = (1,−1), v₂ = (1,1); P e K fecham.
- Seleção de trechos: `SECOES=c10,c11` funciona isolada (C11 reconstrói o estado B).

## Intenções de fala novas/corrigidas (frases curtas; não é roteiro)
- **C01:** "Mesmas massas, mesmas velocidades iniciais… e três finais." "O que muda é a interação durante o contato."
  Fechar com "O que falta saber sobre o contato?" — sem equação ainda.
- **C02 (notação):** "m é massa; u, velocidade antes; v, depois; o índice diz qual corpo." "Para a direita é positivo;
  para a esquerda, negativo." "Momento é p = m v." "Somamos com sinal: +4 com −2 dá +2."
- **C02 (impulso):** "Durante o contato, os dois trocam momento: o que um ganha, o outro perde." "Impulso é o efeito
  acumulado da força no intervalo." "Intervalo curto não basta: o que importa é o impulso externo na horizontal ser
  desprezível." "No modelo ideal, tomamos esse impulso como zero — e só então escrevemos igualdade."
  Dica: "Escolha sistema, eixo e intervalo antes de escolher a conservação."
- **C03 (K):** "K é ½ m v²; não fica negativa; o quadrado apaga o sinal." "K é a energia do movimento dos corpos;
  aquecimento e deformação contam como energia interna."
- **C03 (suficiência):** "Elástica dá a segunda equação: K se conserva. Ficar junto também: as velocidades são iguais.
  Mas dizer só 'inelástica' dá uma desigualdade — restringe, não fecha." Síntese: "momento + uma condição adicional
  suficiente". "Completamente inelástica é um caso particular das inelásticas; K final não precisa ser zero."
- **C04:** "Ficar junto vira v₁ = v₂ = v_f." "Fator comum… dividimos pelos dois lados, por m₁ + m₂, que é positivo."
  "É uma média ponderada: pesos positivos que somam 1; v_f fica entre as velocidades iniciais e pode ser negativa."
- **C05:** "Metade da velocidade significa metade da energia?" "A massa em movimento dobra, mas a velocidade ao quadrado
  cai a um quarto." "1 J vira energia interna — não some."
- **C06:** "Por que as duas valem: impulso externo desprezível dá o momento; colisão elástica dá a energia."
  "Multiplicamos os dois lados por 2." "Diferença de quadrados, um lado de cada vez." "Não dividimos: usamos (1) dentro
  de (2)." "Produto nulo, com m₁ positivo: um dos outros fatores é zero."
  **Ramo trivial:** "Velocidades iguais às iniciais: nenhuma transferência líquida de momento. Não é o encontro com
  interação que estamos resolvendo." (não dizer "não houve colisão" como verdade geral)
  **Relativa:** "d é a distância entre os centros. Antes, diminui u₁ − u₂ por segundo; depois, aumenta v₂ − v₁."
  "O que se inverte é a velocidade relativa — cada corpo não precisa inverter a sua."
- **C07:** "Isolar v₂ e substituir o bloco inteiro." "Distributiva: m₂ multiplica cada termo — e o sinal de −m₂u₂ vem de
  −u₂." "Agrupar, fator comum, dividir por m₁ + m₂." "Para v₂: cada colchete vira um único coeficiente."
  "Valem para colisão elástica em 1D; coeficientes sem unidade."
- **C08:** previsão → simplificação → movimento → confere. "No leve contra pesado, o pesado ainda se move (2/31 de u₁)."
  "No pesado contra leve, o leve quase dobra a velocidade: recebe energia do pesado; nada é criado."
- **C09:** "Dá para descobrir a velocidade do projétil medindo a altura?" "u: projétil antes; V: conjunto logo depois."
  "Estados A, B e C." "Pergunte o que acontece em cada intervalo."
- **C10:** "Sistema projétil + bloco. Peso e tensões são verticais; no impacto breve, o impulso externo horizontal é
  desprezível." "Ficou preso: velocidade comum, como no caso que fica junto." "K não se conserva: sobra só 2 %."
- **C11:** hipóteses (sem ar, suportes sem atrito, fios ideais, bloco sem giro); "a tensão é perpendicular ao
  deslocamento e não realiza trabalho"; "o momento NÃO se conserva na subida"; "U_g = 0 no estado B";
  "cancelamos (m + M), multiplicamos por 2"; "raiz positiva porque V é o módulo da velocidade para a direita";
  "de trás para frente: h → V → u"; checagens de unidade e plausibilidade.
- **C12:** método ligado aos exemplos; síntese "sistema + intervalo + conservação válida + condição suficiente";
  teaser: "e quando os corpos podem sair em direções diferentes?".
