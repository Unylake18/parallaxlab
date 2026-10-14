# VID 0022 — V3 editorial silenciosa

V3 implementada para **POR TRÁS DA FÓRMULA · EP. 08**, preservando física, resultados, asset, header e branding aprovados. A V2, seu código e seu MP4 permanecem disponíveis para comparação.

## Preview

- [Abrir preview V3](media/videos/cena_v3/960p15/preview_silencioso_v3.mp4).
- Caminho absoluto: `C:\Users\Pichau\PycharmProjects\manim-fisica\videos\vid_0022_liquido_rotacao\media\videos\cena_v3\960p15\preview_silencioso_v3.mp4`.
- Duração: **168 s / 2min48s**; MP4: 167,999 s.
- 540×960, 15 fps nominais, 2.520 quadros, H.264/yuv420p, sem áudio.
- Peso: 2.903.271 bytes / 2,77 MiB.
- [Metadados](qa_v3/metadados.json) e [marcos efetivos](marcos_v3.json).

## Mudanças V2 → V3

**Elemento:** seção frontal preenchida, eixo r=0, horizontal na altura do elemento e raio medido desde o eixo. A região magenta está dentro da água antes do zoom e mantém preenchimento e contorno na ampliação. Área, espessura, coordenadas e massa entram em sequência.

**Pressão e Newton:** os textos explicam as duas forças, o maior empurrão da face externa e a resultante para o eixo. As parcelas da força nascem dos rótulos das faces. Taylor é consumido na substituição; as pressões iguais desaparecem no cancelamento. A aceleração sai durante Taylor e volta como fonte de Newton. Massa e aceleração são transportadas para a equação e consumidas. O gradiente radial sai antes da análise vertical, que reutiliza o elemento e relaciona pressão ao peso. A faixa radial recebe indicações explícitas de posição e pressão.

**Extração da isóbara:** a meridiana branca permanece exatamente na posição projetada enquanto recipiente, restante da superfície e rótulos desaparecem. Há um breve estado com apenas a curva antes de ela ser enquadrada com os eixos. O ponto percorre a curva com dr/dz e p_atm; a igualdade isobárica e a derivada total vêm depois do movimento. A regra da cadeia destaca os dois deslocamentos.

**Inclinação e integração:** ponto e tangente percorrem continuamente o raio, acompanhados de projeção até o eixo r e pequeno triângulo de inclinação. A barrinha inferior foi removida. A curva cresce junto da integração, e z(0)=z0 fica marcado diretamente no vértice. O espelhamento ocorre depois da solução para r≥0.

**Síntese:** um único título acompanha gradiente radial → diferença de altura → tangente móvel → curva desenhada → parábola espelhada. As expressões são substituídas à medida que cumprem sua função. As trocas de títulos usam saída e entrada sequenciais, evitando títulos sobrepostos.

**Payoff e conclusão:** a parábola faz match com a meridiana projetada, com eixo vertical. O cache existente revela recipiente, superfície e grid, com paralaxe de 4°. A composição reserva espaço para o bracket de Δh e sua fórmula junto à borda; uma guia liga a medição à altura central. Depois de Δh, a conclusão retoma força centrípeta, superfície isobárica, inclinação proporcional a r e altura proporcional a r². A frase final antecede logo e @labparallax.

Foram preservados **12 TransformByGlyphMap**. Ao final de cada mapa, a composição canônica do MathTex é restabelecida, garantindo posições e sinais completos após o transporte dos glifos. Não há índices ou debug no preview.

## Arquivos

Criados nesta rodada: `cena_v3.py`, `validar_v3.py`, `inspecionar_v3.py`, `marcos_v3.json`, `relatorio_v3.md`, logs `validar_v3.log` e `render_v3.log`, preview e pastas `qa_v3/`, `qa_v3_preflight_01/`, `qa_v3_preflight_02/`.

Atualizado: `ficha.md`, para registrar a V3 como versão atual e descrever seu uso dos caches. Os arquivos V2 e os arquivos globais não foram alterados nesta rodada; alterações preexistentes do repositório foram preservadas.

## Validação e QA

- `py_compile` passou nos três módulos V3.
- Importação e construção completa sem vídeo passaram: 168 s e 12 mapas. Dois preflights com quadros estáticos permitiram revisar contexto, álgebra e composição antes do render.
- **Um único render completo V3**, concluído sem erro; 127 animações incluindo esperas.
- PyAV confirmou resolução, duração, fps, quadros, codec e ausência de áudio.
- Foram extraídos **47 quadros** do próprio MP4. As três folhas cobrem toda a unidade; estados críticos também foram conferidos em tamanho integral.
- Conferidos: elemento dentro da água e raio; continuidade do zoom; forças e desigualdade; Taylor/cancelamentos; consumo das fontes de Newton; rotação vertical; meridiana imóvel; movimento dr/dz e isóbara; regra da cadeia; tangente/projeção; integração/crescimento; z(0)=z0; espelhamento; quatro estados da síntese; match/revelação/paralaxe; bracket/fórmula de Δh; conclusão e branding.
- A presença do header foi verificada nos pixels de todos os 46 quadros amostrados anteriores ao cartão final. Não foi encontrado clipping impeditivo, sobreposição persistente de títulos ou expressão auxiliar órfã nos estados conferidos.
- `git diff --check` não apontou erro de whitespace; apenas aviso LF/CRLF em arquivo preexistente do arsenal.

Folhas de QA: [parte 1](qa_v3/folha_qa_1.png), [parte 2](qa_v3/folha_qa_2.png), [parte 3](qa_v3/folha_qa_3.png).

## Teste do arsenal

Sólido usado: **liquido_rotacao**, aprovado, com quatro inserções. Resolução: 540×960 RGBA, 24 amostras no cache. Sem tracers editoriais.

Todos os caches e projeções da V2 foram reutilizados: abertura, seção estática e payoff. **Nenhum render Blender nesta rodada; custo adicional de Blender: zero.** São 397 PNGs existentes, aproximadamente 179,12 MiB. O payoff usa os controles e a sequência locais já disponíveis; não houve alteração no asset, construtor ou ponte global.

Funcionou: correspondência espacial da meridiana, retirada progressiva do 3D, recuperação da superfície a partir da seção e medição conectada ao objeto. Não faltou parâmetro do arsenal para esta revisão. Qualidade/custo em 1080×1920 não foram avaliados nesta fase.

## Pendências e parada

Pronta para revisão editorial. Sem bloqueio técnico conhecido. A validação visual foi feita no preview 540p/15 fps e não constitui aprovação de um master final. Não foram produzidos voz, SRT, master, capa ou publicação; não houve render final, alteração de dependências, commit ou push.
