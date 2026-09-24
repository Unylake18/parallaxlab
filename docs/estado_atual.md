# Estado atual — Parallax Lab

**Atualizado em:** 2026-09-24

**Marca:** Parallax Lab · **Instagram aprovado:** @labparallax

**Guia vigente:** `docs/guia_mestre.md`, versão 1.4, com atualização editorial de 2026-09-23.

**Fonte operacional:** este arquivo; identidade detalhada em `docs/identidade_visual.md`.

## Ambiente e repositório verificados

- Windows + PyCharm; Python 3.12.4, `uv` 0.12.17, `.venv` e Manim Community 0.21.0 validados com `uv run python -m manim --version`; MiKTeX/MathTex já usados em renders.
- Projeto local: `C:\Users\KaioOrtiz\PycharmProjects\manim-fisica`; branch `main`.
- Remoto `origin` configurado: `https://github.com/Unylake18/parallaxlab.git`.
- A consolidação técnica dos dois primeiros vídeos e a limpeza restrita de
  `media/` foram concluídas e enviadas ao `origin/main`. A `main` local e
  `origin/main` estavam sincronizadas naquele fechamento. A implementação do
  vídeo 3 e sua documentação são commits locais posteriores; sem push nesta etapa.
- A unidade de fechamento do `vid_0001` reúne a configuração visual, a cena, a narração final e a legenda no mesmo commit de produção.
- Preservar o ambiente: não reinstalar, recriar `.venv`, executar `uv init` ou alterar dependências sem diagnóstico concreto. `pyproject.toml` e `uv.lock` não possuem alterações locais.
- MVP: trabalhar em `main`, com commits pequenos; branch/PR para alterações maiores ou arriscadas.

## Identidade: aprovado × implementado

**Aprovado:** marca e @ acima; símbolo de planos geométricos translúcidos deslocados com orbe central; linguagem científica, futurista, cósmica, elegante e limpa. Influência psicodélica leve, sem estética infantil, escolar genérica ou gamer.

**Paleta operacional inicial:** fundo `#050816`, ciano `#35D9FF`, azul `#267BFF`, violeta `#745CFF`, magenta `#EA63FF`, branco `#F5F7FF`. Extração/refinamento pelos assets ainda pendente. Tipografia exata ainda não escolhida/licenciada.

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

**Produção atual:** `vid_0003`, teoria curta — “De onde vem a fórmula da
integração por partes?”. Cena e storyboard implementados em
`videos/vid_0003_origem_integracao_por_partes/`, classe `Integral003`.
Preview vertical silencioso com coda e alternativa `Integral003SemCoda`
renderizados em 540×960/15 fps. Derivação principal de 55,933 s,
coda geométrica de 8,933 s, total de 64,866 s. Arquivos locais:

- `renders/vid_0003_origem_integracao_por_partes_preview_com_coda.mp4`
- `renders/vid_0003_origem_integracao_por_partes_preview_sem_coda.mp4`

Derivação: regra do produto → dx nos três termos → d(uv), v du e u dv
termo a termo → travessia de +v du e mudança para −v du → integração e
resultado em caixa. Verificação: u'v + uv' − vu' → uv', com cancelamento
visível. A coda mostra apenas a interpretação no retângulo e arco crescente
desenhados, com escopo explícito; não é prova geral. Retirá-la mantém o
fechamento principal. QA e medições em `revisao.md` da unidade; frames e
metadados em `renders/vid_0003_qa/`. Preview sujeito à revisão do usuário;
sem voz, SRT sincronizado, capa, render final ou publicação nesta etapa.

O comando `uv run python -m manim -r 540,960 --fps 15
videos/vid_0003_origem_integracao_por_partes/cena.py Integral003` funcionou
com acesso autorizado ao cache externo do uv e ao ambiente existente.
A primeira tentativa restrita retornou erro 183 no cache; a execução com
acesso adequado confirmou Manim 0.21.0. Nenhum pacote, Python, `.venv`,
template ou dependência foi alterado. `-p` foi omitido para não abrir um
player externo automaticamente; o arquivo é o mesmo preview vertical.

**Próxima ação:** revisar o preview do vídeo 3 e decidir sobre a coda antes
de voz/sincronização e final. `vid_0004` deve trabalhar explicitamente a
escolha de u em integração por partes; sua família de exercício permanece,
com enunciado a definir. **Inconsistência editorial pendente:** “derivada pela
regra da cadeia”, antes no vídeo 4, não tem nova posição aprovada. Não foi
realocada nem excluída definitivamente. Distribuição e vídeos 1, 2 e 5–10
preservados. Antes de publicar os vídeos 1 e 2, fazer QA físico em celular
e confirmar backup externo dos MP4s. Sem publicação ou push nesta etapa.

**Pendências seguintes:** definir a tipografia oficial; confirmar backup dos MP4s e QA físico em celular; preparar publicação e conferir regras atuais da plataforma. Nenhuma publicação confirmada no repositório.
