"""Seção 4: a lei de Biot–Savart, montada fator por fator sobre o diagrama vivo da geometria."""
import math

import numpy as np
from manim import (
    VGroup, Polygon, FadeIn, FadeOut, Create, Indicate, ValueTracker, always_redraw, linear, smooth,
)
from base import *  # noqa: F401,F403


class Sec3:
    def lei(self):
        self.section("lei", "Biot–Savart: uma lei experimental")
        self.drop("H")
        self.drop("A")
        L, W = self.L, self.W
        th, Rd = self.theta_local, self.Rd
        self.play(self.Rd.animate.set_value(2.0), run_time=1.0)
        ia = arrow(W([-2.0, 0.42, 0]), W([-1.15, 0.42, 0]), GREEN, 5, z=7)
        il = self.lab("I", W([-1.6, 0.8, 0]), "I", size=M_M)
        dbs = always_redraw(lambda: self.out_symbol(
            W(self.local_pt()) + np.array([0.62, 0.0, 0]),
            1, radius=max(0.035, 0.24 * math.sin(th.get_value()) * (2.0 / Rd.get_value()) ** 2)))
        dbl = self.lab(r"d\mathbf B", [0, 0, 0], r"d\mathbf B", size=M_M)
        dbl.add_updater(lambda m: m.move_to(W(self.local_pt()) + np.array([1.2, 0.0, 0])))
        self.play(FadeIn(ia), FadeIn(il), FadeIn(dbs), FadeIn(dbl), run_time=1.0)
        self.caption("O elemento de corrente $I\\,d\\ell$ produz uma contribuição $d\\mathbf B$ em $P$")
        self.show(E(r"dB\propto I\,d\ell", "dB", "I", r"d\ell", r"\propto", size=M_XL),
                  src={("dB", 0): dbl, ("I", 0): il, (r"d\ell", 0): L["dll"]}, rt=2.2, wait=2.5)
        self.mark("lei_idl")
        # 1/R²
        self.caption("Quanto mais longe de $P$, mais fraca a contribuição")
        self.play(Rd.animate.set_value(4.0), run_time=3.0)
        self.hold(1.0)
        self.show(E(r"dB\propto\frac{I\,d\ell}{R^2}", "dB", "I", r"d\ell", r"\propto", "R^2", size=M_XL),
                  src={("R^2", 0): L["Rl"]}, rt=2.0, wait=2.0)
        self.show(E(r"R\to2R\ \implies\ dB\to\frac{dB}{4}", "R", "dB", size=M_M), slot="A",
                  src={("dB", 0): dbl, ("dB", 1): dbl, ("R", 0): L["Rl"]}, rt=1.8, wait=3.0)
        self.mark("lei_inverso_quadrado")
        self.play(Rd.animate.set_value(2.0), run_time=1.5)
        self.drop("A")
        # sin θ
        self.caption("A direção importa: só a parte perpendicular de $d\\boldsymbol\\ell$ conta")
        self.play(th.animate.set_value(math.radians(22)), run_time=2.0)
        self.play(th.animate.set_value(math.pi / 2), run_time=2.5)
        self.show(E(r"dB\propto\frac{I\,d\ell\,\sin\theta}{R^2}", "dB", "I", r"d\ell", r"\propto", "R^2", r"\sin\theta", size=M_XL),
                  src={(r"\sin\theta", 0): L["thl"]}, rt=2.0, wait=2.5)
        self.mark("lei_sen")
        # constante
        self.show(E(r"\frac{\mu_0}{4\pi}", r"\frac{\mu_0}{4\pi}", size=M_L), slot="A", rt=1.2, wait=0.5)
        auxc = txt("constante no vácuo (SI)", T_NOTE, color=DIM).move_to(AUX + np.array([0, -0.85, 0]))
        self.play(FadeIn(auxc), run_time=0.6)
        self.caption("A constante de proporcionalidade, no SI, é $\\mu_0/4\\pi$")
        self.hold(2.5)
        self.show(E(r"dB=\frac{\mu_0}{4\pi}\frac{I\,d\ell\,\sin\theta}{R^2}", "dB", "I", r"d\ell", "=", "R^2", r"\sin\theta",
                    r"\frac{\mu_0}{4\pi}", size=M_L),
                  (r"\propto", "="), src={(r"\frac{\mu_0}{4\pi}", 0): glyphs(self.slots["A"]["eq"], r"\frac{\mu_0}{4\pi}", 0)},
                  rt=2.2, wait=2.0)
        self.play(FadeOut(auxc), run_time=0.4)
        self.drop("A")
        self.mark("lei_modulo")
        # produto vetorial: paralelogramo
        par = always_redraw(lambda: Polygon(W([0, 0, 0]), W([1.0, 0, 0]),
                                            W([1.0 + math.cos(th.get_value()), math.sin(th.get_value()), 0]),
                                            W([math.cos(th.get_value()), math.sin(th.get_value()), 0]),
                                            color=VIOLET, fill_color=VIOLET, fill_opacity=0.22, stroke_width=2).set_z_index(2))
        rh = always_redraw(lambda: arrow(W([0, 0, 0]), W([math.cos(th.get_value()), math.sin(th.get_value()), 0]),
                                         VIOLET, 3.5, z=8, tip=0.2))
        rhl = self.lab(r"\hat{\mathbf R}", [0, 0, 0], r"\hat{\mathbf R}", size=M_M)
        rhl.add_updater(lambda m: m.move_to(W([1.0 * math.cos(th.get_value()) + 0.4, 1.0 * math.sin(th.get_value()) + 0.12, 0])))
        self.play(FadeIn(par), FadeIn(rh), FadeIn(rhl), run_time=1.2)
        self.caption("A área do paralelogramo de $d\\boldsymbol\\ell$ e $\\hat{\\mathbf R}$ vale $d\\ell\\,\\sin\\theta$")
        self.play(th.animate.set_value(math.radians(35)), run_time=2.0)
        self.play(th.animate.set_value(math.pi / 2), run_time=2.0)
        self.show(E(r"\left|d\boldsymbol\ell\times\hat{\mathbf R}\right|=d\ell\,\sin\theta", r"d\boldsymbol\ell", r"\hat{\mathbf R}",
                    r"d\ell", r"\sin\theta", r"\times", size=M_M), slot="A",
                  src={(r"d\boldsymbol\ell", 0): L["dll"], (r"\hat{\mathbf R}", 0): rhl, (r"\sin\theta", 0): L["thl"]},
                  rt=2.0, wait=3.0)
        self.mark("lei_paralelogramo")
        self.caption("O produto vetorial guarda o módulo e ainda dá a direção de $d\\mathbf B$")
        self.show(E(r"d\mathbf B=\frac{\mu_0}{4\pi}\frac{I\,d\boldsymbol\ell\times\hat{\mathbf R}}{R^2}", r"d\mathbf B", "I",
                    r"d\boldsymbol\ell", r"\times", r"\hat{\mathbf R}", "R^2", r"\frac{\mu_0}{4\pi}", "=", size=M_L),
                  ("dB", r"d\mathbf B"), (r"d\ell", r"d\boldsymbol\ell"), (r"\sin\theta", None),
                  src={(r"\times", 0): glyphs(self.slots["A"]["eq"], r"\times", 0),
                       (r"\hat{\mathbf R}", 0): glyphs(self.slots["A"]["eq"], r"\hat{\mathbf R}", 0)}, rt=2.4, wait=3.0)
        self.mark("lei_unitario")
        self.drop("A")
        # R̂ = R/R
        self.play(FadeOut(par), FadeOut(rh), FadeOut(rhl), run_time=0.7)
        self.caption("$\\hat{\\mathbf R}$ é o vetor $\\mathbf R$ com módulo 1")
        self.show(E(r"\hat{\mathbf R}=\frac{\mathbf R}{R}", r"\hat{\mathbf R}", r"\mathbf R", "R", size=M_L), slot="A",
                  src={(r"\hat{\mathbf R}", 0): glyphs(self.slots["H"]["eq"], r"\hat{\mathbf R}", 0), (r"\mathbf R", 0): L["Rl"]},
                  rt=1.8, wait=2.0)
        aux = self.slots["A"]["eq"]
        self.show(E(r"d\mathbf B=\frac{\mu_0}{4\pi}\frac{I\,d\boldsymbol\ell\times\frac{\mathbf R}{R}}{R^2}", r"d\mathbf B", "I",
                    r"d\boldsymbol\ell", r"\times", r"\mathbf R", "R^2", r"\frac{\mu_0}{4\pi}", "=", "R", size=M_L),
                  (r"\hat{\mathbf R}", r"\mathbf R"), src={("R", 0): glyphs(aux, "R", 0)}, rt=2.2, wait=2.0)
        self.caption("O $R$ extra vem da normalização de $\\hat{\\mathbf R}$: sobe $\\mathbf R$, desce $R$")
        self.show(E(r"d\mathbf B=\frac{\mu_0}{4\pi}\frac{I\,d\boldsymbol\ell\times\mathbf R}{R^2\,R}", r"d\mathbf B", "I",
                    r"d\boldsymbol\ell", r"\times", r"\mathbf R", "R^2", r"\frac{\mu_0}{4\pi}", "=", "R", size=M_L),
                  rt=2.2, wait=2.0)
        new = E(r"d\mathbf B=\frac{\mu_0}{4\pi}\frac{I\,d\boldsymbol\ell\times\mathbf R}{R^3}", r"d\mathbf B", "I",
                r"d\boldsymbol\ell", r"\times", r"\mathbf R", "R^3", r"\frac{\mu_0}{4\pi}", "=", size=M_L)
        self.show(new, ("R^2", "R^3"), ("R", None), rt=2.2, wait=2.0)
        self.drop("A")
        bx = box(self.slots["H"]["eq"], MAG)
        self.play(FadeIn(bx), run_time=0.6)
        self.caption("Lei de Biot–Savart: o campo de um elemento de corrente")
        self.mark("lei_R_adicional")
        self.hold(4)
        self.play(FadeOut(bx), run_time=0.4)
