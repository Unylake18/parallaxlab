# CENTRO DE MASSA: 6 PROBLEMAS QUE PARECEM IMPOSSÍVEIS

- **ID:** yt_0018 (continuação direta do yt_0017 · Centro de massa; o EN3 de lá promete a placa com furo, o fio no cubo, o gafanhoto e a
  resposta do disco). Série do 4.9: yt_0015 → yt_0016 → yt_0017 → **yt_0018 exercícios de centro de massa** → foguete.
- **formato:** longo_horizontal
- **natureza:** exercicio_resolvido
- **disciplina:** Física I · **bloco:** Momento e colisões · **modulo:** 4.9 Momento linear e impulso
- **referencia:** Sears 14ª ed. §8.5; Moysés vol. 1 cap. 8 (só na ficha e na descrição, nunca na tela). Epílogo: Einstein (1906). Números dos
  problemas: construção do Parallax Lab.
- **pergunta_central:** Em que ângulo o gafanhoto precisa pular para cair de volta na folha que boia?
- **pre_requisitos:** yt_0017 (média ponderada, por partes, massa negativa, M A⃗_cm = F⃗_ext, referencial do CM, energia relativa)
- **payoff_principal:** escolher bem o sistema e o referencial elimina a parte difícil da conta; o gafanhoto só cai na folha se pular quase
  rasante (θ ≤ 4,23°) ou quase vertical (θ ≥ 85,77°)
- **duracao_alvo:** ~16 min (sai da fala; narração v2.1: 2.530 palavras, 15,6 min nominais a 2,7 palavras/s)
- **3d_threejs:** hook e X3 (lago com gafanhoto e folha procedurais, cena `lago`, `threejs/cena3d/lago3d.js`), X2 (fio no cubo, cena `cubo`),
  EN2 (foguete, cena `fog`), as duas em `threejs/cena3d/cm18.js`. O X5 (balança) é 2D; a cena `roj` do v1 ficou sem uso. O A3 reaproveita a granada do yt_0017 (`gra`, `cm3d.js` + `campo.js`) pequena no PALCO.
- **solido_3d:** nenhum do arsenal Blender; geometrias próprias em Three.js
- **Canto:** linha 1 `MECÂNICA · CENTRO DE MASSA: PROBLEMAS`; linha 2 = `PROBLEMA N · NOME`
- **Status:** v5 preview silencioso 960×540 / 15 fps do vídeo inteiro (handoff v5 de 2026-10-31) em `renders/preview_yt0018_v5_960x540.mp4`,
  mais o texto da narração v1.1 com audio tags para validação (`narracao_tags_v1_1.md`, gerado por `narracao_tags.py`, com o diff para a v1); o v4 ficou em
  `renders/preview_yt0018_v4_960x540.mp4` e o código dele em `_v4/`; v3 em `_v3/` (o `_teste_v3/` é o v3 com a auditoria v4), v2 em `_v2/`, v1 em `_v1/`.
  Sem voz, SRT, master nem entrega (a voz espera a aprovação do Kaio do v5 e da narração v1.1).

## Estrutura e lotes
hook H1–H3 + abertura A1–A4 (PH) · X0 disco furado + X1 placa com furo (PX0) · X2 fio no cubo (PX2) · X3 gafanhoto (PX3) · X4 naves (PX4) ·
X5 a balança que marca menos (PX5) · epílogo EP1–EP2, síntese S2, encerramento EN1–EN2 (PEP). Render: `./render.sh LOTE` (2D) ou `./render3d.sh LOTE` (com 3D);
`./render_todos.sh ...` em paralelo; `montar_preview.py` emenda; `qa.py` → `renders/qa.txt`.
v3: `./render_v3.sh LOTE` (pedidos 3D → Three.js → render sem auditoria, e em paralelo `./auditar.sh LOTE`, a auditoria a cada 3 quadros);
`casos14.py` (os 14 casos da §2 como teste da auditoria), `prancha_humana.py` (G28 v3), `p99.py` + `threejs/p99.js` (exposição),
`casos_quadros.py` e `lago_v2_x_v3.py` (antes × depois).
v4: `casos13.py` (os 13 casos da §2 do handoff v4), `agua.py` (brilho da água por cena e p99 da coluna da lua), `comparar_v4.py`
(13 casos antes × depois, lago v3 × v4, X3 PERTO × LONGE), `narracao_tags.py` (narração v2.2 com tags).
v5: auditorias novas em `kit.py` (`_auditar_v5`: ESQUELETO G29, 3D × TEXTO G30, DUPLICATA G31, VAZIO G32), `voa()` com esqueleto antes dos tokens e origem a 35% (`dim_origem`),
`comparar_v5.py` (12 tempos v4 × v5), `./render_v3.sh LOTE` como no v3/v4; `qa.py` com o portão G28 v5 e a BALANÇA estendida à montagem.

## Arquivos
`narracao_sugestao.md` (narração v2 = Anexo A do handoff v2) → `gerar_ancoras.py` → `ancoras.json` · `kit.py` (copiado do yt_0017: paleta, ⊕ em
degradê, texto, relógio por quadro, Fundo3D/projeta3d, auditorias) · `prob.py` (esqueleto dos problemas: selos, HIPÓTESES, checklist, selo
de referencial G20, auditorias novas) · `prob2.py` (v2: Pilha da CONTA, selo único, chip, rótulos com teste de colisão, passo/voa G23, pausas) · `lago2.py` (o gafanhoto e a folha, física exata, estado do lago 3D) · `icones.py` · `pecas3d.py` (granada do yt_0017) ·
`pecas18.py` (cubo, rojão, foguete) · `sec_*.py` (um por lote) · `fundo.py`/`fundo_lab*.png` (céu do laboratório do yt_0017).
