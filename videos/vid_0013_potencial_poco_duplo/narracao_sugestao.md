# vid_0013 — narração e notas de gravação

DA EQUAÇÃO AO FENÔMENO · EP. 04. Base visual fechada: preview V9 (`renders/vid_0013_potencial_poco_duplo_preview_v9.mp4`, 178,0 s). Texto para o TTS em `texto_narracao.txt`: 14 parágrafos, um por bloco da tabela abaixo, **460 palavras** (contagem por espaços em UTF-8; o `wc -w` do Git Bash sem `LC_ALL=C.UTF-8` erra com acentos), **892 sílabas**.

Limite: o vídeo final não passa de 180 s. A voz precisa caber; a cena não deve ser esticada para acompanhar um áudio longo. A duração real só é confirmada com o áudio gravado.

## Estimativa de encaixe

Taxa calibrada no áudio real do vid_0012 (mesma voz): 945 sílabas em 165,04 s = 5,73 síl/s efetivas, pausas incluídas (2,88 pal/s). Contagem silábica igual à do `gerar_sync.py`. Estimativa total: **≈ 156 s** de voz contra 178 s de cena.

| Janela V9 (s) | Bloco | Pal | Síl | Voz est. (s) | Dif. (s) | Na tela |
| --- | --- | --- | --- | --- | --- | --- |
| 0,0–8,2 | Gancho | 28 | 52 | 9,1 | +0,9 | partícula, seta curva com "?", seta de força |
| 8,2–18,3 | Força e zeros | 27 | 44 | 7,7 | −2,4 | F(x), x/ℓ em evidência, x = 0 e x = ±ℓ |
| 18,3–30,5 | Valor F(ℓ/2) | 32 | 61 | 10,7 | −1,5 | F(ℓ/2) = 3F₀/8 > 0, ponto (ℓ/2, 3F₀/8) |
| 30,5–40,5 | Curva e sinais | 29 | 53 | 9,3 | −0,7 | curva, F(−x) = −F(x), sondas |
| 40,5–68,4 | Integração | 60 | 108 | 18,9 | −9,0 | F = −U′ → U = −∫F dx → primitivas → −F₀ distribuído |
| 68,4–86,5 | Referência e C | 48 | 89 | 15,5 | −2,6 | d/dx(U+C) = U′, U(±ℓ) = 0, C = F₀ℓ/4 |
| 86,5–100,7 | Forma final | 32 | 62 | 10,8 | −3,4 | F₀ℓ/4 em evidência, quadrado perfeito |
| 100,7–117,3 | Mínimos e U″ | 38 | 79 | 13,8 | −2,8 | gráfico de U, tangente, simetria, U″ |
| 117,3–139,3 | Energia | 63 | 126 | 22,0 | 0,0 | E = K + U → K = ½mv² ≥ 0 → U ≤ E, linha E |
| 139,3–144,5 | E = 0 | 12 | 25 | 4,4 | −0,8 | repouso nos mínimos |
| 144,5–152,5 | Abaixo | 19 | 39 | 6,8 | −1,2 | duas regiões, oscilação, retornos |
| 152,5–163,6 | Separatriz | 29 | 62 | 10,8 | −0,3 | aproximação lenta, x→0 quando t→∞ |
| 163,6–171,0 | Acima + conclusão | 34 | 74 | 12,9 | +5,5 | travessia e retorno externo; a conclusão começa aqui |
| 171,0–178,0 | Último quadro | 9 | 18 | 3,1 | −3,9 | três níveis, "A ENERGIA DECIDE A TRAVESSIA", @labparallax |

Leitura: "Acima + conclusão" e "Último quadro" formam um par (14,4 s de cena, ≈ 16 s de voz, +1,6 s). A maior folga é a Integração (−9 s): na sincronização, decidir entre comprimir a álgebra (≈ 0,7×) ou manter o ritmo visual com respiros na voz — sem ultrapassar 180 s no total.

## Notas de gravação

- Uma tomada única com os 14 parágrafos, mesma voz/configuração dos vídeos anteriores (prosódia contínua). Não acelerar a voz.
- Grafia no texto do TTS: ℓ → "L", x → "x" (a voz lê bem), t → "tê", U_b → "U bê", mv² → "eme vê ao quadrado", F₀ → "F zero". Testar antes: "x sobre L em evidência", "F zero L sobre quatro", "altura U bê", "um meio de eme vê ao quadrado", "o quadrado da razão entre x e L, menos um; tudo isso ao quadrado", "Siga o Parallax Lab".
- Fórmula fatorada: ler em três tempos, com micro-pausas nas vírgulas e no ponto e vírgula ("o quadrado da razão entre x e L | menos um | tudo isso ao quadrado"), acompanhando os destaques da expressão.
- Marca: "Parallax Lab" (nunca "Lab Parallax"). O handle @labparallax fica só na tela.
- Pausas curtas (≈ 0,5–0,7 s): depois da pergunta do gancho; depois de "Que potencial gera essa força?"; depois de "a constante vale F zero L sobre quatro"; depois de "tudo isso ao quadrado".
- Separatriz em ritmo calmo; não apressar "cada vez mais devagar".
- Não narrar as contas intermediárias (razões de F(ℓ/2), potências de ℓ, frações): ficam na animação.

## Orientações para a sincronização (Produção)

- V9 intacta até medir o áudio real, pausas incluídas; só então ajustar as âncoras, dentro de 180 s.
- Integração: preservar o ritmo da álgebra; não comprimir automaticamente para ≈ 0,7×. Distribuir respiros enquanto as constantes saem, as frações se simplificam e os termos se reorganizam.
- Separatriz: preservar a desaceleração. Se a fala terminar antes da animação, aceitar um breve silêncio; não acelerar o movimento.
- Travessia e conclusão medidas juntas: a conclusão começa durante a dinâmica; o último quadro recebe só "A energia decide a travessia. Siga o Parallax Lab."
- Nesta rodada, nenhum conteúdo novo.

## Âncoras previstas (por palavra, para a sincronização depois do áudio real)

"Dá para descobrir" → apoio do gancho; "A força depende" → F(x); "um dos fatores zera" → zeros; "Em x igual a L sobre dois" → F(ℓ/2); "Cada ponto do gráfico" → ponto (ℓ/2, 3F₀/8); "Trocar o sinal" → curva espelhada; "Perto de L" → sondas; "A força é menos a derivada" → F = −U′; "Substituímos a força" → substituição; "integramos termo a termo" → primitivas; "Ao distribuir" → distribuição de −F₀; "menos com menos" → (−)·(−) = +; "Somar uma constante" → d/dx(U+C); "Escolhemos potencial zero" → U(±ℓ) = 0; "Somando F zero L sobre quatro" → isolamento de C; "Com a constante no lugar" → S4; "quadrado perfeito" → G4; "São dois mínimos" → gráfico de U; "A segunda derivada" → U″; "Em uma dimensão" → E = K + U; "um meio de eme vê" → K = ½mv²; "só são permitidas" → U ≤ E e linha E; "Cada condição inicial" → mensagem de energia; "energia zero" → E = 0; "Abaixo da barreira" → 0 < E < U_b; "exatamente igual à barreira" → separatriz; "O repouso exato" → nota "repouso exato em x = 0 é outro caso"; "Acima da barreira" → E > U_b; "retorna nos extremos" → retorno externo; "A energia decide a travessia" → último quadro.

## Legenda

O SRT deve mostrar a escrita matemática, não a grafia do TTS: "L" → ℓ, "tê" → t, "U bê" → U_b, "eme vê ao quadrado" → mv², "F zero" → F₀.
