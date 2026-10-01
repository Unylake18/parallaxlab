# vid_0009 — Campo magnético de um solenoide

- Série pública: **DA EQUAÇÃO AO FENÔMENO · EP. 03**.
- **Concluído tecnicamente em 2026-09-30: voz, sincronia por âncoras, legenda e master gerados; publicação e aprovação humana do vídeo final pendentes.**
- Origem: metade solenoide do preview combinado do `vid_0008` (174,7 s), agora unidade própria
  e mais calma (decisão de 2026-09-30, ver `docs/decisoes.md`). Vem DEPOIS do `vid_0008`
  (espira), que constrói a ferramenta B_z(z); este vídeo a usa.
- Pergunta: como enrolar um fio reforça o campo dentro da bobina?
- Cena: `cena.py`, classe `CampoSolenoide009`; base local `comum.py` (cópia do estado de
  2026-09-29 — **não tem** o template de cor no LaTeX, fichas nem halo que o `vid_0008`
  ganhou depois; portar à mão se forem necessários).
- Final: `renders/vid_0009_campo_solenoide_final_master_limpo.mp4` e `..._final_legendado.mp4` — 1080×1920, 30 fps, 5.244 quadros, 174,78 s; AAC 174,40 s. Sem âncora atrasada (`SYNC atraso`: 0).
- Narração: `audio/narracao_final.wav` (ElevenLabs, 174,4 s, estéreo 44,1 kHz, intacta; texto abaixo). A cena segue a voz por 53 âncoras: `sync.json` (instantes do áudio, obtidos por contagem de sílabas da fala + pausas medidas, sem ASR, margem ~±0,6 s) e `native.json` (tempo nativo, `SYNC_CAL=1`). Refazer a calibragem só se a cena mudar:
  `SYNC_CAL=1 uv run python -m manim -r 108,192 --fps 15 videos/vid_0009_campo_solenoide/cena.py CampoSolenoide009`.
- Legenda: `legenda.srt` (83 cues, largura ≤ 446 px; cores de `SUBTITLE_TERM_COLORS`: campo ciano, corrente/densidade verde, comprimento violeta, Ampère/retângulo/transversais/cancelam magenta).
- Comandos: `uv run python -m manim -r 1080,1920 --fps 30 videos/vid_0009_campo_solenoide/cena.py CampoSolenoide009`; `videos/montar_master.py` (render + WAV); `videos/montar_legendado.py … --color-module videos/vid_0009_campo_solenoide/cena.py`.
- Capa oficial: `capa_instagram.png` (1080×1920), headline “E SE FOREM / MUITAS ESPIRAS?”, painel “espira → poucas espiras → solenoide” com o vetor B crescendo (versão sem texto nem fórmula; a variante com vetor final mais grosso foi descartada). Gerada por `gerar_capa.py` (`CAPA_SET=final uv run python videos/vid_0009_campo_solenoide/gerar_capa.py PASTA`, arquivo `capa_final.png`); logo reduzido a 78% e moldura do painel 16% maior que nas capas anteriores da série. As demais propostas ficaram fora do Git.
- Preview anterior (silencioso, sem voz): 540×960, 15 fps, 165,9 s, ~211 animações.
- `prototipo_combinado.py` (classe `CampoSolenoide008`) é o protótipo combinado original,
  preservado só como fonte; não é uma cena de produção.

## Roteiro do vídeo (blocos B1–B15)

Cores fixas: azul = bobina/fios; ciano = campo B; **verde = corrente** (I, I_enc, N_ℓ, n, espira
ativa, fios enlaçados); **magenta = contorno de Ampère** (retângulo, dℓ, ℓ, ρ); violeta = medidas
geométricas (L, dz′) e componentes transversais; branco = álgebra neutra e o ponto P. Sem laranja
nem amarelo (checagem automática de pixels quentes: 0).

B1 retomada: uma espira e B_esp(Δz) = μ₀IR² / 2(R²+Δz²)^{3/2} · B2 cada espira acende, mostra Δz até
P, entrega B_j(P) e B(P) = B₁(P)+B₂(P)+B₃(P)+⋯ vira Σ_j B_j(P) e depois B(z) = Σ_j B_j(z) ·
B3 n = N/L (em linha), fatia dz′, dN = n dz′, Δz = z − z′ (uma vez), dB = B_esp(z−z′) dN,
substituição, B = ∫dB e a integral completa, cada linha substituindo a anterior · B4 a integral sobe
e a curva B(z)/(μ₀nI) nasce junto com P · B5 "no centro: z = 0" ⇒ B(0) = μ₀nI·L/√(L²+4R²); com **R e n
fixos**, L/√(L²+4R²) = 1/√(1+4(R/L)²) e, só no limite L/R → ∞, → 1 · B6 limite ideal · B7 simetria:
dB axial + transversal, transversais se cancelam par a par, B⃗ = B(ρ)ẑ · B8 Ampère (magenta): cada
lado entrega o seu termo; B_fora = 0 e B_dentro uniforme só no modelo infinito; um único resultado
de estado por vez na base · B9–B11 atravessando a parede: Bℓ; N_ℓ = nℓ, I_enc = nℓI; o mesmo ℓ
cancela ⇒ B = μ₀nI · B12 I ↑ ⇒ B ↑; n ↑ ⇒ B ↑ · B13 "=" vira "≈" na região central (L ≫ R) · B14
atuador: núcleo ferromagnético na entrada · B15 fechamento.

Notas com símbolos (μ, ρ, ⇒, ≫, ⊥) são MathTex: a fonte de texto não tem esses glifos.

## Sincronia: o que foi comprimido

A cena tem 157,5 s em tempo nativo e a voz 174,4 s; o motor (`ancora`) escala `play`/`wait` entre âncoras (0,45–2,0×) e segura o último quadro quando sobra tempo. Trechos mais apertados (≈0,55–0,60×): Σ→∫ (B3), Ampère com o retângulo todo fora (B8) e atravessando a parede (B9). Para caber, as esperas nativas de B2, B3, B8 e B9 foram encurtadas, o passo Δz = z − z′ passou a vir junto da fatia e o fecho ganhou revelação em etapas (uma linha por trecho da fala). Nenhum passo físico foi removido.

## Narração (texto enviado ao ElevenLabs)

No vídeo anterior, a gente entendeu o campo de uma única espira. Agora vem a pergunta natural: e se colocarmos muitas, uma ao lado da outra?

Cada espira dá a sua contribuição para o campo no ponto observado, e ela diminui quanto mais longe a espira está. Mas todas apontam para o mesmo lado, ao longo do eixo. Então o campo total é a soma de todas elas.

Só que, com as espiras muito próximas, contar uma por uma deixa de ser prático. É melhor descrever a bobina pela quantidade de espiras por comprimento. Numa fatia fina, o número de espiras é essa densidade vezes a largura da fatia. Multiplicando pela contribuição de uma espira e somando todas as fatias, a soma vira uma integral.

Essa integral determina o perfil do campo ao longo do eixo, que aparece no gráfico. Longe da bobina, o campo é pequeno; ele cresce na entrada, atinge o máximo no centro e volta a cair na outra extremidade.

Agora olha para o centro. Mantendo o raio e a densidade fixos e aumentando só o comprimento, essa região fica cada vez mais plana, e o campo ali tende a mi zero vezes a densidade de espiras vezes a corrente. Já na extremidade de uma bobina longa, ele tende à metade desse valor.

Isso sugere um modelo ideal: uma bobina infinita, sem pontas. Ela não existe, mas a simetria simplifica bastante o problema.

Para cada contribuição transversal existe outra simétrica, no sentido oposto. Elas se cancelam, e sobra só a componente ao longo do eixo. E, sendo infinita, deslocar o ponto ao longo do eixo não muda nada: o campo só depende da distância até o eixo.

Agora a lei de Ampère. Com um retângulo todo do lado de fora, os lados curtos não contribuem, e os lados longos mostram que o campo externo é o mesmo em qualquer distância. Mas, muito longe, ele tende a zero. Então, nesse modelo ideal, o campo externo só pode ser zero. O mesmo argumento mostra que, por dentro, ele é uniforme.

Agora o retângulo atravessa a parede. Só o trecho de dentro contribui: campo vezes comprimento. Do outro lado, a corrente envolvida: densidade de espiras vezes esse comprimento, vezes a corrente. O comprimento cancela, e o campo dentro do solenoide ideal é mi zero vezes a densidade de espiras vezes a corrente. Mais corrente, mais campo. Mais espiras no mesmo comprimento, mais campo.

Numa bobina real, a igualdade vira aproximação. No centro de uma bobina longa, o campo é quase uniforme e muito próximo desse valor; nas extremidades ele varia, e fora não é exatamente zero.

Essa variação importa num atuador: um núcleo ferromagnético perto da entrada da bobina, onde o campo muda bastante, é atraído para a região de campo mais intenso, entra e movimenta a válvula.

Resumindo: começamos com uma espira, somamos muitas e chegamos ao campo no centro de um solenoide longo: aproximadamente mi zero vezes a densidade de espiras vezes a corrente. Se curtiu, siga o Parallax Lab.

## Pendências

- `publicacao.md`, `revisao.md` e aprovação humana do vídeo final; publicação não registrada.
- Sincronia com margem de ±0,6 s (sem ASR): conferir no vídeo se algum passo da cena adianta/atrasa em relação à fala.
- QA físico em celular não confirmado; `docs/estado_atual.md` não atualizado.
