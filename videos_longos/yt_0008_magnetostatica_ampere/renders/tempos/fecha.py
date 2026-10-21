import io, re
D = r"C:\Users\KaioOrtiz\PycharmProjects\parallax-long-0008\videos_longos\yt_0008_magnetostatica_ampere"
t = io.open(D + r"\narracao_tags.md", encoding="utf-8").read()
body = t.split("## Texto corrido (para gravação)")[1].strip()
clean = re.sub(r"\[[^\]]*\]\s*", "", body)          # sem audio tags (legenda, SRT e ASR usam este texto)
clean = re.sub(r"\n{3,}", "\n\n", clean).strip() + "\n"
io.open(D + r"\texto_narracao.txt", "w", encoding="utf-8", newline="\n").write(clean)
print(len(clean.split()), "palavras;", body.count("["), "tags no arquivo com tags")
assert "[" not in clean and "\\(" not in clean
