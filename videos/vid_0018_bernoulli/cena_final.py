"""Montagem do vid_0018 guiada pelo WAV recebido; V5 silenciosa preservada."""
import json
import sys
from pathlib import Path

import numpy as np
from manim import *
from manim.renderer.cairo_renderer import CairoRenderer
from manim.scene.scene_file_writer import SceneFileWriter

UNIT = Path(__file__).resolve().parent
sys.path.insert(0, str(UNIT))
import cena as base

# Somente o título/CTA desta montagem seguem a fala recebida.
original_text = base.text
def final_text(content, *args, **kwargs):
    if content == "Segue o Parallax Lab / @labparallax":
        content = "Siga o Parallax Lab"
    return original_text(content, *args, **kwargs)
base.text = final_text


class BernoulliMontagem(base.BernoulliV5):
    native_mode = False
    timeline_filename = "tempos_final.json"

    def phase(self, content):
        if content == "O trabalho muda a energia mecânica":
            self.energy_phases += 1
            if self.energy_phases == 1:
                content = "Da entrada à saída"
        self.events.append({"tipo": "fase", "nome": content, "cue": len(self.executed), "tempo": self.time})
        return super().phase(content)

    def record(self, name, hold=1.5):
        start, cue_index = self.time, len(self.executed)
        self.events.append({"tipo": "estado", "nome": name, "cue": len(self.executed), "tempo": self.time})
        super().record(name, hold)
        if not self.native_mode:
            self.marks[name] = start + min(.15, (self.executed[cue_index]["fim"] - start) / 2)
        if name == "unidades":
            # A fala recebida interpreta pressão depois de explicar as unidades.
            self.events.append({"tipo": "extra", "nome": "pressao_apos_unidades", "cue": len(self.executed), "tempo": self.time})
            caption = base.note("Trabalho das forças de pressão\npor unidade de volume", 26, base.PRESSURE, y=-3.85)
            self.play(FadeIn(caption), Indicate(self.current.term("P"), color=base.PRESSURE), run_time=.6)
            self.wait(1.5)
            self.play(FadeOut(caption), run_time=.3)

    def glyph(self, *args, **kwargs):
        start, cue_index = self.time, len(self.executed)
        super().glyph(*args, **kwargs)
        if not self.native_mode:
            self.marks[f"morph_{len(self.glyph_steps):02d}_meio"] = start + self.executed[cue_index]["animacao_s"] / 2

    def construct(self):
        self.executed, self.events, self.energy_phases = [], [], 0
        self.processed_marks = set()
        if not self.native_mode:
            self.sync = json.loads((UNIT / "sync.json").read_text(encoding="utf-8"))
            self.agenda = self.sync["agenda"]
            self.add_sound(str(UNIT / "audio/narracao_final.wav"), time_offset=self.sync["audio_offset_s"])
        super().construct()
        if not self.native_mode:
            assert len(self.executed) == len(self.agenda)
        (UNIT / ("native.json" if self.native_mode else "execucao_final.json")).write_text(
            json.dumps({"cues": self.executed, "eventos": self.events, "duracao_s": self.time,
                        "resolucao": [config.pixel_width, config.pixel_height], "fps": config.frame_rate},
                       ensure_ascii=False, indent=2), encoding="utf-8")

    def play(self, *animations, **kwargs):
        waiting = len(animations) == 1 and isinstance(animations[0], Wait)
        index, start = len(self.executed), self.time
        if self.native_mode:
            result = super().play(*animations, **kwargs)
            self.executed.append({"indice": index, "inicio": start, "fim": self.time,
                                  "pausa": waiting, "nativo": self.time - start})
            return result
        item = self.agenda[index]
        pending = [(name, at) for name, at in getattr(self, "marks", {}).items()
                   if name not in self.processed_marks]
        nominal = kwargs["run_time"] if "run_time" in kwargs else (animations[0].run_time if waiting else 1.0)
        fps = config.frame_rate
        total_frames = round(item["fim"] * fps) - round(item["inicio"] * fps)
        count = total_frames if waiting else min(total_frames, max(1, round(item["animacao_max_s"] * fps)))
        # Cairo usa arange(0, duração, dt): o extremo fica estritamente fora.
        duration = (count - 1e-7) / fps
        if waiting:
            animations[0].is_static_wait = False
        kwargs["run_time"] = duration
        result = super().play(*animations, **kwargs)
        for name, at in pending:
            if at > start:
                self.marks[name] = start + min(1.0, (at - start) / nominal) * count / fps
            self.processed_marks.add(name)
        remainder = total_frames - count
        if remainder:
            Scene.play(self, Wait((remainder - 1e-7) / fps, frozen_frame=False))
        self.executed.append({"indice": index, "inicio": start, "fim": self.time,
                              "pausa": waiting, "animacao_s": count / fps})
        return result


class BernoulliMedir(BernoulliMontagem):
    native_mode = True
    timeline_filename = "tempos_native.json"


class EscritorSemPerdas(SceneFileWriter):
    def open_partial_movie_stream(self, file_path=None):
        super().open_partial_movie_stream(file_path)
        stream = self._current_encode_job.stream
        stream.pix_fmt = "yuv444p"
        stream.options = {"an": "1", "crf": "0", "preset": "medium"}


class BernoulliFinal(BernoulliMontagem):
    def __init__(self, renderer=None, **kwargs):
        renderer = renderer or CairoRenderer(file_writer_class=EscritorSemPerdas)
        super().__init__(renderer=renderer, **kwargs)
