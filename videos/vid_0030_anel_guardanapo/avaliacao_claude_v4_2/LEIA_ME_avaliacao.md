# vid_0030 — pacote de avaliação (visual v4.2 + narração v1)

Série pública: **ABSURDO CALCULÁVEL · EP. 03** · "O anel de guardanapo: por que só a altura determina o volume?"
Formato: curto vertical. Preview silencioso 540×960 / 15 fps, 180 s, CRF 14 (o final será 1080×1920 / 30 fps com voz).
Estado: visual v4.2 **aprovado pelo Kaio** em 2026-10-29; voz **ainda não gerada** (só o texto com tags).

## O que tem aqui
| Arquivo | Conteúdo |
|---|---|
| `preview_v4_2_540x960.mp4` | o vídeo inteiro (sem voz) |
| `vid_0030_preview_v4_2.zip` | os 2700 quadros, o MP4, código (`cena.py`, `cena3d.js`, `timeline.json`, `Vid0030.tsx`), `ficha.md`, JSONs de QA e pranchas |
| `narracao_tags_v1.md` | narração por cena e texto corrido com audio tags do ElevenLabs v4 (≈ 477 palavras, 2765 caracteres) |
| `v4_2_h_magenta.png` | uma cena de cada trecho (padrão de cor) |
| `v4_detalhe_*.png` | hook, C02–C06 e C06–END em detalhe |

## Estrutura (tempos do preview; a cena se estica com a voz)
C01 hook 0–30 s (porta-guardanapo → "= ESFERA FURADA" → três esferas furadas viram o trio de h = 6 cm) · C02 anatomia
30–48 (R² − a² = (h/2)²) · C03 fatia 48–82 (A(z) = π[(h/2)² − z²], o R some) · C04 Cavalieri 82–110 · C05 volume
110–138 (V = πh³/6 por Cavalieri e pela integral) · C06 paredes (1,00 / 0,68 / 0,46 cm) + prova ao vivo + proteção
138–162 · C07 limites vistos no 3D + trio + fecho 162–176 · END 176–180.

## Padrão de cor (decisão do Kaio)
h (e h/2, h³…) **magenta #EA63FF em todo o vídeo**; R **branco**; a violeta #9C8CFF; z cinza GEO; ρ rosa-claro #F7B8FF;
ciano #35D9FF só como destaque (setas, ✓, riscos de cancelamento, "O MESMO VOLUME"). Sem contorno preto nem chip atrás
de rótulos sobre o 3D.

## QA já medido
- Sobreposição (máscaras por grupo, todas as camadas, 2700 quadros): **0** em texto×texto, texto×3D, folga de rótulo,
  margem 24 px e zona do 3D. Menor opacidade de texto estável 77 %; entradas/saídas ≤ 0,4 s.
- Réguas de h ancoradas no 3D: erro ≤ 0,006 px; pontas das linhas ≤ 0,67 px.
- Contas: V = πh³/6 = 113,097 cm³ pelas duas rotas; 36π ≈ 113,1; espessuras 1,0000 / 0,6754 / 0,4606 cm;
  π(2R)³/6 = (4/3)πR³.
- Contraste WCAG: abaixo da meta (texto 4,5:1, linha 3:1) desde que os contornos foram retirados a pedido do Kaio:
  linha de h magenta sobre o azul ≈ 2,4:1; linha ρ sobre a esfera rosa ≈ 1,8:1; rótulos sobre o sólido ≈ 1,7–3,6:1;
  rótulo "6 cm" do hook ≈ 4,2:1.

## O que avaliar (sugestão)
1. **Narração × tela:** cada frase do `narracao_tags_v1.md` tem o que mostrar na tela, na ordem certa? Algo que a fala
   diz e a tela não mostra (ou o contrário)?
2. **Texto da fala:** clareza para quem está no ensino médio/cursinho; nome completo das grandezas (a letra "a" só uma
   vez); conectivos; tags (uma por frase, sem [slowly]); trechos que a voz pode ler errado (ex.: "aparece como a").
3. **Duração:** 2765 caracteres ≈ 158–177 s; cabe nos 180 s do preview sem pressa?
4. **Matemática e didática:** cancelamento 4/8 = 1/2 e 8/6 = 4/3 escritos; proteção ("não é qualquer furo…") só no C06;
   história (Seki Kōwa) só na fala, sem data e sem "descobriu".
5. **Visual:** padrão de cor de h, legibilidade dos rótulos sobre o 3D sem contorno, ritmo do hook.

Não alterar nada no repositório a partir deste pacote: devolver a avaliação como lista de ajustes.
