# yt_0018 v5 — tabela do §3 do handoff (cada linha: corrigido, ou não corrigido e por quê)

Preview: `renders/preview_yt0018_v5_960x540.mp4` (15:44, 960×540, 15 fps). QA: `renders/qa.txt` (portão G28 v5 ABERTO; 62 gatilhos, 0 fora de ±0,3 s).
"Medido" = número calculado no QA ou nos quadros. "Auditoria" = categoria do `qa.py` zerada. "Visual" = só conferido na prancha, sem número.

## 3.1 Hook
| Linha | Estado | Como / por quê |
|---|---|---|
| 0:00–0:09 enquadramento | **corrigido** | Dolly-in PERTO (K 22→26→29) em `sec_hook.py`. Medido: a folha ocupa 442 px = **46%** da largura no quadro de 9,0 s (meta ≥ 35%). |
| 0:24–0:33 pergunta × gafanhoto | **corrigido** | Pergunta reposicionada fora do arco do voo. Auditoria 3D × TEXTO zerada no PH. |

## 3.2 Abertura
| Linha | Estado | Como / por quê |
|---|---|---|
| 0:45 quadro vazio | **corrigido (visual)** | A2→A3 viraram um único crossfade (faixa, 3D, caixa e par juntos). O QA isenta A1–A4 do VAZIO, então a conferência é visual (a prancha humana tem o quadro 0:44,8). |

## 3.3 X0
| Linha | Estado | Como / por quê |
|---|---|---|
| 1:45 e 1:48 tokens soltos | **corrigido** | G29: "X =", barra, "+" e "−" entram primeiro; −¼ e 0,25 voam depois. Auditoria ESQUELETO zerada. |
| 2:09 DICA | **corrigido (visual)** | O furo volta a +0,25 m enquanto "X = −1/12 m ≈ −8,3 cm" substitui "X = 0"; selo "O ⊕ FOGE DO FURO" e seta GEO do furo ao ⊕. Conferir no quadro 129 s da prancha de 12 tempos. |

## 3.4 X1
| Linha | Estado | Como / por quê |
|---|---|---|
| 2:39–2:42 SIMETRIA some | **corrigido** | Era um defeito do `wait()`: o pulso removia as peças da linha. Agora remove só o envelope. "SIMETRIA ⇒ X = Y" fica como linha-mãe. |
| 2:51 dois A□ | **corrigido** | G31: a origem fica a 35% enquanto a cópia voa. Auditoria DUPLICATA zerada. |
| 2:54 tokens da fração | **corrigido** | G29, ESQUELETO zerada. |
| 3:00–3:10 cota d | **corrigido** | Cota GEO ao longo da diagonal, rótulo "d ≈ 2,76 cm" fora da placa, com diagonal tracejada até ele. |
| 3:12–3:17 CONFERE | **corrigido** | Linha "r → 0 ⇒ A_furo → 0 ⇒ X → 0" com o X vivo numa vaga reservada da Pilha. VAZIO zerada. |
| 3:21–3:30 DICA estática | **corrigido (parcial na medida)** | Diagonal pisca, metade de cima se espelha duas vezes, ⊕ desliza, cartão "1 CONTA EM VEZ DE 2". PAUSAS: 0 trechos ≥ 4 s. **Não medi "algo muda a cada ≤ 1,5 s"** quadro a quadro. |
| (extra) selo PEDE do X1 | corrigido | O selo agora entra logo depois do chip: a CONTA não fica vazia no começo do X1. |

## 3.5 X2
| Linha | Estado | Como / por quê |
|---|---|---|
| 3:33–3:39 ocioso | **corrigido** | O caminho tracejado cresce aresta por aresta com a fala e o cubo gira. O cartão "FIO UNIFORME DOBRADO EM 3 ARESTAS DE 1 m" já está na CONTA no primeiro quadro (o QA de pixel exigia isso: o cubo é só linha fina). |
| 4:09/4:15/4:21 médias X, Y, Z | **corrigido** | G29, ESQUELETO zerada. |
| 4:15–4:21 ticks × esferas e origem | **corrigido** | Rótulos fora das esferas, "0" da origem uma vez só. ENCOSTADO zerada. |
| 4:24 "55/66" | **corrigido (auditoria)** | DUPLICATA zerada. **Não reconferi a fração intermediária glifo a glifo** — conferir no quadro 264 s da prancha de 12 tempos. |
| 4:30–4:45 inset × eixo z | **corrigido em parte — LIMITAÇÃO** | Usei a alternativa "zoom de verdade" (selo "ZOOM ×5", ligado por duas linhas à região ampliada). PALCO 3D e 3D × TEXTO estão zeradas e os rótulos x/y/z saem antes de ele entrar. **Mas a moldura ainda cobre uma parte das arestas do cubo** (canto inferior direito): na busca de posição, o melhor ponto tinha 45 de ~720 pontos de aresta amostrados sob o painel (~6%). O cubo ocupa quase todo o ESQUEMA; não há canto livre sem reduzir o cubo (K) nesse trecho, o que mexe no render 3D. Decisão pendente. |
| 5:03–5:09 rótulo d ≈ 24 cm | **corrigido** | Posição escolhida por busca, com chamada GEO fora do fio. CHAMADA CRUZA CORPO zerada. |

## 3.6 X3
| Linha | Estado | Como / por quê |
|---|---|---|
| 5:12–5:15 dois chips | **não alterado** | Não mexi no `chip()` nem estendi a auditoria SELO DUPLO a chips. SELO DUPLO segue zerada para selos. Conferir na prancha. |
| 5:39+ rótulo "M g⃗" some | **corrigido (visual)** | O rótulo fica enquanto a seta existir (abaixo da ponta da seta). A auditoria "RÓTULO SOLTO inverso" (seta sem rótulo) **não foi automatizada**; conferência só visual. |
| 6:03–6:15 rótulos empilhados | **corrigido (visual)** | Embaixo da folha só M; m junto do gafanhoto; v⃗ na ponta da seta; hipóteses viraram lista na CONTA. |
| 6:18–6:24 g⃗ × v sen θ | **corrigido** | Seta g⃗ afastada para a borda direita. ENCOSTADO zerada. |
| 6:24 ESCALA ÷3 | **corrigido** | O selo acende junto com o dolly (mesmo play). |
| 6:30–6:36 LONGE vazio | **corrigido** | Trajetória tracejada e réguas em LONGE; a parábola sai com o selo da vista. VAZIO zerada. |
| 7:09–7:28 principal (G30) | **corrigido, com uma interpretação** | A conta de Δx usa o salto **rasante** (θ = 4,23°, Δx_g = 24 cm, Δx_f = 6 cm) em PERTO, de modo que o voo cabe no ESQUEMA; o quase vertical é mostrado em LONGE (ESCALA ÷3). "m = 1 g" saiu da CALHA (ficou junto do gafanhoto). As duas setas GEO voltaram, separadas, saindo da posição inicial. 3D × TEXTO e CALHA zeradas. A leitura "rasante" para a conta de 7:09 é minha; se o briefing queria o quase vertical, é uma troca de ângulo. |
| 7:33 tokens soltos | **corrigido** | ESQUELETO zerada. |
| 8:36 setas 6/24 e precisão | **corrigido** | Duas setas na seção toda; rótulos "6 cm" e "24 cm" no mesmo formato. |
| 9:17–9:20 quase vazio | **corrigido** | A caixa final já nasce na CONTA junto com a limpeza. VAZIO zerada. |
| 9:21–9:28 X3-10 | **corrigido em parte** | Caixa "θ ≤ 4,23° OU θ ≥ 85,77°" e a frase "SÓ QUASE RASANTE / OU QUASE NA VERTICAL" (duas linhas) na CONTA. ENCOSTADO zerada, mas **não alterei de forma explícita o rótulo "85,77° a 90°" do arco** (raio + 0,35). |
| X3 glints (G34) | **corrigido (shader)** | Glints × 0,2 e vinheta #0B1A3A a 35% na zona da Pilha. **Não medi o brilho dos glints por pixel**; FUNDO e água seguem dentro da meta (ver `qa.txt`). |

## 3.7 X4
| Linha | Estado | Como / por quê |
|---|---|---|
| 9:45–9:57 "3.000 J" solto | **corrigido** | "3.000 J LIBERADOS" preso à carga; depois o dado voa para a CONTA como E_lib e a origem some na chegada. |
| 10:00–10:40 chave | **corrigido** | Chave GEO com "TOTAL = 3.000 J" sobre as barras. |
| 10:27 tokens soltos | **corrigido** | ESQUELETO zerada. |
| 10:36 trânsito v/K | **corrigido** | Duas linhas, leve primeiro, K de cada nave em 100%. TRÂNSITO e DUPLICATA zeradas. |
| 10:39 CONFERE barras 1:1 | **implementado, não medido** | A barra anima contínua de 2:1 a 1:1 (massas iguais) e vai a ~3.000 J (pesadíssima). **Não medi o 1:1** no vídeo. |

## 3.8 X5
| Linha | Estado | Como / por quê |
|---|---|---|
| 11:15 mostrador 6,0 vazio | **corrigido** | G33: 0,0 → 2,0 (suporte) → 6,0 (blocos). Auditoria BALANÇA estendida: mostrador × N/g, diferença máxima 0,045 kg em 1.877 quadros + 27 da montagem. |
| 11:48–12:00 "INTERNA" | **corrigido** | Texto "T: FORÇA INTERNA" na CONTA. |
| 11:54/12:06/12:18 tokens | **corrigido em parte** | ESQUELETO zerada nas linhas com `voa()`. **As linhas feitas por `passo()` (ex.: N = 6·(9,8 − 1,63)) não são cobertas pela auditoria**, porque o esqueleto é por glyph map; conferência visual. |
| 12:51 "N = 49 N" duas vezes | **corrigido** | DUPLICATA zerada. |
| 13:03 "T" perdido | **não localizado por pixel** | RÓTULO SOLTO zerado; a força interna agora é texto na CONTA. Não achei o "T" do v4 por inspeção direta. |
| 13:21 estado explícito | **corrigido** | Selo TRAVADO ao voltar a 3/1 kg, mostrador em 6,0; a trava abre no caso BLOCO LEVE → 0. |
| 13:24 ":" sobrando | **corrigido** | "BLOCO LEVE → 0 ⇒ 2,0 kg". |
| 13:27 rótulo some | **corrigido** | "m → 0" acompanha o bloco enquanto encolhe. |

## 3.9 Epílogo
| Linha | Estado | Como / por quê |
|---|---|---|
| 13:46–14:28, 14:36–15:33 | sem mudança | Conforme o handoff. |
| 14:30–14:33 metade de baixo vazia | **corrigido** | O primeiro cartão entra no mesmo play em que a lista sobe. |

## Outros pontos que o relatório precisa dizer
- 3 selos têm 3 linhas (DICA, CONFERE, HIPÓTESES: 5,9–6,4 × 1,02–1,09, acima do nominal 0,85): a Pilha desce junto. A auditoria imprime o aviso, mas não entra no portão.
- Os gatilhos de tempo foram estimados com a narração v1.1 com tags (2,7 palavras/s). Voltam a ser medidos com a voz real.
- SEM PALCO: 12 ocorrências no A1/EN1 (isentas) e nenhuma fora.
