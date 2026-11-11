"""[eixos] origem de cada plano cartesiano num cruzamento da grade GROSSA (múltiplos de 120 px a partir do centro (960, 540)) e unidade múltipla de 24 px."""
PLANOS = [("B1 curva", (360, 540), (72, 72)), ("B1 campo", (1560, 540), (48, 48)), ("B2 entrada", (240, 660), (96, 144)), ("B2 saída", (1440, 540), (96, 96)),
          ("B3 entrada", (480, 540), (96, 96)), ("B3 saída", (1440, 660), (48, 48)), ("B5 palco", (600, 540), (96, 96)), ("B5 miniatura 2", (1320, 780), (48, 48)), ("B5 miniatura 3", (1320, 900), (48, 48)), ("B6 palco", (600, 540), (96, 96)),
          ("H1/H2 palco", (960, 540), (96, 96)), ("H3 esquerda", (480, 540), (72, 72)), ("H3 direita", (1440, 540), (72, 72)), ("S2 esquerda", (480, 540), (72, 72)),
          ("S2 direita", (1440, 540), (72, 72)), ("S1 disco", (360, 420), (72, 72)), ("S1 campo", (1560, 420), (48, 48))]
for n, (x, y), (ux, uy) in PLANOS:
    ok = (x - 960) % 120 == 0 and (y - 540) % 120 == 0 and ux % 24 == 0 and uy % 24 == 0
    print(f"[eixos] {n}: origem ({x}, {y}) {'num cruzamento grosso' if (x - 960) % 120 == 0 and (y - 540) % 120 == 0 else 'FORA da grade grossa'}; unidade {ux} × {uy} px {'(múltipla de 24)' if ux % 24 == 0 and uy % 24 == 0 else 'FORA'} {'OK' if ok else 'FALHA'}")
