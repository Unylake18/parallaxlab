# Superfície de um líquido em rotação

formato: curto_vertical

Série pública: **POR TRÁS DA FÓRMULA · EP. 08** (número confirmado pelo usuário)

Fase: postagem V4 renderizada e validada, após aprovação do preview revisado. Fontes e previews anteriores preservados. Unidade: `vid_0022`. V1, V2, V3, V3.1 silenciosa e preview sincronizado preservados.

- Cena de postagem atual: `cena_v4_postagem.py`, classe `LiquidoRotacao022V4Postagem`; preview aprovado em `cena_v4.py`. Postagem anterior em `cena_postagem.py`; V3.1 em `cena_v3_1.py`, V3 em `cena_v3.py`, V2 em `cena_v2.py`, V1 em `cena.py`.
- Postagem: 170,8 s, 1080×1920, 30 fps nativos, H.264/yuv420p/CRF 14, áudio AAC e início rápido de reprodução. Master e legendado em `renders/vid_0022_v4_postagem_*.mp4`, copiados para `entregas/` pelo fluxo oficial.
- Duração V3.1: 168 s; preview 540×960, 15 fps (V3/V2: 168 s; V1: 174 s).
- Pergunta: “Por que a superfície de um líquido girando vira uma parábola?”
- Inercial, +r para fora: a_r = −ω²r. Sem força centrífuga.
- Pressão radial construída pelas duas faces de um elemento local plano: F_r = p(r)A − p(r+dr)A ≈ −(∂p/∂r)A dr.
- Newton: ∂p/∂r = ρω²r > 0. Hidrostática vertical: ∂p/∂z = −ρg.
- Superfície isobárica: regra da cadeia de p(r,z(r)) = p_atm, explicitamente.
- Resultados: z(r) = z0 + ω²r²/(2g); Δh = z(R)−z(0) = ω²R²/(2g).
- z0 é z(0) no estado final; não é o nível inicial plano. Derivação com r≥0; espelhamento somente no final.
- Space Grotesk para texto, MathTex para matemática; área abaixo de y=−5,8 reservada, exceto marca.

solido_3d: liquido_rotacao

Asset aprovado explicitamente. Handoff V2 autoriza quatro inserções: fenômeno, localização/extração do elemento, superfície isobárica e payoff. Sem tracers. A álgebra permanece Manim 2D. Cor: coordenadas ciano, pressão violeta/magenta, forças brancas, superfície azul-ciano.

Sequências da abertura preparadas por `preparar_3d.py` via `ponte.sequencia`, abertas por `Solido3D(render='nunca')`. `preparar_3d_v2.py` acrescenta um estado de seção sem grid e um payoff local de 76 PNGs, com os controles existentes de revelação e paralaxe de 4°. Exporta projeções da seção, região interna, superfície e Δh. Nenhum construtor ou helper global foi alterado. Abertura usa somente a metade crescente do morph; o morph é interpolação didática, não dinâmica do transiente.

V3 reutiliza integralmente os caches e projeções V2, sem render Blender ou alteração do asset. Seção 2D preenchida, raio medido na altura do elemento, zoom com identidade magenta, fórmulas consumidas, meridiana imóvel durante a retirada do 3D, projeção radial e triângulo da tangente, z(0)=z0 no vértice, síntese causal por transformação e bracket de Δh ligado ao objeto. Header e branding V2 preservados.

V3.1 preserva essa estrutura. Headlines curtas e centralizadas na largura segura de 7,4; zoom/cancelamentos sem headline; rótulos locais ancorados; contexto azul durante o zoom; gradiente de pressão contínuo; dr/gradiente radial e dz/gradiente vertical compartilham as cores na regra da cadeia; relação da inclinação acompanha a tangente. Payoff 13,6% maior que na V3. Conclusão em três batidas separadas: Δh, seção e transformação inclinação→altura quadrática, paraboloide limpo e frase final.

Marcos V3: fenômeno 0–12; corte/extração/zoom 12–26; movimento e dimensões 26–32; pressão/Taylor 32–55; Newton/pressão radial 55–69; vertical 69–81; isobárica 3D/deslocamento/regra da cadeia 81–101; inclinação móvel 101–119; integração/espelhamento 119–140; síntese causal 140–149; payoff/Δh/conclusão 149–164; logo + @labparallax 164–168 s.

MF-Tools: mapas explícitos transportam fatores na substituição de Taylor, cancelamento das pressões iguais, Newton, balanço vertical, regra da cadeia, substituição dos gradientes, diferencial, integrais e solução. Fontes são MathTex de string única; nenhuma numeração de glifos aparece no vídeo.

A rodada de acabamento silencioso não incluiu voz ou SRT. A etapa seguinte, autorizada pelo usuário, sincroniza o WAV recebido e acrescenta legendas coloridas: `preview_legendado.mp4`, `preview_sincronizado.mp4`, `legenda.srt` e `legenda_colorida.ass`. Duração montada: 170,8 s, 540×960/15 fps. Referência textual: texto da gravação confirmado pelo usuário (458 palavras), com tempos estimados por pausas/frases; ver `sincronizacao.md`. A montagem segue a ordem narrada: seção → paraboloide/desnível → síntese causal → frase final → chamada sobre a marca. A primeira sincronização baseada na R2 foi preservada em `sync_anterior_r2/`. Essa etapa de preview foi seguida pelo fechamento de postagem descrito abaixo.


Postagem autorizada e concluída: render nativo em 30 fps, com transições de equações limitadas a 1,4 s e pausas separadas para leitura. Interpolação local dos quadros 3D reduz os saltos entre poses. Mantidos a estrutura didática, os 12 mapas de glifos, a voz recebida e a sincronização aprovada; não foi utilizado o preview de 15 fps como fonte do final. Legendas: 65 entradas, 458 palavras, cores semânticas do vídeo. QA completo: decodificação dos 5.124 quadros de cada final, cadência constante, CRF 14, áudio completo, inspeção de 41 instantes e verificação de 15 movimentos matemáticos. Ver `postagem.md` e `qa_postagem/validacao.json`. Sem capa nova ou publicação nesta rodada.


Revisão V4: `cena_v4.py`, classe `LiquidoRotacao022V4`. Preview 540×960 a 30 fps nativos, 170,8 s, com a voz e as legendas existentes. Abertura com rotação ampliada, desenho do perfil e textos de co-rotação; corte, extração e distância radial redistribuídos pelas frases. Área, espessura, volume e massa aparecem em etapas; um único elemento retangular percorre uma órbita com velocidade tangente e aceleração centrípeta. O zoom local mostra as forças, e o balanço vertical recebe cópias dos termos associados aos vetores. Adicionadas ênfases no sinal, percurso no campo de pressão e varredura da tangente. `@labparallax` reduzido de 33 para 28 e com degradê ciano→azul. Saídas: `preview_v4_legendado.mp4` e `preview_v4_sincronizado.mp4`. QA completo do preview em `qa_v4/validacao.json`; relatório em `revisao_v4.md`. O preview V4 foi aprovado para o fechamento de postagem descrito abaixo.


Fechamento V4 autorizado e concluído em 12/10/2026: render completo nativo em 1080×1920/30 fps, H.264/yuv420p/CRF 14, preservando movimentos, textos, sincronização, legendas coloridas e `@labparallax` menor em degradê. Reutilizados os 397 quadros 3D nativos existentes, sem novo Blender. Montagem em `montar_v4_postagem.py`; QA em `verificar_v4_postagem.py`. Ambos os finais têm 5.124 quadros, 170,8 s de vídeo e 166,8 s de áudio. QA técnico e inspeção de 55 instantes aprovados. Entrega oficial atualizada pelo fluxo `videos/entregar.py vid_0022`; fontes antigas permanecem na unidade. Relatório: `postagem_v4.md`.
