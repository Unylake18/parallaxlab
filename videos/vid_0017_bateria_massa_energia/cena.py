"""ABSURDO CALCULÁVEL — piloto; cena silenciosa e montagem com voz aprovada.

Render (a partir da raiz):
uv run python -m manim -r 540,960 --fps 15 --media_dir videos/vid_0017_bateria_massa_energia/media_r5 videos/vid_0017_bateria_massa_energia/cena.py BateriaMassaEnergia

Rodada 5: +1 g, contagem de baterias, massa do sistema e energia equivalente
a cerca de 8 h do consumo elétrico médio do município de São Paulo.
Rodada 6: BateriaMassaEnergiaFinal segue sync.json e audio/narracao_final.wav.
uv run python -m manim -r 1080,1920 --fps 30 --media_dir videos/vid_0017_bateria_massa_energia/media_sync videos/vid_0017_bateria_massa_energia/cena.py BateriaMassaEnergiaFinal
Matemática preservada; CTA: Siga o Parallax Lab.
Rodada 7: cabeçalho ABSURDO CALCULÁVEL • EP.01, logo pré-reduzido com
Lanczos e master H.264 4:4:4 com QP 0 (sem perdas de compressão).
Render atual: usar o comando acima com --media_dir videos/vid_0017_bateria_massa_energia/media_r7.
Depois: uv run python videos/vid_0017_bateria_massa_energia/montar_final.py
"""
from contextlib import contextmanager
from PIL.Image import Resampling
from PIL import Image
from manim.renderer.cairo_renderer import CairoRenderer
from manim.scene.scene_file_writer import SceneFileWriter
import json
from pathlib import Path
import sys

import numpy as np
from manim import *
from MF_Tools import TransformByGlyphMap

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from template.config import (
    BACKGROUND_COLOR, TEXT_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, WATERMARK_PATH,
)
from template.fonts import screen_text

UNIT = Path(__file__).resolve().parent
INK, ENERGY, ACCENT = TEXT_COLOR, PRIMARY_COLOR, SECONDARY_COLOR
# Mesmos acentos das unidades 0015/0016; nenhum asset/padrão global alterado.
BLUE, VIOLET, MAGENTA, MUTED = "#267BFF", "#9C8CFF", "#EA63FF", "#ADB8D1"

SOURCE_SP = {
    "instituicao": "SEMIL — Secretaria de Meio Ambiente, Infraestrutura e Logística",
    "titulo": "Anuário de Energéticos por Município 2024 — ano-base 2023",
    "pagina": 8, "municipio": "São Paulo", "consumo_TWh_2023": 26.91,
    "url": "https://smastr16.blob.core.windows.net/home/2025/04/Anuario-de-Energeticos-por-Municipios-do-Estado-de-Sao-Paulo-2024-ano-base-2023.pdf",
}


def verify_physics():
    """QA numérico independente dos números arredondados desenhados em tela."""
    c = 299_792_458
    energy_wh = 3.8 * (4000 / 1000)
    energy_j = energy_wh * 3600
    gram_j = 0.001 * c**2
    gram_wh = gram_j / 3600
    average_gwh_h = SOURCE_SP["consumo_TWh_2023"] * 1000 / 8760
    numbers = {
        "bateria_Wh": energy_wh, "bateria_J": energy_j,
        "bateria_delta_kg": energy_j / c**2,
        "bateria_delta_ng": energy_j / c**2 * 1e12,
        "1g_J": gram_j, "1g_Wh": gram_wh, "1g_GWh": gram_wh / 1e9,
        "baterias": gram_wh / energy_wh, "massa_sistema_kg": gram_wh / 250,
        "SP_media_GWh_h": average_gwh_h,
        "SP_equivalencia_h": gram_wh / 1e9 / average_gwh_h,
    }
    assert abs(energy_wh - 15.2) < 1e-10 and abs(energy_j - 54720) < 1e-6
    assert 0.608 < numbers["bateria_delta_ng"] < 0.610
    assert round(numbers["1g_GWh"]) == 25
    assert round(numbers["baterias"] / 1e9, 1) == 1.6
    assert 99e6 < numbers["massa_sistema_kg"] < 100e6
    assert 3.07 < average_gwh_h < 3.08
    assert 8.12 < numbers["SP_equivalencia_h"] < 8.14
    return numbers


def leave_early(t):
    return smooth(min(1, t / 0.38))


def enter_late(t):
    return smooth(max(0, (t - 0.6) / 0.4))


@contextmanager
def wide_pango():
    """Evita quebra automática do Pango ao gerar os textos em oversampling."""
    pw, ph = config.pixel_width, config.pixel_height
    config.pixel_width = config.pixel_height = 4000
    try:
        yield
    finally:
        config.pixel_width, config.pixel_height = pw, ph


def txt(content, size=30, color=INK, width=7.7):
    with wide_pango():
        lines = [screen_text(line, size, color=color) for line in content.split("\n")]
    mob = lines[0] if len(lines) == 1 else VGroup(*lines).arrange(DOWN, buff=0.17)
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def eq(*parts, size=64, y=0, color=INK, width=7.5):
    mob = MathTex(*parts, font_size=size, color=color)
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob.move_to([0, y, 0])


def frame(mob, color=ENERGY, buff=0.28):
    return SurroundingRectangle(mob, buff=buff, corner_radius=0.13,
                                color=color, stroke_width=2.2)


class GlyphEq:
    """Mapa local por spans; os dois lados do MF-Tools são strings únicas.

    As contagens vêm de partes completas (incluindo frações), após estabilizar
    o LaTeX. Asserções protegem contra mudanças silenciosas no mapa.
    """
    def __init__(self, *parts, size=64, y=0, color=INK, width=7.5):
        chunks = MathTex(*parts, font_size=size)
        self.offsets = np.concatenate([[0], np.cumsum([len(p) for p in chunks])]).astype(int)
        self.mob = eq(" ".join(parts), size=size, y=y, color=color, width=width)
        assert len(self.mob[0]) == int(self.offsets[-1]), parts

    def p(self, i):
        return list(range(int(self.offsets[i]), int(self.offsets[i + 1])))

    def group(self, ids):
        return VGroup(*[self.mob[0][i] for i in ids])

    def color(self, i, color):
        self.group(self.p(i)).set_color(color)
        return self

    def frac(self, i):
        ids = self.p(i)
        bar = max(ids, key=lambda k: self.mob[0][k].width)
        y = self.mob[0][bar].get_y()
        num = sorted([k for k in ids if self.mob[0][k].get_y() > y], key=lambda k: self.mob[0][k].get_x())
        den = sorted([k for k in ids if self.mob[0][k].get_y() < y], key=lambda k: self.mob[0][k].get_x())
        assert len(num) + len(den) + 1 == len(ids)
        return num, [bar], den

    def copy_reference(self, reference):
        first = len(self.mob[0])
        self.mob[0].add(*[g.copy() for g in reference])
        return list(range(first, len(self.mob[0])))


def battery(width=3.3, charged=True):
    """Indicador 2D: a carcaça não muda de geometria com a carga."""
    shell = RoundedRectangle(width=width, height=width * 0.48,
                             corner_radius=width * 0.055, color=BLUE, stroke_width=3)
    cap = RoundedRectangle(width=width * 0.075, height=width * 0.19,
                           corner_radius=width * 0.018, color=INK,
                           fill_color=INK, fill_opacity=1, stroke_width=0)
    cap.next_to(shell, RIGHT, buff=0.025)
    cells = VGroup(*[
        RoundedRectangle(width=width * 0.18, height=width * 0.33,
                         corner_radius=width * 0.025, stroke_width=0,
                         fill_color=ENERGY, fill_opacity=0.9 if charged else 0.06)
        for _ in range(4)
    ]).arrange(RIGHT, buff=width * 0.035).move_to(shell)
    return VGroup(shell, cap, cells)


def skyline(width=7.4):
    """Metrópole simbólica; quatro regiões de janelas acendem em sequência."""
    specs = [(0.54, 1.3), (0.58, 2.0), (0.64, 1.65), (0.52, 2.55),
             (0.62, 1.9), (0.56, 1.45), (0.68, 2.3), (0.5, 1.8),
             (0.6, 2.7), (0.55, 1.65), (0.62, 1.25)]
    total = sum(w for w, h in specs) + 0.07 * (len(specs) - 1)
    x = -total / 2
    outlines = VGroup()
    regions = VGroup(*[VGroup() for _ in range(4)])
    for i, (w, h) in enumerate(specs):
        cx = x + w / 2
        outlines.add(Rectangle(width=w, height=h, color=BLUE, stroke_width=1.8,
                               fill_color=BLUE, fill_opacity=0.1).move_to([cx, h / 2, 0]))
        if i in (1, 3, 8):
            outlines.add(Line([cx, h, 0], [cx, h + 0.22, 0], color=BLUE, stroke_width=1.4))
        columns = 3 if w >= 0.6 else 2
        for wx in np.linspace(cx - w * 0.26, cx + w * 0.26, columns):
            for wy in np.arange(0.26, h - 0.12, 0.32):
                window = Rectangle(width=0.075, height=0.1, stroke_width=0,
                                   fill_color=ENERGY, fill_opacity=0.045)
                window.move_to([wx, wy, 0])
                regions[min(3, i * 4 // len(specs))].add(window)
        x += w + 0.07
    baseline = Line([-total / 2 - 0.05, -0.04, 0], [total / 2 + 0.05, -0.04, 0],
                    color=BLUE, stroke_width=2)
    city = VGroup(outlines, regions, baseline)
    city.scale_to_fit_width(width).move_to(ORIGIN)
    return city


class BateriaMassaEnergia(Scene):
    def construct(self):
        # Cache apenas desta execução; mantém os segmentos para timestamps
        # exatos de QA, sem alterar configuração global do projeto.
        config.max_files_cached = 400
        self.numbers = verify_physics()
        self.camera.background_color = BACKGROUND_COLOR
        self.states = []
        self.transitions = []
        self.blocks = []
        self.setup_identity()
        self.b1_pergunta()
        self.b2_especificacao()
        self.b3_joules()
        self.b4_ponte()
        self.b5_escala()
        self.run_block("caso_1_g", self.caso_um_grama)
        self.run_block("comparacao_SP", self.b9_sao_paulo)
        self.run_block("conclusao_CTA", self.b10_conclusao)
        # Metadados locais de inspeção; não fazem parte da tela nem fixam timing.
        out = Path(config.media_dir) / "estados_preview.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({
            "classe": type(self).__name__, "duracao_provisoria_s": self.time,
            "resolucao": [config.pixel_width, config.pixel_height],
            "fps": config.frame_rate, "estados": self.states,
            "transicoes": self.transitions, "blocos": self.blocks,
            "numeros_verificados": self.numbers, "fonte_SP": SOURCE_SP,
            "partial_files": self.renderer.file_writer.partial_movie_files,
        }, ensure_ascii=False, indent=2), encoding="utf-8")

    def run_block(self, name, action):
        start = self.time
        play_start = self.renderer.num_plays
        action()
        self.blocks.append({"nome": name, "inicio": round(start, 3),
                            "fim": round(self.time, 3), "duracao": round(self.time - start, 3),
                            "play_start": play_start, "play_end": self.renderer.num_plays})

    def caso_um_grama(self):
        self.b6_um_grama()
        self.b7_contagem()
        self.b8_massa_modelo()

    def setup_identity(self):
        rng = np.random.default_rng(17)
        stars = VGroup(*[
            Dot([rng.uniform(-4.35, 4.35), rng.uniform(-7.8, 7.8), 0],
                radius=rng.uniform(0.008, 0.018), color=INK).set_opacity(0.12)
            for _ in range(45)
        ])
        header = txt("ABSURDO CALCULÁVEL • EP.01", 20).set_opacity(0.65)
        header.to_corner(UP + LEFT, buff=0.4)
        self.identity = VGroup(stars, header)
        self.add(self.identity)
        self.fixed = [self.identity]
        if WATERMARK_PATH.exists():
            # Pré-reduzir o original com filtro Lanczos. A transformação de
            # perspectiva do Cairo só admite bicúbico, mesmo sem rotação.
            logo = Image.open(WATERMARK_PATH).convert("RGBA")
            pixels = round(1.8 * config.pixel_width / config.frame_width)
            logo = logo.resize((pixels, round(pixels * logo.height / logo.width)), Resampling.LANCZOS)
            mark = ImageMobject(np.array(logo)).set_width(1.8).set_opacity(0.35)
            mark.to_corner(UP + RIGHT, buff=0.28)
            self.add(mark)
            self.fixed.append(mark)

    def clear_stage(self, keep=()):
        objects = [m for m in self.mobjects if m not in self.fixed and m not in keep]
        if objects:
            self.play(*[FadeOut(m, shift=UP * 0.08) for m in objects], run_time=0.45)

    def title(self, content):
        mob = txt(content, 38).move_to([0, 6.45, 0])
        self.play(FadeIn(mob, shift=DOWN * 0.12), run_time=0.45)
        return mob

    def hold(self, name, seconds=2):
        # Limites do conteúdo editorial; a faixa inferior fica reservada.
        active = [m for m in self.mobjects if m not in self.fixed]
        for m in active:
            assert m.get_left()[0] >= -4.08 and m.get_right()[0] <= 4.08, name
            assert m.get_top()[1] <= 6.9 and m.get_bottom()[1] >= -5.55, name
        self.states.append({"nome": name, "t": round(self.time + seconds / 2, 3),
                            "play_index": self.renderer.num_plays})
        # Quadro real da câmera no estado assentado, sem depender do pequeno
        # desvio temporal de segmentos em cache. Só artefatos locais da unidade.
        out = Path(config.media_dir) / "qa" / "estados"
        out.mkdir(parents=True, exist_ok=True)
        self.camera.reset()
        self.camera.capture_mobjects(self.mobjects)
        self.camera.get_image().save(out / f"{name}.png")
        self.wait(seconds)

    def replace_number(self, old, new, duration=0.7):
        self.play(FadeOut(old, shift=UP * 0.15),
                  FadeIn(new, shift=UP * 0.15), run_time=duration)
        return new

    def motion_mark(self, name, duration, kind):
        self.transitions.append({"nome": name, "t": round(self.time + duration / 2, 3), "tipo": kind,
                                 "play_index": self.renderer.num_plays, "duration": duration})

    def match(self, old, new, name, duration=1, collapse=False, extras=(), **kwargs):
        self.motion_mark(name, duration, "TransformMatchingTex")
        animation = TransformMatchingTex(old, new, **kwargs)
        # O matching continua ao longo de todo o passo. Só os termos distintos
        # saem/entram em fases, sem cruzar números diferentes no mesmo lugar.
        for child in animation.animations:
            if isinstance(child, (FadeOut, FadeIn)):
                child.rate_func = leave_early if isinstance(child, FadeOut) else enter_late
                child.shift_vector = UP * 0.06
                child.point_target = False
                if collapse:
                    child.scale_factor = 0.78 if isinstance(child, FadeOut) else 0.9
                    child.rate_func = (
                        (lambda t: smooth(min(1, t / 0.48))) if isinstance(child, FadeOut)
                        else (lambda t: smooth(max(0, (t - 0.5) / 0.5)))
                    )
        self.play(animation, *extras, run_time=duration)
        return new

    def glyph(self, old, new, name, *maps, extras=(), duration=1.1):
        self.motion_mark(name, duration, "TransformByGlyphMap")
        used_from = {i for entry in maps for i in entry[0]}
        used_to = {i for entry in maps for i in entry[1]}
        leaving = [i for i in range(len(old.mob[0])) if i not in used_from]
        entering = [i for i in range(len(new.mob[0])) if i not in used_to]
        phased_maps = (*maps, (leaving, [], {"rate_func": leave_early}),
                       ([], entering, {"rate_func": enter_late}))
        self.play(TransformByGlyphMap(old.mob, new.mob, *phased_maps,
                                     auto_fade=True, printing=False),
                  *extras, run_time=duration)
        self.remove(old.mob)
        self.add(new.mob)
        return new

    def b1_pergunta(self):
        title = txt("Uma bateria carregada", 38).move_to([0, 6.45, 0])
        hook = txt("PESA MAIS?", 60, MAGENTA).move_to([0, 4.65, 0])
        bat = battery(charged=False).move_to([0, 1.35, 0])
        self.play(FadeIn(title, shift=DOWN * 0.12),
                  FadeIn(hook, shift=DOWN * 0.2), FadeIn(bat), run_time=0.8)
        self.hold("01_pergunta", 2)
        self.motion_mark("carga_em_quatro_etapas", 1.6, "segmentos_e_brilho")
        self.play(LaggedStart(*[
            AnimationGroup(cell.animate.set_fill(opacity=0.9),
                           ShowPassingFlash(cell.copy().set_fill(opacity=0)
                                            .set_stroke(ENERGY, width=6, opacity=0.45),
                                            time_width=0.5))
            for cell in bat[2]
        ], lag_ratio=0.35), run_time=1.6)
        # Pulso só de luz: a carcaça mantém exatamente a mesma geometria.
        self.play(bat[0].animate.set_stroke(ENERGY, width=4.5), run_time=0.2)
        self.play(bat[0].animate.set_stroke(BLUE, width=3), run_time=0.3)
        self.wait(0.35)
        yes = txt("SIM.", 72, ENERGY).move_to([0, -0.65, 0])
        self.play(FadeIn(yes, scale=0.82), run_time=0.55)
        self.wait(0.3)
        precise = txt("Mais precisamente:\na massa total aumenta.", 28).move_to([0, -2.45, 0])
        self.play(FadeIn(precise), run_time=0.5)
        self.hold("02_massa_total", 2.5)
        statement = txt("Uma bateria carregada tem uma\nmassa total ligeiramente maior.",
                        25).move_to([0, -2.45, 0])
        self.replace_number(precise, statement)
        self.hold("03_formulacao", 2.5)

    def b2_especificacao(self):
        self.clear_stage()
        self.title("QUANTA ENERGIA?")
        tag = txt("MODELO FICTÍCIO", 20, VIOLET).move_to([0, 4.85, 0])
        badge = frame(tag, VIOLET, buff=0.16).set_stroke(width=1.3)
        badge.set_fill(VIOLET, opacity=0.05)
        bat = battery(width=2.25).move_to([-2.15, 3.35, 0])
        specs = VGroup(eq("4000", r"\,\mathrm{mAh}", size=42),
                       eq("3{,}8", r"\,\mathrm V", size=42)).arrange(DOWN, buff=0.3)
        specs.move_to([1.4, 3.35, 0])
        specs[1].set_color(VIOLET)
        note = txt("Tensão nominal: aproximação\npara estimar a energia armazenada.", 23)
        note.set_opacity(0.65).move_to([0, -3.85, 0])
        self.play(FadeIn(tag), FadeIn(badge), FadeIn(bat), FadeIn(note), run_time=0.6)
        leaders = VGroup(*[Line(bat.get_right() + RIGHT * 0.08,
                               s.get_left() + LEFT * 0.12, color=BLUE,
                               stroke_width=1.5).set_opacity(0.65) for s in specs])
        self.motion_mark("dados_saindo_da_bateria", 1.1, "rotulos_extraidos")
        self.play(LaggedStart(*[
            AnimationGroup(GrowFromPoint(line, bat.get_right()),
                           FadeIn(s, shift=s.get_center() - bat.get_center()))
            for line, s in zip(leaders, specs)
        ], lag_ratio=0.25), run_time=1.1)
        self.add(specs)
        source = eq("4", "000", r"\,\mathrm{m}", r"\mathrm{Ah}", y=0.65, size=56).set_x(-1.85)
        normalized = eq("4", r"\mathrm{Ah}", size=56, y=0.65).set_x(2.25)
        normalized[1].set_color(VIOLET)
        arrow = Arrow([0.1, 0.65, 0], [0.9, 0.65, 0], buff=0, color=BLUE, tip_length=0.15)
        factor = txt("÷ 1000", 22, VIOLET).move_to([0.5, 1.55, 0])
        self.play(TransformFromCopy(specs[0], source), run_time=0.65)
        working = source.copy()
        self.add(working)
        self.play(FadeIn(factor), GrowArrow(arrow), run_time=0.4)
        self.match(working, normalized, "mAh_para_Ah", path_arc=-PI / 5)
        self.hold("04_mAh_Ah", 2)
        product = eq("E", "=", "3{,}8", r"\,\mathrm V", r"\times", "4", r"\mathrm{Ah}", y=0.65, size=58)
        product[3].set_color(VIOLET)
        product[6].set_color(VIOLET)
        voltage = specs[1].copy()
        self.add(voltage)
        self.motion_mark("convergencia_V_e_Ah", 0.7, "aproximacao_dos_fatores")
        self.play(voltage.animate.move_to([-1.45, 0.65, 0]),
                  normalized.animate.move_to([1.65, 0.65, 0]),
                  FadeOut(source), FadeOut(arrow), FadeOut(factor), FadeOut(leaders), run_time=0.7)
        self.match(Group(voltage, normalized), product, "especificacoes_para_produto", duration=0.8)
        self.play(Indicate(VGroup(*product[2:4]), color=VIOLET, scale_factor=1.06),
                  Indicate(VGroup(*product[5:7]), color=VIOLET, scale_factor=1.06), run_time=0.55)
        self.hold("05_V_Ah", 2)
        result = eq("E", "=", "15{,}2", r"\,\mathrm{Wh}", y=0.65, size=76)
        VGroup(*result[2:]).set_color(ENERGY)
        self.match(product, result, "produto_para_15_2_Wh", duration=1.1, collapse=True)
        box = frame(result, BLUE)
        self.play(Create(box), run_time=0.4)
        self.hold("06_15_2_Wh", 3)
        self.wh_value = result

    def b3_joules(self):
        origin = self.wh_value
        self.clear_stage(keep=(origin,))
        self.title("ESSA ENERGIA, EM JOULES")
        value = eq("15{,}2", r"\,\mathrm{Wh}", size=76, y=3.0, color=ENERGY)
        self.match(origin, value, "Wh_entrada_no_conversor", duration=0.75)
        conversion = eq("1", r"\,\mathrm{Wh}", "=", "3600", r"\,\mathrm J", size=44, y=0.7)
        converter = frame(conversion, VIOLET, buff=0.22).set_fill(VIOLET, opacity=0.04)
        incoming = Arrow([0, 2.25, 0], [0, 1.35, 0], buff=0,
                         color=BLUE, stroke_width=2.5, tip_length=0.14)
        outgoing = Arrow([0, 0.05, 0], [0, -0.85, 0], buff=0,
                         color=BLUE, stroke_width=2.5, tip_length=0.14)
        self.play(GrowArrow(incoming), FadeIn(conversion), Create(converter), run_time=0.65)
        joules = eq(r"54\,720", r"\,\mathrm J", size=85, y=-1.55, color=ENERGY)
        self.motion_mark("conversor_Wh_J", 0.75, "origem_conversor_saida")
        self.play(GrowArrow(outgoing), FadeIn(joules, shift=DOWN * 0.2), run_time=0.75)
        self.hold("06b_conversor_Wh_J", 1.1)
        self.play(FadeOut(value), FadeOut(conversion), FadeOut(converter),
                  FadeOut(incoming), FadeOut(outgoing),
                  joules.animate.move_to([0, 0.6, 0]), run_time=0.6)
        energy_box = frame(joules, BLUE)
        self.play(Create(energy_box), run_time=0.4)
        label = txt("ENERGIA ARMAZENADA", 21, ENERGY).move_to([0, -1.4, 0])
        self.play(FadeIn(label), run_time=0.4)
        self.hold("07_54_720_J", 3)
        self.energy_value = joules
        self.energy_tag = VGroup(joules, energy_box)
        self.add(self.energy_tag)

    def b4_ponte(self):
        energy = self.energy_value
        energy_tag = self.energy_tag
        self.clear_stage(keep=(energy_tag,))
        self.motion_mark("etiqueta_J_alimenta_delta_E", 0.7, "continuidade_da_etiqueta")
        self.play(energy_tag.animate.scale(0.51).move_to([-1.65, 2.4, 0]), run_time=0.7)
        self.title("E QUANTA MASSA?")
        concept = txt("Mais energia interna armazenada\ncorresponde a uma diferença de massa.", 26)
        concept.move_to([0, 3.8, 0])
        condition = txt("Mesma bateria • mesma temperatura\nSem ganho ou perda de matéria", 22)
        condition.set_opacity(0.65).move_to([0, -4.35, 0])
        relation = GlyphEq(r"\Delta E", "=", r"\Delta m", "c^2", size=76, y=0.65)
        relation.color(0, ENERGY).color(3, VIOLET)
        cue = Arrow(energy_tag.get_bottom() + DOWN * 0.12,
                    relation.group(relation.p(0)).get_top() + UP * 0.14, buff=0,
                    color=BLUE, stroke_width=2.5, tip_length=0.13)
        self.play(FadeIn(concept), Write(relation.mob), FadeIn(condition),
                  GrowArrow(cue), run_time=0.9)
        box = frame(relation.mob, VIOLET)
        self.play(Create(box), run_time=0.4)
        self.play(ShowPassingFlash(cue.copy().set_color(ENERGY).set_stroke(width=4),
                                   time_width=0.4), run_time=0.55)
        self.hold("08_relacao_massa_energia", 3)
        solved = GlyphEq(r"\Delta m", "=", r"\frac{\Delta E}{c^2}", size=76, y=0.65)
        num, bar, den = solved.frac(2)
        solved.group(num).set_color(ENERGY)
        solved.group(den).set_color(VIOLET)
        self.glyph(relation, solved, "c_quadrado_para_denominador",
                   (relation.p(0), num, {"path_arc": -PI / 3}),
                   (relation.p(1), solved.p(1)),
                   (relation.p(2), solved.p(0), {"path_arc": -2 * PI / 3}),
                   (relation.p(3), den, {"path_arc": PI / 2}),
                   extras=(FadeOut(box), FadeOut(cue)), duration=1.3)
        speed = eq("c", r"\approx", r"3\times10^8", r"\ \mathrm{m/s}", size=38, y=-1.8, color=VIOLET)
        self.play(FadeIn(speed), run_time=0.4)
        self.hold("09_isolamento", 2)
        sub = GlyphEq(r"\Delta m", r"\approx", r"\frac{54\,720}{(3\times10^8)^2}", size=69, y=0.65)
        snum, sbar, sden = sub.frac(2)
        sub.group(snum).set_color(ENERGY)
        sub.group(sden).set_color(VIOLET)
        ecopy = solved.copy_reference(energy[0])
        ccopy = solved.copy_reference(speed[2])
        assert len(ecopy) == len(snum) == 5
        assert len(ccopy) == len(sden[1:-2]) == 5
        self.glyph(solved, sub, "substituicao_energia_e_c",
                   (solved.p(0), sub.p(0)), (bar, sbar),
                   (ecopy, snum, {"path_arc": -PI / 7}),
                   (ccopy, sden[1:-2], {"path_arc": PI / 7}),
                   ([den[-1]], [sden[-1]]))
        self.hold("10_substituicao", 2.5)
        answer = GlyphEq(r"\Delta m", r"\approx", r"6{,}1\times10^{-13}", r"\ \mathrm{kg}", size=60, y=0.65)
        answer.color(2, ENERGY)
        self.glyph(sub, answer, "avaliacao_massa_kg",
                   (sub.p(0), answer.p(0)), (sub.p(1), answer.p(1)),
                   extras=(FadeOut(speed), FadeOut(energy_tag)))
        self.hold("11_massa_kg", 1.8)
        self.mass_value = answer

    def b5_escala(self):
        old = self.mass_value
        self.clear_stage(keep=(old.mob,))
        self.title("UMA MASSA MINÚSCULA")
        value = GlyphEq(r"6{,}1\times10^{-13}", r"\ \mathrm{kg}", size=58, y=2.8)
        self.glyph(old, value, "massa_para_regua", (old.p(2), value.p(0)),
                   (old.p(3), value.p(1)), duration=0.8)
        positions = np.linspace(-3.1, 3.1, 5)
        labels = VGroup(*[eq(unit, size=46).move_to([x, 0.45, 0])
                           for unit, x in zip([r"\mathrm{kg}", r"\mathrm g", r"\mathrm{mg}", r"\mu\mathrm g", r"\mathrm{ng}"], positions)])
        line = Line([-3.1, -0.15, 0], [3.1, -0.15, 0], color=BLUE, stroke_width=2).set_opacity(0.5)
        ticks = VGroup(*[Line([x, -0.28, 0], [x, -0.02, 0], color=BLUE, stroke_width=2) for x in positions])
        labels[0].set_color(VIOLET)
        self.play(Create(line), FadeIn(labels[0]), FadeIn(ticks[0]), run_time=0.5)
        cursor = Dot([positions[0], -0.15, 0], radius=0.085, color=ENERGY)
        self.add(cursor)
        progress = Line([-3.1, -0.15, 0], [-3.099, -0.15, 0], color=VIOLET, stroke_width=3)
        self.add(progress)
        self.wait(0.3)
        self.motion_mark("regua_construida_kg_ate_ng", 2.2, "rotulos_nascem_na_chegada")
        for i in range(1, 5):
            labels[i].set_color(VIOLET if i < 4 else ENERGY)
            self.play(FadeIn(labels[i], shift=UP * 0.08), FadeIn(ticks[i]),
                      cursor.animate.move_to([positions[i], -0.15, 0]),
                      labels[i-1].animate.set_color(INK).set_opacity(0.45),
                      progress.animate.put_start_and_end_on([-3.1, -0.15, 0], [positions[i], -0.15, 0]),
                      run_time=0.55)
        result = eq(r"\approx", "0{,}6", r"\,\mathrm{ng}", size=108, y=-2.25, color=ENERGY)
        self.motion_mark("regua_para_0_6_ng", 0.9, "copia_da_unidade_e_fade_numerico")
        self.play(FadeOut(value.mob), FadeIn(result[0]), FadeIn(result[1], shift=UP * 0.15),
                  TransformFromCopy(labels[-1], result[2]),
                  labels[-1].animate.set_color(ENERGY), cursor.animate.set_color(MAGENTA), run_time=0.9)
        # Reunir as partes mantém a continuidade entre este payoff e o rehook.
        self.add(result)
        pulse = Circle(radius=0.18, color=MAGENTA, stroke_width=2).move_to(cursor)
        self.play(Create(frame(result, MAGENTA)), FadeOut(pulse, scale=1.8), run_time=0.45)
        self.hold("12_0_6_ng", 4)
        self.nano_value = result

    def b6_um_grama(self):
        old = self.nano_value
        self.clear_stage(keep=(old,))
        self.motion_mark("ng_recua_para_rehook", 0.75, "resultado_vira_contexto")
        self.play(old.animate.scale(0.35).move_to([1.8, 4.65, 0]).set_opacity(0.5), run_time=0.75)
        original = battery(width=1.65).move_to([-1.9, 4.65, 0])
        original_specs = txt("3,8 V · 4000 mAh", 21).move_to([-1.9, 3.8, 0])
        before = self.flow("energia", "massa", y=2.8)
        self.play(FadeIn(before), FadeIn(original), FadeIn(original_specs), run_time=0.45)
        self.wait(0.25)
        hook = txt("E PARA ACRESCENTAR", 35, MAGENTA).move_to([0, 0.9, 0])
        gram = eq(r"1\ \mathrm g", size=118, y=-0.7, color=ENERGY)
        mass_label = txt("À MASSA?", 28).move_to([0, -2.15, 0])
        self.play(FadeIn(hook, shift=UP * 0.16),
                  FadeIn(gram, scale=0.78),
                  FadeIn(mass_label), run_time=0.8)
        self.add(gram)
        # Rótulos fixos; agora massa (à direita) alimenta energia (à esquerda).
        # A inversão da seta é a virada física, sem morph entre palavras.
        self.motion_mark("inversao_massa_energia", 0.85, "seta_inverte_sentido")
        self.play(Rotate(before[1], angle=PI), run_time=0.65)
        self.play(before[1].animate.set_color(VIOLET), run_time=0.2)
        after = before
        self.hold("13_rehook_1_g", 1.2)
        self.play(FadeOut(old), FadeOut(hook), FadeOut(gram), FadeOut(mass_label),
                  FadeOut(original), FadeOut(original_specs), run_time=0.4)
        self.title("PARA ACRESCENTAR 1 g")
        units = eq(r"1\ \mathrm g", "=", r"10^{-3}\ \mathrm{kg}", size=49, y=4.3)
        units[2].set_color(VIOLET)
        relation = eq(r"\Delta E", "=", r"\Delta m", "c^2", size=74, y=0.35)
        relation[3].set_color(VIOLET)
        relation[0].set_color(ENERGY)
        mass_input = Arrow(units[2].get_bottom() + DOWN * 0.12,
                           before[2].get_top() + UP * 0.12, buff=0,
                           color=BLUE, stroke_width=2.5, tip_length=0.13)
        self.play(FadeIn(units), Write(relation), run_time=0.8)
        self.play(GrowArrow(mass_input), run_time=0.35)
        self.hold("14_1_g_kg", 0.6)
        self.play(FadeOut(units), FadeOut(mass_input), run_time=0.3)
        joules = eq(r"\Delta E", r"\approx", r"8{,}99\times10^{13}", r"\ \mathrm J", size=60, y=0.35)
        joules[2].set_color(ENERGY)
        self.match(relation, joules, "energia_para_um_grama", duration=0.9)
        self.hold("15_energia_1_g_J", 0.8)
        factor = eq(r"1\ \mathrm{Wh}=3600\ \mathrm J", size=39, y=-1.6).set_opacity(0.7)
        self.play(FadeIn(factor), run_time=0.35)
        big = eq(r"\approx", "25", r"\ \mathrm{GWh}", size=108, y=0.35, color=ENERGY)
        self.match(joules, big, "25_GWh", duration=0.9)
        self.play(FadeOut(after), FadeOut(factor), run_time=0.4)
        self.play(Create(frame(big, MAGENTA)), run_time=0.4)
        note = txt("Energia para +1 g\nna massa total", 28).move_to([0, -2.3, 0])
        self.play(FadeIn(note), run_time=0.4)
        self.hold("17_25_GWh", 1.4)
        self.gwh_value = big

    def flow(self, left, right, y):
        colors = {"energia": ENERGY, "massa": VIOLET}
        a, b = txt(left, 25, colors[left]), txt(right, 25, colors[right])
        a.move_to([-2, y, 0])
        b.move_to([2, y, 0])
        arrow = Arrow([-0.65, y, 0], [0.65, y, 0], buff=0, color=ENERGY,
                      stroke_width=3, tip_length=0.16)
        return VGroup(a, arrow, b)

    def b7_contagem(self):
        energy = self.gwh_value
        self.clear_stage(keep=(energy,))
        self.title("QUANTAS BATERIAS?")
        self.play(energy.animate.scale(0.46).move_to([0, 4.4, 0]), run_time=0.45)
        hero = battery(width=2.1).move_to([0, 2.5, 0])
        each = eq("15{,}2", r"\,\mathrm{Wh}", size=55, y=1.2, color=ENERGY)
        each_note = txt("por bateria · 3,8 V · 4000 mAh", 23).move_to([0, 0.35, 0])
        division = eq("N", r"\approx", r"\frac{25\times10^9\,\mathrm{Wh}}{15{,}2\,\mathrm{Wh}}",
                      size=56, y=-1.35)
        division[2].set_color(ENERGY)
        self.play(FadeIn(hero), FadeIn(each), FadeIn(each_note), Write(division), run_time=0.75)
        self.hold("18_bateria_15_2_Wh", 0.9)
        self.play(FadeOut(energy), FadeOut(each), FadeOut(each_note), run_time=0.35)
        grid = VGroup(*[battery(width=0.64) for _ in range(48)])
        grid.arrange_in_grid(rows=6, cols=8, buff=(0.16, 0.18)).move_to([0, 3.15, 0])
        symbolic = txt("QUANTIDADE SIMBÓLICA", 17, VIOLET).set_opacity(0.7).move_to([0, 1.3, 0])
        self.play(FadeIn(symbolic), ReplacementTransform(hero, grid[19]), run_time=0.4)
        inner = [19, 20, 27, 28]
        self.motion_mark("contagem_uma_para_quatro", 0.55, "multiplicacao_simbolica")
        self.play(LaggedStart(*[TransformFromCopy(grid[19], grid[i]) for i in inner[1:]],
                             lag_ratio=0.1), run_time=0.55)
        self.hold("19a_quatro_baterias", 0.2)
        middle = [r * 8 + c for r in range(1, 5) for c in range(2, 6)]
        self.motion_mark("contagem_quatro_para_dezesseis", 0.6, "multiplicacao_simbolica")
        self.play(LaggedStart(*[
            TransformFromCopy(grid[min(inner, key=lambda j: np.linalg.norm(grid[j].get_center() - grid[i].get_center()))], grid[i])
            for i in middle if i not in inner
        ], lag_ratio=0.035), run_time=0.6)
        self.hold("19b_dezesseis_baterias", 0.2)
        billion = txt("≈ 1,6 BILHÃO", 53, ENERGY).move_to([0, -0.7, 0])
        kind = txt("de baterias iguais à do exemplo", 27).move_to([0, -1.75, 0])
        purpose = txt("para a energia acrescentar +1 g à massa total", 22, VIOLET).move_to([0, -3.05, 0])
        self.motion_mark("grade_para_1_6_bilhao", 0.75, "grade_amplia_e_payoff")
        self.play(LaggedStart(*[FadeIn(grid[i], shift=DOWN * 0.08) for i in range(48) if i not in middle], lag_ratio=0.018),
                  FadeOut(division, rate_func=leave_early), FadeIn(billion, rate_func=enter_late),
                  FadeIn(kind, rate_func=enter_late), FadeIn(purpose, rate_func=enter_late), run_time=0.75)
        self.add(grid)
        self.hold("20_1_6_bilhao", 2.6)
        self.battery_grid, self.billion_value = grid, billion

    def b8_massa_modelo(self):
        grid, billion = self.battery_grid, self.billion_value
        self.clear_stage(keep=(grid, billion))
        self.title("MASSA DO SISTEMA")
        self.play(grid.animate.scale(0.57).move_to([0, 4.6, 0]),
                  billion.animate.scale(0.5).move_to([0, 3.25, 0]), run_time=0.5)
        tag = txt("HIPÓTESE DO MODELO", 22, VIOLET).move_to([0, 2.15, 0])
        density = eq(r"250\ \mathrm{Wh/kg}", size=55, y=1.2, color=VIOLET)
        badge = frame(VGroup(tag, density), BLUE, buff=0.22)
        self.play(FadeIn(tag), FadeIn(density), Create(badge), run_time=0.55)
        division = GlyphEq("M", "=", r"\frac{25\times10^9\,\mathrm{Wh}}{250\,\mathrm{Wh/kg}}", size=59, y=-0.65)
        num, bar, den = division.frac(2)
        assert len(num) == len(den) == 8
        division.group(num).set_color(ENERGY)
        division.group(den[3:]).set_color(VIOLET)
        explanation = txt("energia total ÷ energia por quilograma", 21).set_opacity(0.7).move_to([0, -2.4, 0])
        outcome = txt("= massa do sistema", 23, VIOLET).move_to([0, -3.1, 0])
        self.play(Write(division.mob), FadeIn(explanation), FadeIn(outcome), run_time=0.7)
        self.hold("21_hipotese_massa", 0.8)
        cancellation = VGroup(*[
            Line(division.group(ids).get_corner(DL) + LEFT * 0.04,
                 division.group(ids).get_corner(UR) + RIGHT * 0.04,
                 color=MAGENTA, stroke_width=2.5) for ids in (num[-2:], den[3:5])
        ])
        self.play(Create(cancellation), run_time=0.3)
        self.wait(0.25)
        million = txt("≈ 100 MILHÕES", 44, ENERGY).move_to([0, -0.65, 0])
        kg = txt("de kg de massa total", 27).move_to([0, -1.75, 0])
        self.motion_mark("divisao_para_100_milhoes_kg", 0.7, "resultado_arredondado")
        self.play(FadeOut(division.mob, rate_func=leave_early), FadeOut(cancellation, rate_func=leave_early),
                  FadeOut(explanation), FadeOut(outcome),
                  FadeIn(million, rate_func=enter_late), FadeIn(kg), run_time=0.7)
        self.hold("22_100_milhoes_kg", 1.0)

    def b9_sao_paulo(self):
        # Recuperar a energia, sem sugerir uma transformação de massa em horas.
        self.clear_stage()
        self.title("MUNICÍPIO DE SÃO PAULO")
        context = txt("A MESMA ENERGIA PARA +1 g", 21, VIOLET).move_to([0, 5.65, 0])
        energy = self.gwh_value.copy().set_opacity(1).set_width(4.2).move_to([0, 4.85, 0])
        city = skyline().move_to([0, 2.55, 0])
        self.motion_mark("25_GWh_para_cidade", 0.75, "energia_como_origem_da_comparacao")
        self.play(FadeIn(energy, shift=UP * 0.15), FadeIn(city), FadeIn(context), run_time=0.75)
        time = eq("0", r"\,\mathrm h", size=90, y=-0.3, color=VIOLET)
        description = txt("do consumo elétrico médio\ndo município de São Paulo", 29).move_to([0, -2.05, 0])
        base = txt("base: consumo municipal de 2023", 21, VIOLET).move_to([0, -3.35, 0])
        purpose = txt("Energia para acrescentar +1 g à massa", 23).move_to([0, -4.4, 0])
        self.play(FadeIn(time), FadeIn(description), FadeIn(base), FadeIn(purpose), run_time=0.5)
        self.hold("23_skyline_SP_0_h", 0.5)
        self.play(energy.animate.scale(0.72).set_opacity(0.8), run_time=0.35)
        for i, hours in enumerate((2, 4, 6, 8)):
            new = eq(str(hours), r"\,\mathrm h", size=90, y=-0.3, color=ENERGY)
            self.match(time, new, f"SP_{hours}_h", duration=0.6,
                       extras=(city[1][i].animate.set_fill(opacity=0.88),))
            time = new
        payoff = txt("≈ 8 HORAS", 58, ENERGY).move_to([0, -0.3, 0])
        self.play(FadeOut(time, rate_func=leave_early),
                  FadeIn(payoff, rate_func=enter_late), run_time=0.45)
        self.hold("24_8_horas_SP", 3.2)
        self.city_value = city

    def b10_conclusao(self):
        city = self.city_value
        self.clear_stage(keep=(city,))
        self.title("UMA BATERIA CARREGADA")
        hook = txt("PESA MAIS?", 53, MAGENTA).move_to([0, 4.85, 0])
        bat = battery(width=2.45).move_to([0, 2.95, 0])
        specs = txt("3,8 V · 4000 mAh", 25).move_to([0, 1.7, 0])
        self.motion_mark("cidade_recua_bateria_original", 0.65, "retorno_ao_exemplo")
        self.play(FadeOut(city, scale=0.12, rate_func=leave_early),
                  FadeIn(bat, scale=0.8, rate_func=enter_late), FadeIn(hook),
                  FadeIn(specs, rate_func=enter_late), run_time=0.65)
        yes = txt("SIM.", 67, ENERGY).move_to([0, 0.3, 0])
        statement = txt("MAS QUASE NADA.", 32).move_to([0, -0.8, 0])
        nano = eq("+", r"\approx", "0{,}6", r"\,\mathrm{ng}", size=80, y=-2.0, color=ENERGY)
        nano[0].set_color(MAGENTA)
        each = txt("por carga completa do exemplo", 21, VIOLET).move_to([0, -3.0, 0])
        self.play(FadeIn(yes, scale=0.85), run_time=0.45)
        self.play(FadeIn(statement), FadeIn(nano), FadeIn(each), run_time=0.5)
        self.hold("25_retorno_0_6_ng", 2.0)
        recap = txt("Tudo aquilo para acrescentar 1 g.", 23, VIOLET).move_to([0, -3.75, 0])
        self.play(FadeIn(recap), run_time=0.35)
        self.wait(0.6)
        cta = VGroup(txt("Siga o Parallax Lab", 29), txt("@labparallax", 34, ENERGY)).arrange(DOWN, buff=0.2)
        cta.move_to([0, -4.85, 0])
        self.play(FadeIn(cta), run_time=0.35)
        self.hold("26_CTA", 1.6)


class EscritorMasterSemPerdas(SceneFileWriter):
    """Qualidade restrita a esta unidade; não altera Manim nem o template."""
    def open_partial_movie_stream(self, file_path=None):
        super().open_partial_movie_stream(file_path)
        stream = self._current_encode_job.stream
        # O encoder ainda aguarda o primeiro quadro. Chroma integral preserva
        # detalhes coloridos; CRF 0 evita perdas de compressão no master.
        stream.pix_fmt = "yuv444p"
        stream.options = {"an": "1", "crf": "0", "preset": "medium"}


class BateriaMassaEnergiaFinal(BateriaMassaEnergia):
    """Montagem guiada pelo WAV aprovado; a cena silenciosa continua disponível.

    sync.json registra os instantes medidos e a agenda dos plays. Quantizar
    limites absolutos evita acumular arredondamentos entre 15 e 30 fps.
    """
    def __init__(self, renderer=None, **kwargs):
        renderer = renderer or CairoRenderer(file_writer_class=EscritorMasterSemPerdas)
        super().__init__(renderer=renderer, **kwargs)

    def construct(self):
        self.sync = json.loads((UNIT / "sync.json").read_text(encoding="utf-8"))
        self.agenda = self.sync["agenda"]
        self.cue_index = 0
        self.executed = []
        self.add_sound(str(UNIT / "audio" / "narracao_final.wav"),
                       time_offset=self.sync["audio_offset_s"])
        super().construct()
        assert self.cue_index == len(self.agenda), "Agenda diferente da cena"
        out = Path(config.media_dir) / "estados_preview.json"
        data = json.loads(out.read_text(encoding="utf-8"))
        data["sincronizacao"] = {"audio_offset_s": self.sync["audio_offset_s"],
            "audio_s": self.sync["audio_s"], "metodo": self.sync["metodo"],
            "agenda": self.agenda, "execucao": self.executed}
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def planned_duration(self):
        item = self.agenda[self.cue_index]
        fps = config.frame_rate
        return (round(item["fim"] * fps) - round(item["inicio"] * fps)) / fps

    def play(self, *animations, **kwargs):
        item = self.agenda[self.cue_index]
        total = self.planned_duration()
        waiting = len(animations) == 1 and isinstance(animations[0], Wait)
        duration = total if waiting else min(total, item["animacao_max_s"])
        fps = config.frame_rate
        count = max(1, round(duration * fps))
        duration = count / fps
        if waiting and int(duration / (1 / fps)) < count:
            # Cairo congela Wait com int(duration / dt): um float abaixo
            # do inteiro perde um quadro. Só a pausa recebe este ajuste.
            duration = float(np.nextafter(duration, np.inf))
        self.executed.append({"cue": self.cue_index, "play_index": self.renderer.num_plays,
                              "duracao_animacao": duration, "duracao_total": total})
        self.cue_index += 1
        kwargs["run_time"] = duration
        result = super().play(*animations, **kwargs)
        # Sobras viram permanência do estado pronto, sem deixar uma entrada
        # ou transformação curta se arrastar durante a explicação da voz.
        remainder_count = round(total * fps) - count
        if remainder_count > 0:
            remainder = remainder_count / fps
            if int(remainder / (1 / fps)) < remainder_count:
                remainder = float(np.nextafter(remainder, np.inf))
            Scene.play(self, Wait(remainder))
        return result

    def motion_mark(self, name, duration, kind):
        item = self.agenda[self.cue_index]
        super().motion_mark(name, min(self.planned_duration(), item["animacao_max_s"]), kind)

    def b10_conclusao(self):
        # A voz primeiro volta à bateria/0,6 ng; só depois repete a pergunta
        # e responde. Mantém a matemática e dá a cada fala seu próprio estado.
        city = self.city_value
        self.clear_stage(keep=(city,))
        self.title("UMA BATERIA CARREGADA")
        bat = battery(width=2.45).move_to([0, 2.95, 0])
        specs = txt("3,8 V · 4000 mAh", 25).move_to([0, 1.7, 0])
        nano = eq("+", r"\approx", "0{,}6", r"\,\mathrm{ng}", size=80, y=-2, color=ENERGY)
        nano[0].set_color(MAGENTA)
        each = txt("por carga completa do exemplo", 21, VIOLET).move_to([0, -3, 0])
        self.motion_mark("cidade_recua_bateria_original", 0.55, "retorno_ao_exemplo")
        self.play(FadeOut(city, scale=0.12, rate_func=leave_early),
                  FadeIn(bat, scale=0.8, rate_func=enter_late),
                  FadeIn(specs, rate_func=enter_late), FadeIn(nano, rate_func=enter_late),
                  FadeIn(each, rate_func=enter_late))
        self.hold("25_retorno_0_6_ng", 4)
        hook = txt("PESA MAIS?", 53, MAGENTA).move_to([0, 4.85, 0])
        self.play(FadeIn(hook))
        self.wait(2)
        yes = txt("SIM.", 67, ENERGY).move_to([0, 0.3, 0])
        statement = txt("MAS QUASE NADA.", 32).move_to([0, -0.8, 0])
        self.play(FadeIn(yes, scale=0.85))
        self.play(FadeIn(statement))
        self.wait(0.5)
        cta = VGroup(txt("Siga o Parallax Lab", 29), txt("@labparallax", 34, ENERGY)).arrange(DOWN, buff=0.2)
        # Duas linhas de legenda começam abaixo de y ≈ −4,87; conservar
        # distância também da máscara, que ultrapassa o texto alguns pixels.
        cta.move_to([0, -4.15, 0])
        self.play(FadeIn(cta))
        self.hold("26_CTA", 2)
