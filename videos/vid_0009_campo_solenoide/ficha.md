# vid_0009 — Campo magnético de um solenoide

- Série pública: **DA EQUAÇÃO AO FENÔMENO · EP. 03**.
- **Em preparação (2026-09-30): preview silencioso aprovado como protótipo; narração, SRT,
  master, capa e publicação não iniciados.**
- Origem: metade solenoide do preview combinado do `vid_0008` (174,7 s), agora unidade própria
  e mais calma (decisão de 2026-09-30, ver `docs/decisoes.md`). Vem DEPOIS do `vid_0008`
  (espira), que constrói a ferramenta B_z(z); este vídeo a usa.
- Pergunta: como enrolar um fio reforça o campo dentro da bobina?
- Cena: `cena.py`, classe `CampoSolenoide009`; base local `comum.py` (cópia do estado de
  2026-09-29 — **não tem** o template de cor no LaTeX, fichas nem halo que o `vid_0008`
  ganhou depois; portar à mão se forem necessários).
- Preview: 540×960, 15 fps, **139,2 s**, 192 animações
  (`uv run python -m manim -r 540,960 --fps 15 videos/vid_0009_campo_solenoide/cena.py CampoSolenoide009`).
- `prototipo_combinado.py` (classe `CampoSolenoide008`) é o protótipo combinado original,
  preservado só como fonte; não é uma cena de produção.

## Roteiro do vídeo (blocos B1–B18)

B1 retomada da espira (B_j = μ₀IR²/2[R²+(z−z_j)²]^{3/2}) · B2 superposição 1→2→4→8 espiras
(b_sum real: 1,00 / 1,83 / 2,85 / 3,58 na escala B/B₁(0)) · B3 bobina finita: retornos externos
e B(z) axial, pontas ≈ 54% do centro · B4 idealização: finita → longa → contínua e uniforme ·
B5 simetria (B⃗ = B(s)ẑ só no modelo ideal) · B6–B9 Ampère cumulativo com o MESMO retângulo:
fora (B_fora constante, depois B→0 ⇒ B_fora = 0), dentro (B_dentro constante) · B10–B13
atravessando: contorno Bℓ × corrente envolvida N_ℓ = nℓ, I_enc = nℓI ⇒ B = μ₀nI · B14 leitura
de n e I · B15 “=” vira “≃” na bobina longa finita · B16 testes de I e de N (L e I fixos) ·
B17 atuador (plunger e válvula) · B18 fechamento.

## Pendências

- Narração, alinhamento, sincronia por âncoras (o mecanismo de `sync.json`/`native.json` do
  `vid_0008` serve de modelo), SRT, capa, master e publicação.
- Aplicar ao solenoide a linguagem visual do `vid_0008` (objetos persistentes, cor na equação,
  transformação em vez de troca, fichas como memória) — hoje o `cena.py` ainda usa a versão
  anterior; a Ampère cumulativa já está implementada.
- Refazer os tempos e comentários de bloco depois de mexer na cena.
