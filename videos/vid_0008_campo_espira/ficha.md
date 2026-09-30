# vid_0008 — Campo magnético no eixo de uma espira

- Série pública: **POR TRÁS DA FÓRMULA · EP. 03**.
- **Concluído tecnicamente em 2026-09-30; publicação não registrada.** Roteiro com tempos:
  `roteiro.md`; QA: `revisao.md`.
- Origem: o `vid_0008` nasceu como um preview combinado (espira + solenoide, 174,7 s) que foi
  **dividido em dois vídeos independentes** (decisão de 2026-09-30, ver `docs/decisoes.md`):
  este é o primeiro; o solenoide é o `vid_0009_campo_solenoide`.
- Pergunta: de onde vem B_z(z) = μ₀IR²/2(R²+z²)^{3/2} para um ponto no eixo de uma espira?
- Método: Biot-Savart + simetria + integração. Passo central: elemento oposto → transversais
  se cancelam → axiais se somam; dℓ = R dφ; r³ = (R²+z²)^{3/2}; ∫₀²π dφ = 2π; 2π/4π = 1/2.
  Checagens: z = 0 (B = μ₀I/2R) e z ≫ R (B ≃ μ₀IR²/2z³, B ∝ 1/z³).
- Cena: `cena.py`, classe `CampoEspira008`; base local `comum.py` (modelo físico, paleta,
  template de cor no LaTeX, fichas, halo). Cópia irmã em `vid_0009_campo_solenoide/comum.py`,
  que divergiu de propósito (cada pasta é autocontida).
- Narração: `audio/narracao_final.wav` (ElevenLabs, 152,3 s, estéreo 44,1 kHz, intacta).
  A cena segue a voz por 45 âncoras: `sync.json` (instantes do áudio) e `native.json` (tempo
  nativo de cada âncora, medido por `SYNC_CAL=1`). Refazer a calibragem só se a cena mudar.
- Legenda: `legenda.srt` (64 cues, fala final “Se curtiu, siga o Parallax Lab.”), cores de
  `SUBTITLE_TERM_COLORS` da cena (raio ciano, distância axial azul, distância violeta;
  cancelam, transversais, cosseno, ângulo e π em magenta).
- Capa: **6 propostas** em `capas/` (A–F, 1080×1920), geradas por `gerar_capa.py`, todas com
  a fórmula estampada. **Escolha pendente**; `capa_instagram.png` ainda não existe.
- Finais: `renders/vid_0008_campo_espira_final_master_limpo.mp4` e
  `renders/vid_0008_campo_espira_final_legendado.mp4` — 1080×1920, 30 fps, 4.581 frames,
  152,7 s; AAC 44,1 kHz estéreo, 152,3 s.
- Comandos: `uv run python -m manim -r 1080,1920 --fps 30 videos/vid_0008_campo_espira/cena.py CampoEspira008`;
  `montar_master.py` (render + WAV); `montar_legendado.py … --color-module …/cena.py`;
  `uv run python videos/vid_0008_campo_espira/gerar_capa.py [PASTA [A-F]]`.

## Modelo aprovado

- Espira de raio R, corrente I, ponto P = (0, 0, z) no eixo; r² = R² + z² para todo elemento.
- |dB| = (μ₀I/4π) dℓ/r² (dℓ ⟂ r); componente axial dB_z = |dB| cos α, cos α = R/r;
  dℓ = R dφ ⇒ dB_z = μ₀IR² dφ / 4π(R²+z²)^{3/2}.
- B_z(z) = μ₀IR² / 2(R²+z²)^{3/2}; B_z(0) = μ₀I/2R; z ≫ R ⇒ B_z ≃ μ₀IR²/2z³ ∝ 1/z³.
- Interno: R = 1; `b_loop(z) = 1/(1+z²)^{3/2}` (em unidades de μ₀I/2R) é a MESMA função da
  derivação (assert), do gráfico e da seta de B em P. Asserts no import conferem r² = R² + z²,
  dB ⟂ r, soma do par = 2× a projeção de um, cos α igual no elemento e em P, dℓ = R dφ,
  r³ = (r²)^{3/2}, ∫dφ = 2π, 2π/4π = 1/2, (R²)^{3/2} = R³, B_z z³ → 1 e z → 2z ⇒ B → B/8.

## Cores e tipografia

Ciano #35D9FF = R e componente axial · Azul #267BFF = z e o fio · Violeta #745CFF = r ·
Ciano claro #8AE9FF = dℓ e corrente · Magenta #EA63FF = operação (cancelamento, substituição,
ângulo α, componente transversal) · Branco #F5F7FF = campo e resultados. A cor da variável
viaja no LaTeX (`\vR \vZ \vr \vL \vM`, em `comum.py`), inclusive dentro de `\frac`.
Texto na tela: Space Grotesk Medium (`screen_text`); matemática em MathTex.

## Narração (texto enviado ao ElevenLabs; início medido no WAV)

| Bloco | Início (s) | Fala |
|---|---|---|
| A1 Gancho | 0,05 | Essa fórmula do campo magnético de uma espira costuma aparecer pronta. Mas ela não surge do nada: dá para construir tudo, passo a passo. |
| A2 Geometria | 7,92 | Começa pela geometria. O raio, a distância axial até o ponto e a distância do trecho do fio até o ponto formam um triângulo retângulo. Por Pitágoras, essa última ao quadrado é o raio ao quadrado mais a distância axial ao quadrado. Guarda isso. |
| A3 Biot-Savart | 22,80 | Agora entra Biot-Savart, que dá o campo de cada trecho. O trecho do fio é perpendicular à reta que o liga ao ponto, então o produto vetorial simplifica. Reescrevendo a distância ao cubo como distância ao quadrado vezes distância, um fator cancela. |
| A4 Simetria | 37,31 | Agora a simetria. Para cada trecho do fio, existe outro exatamente do lado oposto da espira. Os campos dos dois têm componentes transversais iguais e opostas, e elas se cancelam. As componentes axiais apontam para o mesmo lado e se somam. Então basta calcular um trecho e dobrar. |
| A5 Projeção axial | 54,38 | Quanto disso aponta ao longo do eixo? Essa fração é o cosseno do ângulo mostrado na tela, e é o mesmo ângulo que aparece no ponto e no triângulo. Pela geometria, ele é o raio dividido pela distância do trecho ao ponto. Então a parte axial é o campo do trecho vezes essa razão, e esse campo a gente já guardou. |
| A6 Arco | 72,20 | Falta o tamanho do trecho. Visto de frente, ele é um pequeno arco da circunferência. E o comprimento de um arco é o raio vezes o ângulo que ele abre. |
| A7 Encaixe | 80,72 | Agora encaixa. O tamanho do trecho vira raio vezes ângulo. Os dois raios formam raio ao quadrado. Embaixo, distância ao quadrado vezes distância dá distância ao cubo. E a relação guardada troca isso por raio ao quadrado mais distância axial ao quadrado, elevado a três meios. |
| A8 Soma a volta | 97,66 | Agora soma a volta inteira. Ao redor da espira, o raio, a corrente e a posição do ponto não mudam, então saem da integral. O que sobra é integrar o ângulo em uma volta completa, e isso dá dois pi. Dois pi sobre quatro pi: os pi cancelam, dois sobre quatro vira um meio. E aparece o campo magnético no eixo da espira. |
| A9 Checagem em z = 0 | 117,33 | Confere no centro. Leva o ponto até o centro da espira: a distância axial vai a zero, e o campo vira mi zero vezes a corrente, sobre duas vezes o raio. No gráfico, é o máximo. |
| A9B Muito longe | 128,56 | E muito longe, ainda no eixo? Quando a distância axial fica bem maior que o raio, o raio perde importância, e o denominador vira a distância axial ao cubo. Por isso, longe da espira, o campo cai com um sobre essa distância ao cubo. |
| A10 Fechamento e gancho | 142,53 | Uma espira está entendida. E se forem muitas? No próximo vídeo, a gente soma várias espiras e chega ao solenoide. Se curtiu, siga o Parallax Lab. |

Tempos obtidos por alinhamento às pausas medidas (sem transcrição automática).

## Fora de escopo

Linhas de campo completas, campo fora do eixo, momento de dipolo, soma de várias espiras e
solenoide (o gancho “E SE FOREM MUITAS?” termina aqui; o solenoide é o `vid_0009`).

## Pendências

- Escolher a capa (A–F) e gerar `capa_instagram.png`; publicação e URLs não registradas
  (`publicacao.md`); QA físico em celular não confirmado.
- Sincronia por âncoras com margem de ±0,5 s (alinhamento por pausas, sem ASR).
