import re, io
D = r"C:\Users\KaioOrtiz\PycharmProjects\parallax-long-0008\videos_longos\yt_0008_magnetostatica_ampere"
raw = io.open(D + r"\narracao_revisada_gpt.md", encoding="utf-8").read()
body = raw.split("\n---\n")[1].strip().replace("**", "")

# LaTeX -> fala (ordem importa: do mais longo para o mais curto)
SUB = [
    (r"\(\mathbf R=\mathbf r-\mathbf r'\)", "erre maiúsculo, igual a erre menos erre linha"),
    (r"\(\mathbf R/R^3\)", "o vetor separação dividido pela distância ao cubo"),
    (r"\(\mathbf J(\mathbf r')\)", "jota de erre linha"),
    (r"\(\mathbf r'\)", "erre linha"),
    (r"\(\mathbf r\)", "erre"),
    (r"\(\mathbf J\)", "jota"),
    (r"\(\mathbf F\)", "efe"),
    (r"\(R\)", "erre maiúsculo"),
    (r"\(nL\)", "ene vezes ele"),
    (r"\(n\)", "ene"),
    (r"\(N\)", "ene maiúsculo"),
    (r"\(K\)", "cá"),
    (r"\(L\)", "ele maiúsculo"),
    (r"\(C\)", "cê"),
    (r"\(S\)", "esse maiúsculo"),
    (r"\(s\)", "ésse"),
]
for a, b in SUB:
    body = body.replace(a, b)
assert "\\(" not in body, re.findall(r"\\\(.*?\\\)", body)

# tags (inglês, descritivas, uma por frase, só nos pontos-chave); cada frase inicial aparece uma vez em sequência
TAGS = [
    ("Existe uma coisa estranha", "[curious]"),
    ("Como um campo pode circular", "[curious]"),
    ("É essa aparente contradição", "[thoughtful]"),
    ("Fala, pessoal!", "[happy]"),
    ("Em vez de começar pela corrente", "[thoughtful]"),
    ("Comecemos pelo exemplo mais simples.", "[thoughtful]"),
    ("Mas agora vamos inverter", "[curious]"),
    ("Será que isso significa", "[curious]"),
    ("Visto de cima", "[thoughtful]"),
    ("Agora calculamos o rotacional.", "[thoughtful]"),
    ("Como a derivada de uma constante é zero", "[slow, measured pace]"),
    ("Essa é a primeira ideia importante", "[slow, measured pace]"),
    ("Para entender o que o rotacional realmente mede", "[thoughtful]"),
    ("Neste campo do fio, podemos enxergar", "[thoughtful]"),
    ("Mas agora vem a parte interessante.", "[curious]"),
    ("E surge a pergunta:", "[curious]"),
    ("A resposta está exatamente", "[slow, measured pace]"),
    ("Antes de resolver essa singularidade", "[thoughtful]"),
    ("Será que o campo magnético possui", "[curious]"),
    ("Essa é a forma diferencial da lei de Gauss", "[slow, measured pace]"),
    ("O contraste com o campo elétrico", "[thoughtful]"),
    ("Agora vamos mostrar que esse resultado", "[curious]"),
    ("Agora calculamos o divergente do campo magnético", "[thoughtful]"),
    ("Antes, vale separar muito bem", "[slow, measured pace]"),
    ("Perceba que agora a justificativa", "[slow, measured pace]"),
    ("Desta vez, em vez do divergente", "[curious]"),
    ("Mas algo especial acontece", "[curious]"),
    ("E é exatamente esse tipo de objeto", "[slow, measured pace]"),
    ("A delta de Dirac não deve ser pensada", "[thoughtful]"),
    ("Portanto, a primeira parcela", "[slow, measured pace]"),
    ("Ainda precisamos verificar a segunda.", "[curious]"),
    ("Aqui, finalmente, entra a equação da continuidade.", "[slow, measured pace]"),
    ("E sobra a relação local fundamental:", "[excited]"),
    ("Essa é a forma local da lei de Ampère", "[slow, measured pace]"),
    ("Mas antes podemos voltar ao paradoxo do fio.", "[curious]"),
    ("Em vez de um fio matematicamente sem espessura", "[thoughtful]"),
    ("Mas esse termo explodiria no eixo.", "[thoughtful]"),
    ("Agora temos o perfil completo.", "[calm, satisfied]"),
    ("Agora vamos comprimir esse fio.", "[curious]"),
    ("E finalmente resolvemos o paradoxo da abertura.", "[excited]"),
    ("Portanto, um laço que envolve o fio", "[slow, measured pace]"),
    ("Agora temos uma lei local:", "[thoughtful]"),
    ("Agora falta transformar", "[curious]"),
    ("Esse é o teorema de Stokes.", "[slow, measured pace]"),
    ("Aplicando-o à lei local", "[excited]"),
    ("Se mantemos a mesma borda", "[curious]"),
    ("Agora temos uma lei poderosa.", "[thoughtful]"),
    ("Como já vimos com a lei de Gauss", "[thoughtful]"),
    ("A estratégia é:", "[slow, measured pace]"),
    ("Vamos aplicar esse método", "[thoughtful]"),
    ("Mas agora ele apareceu", "[calm, satisfied]"),
    ("Segundo exemplo:", "[thoughtful]"),
    ("Terceiro caso:", "[thoughtful]"),
    ("Num solenoide real e finito", "[thoughtful]"),
    ("Nosso último exemplo é o toroide.", "[thoughtful]"),
    ("O gráfico reúne as três regiões:", "[calm, satisfied]"),
    ("Agora podemos enxergar a estrutura completa.", "[thoughtful]"),
    ("Esses qualificadores são importantes.", "[slow, measured pace]"),
    ("Então, se você quiser guardar", "[slow, measured pace]"),
    ("Mas ainda ficou uma última pergunta.", "[curious]"),
    ("Existe.\n", "[thoughtful]"),
    ("Se esse vídeo te ajudou", "[happy]"),
]
cur = 0
out = body
for ph, tag in TAGS:
    i = out.find(ph, cur)
    assert i >= 0, ph
    # uma tag por frase: o ponto de inserção tem de ser início de frase/linha
    assert i == 0 or out[i - 1] in "\n ", (ph, repr(out[i - 5:i]))
    out = out[:i] + tag + " " + out[i:]
    cur = i + len(tag) + 1 + len(ph)

head = """# yt_0008 — narração com audio tags (v4, revisão GPT ≤ 25 min, para gerar a voz)

Fonte do texto: `narracao_revisada_gpt.md` (revisão do GPT sobre a v1; "corrente envolvida" padronizado). Fala sem alteração de conteúdo; só (1) símbolos LaTeX trocados pela fala (ver tabela abaixo) e (2) tags em inglês nos pontos-chave, uma por frase, que valem até a próxima tag e não entram na legenda nem no SRT.
Voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`. **Gerar só depois da confirmação do usuário** (gasta crédito). Âncoras e tempos: `narracao_ancoras.md`.

Letras faladas (a tela mostra o símbolo; a fala usa o nome): s → "ésse"; J → "jota"; r → "erre"; r′ → "erre linha"; R → "erre maiúsculo"; F → "efe"; C → "cê"; S → "esse maiúsculo"; K → "cá"; L → "ele maiúsculo"; n → "ene"; N → "ene maiúsculo".

## Texto corrido (para gravação)

"""
io.open(D + r"\narracao_tags.md", "w", encoding="utf-8").write(head + out + "\n")
print("tags", len(TAGS), "chars", len(out), "palavras", len(re.sub(r"\[[^\]]*\]", "", out).split()))
