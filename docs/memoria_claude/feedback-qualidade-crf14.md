---
name: feedback-qualidade-crf14
description: "padrão único de qualidade de vídeo — CRF 14 em master e legendado (limiar medido); sem \"qualidade desnecessária\""
metadata:
  node_type: memory
  type: feedback
  originSessionId: 00be2549-face-4cf9-bbd1-71f65a0436bd
  modified: 2026-10-09T17:35:50.348Z
---

O usuário quer **uma qualidade alta e igual** em master e legendado, no limiar em que mais qualidade já não aparece (não desperdiçar bits). Decidido em 2026-10-09: H.264 yuv420p **CRF 14**.

**Why:** medido no yt_0002 (trecho denso): abaixo de 14 ganho desprezível e +12–25% de arquivo; acima, linhas finas degradam. O master era maior que o legendado só porque o legendado usava CRF 18/19 fixo e `veryfast`.

**How to apply:** render Manim ≥1080p já sai em 14 via `template/qualidade.py` (chamado por `template/config.py`); `videos/montar_legendado.py --crf auto` = `max(14, CRF do master − 5)`; detalhes em AGENTS.md ("Qualidade de render e codificação"). Master antigo em CRF 23 só melhora re-renderizando. Ver [[projeto-yt0002-gauss]].
