from kit import *

class TF(Base):
    def construct(self):
        self.setup_base(cap="TESTE", selo="SELO")
        cv, pts = cavalo(0.0, 0.0)
        cv.scale(0.8, about_point=ORIGIN).shift(P3(1.0, -0.3))
        cv2, _ = cavalo(1.3, 1.0)
        cv2.scale(0.5, about_point=ORIGIN).shift(P3(4.8, -0.3))
        pd = pedra().scale(0.8, about_point=ORIGIN).shift(P3(-3.0, -0.3))
        self.add(chao(-7, 7, -0.3), cv, cv2, pd)
        xs = [-6.3, -4.8, -3.3, -1.6, 0.2, 2.0, 3.6, 5.2]
        for x, pz in zip(xs, ["pe", "agarra", "mira", "sentado", "joga", andar(0.0), andar(1.6), andar(3.2)]):
            q = None if pz not in ("sentado", "joga") else -3.2
            self.add(PessoaPerfil(x, -3.7, 1.6, 1 if x < 4 else -1, pz, quadril=q))
        r, b = rifle(0.98)
        self.add(r.shift(P3(6.2, 1.2)), ima().shift(P3(-6, 1.5)), mola(P3(-6, 2.2), P3(-4.5, 2.2)))
        self.wait(0.1)
