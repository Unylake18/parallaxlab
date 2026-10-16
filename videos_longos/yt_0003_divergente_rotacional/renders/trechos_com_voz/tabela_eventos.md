# yt_0003 — correções de sincronia com base no ASR (tempos absolutos do vídeo com voz)

Janela da fala = transcrição faster-whisper large-v3. "Novo visual" = instante-alvo programado na cena (`self.marco`), conferido por quadros nos trechos renderizados. Desvio = atraso do marco medido na execução (0 = chegou no alvo). O ASR tem incerteza de décimos de segundo.

| Bloco | Janela da fala (s) | Novo início/fim visual (s) | Desvio restante |
|---|---|---|---|
| G04 | "de frente… máxima" 120,20–123,44; "tangente… zero" 123,44–127,14 | diagrama 119,9; vetor de frente até 123,5; rotação 123,5→126,8; sai em 127,0 | 0 |
| D10 | "secante vira tangente" 354,10–355,68; "derivada" 356,76–357,96 | Indicate 347,7; convergência 349,5→355,5; ∂E_x/∂x 356,1→357,6 | marco 356,1 com +0,19 s |
| D11 | "y e z fixos" ≈ 361 | destaque 361,0–362,0; limpeza 369,2–369,8 | 0 |
| D12 | fala 369,92 | entrada ≈ 370,2 (instante do bloco corrigido pelo ASR); dx·dy·dz 371,4; dV 377,0–377,6; ∂E_x/∂x·dV 378,0 | 0 |
| K01 | "Veja um exemplo simples" 633,94–634,92 | entrada 634,2 (instante do bloco corrigido pelo ASR) | 0 |
| K03 | 3κ 664,06–664,70; densidade uniforme 667,40–670,46; ρ 670,46–672,78 | 3κ ≈ 664,6; campo+nuvem 665,9–667,0 e rótulo 668,4; ρ=3ε₀κ 670,6–671,4 | 0 |
| P06 | motivação até 763,72; nome 763,94–766,80; notação 767,02–770,68 | fonte concentrada mantida até 763,1; nome 764,0; símbolo 766,7 (nome sai ao entrar o símbolo) | marco 763,95 com +0,12 s |
| P08 | seleção 800,40–803,96; "resultado é f de zero" 804,12–805,86; explicação até 815,42 | f 793,8; integrando 796,2; seleção 800,4; f(0) 802,7; igualdade 804,1→805,7; sustentada até 815,4 | 0 |
| R02 | tangência 891,30–895,48 | eixos 889,4; vetor 892,3; Ω 895,6 | 0 |
| S03 | pares 1190,22–1197,14; "elas se cancelam" 1197,26–1198,42 | par 1190,3; todos 1193,0; cancelamento 1197,3–1198,3; borda externa depois | 0 |
| F04 | gradiente 1425,30–1430,42; E 1430,62–1435,32 | equipotenciais 1420,0; ponto 1422,6; gradiente 1425,3; E 1430,6 | 0 |

Não retemporizados (por decisão do parecer): P07, F01. Excessos remanescentes de animação sobre a fala (fora do escopo): P07 0,44 s, D16 0,27 s, M02 0,22 s.
Os clipes `trecho_<T>_com_voz.mp4` usam a fatia da voz correspondente (A 0–198 s, B 197–483, K 634–683, D 682–1019, E 1018–1325, F 1324–1486); o trecho C (teorema/Gauss diferencial, 483–634 s) não foi alterado e não foi re-renderizado.

## Correção do áudio dos clipes (15/10/2026)
O empacotamento dos canais estava errado (`seg.T.reshape(1,-1)`); corrigido para `seg.reshape(1,-1)` (amostras intercaladas L0,R0,L1,R1…). Validação numérica nos seis clipes (3 janelas de 2 s por clipe, decodificando o AAC e comparando com a fatia do WAV): correlação 0,956–1,000 com o canal esquerdo do WAV, lag constante de 1.024 amostras (23 ms, atraso de codificação do AAC, não compensado); correlação L×R = 1,0; 2 canais; durações áudio × vídeo: A 198,23/198,20 s, B 285,16/285,13, K 49,50/49,47, D 336,11/336,06, E 307,08/307,06, F 160,77/162,13 (a voz termina 1,4 s antes do fim do vídeo, na cauda do CTA).
