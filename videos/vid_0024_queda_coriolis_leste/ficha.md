# Desvio para Leste na Queda Livre (Efeito Coriolis)

formato: curto_vertical

Série pública: **DA EQUAÇÃO AO FENÔMENO · EP. 06**

Fase: em produção — preview silencioso V9 (540×960 @ 15 fps), revisão espacial e didática; validação por estados críticos, sem QA completo nesta rodada.

- Unidade: `vid_0024_queda_coriolis_leste`
- Pergunta central: “Se eu soltar uma bola de uma torre, ela cai exatamente no ponto abaixo dela?”
- Caso estudado: Equador, queda de 50 m, repouso inicial relativo à Terra, sem resistência do ar, gravidade uniforme, rotação terrestre constante.
- Equação protagonista: \(\vec a_C = -2\vec\omega_T \times \vec v\)
- Núcleo didático V9: ponto P no equador → raios e velocidades tangenciais → triedro oblíquo → norte entrando na tela → zoom em P → h, g e condições iniciais na torre → queda antes de v(t) → Coriolis construído a partir dos vetores → integrações com o mesmo t → distância x(t) → escala real antes do payoff.
- A origem do fator 2, momento angular e derivação formal de referenciais ficam fora deste vídeo; pertencem ao futuro `vid_0023_coriolis`, planejado para depois do fechamento técnico do 0024. Publicação pretendida: 0023 → 0024. A aplicação funciona isoladamente.
- MF-Tools: cancelamento explícito dos fatores 2 na primeira integral. TransformMatchingTex e cópias de termos nas demais passagens.
- Dinâmica local no equador:
  - \(x = \text{leste}\), \(y = \text{norte}\), \(z = \text{cima}\)
  - \(\vec v = -gt\,\hat z\)
  - \(\vec\omega_T = \omega_T\hat y\) (entrando na tela, \(\otimes\))
  - \(\vec a_C = 2\omega_T gt\,\hat x\) (para leste)
  - \(v_x = \omega_T gt^2\)
  - \(x = \frac{1}{3}\omega_T gt^3\)
- Resultado numérico para \(h = 50\,\text{m}\):
  - \(t_f \approx 3{,}19\,\text{s}\)
  - \(x \approx 0{,}77\,\text{cm}\) para leste
- solido_3d: nenhum
- Justificativa de solido_3d: Conforme especificado pelo handoff de Produção, animação 2D vetorial no Manim explica os planos, vetores e desvio de forma ideal e limpa.
