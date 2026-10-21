# Magnetostática — divergente e rotacional de B, Lei de Ampère

- id: `yt_0008`
- formato: `longo_horizontal`
- natureza: `teoria_visual`
- identificação editorial: **5.3** (continuação do 5.2 · Biot–Savart, `yt_0006`)
- posição curricular: **6.9 Lei de Ampère** em `docs/mapa_curricular.md`
- solido_3d: `nenhum` — avaliados `fio_infinito`, `amperiano_circular`, `amperiano_retangular`, `solenoide_corrente`, `toroide_corrente`,
  `teorema_stokes`, `divergencia_local`, `rotacional_roda_de_pas`. Não integrados: (1) a gramática de cor do arsenal (campo ciano,
  corrente azul) conflita com a da série (B magenta, corrente verde); (2) as sequências PNG têm câmera fixa e não acompanham a projeção
  2.5D viva (superfície nascendo da borda, cúpula deformando, amperianos deslizando, sonda girando); (3) no toroide, o 2.5D procedural
  garante o campo só no interior (ideal). Geometria 2.5D procedural em Manim, como no yt_0005/yt_0006.
- fase: **preview silencioso 960×540 / 15 fps** (N01–N23). Sem voz, SRT, master, capa ou publicação.
- classe: `YT0008Ampere` (`cena.py`), uma cena contínua.

## Especificação

Handoff de Produção de 2026-10-19 (física, matemática, narração, storyboard e direção visual congelados): N01 pergunta → N02 paradoxo
do fio → N03 sonda local → N04 circulação global → N05 divergente → N06 divergente formal → N07 dois nablas → N08 rotacional (quatro
termos) → N09 delta → N10 segundo termo → N11 fio de raio finito → N12 região externa → N13 limite filamentar → N14 integrar em S →
N15 Stokes → Ampère (e deformação de S) → N16 validade × utilidade → N17 fio → N18 lâmina → N19 solenoide (dois amperianos) →
N20 toroide ideal → N21 eletrostática × magnetostática → N22 síntese → N23 gancho B = ∇×A.

O texto da narração não veio no handoff; a cena segue o storyboard N01–N23 e as legendas curtas só nomeiam a operação.

## Estrutura

`kit.py`, `base.py` (copiados do yt_0006 e estendidos: famílias r/r′, pintura por subtermo, layout `app`, `src` com vários tokens) ·
`geo.py` (laços, discos, anéis, caixa, barra de estratégia; `tau < 0` = vista de cima, projeção destra) · `sec1`–`sec7.py` (N01–N23) ·
`fisica.py` (estados) · `qa_fisica.py` (QA numérico) · `_grupo.sh`, `juntar.py`, `contato.py` (render por trechos, junção, folhas).

Cores: B magenta · corrente/J verde · geometria (s, R, F, S, C, amperianos) violeta · observador r, ∇ ciano · fonte r′, ∇′, J(r′) verde.

## Execução

```bash
uv run --no-sync python videos_longos/yt_0008_magnetostatica_ampere/qa_fisica.py
bash videos_longos/yt_0008_magnetostatica_ampere/_grupo.sh t1 pergunta,paradoxo,sonda,circulacao,divergente divergente
```
