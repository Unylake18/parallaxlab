# Estado atual — Parallax Lab

**Atualizado em:** 2026-10-07 (arsenal de sólidos 3D em Blender, em sandbox); antes, 2026-10-06 (reconciliação dos vídeos 12–15 e do primeiro vídeo longo; segundo PC); antes, 2026-10-03 (suporte horizontal integrado; reconciliação dos vídeos 11–13) e 2026-10-01 (adoção do MF-Tools; reconciliação do `vid_0010`)

## Formatos: curto vertical + longo horizontal (2026-10-03)

- Trilha de YouTube longo aprovada para teste e **disponível tecnicamente** (decisão em `docs/decisoes.md`; regras em `docs/formatos.md`). **Primeiro vídeo longo: `yt_0001` — LEI DE GAUSS** (“O segredo não é a integral — é a simetria”), em `videos_longos/yt_0001_lei_gauss/`, **publicado segundo o usuário (2026-10-06)**. Foi desenvolvido na branch `video/long-0001`, num worktree em `C:\Users\Pichau\PycharmProjects\parallax-long`, e **integrado à `main` em 2026-10-06** (merge); a branch continua em `origin/video/long-0001` para ajustes. Final local: `renders/yt_0001_lei_gauss_final_1080p30.mp4` (1920×1080, 30 fps, 69,4 MB, 2026-10-05; `renders/` é ignorado pelo Git), com `.srt` ao lado. Segundo a `ficha.md`, a etapa final de 2026-10-05 foi voz ElevenLabs em 3 partes, sincronia por âncoras, legenda SRT e render 1080p. Os WAV da unidade (`narracao_final`, `narracao_montagem` e `partes/`, de 26 a 122 MB cada) **não são versionados**: passam do limite de 100 MB por arquivo do GitHub e estão no `.gitignore` (`videos_longos/*/audio/*.wav` e `partes/`); existem só no PC onde foram gerados, e o backup externo deles não está confirmado. **Segundo longo: `yt_0002_lei_gauss_casos_classicos`** — três simetrias e aplicações clássicas, continuação do `yt_0001`; pacote do Work aprovado como fonte canônica de Produção em 2026-10-06, com `ficha.md`, `narracao.md`, `producao.md` e `storyboard.md` na unidade, sem implementação. A pauta anterior de energia potencial foi descartada editorialmente e sua pasta removida por autorização do usuário. Próximo longo do módulo: exercícios mais elaborados de Gauss, com ID a definir; a implementação do `yt_0002` aguarda handoff específico, começando somente por N01–N03.
- Suporte horizontal **aditivo** integrado na `main` por fast-forward (commit `f78ddc8`, feito na branch `feat/formatos-curto-longo`, worktree `../parallax-formatos`): `template/config_horizontal.py` (frame 16 × 9, mesma paleta e watermark), `template/layout_horizontal.py` (regiões FOCUS/split, safe area, guias só com `GUIAS=1`), `template/smoke_horizontal.py` (cena `SmokeHorizontal`) e a pasta vazia `videos_longos/`.
- Smoke test renderizado e aprovado: **960×540, 15 fps, 168 quadros, 11,2 s**; SPLIT, MathTex, `TransformMatchingTex`, Space Grotesk, watermark e safe area conferidos por quadros. Final 1920×1080 não renderizado.
- `template/config.py`, os vídeos verticais e as dependências não mudaram; o worktree usou a `.venv` do checkout principal (`UV_PROJECT_ENVIRONMENT` + `uv run --no-sync`), sem criar `.venv` nova.

**Marca:** Parallax Lab · **Instagram aprovado:** @labparallax

**Guia vigente:** `docs/guia_mestre.md`, versão 1.6 (2026-10-01: MF-Tools); atualização editorial de 2026-09-23 preservada.

**Fonte operacional:** este arquivo; identidade detalhada em `docs/identidade_visual.md`.

## Ambiente e repositório verificados

- Windows + PyCharm; Python 3.12.4, `uv` 0.12.17, `.venv`, Manim Community 0.21.0 e MF-Tools 1.4.9 validados com `uv run python -m manim --version`; MiKTeX/MathTex já usados em renders.
- Projeto local: `C:\Users\KaioOrtiz\PycharmProjects\manim-fisica`; branch `main`.
- **Segundo PC (pessoal, 2026-10-06):** clone em `C:\Users\Pichau\PycharmProjects\manim-fisica`; ambiente criado com `uv sync` a partir do `uv.lock` (`uv` 0.12.22, Manim CE 0.21.0, MF-Tools 1.4.9), MiKTeX 26.5 e Git 2.55; preview `ATE=1` do `vid_0012` renderizado para provar o LaTeX. Os MP4 de `renders/` foram copiados à mão do Drive (a pasta é ignorada pelo Git). Commits deste PC usam a identidade de Git local ao repositório (`kaio.ortiz@usp.br`).
- Remoto `origin` configurado: `https://github.com/Unylake18/parallaxlab.git`.
- A consolidação técnica dos dois primeiros vídeos e a limpeza restrita de
  `media/` foram concluídas e enviadas ao `origin/main`. A `main` local e
  `origin/main` estavam sincronizadas naquele fechamento. A implementação do
  vídeo 3 e sua documentação já foram enviadas ao `origin/main`; `main` local e
  `origin/main` estão sincronizadas neste fechamento.
- A unidade de fechamento do `vid_0001` reúne a configuração visual, a cena, a narração final e a legenda no mesmo commit de produção.
- Preservar o ambiente: não reinstalar, recriar `.venv`, executar `uv init` ou alterar dependências sem diagnóstico concreto. MF-Tools foi adicionado a `pyproject.toml` e `uv.lock` em 2026-10-01 (commit `chore: adicionar MF-Tools ao pipeline`).
- **MF-Tools 1.4.9 adotado oficialmente (2026-10-01)** como dependência utilitária seletiva (`MF-Tools[manimce]==1.4.9`), compatível com Python 3.12.4 + Manim CE 0.21.0; presente em `pyproject.toml` e `uv.lock`. O fluxo de render continua `uv run python -m manim ...`. Uso seletivo: `TransformMatchingTex` segue padrão, `TransformByGlyphMap` só com ganho didático real, glyph maps depois de estabilizar o LaTeX; ver `AGENTS.md` e `docs/decisoes.md`.
- MVP: trabalhar em `main`, com commits pequenos; branch/PR para alterações maiores ou arriscadas.
- `AGENTS.md` é a instrução operacional vigente para agentes de código: contexto mínimo suficiente, validação proporcional ao que mudou e nenhuma expansão espontânea de escopo.

## Arsenal de sólidos 3D (Blender) — sandbox, sem uso em vídeo (2026-10-07)

- **O que é:** biblioteca de sólidos 3D reutilizáveis em `experimentos/blender/arsenal/`, descritos por fichas JSON (`solidos/<id>.json`) com "usar quando / não usar quando", parâmetros, enquadramento, custo de render e status. Índice legível e gerado: `experimentos/blender/arsenal/catalogo.md` (regerar com `python experimentos/blender/arsenal/gerar_catalogo.py`, que também valida as fichas). Padrão visual único em `experimentos/blender/arsenal/estilo.json`, derivado de `docs/identidade_visual.md` e da gramática de cor do 2D de `yt_0001`/`yt_0002`: ciano reservado ao campo elétrico, azul `#267BFF` (preenchimento) e `#7FB2FF` (contorno) para fontes físicas, violeta `#9C8CFF` tracejado/translúcido para superfícies gaussianas, branco para o neutro.
- **Estado:** **90 sólidos, todos `aprovado` pelo usuário em 2026-10-07** (os 57 anteriores, o `ima_espira_inducao` ajustado a pedido, os 30 da fila B e `centro_de_massa_3d` e `campo_conservativo`, as últimas lacunas 3D). Aprovados — Lei de Gauss: `casca_cilindrica_oca`, `cilindro_macico_isolante`, `casca_esferica_oca`, `esfera_macica_isolante`, `placa_infinita_carregada`, `cilindro_coaxial`, `gaussiana_esferica`, `gaussiana_cilindrica`, `gaussiana_caixa`; campo elétrico de distribuições contínuas: `anel_carregado`, `disco_carregado`, `haste_carregada` (anel, disco e haste têm `com_cargas=0` para uso em momento de inércia). Ampère: `solenoide_corrente`, `toroide_corrente`, `fio_infinito`, `amperiano_circular`, `amperiano_retangular`. **Cargas em movimento** (loop sem emenda, parâmetro `fase`) em 7 sólidos: fio, solenoide, toroide, anel, disco, haste e placa. Mecânica: `esfera_rolando`, `cilindro_rolando`, `aro_rolando` (rolam sem deslizar; a câmera acompanha o corpo e o chão corre, com eixo instantâneo violeta); Cálculo: `solido_revolucao_disco`, `solido_revolucao_arruela`, `solido_revolucao_cascas` (a fatia elementar violeta varre o sólido em vaivém). Os 6 também têm loop (`fase`). Eletromagnetismo: `capacitor_placas_paralelas` (com dielétrico opcional), `capacitor_esferico`; Óptica: `lente_delgada` (biconvexa e biconcava), `prisma_triangular`, `anteparo_fenda_dupla`; Termodinâmica e Fluidos (com loop): `caixa_gas_cinetica` (moléculas e êmbolo oscilante), `tubo_escoamento` (continuidade). Gravitação: `poco_gravitacional` (aprovado; potencial, bola em órbita circular) e `orbita_kepleriana` (elipse, setores de áreas iguais, loop de um período, corpo central com degradê); Cálculo vetorial (aprovados): `campo_vetorial` (radial, rotacional, sela, espiral; 2D ou 3D), `superficie_parametrizada` (remendo dS, r_u, r_v e n̂), `teorema_stokes` (hemisfério e contorno), `gradiente_colina` (curvas de nível e ∇f). MHS: `massa_mola`, `pendulo_simples`; Ondas: `onda_corda` (progressiva e estacionária) e `ondas_duas_fontes` (interferência na superfície); Colisões: `colisao_1d` (elástica a inelástica, marca do centro de massa; **movimento de ciclo único, sem loop**, ver README do arsenal). **Fila A (aprovada em 2026-10-07, exceto o ímã; loop = fase 1 repete a 0, único = não repete):** Física — `onda_eletromagnetica` (E ciano, B magenta; loop), `particula_em_campo_magnetico` (sinal esculpido; único), `espira_em_campo_magnetico` (torque; loop), `ima_espira_inducao` (N azul, S magenta; único), `barra_trilhos_fem_movimento` (loop), `biot_savart_espira` (loop), `equipotenciais` (carga pontual e dipolo), `giroscopio_precessao` (loop), `paisagem_potencial` (loop), `cone_de_luz` (único), `orbital_atomico` (1s, 2s, 2p, 3d; loop); Cálculo — `produto_vetorial`, `plano_tangente`, `elemento_volume` (loops), `superficie_quadrica`, `pontos_criticos` (estáticos), `integral_dupla_colunas` (único). Decisões visuais do usuário: sinal da carga esculpido, B magenta, vetores físicos brancos, polos N azul e S magenta. **Fila B (30 sólidos, aprovada em 2026-10-07):** Mecânica — `plano_inclinado`, `movimento_circular`, `curva_inclinada`, `colisao_2d`, `explosao`, `rampa_rolamento`, `trilho_looping`; Fluidos — `tanque_hidrostatico`, `prensa_hidraulica`, `tanque_torricelli`; Eletricidade — `cargas_pontuais`, `dipolo_eletrico`, `linhas_de_campo_3d`, `condutor_com_cavidade`; Óptica e física moderna — `espelho_esferico`, `dioptro_plano`, `filme_fino`, `interferometro_michelson`, `rede_de_difracao`, `polarizador_malus`, `relogio_de_luz`, `atomo_bohr`; Cálculo, álgebra linear e EDP — `plano_e_reta_r3`, `lagrange_restricao`, `integral_de_linha`, `divergencia_local`, `rotacional_roda_de_pas`, `transformacao_linear_3d`, `autovetores_elipsoide`, `membrana_modos` (loops de fase 0 a 1, exceto os de ciclo único `relogio_de_luz`, `atomo_bohr` e `integral_de_linha`; estáticos: `espelho_esferico`, `rede_de_difracao`, `condutor_com_cavidade`). **Para ver qualquer sólido no Blender:** dois cliques em `experimentos/blender/arsenal/abrir/<id>.bat` (índice em `abrir/LEIA-ME.md`). Cobertura por capítulo do mapa e lacunas: `experimentos/blender/arsenal/cobertura.md`.
- **Como consultar:** `AGENTS.md` ("Consulte conforme necessidade") manda ler o catálogo antes de modelar um sólido novo; a ficha do vídeo ganhou o campo opcional `solido_3d:` (`docs/formatos.md`). Só `aprovado` serve, e registrar o campo não autoriza integrar.
- **Ferramentas e custo:** Blender 5.2.2 LTS (winget, `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`), Eevee, 64 amostras, via `renderizar.py` (`blender -b -P ... -- <id>`). Custo medido em RTX 2060: **0,45 a 1,38 s por frame em 1920×1080 com alpha** (quase todos os sólidos medidos; o cilindro maciço não foi medido isoladamente), cerca de 0,5 a 1,8 MB por PNG. Medido só neste PC (o segundo PC, pessoal).
- **Ponte com o Manim: pronta, em sandbox, ainda não usada em vídeo.** `experimentos/blender/arsenal/ponte.py` (cache de sequências PNG com alpha em `renders/arsenal3d/`, ignorado pelo Git; também CLI) e `manim_solido3d.py` (classe `Solido3D` que devolve um `ImageMobject` transparente, com loop de cargas em movimento; a fase vem de `cena.time`). Testada por `exemplo_manim.py` em horizontal (960×540) e vertical (540×960), com Manim atrás e na frente do 3D, FadeIn/FadeOut e pausa; sem compressão, o loop fecha com diferença 0,0 e a pausa congela. **Não alterou `template/` nem vídeos:** usar um sólido num vídeo continua exigindo handoff explícito e preparar as sequências antes do render final. Frames de 1080p são pesados (um loop de 60 quadros pesa de ~36 a ~100 MB por sólido) e ficam fora do Git.
- **Não verificado:** uso em vídeo real; funcionamento do Blender no outro PC (`C:\Users\KaioOrtiz\...`). Por decisão do usuário (2026-10-07), o arsenal segue a gramática de cor da Lei de Gauss também em Mecânica e Cálculo, sem reconciliar com vídeos antigos.
- **Git:** o arsenal foi commitado na `main` em etapas (`5c1a3ab`, `6976019`, `cfe07cc`, `abe607c`, `c99e512`; sem push). `experimentos/blender/out/` e os `.blend` são ignorados. Mecânica e Cálculo vieram depois: conferir com `git status`.
- **Para testar nos próximos vídeos (curto e longo):** o arsenal está pronto para uso. Em cada vídeo novo, avalie no planejamento se algum sólido aprovado encaixa (campo `solido_3d:` da ficha, ver `docs/formatos.md`) e registre o que funcionou ou não, para decidirmos o encaixe com base em uso real. Integrar continua exigindo handoff explícito.
- **O que ainda falta:** não restam lacunas 3D no mapa; ficam os assuntos melhor tratados no Manim, em `experimentos/blender/arsenal/cobertura.md`.

## Identidade: aprovado × implementado

**Aprovado:** marca e @ acima; símbolo de planos geométricos translúcidos deslocados com orbe central; linguagem científica, futurista, cósmica, elegante e limpa. Influência psicodélica leve, sem estética infantil, escolar genérica ou gamer.

**Paleta operacional inicial:** fundo `#050816`, ciano `#35D9FF`, azul `#267BFF`, violeta `#745CFF`, magenta `#EA63FF`, branco `#F5F7FF`. Extração/refinamento pelos assets ainda pendente.

**Tipografia oficial implementada:** Space Grotesk (display) e Inter (texto), com MathTex para matemática; fontes e licenças em `assets/fonts/`, carregamento em `template/fonts.py`, teste 1080×1920 aprovado tecnicamente. Vigente para os próximos vídeos, salvo decisão editorial posterior; vídeos 1–3 não mudam. O `vid_0004` foi exceção de transição: `Text` padrão do Manim nos textos de apoio/CTA e Century Gothic na capa, por escolha do usuário. Desde o `vid_0005`, todo texto na tela das animações fora da matemática usa Space Grotesk Medium (`screen_text` em `template/fonts.py`).

**Assets aprovados e versionados:** os oito PNGs estão presentes na organização prevista abaixo, são rastreados pelo Git e já integram o histórico do repositório. Funções em `docs/identidade_visual.md`; propriedades finais de aplicação ainda dependem do contexto de uso.

```text
assets/branding/
├── master/
│   ├── parallax_lab_logo_master.png
│   ├── parallax_lab_icon_profile.png
│   ├── parallax_lab_icon_transparent.png
│   └── parallax_lab_logo_monochrome.png
├── social/
│   ├── parallax_lab_banner_16x9.png
│   └── parallax_lab_cover_template_9x16.png
└── overlays/
    ├── parallax_lab_watermark.png
    └── parallax_lab_logo_horizontal.png
```

**Implementado e aprovado:** template vertical 9×16, helpers `make_title`/`make_equation`, assets oficiais, paleta, watermark e composição do piloto. Prioridade: legibilidade → compreensão → matemática/física → identidade; logo discreto e faixa inferior livre.

## Unidades de produção concluídas tecnicamente

**vid_0001 / integral_001 — integração por partes**, em `videos/vid_0001_integracao_por_partes/cena.py`, classe `Integral001`.

\[
\int x^2e^x\,dx=e^x(x^2-2x+2)+C.
\]

Cena implementada com duas aplicações explícitas, motivação da escolha de u, distribuição do −2, expansão/fatoração e verificação pela derivada, recuperando x²eˣ. Smoke test preservado como `TemplateSmokeTest`.

- Manim, narração, identidade visual, composição, sincronização e legendas do `vid_0001` estão aprovados. Os sete blocos originais permanecem intactos; `narracao_final.mp3` preserva silêncio limpo de **0,700 s** entre os blocos 3 e 4.
- `legenda.srt` contém 29 cues aprovados, com até duas linhas e notação matemática escrita em Unicode.
- Finais locais em **1080×1920, 30 fps**, duração de **69,500 s**: `renders/vid_0001_integracao_por_partes_final_master_limpo.mp4` e `renders/vid_0001_integracao_por_partes_final_legendado.mp4`.
- QA técnico concluído: H.264 vertical, 2.085 frames, áudio AAC mono a 44,1 kHz completo, legendas presentes, watermark presente, safe area preservada e sem clipping ou sobreposição nos frames inspecionados.
- O QA e a verificação matemática estão consolidados em `videos/vid_0001_integracao_por_partes/revisao.md`; cena, narração, SRT, ficha, roteiro retrospectivo, capa e publicação pendente estão na unidade.
- A conferência visual por frames em 3, 8, 18, 25, 28, 32, 38, 45, 51, 58, 63 e 68 s confirmou equivalência de proporções e posicionamento com o preview aprovado. Reprodução física final em aparelho/plataforma permanece pendente.
- Publicação **não comprovada**; sem link ou data no repositório. Backup externo dos MP4s e reprodução física final em celular não foram verificados.

## Comandos e pipeline preservados

```powershell
# Preview já executado com sucesso
uv run python -m manim -p -r 540,960 --fps 15 videos/vid_0001_integracao_por_partes/cena.py Integral001

# Render final operacional
uv run python -m manim -p -r 1080,1920 --fps 30 videos/vid_0001_integracao_por_partes/cena.py Integral001
```

Resolução explicitamente vertical; `config.frame_width = 9` e `config.frame_height = 16`. O render Manim é silencioso: `videos/montar_master.py` e `videos/montar_legendado.py` documentam a montagem posterior com PyAV/Pillow. O executável `ffmpeg` não é necessário para esse fluxo.

Na execução final de 2026-09-22, `uv run` falhou no ambiente restrito do Codex; o master foi produzido com outro runtime Python 3.12 e os pacotes da `.venv`. O diagnóstico posterior confirmou que o Python base, a `.venv`, o cache do `uv`, Manim e os imports do template funcionam quando há acesso aos caminhos externos do usuário. A falha observada era de permissão do ambiente de execução, não de corrupção da `.venv`. O fluxo operacional continua `uv run python -m manim ...`; se o erro ocorrer somente no Codex restrito, verificar acesso antes de alterar Python, dependências ou cache.

## vid_0002 — integral por substituição

Implementado em `videos/vid_0002_integral_substituicao/cena.py`, classe
`Integral002`: ∫ 2x cos(x²) dx = sin(x²) + C, com substituição explícita,
regra da cadeia no caso concreto, verificação aplicada, síntese derivada/integral
e coda sincronizada F/F′ removível. `Integral002SemCoda` encerra após a síntese.

Os finais locais são `renders/vid_0002_integral_substituicao_final_master_limpo.mp4`
e `renders/vid_0002_integral_substituicao_final_legendado.mp4`: **1080×1920,
30 fps, 2.083 frames e ~69,433 s**. O SRT final tem 25 entradas; áudio AAC de
**69,224 s**. A fonte original `audio/narracao_final.wav` (**71,024 s**) fica
intacta; `preparar_audio.py` reproduz byte a byte a versão final de montagem
`audio/narracao_montagem.wav`, com corte de 1,8 s de silêncio inicial e ajuste
de +1,2 dB somente entre 26,12–29,44 s. A matemática, CTA, coda e QA final
estão em `videos/vid_0002_integral_substituicao/revisao.md`; a publicação
permanece sem evidência. Capa e demais fontes estão na pasta da unidade.

Os dois vídeos são tecnicamente finalizados, mas a revisão física em celular,
o backup externo dos MP4s e a publicação não estão confirmados. Os MP4s ficam
em `renders/`, ignorado pelo Git; cenas, áudio, SRT, capas e documentação
ficam nas pastas versionadas. O template Manim não foi expandido nesta
consolidação. Aprendizados comparados em `docs/padroes_producao.md`.

Na limpeza local, previews/logs de `renders/` e duas cópias WAV intermediárias
foram removidos após auditoria. Uma auditoria restrita posterior classificou
individualmente os 920 arquivos de `media/` e removeu 859 caches, previews
substituídos e imagens/vídeos temporários de QA. Uma checagem adicional dos
26 arquivos históricos (`.py`, `.mp3`, `.srt`) confirmou que não são necessários
para reconstrução, e eles também foram removidos. No total, saíram 885 arquivos
(55.429.804 bytes). Permanecem 35 incertos: relatórios de QA (`.json`, `.log`)
e dois visuais silenciosos de 1080×1920 usados na montagem.
O inventário com caminho, tamanho, classe e ação está em
`renders/auditoria_media_restrita_2026-09-23.csv`; nenhuma fonte necessária
à versão final nem MP4 final foi removido nessa auditoria.

## Estratégia e próxima ação

Primeiro ciclo aprovado: **10 vídeos — 6 exercícios, 2 teorias curtas, 2 aplicações**, em **Cálculo + aplicações físicas**. Não é um curso linear. Medir formato, retenção, clareza, interesse, tempo de produção e gargalos; ampliar automação somente após o ciclo e a identificação de um gargalo real.

### Capacidade futura planejada

**Status: PLANEJADA / NÃO IMPLEMENTADA.** O Parallax Lab possui como direção futura aprovada visualizações matemáticas dinâmicas, física animada ampliada, conteúdos de intuição e curiosidades e representações complementares ou sincronizadas de um mesmo fenômeno. Essa expansão não está implementada, não constitui pendência atual e não altera `vid_0001`, os dez primeiros vídeos ou a próxima ação operacional do MVP.

**vid_0003 — tecnicamente concluído (2026-09-25):** teoria curta — “De onde
vem a fórmula da integração por partes?”, em
`videos/vid_0003_origem_integracao_por_partes/`, classe `Integral003`.
Finais locais em **1080×1920, 30 fps, 2.709 frames, 90,3 s** de vídeo
(áudio AAC de 90,517 s):

- `renders/vid_0003_origem_integracao_por_partes_final_master_limpo.mp4`
- `renders/vid_0003_origem_integracao_por_partes_final_legendado.mp4`

Áudio: `audio/narracao_final.wav`, fonte aprovada sem processamento. SRT:
`legenda.srt`, 27 cues com notação matemática escrita; legendas coloridas
por `SUBTITLE_TERM_COLORS` da cena via `videos/montar_legendado.py --style
solid --color-module`. Coda geométrica de 56,5 a 84,7 s; CTA “Segue o
Parallax Lab / @labparallax” no fechamento. QA técnico concluído; detalhes em
`revisao.md` da unidade. Capa `capa_instagram.png` pronta, série pública
“POR TRÁS DA FÓRMULA · EP. 01”. QA físico em celular, backup externo e
publicação não comprovados.

**vid_0004 — tecnicamente concluído (2026-09-26):** Aplicação — derivada
como velocidade instantânea (`DA EQUAÇÃO AO FENÔMENO · EP. 01`), em
`videos/vid_0004_velocidade_instantanea/`, classe `VelocidadeInstantanea004`.
Finais locais em **1080×1920, 30 fps, 3.045 frames, 101,5 s** (áudio AAC de
99,93 s): `renders/vid_0004_velocidade_instantanea_final_master_limpo.mp4` e
`renders/vid_0004_velocidade_instantanea_final_legendado.mp4`. Áudio
`audio/narracao_montagem.wav` (derivada da voz final `narracao_final.wav`,
intacta, por `preparar_audio.py`); SRT `legenda.srt` com 33 cues coloridos;
capa `capa_instagram.png` (regenerável por `gerar_capa.py`). QA técnico,
visual e matemático concluído em `revisao.md` da unidade. **Publicado
manualmente pelo usuário em 2026-09-26** (Instagram, YouTube Shorts, TikTok,
Facebook); URLs ainda não registradas no repositório. Backup externo dos MP4s
não confirmado.

**vid_0005 — concluído (2026-09-27):** `POR TRÁS DA FÓRMULA · EP. 02`,
origem geométrica da aceleração centrípeta (a_c = v²/R), em
`videos/vid_0005_aceleracao_centripeta/`, classe `AceleracaoCentripeta005`.
Finais locais em **1080×1920, 30 fps, 3.840 frames, 128,0 s** (áudio AAC
estéreo de 127,2 s): `renders/vid_0005_aceleracao_centripeta_final_master_limpo.mp4`
e `renders/vid_0005_aceleracao_centripeta_final_legendado.mp4`. Narração
ElevenLabs `audio/narracao_final.wav`, intacta; SRT `legenda.srt` com 41 cues
coloridos; capa `capa_instagram5.png` (regenerável por `gerar_capa.py`). QA em
`revisao.md` da unidade. **Publicado manualmente pelo usuário em 2026-09-27**;
URLs ainda não registradas.

**vid_0006 — concluído (2026-09-28):** `DA EQUAÇÃO AO FENÔMENO · EP. 02`,
interferência de ondas aplicada ao cancelamento ativo de ruído em fones, em
`videos/vid_0006_cancelamento_ruido/`, classe `CancelamentoRuido006`. Finais
locais em **1080×1920, 30 fps, 3.166 frames, 105,53 s** (áudio AAC estéreo de
104,64 s): `renders/vid_0006_cancelamento_ruido_final_master_limpo.mp4` e
`renders/vid_0006_cancelamento_ruido_final_legendado.mp4`. Narração ElevenLabs
`audio/narracao_final.wav`, intacta; SRT `legenda.srt` com 43 cues coloridos;
capa `capa_instagram.png` (regenerável por `gerar_capa.py`). QA em
`revisao.md` da unidade. **Publicado manualmente pelo usuário em 2026-09-28**;
URLs ainda não registradas.

**vid_0007 — concluído (2026-09-28):** `EXERCÍCIO RESOLVIDO · EP. 03`, campo
elétrico no eixo de um anel carregado e posição do máximo (z = R/√2 ≈ 0,71R), em
`videos/vid_0007_campo_anel_carregado/`, classe `CampoAnel007`. Finais locais em
**1080×1920, 30 fps, 4.449 frames, 148,3 s** (áudio AAC estéreo de 148,0 s):
`renders/vid_0007_campo_anel_carregado_final_master_limpo.mp4` e
`renders/vid_0007_campo_anel_carregado_final_legendado.mp4`. Narração ElevenLabs
`audio/narracao_final.wav`, intacta; SRT `legenda.srt` com 54 cues coloridos;
capa `capa_instagram.png` (“ONDE O CAMPO ELÉTRICO É MAIS FORTE?”, regenerável por
`gerar_capa.py`). QA em `revisao.md` da unidade. **Publicado manualmente pelo usuário em
2026-09-28**; URLs ainda não registradas.

**vid_0008 — concluído tecnicamente (2026-09-30):** `POR TRÁS DA FÓRMULA · EP. 03`,
campo magnético no eixo de uma espira (B_z(z) = μ₀IR²/2(R²+z²)^{3/2}; checagens z = 0 e
z ≫ R), em `videos/vid_0008_campo_espira/`, classe `CampoEspira008`. Nasceu do preview
combinado espira + solenoide, dividido em dois vídeos (decisão de 2026-09-30). Finais locais em
**1080×1920, 30 fps, 4.581 frames, 152,7 s** (áudio AAC estéreo de 152,3 s):
`renders/vid_0008_campo_espira_final_master_limpo.mp4` e
`renders/vid_0008_campo_espira_final_legendado.mp4`. Narração ElevenLabs
`audio/narracao_final.wav`, intacta; a cena segue a voz por 45 âncoras (`sync.json`,
`native.json`); SRT `legenda.srt` com 64 cues coloridos; **6 propostas de capa** em `capas/`
(A–F, regeneráveis por `gerar_capa.py`), **escolha pendente**. QA em `revisao.md` da unidade.
**Não publicado.**

**vid_0009 — concluído tecnicamente (2026-09-30):** `DA EQUAÇÃO AO FENÔMENO · EP. 03`, campo
magnético de um solenoide (superposição → Σ→∫ → gráfico B(z) → L/R → limite ideal → simetria → lei de
Ampère → B = μ₀nI → bobina real → atuador), em `videos/vid_0009_campo_solenoide/`, classe
`CampoSolenoide009`. Finais locais em **1080×1920, 30 fps, 5.244 quadros, 174,78 s** (áudio AAC
estéreo de 174,4 s): `renders/vid_0009_campo_solenoide_final_master_limpo.mp4` e
`renders/vid_0009_campo_solenoide_final_legendado.mp4`. Narração ElevenLabs `audio/narracao_final.wav`,
intacta; a cena segue a voz por 53 âncoras (`sync.json`, `native.json`; instantes obtidos por contagem de
sílabas e pausas, sem ASR, margem ~±0,6 s); SRT `legenda.srt` com 83 cues coloridos. Corrente em verde
(sem laranja/amarelo). Para caber na voz, esperas nativas de B2, B3, B8 e B9 foram encurtadas (sem
remover passos físicos). Capa oficial `capa_instagram.png` (“E SE FOREM / MUITAS ESPIRAS?”, `gerar_capa.py`). **Não publicado.** Ficha em `ficha.md` da unidade
(inclui o texto da narração). `prototipo_combinado.py` guarda o preview combinado original.

**vid_0010 — em produção (verificado em 2026-10-01):** `EXERCÍCIO RESOLVIDO · EP. 04`, esfera maciça
no looping (altura mínima 2,5R → 2,7R; I_CM = 2/5 ma²; K = 7/10 mv²), em
`videos/vid_0010_looping_esfera/cena.py`, classe `LoopingEsfera010` (pauta decidida em 2026-10-01;
substitui a antiga “derivada ou integral aplicada a um problema curto de movimento”, que não foi realocada). No filesystem existe **apenas
`cena.py`**, versionado como checkpoint de produção (commit `feat: iniciar vid_0010 looping com MF-Tools`); não há `ficha.md`, áudio, SRT, capa nem render final. Segundo o docstring da cena
é um preview silencioso (3ª versão). Preview 540×960/15 fps renderizado em 2026-10-01 (~154 s). Três transformações
algébricas usam `TransformByGlyphMap` (Pitágoras a²=x²+r² → r²=a²−x²; cancelamento de π e a³ em
I = … → I_CM = 2/5 ma²; K = ½mv² + ½(⅖ma²)(v/a)² → K = ½mv² + ⅕mv²); as demais seguem `TransformMatchingTex`/fade.
O preview é estado de produção, não final. QA completo, voz, SRT, capa, final e publicação **não** foram feitos.

**vid_0011 — concluído tecnicamente (2026-10-02):** `POR TRÁS DA FÓRMULA · EP. 04`, origem de
PV^γ = constante, em `videos/vid_0011_adiabatica_pv_gama/`, classe `AdiabaticaPVGama011`. Finais locais em
**1080×1920, 30 fps, 4.751 quadros, ~158,35 s** (AAC estéreo): `renders/vid_0011_adiabatica_pv_gama_final_master_limpo.mp4`
e `..._final_legendado.mp4`. Narração ElevenLabs `audio/narracao_final.wav`, intacta; 34 âncoras (`sync.json`,
`native.json`); SRT `legenda.srt` com 63 cues coloridos. Seis propostas de capa versionadas em `capas/`
(`gerar_capa.py`), escolha pendente. Segundo a `ficha.md`, aprovação humana do vídeo final e publicação pendentes.
**Não publicado.**

**vid_0012 — vídeo final aprovado (2026-10-02); termo trocado em 2026-10-03:** `EXERCÍCIO RESOLVIDO · EP. 05`, campo de uma
esfera isolante com ρ(r) = ρ0(1 − r/R) e máximo em r = 2R/3, em `videos/vid_0012_campo_esfera_nao_uniforme/`, classe
`CampoEsfera012`. Em 2026-10-03 o termo “carga encerrada, Q_enc” passou a **“carga envolvida, Q_env”** (voz regravada, sincronia,
legenda, final e capa 6 refeitos; os finais anteriores ficam em `renders/` com sufixo `_qenc`). Finais locais atuais em
**1080×1920, 30 fps, 4.978 quadros, ~165,92 s** (AAC estéreo de 165,04 s):
`renders/vid_0012_campo_esfera_nao_uniforme_final_master_limpo.mp4` e `..._final_legendado.mp4`. Narração ElevenLabs
`audio/narracao_final.wav` (take Q_env), intacta; 58 âncoras de fala (`sync.json`; `PAUSAS_FIXAS` em `gerar_sync.py` corrige duas
pausas que o alinhador errava); SRT `legenda.srt` com 65 cues. Capas: seis propostas versionadas em `capas/` (`gerar_capa.py`; a 6,
“LEI DE GAUSS COM / DENSIDADE DE CARGA VARIÁVEL”, já com Q_env) e alternativas em `capas_codex/` e `capas_teste/`. **Segundo a
`ficha.md`, escolha da capa e publicação seguem pendentes; publicação não comprovada no repositório.** O take anterior da voz
(`audio/narracao_final_qenc_antiga.wav`, ~29 MB) não foi versionado.

**vid_0013 — publicado, segundo o usuário (2026-10-06):** `DA EQUAÇÃO AO FENÔMENO · EP. 04`, potencial de poço duplo
(partícula presa ou atravessando a barreira, a partir de F(x) e U(x)), em `videos/vid_0013_potencial_poco_duplo/`, classe
`PotencialPocoDuplo013`. Versionado em 2026-10-06 a partir do trabalho do outro computador: cena final `cena.py` (mais as
iterações `cena_v2`–`cena_v9`), narração `audio/narracao_final.wav` (159,68 s de fonte) com `montagem.json` (inserções de
silêncio, 17,25 s no total), `sync.json`/`native.json`, `legenda.srt`, `texto_narracao.txt`, `gerar_sync.py`, capas
(`capas/`, `gerar_capa.py`, `gerar_capas_variacoes.py`) e pranchas de QA (`frames_preview*`). Não há `ficha.md` nem `revisao.md`
na pasta; a publicação vem do relato do usuário, sem URL nem data registradas. O WAV intermediário `audio/narracao_montagem.wav`
(~30 MB, derivado da voz final conforme `montagem.json`) não foi versionado.

**vid_0014 — em finalização, segundo o usuário (2026-10-06):** `POR TRÁS DA FÓRMULA · EP. 05`, “Por que o eixo muda o momento
de inércia?” (teorema dos eixos paralelos, barra fina, caso final d = L/2), em
`videos/vid_0014_momento_inercia_eixos_paralelos/`, classe `MomentoInercia014`. Versionados `cena.py`, `ficha.md`, `roteiro.md` e
as pranchas de QA em `frames_preview/` (v1–v5). Pela `ficha.md`, o estado documentado é **preview Manim V5 silencioso**
(sem voz, SRT, capa, final ou publicação); o relato de “finalização” ainda não está refletido na ficha.

**vid_0015 — iniciando, segundo o usuário (2026-10-06):** ainda sem pasta, arquivo nem commit neste repositório. Não registrar
como iniciado em disco sem evidência.

**Próxima ação:** escolher a capa do `vid_0008` (propostas A–F) e publicá-lo; publicar o
`vid_0009` (capa pronta); continuar o `vid_0010` (preview em produção). **Pendências editoriais:** as antigas pautas 8
(“o que uma integral realmente acumula”) e 9 (“de v(t) ao deslocamento”) ficaram sem
posição depois da decisão de 2026-09-30 (8 = espira, 9 = solenoide); a família editorial dos
novos 8 e 9 não foi decidida; a pauta 6
original (“limite simples com interpretação visual”) ficou sem posição depois
que o `vid_0006` passou a ser a aplicação de interferência/ANC, e a pauta 7
original (“outra integração por partes, com estrutura diferente”) ficou sem
posição depois que o `vid_0007` passou a ser o campo do anel (decisões de
2026-09-28); “como escolher u” continua aprovada como pauta, mas sem posição; a
contagem por família precisa ser reconciliada pela Produção. O vídeo 10 passou a ser o
exercício da esfera em looping (decisão de 2026-10-01); a pauta anterior do vídeo 10 não foi realocada.
**Inconsistência editorial pendente:** “derivada pela
regra da cadeia”, antes no vídeo 4, não tem nova posição aprovada. Não foi
realocada nem excluída definitivamente. Distribuição e vídeos 1, 2 e 5–10
preservados. Antes de publicar os vídeos 1 e 2, fazer QA físico em celular
e confirmar backup externo dos MP4s. Publicação dos vídeos 1–3 não comprovada no repositório.

**Pendências seguintes:** definir regras tipográficas por contexto (tamanhos, pesos, espaçamentos) no primeiro vídeo com a tipografia oficial; QA físico em celular dos vídeos 1–3; registrar, se desejado, as URLs do `vid_0004` ao `vid_0007`; conferir regras atuais da plataforma antes de novas publicações. Publicações registradas (manuais): `vid_0004` (2026-09-26), `vid_0005` (2026-09-27), `vid_0006` e `vid_0007` (2026-09-28). Backup: o usuário informou (2026-09-28) que mantém os finais no Google Drive.
