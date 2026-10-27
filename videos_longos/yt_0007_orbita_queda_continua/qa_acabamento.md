# Longo 0007 — acabamento visual N01–N18

**Estado: preview silencioso concluído e conferido para revisão editorial.**

Implementação da reavaliação recebida em `reavaliacao_acabamento.md`. A base de arte, a abertura próxima da montanha, o acompanhamento dos lançamentos e os movimentos principais de zoom foram preservados. O trabalho permanece em preview silencioso, com header **GRAVITAÇÃO — ÓRBITAS**, marca oficial e ausência do contador.

## Resultado visual

**Terra:** `superficie.py` calcula o material somente no recorte exibido, com um pixel de imagem para cada pixel de saída. O mesmo campo de iluminação e material serve ao globo e ao horizonte; o contorno é vetorial e o detalhe geográfico desaparece gradualmente no grande aumento. Foram eliminadas a ampliação da imagem fixa de 512 pixels e a troca abrupta de material. As orientações são contínuas, sem quantização em graus. A câmera continua independente do estado físico em SI.

**Canhão e pedra:** tubo arredondado, boca escura com borda, culatra, suporte e duas rodas. As chamadas “canhão idealizado”, “pedra” e “velocidade inicial” entram em sequência; a seta parte da pedra. O aviso da montanha idealizada e do modelo sem atmosfera permanece.

**N05–N06:** identificação das massas e da distância; atração da Terra e lei `F_g=GMm/r²`; aceleração necessária ao círculo; composição de `GMm/r²=mv²/r` por cópias das relações anteriores e da massa da pedra. MF-Tools explicita os cancelamentos de massa e raio e a reorganização da igualdade. A raiz positiva dá a velocidade circular. Uma única seta radial representa a gravidade; nenhuma segunda força “centrípeta” foi acrescentada.

**N07–N08:** a altitude de 400 km é identificada antes do detalhe. O tempo físico, a distância na tangente e a queda aparecem antes das contas. As chamadas distinguem “queda” de “curvatura da órbita”. Duas expressões grandes são apresentadas e depois dão lugar a uma relação curta, com faixa inferior de leitura. Os avisos de aproximação e escalas distintas continuam presentes; o detalhe retorna ao mesmo planeta.

**N10–N12:** órbitas baixa e alta nomeadas, com chamadas ligadas às respectivas trajetórias e relógio comum. Em N11, partida, percurso e retorno motivam “uma volta”, `T` e `2πr`. A velocidade circular reaparece; seu radical é copiado para o denominador. MF-Tools acompanha a inversão da razão, a entrada do raio ao quadrado no radical e a combinação dos fatores de raio. A equação ocupa uma região própria à direita, separada da órbita. N12 conserva a relação anterior durante a generalização para o semieixo maior da elipse.

**N16–N17:** Terra e Lua recebem nomes; a Lua tem disco sombreado e crateras vetoriais. Velocidade tangente e atração terrestre acompanham seu movimento. A abertura de escala conserva as posições dos centros e avisa os tamanhos ampliados. O movimento terrestre é apresentado antes da busca do ponto comum. “Centro da Terra” e “baricentro” são nomeados em momentos separados, com ponto e cruz distintos. A ampliação e a visão geral compartilham a fase; o baricentro permanece fixo e dentro da Terra, com `r_b/R_T≈0,733`.

Os títulos seguem a proposta ligada ao fenômeno. N13 conserva os cinco lançamentos e seus reinícios explícitos; N14 mantém a distinção entre impacto físico e continuação matemática. N18 preserva as duas frases aprovadas e o retorno à montanha.

## Cor e tipografia

| Papel | Cor |
|---|---|
| Fundo | `#050816` |
| Terra e massa central `M` | `#267BFF` |
| Gravidade, `F_g`, `g`, aceleração radial | `#35D9FF` |
| Raios, distâncias, semieixo | `#745CFF` |
| Tempo, período, relógios, percurso temporal | `#EA63FF` |
| Pedra, velocidade, massa de teste, constantes, operadores e unidades | `#F5F7FF` |

Sombras e gradações derivam dessas famílias; o logo permanece intacto. A cor dos símbolos é declarada em LaTeX, sem comparação da forma geométrica dos glifos. Unidades, inclusive `s` em segundo, são protegidas da coloração de variáveis. Medidas distinguem valor em violeta e unidade em branco. Os textos usam Space Grotesk e as expressões formais usam MathTex.

## Física e verificações já concluídas

- `modelo_orbital.py` preservado. Constantes, casos iniciais, condições de impacto, integração e storyboard conceitual permanecem.
- `validar_acabamento.py`: física dos cinco lançamentos, fechamento das órbitas ligadas sem colisão, primeiro impacto, independência da projeção e oclusão aprovados; resultados em `validacao_acabamento.json`.
- Referências a 400 km preservadas: `v≈7672,5986 m/s`, `g≈8,6942505 m/s²`, `T≈92,41425 min`, queda local `≈4,347125 m` em 1 s.
- Densidade nativa verificada em 960×540 e 1920×1080, incluindo aumento extremo. O recorte nunca ultrapassa a resolução de saída. Teste de continuidade no antigo limiar globo/horizonte aprovado.
- Trecho de zoom renderizado em 1920×1080/15 fps e inspecionado também em PNG nativo. Evidências em `qa_acabamento/definicao1080/` e no vídeo técnico curto incluído no ZIP.
- Expressões estabilizadas e contagens/cores dos glifos conferidas. Teste específico protege unidades sem retirar a cor de `s` como distância ou confundir `T` temporal com o índice de `R_T`.
- Compilação Python e captura estática dos marcos executadas. Render completo e revisões locais executados nesta unidade. A montagem copia pacotes H.264 e verifica a quantidade de frames de cada bloco.

## Conferência do arquivo entregue

Arquivo entregue: **488,1333 s (8min08,1s), 7.322 frames, 960×540, 15 fps, H.264/yuv420p, CRF 23 de preview, nenhuma faixa de áudio**. Os 18 blocos e suas contagens de frames foram conferidos na montagem sem recompressão. Resultados em `qa_acabamento/tecnico.json` e `montagem_acabamento.json`.

Extraídos e inspecionados **68 quadros de marcos/finais em 12 pranchas**, além de **216 amostras temporais em 18 pranchas**. As imagens provêm do MP4 montado. Foram conferidos o afastamento das contas em N07, as chamadas das órbitas em N10, a construção e separação da fórmula em N11 e a sequência de identificação e movimento em N16–N17. A inspeção visual é por amostragem temporal, sem alegação de examinar visualmente cada frame individual.

A auditoria de amarelo decodificou os **7.322 frames** e não encontrou ocorrências na amostragem espacial de um pixel a cada quatro por eixo, excluindo a região da marca oficial. Resultado em `qa_acabamento/paleta.json`. A definição em 1080p foi conferida no trecho curto de zoom; não foi renderizado um vídeo completo em 1080p.

## Teste do arsenal e custo

Nenhum sólido Blender utilizado, conforme a ficha e a restrição desta rodada. Resolução principal: 960×540/15 fps; prova curta de definição em 1920×1080/15 fps. Não houve geração de sequências externas.

O cache guarda dois recortes RGBA. O teto teórico dos pixels em cache em 1080p é cerca de **15,8 MiB**; os temporários de cálculo e demais objetos do Manim não estão incluídos nesse número. Nos enquadramentos medidos, cada recorte ocupou de 0,24 a 4,62 MB. O cálculo isolado do material custou aproximadamente **58–358 ms em 540p** e **303–1664 ms em 1080p**, neste ambiente; a tabela por enquadramento está no JSON de validação. Esses tempos não são uma promessa de FPS de render.

Funcionaram a densidade adequada ao enquadramento, a iluminação contínua, o contorno e a oclusão compartilhada. A geografia continua esquemática. O teste 1080p cobre a definição do zoom; a unidade inteira permanece em preview 540p. A Lua conserva a aproximação circular esquemática aprovada, sem nova derivação lunar.

## Arquivos desta rodada

Alterados: `encenacao.py`, `geometria_visual.py`, `validar_repagina.py`, `ficha.md` e `.gitignore` da unidade.

Criados: `superficie.py`, `matematica_visual.py`, `cadeia_equacoes.py`, `sistema_lunar.py`, `validar_acabamento.py`, `montar_acabamento.py`, `fechar_acabamento.py`, `reavaliacao_acabamento.md` e este relatório. Cópias do código e do timing anteriores preservam a referência da repaginação. Os utilitários de extração e a regressão curta de câmera foram reutilizados.

Nenhum arquivo global, dependência ou outra unidade foi alterado por esta rodada. As alterações preexistentes no repositório foram preservadas. Sem branch, commit, PR ou publicação.

## Artefatos e fase

- `media_acabamento/preview_acabamento_0007_960x540_15fps.mp4` — preview completo silencioso.
- `avaliacao_acabamento_visual_0007.zip` — MP4, quadros, amostras temporais, pranchas, teste 1080p, relatórios e manifesto SHA-256.
- `timing_acabamento.json` e `montagem_acabamento.json` — tempos dos blocos e proveniência dos pacotes copiados.
- `qa_acabamento/` — conferências do arquivo montado.

A aprovação artística permanece com o usuário. O ritmo é editorial e silencioso; sincronização com narração pertence à etapa posterior. Voz, SRT, master, capa e publicação permanecem fora desta rodada. Os previews e ZIPs anteriores foram preservados.
