from ptch6 import patch
# T2: unidades numa linha só (sai da margem)
patch("sec_t2.py", [
 (r'''U_, iu = M(r"\frac{\mathrm{m}}{\mathrm{s}}\cdot\frac{\mathrm{kg}}{\mathrm{s}}", "=", r"\frac{\mathrm{kg\cdot m}}{\mathrm{s^2}}", "=", r"\mathrm{N}", size=40)
        U_.move_to(P3(-7.2 + U_.width / 2, -4.1))''',
  r'''U_, iu = M(r"\mathrm{m/s}\cdot\mathrm{kg/s}", "=", r"\mathrm{kg\cdot m/s^2}", "=", r"\mathrm{N}", size=40)
        U_.move_to(P3(-7.2 + U_.width / 2, -3.95))'''),
])
# T4-3: rótulos de vazão afastados na origem
patch("sec_t4.py", [
 ("r1.add_updater(lambda m_: m_.next_to(G.pt(tp1(), v_sub(tp1(), 240.0)), RIGHT, buff=0.22).shift(0.28 * DOWN))",
  "r1.add_updater(lambda m_: m_.next_to(G.pt(tp1(), v_sub(tp1(), 240.0)), RIGHT, buff=0.22).shift(0.12 * UP))"),
 ("r2.add_updater(lambda m_: m_.next_to(G.pt(tp2(), v_sub(tp2(), 120.0)), RIGHT, buff=0.22).shift(0.28 * DOWN))",
  "r2.add_updater(lambda m_: m_.next_to(G.pt(tp2(), v_sub(tp2(), 120.0)), RIGHT, buff=0.22).shift(0.42 * DOWN))"),
 ("r1.next_to(G.pt(0, 0), RIGHT, buff=0.3)\n        r2.next_to(G.pt(0, 0), RIGHT, buff=0.3)",
  "r1.next_to(G.pt(0, 0), RIGHT, buff=0.3).shift(0.12 * UP)\n        r2.next_to(G.pt(0, 0), RIGHT, buff=0.3).shift(0.42 * DOWN)"),
])
