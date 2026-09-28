# vid_0007 — Campo elétrico no eixo de um anel carregado

- Série pública: **EXERCÍCIO RESOLVIDO · EP. 03**.
- **Concluído em 2026-09-28**; publicação manual pendente (`publicacao.md`). Headline da
  capa: “ONDE O CAMPO ELÉTRICO É MAIS FORTE?”.
  Roteiro com tempos: `roteiro.md`; QA: `revisao.md`.
- Pergunta: onde, no eixo de um anel uniformemente carregado, o módulo do campo é máximo?
- Método: Lei de Coulomb + simetria + integração (sem Lei de Gauss) e derivada para o máximo.
  Passo central: par oposto → laterais se cancelam → axiais se somam.
- Cena: `cena.py`, classe `CampoAnel007`.
- Narração: `audio/narracao_final.wav` (ElevenLabs, 148,0 s, estéreo 44,1 kHz, intacta);
  a cena a toca por `add_sound` e segue seus tempos com `until(...)` (pontos de sincronia
  obtidos pelas pausas medidas no WAV).
- Legenda: `legenda.srt` (54 cues, fala final “Se curtiu, siga o Parallax Lab.”), cores de
  `SUBTITLE_TERM_COLORS` da cena.
- Capa: `capa_instagram.png`, gerada por `gerar_capa.py`: “ONDE O / CAMPO ELÉTRICO /
  É MAIS FORTE?” + painel com o anel carregado (P no máximo, seta do campo, rótulo “anel”)
  e o gráfico E(z) com o pico em magenta; sem fórmula e sem revelar R/√2.
- Finais: `renders/vid_0007_campo_anel_carregado_final_master_limpo.mp4` e
  `renders/vid_0007_campo_anel_carregado_final_legendado.mp4` — 1080×1920, 30 fps,
  4.449 frames, 148,3 s; AAC 44,1 kHz estéreo, 148,0 s.
- Comandos: `uv run python -m manim -r 1080,1920 --fps 30 videos/vid_0007_campo_anel_carregado/cena.py CampoAnel007`;
  `montar_master.py` (render + WAV); `montar_legendado.py … --color-module …/cena.py`;
  `uv run python videos/vid_0007_campo_anel_carregado/gerar_capa.py`.

## Modelo aprovado

- Anel fino de raio R, carga Q > 0 uniforme, no plano xy; P = (0, 0, z), z ≥ 0; k = 1/(4πε₀).
- s² = R² + z² para todo dq; dE = k dq/s²; só a componente axial sobrevive:
  dE_z = dE cos θ, cos θ = z/s ⇒ dE_z = k dq/s² · z/s = kz dq/s³, s³ = (R² + z²)^{3/2}.
- E(z) = kQz/(R² + z²)^{3/2}; E(0) = 0; z ≫ R ⇒ E ≈ kQ/z²; E_z(−z) = −E_z(z).
- dE/dz = kQ(R² − 2z²)/(R² + z²)^{5/2}: + antes, 0 e − depois de z_max = R/√2 ≈ 0,71R
  (E_max = 2kQ/(3√3 R²) ≈ 0,3849 kQ/R², só no QA interno).
- Interno: u = z/R, e(u) = u/(1 + u²)^{3/2}; posição de P, seta do campo e marcador do
  gráfico saem do mesmo `self.u` (um único ValueTracker). Asserts no import conferem
  E(0) = 0, pico em u = 1/√2, sinais da derivada, limite distante, paridade, par oposto
  (laterais opostas, axiais iguais), θ desenhado = arccos(z/s) e pico do gráfico = pico físico.
- Vista pseudo-3D por projeção oblíqua (eixo e diâmetro em verdadeira grandeza); o corte
  lateral (tilt = 0) mostra R, z, s e θ geometricamente fiéis. Sem ThreeDScene.

## Cores e tipografia

Ciano #35D9FF = dq / 1ª contribuição / curva E(z) · Magenta #EA63FF = dq oposto e sua
decomposição; pico da capa · Violeta #745CFF = s, θ, s²·s → s³, raiz → 3/2, numerador da
derivada, sinais e cota do máximo · Branco #F5F7FF = resultante, equações e respostas ·
Azul #267BFF = anel, eixo e geometria. Texto na tela: Space Grotesk Medium
(`screen_text`); matemática em MathTex. Faixa y < −4,6 livre; |x| < 3,5.

## Narração (texto enviado ao ElevenLabs; início medido no WAV)

| Bloco | Início (s) | Fala |
|---|---|---|
| C1 | 0,04 | Onde o campo elétrico de um anel carregado é mais forte? Se você pensou “no centro”, errou: lá ele é zero. Ele cresce, chega a um pico e depois cai. Mas onde fica esse pico? |
| C2 | 11,94 | Temos um anel fino, de raio R, com carga total positiva Q distribuída por igual. O ponto P está a uma distância z do centro. |
| C3 | 20,10 | Pega um pedacinho do anel, um elemento de carga. A distância dele até P é a hipotenusa de um triângulo retângulo: um cateto é o raio, o outro é a altura. Então essa distância ao quadrado é R ao quadrado mais z ao quadrado. E todo pedacinho do anel está a essa mesma distância de P. |
| C4 | 36,76 | Agora vem a simetria. Pra cada pedacinho, existe outro do lado oposto. Os campos dos dois têm partes laterais iguais e opostas, então elas se cancelam. Já as partes ao longo do eixo apontam pro mesmo lado e se somam. No anel inteiro, só sobra o campo no eixo. |
| C5 | 52,52 | Então vamos calcular essa parte pra um pedacinho. Pela lei de Coulomb, o campo que ele cria é k vezes a carga dele, dividido pela distância ao quadrado. Mas só interessa a parte no eixo, e aí entra o cosseno do ângulo com o eixo. No triângulo, cosseno é cateto adjacente sobre hipotenusa: a altura z dividida pela distância. Juntando as duas coisas, aparece mais uma distância embaixo: ao quadrado vezes mais uma, dá ao cubo. E, como a distância é a raiz de R ao quadrado mais z ao quadrado, elevar ao cubo dá R ao quadrado mais z ao quadrado, elevado a três meios. |
| C6 | 86,04 | Agora é só somar o anel inteiro. Temos que o raio e a altura são os mesmos pra todo pedacinho, então saem da soma. Sobra somar as cargas, e isso dá a carga total Q. Pronto: esse é o campo no eixo. |
| C7 | 97,88 | Dois testes rápidos: no centro, z igual a zero dá campo zero. E, visto de muito longe, a expressão vira kQ sobre z ao quadrado: o anel parece uma carga pontual. |
| C8 | 108,57 | Agora acompanha o mesmo ponto no eixo e no gráfico: o campo sai de zero, cresce, passa pelo pico e cai. |
| C9 | 115,38 | Pra achar esse pico, derivamos o campo em relação à altura. O denominador é sempre positivo, então o sinal depende do numerador: R ao quadrado menos dois z ao quadrado. Ele zera quando z é R sobre raiz de dois, e a derivada passa de positiva pra negativa. Aí isso diz que ali é o máximo. |
| C10 | 133,14 | Portanto, o campo é mais forte a R sobre raiz de dois, cerca de zero vírgula setenta e um R acima do plano do anel. |
| C11 | 140,26 | Simetria pra saber o que sobra, integração pra somar as cargas e derivada pra achar o máximo. Se curtiu, siga o Parallax Lab. (na tela: síntese em três passos e @labparallax em 145,91) |

Tempos obtidos por alinhamento às pausas (sem transcrição automática).

## Fora de escopo

Lei de Gauss, potencial elétrico, semieixo negativo na tela, valor de E_max ao público,
distribuições não uniformes.

## Pendências

- Publicação manual pelo usuário; URLs a registrar em `publicacao.md`.
- QA físico em celular e backup externo dos MP4s não confirmados.
- Duração 148,3 s com a voz (o preview silencioso tinha ~122 s; o C5 detalhado e a fala
  definiram o tempo final).
