# QA — vid_0015, preview silencioso V3

Rodada de 2026-10-06. Implementação do handoff V3, sem iniciar outra fase.
V1 e V2 preservadas como histórico; este relatório corresponde à V3.

## Arquivos e artefatos

- `cena.py`: implementação V3, classe `LinhasCarga015`.
- `ficha.md`: registro do briefing aprovado e requisitos da V3.
- `inspecionar_preview.py`: decoder, estados, transições e pacote para Produção.
- `auditar_cena.py`: auditoria localizada de tipografia e spans matemáticos.
- `qa_preview.md`: relatório atual.
- `cena_v2.py`, `qa_preview_v2.md`, `inspecionar_preview_v2.py`: cópias históricas.
- `auditoria_v3.json`, `auditoria_v3.log`: auditoria tipográfica/matemática.
- `qa_estados_v3.json`: 82 estados e 24 transformações MF-Tools.
- `qa_tecnico_v3.json`: medidas técnicas e associação de cada estado ao PNG.
- `render_preview_v3.log`: saída do render.
- `media/videos/cena/960p15/vid_0015_preview_v3_silencioso.mp4`: preview.
- `frames_preview_v3/`: 82 estados do MP4, 32 quadros intermediários e contatos.
- `frames_producao_v3/`: 19 JPGs com seis frames por imagem, em ordem temporal.
- `vid_0015_v3_frames_producao.zip`: as mesmas 19 imagens para envio à Produção.

Os 114 frames estão agrupados em 19 anexos, abaixo do limite de 20. Cada célula
mantém o frame em 540×960; identificação/tempo ficam fora do vídeo.
Nenhum arquivo global ou de outra unidade foi alterado nesta rodada.
Alterações preexistentes das outras unidades foram preservadas.

## Cadeias matemáticas implementadas

1. **Gauss:** integral fechada de E·dA=Q_enc/ε₀; Q_enc=λℓ;
   integral=E A_lat; substituição da carga; A_lat=2πdℓ;
   E(2πdℓ)=λℓ/ε₀; cancelamento de ℓ; E(2πd)=λ/ε₀;
   E(d)=λ/(2πε₀d).
2. **Elétrica:** q=λℓ; F_E=qE; F_E=(λℓ)E(d); substituição de E;
   F_E=λ²ℓ/(2πε₀d); F_E/ℓ=λ²/(2πε₀d).
3. **Ampère:** B paralelo a dℓ e constante pela simetria;
   integral fechada de B·dℓ=μ₀I_enc; I_enc=I; substituição de I;
   retirada de B da integral; B∮dℓ=μ₀I; comprimento 2πd;
   B(d)(2πd)=μ₀I; B(d)=μ₀I/(2πd).
4. **Magnética:** vetor F_B=I vetor ℓ × vetor B; +x×(−z)=+y;
   F_B=IℓB sen 90°; F_B=IℓB; substituição de B;
   F_B=μ₀I²ℓ/(2πd); F_B/ℓ=μ₀I²/(2πd).
5. **Igualdade:** cópias das duas forças por comprimento; igualdade dos módulos;
   cancelamento de 2πd; λ²/ε₀=μ₀I²; λ²=μ₀ε₀I²;
   I²/λ²=1/(μ₀ε₀); raiz e módulos; |I|/|λ|=1/√(μ₀ε₀);
   definição de c; pausa em |I|/|λ|=c.
6. **Corrente das cargas:** retorno ao movimento do enunciado; trecho vΔt
   atravessando ponto fixo; Δq=λvΔt; I=Δq/Δt; substituição;
   cancelamento de Δt; I=λv; |I|=|λ|v; |I|/|λ|=v;
   recuperar primeiro payoff; v=|I|/|λ|=c; pausa em v=c.
7. **Razão:** divisão completa das expressões F_B/ℓ e F_E/ℓ;
   cancelamento de 2πd; F_B/F_E=μ₀ε₀I²/λ²; recuperar |I|/|λ|=v;
   elevar ao quadrado; F_B/F_E=μ₀ε₀v²; recuperar μ₀ε₀=1/c²;
   substituir; F_B/F_E=v²/c² antes do gráfico.

A expressão corrente se transforma em cada passo. Referências ficam somente
quando necessárias. A duração não foi encurtada para imitar a V2.

## Tipografia, MF-Tools e layout

Auditoria AST: nenhum Text/MarkupText/Paragraph fora do helper oficial; nenhum
texto de tela em MathTex. Amostra em runtime confirma Space Grotesk.
Texto usa Space Grotesk Medium via `template.fonts.screen_text`; matemática usa
MathTex; readouts numéricos usam DecimalNumber. Logo permanece asset.

34 expressões GlyphEq construídas no preflight, com glifos/spans verificados,
inclusive a fração dupla. As 24 passagens TransformByGlyphMap usam string única
estabilizada e auto_fade. Controlam cancelamentos de ℓ, 2πd, Δt e |λ|,
reorganizações, raízes/módulos, cópias deliberadas de c, v² e 1/c² e conversões
entre razão compacta e fração. TransformMatchingTex atende às correspondências
naturais. Não há índices/debug no vídeo.

Regiões locais estáveis: HEADER, TITLE, PHYSICS, MATH, SECONDARY e SUBTITLE SAFE.
O gráfico sai antes da conclusão. Sistema centralizado, seguido de v<c,
F_B/F_E=v²/c²<1, F_B<F_E e REPULSÃO LÍQUIDA. Região inferior reservada para
legendas futuras permanece livre. Template preservado.

## Transição Gauss → Ampère e gráfico

Uma seção interior é marcada no cilindro inteiro. A superfície e as duas tampas
são atenuadas e removidas; a seção sobrevive e seu contorno vira curva amperiana.
Não há compressão física do cilindro. Curva de integração e B tangente têm códigos
visuais distintos. Mão direita encadeia corrente/polegar, enrolamento/dedos e campo.
O ⊗ fica separado, com halo abaixo do glifo e guia neutra curta até P.

No gráfico, um único tracker controla ponto, curva revelada, readouts, seta
magnética, resultante e deslocamento da linha 2 atual frente à referência fantasma
fixa. F_E constante; F_B/F_E=β²; resultante normalizada=1−β².
β=v/c percorre 0; 0,2; 0,6; 0,85; 0,97; 0,995, sempre abaixo de 1.
Limite v=c é fronteira marcada. “MODELO IDEAL · linhas infinitas de carga” permanece.
Nota sobre elétrons num fio aparece no início e depois sai. Rótulos ampliados.

## Comandos executados

```powershell
uv run --no-sync python -m py_compile videos/vid_0015_linhas_carga_movimento/cena.py videos/vid_0015_linhas_carga_movimento/auditar_cena.py videos/vid_0015_linhas_carga_movimento/inspecionar_preview.py
uv run --no-sync python videos/vid_0015_linhas_carga_movimento/auditar_cena.py
uv run --no-sync python -m manim -r 540,960 --fps 15 --media_dir videos/vid_0015_linhas_carga_movimento/media -o vid_0015_preview_v3_silencioso videos/vid_0015_linhas_carga_movimento/cena.py LinhasCarga015
uv run --no-sync python videos/vid_0015_linhas_carga_movimento/inspecionar_preview.py
```

Ambiente e dependências preservados; somente a variante V3 foi renderizada.
Resultado: H.264, 540×960, 15 fps nominal, 5.226 quadros, nenhum stream de áudio,
348,396 s (5min48,4s). Decoder verifica todos os quadros e intervalos compatíveis
com 15 fps. Arredondamento de PTS inferior a 1 ms nas fronteiras; medidas exatas
no JSON técnico. Comandos encerrados com código 0.

## Estados inspecionados

| Grupo | Estados e tempos aproximados |
| --- | --- |
| Enunciado e forças opostas | 01–03, 2,8–12,9 s |
| Cilindro, radial, lateral e cada tampa | 04–08, 18,9–34,2 s |
| Gauss completo | 09–17, 39,1–66,0 s |
| Campo externo e força elétrica | 18–23, 71,8–90,1 s |
| Seção no cilindro e superfície → curva | 24–26, 95,9–104,3 s |
| Ampère completo | 27–35, 110,8–138,4 s |
| Mão direita, ⊗ e produto vetorial | 36–38, 144,4–157,4 s |
| Força magnética completa | 39–43, 161,7–176,9 s |
| Igualdade, cancelamentos e primeiro payoff | 44–51, 181,7–210,4 s |
| Retorno, derivação da corrente e v=c | 52–63, 217,2–263,8 s |
| Derivação completa da razão | 64–72, 270,5–299,0 s |
| Exploração do modelo ideal | 73–78, 306,6–328,3 s |
| Condição massiva e conclusão separada | 79–82, 334,2–345,9 s |

Inspeção visual de 82 estados e 32 quadros intermediários extraídos do MP4.
Estados/transições afetados pelas correções finais novamente conferidos no vídeo
atualizado. Intermediários incluem seção, enrolamento, trecho atravessando P,
mapas de glifos e variação do gráfico.

QA físico: E radial; lateral paralela a dA; em cada tampa, E perpendicular ao
vetor área axial, cada uma com fluxo zero individualmente; Gauss usa superfície;
Ampère usa curva e circulação, sem “fluxo magnético”; campo da linha 1 atua na
linha 2, sem força pelo campo próprio. Geometria horizontal aprovada: corrente +x
na linha superior, B=−z na inferior, +x×(−z)=+y; F_B para cima, F_E para baixo.
Primeiro payoff precede I=λv; v=c somente após retorno; modelo ideal explícito;
F_B nunca ultrapassa F_E para v<c. Texto de retorno aprovado preservado:
“Mas aqui a corrente é produzida justamente pela própria linha de carga em movimento.”

## Correções e limites

Corrigidos: distância entre vΔt e seta de velocidade; legibilidade da fração dupla;
referência correta das constantes; halo que escondia ⊗; sobreposição na entrada
de v<c; deformação em substituições de referências, conversões da razão compacta
e cópias para F_B<F_E. Mapas finais acompanham símbolos individualmente.

Movimentação da linha é qualitativa, conforme briefing: sem integração dinâmica,
massa, aceleração ou tempo físico. Não foi encontrada inconsistência objetiva que
exigisse reabrir decisões aprovadas. Não ficaram pendências técnicas/visuais
identificadas nos pontos inspecionados. Voz, SRT, master, legendado, capa,
publicação e render final não foram iniciados.
