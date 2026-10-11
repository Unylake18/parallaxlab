---
name: feedback-arsenal-decisoes-visuais
description: "Convenções visuais decididas pelo usuário para o arsenal 3D (sinal da carga, cor de B, vetores, polos do ímã)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 52a8776a-3165-4130-b609-47a0583f1cd4
  modified: 2026-10-07T16:51:26.917Z
---

Decisões do usuário em 2026-10-07 para o arsenal 3D (estilo.json):
- **Sinal da carga**: esculpido na geometria (+ ou − em relevo na esfera, virado para a câmera), não por cor.
- **Campo magnético B = magenta #EA63FF**; ciano segue só para o campo elétrico E.
- **Velocidade, força, torque, momento angular = branco neutro** (os vídeos antigos divergem; ele autorizou branco "de primeira").
- **Polos do ímã**: N azul, S magenta, "tem que ser bem claro que são diferentes"; nomes N e S por rótulo no Manim.

**Why:** destrava a fila A do arsenal (onda EM, partícula em B, espira, indução, equipotenciais, giroscópio). Ver [[feedback-arsenal-padrao-gauss]] e [[projeto-arsenal-3d-blender]].

**How to apply:** ao desenhar vetores/campos novos, use essas cores sem perguntar de novo. Atenção: magenta é usado ao mesmo tempo para B e para o polo S; testar a leitura em cenas com ímã e linhas de B.
