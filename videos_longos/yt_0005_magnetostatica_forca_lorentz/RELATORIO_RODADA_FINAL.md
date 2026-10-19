# yt_0005 — rodada final de correções (antes da narração)

Entrega: contínuo B01–B09 revisado, 960×540 / 30 fps, silencioso. **14:44,3** (a versão anterior tinha 14:53,4; −9,1 s, sobretudo na hélice e em pausas de transição).
Não foi gerada narração, música, legenda nem publicação. Nenhum arquivo global alterado. Sem commit.

## Arquivos
- `yt0005_continuo_final_540p30.mp4` — render único de ponta a ponta de `YT0005MagnetostaticaM1` (sem `SEG`), tentativa 1, sem erro.
- `cena.py` — idêntica à usada no render (conferida byte a byte com a cópia guardada em `renders/redesign/final5/`).
- `pontos_corrigidos/` — folhas de contato dos pontos corrigidos e das transições (1 quadro a cada 1–3 s), mais `qa_fisica_rodada_final.txt` e `revisao_notas.md` (lista da revisão completa).

## O que foi feito
1. **Sinal de q (3:36–3:52):** dois casos físicos separados, com troca discreta (nada interpola o sinal e a rapidez fica constante). Carga, trajetória, F, v, espaço das velocidades, gráficos e fórmula (`v_y = −v⊥ sen ωt` para q<0) trocam juntos; relógio e condição inicial reiniciam. Rótulos "gira no sentido horário/anti-horário".
2. **Objetos residuais (4:32–5:08):** carga, v⊥, F e trilha do círculo saem por inteiro ao entrar a hélice e voltam só quando o círculo reaparece.
3. **Retorno à força centrípeta (5:00):** a composição anterior sai antes do novo título; o título ficou menor e no alto da coluna.
4. **Analisador (B08, 13:20–14:05):** feixe reto fora do campo → semicircunferência inteiramente dentro da região de B → sai pela borda de entrada; fundo, borda e símbolos de B delimitam a mesma região; vale para q>0 (curva para baixo) e q<0 (para cima). A região de B não cobre o trecho reto.
5. **Nomes dos resultados:** os 11 pedidos aparecem junto de cada resultado (força magnética; oscilador harmônico para v_y; frequência angular ciclotrônica; raio da órbita magnética; período ciclotrônico; passo da hélice; teorema trabalho–energia; força sobre fio com corrente; equação da continuidade; condição de seleção de velocidades; razão carga–massa em módulo).
6. **Álgebra:** integração com igualdades alinhadas, uma operação por vez e `+C` na primitiva (cancela nos limites); |q|/m rastreável (m desce, B atravessa a igualdade, v→E/B). Todas as trocas entre fórmulas passaram a ser saída/entrada limpa (sem deformar glifos); `TransformMatchingTex`/MF-Tools só onde pedido (nenhum ponto exigiu o glyph map).
7. **Síntese final (14:10–14:25):** transições curtas; círculo→hélice com correspondência geométrica; frases sem se deformar umas nas outras.
8. **Acabamento:** diagrama de velocidades com folga entre painéis/eixos; células de continuidade com entrada = saída (divergência nula, coerente com o fluxo uniforme); B nos fios por setas tangentes fixas; título do B04 sem colisão com o painel; cards de energia com o texto sempre acima do pulso.
9. **Hélice:** primeira apresentação encurtada, conclusão sobre v∥ preservada; a construção posterior de passo e variações ficou intacta.

## Verificações
- `qa_fisica_rodada_final.txt` (TUDO OK): dv/dt = (qB/m)(v_z,−v_y) integrado por RK4 e comparado com as soluções analíticas para q>0 e q<0 (erro < 1e−12); |v| constante (erro 3e−15); R = m v⊥/(|q|B), T = 2πm/(|q|B), p = 2πm v∥/(|q|B); `Orbit` da cena coerente com a solução e com F = q v×B; primitiva de sen por derivação numérica e ∫₀ᵗ v⊥ sen = (v⊥/ω)(1−cos ωt); B08: arco dentro da região, reta fora, saída em y = ∓2R, para os dois sinais.
- `py_compile` e checagem de nomes indefinidos (AST).
- Testes locais antes do render final: abertura→M1-06, trecho K e B04.
- Render final: 26.529 quadros decodificados sem erro, sem tempos não crescentes e sem lacunas > 50 ms.
- Revisão visual completa de rascunho anterior (1 quadro/s, 0:00–14:44) e do final nos pontos corrigidos e nas transições.

## Limitações reais (não declaro o vídeo aprovado)
- **Trocas por crossfade** deixam dois textos sobrepostos por ~0,5–0,8 s (ex.: 13:50 "q<0: curva para cima" × "o sentido da curva dá o sinal de q"; 10:58 frase×equação). São transitórias e legíveis, mas ainda são sobreposições.
- 7:10 e 7:11: o rótulo "F_B força magnética" passa sobre o arco do círculo (com halo, legível).
- Não foi feita inspeção quadro a quadro dos 26.529 quadros; a revisão foi por amostragem (1–3 s) e por sequências nos pontos de risco.
- Pausas estáticas de leitura (3–4 s) permanecem; a sincronização fina será feita com a voz.
- O verde da corrente é o do `vid_0009`; v⊥ continua branco no B01 e violeta no restante (gramática anterior).

## Teste do arsenal
Nenhum sólido Blender integrado (o B06 é 2.5D em Manim).
