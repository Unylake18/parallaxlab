# liquido_rotacao — rodada 3: indicação estrutural de co-rotação

Tracers removidos dos modos editoriais. `fenomeno` usa um único setor angular translúcido preso à superfície; `geometria` conserva a prioridade da seção meridiana e do paraboloide, sem setor por padrão.

## Implementação

- Um setor de **24°**, sem espessura sólida nem contorno, com opacidade constante **18%**, cor neutra da paleta e emissão baixa. Não há textura, rastro, partículas ou novas linhas decorativas.
- Setor suave com **321 vértices / 288 faces**, mesma amostragem radial de 32 anéis da superfície. Corpo permanece em **128×32**, com a mesma fórmula e parâmetros físicos.
- A camada fica 0,003 u acima da lâmina existente para evitar z-fighting. É visível dos dois lados: o descarte de faces apagava a região frontal do paraboloide, vista através do líquido.
- `lambda` atualiza somente a curvatura da superfície e do setor. `fase_rotacao` aplica uma rotação rígida ao setor em torno do eixo z: `φ = fi_setor + 2π × voltas × fase_rotacao`. Um controle não modifica o outro.
- `setor=-1` segue o modo: visível em `fenomeno`/`qa`, oculto em `geometria`; 0/1 permite ocultar ou mostrar explicitamente.
- `angulo_setor=24` e `fi_setor=-35` controlam abertura e orientação inicial.
- Tracers permanecem disponíveis somente em `estado_visual='qa'`. Fora desse modo, `marcadores=1` também é ignorado, evitando que configurações antigas recoloquem partículas no editorial.
- A referência magenta, o morph one-shot, o hold final e o payoff geométrico foram preservados.

## Arquivos alterados

Caminhos relativos a `experimentos/blender/arsenal/`:

- `liquido_rotacao.py`: setor paramétrico, deformação/rotação independentes, modos e bloqueio dos tracers editoriais.
- `solidos/liquido_rotacao.json`: controles do setor, descrições e thumbnail atual; status permanece `estudo`.
- `construtores.py`: somente o adaptador deste sólido, com os novos argumentos nomeados.
- `verificar_liquido_rotacao.py`: QA dos modos, bloqueio de tracers, aderência do setor à superfície e rotação rígida.
- `preview_liquido_rotacao.py`: destino separado por rodada e opção de renderizar apenas os stills afetados; verifica ausência de tracers nos quadros editoriais.
- `montar_previews_liquido_rotacao.py`: pasta selecionável e montagem das sequências presentes, permitindo reaproveitar a geometria sem rerender.
- `previews/liquido_rotacao_rodada3/`: novos previews, logs, estados por quadro, resumo e este relatório.

Arquivos e previews da rodada 2 foram preservados. Nenhuma documentação global foi alterada.

## Previews desta rodada

**540×960, Eevee, 24 amostras**. Clipes de **48 quadros, 15 fps, 3,2 s**, H.264/yuv420p, CRF 14, preset medium, sem áudio.

- [Plano com setor](fenomeno_lambda0.png)
- [Paraboloide com setor](fenomeno_lambda1.png)
- [Comparação com o modo geometria](comparacao.png)
- [Rotação do setor, λ=1 fixo](rotacao.mp4)
- [Morph one-shot com setor preso à superfície](morph.mp4)
- [Loop 0→1→0 com rotação do setor](loop_qa.mp4)
- [Folha de quadros das animações](sequencias.png)

O still `geometria_meridiana.png` é uma cópia do preview inalterado da rodada 2, para comparação. O [payoff seção → superfície](../liquido_rotacao_rodada2/payoff.mp4) continua válido e não foi rerenderizado. PNGs das novas sequências em `rotacao/`, `morph/`, `loop_qa/`; controles em `*_estados.json`; custo e tamanho em `resumo.json`.

## Verificações

- Compilação Python dos cinco módulos envolvidos, inspeção do diff e verificador local do Blender.
- [QA do Blender](qa.log): **RESULTADO: OK**. Conservação analítica preservada; erro da discretização da malha continua **0,0121%**. Corpo fechado e normais conferidos.
- Setor acompanha `z(r,lambda)` em sete estados, mantendo o azimute durante a deformação. Um quarto de fase gira 90° sem alterar a malha do líquido nem as coordenadas locais do setor; uma volta fecha a orientação.
- Modos editoriais sem tracers, inclusive com tentativa explícita de `marcadores=1`; modo QA permite ativar e ocultar os pontos.
- Morph segue monotônico e mantém o hold final. Rotação e forma continuam independentes.
- Projeção do recipiente conferida em todos os quadros gerados; sem clipping. Novos MP4 decodificados integralmente na montagem.
- Inspeção visual dos stills e quadros da rotação para confirmar leitura do setor em diferentes azimutes, sem aparência de bolhas.

## Limitações e parada

O setor é uma seleção visual presa à geometria, não uma parcela de material diferente nem uma simulação de fluido. A transparência atenua o contraste ao passar pela parte posterior; o indicador deve continuar discreto. A avaliação desta rodada é em 540×960, sem render final 1080×1920.

Sem integração ao vid_0022, sem aprovação do asset, sem commit ou push. Próximo passo: avaliação humana dos novos previews.
