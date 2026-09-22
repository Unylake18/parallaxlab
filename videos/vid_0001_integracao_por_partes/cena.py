from manim import (
    DOWN, GREEN, TEAL, YELLOW, FadeIn, FadeOut, Indicate, Line,
    Rectangle, Scene, SurroundingRectangle, TransformMatchingTex,
    VGroup, Write, config,
)

import template.config
from template.helpers import make_equation, make_title


class TemplateSmokeTest(Scene):
    def construct(self):
        frame = Rectangle(
            width=config.frame_width - 0.2,
            height=config.frame_height - 0.2,
        )

        # Smoke test temporário dos helpers, sem conteúdo do piloto.
        title = make_title("Parallax Lab\nTemplate vertical OK")
        equation = make_equation(r"1 + 1 = 2")
        content = VGroup(title, equation).arrange(DOWN, buff=0.8)

        self.add(frame, content)
        self.wait(1)


class Integral001(Scene):
    """Preview de aproximadamente 69 s para os sete blocos de narração."""

    def construct(self):
        self.camera.background_color = "#101820"

        def equation(tex, y=1.5, scale=1):
            mob = make_equation(tex).scale(scale)
            if mob.width > 7.7:
                mob.scale_to_fit_width(7.7)
            return mob.move_to([0, y, 0])

        def note(text, y=4.6):
            mob = make_title(text).scale(0.72)
            if mob.width > 7.7:
                mob.scale_to_fit_width(7.7)
            return mob.move_to([0, y, 0])

        def hold_until(seconds):
            remaining = seconds - self.time
            if remaining > 0:
                self.wait(remaining)

        # Bloco 1: 0–4,963 s; transições antecipam levemente o próximo bloco.
        original = equation(r"I=\int {{x^2}} e^x\,dx", scale=1.25)
        original.set_color_by_tex("x^2", YELLOW)
        self.add(original)
        hold_until(3.2)  # "A ideia é fazer o polinômio diminuir."
        self.play(Indicate(original.get_part_by_tex("x^2")), run_time=0.8)
        hold_until(4.6)

        # Bloco 2: 5,163–14,855 s; motivação antes dos diferenciais.
        choice = equation(r"{{u=x^2}},\qquad {{dv=e^x\,dx}}", y=3)
        choice_dv = choice.get_part_by_tex(r"dv=e^x\,dx", substring=False)
        choice_dv.set_opacity(0)
        motivation = note("Derivar reduz o grau", y=0.9)
        polynomial = equation(r"x^2\xrightarrow{\text{derivar}}2x", y=-0.4)
        polynomial.set_color(YELLOW)
        exponential = equation(r"e^x\xrightarrow{\text{integrar}}e^x", y=-2)
        exponential.set_color(TEAL)
        self.play(original.animate.scale(0.72).move_to([0, 5.8, 0]), run_time=0.6)
        self.play(FadeIn(choice), run_time=0.4)
        hold_until(7.2)  # "e dê vê igual..."
        self.play(choice_dv.animate.set_opacity(1), run_time=0.4)
        hold_until(9.4)  # "Derivar o polinômio reduz o grau..."
        self.play(FadeIn(motivation), Write(polynomial), run_time=0.8)
        hold_until(11.7)
        self.play(Write(exponential), run_time=1)
        hold_until(14.9)
        differentials = equation(r"{{du=2x\,dx}},\qquad {{v=e^x}}", y=0.8)
        differential_v = differentials.get_part_by_tex("v=e^x", substring=False)
        differential_v.set_opacity(0)
        self.play(FadeOut(motivation, polynomial, exponential),
                  FadeIn(differentials), run_time=0.4)
        hold_until(17.3)
        self.play(differential_v.animate.set_opacity(1), run_time=0.4)
        hold_until(19.4)

        # Bloco 3: 15,055–27,672 s; fórmula, aplicação e fator constante.
        rule = equation(r"\int u\,dv=uv-\int v\,du", y=-1.4)
        self.play(Write(rule), run_time=0.8)
        hold_until(21)
        applied = equation(r"I=x^2e^x-\int e^x(2x)\,dx", y=2)
        self.play(FadeOut(original, choice, differentials),
                  rule.animate.move_to([0, 4.6, 0]), FadeIn(applied), run_time=0.6)
        hold_until(23.9)
        first = equation(r"I=x^2e^x-2 {{\int xe^x\,dx}}", y=2)
        first.set_color_by_tex(r"\int xe^x\,dx", YELLOW)
        self.play(FadeOut(applied, rule), FadeIn(first), run_time=0.6)
        pending = note("A integral restante\npede partes de novo", y=-0.3)
        self.play(FadeIn(pending),
                  Indicate(first.get_part_by_tex(r"\int xe^x\,dx")), run_time=1)
        hold_until(27.65)

        # Bloco 4: 27,872–33,201 s; queda de grau, nunca uma igualdade x²=x.
        second = equation(r"\int xe^x\,dx", y=2.2, scale=1.2)
        degree = equation(r"\text{grau }2\longrightarrow\text{grau }1", y=-0.1)
        degree.set_color(YELLOW)
        self.play(FadeOut(first, pending), FadeIn(second), run_time=0.4)
        hold_until(29.05)  # "mas o grau caiu de dois para um"
        self.play(FadeIn(degree), run_time=0.4)
        heading = note("Por partes, mais uma vez", y=6.2)
        hold_until(31.3)
        self.play(FadeIn(heading), run_time=0.4)
        hold_until(32.8)

        # Bloco 5: 33,401–42,596 s; segunda aplicação explícita.
        choice2 = equation(r"{{u=x}},\qquad {{dv=e^x\,dx}}", y=2.7)
        choice2_dv = choice2.get_part_by_tex(r"dv=e^x\,dx", substring=False)
        choice2_dv.set_opacity(0)
        diff2 = equation(r"{{du=dx}},\qquad {{v=e^x}}", y=0.9)
        diff2_v = diff2.get_part_by_tex("v=e^x", substring=False)
        diff2_v.set_opacity(0)
        degree2 = equation(r"x\xrightarrow{\text{derivar}}1", y=-1.2)
        degree2.set_color(YELLOW)
        self.play(FadeOut(degree), second.animate.scale(0.8).move_to([0, 4.5, 0]),
                  run_time=0.4)
        hold_until(33.4)
        self.play(FadeIn(choice2), run_time=0.3)
        hold_until(34.45)
        self.play(FadeIn(diff2, degree2), run_time=0.4)
        hold_until(35.55)
        self.play(choice2_dv.animate.set_opacity(1), diff2_v.animate.set_opacity(1),
                  run_time=0.4)
        hold_until(37.2)
        intermediate = equation(r"{{\int xe^x\,dx}} = {{xe^x}} - \int e^x\,dx", y=2)
        self.play(FadeOut(second, choice2, diff2, degree2),
                  FadeIn(intermediate), run_time=0.6)
        hold_until(40.3)
        evaluated = equation(r"{{\int xe^x\,dx}} = {{xe^x}} - e^x", y=2)
        self.play(TransformMatchingTex(intermediate, evaluated), run_time=0.6)
        hold_until(42.1)

        # Bloco 6: 42,796–56,771 s; distribuir, expandir e fatorar.
        recovered = equation(r"I=x^2e^x-2\int xe^x\,dx", y=3)
        self.play(FadeOut(heading), evaluated.animate.scale(0.8).move_to([0, 5.5, 0]),
                  FadeIn(recovered), run_time=0.4)
        hold_until(42.6)
        substituted = equation(r"{{I=}} {{x^2e^x}} {{-2}} (xe^x-e^x) {{+C}}", y=2)
        substituted.set_color_by_tex("-2", YELLOW, substring=False)
        self.play(FadeOut(recovered), FadeIn(substituted), run_time=0.4)
        distribution1 = equation(r"(-2)\cdot(xe^x)=-2xe^x", y=-0.1)
        distribution2 = equation(r"(-2)\cdot(-e^x)=+2e^x", y=-1.5)
        distribution1.set_color(YELLOW)
        distribution2.set_color(TEAL)
        hold_until(44.2)  # "o menos dois distribui nos dois termos"
        self.play(FadeIn(distribution1, distribution2), run_time=0.4)
        hold_until(46.35)  # "Expandindo..."
        expanded = equation(r"{{I=}} {{x^2e^x}} -2xe^x+2e^x {{+C}}", y=2)
        self.play(FadeOut(distribution1, distribution2),
                  TransformMatchingTex(substituted, expanded), run_time=0.4)
        hold_until(48.3)  # "colocando ê elevado a xis em evidência"
        result = equation(r"{{I=}} e^x(x^2-2x+2) {{+C}}", y=2)
        box = SurroundingRectangle(result, color=TEAL, buff=0.25)
        self.play(FadeOut(evaluated), TransformMatchingTex(expanded, result),
                  run_time=3)
        hold_until(52)
        self.play(FadeIn(box), run_time=0.3)
        hold_until(56.5)

        # Bloco 7: 56,971–68,439 s; produto, pares e integrando recuperado.
        verify = note("Conferindo pela derivada", y=6.2)
        function = equation(r"F(x)=e^x(x^2-2x+2)", y=4.6)
        derivative = equation(
            r"\begin{aligned}F'(x)&=e^x(x^2-2x+2)\\&\quad+e^x(2x-2)\end{aligned}",
            y=1.8,
        )
        self.play(FadeOut(result, box), FadeIn(verify, function),
                  run_time=0.5)
        hold_until(59.05)  # "Pela regra do produto..."
        self.play(FadeIn(derivative), run_time=0.4)
        hold_until(60.35)
        factored = equation(
            r"\begin{aligned}F'(x)&=e^x\bigl[ x^2 {{-2x}} {{+2}}"
            r"\\&\qquad\quad {{+2x}} {{-2}} \bigr]\end{aligned}", y=1.8,
        )
        self.play(FadeOut(derivative), FadeIn(factored), run_time=0.5)
        linear_pair = VGroup(*(factored.get_part_by_tex(term, substring=False)
                               for term in ("-2x", "+2x")))
        constant_pair = VGroup(*(factored.get_part_by_tex(term, substring=False)
                                 for term in ("+2", "-2")))
        linear_boxes = VGroup(*(SurroundingRectangle(part, color=YELLOW, buff=0.09)
                                for part in linear_pair))
        constant_boxes = VGroup(*(SurroundingRectangle(part, color=TEAL, buff=0.09)
                                  for part in constant_pair))
        linear_zero = equation(r"-2x+2x=0", y=-0.7).set_color(YELLOW)
        constant_zero = equation(r"2-2=0", y=-2).set_color(TEAL)
        self.play(linear_pair.animate.set_color(YELLOW),
                  FadeIn(linear_boxes, linear_zero), run_time=0.4)
        hold_until(62.45)  # "os constantes também"
        self.play(constant_pair.animate.set_color(TEAL),
                  FadeIn(constant_boxes, constant_zero), run_time=0.4)
        hold_until(63.55)  # "e sobra xis ao quadrado..."
        checked = equation(r"F'(x)=x^2e^x", y=2, scale=1.2)
        final_box = SurroundingRectangle(checked, color=GREEN, buff=0.25)
        check = VGroup(Line([3, 0, 0], [3.15, -0.15, 0]),
                       Line([3.15, -0.15, 0], [3.5, 0.3, 0])).set_color(GREEN)
        final_note = note("Recuperamos o integrando original", y=-0.7)
        self.play(FadeOut(function, factored, linear_boxes, constant_boxes,
                          linear_zero, constant_zero),
                  FadeIn(checked), run_time=0.6)
        hold_until(66.2)  # "exatamente o integrando original"
        self.play(FadeIn(final_box, check, final_note), run_time=0.4)
        # Fala termina em 68,439 s; sobra aproximadamente meio segundo.
        hold_until(69)
