# Notas da revisão completa (rascunho final4, 14:44) — lista única de ajustes
Lidas as folhas r1_1..r1_36 (0:00–7:11). Falta r1_37..r1_74.
A. 0:05 título→tag: "MAGNETOSTÁTICA" espaçado sobrepõe "PARALLAX LAB" (transição). Sair brand/ask antes.
B. 0:46 cap_obl→cap_per: texto garbled na transição. Trocar por fade.
C. 0:57 fórmula |F_B|=... atravessa a caixa de F_B ao mover. Fade antes de mover.
D. 1:47/1:53 "Newton + Lorentz" cap sobreposto à equação durante transição.
E. 2:13 e2→e3 garbled.
F. 4:13/4:16/4:22 transições da integração/circunferência garbled (b2→b3 com b1 saindo; R1/R2→c2a/c2b; c2a2→sq).
G. 5:14–5:27 "2πR uma volta" colide com órbita/partícula/v⊥ → mover para fora.
H. 5:54 "v⊥ → movimento circular" sobreposto a "nova condição inicial".
J. 7:09 labels "velocidade"/"força magnética" cruzam o círculo → halo.
Lidas r1_37..r1_56 (7:12–11:12):
K. 7:32 (ρ em "V fixo") ok. 7:47 "só a força magnética atua" cruza "energia cinética" (fade-in simultâneo). Fade-out antes.
L. 7:12–7:23 setas dr/vel/F pequenas e sobrepostas na partícula; dr minúsculo (ok, mas halo).
M. 8:11 B⊙ e I ficam longe; ok.
N. 8:21 "dℓ" rótulo sobrepõe quadrado tracejado durante fade. OK.
O. 8:44 "I = dq/dt" transição para λvdt: ReplacementTransform com sobreposição "λ dq dt" ilegível (morph alias) -> usar fade (feito no morph).
P. 8:57–9:07 F = ... transições com termo encostando (I dℓ × B): "dF = I dℓ × B" mostra "λ" fantasma. Corrigido no morph (alias vira fade).
Q. 9:12 "corrente numa linha" + I: ok. 9:16 painel anterior "corrente numa linha" sobreposto a "a linha ganha largura" (c0→c1 ReplacementTransform): trocar por fade.
R. 9:33 c5 vs c4 texto sobreposto ("a superfície ganha espessura" + "J corrente/área"): fade.
S. 9:44 c6b→c7 sobreposto: fade.
T. 10:00–10:08 "mesma interação" + F= ∫ ... : ok. 10:03 transição K×B dA→J×B dτ ilegível.
U. 10:26–10:30 transição frase→equação (variação=entra−sai → dQ/dt): "variação" sobreposta à equação.
V. 10:56–11:00 "fluxo líquido para fora:" e equações com termos sobrepostos na transição.
W. 11:08 B06 ok (volume vivo), setas/células. 

## REVISÃO COMPLETA (r1_1..r1_74, 0:00–14:44) do rascunho final4 — LISTA ÚNICA
Corrigir tudo de uma vez; depois testes locais e UM render final.

A. 0:04–0:05 título→tag: "MAGNETOSTÁTICA" espaçado (letras) sobrepõe "PARALLAX LAB" na troca. -> sair brand/ask/título por fade e entrar tag.
B. 0:48 (q_0047) cap_obl→cap_per: texto garbled na troca. -> fade.
C. 0:57 (q_0057) fórmula |F_B| ... mistura com a caixa da força ao mover: -> fade antes de mover.
D. 1:47–1:51 "Newton + Lorentz" cap sobreposto à equação na entrada, e newton2: ok mas v×B em vermelho no fundo.
E. 1:35–1:45 matriz/determinante: ok. 1:44 "v×B = Bv_z ŷ - Bv_y ẑ" sobreposto durante ReplacementTransform col→res. -> fade/TransformFromCopy já; ok.
F. 2:05–2:10 "derivando a equação de v_y em t" + e1: ok.  2:13 e2→e3 garbled (q_0133). -> fade.
G. 2:36 "derivar 2× ...": ok.
H. 3:12–3:17 troca para painéis: ok; 3:18 "trajetória real" painel: carga pequena fica em cima do arco: ok.
I. 3:36–3:52 sinal de q: OK (dois casos; trilha da carga negativa começa pontilhada = trail cresce; ok).
J. 4:03–4:09 integração: igualdade alinhada OK; primitiva "∫ sin..." está colada na seta v (q_0241 seta atravessa o texto da primitiva!) -> seta v⊥ cruza a equação: o desenho (ox) cresce e v⊥ longo avança sobre a coluna da álgebra. Reduzir escala do diagrama (gs) no trecho 8 ou deslocar RX.
K. 4:12–4:14 (q_0253,0256) ReplacementTransform b2→b3 / R1→c2a: texto garbled. -> usar RT (feito) mas ainda mostra "defina + y..." fantasma: usar fade.
L. 4:21–4:23 sq1/sq2 garbled na troca. -> fade.
M. 4:28–4:30 "R" legenda: ok. 
N. 4:48–4:51 hélice: caixa "a Lorentz não cria v∥" ok (glifo ok).
O. 4:53 volta ao círculo: ok. 4:55 q_0295 F_B/vetor: ok.
P. 5:00 "a força magnética é a força centrípeta" sobrepõe-se ao rótulo v⊥ da partícula em q_0300 (v⊥ perto do título) -> mover título para cima/esquerda? título está em x=1 y=2.5: partícula no alto cruza. Mover título para a coluna direita (x=RX).
Q. 5:06–5:09 centrípeta: strike ok, "|q| B = m v⊥/R" com fantasmas na transição (q_0306,0307: "v⊥" riscado sobreposto) -> aceitável (strike).
R. 5:14–5:27 "2πR uma volta" cruza órbita/partícula/v⊥ (q_0317,0322) -> mover para fora (abaixo do círculo mais baixo, y=-3.0).
S. 5:30 T= transições ok. 5:35 "R1≠R2" ok.
T. 5:51–5:55 (q_0354,0355) "v⊥ → movimento circular" sobreposto a "nova condição inicial" + x(t) (ReplacementTransform row1→newc): fade.
U. 5:57–6:00 "v∥ = constante (já definida)" tem v∥ minúsculo ("v∥" glifo fino vs texto): ok. Pequeno: "v⊥" label do B03 cruza trilha. ok.
V. 6:12–6:14 "p = |v∥| T" ->  p=2πm... transição sobreposta (q_0374): fade.
W. 6:18 q_0378 fade ok.
X. 6:20 "v⊥ ↓, R ↓, p igual" ok.
Y. 7:00–7:11 "A partícula está acelerando..." + painel "v muda de direção" sobrepõe pergunta (q_0415: "v muda de direção" cola na 2ª linha da pergunta) -> mover painel para baixo / pergunta para cima.
Z. 7:07–7:11 labels "velocidade" e "força magnética" no círculo: "F_B força magnética" cruza o círculo (q_0429) -> halo + mover.
