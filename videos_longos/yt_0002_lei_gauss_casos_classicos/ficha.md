# yt_0002 — Lei de Gauss: três simetrias, um método

## Estado

**PACOTE DO WORK APROVADO COMO FONTE CANÔNICA DE PRODUÇÃO — SEM IMPLEMENTAÇÃO.**

Data: 2026-10-06. Identificação definitiva aprovada pelo usuário: **`yt_0002_lei_gauss_casos_classicos`**. A pauta anterior de energia potencial foi descartada editorialmente e sua pasta foi removida por autorização explícita nesta conversa. O pacote canônico está nesta unidade definitiva; não há mais colisão de ID.

O pacote fecha física, seleção, narração e storyboard para revisão por blocos. “Auditado” significa conferência analítica/documental; não significa voz cronometrada, preview aprovado ou vídeo pronto. Não iniciar `cena.py` automaticamente.

### Aprovação editorial registrada em 2026-10-06

Aprovação explícita recebida nesta conversa: `ficha.md`, `narracao.md`, `producao.md` e `storyboard.md` do Work constituem a base canônica daqui para frente. O fechamento do chat de Produção permanece referência de origem; em divergências entre os pacotes, prevalecem as decisões abaixo, confirmadas pelo usuário:

- `Q_env` / “carga envolvida”, em continuidade com o primeiro longo.
- Referência editorial de 18:42, faixa estimada de 18:40–19:20 e teto de 20 min; não comprimir para 17:30–18:00.
- B4 mantido com aproximadamente 56 s e distinção entre `σ/(2ε₀)` e `σ_face/ε₀`.
- Esfera maciça mantida com aproximadamente 66 s, como revisão/comparação.
- Payoff das potências condicionado à simetria e à carga envolvida fixa nas regiões comparadas.
- Narração e storyboard do Work preservados, com 29 beats e continuidade visual extraída do `yt_0001`.

Não pedir nova rodada de Produção por essas divergências já resolvidas. A identificação foi posteriormente resolvida pelo usuário, como registrado acima. A aprovação do pacote e a organização da unidade não abrem a implementação. Mediante handoff específico, começar somente pela abertura/recap N01–N03; seguir cilíndrico → planar → esférico → comparação/síntese e só então integração.

## Classificação

- id: `yt_0002`
- slug: `yt_0002_lei_gauss_casos_classicos`
- formato: `longo_horizontal`
- natureza: `derivacao_aplicada`
- curso: `Física III`
- eixo: `Eletricidade e Magnetismo`
- macroassunto: `eletromagnetismo`
- modulo: `lei_de_gauss`
- posição curricular: `docs/mapa_curricular.md`, §6.3 Lei de Gauss.
- papel no módulo: segunda aula, aplicações canônicas; anterior: `yt_0001_lei_gauss` (fundamentos); seguinte planejada no briefing: problemas elaborados, sem ID ou data de publicação atribuídos nesta rodada.
- destino: YouTube long-form.
- proporção/frame lógico: 16:9 / 16×9.
- preview futuro: 960×540 / 15 fps.
- final futuro: 1920×1080 / 30 fps.
- duracao_alvo: 15–18 min inicialmente; 18–19 min quando necessário; teto 20 min.
- estimativa após roteiro: **18:42** como referência a 150 palavras/min, com 93 s de pausas/leituras e arredondamento por beat; aproximadamente 18:40–19:20 para planejamento. Cronometragem real pendente.
- narração selecionada: **2551 palavras**, 28 beats com fala + 1 pausa sem fala; ganchos alternativos não contados.

## Título, pergunta e payoff

Título editorial recomendado: **As 3 simetrias que resolvem a Lei de Gauss**.

Título na intro: **LEI DE GAUSS**. Subtítulo: **Três simetrias, um método**. Oito títulos candidatos estão em `producao.md`, seção 6. Não há título final de publicação ou thumbnail produzida.

pergunta_central: **Como reconhecer a superfície gaussiana certa e resolver os casos clássicos da Lei de Gauss sem decorar uma fórmula diferente para cada geometria?**

payoff_principal: **Identifique a simetria da fonte, escolha uma superfície onde o fluxo simplifique e calcule a carga envolvida na região. Esfera, cilindro e plano são três versões do mesmo raciocínio.**

## Pré-requisitos

Fundamentos do primeiro longo: fluxo por superfície fechada, normal exterior, produto escalar, papel da simetria e distinção fluxo/campo. Conhecimento introdutório de campo elétrico, vetores, superposição e densidades de carga. Recap de 41 s; não reconstruir a aula anterior. Fatos de condutores entram como hipóteses necessárias em comentários curtos.

## Seleção congelada para revisão

- A: linha infinita; casca cilíndrica infinita; cilindro maciço uniforme; capacitor coaxial.
- B: chapa infinita não condutora; slab volumétrico uniforme; duas chapas opostas/capacitor plano; condição local da face de um condutor.
- C: casca esférica uniforme; revisão da esfera maciça uniforme; capacitor esférico.
- D: três capacitores; áreas e potências com simetria/Q_env fixo; quadro comparativo; checklist aplicado; payoff e CTA.

Sem densidades variáveis, objetos finitos, cavidades deslocadas, potencial, capacitância, Poisson/Laplace ou método das imagens. Casos aparentemente redundantes foram mantidos por função didática específica, conforme auditoria.

## Modelos e notação fechados

Eletrostática no vácuo, sem fontes externas. Fontes cilíndricas/planas idealmente infinitas; distribuições uniformes; polaridade principal positiva. Maciços/slab são isolantes com carga volumétrica, sem folha extra na fronteira. Cascas A2/C1 são camadas superficiais delgadas uniformes. Coaxial e capacitor esférico têm núcleo condutor maciço de raio a e casca externa condutora ideal delgada de raio b; cargas iguais e opostas; campo só no vão. σ_face é densidade local na face em B4.

Preservar a notação pública **`Q_{\mathrm{env}}` / carga envolvida**, vigente no yt_0001; é equivalente ao `Q_enc` / carga encerrada do briefing. Não introduzir duas versões concorrentes na aula. Em B2, gráfico de **`E_x(x)` assinado**, não módulo. Não atribuir campo único em uma camada superficial ideal; mostrar limites laterais.

Soluções de todos os casos, hipóteses, unidades, sinais, saltos, continuidade e limites em `producao.md`, §§3–5 e 16. Equações públicas P0–P14 em §13; QA reservado em §14. Três gráficos completos: cilindro maciço, slab assinado, esfera maciça, com gaussiana e marcador sincronizados.

## Arquitetura e portas de implementação futuras

| Unidade de revisão | Beats | Janela estimada | Critério principal antes de integrar |
| --- | --- | --- | --- |
| Abertura/recap | N01–N03 | 0:00–1:17 | Ciência primeiro; sistema de título existente; método legível |
| Cilíndrico | N04–N11 | 1:17–6:32 | Tampas sem fluxo; Q_env por região; mudança de material explícita |
| Planar | N12–N19 | 6:32–12:03 | Duas tampas; slab assinado; superposição; σ_face local |
| Esférico | N20–N23 | 12:03–15:27 | Mesmo aparato; casca versus maciço; núcleo condutor definido |
| Comparação/síntese | N24–N29 | 15:27–18:42 | Potências só nos domínios corretos; método como payoff; pausa antes do CTA |
| Integração | Todos | Após revisões acima | QA completo da unidade; voz futura determina sincronia real |

Não implementar um bloco sem abertura explícita dessa fase. O briefing permite revisão separada de cada bloco para evitar retrabalho tardio.

## Continuidade visual obrigatória

Seguir `yt_0001_lei_gauss` e os helpers horizontais vigentes; nenhuma alteração de template ou asset global. Especificação numérica/semântica em `producao.md`, §18. Manter header, watermark, margens, sistema de título, fontes, cores, setas, boxes, hierarquia e outro. Modos FOCUS/SPLIT/COMPARE/BUILD alternam por função, sem painéis rígidos permanentes. Comparar três miniaturas somente após leitura sequencial, sem três derivações simultâneas.

## Pacote de Produção

1. `producao.md`: dezenove itens do retorno solicitado, em ordem, com soluções, bibliografia, decisões e QA.
2. `narracao.md`: três opções de gancho e texto completo selecionado, N01–N29; sem voz gerada.
3. `storyboard.md`: tempo, fala, tela, animação, modo e objetivo; quadro final e mapa de retenção.
4. `ficha.md`: esta consolidação para o handoff de implementação posterior.

Referências verificadas: OpenStax *University Physics Volume 2* §§6.3–6.4 e MIT OCW 8.02, Class Slides `presentati_w02d2.pdf`; links e delimitação da conferência em `producao.md`, §16. Não atribuir exercícios a edições não consultadas.

## QA e pendências reais

Concluído nesta rodada: auditoria das onze configurações; derivações e conferências analíticas; distinção de densidades/modelos; decisões público/QA; contagem da narração; consistência das janelas e IDs; leitura dos trechos relevantes da referência de série.

Ainda não executado: cronometragem de voz, sincronização, legibilidade em preview, inspeção de animação/continuidade dos gráficos, render e reprodução física. Esses testes pertencem às fases posteriores, não são pendências a executar agora. Identificação administrativa resolvida; pauta anterior descartada e removida por autorização explícita.

Nenhum código, render, áudio, SRT, thumbnail, publicação, commit ou push criado/executado. A rodada termina no pacote editorial, sem começar a fase seguinte.
