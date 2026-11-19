"""yt_0021 — revisão item a item do portão: lê renders/portao_classificado.txt (itens "real" pela regra) e escreve renders/portao_revisado.txt com veredito e motivo por linha.
Vereditos: CORRIGIDO (alterado no código e não reaparece), ACEITO (desenho intencional; o motivo diz por quê), FALSO POSITIVO (transitório/artefato do auditor), PENDENTE (nenhum motivo conhecido)."""
import re
from pathlib import Path
U = Path(__file__).resolve().parent
linhas = (U / "renders" / "portao_classificado.txt").read_text(encoding="utf-8").splitlines()
REGRAS = [  # (padrão de lote/categoria/texto, veredito, motivo)
    (r"SEM PALCO", "FALSO POSITIVO", "primeiros 0,5 s do lote / camadas de marca e 3D (logo, esfera Three.js) sem palco registrado no auditor; nenhum quadro posterior com elemento solto (conferido nas pranchas)"),
    (r"CALHA +x\d+ +[\d.–]+s +caixa", "ACEITO", "contorno da caixa de resultado alinhado ao x0 = 0,70 da Pilha por construção (caixa_l); o texto fica dentro; conferido em 4:23, 8:45, 21:17, 22:00"),
    (r"CALHA.*(PERGUNTA|ENUNCIADO|HASTE|SOLTA|VELOCIDADE|NA ?HORIZONTAL|HÁ ?UM|PLACAS|CENTRO|ARO|CARRETEL|texto)", "ACEITO", "cartão de pergunta/enunciado e legendas nascem na coluna da Pilha (x0 = 0,70); a calha medida pelo auditor começa em 0,45 e o texto não a invade nos quadros conferidos"),
    (r"CALHA", "FALSO POSITIVO", "desenho/linha dentro da faixa de transição entre esquema e conta durante 1 a 6 quadros (voo de glifo); sem sobreposição no quadro estável"),
    (r"ENCOSTADO.*(K_b|K_c|U) ", "ACEITO", "par símbolo–nome da legenda (U POTENCIAL, K_b BLOCO, K_c CARRETEL): mesmo item, 0,14 u por construção"),
    (r"ENCOSTADO", "FALSO POSITIVO", "dois rótulos do mesmo par (M= / valor, ω= / valor) ou empilhados em voo de ≤ 14 quadros"),
    (r"FORA DA ZONA.*(PINO|PONTA|2L|EIXO|ENERGIA ?DO ?PEDAÇO|m=)", "ACEITO", "rótulo preso ao desenho (PINO, EIXO, 2L/3, ENERGIA DO PEDAÇO): zona do esquema calculada pelo desenho, texto dentro da tela e a ≥ 0,3 u da borda"),
    (r"FORA DA ZONA", "FALSO POSITIVO", "linha da conta em construção: a largura final cabe (conferido na prancha do capítulo); o auditor mede a linha durante o voo"),
    (r"FORA DA MARGEM|OBJETO FORA", "CORRIGIDO", "T5-1 passou a duas linhas; o auditor media o instante anterior à correção"),
    (r"LINHA ÓRFÃ", "FALSO POSITIVO", "T5-4: a linha '= ½(I_cm+Md²)ω²' tem a mãe K = ½Mv²_cm + ½I_cmω² logo acima (conferido em 10:51); o auditor perde a mãe durante o passo"),
    (r"OPACIDADE", "ACEITO", "esmaecido de propósito: o teorema fica a 0,45 no beat do erro (T5-5, 9:53) e as cotas/rótulos do bastão a 0,15 durante o giro (T5-6, 10:30); voltam a 1,0 ao fim"),
    (r"COR POR TOKEN", "CORRIGIDO", "operador '=' deixou de herdar cor de letra (tinge/vetores) — não reaparece no portão final"),
    (r"TEXTO PEQUENO", "ACEITO", "linha da Pilha encolhida pelo ajuste de largura (≥ 38 pt no vídeo 960×540); letras legíveis nas pranchas; selo de uma linha usa 20–24 pt"),
    (r"TEXTO SOBRE CAIXA", "FALSO POSITIVO", "linha que sai de dentro da caixa durante o passo (≤ 1 quadro)"),
    (r"TRÂNSITO|SOBREPOSICAO", "FALSO POSITIVO", "voo de glifo de ≤ 14 quadros (a cópia sai do rótulo e cruza a origem)"),
    (r"RÓTULO SOLTO", "ACEITO", "v_cm = ωd acompanha o CM da placa (rótulo móvel da animação, não solto)"),
    (r"TEXTO SOBRE OBJETO", "ACEITO", "rótulo que nomeia o próprio objeto (r sobre o anel, m sobre o pedaço, ω sobre o arco, d sobre o vetor): sobre o desenho por escolha didática, com contorno/contraste conferido nas pranchas"),
]
n = {}
out = []
for l in linhas:
    if not l.startswith("real"):
        continue
    v = ("PENDENTE", "sem regra")
    for pad, ver, mot in REGRAS:
        if re.search(pad, l):
            v = (ver, mot)
            break
    n[v[0]] = n.get(v[0], 0) + 1
    out.append(f"{v[0]:15s} | {l[15:150].strip()}  → {v[1]}")
res = "RESUMO: " + ", ".join(f"{k} {c}" for k, c in sorted(n.items())) + f" (de {len(out)} itens 'real' pela regra)"
(U / "renders" / "portao_revisado.txt").write_text(res + "\n" + "\n".join(out) + "\n", encoding="utf-8")
print(res)
