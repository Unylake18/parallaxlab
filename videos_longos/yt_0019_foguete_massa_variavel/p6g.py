from ptch6 import patch
patch("conferencia.py", [
 (r'''b = pega(U / "renders" / "preview_yt0019_v5_960x540.mp4")''', r'''b = pega(U / "renders" / "preview_yt0019_v6_960x540.mp4")'''),
 (r'''"""yt_0019 v4 — R0: conferência visual antes × depois dos 65 pontos do handoff v4 (§3) + pranchas extras (§7).
Para cada ponto: quadro do v3 e do v4 no MESMO tempo, lado a lado, 960×540 cada. Saídas em renders/v5/:''',
  r'''"""yt_0019 v6 — R0: conferência visual antes × depois dos 70 pontos (v5 × v6) + pranchas extras.
Para cada ponto: quadro do v5 e do v6 no MESMO tempo, lado a lado, 960×540 cada. Saídas em renders/v6/:'''),
 (r'''COR = ["0:20",''', r'''FADES = [("#2", "1:18"), ("#4", "1:51"), ("#5", "2:12"), ("#11", "3:33"), ("#27", "8:39"), ("#56", "16:30")]
COR = ["0:20",'''),
 (r'''for t_ in COR:
    alvo[int(mm(t_) * FPS)] = []
''', r'''for t_ in COR:
    alvo[int(mm(t_) * FPS)] = []
for _, t_ in FADES:
    for dq in (0, 5, 10):                        # t, t + 0,33 s, t + 0,67 s
        alvo[int(mm(t_) * FPS) + dq] = []
'''),
 (r'''fo2 = Image.new("RGB", (2 * 640, 360 * len(COR)), "black")''',
  r'''fo3 = Image.new("RGB", (3 * 640, 360 * len(FADES)), "black")
for j, (n_, t_) in enumerate(FADES):
    for k_, dq in enumerate((0, 5, 10)):
        fo3.paste(b[int(mm(t_) * FPS) + dq].resize((640, 360)), (640 * k_, 360 * j))
fo3.save(OUT / "extra_fades.png")
fo2 = Image.new("RGB", (2 * 640, 360 * len(COR)), "black")'''),
])
