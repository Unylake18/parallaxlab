> Registro histórico da primeira versão. O usuário rejeitou seu resultado visual; os testes abaixo não representam aprovação didática ou estética. A revisão atual será descrita em `RELATORIO_REVISAO.md`.

# 5.2 — Lei de Biot–Savart · entrega da rodada

Data: 2026-10-17. Escopo concluído: **uma cena contínua + preview horizontal completo + QA**.

## Arquivos

Referência exclusiva do 5.1: `C:/Users/Pichau/PycharmProjects/manim-fisica/videos_longos/yt_0005_magnetostatica_forca_lorentz/cena.py`. Foram lidas as constantes, helpers, projeção W, abertura, tratamento de correntes e fechamento. Não existe `ficha.md` nessa unidade. O curto `vid_0005` não foi usado.

Helpers compartilhados consultados: `template/config_horizontal.py`, `template/fonts.py` e `template/layout_horizontal.py`. A posição curricular foi conferida em `docs/mapa_curricular.md`: **6.8**, mantendo **5.2** como identificação editorial do handoff.

Arquivos criados nesta unidade:

- `cena.py` — classe única `YT0006BiotSavart`, da abertura ao gancho de estrutura local.
- `fisica.py` — estados e grandezas derivadas de clínica, trecho, fios e espira.
- `ficha.md` — formato, escopo, referência e decisão de não integrar Blender.
- `qa_fisica.py` — verificação numérica independente das integrais, sinais e limites.
- `qa_referencia.py` — render apenas do fechamento real do 5.1, sem editar sua unidade.
- `qa_visual.py` — decodificação integral, capturas por estado e amostragem temporal.
- `RELATORIO.md` — este relatório.

O `git status --short` inicial já mostrava alteração em `yt_0005.../cena.py`. Ela foi preservada. Foi detectada atualização externa nesse arquivo durante a rodada; as constantes e o fechamento foram reconsultados. Nenhum arquivo do 5.1, template, assets, dependências ou documentação global foi editado nesta implementação. Sem branch, commit, PR ou push.

## Continuidade

Herdados do 5.1 longo:

| Convenção | Implementação no 5.2 |
|---|---|
| Fundo / texto | `#050816` / `#F5F7FF` |
| Campo magnético | `#EA63FF` |
| Corrente I, K, J | `#35D9FF`, conforme a gramática de correntes do B05 |
| Fios | `#7FB2FF` |
| Construções e componentes auxiliares | `#9C8CFF` |
| Força | `#5AA2FF` |
| Frame | 16×9, `template.config_horizontal` |
| Câmera espacial | `Scene` com a mesma projeção ortográfica W, controlada por beta/tau |
| Vetores | helper Arrow local equivalente; largura principal 5, campo 3, fio 6; ponta 0,26 |
| Tipografia | Space Grotesk Medium via helper oficial; matemática em MathTex |
| Escalas matemáticas | referência 46/38/30; ajuste de largura no SPLIT, sem perspectiva no texto |
| Marca | watermark com largura 1,92 e opacidade 0,45; mesmo cabeçalho e margens |
| Transições | Fade, ReplacementTransform e TransformMatchingTex |
| Organização | métodos didáticos locais, uma única cena; FOCUS, SPLIT e BUILD |

Os dois fios da abertura recuperam a geometria do encerramento do 5.1. `txt`, `eq`, labels com halo, setas, limpeza e notas são equivalentes locais dos helpers de referência. O cache da espira segue o padrão de cache geométrico do `mk_bgrid()` do 5.1, com todos os estados físicos e de vista na chave, sem arredondamento dos parâmetros.

As pausas de fala atualizam o estado final e reutilizam um quadro estacionário. Não há relógio ou fluxo por `dt` nesta unidade; todos os movimentos continuam sendo animações dos trackers. O texto aprovado orienta as pausas, sem áudio ou sincronização.

## Testes

Compilação final, **exit code 0**:

```powershell
uv run --no-sync --cache-dir videos_longos/yt_0006_magnetostatica_biot_savart/renders/uv_cache python -m py_compile videos_longos/yt_0006_magnetostatica_biot_savart/cena.py videos_longos/yt_0006_magnetostatica_biot_savart/fisica.py videos_longos/yt_0006_magnetostatica_biot_savart/qa_fisica.py videos_longos/yt_0006_magnetostatica_biot_savart/qa_referencia.py videos_longos/yt_0006_magnetostatica_biot_savart/qa_visual.py
```

Import localizado, **exit code 0**, classe encontrada e frame **16×9**:

```powershell
uv run --no-sync python -c "import sys;sys.path.insert(0,'videos_longos/yt_0006_magnetostatica_biot_savart');import cena;print('Import OK:',cena.YT0006BiotSavart.__name__);print('Frame:',cena.config.frame_width,cena.config.frame_height)"
```

QA físico, **16 verificações aprovadas**:

```powershell
uv run --no-sync --cache-dir videos_longos/yt_0006_magnetostatica_biot_savart/renders/uv_cache python videos_longos/yt_0006_magnetostatica_biot_savart/qa_fisica.py
```

O render e o import final foram executados no perfil validado, porque o perfil temporário do sandbox não carregou corretamente o MiKTeX e, em uma tentativa de import, o registro nativo da fonte. Não houve reinstalação ou alteração do ambiente.

## Preview

Comando executado a partir da raiz do projeto:

```powershell
$env:SEG=''
uv run --no-sync python -m manim -r 960,540 --fps 15 --media_dir videos_longos/yt_0006_magnetostatica_biot_savart/renders --progress_bar none -v WARNING videos_longos/yt_0006_magnetostatica_biot_savart/cena.py YT0006BiotSavart
```

- Classe: **YT0006BiotSavart**.
- MP4: `C:/Users/Pichau/PycharmProjects/manim-fisica/videos_longos/yt_0006_magnetostatica_biot_savart/renders/videos/cena/540p15/YT0006BiotSavart.mp4`.
- Resolução: **960×540**. FPS nominal: **15**.
- Duração medida no contêiner: **985,253 s — 16min25,253s**.
- Quadros decodificados: **14.779**, sem erro de decodificação.
- Codec / formato: **H.264 / yuv420p**.
- Peso: **9.323.853 bytes**.
- Sem voz, SRT, legendado, master, capa ou publicação.

## QA físico

- **Biot–Savart:** vetor R sempre da fonte ao observador; produto na ordem dℓ × R; formas com R unitário/R² e R vetorial/R³, além do módulo com seno. Checagem dimensional em teslas.
- **Regime:** as duas derivadas temporais são hipóteses; divergente de J igual a zero decorre da continuidade com carga estacionária. A estacionariedade de J não é atribuída à continuidade.
- **Clínica:** 361 estados testados entre 0° e 90°. R fica em 2,6, com variação apenas de ponto flutuante: 2,5999999999999996 a 2,6000000000000005. Campo nulo em zero; máximo em 90°; razão de magnitudes igual a seno. P, R, arco, valor e campo dependem de `theta_local`.
- **Notação:** θ reservado ao ângulo entre dℓ e R; α reservado à substituição do trecho. Indicadores e arcos usam o mesmo `x_src`; relação assinada interna θ = π/2 + α conferida.
- **Interpretação:** o trecho aparece inicialmente em circuito fechado. B total é distinguido de B do trecho e B do restante.
- **Trecho finito:** R = −x x̂ + a ŷ; produto vetorial = a dx ẑ; direção +z em todas as posições mostradas. Substituição nasce do triângulo, passa por x = a tan α, dx e denominador, até o integrando com cosseno. Sinais αA < 0 e αB > 0 mostrados antes dos módulos positivos. Quadratura direta em quatro geometrias: erro máximo **2,659×10⁻¹¹** em unidades sem o prefator comum.
- **Fio infinito:** resultado μ₀I/(2πa) surge do limite do trecho. Extensão e ângulos são derivados de `L_wire`; indicação formal de limite substitui os valores finitos. Erro relativo do teste numérico de limite: **2,205×10⁻¹²**; dependência 1/a conferida.
- **Força entre fios:** campo do fio 1 no segundo, depois produto vetorial e F/L = μ₀I₁I₂/(2πd), em N/m. As quatro combinações de sinais foram testadas. Mesmos sentidos atraem, opostos repelem; forças opostas entre si. Ao inverter I2, B1 permanece, porque I1 e d permanecem.
- **Espira:** ortogonalidade dℓ·R = 0 em todos os estados testados. Pares φ e φ+π têm transversais opostas e axiais iguais; soma axial explícita 2dBz. Integração vetorial independente por cordas, inclusive z negativo: erro máximo **2,493×10⁻¹⁰** sem o fator μ₀I. Resultado Bz(z) = μ₀IR²/[2(R²+z²)³ᐟ²].
- **Centro:** transversais exatamente zero em z = 0; cada contribuição já é axial. Resultado μ₀I/(2R). Nenhum cancelamento lateral fictício é desenhado.
- **Distante:** a expressão geral aparece antes de o observador sair do centro. O esquema graduado em z/R mantém a fonte legível. Para z/R = 12, a aproximação com |z|³ tem erro relativo de **1,043%**, e é apresentada como assintótica. Simetria em z e decaimento 1/|z|³ conferidos.

Evidência numérica: `renders/qa_fisica.json`.

## QA visual e de continuidade

Método: decodificação do vídeo inteiro; inspeção dos **44 estados didáticos**, **197 amostras temporais a cada cinco segundos**, capturas em resolução completa nos pontos críticos e comparação com o fechamento real do 5.1. Os timestamps dos estados foram alinhados à lista real das partes do MP4, eliminando a diferença entre o relógio estimado do cache e os quadros do contêiner.

Conferidos: fórmulas completas, labels, contraste, vetores, direção da fonte ao observador, arcos θ/α, câmera, transições, branding e faixa inferior. A auditoria de enquadramento dos textos/equações registrou **zero saídas dos limites previstos**. Símbolos gregos nas notas usam MathTex; os indicadores numéricos têm colunas fixas. O arco da clínica não possui preenchimento. A nota de atração sai antes da inversão dos fios. A síntese cabe em uma linha.

A comparação de continuidade usa o fechamento atual do 5.1, renderizado por `qa_referencia.py` dentro desta unidade, e a abertura do 5.2. Frame, fundo, fios, campo, força, fonte, marca, espessuras e composição permanecem na mesma linguagem.

Evidências:

- `renders/qa_video.json` — metadados e integridade.
- `renders/qa_timeline_video.json` — estados e seções com tempos reais do MP4.
- `renders/qa_visual/estados_00.jpg` a `estados_03.jpg` — estados didáticos.
- `renders/qa_visual/temporal_00.jpg` a `temporal_16.jpg` — amostragem temporal.
- `renders/qa_visual/continuidade_00.jpg` — comparação 5.1 → 5.2.
- `renders/referencia_51/videos/540p15/QAContinuidade51.mp4` — referência de QA, 13 s, sem editar o 5.1.
- `renders/render_qa_fechado.log` — render entregue.

## Teste do arsenal

**Nenhum sólido Blender integrado**, conforme o handoff. Vetores, curvas, espira, componentes e projeção são Manim. Não houve sequência 3D, preparação com `ponte.py` ou custo/peso de assets Blender. Resolução testada: 960×540. Veredito: **não aplicável nesta unidade**, por decisão explícita do briefing.

## Limitações e parada

Nenhuma pendência física, de clipping ou de enquadramento foi identificada após as correções. A avaliação visual foi feita por estados e amostragem temporal; a integridade foi verificada em todos os quadros.

Rodada encerrada em **cena + preview completo + QA**. Nenhuma fase seguinte foi iniciada.
