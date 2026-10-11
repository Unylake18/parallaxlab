---
name: feedback-enviar-frames
description: "Ao entregar um preview de vídeo, sempre enviar os quadros-chave ao usuário (SendUserFile) para ele repassar ao GPT avaliar"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 00be2549-face-4cf9-bbd1-71f65a0436bd
  modified: 2026-10-07T02:13:22.605Z
---

Sempre enviar ao usuário os frames (pranchas 2×2 de quadros do preview) junto com o relatório de entrega de qualquer preview renderizado.

**Why:** o usuário leva os quadros a outro modelo (GPT) para uma segunda avaliação visual; sem os arquivos ele não consegue fazer isso.

**How to apply:** depois de renderizar, extrair quadros dos momentos-chave (PyAV, sem ffmpeg no PATH) em pranchas PNG no scratchpad e enviá-los com `SendUserFile`, sem esperar pedido. Ver [[projeto-yt0002-gauss]] para o fluxo da unidade.
