# vid_0005 — De onde vem a aceleração centrípeta

- Série pública: **POR TRÁS DA FÓRMULA · EP. 02**.
- Tema: origem geométrica de a_c = v²/R no movimento circular uniforme.
- Mensagem: o módulo da velocidade (|v| = v) permanece constante, mas a direção do vetor velocidade
  muda continuamente; essa mudança vetorial produz uma aceleração dirigida
  para o centro.
- Cena: `cena.py`, classe `AceleracaoCentripeta005`.
- Formato: área lógica 9×16; preview 540×960/15 fps; final 1080×1920/30 fps.
- Estado: **preview visual silencioso, 2ª rodada** (≈101,6 s). Sem voz, SRT,
  master, versão legendada, capa ou publicação.
- Roteiro visual: `roteiro.md`.

## Derivação aprovada

Instantes simétricos em torno de t: t± = t ± Δt/2.

- r₋, r₊: módulo R, separados por Δθ. Δr = r₊ − r₋ (corda).
- v₋, v₊: módulo v, tangentes, separados pelo mesmo Δθ (v ⊥ r em cada ponto).
- Δv = v₊ − v₋, construído com v₋ e v₊ transladados para a origem comum.
- Triângulos isósceles com o mesmo ângulo Δθ ⇒ semelhantes:
  |Δv|/v = |Δr|/R ⇒ |Δv|/Δt = (v/R)·|Δr|/Δt.
- Limite Δt → 0: |Δr|/Δt → v; depois |Δv|/Δt → a_c. Logo a_c = (v/R)·v = v²/R.
- Fechamento: v tangente, a_c para o centro, v ⊥ a_c.

Sem aproximação de arco (Δs ≈ RΔθ): o lado do triângulo das posições é a corda |Δr|.

## Verificação da construção

Com o instante central em θ = 0 e ângulos θ± = ±Δθ/2 (movimento anti-horário):

- v± = v(−sin θ±, cos θ±) ⇒ Δv = v₊ − v₋ = (−2v sin(Δθ/2), 0): exatamente −r̂(t),
  a direção radial interna do instante central.
- Δr = R(0, 2 sin(Δθ/2)): paralelo a v(t); |Δr| = 2R sin(Δθ/2), |Δv| = 2v sin(Δθ/2),
  o que confirma |Δv|/v = |Δr|/R para qualquer Δθ.

Na cena: Δθ inicial = 50° (`DTH_START`), limite para em 16° (`DTH_MIN`, nunca zero,
v₋ e v₊ ainda distinguíveis); |v| na tela fixo (`L_V`); a translação para a origem comum usa apenas `shift`.

## Cores

Trajetória: azul discreto · r e matemática: branco · Δr: azul · v: ciano ·
Δv: magenta · a_c: violeta. Paleta vigente, sem cores novas. Tipografia:
Space Grotesk Medium em todo texto fora da matemática (manchetes, rótulos,
tag da série), via `screen_text` de `template/fonts.py`; MathTex na matemática.
