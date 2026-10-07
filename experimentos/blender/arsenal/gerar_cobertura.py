"""Gera cobertura.md: o que o arsenal tem e o que falta, capítulo a capítulo do mapa curricular. Python puro.

    python experimentos/blender/arsenal/gerar_cobertura.py

O status de cada sólido vem das fichas (solidos/*.json): rode de novo depois de promover ou criar sólidos. As colunas
"o que falta" e "limitação" são escritas à mão aqui (LACUNAS) e cada id citado é validado contra as fichas.
"""

import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent

# capítulo do mapa -> (título, [ids que cobrem], nota opcional)
CAPITULOS = [
    ("4.4–4.5", "Plano inclinado", ["plano_inclinado"], "o diagrama de forças é do Manim"),
    ("4.6", "Movimento circular e curva inclinada", ["movimento_circular", "curva_inclinada"], ""),
    ("4.7–4.8", "Energia potencial e conservação", ["paisagem_potencial"], ""),
    ("4.9–4.10", "Momento linear e colisões", ["colisao_1d", "colisao_2d", "explosao"], "1D, 2D e explosão"),
    ("4.11", "Rotação de corpos rígidos", ["giroscopio_precessao", "anel_carregado", "disco_carregado", "haste_carregada"], "anel, disco e haste com `com_cargas=0` e `eixo=1` servem ao momento de inércia"),
    ("4.12", "Rolamento", ["esfera_rolando", "cilindro_rolando", "aro_rolando", "rampa_rolamento", "trilho_looping"], "chão plano, rampa e looping"),
    ("4.13", "Gravitação", ["orbita_kepleriana", "poco_gravitacional"], ""),
    ("5.1", "Movimento harmônico simples", ["massa_mola", "pendulo_simples"], ""),
    ("5.3–5.4", "Ondas mecânicas, superposição e estacionárias", ["onda_corda", "ondas_duas_fontes"], ""),
    ("5.6", "Fluidos em repouso", ["tanque_hidrostatico", "prensa_hidraulica"], "pressão, empuxo e Pascal"),
    ("5.7", "Fluidos em movimento", ["tubo_escoamento", "tanque_torricelli"], "continuidade e Torricelli"),
    ("5.8–5.10", "Teoria cinética e gases ideais", ["caixa_gas_cinetica"], "êmbolo oscilante"),
    ("6.1", "Lei de Coulomb", ["cargas_pontuais", "dipolo_eletrico"], ""),
    ("6.2", "Campo elétrico (distribuições contínuas)", ["anel_carregado", "disco_carregado", "haste_carregada", "campo_vetorial", "dipolo_eletrico", "linhas_de_campo_3d"], ""),
    ("6.3", "Lei de Gauss", ["casca_cilindrica_oca", "cilindro_macico_isolante", "casca_esferica_oca", "esfera_macica_isolante", "placa_infinita_carregada",
                              "cilindro_coaxial", "gaussiana_esferica", "gaussiana_cilindrica", "gaussiana_caixa"], ""),
    ("6.4", "Potencial elétrico", ["equipotenciais", "gradiente_colina"], "o gradiente é o de uma colina genérica"),
    ("6.5", "Condutores e capacitores", ["capacitor_placas_paralelas", "capacitor_esferico", "cilindro_coaxial", "condutor_com_cavidade"], ""),
    ("6.7", "Força magnética", ["particula_em_campo_magnetico", "espira_em_campo_magnetico"], ""),
    ("6.8", "Biot–Savart", ["biot_savart_espira"], ""),
    ("6.9", "Lei de Ampère", ["fio_infinito", "solenoide_corrente", "toroide_corrente", "amperiano_circular", "amperiano_retangular"], ""),
    ("6.10", "Indução eletromagnética", ["ima_espira_inducao", "barra_trilhos_fem_movimento"], ""),
    ("6.12 e 7.1", "Maxwell e ondas eletromagnéticas", ["onda_eletromagnetica"], ""),
    ("7.2", "Óptica geométrica", ["lente_delgada", "prisma_triangular", "espelho_esferico", "dioptro_plano"], "os raios são do Manim"),
    ("7.3–7.4", "Interferência e difração", ["anteparo_fenda_dupla", "ondas_duas_fontes", "rede_de_difracao", "filme_fino", "interferometro_michelson"], "fenda dupla, N fendas, filme fino e Michelson"),
    ("7.5", "Polarização e lei de Malus", ["polarizador_malus"], ""),
    ("7.6", "Relatividade especial", ["cone_de_luz", "relogio_de_luz"], ""),
    ("7.11", "Estrutura atômica", ["orbital_atomico", "atomo_bohr"], "orbitais 1s, 2s, 2p, 3d e o modelo de Bohr"),
    ("8.12 e 9.5", "Volumes de revolução", ["solido_revolucao_disco", "solido_revolucao_arruela", "solido_revolucao_cascas"], ""),
    ("10.1", "Geometria e vetores em R³", ["produto_vetorial", "superficie_quadrica", "plano_e_reta_r3"], ""),
    ("10.3", "Derivadas parciais e plano tangente", ["plano_tangente"], ""),
    ("10.5", "Gradiente", ["gradiente_colina"], ""),
    ("10.6", "Extremos em várias variáveis", ["pontos_criticos", "lagrange_restricao"], ""),
    ("10.7", "Integrais duplas", ["integral_dupla_colunas"], ""),
    ("10.8–10.9", "Integrais triplas e Jacobiano", ["elemento_volume"], ""),
    ("11.1 e 11.8", "Campos vetoriais, divergência e rotacional", ["campo_vetorial", "divergencia_local", "rotacional_roda_de_pas"], ""),
    ("11.2–11.3", "Integrais de linha", ["integral_de_linha"], ""),
    ("11.6–11.7", "Superfícies parametrizadas e integrais de superfície", ["superficie_parametrizada", "gaussiana_esferica", "gaussiana_cilindrica", "gaussiana_caixa"], ""),
    ("13", "Álgebra linear", ["transformacao_linear_3d", "autovetores_elipsoide"], ""),
    ("15", "Equações diferenciais parciais", ["membrana_modos"], "um modo por vez"),
    ("11.9", "Teorema de Stokes", ["teorema_stokes"], ""),
    ("11.10", "Teorema da divergência de Gauss", ["gaussiana_esferica", "gaussiana_cilindrica", "gaussiana_caixa"], ""),
]

# (capítulo, assunto, sólido sugerido, tipo, limitação / motivo)   tipo: "3D possível" ou "Manim"
LACUNAS = [
    ("4.4–4.5", "Polias, atrito e máquina de Atwood", "—", "Manim", "o essencial são os diagramas de corpo livre e as equações: o 3D acrescenta pouco"),
    ("5.2", "Oscilações amortecidas e forçadas", "—", "Manim", "o essencial é o gráfico x(t) e o plano de fase"),
    ("5.5", "Som (pressão, Doppler, batimentos)", "—", "Manim", "ondas longitudinais e figuras de pressão pedem 2D (cortes) e animação de frentes"),
    ("5.11–5.12", "Entropia, máquinas térmicas, condução e radiação", "—", "Manim", "dependem de uma escala de cor de temperatura (não definida no padrão) e de diagramas planos"),
    ("6.6", "Circuitos DC, RC e Kirchhoff", "—", "Manim", "esquemas elétricos são diagramas planos"),
    ("6.11", "Indutância, RL, LC e RLC", "—", "Manim", "circuitos e gráficos de oscilação"),
    ("7.7–7.10", "Corpo negro, fótons, ondas de matéria e Schrödinger", "—", "Manim", "gráficos e funções de onda 1D"),
    ("7.12", "Física nuclear e partículas", "—", "Manim", "decaimento exponencial e panorama de partículas"),
    ("8.1–8.11, 9.1–9.4, 9.8–9.11", "Funções, limites, derivadas, integrais, séries e Taylor", "—", "Manim", "são curvas e equações em 2D"),
    ("9.6–9.7", "Curvas paramétricas e polares", "—", "Manim", "planas: o sólido de revolução cobre a parte 3D (9.5)"),
    ("10.4", "Regra da cadeia multivariável", "—", "Manim", "é uma fórmula com diagrama de dependências"),
    ("10.10", "Centro de massa e momentos em 3D", "—", "3D possível", "reutiliza os sólidos de revolução e `elemento_volume`; não há um sólido dedicado"),
    ("11.4", "Campos conservativos e potencial", "—", "3D possível", "`gradiente_colina` mostra o potencial; o teste de conservatividade é do Manim"),
    ("11.5", "Teorema de Green", "—", "Manim", "região plana e contorno (o `teorema_stokes` é o análogo 3D)"),
    ("14", "Equações diferenciais ordinárias e planos de fase", "—", "Manim", "campos de direção e retratos de fase em 2D"),
]


def ler_fichas():
    return {f.stem: json.loads(f.read_text(encoding="utf-8")) for f in sorted((AQUI / "solidos").glob("*.json"))}


def main():
    fichas = ler_fichas()
    erros = []
    linhas = []
    usados = set()
    for cap, titulo, ids, nota in CAPITULOS:
        for i in ids:
            if i not in fichas:
                erros.append(f"capítulo {cap}: sólido '{i}' não existe nas fichas")
            usados.add(i)
        sts = {i: fichas[i]["status"] for i in ids if i in fichas}
        cels = ", ".join(f"`{i}` ({sts.get(i, '?')}{', anima' if 'animacao' in fichas.get(i, {}) else ''})" for i in ids)
        linhas.append(f"| {cap} | {titulo} | {cels} | {nota} |")
    if erros:
        print("ERROS:\n  " + "\n  ".join(erros))
        sys.exit(1)

    nao_listados = sorted(set(fichas) - usados)
    n_anim = sum(1 for f in fichas.values() if "animacao" in f)
    st = {}
    for f in fichas.values():
        st[f["status"]] = st.get(f["status"], 0) + 1
    resumo = ", ".join(f"{v} {k}" for k, v in sorted(st.items()))

    lac_3d = [l for l in LACUNAS if l[3] == "3D possível"]
    lac_m = [l for l in LACUNAS if l[3] == "Manim"]
    texto = f"""# Cobertura do arsenal 3D por capítulo do mapa curricular

> Arquivo **gerado** por `gerar_cobertura.py`. O status vem das fichas (`solidos/*.json`); as lacunas são mantidas no script.
> Total: **{len(fichas)} sólidos** ({resumo}); **{n_anim}** têm animação (loop ou ciclo único). Fonte dos capítulos: `docs/mapa_curricular.md`.

## 1. O que temos, por assunto do curso

| Capítulo | Assunto | Sólidos (status, animação) | Observação |
|---|---|---|---|
{chr(10).join(linhas)}

{f"Sólidos que não aparecem em nenhum capítulo acima: {', '.join(nao_listados)}." if nao_listados else "Todos os sólidos aparecem em pelo menos um capítulo."}

## 2. O que não temos, com o assunto e a limitação

### 2a. Poderiam ser sólidos 3D ({len(lac_3d)} lacunas)

| Capítulo | Assunto | Sólido sugerido | Limitação / por que ainda não |
|---|---|---|---|
{chr(10).join(f"| {c} | {a} | `{s}` | {l} |" for c, a, s, t, l in lac_3d)}

### 2b. Melhor no Manim, sem sólido 3D ({len(lac_m)} blocos)

| Capítulo | Assunto | Motivo |
|---|---|---|
{chr(10).join(f"| {c} | {a} | {l} |" for c, a, s, t, l in lac_m)}

## 3. Limitações que valem para todo o arsenal

- **Só o objeto**: fórmulas, valores, gráficos, rótulos (N/S, +/−, nomes de vetores) e raios são do Manim.
- **Cor**: segue `estilo.json` (E = ciano, B = magenta, vetores físicos = branco, normal = azul, construções = violeta).
- **Uso em vídeo**: nenhum sólido foi usado em vídeo real ainda; usar um exige handoff (ver `AGENTS.md`).
- **Movimento**: calculado por fórmula (didático), não uma simulação física; os loops fecham sem emenda, os de ciclo único (colisão, partícula em B, ímã, cone de luz, soma de Riemann) não.
- **Custo**: de 0,4 a 1,7 s por quadro em 1080p com alpha; frames ficam fora do Git (`renders/arsenal3d/`).
"""
    (AQUI / "cobertura.md").write_text(texto, encoding="utf-8")
    print(f"OK: cobertura.md ({len(fichas)} sólidos, {len(lac_3d)} lacunas 3D, {len(lac_m)} blocos Manim)")


main()
