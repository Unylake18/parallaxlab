"""v7 (handoff v7 §1 e §4): quadros 960×540 dos previews v6 e v7 no MESMO instante (a voz e os tempos não mudaram) →
renders/stills_v7/<nome>_v6.png e _v7.png; pranchas renders/look_v7.png (o look: T7-8, T9-5, E8-1, dois quadros cada),
renders/antes_depois_v7.png (cada linha da tabela 1.2) e renders/residuos_v7.png (1.1, N1–N8).
Instante = quando a voz diz a frase (ancoras.json) + atraso. uso: python stills_v7.py"""
import json
import unicodedata
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
R = U / "renders"
V6, V7 = R / "preview_yt0016_v6_960x540.mp4", R / "preview_yt0016_v7_960x540.mp4"
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if c.isalnum() or c == " ").split()


def quando(aid, frase, atraso):
    pal = ANC[aid]["palavras"]
    alvo = norm(frase)
    ws = [norm(w[0])[0] if norm(w[0]) else "" for w in pal]
    for i in range(len(ws) - len(alvo) + 1):
        if ws[i:i + len(alvo)] == alvo:
            return pal[i][1] + atraso
    raise KeyError((aid, frase))


LOOK = [("look_T7-8_disco", "T7-8", "Olha esse disco no gelo", 2.5), ("look_T7-8_conta", "T7-8", "Esse giro fica", 1.5),
        ("look_T9-5_blocos", "T9-5", "aponta para a direita", 0.3), ("look_T9-5_grafico", "T9-5", "começa a descer", 0.8),
        ("look_E8-1_tiro", "E8-1", "A bala sai", 0.25), ("look_E8-1_gases", "E8-1", "em relação ao chão", 0.8)]
TAB = [("T7-8 disco", "T7-8", "Mas o disco gira", 0.6), ("T9-6 blocos", "T9-6", "O pesado para primeiro", 0.9),
       ("T10-1 blocos + barras", "T10-1", "Mas as energias", 1.2), ("E8-1 rifle", "E8-1", "um vírgula oitenta e cinco", 0.4),
       ("T8-7 Cyrano (subida)", "T8-7", "você joga o ímã de novo", 1.0), ("T8-7 Cyrano (fronteira)", "T8-7", "a atração entre o ímã e a placa", 0.6),
       ("T9-1 bola", "T9-1", "catorze metros por segundo", 0.5), ("T9-2 Terra", "T9-2", "Ninguém percebe", 0.5),
       ("fundo e chão (manequim)", "E7-2", "A velocidade de recuo", 0.0), ("A3 disco", "A3", "a área embaixo", 0.5),
       ("A4 dois discos", "A4", "Durante o choque", 0.5), ("T7-9 parábola", "T7-9", "o vertical muda", 0.0),
       ("T7-9 cargas e campo", "T7-9", "o momento do campo", 0.6), ("C-1 placas", "C-1", "No espelho, a luz volta", 0.8),
       ("A6 mapa", "A6", "vira uma ferramenta", 1.2), ("E9-5 água", "E9-5", "ao entrar na água", 0.6),
       ("E9-2 espelho", "E9-2", "Repara nas setinhas", 1.0), ("E9-1 retrato", "E9-1", "o Newton", 0.5),
       ("EN2 granada", "EN2", "na mesma parábola", 0.2), ("cavalo (H1)", "H1", "o cavalo", 0.5), ("vela (C-2)", "C-2", "Uma vela solar refletora", 0.5)]
RES = [("1.1 A3 glifo", "A3", "que é a variação do momento", 0.5), ("1.1 A5 legenda", "A5", "uma força interna", 0.5),
       ("1.1 T9-6 troca", "T9-6", "O pesado para primeiro", 0.3), ("1.1 T10-4 DICA", "T10-4", "", 0.25),
       ("1.1 E8-2 rótulos", "E8-2", "quinhentos e noventa e nove", 0.8), ("1.1 EN2 pedaço", "EN2", "No próximo vídeo", 0.5),
       ("N1 T8-8 dica", "T8-8", "Por isso andar no gelo", 0.8), ("N2 E7-5 chips", "E7-5", "E a energia", 0.5),
       ("N3/N4 E9-5", "E9-5", "a luz se aproxima da normal", 1.2), ("N5 C-2 fótons", "C-2", "Uma vela solar refletora", 0.5),
       ("N6 E7-4", "E7-4", "Só a parte horizontal", 0.2), ("N7 E6-4", "E6-4", "Ela só se conserva", 1.6), ("N8 T9-2", "T9-2", "Ninguém percebe", 0.5)]


def tempo(aid, frase, at):
    if not frase:
        return ANC[aid]["t0"] + at
    try:
        return quando(aid, frase, at)
    except KeyError:
        print("frase não achada:", aid, frase)
        return ANC[aid]["t0"] + at


def quadros(video, ts):
    c = av.open(str(video))
    st = c.streams.video[0]
    alvo = sorted(set(round(t * 15) for t in ts))
    out, i = {}, 0
    for k, fr in enumerate(c.decode(st)):
        if i < len(alvo) and k == alvo[i]:
            out[k] = fr.to_image().convert("RGB")
            i += 1
            if i == len(alvo):
                break
    c.close()
    return {t: out.get(round(t * 15)) for t in ts}


def fonte(n):
    try:
        return ImageFont.truetype("arial.ttf", n)
    except OSError:
        return ImageFont.load_default()


def prancha(itens, nome, pares=True, cols=2):
    W, H = 480, 270
    if pares:
        lin = len(itens)
        img = Image.new("RGB", (2 * W + 30, lin * (H + 26) + 10), (12, 16, 30))
        d = ImageDraw.Draw(img)
        for i, (rot, a, b) in enumerate(itens):
            y = 10 + i * (H + 26)
            d.text((10, y), rot + "  (v6 | v7)", fill=(220, 228, 245), font=fonte(16))
            for j, im in enumerate((a, b)):
                if im is not None:
                    img.paste(im.resize((W, H)), (10 + j * (W + 10), y + 20))
    else:
        lin = (len(itens) + cols - 1) // cols
        img = Image.new("RGB", (cols * (W + 10) + 10, lin * (H + 26) + 10), (12, 16, 30))
        d = ImageDraw.Draw(img)
        for i, (rot, im) in enumerate(itens):
            x, y = 10 + (i % cols) * (W + 10), 10 + (i // cols) * (H + 26)
            d.text((x, y), rot, fill=(220, 228, 245), font=fonte(16))
            if im is not None:
                img.paste(im.resize((W, H)), (x, y + 20))
    img.save(R / nome)
    print(nome, img.size)


if __name__ == "__main__":
    (R / "stills_v7").mkdir(exist_ok=True)
    grupos = {"look": LOOK, "tab": TAB, "res": RES}
    ts = {g: [tempo(a, f, at) for _, a, f, at in L] for g, L in grupos.items()}
    todos = sorted(set(t for v in ts.values() for t in v))
    q6, q7 = quadros(V6, todos), quadros(V7, todos)
    for g, L in grupos.items():
        for (nome, *_), t in zip(L, ts[g]):
            arq = "".join(c if c.isalnum() or c in "-_" else "_" for c in nome)
            for v, q in (("v6", q6), ("v7", q7)):
                if q[t] is not None:
                    q[t].save(R / "stills_v7" / f"{arq}_{v}.png")
    prancha([(f"{n} · {int(t // 60)}:{t % 60:04.1f}", q7[t]) for (n, *_), t in zip(LOOK, ts["look"])], "look_v7.png", pares=False)
    prancha([(f"{n} · {int(t // 60)}:{t % 60:04.1f}", q6[t], q7[t]) for (n, *_), t in zip(TAB, ts["tab"])], "antes_depois_v7.png")
    prancha([(f"{n} · {int(t // 60)}:{t % 60:04.1f}", q6[t], q7[t]) for (n, *_), t in zip(RES, ts["res"])], "residuos_v7.png")
