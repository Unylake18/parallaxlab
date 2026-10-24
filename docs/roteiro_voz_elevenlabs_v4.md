# Roteiro e voz com ElevenLabs v4

Como escrever e gerar a narração dos vídeos usando o Eleven v4 (registrado em 2026-10-16, a partir do teste no vid_0023).
Vale para curtos e longos. A matemática e o storyboard continuam sendo do briefing de Produção; este documento trata só de **como a fala é escrita e gerada**.

## Configuração de geração

| Item | Valor |
|---|---|
| Voz (voice ID) | `qw7jgPZWOKrl10GsjQ82` (não é segredo) |
| Modelo | `eleven_v4` (variante `eleven_v4_turbo` é para tempo real; não usar na narração final) |
| Controles de voz | Stability e Similarity no padrão. Style e Speed não existem no v4 |
| Plano | Creator. PCM 44,1 kHz exige Pro, então o formato padrão é `mp3_44100_192`, decodificado para WAV mono 16 bits 44,1 kHz |
| Chave de API | **Só** na variável de ambiente `ELEVENLABS_API_KEY`, definida na sessão do PowerShell. Nunca em arquivo, commit, chat ou handoff. Se uma chave vazar, revogar em Developers → API Keys e criar outra |
| Script | `videos/gerar_voz_elevenlabs.py` |

Comando (a partir da raiz do repositório). Primeiro, a chave só nesta sessão:

```powershell
$env:ELEVENLABS_API_KEY = "cole-a-chave-aqui"
```

Depois, a geração:

```powershell
uv run --no-sync python videos/gerar_voz_elevenlabs.py videos/vid_NNNN_x/narracao_tags.md videos/vid_NNNN_x/audio/narracao_v4.wav --voz qw7jgPZWOKrl10GsjQ82 --secao "## Texto corrido (para gravação)"
```

- `--seco` só mostra os blocos, sem chamar a API nem gastar crédito. Use antes de gerar.
- O texto é dividido em blocos de até 4.500 caracteres, nos finais de frase. O limite por requisição na API não foi confirmado na documentação do v4; o app informa 10.000.
- `--contexto` envia `previous_text`/`next_text` entre blocos; o v4 pode não aceitar, então fica desligado. Ligar só se a fronteira entre blocos soar cortada.
- Não sobrescreva `audio/narracao_final.wav` de um vídeo já fechado: gere com outro nome (`narracao_v4.wav`) e promova depois de ouvir.

## Audio tags `[ ]`

Fonte: documentação do ElevenLabs, seção "Prompting Eleven v4" (best practices de Text to Speech).

- A tag vai entre colchetes, antes (ou depois) do trecho que ela afeta. Vale até a próxima tag.
- **Uma tag por frase.** Tags contrastantes nas mesmas palavras prejudicam a entrega.
- Prefira tags **descritivas** de entrega: `[slow, measured pace]`, `[calm, satisfied]`. Tags ambíguas podem ser lidas em voz alta.
- Tags validadas pela documentação: `[curious]`, `[excited]`, `[thoughtful]`, `[whispers]`, `[sighs]`, `[short pause]`, `[long pause]`, `[happy]`, `[sad]`, `[surprised]`, `[clears throat]`. `[playful]` vem só da lista do blog: testar.
- **Longos:** regras específicas em `docs/padrao_video_longo.md` §5 (sem `[slowly]`/`[slow, measured pace]`, nunca a letra solta).
- Para narração didática, a base é `[thoughtful]` e `[curious]`; `[excited]` só no momento da descoberta (o resultado, o ponto ótimo); `[slow, measured pace]` no conceito-chave; `[calm, satisfied]` no fechamento.
- Não usar tags de postura ou ação (`[standing]`, `[grinning]`), música nem efeitos sonoros: estragam a voz e não pertencem à narração.
- **Não existe `<break>`** no v4. Pausa com `[short pause]`/`[long pause]`, reticências (`...`) ou quebra de frase.
- Ênfase: maiúsculas em uma palavra ("o MÁXIMO do denominador") e pontuação. Com parcimônia.
- Pronúncia difícil: IPA entre barras, como `/ˈkɔsenu/`. Testar na voz escolhida; o resultado varia.
- Se uma tag soar errada ou for lida em voz alta, apague-a ou troque por uma vizinha e gere de novo. Gerar duas ou três tomadas e escolher a melhor é normal.
- As tags ficam em inglês e **não entram na legenda** nem na sincronização de texto: o `.srt` e o ASR usam o texto sem `[ ]`.

Arquivo de exemplo: `videos/vid_0023_angulo_puxar_caixa/narracao_tags_v5.md` (17 tags em ~3.000 caracteres).

## Estilo da fala: professor de cursinho pré-vestibular

Tom: amigável, didático, conversado. Explique como quem está ao lado do aluno, sem jargão desnecessário e sem pressa.

**Variáveis sempre pelo nome, nunca pela letra.** O ouvido não vê o símbolo na tela.

| Escrito na tela | Falado |
|---|---|
| F, F_x, F_y | força, parte horizontal da força, parte vertical da força |
| θ | ângulo |
| N | normal (o empurrão do chão) |
| P, m·g | peso, massa vezes aceleração da gravidade |
| μ | coeficiente de atrito |
| f_at | atrito estático máximo |
| a, v, t | aceleração, velocidade, tempo |
| E, V, ρ | campo elétrico, potencial, densidade |

- Se o símbolo é novo, apresente uma vez junto ao nome ("a força, que na tela aparece como F") e depois use só o nome.
- Operações por extenso: "vezes", "dividido por", "mais", "menos", "ao quadrado", "raiz quadrada de", "igual a". Nada de "asterisco" ou "barra".
- Números como serão falados: "vinte e seis vírgula seis graus", "noventa e oito newtons". Unidades por extenso e no plural certo. A fala usa precisão simplificada; a tela pode mostrar mais casas.
- Funções: "cosseno", "seno", "tangente", "derivada de ... em relação a ...", "integral de ... até ...".

**Conectivos que conduzem o raciocínio** (variar, não repetir o mesmo na sequência):
- abrir uma etapa: "Primeiro", "Agora", "Vamos por partes", "Olha só";
- ligar causa e consequência: "Então", "Por isso", "Ou seja", "Logo";
- retomar: "Lembrando:", "Repara que", "Como a gente viu";
- contrapor: "Mas", "Só que", "Em compensação";
- fechar: "Por fim", "Resumindo", "E chegamos a...".

**Estrutura da explicação:** pergunta que prende → ideia em palavras → conta → o que o resultado significa → conferência ou comparação → fechamento curto. Uma ideia por frase; frases curtas, na ordem em que a cena mostra.

**Ritmo:** cerca de 2,7 palavras por segundo no roteiro (a voz real do ElevenLabs fica entre 2,7 e 3,0). O vídeo se molda à voz, não o contrário. Reticências e `[short pause]` antes de um resultado importante ajudam a cena a respirar.

## Fluxo no vídeo

1. Roteiro limpo (`narracao_sugestao*.md`) segue como fonte da fala e dos tempos.
2. Cópia com tags (`narracao_tags*.md`) para gerar a voz, com a seção `## Texto corrido (para gravação)`.
3. `--seco`, depois geração; ouvir; ajustar tags e regerar só o necessário.
4. Escolhida a tomada, promover para `audio/narracao_final.wav` e seguir o fluxo normal de sincronização, legenda e master.
5. Registrar no relatório de entrega: modelo, voz, versão do texto e se houve tags.

## Pendências conhecidas

- Português do Brasil no v4 não é detalhado na documentação consultada: validar pronúncia com o QA de sempre (números por extenso, "cosseno", "newtons").
- A primeira geração real com tags (vid_0023, `narracao_tags_v5.md`) ainda precisa ser ouvida; atualizar este documento com o que funcionar ou falhar.
