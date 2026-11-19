# Dinâmica da rotação: 4 problemas em que o momento de inércia decide tudo

Série pública: **MECÂNICA · EP. 4 (ROTAÇÃO DE CORPOS RÍGIDOS)** (provisório)

formato: longo_horizontal
natureza: exercicio_resolvido
disciplina: Física I
bloco: Rotação
modulo: 4.11 Rotação de corpos rígidos (exercícios de dinâmica)
referencia: Moysés vol. 1, cap. 12, prob. 13 (E2, ampliado); Kleppner & Kolenkow, An Introduction to Mechanics, 1ª ed., probs. 6.15 e 6.16 (E4); E1 e E3 autorais
pergunta_central: como torque, momento de inércia e vínculo resolvem, juntos, um sistema que gira e translada, e como conferir se a resposta está certa?
pre_requisitos: Στ = Iα; I de disco, anel e haste; eixos paralelos; K = ½Iω²; v = ωr; a_t = αr; a_c = ω²r; pêndulo simples (T = 2π√(l/g))
payoff_principal: a distribuição da massa decide o movimento (a = g/(1 + I/mr²)); a força no eixo muda durante o giro; massa × raio, e não massa, decide o sentido; I e torque viram ferramenta de projeto (período mínimo em l = R/√2)
frase_guia: começa pela física: identifica as forças, escolhe o eixo, escreve as equações, aplica os vínculos e confere
duracao_alvo: ~30 min (sai da fala); preview nominal 30:59 a 2,7 palavras/s, sem voz
3d_threejs: carretel (H1–H3, E3-1 a E3-10), volante (E1 inteiro), regua (D1–D3, régua do yt_0022 com massa M na ponta)
solido_3d: nenhum do arsenal Blender; geometrias próprias em Three.js (threejs/cena3d/f23.js); régua copiada de yt_0022 (f22.js)
canto: linha 1 `MECÂNICA · EXERCÍCIOS DE ROTAÇÃO`; linha 2 = bloco da vez
fase: preview silencioso 960×540 / 15 fps (sem voz, SRT, master ou entrega)

## Lotes (cena.py)

| Lote | Âncoras | Arquivo |
|---|---|---|
| PH | H1–H3, A1–A3, D1–D3 | sec_ph.py |
| PE1a | E1-1 a E1-10 | sec_e1a.py |
| PE1b | E1-11 a E1-18 | sec_e1b.py |
| PE2 | E2-1 a E2-11 | sec_e2.py |
| PE3 | E3-1 a E3-10 | sec_e3.py |
| PE4 | E4-1 a E4-10 | sec_e4.py |
| PS | S1, S2, EN1, EN2 | sec_ps.py |

Especificação completa (storyboard, narração v1.1, conferência numérica): `handoff_v2.md` (Anexo A extraído em `narracao_sugestao.md`).
Referências bibliográficas ficam só nesta ficha e na descrição do YouTube, nunca na tela nem na fala.
