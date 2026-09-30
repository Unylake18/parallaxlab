# vid_0008 — Roteiro visual e narração sincronizada

Narração ElevenLabs (`audio/narracao_final.wav`, 152,3 s, intacta); vídeo de 152,7 s.
A cena segue a voz por âncoras (`sync.json`): cada âncora casa um ponto do código com um
instante do áudio, e `play`/`wait` entre duas âncoras são escalados para o trecho durar o que
a fala dura. Os instantes foram obtidos alinhando as frases às pausas medidas no WAV (sem ASR).

Arco: geometria → Biot-Savart → simetria → projeção axial → elemento de arco → encaixe dos
fatores → soma da volta → checagem em z = 0 → checagem de z ≫ R → gancho (muitas espiras).
Cores: ciano = R e componente axial · azul = z · violeta = r · ciano claro = dℓ e corrente ·
magenta = operação (cancelamento, substituição, ângulo, transversal) · branco = campo e resultados.

| Bloco | Tempo (s) | Visual | Texto na tela |
|---|---|---|---|
| A1 Gancho | 0,05–7,9 | Espira; ponto de luz percorre o fio (corrente); P surge no eixo com um pulso. | DE ONDE VEM O CAMPO MAGNÉTICO DE UMA ESPIRA? · QUAL É O CAMPO AQUI? |
| A2 Geometria | 7,9–22,8 | R, z, r e o ângulo reto; os rótulos voam e montam r² = R² + z²; vira a ficha GEOMETRIA. | COMEÇA PELA GEOMETRIA |
| A3 Biot-Savart | 22,8–37,3 | dB = (μ₀I/4π)(dℓ × r)/r³; dℓ ⟂ r; r³ = r²·r; os dois r (magenta) cancelam → \|dB\| = (μ₀I/4π) dℓ/r²; ficha BIOT-SAVART. | BIOT-SAVART · o seno de 90 graus vale 1 |
| A4 Simetria | 37,3–54,4 | Elemento oposto; transversais (magenta) se fecham → 0; axiais deslizam ponta a ponta → 2 dB_z; segue-se com um. | ELEMENTOS OPOSTOS · TRANSVERSAIS CANCELAM · AXIAIS SOMAM |
| A5 Projeção axial | 54,4–72,2 | Mesmo α em P e no triângulo; dB_z/\|dB\| = cos α = R/r; slot em \|dB\|, a ficha BIOT-SAVART abre grande e devolve o valor. | SÓ SOBRA O EIXO · MESMO ÂNGULO |
| A6 Arco | 72,2–80,7 | Vista de frente cresce; dφ abre; o arco se desenrola: dℓ = R dφ; ficha ARCO. | ARCO = RAIO VEZES ÂNGULO |
| A7 Encaixe | 80,7–97,7 | Slot em dℓ, ARCO devolve R dφ; R·R → R²; r²·r → r³; slot em r³, GEOMETRIA devolve (R²+z²)^{3/2}. | ENCAIXA AS PEÇAS |
| A8 Soma a volta | 97,7–117,3 | B_z = ∫dB_z com o marcador percorrendo a espira; fatores saem da integral; ∫dφ = 2π; os π cancelam; 2/4 → 1/2 → B_z(z). | SOMA A VOLTA |
| A9 Checagem z = 0 | 117,3–128,6 | P vai ao centro (z em tempo real); (R²)^{3/2} → R³; R²/R³ → 1/R; B_z(0) = μ₀I/2R; gráfico B_z/B_z(0) com o pico. | CHECAGEM: z = 0 |
| A9B Muito longe | 128,6–142,5 | P sobe o eixo até z = 7R; R² + z² ≃ z² (R² magenta some); B_z ≃ μ₀IR²/2z³; B_z ∝ 1/z³; o dot desce a curva. | E MUITO LONGE? · z ≫ R |
| A10 Fechamento | 142,5–152,7 | A fórmula geral vira a ficha UMA ESPIRA; a espira é copiada 1 → 2 → 3; @labparallax. | E SE FOREM MUITAS? |

## Narração (texto usado no ElevenLabs)

Essa fórmula do campo magnético de uma espira costuma aparecer pronta. Mas ela não surge do nada: dá para construir tudo, passo a passo.

Começa pela geometria. O raio, a distância axial até o ponto e a distância do trecho do fio até o ponto formam um triângulo retângulo. Por Pitágoras, essa última ao quadrado é o raio ao quadrado mais a distância axial ao quadrado. Guarda isso.

Agora entra Biot-Savart, que dá o campo de cada trecho. O trecho do fio é perpendicular à reta que o liga ao ponto, então o produto vetorial simplifica. Reescrevendo a distância ao cubo como distância ao quadrado vezes distância, um fator cancela.

Agora a simetria. Para cada trecho do fio, existe outro exatamente do lado oposto da espira. Os campos dos dois têm componentes transversais iguais e opostas, e elas se cancelam. As componentes axiais apontam para o mesmo lado e se somam. Então basta calcular um trecho e dobrar.

Quanto disso aponta ao longo do eixo? Essa fração é o cosseno do ângulo mostrado na tela, e é o mesmo ângulo que aparece no ponto e no triângulo. Pela geometria, ele é o raio dividido pela distância do trecho ao ponto. Então a parte axial é o campo do trecho vezes essa razão, e esse campo a gente já guardou.

Falta o tamanho do trecho. Visto de frente, ele é um pequeno arco da circunferência. E o comprimento de um arco é o raio vezes o ângulo que ele abre.

Agora encaixa. O tamanho do trecho vira raio vezes ângulo. Os dois raios formam raio ao quadrado. Embaixo, distância ao quadrado vezes distância dá distância ao cubo. E a relação guardada troca isso por raio ao quadrado mais distância axial ao quadrado, elevado a três meios.

Agora soma a volta inteira. Ao redor da espira, o raio, a corrente e a posição do ponto não mudam, então saem da integral. O que sobra é integrar o ângulo em uma volta completa, e isso dá dois pi. Dois pi sobre quatro pi: os pi cancelam, dois sobre quatro vira um meio. E aparece o campo magnético no eixo da espira.

Confere no centro. Leva o ponto até o centro da espira: a distância axial vai a zero, e o campo vira mi zero vezes a corrente, sobre duas vezes o raio. No gráfico, é o máximo.

E muito longe, ainda no eixo? Quando a distância axial fica bem maior que o raio, o raio perde importância, e o denominador vira a distância axial ao cubo. Por isso, longe da espira, o campo cai com um sobre essa distância ao cubo.

Uma espira está entendida. E se forem muitas? No próximo vídeo, a gente soma várias espiras e chega ao solenoide. Se curtiu, siga o Parallax Lab.

Texto e inícios medidos por bloco em `ficha.md`. Faixa inferior (y < −4,6 na área lógica)
livre para legendas.
