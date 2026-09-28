# vid_0005 — Roteiro visual e narração sincronizada

Preview 540×960/15 fps com a narração ElevenLabs (`audio/narracao_final.wav`,
127,23 s, intacta); vídeo de 128,0 s. Os tempos abaixo são segundos do WAV e
correspondem aos `self.until(...)` da cena; os pontos de sincronia foram
obtidos alinhando as frases às pausas medidas no áudio.

Encadeamento central: v₋, v₊ → Δv → triângulos semelhantes → Δt → 0 → a_c = v²/R.

Terminologia: “módulo da velocidade” para |v| = v; “vetor velocidade” ou
“velocidade tangencial” para a seta. Nenhum texto diz que a velocidade é constante.

| Bloco | Tempo (s) | Visual | Texto na tela |
|---|---|---|---|
| A. Gancho | 0–25,2 | Círculo, partícula em órbita uniforme com v de comprimento fixo; \|v\| = constante em 7,0; direção em 14,6. Microexplicação: três cópias de v (16,4–17,9), MESMO MÓDULO (17,9), DIREÇÃO DIFERENTE (18,9), manchete em 20,1. | “Se o módulo da velocidade não muda, por que existe aceleração?” · \|v\| = constante · “a direção de v muda” · MESMO MÓDULO · DIREÇÃO DIFERENTE · “O vetor velocidade muda” |
| B. Dois instantes | 25,2–43,1 | A partícula retoma o ritmo e congela P₋ e P₊ (≈28,4 e 29,4); r± em 30,6; v± em 32,9; ângulos retos em 36,5; Δθ em 39,9; Δr (corda) em 41,0. | “Dois instantes próximos” · t± = t ± Δt/2 · v± ⊥ r± · Δr = r₊ − r₋ |
| C. Construção de Δv | 43,1–62,5 | Painel da origem comum; translações puras de v₋ e v₊ (44,5–47,3); mesmo Δθ; pontas em 50,2; Δv de ponta a ponta em 51,0; rótulo em 53,4; raio e cópia radial de Δv em 57,8–61,5. | “Variação do vetor velocidade” · Δv = v₊ − v₋ · “Com instantes simétricos, Δv aponta para o centro” |
| D. Semelhança | 62,5–78,9 | Painéis POSIÇÃO e VELOCIDADE (63,5–65,9); “escalas” destacado em 67,0; R ↔ v em 68,8; \|Δr\| ↔ \|Δv\| em 70,6; mesmo Δθ em 73,2; razão termo a termo em 75,3; vira equação das taxas em 77,7. | “Triângulos semelhantes” · “MESMA FORMA · ESCALAS DIFERENTES” · \|Δv\|/v = \|Δr\|/R → \|Δv\|/Δt = (v/R)·\|Δr\|/Δt |
| E. Limite | 78,9–109,3 | Posição: P± se aproximam em 81,3 (Δθ 50° → 16°); v tangente e primeiro limite em 84,0. Velocidade: painel em 89,4, encolhe, segundo limite ≈92. Ponte em 95,7 e 98,9. Substituição em 102,7; a_c = v²/R em 105,2; moldura em 108,0. | “Instantes cada vez mais próximos” · Δt → 0 · \|Δr\|/Δt → \|v\| = v · \|Δv\|/Δt → a_c · “posição muda → velocidade” · “velocidade muda → aceleração” · a_c = (v/R)·v = [v²/R] |
| F. Direção centrípeta | 109,3–124,8 | Círculo com v tangente e a_c para o centro, órbita uniforme até 124,0 (termina no topo); v ⊥ a_c em 114,2; síntese em 119,8. | “Aceleração centrípeta” · v ⊥ a_c · [a_c = v²/R] · “O módulo não muda; o vetor muda.” |
| CTA | 124,8–128,0 | A fórmula emoldurada sai e @labparallax (corpo 30) entra no mesmo lugar. | @labparallax |

## Narração (texto usado no ElevenLabs)

| Início (s) | Fala |
|---|---|
| 0,1 | Se o módulo da velocidade não muda, por que ainda existe aceleração? No movimento circular uniforme, o tamanho do vetor velocidade permanece o mesmo. Mas observa: conforme a partícula percorre a circunferência, a direção do vetor muda. Então, módulo constante não significa vetor constante. E é justamente essa mudança de direção que vamos medir. |
| 25,5 | Agora pegamos dois instantes próximos. Em cada ponto temos um vetor posição, de módulo R, e uma velocidade tangencial, de módulo v. Como velocidade e raio são perpendiculares, o mesmo delta theta aparece nos dois pares. |
| 43,1 | Então, colocamos as duas velocidades com a mesma origem, sem girar nenhuma delas. A seta que vai da ponta de v menos até a ponta de v mais é delta v: a variação do vetor velocidade. |
| 57,9 | E, com instantes simétricos, delta v aponta para o centro. |
| 62,8 | Agora vem a chave. Os dois triângulos têm a mesma forma, só mudam de escala. R corresponde a v, e delta r a delta v. Como delta theta é o mesmo, a semelhança nos dá essa proporção. |
| 78,0 | Então fazemos os instantes se aproximarem: delta t tende a zero. Primeiro, delta r sobre delta t tende ao módulo da velocidade, v. Depois, delta v sobre delta t tende à aceleração centrípeta. Ou seja: posição mudando por tempo dá velocidade; velocidade mudando por tempo dá aceleração. Substituindo na relação anterior, chegamos a a c igual a v ao quadrado sobre R. |
| 109,5 | Essa é a aceleração centrípeta: ela aponta para o centro e é perpendicular à velocidade tangencial. Então, fica tranquilo observar: o módulo da velocidade não muda, mas o vetor muda. Se curtiu, siga o Parallax Lab. |

Faixa inferior (y < −4,6 na área lógica) livre para legendas futuras.
