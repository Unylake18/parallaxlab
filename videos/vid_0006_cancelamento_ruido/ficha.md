# vid_0006 — Interferência e cancelamento ativo de ruído

- Série pública: **DA EQUAÇÃO AO FENÔMENO · EP. 02**.
- **Concluído e publicado manualmente pelo usuário em 2026-09-28** (URLs não registradas). Headline final: “O SOM PODE CANCELAR O SOM?”.
  Roteiro com tempos: `roteiro.md`; QA: `revisao.md`; publicação: `publicacao.md`.
- Ideia única: pressões acústicas se superpõem; contribuições com amplitudes
  semelhantes e fases aproximadamente opostas reduzem a pressão resultante num
  ponto/região. O ANC é aplicação dessa física, não aula de engenharia.
- Arco: curiosidade → superposição → interferência → cancelamento → fone.
- Cena: `cena.py`, classe `CancelamentoRuido006`.
- Narração: `audio/narracao_final.wav` (ElevenLabs, 104,64 s, estéreo 44,1 kHz, intacta);
  a cena a toca por `add_sound` e segue seus tempos com `until(...)` (pontos de sincronia
  obtidos pelas pausas medidas no WAV).
- Legenda: `legenda.srt` (43 cues, fala final “Se curtiu, siga o Parallax Lab.”), cores de
  `SUBTITLE_TERM_COLORS` da cena.
- Capa: `capa_instagram.png`, gerada por `gerar_capa.py`: “O SOM PODE / CANCELAR O SOM?” +
  painel INTERFERÊNCIA (ciano + magenta → branco pequeno) → CANCELAMENTO DE RUÍDO (fone com
  ruído chegando, contribuição magenta saindo e resíduo branco).
- Finais: `renders/vid_0006_cancelamento_ruido_final_master_limpo.mp4` e
  `renders/vid_0006_cancelamento_ruido_final_legendado.mp4` — 1080×1920, 30 fps, 3.166 frames,
  105,53 s; AAC 44,1 kHz estéreo, 104,64 s.
- Comandos: `uv run python -m manim -r 1080,1920 --fps 30 videos/vid_0006_cancelamento_ruido/cena.py CancelamentoRuido006`;
  `montar_master.py` (render + WAV); `montar_legendado.py … --color-module …/cena.py`;
  `uv run python videos/vid_0006_cancelamento_ruido/gerar_capa.py`.

## Modelo aprovado

- Regime linear: p_total = p₁ + p₂.
- Ideal: p₁ = A sin ωt, p₂ = A sin(ωt + φ); A_res = 2A|cos(φ/2)|;
  φ: 0 → π ⇒ 2A → 0. “= 0” só neste modelo.
  - C5: p_total = 2A cos(φ/2) sin(ωt + φ/2); o fator 2A cos(φ/2) é a amplitude em
    0 ≤ φ ≤ π e fica ligado ao colchete A_res. Depois fica A_res = 2A|cos(φ/2)|, com
    um único valor exato nos estados φ = 0 → 2A, φ = π/2 → √2 A (pausa), φ = π → 0.
    Colchete, rótulo e valores usam o mesmo φ das curvas.
  - C6: p₂ = A sin(ωt + π) → −A sin(ωt) → −p₁; p_total = p₁ + p₂ → p₁ − p₁ → 0,
    com “CASO IDEAL” junto do zero.
- ANC: p_ruído = A[sin ωt + c·sin(3ωt + 0,6)], p_fone = −g·p_ruído(t − τ),
  p_residual = soma. Com c = 0: B = gA (B = g na normalização A = 1 da cena), φ = π − ωτ,
  A_res = √(A² + B² + 2AB cos φ).
  - imperfeito: g = 0,9, ωτ = 0,05π (φ = 0,95π) → 0,179A;
  - melhor ajuste: g = 0,95, ωτ = 0,03π (φ = 0,97π) → 0,105A;
  - multifrequência: c = 0,35; mesmo τ ⇒ erro de fase 3× maior em 3ω. Nunca zero.
- Asserts em `cena.py` conferem esses valores com as mesmas funções das curvas.
- Ar: fileiras = deslocamento longitudinal s = s₀ sin(kx − ω_a t + φ_j),
  λ = 3,1, s₀k = 0,55; fileiras “ONDA 1 / ONDA 2 / RESULTANTE” (resultante = s₁ + s₂,
  calculada), nota “DESLOCAMENTO DO AR · MESMO TRECHO” e uma camada destacada nas três.
  p(t) aparece só nos gráficos de pressão; x₀ fica no painel espacial, ligado ao gráfico
  por uma chamada lateral.
- Aplicação: a tela compara amplitudes (A_residual ≪ A_ruído), não valores
  instantâneos — em t = 0 o ruído é zero e o residual vale ≈ 0,089A. Barras de
  amplitude no painel (picos das próprias curvas).

## Cores e tipografia

Ciano #35D9FF = p₁/ruído · Magenta #EA63FF = p₂/fone · Branco #F5F7FF =
soma/resultante · Azul #267BFF = eixos/fone/ícones · Violeta #745CFF =
processamento/atraso. Texto na tela: Space Grotesk Medium (`screen_text`);
matemática em MathTex. Faixa y < −4,6 livre; |x| < 3,5.

## Narração (texto enviado ao ElevenLabs; início medido no WAV)

| Bloco | Início (s) | Fala |
|---|---|---|
| C1–C2 | 0,04 | O som pode cancelar o próprio som? É isso que um fone com cancelamento de ruído explora. Pra entender como, vamos voltar à física: interferência de ondas. |
| C3 | 9,95 | Este gráfico mostra a pressão num ponto ao longo do tempo. As duas pressões se somam, e a curva branca nasce dessa soma: superposição. |
| C4 | 18,02 | Em fase, crista encontra crista e vale encontra vale. As ondas se reforçam: interferência construtiva. |
| C5 | 24,82 | Agora deslocamos a fase da onda magenta. O fator destacado determina a amplitude da soma. Repare na curva branca: de zero a meio ciclo, sua amplitude cai até zero. |
| C6 | 34,80 | Com meio ciclo de diferença, crista encontra vale. Se as amplitudes são iguais, uma compensa a outra e, nesse caso ideal, a soma é zero: interferência destrutiva. |
| C7 | 44,64 | Mas esse gráfico não é o formato do ar. No ar, as camadas oscilam para a frente e para trás, formando compressões e rarefações. As ondas não se aniquilam: o que diminui é a pressão resultante. |
| C8–C9 | 56,10 | Agora, de volta ao fone. Os microfones captam o ruído, o processamento calcula uma resposta, e o alto-falante produz outra contribuição sonora. |
| C10 | 64,49 | Perto do ouvido, acontece a mesma soma. Como amplitude e fase não batem perfeitamente, sobra um resíduo, em branco. |
| C11 | 71,44 | Com um ajuste melhor, o resíduo fica menor. Mas, num fone real, não chega a zero. |
| C12 | 76,22 | O ruído real mistura várias frequências, e o sistema ainda lida com atraso, posição e acústica. |
| C13 | 82,10 | Por isso, o cancelamento ativo costuma funcionar melhor com ruídos contínuos e frequências mais baixas, como motor e avião. O período é maior, então o mesmo atraso gera uma diferença de fase menor. |
| C14 | 93,47 | O som não desaparece. O fone adiciona outra contribuição e reduz a pressão resultante perto do ouvido. |
| CTA | 99,91 | Se curtiu, siga o Parallax Lab. (na tela: síntese em 98,7 e @labparallax em 101,12) |

Tempos obtidos por alinhamento às pausas (sem transcrição automática).

## Fora de escopo

Energia, dB, impedância, equação da onda, Fourier, DSP, controle,
feedforward/feedback, fisiologia da audição, marcas. A arquitetura mostrada
(microfones → processamento → alto-falante) é conceitual, não universal.

## Pendências

- URLs da publicação não registradas (`publicacao.md`); QA físico em celular e backup
  externo dos MP4s não confirmados.
- Duração 105,5 s com a voz (dentro dos 95–105 s previstos, +0,5 s de cauda).
