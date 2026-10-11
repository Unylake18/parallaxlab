"""Render nativo sincronizado: movimentos próprios e pausas de leitura separadas."""
import json
from pathlib import Path
import sys

from manim import Wait, config
import numpy as np

UNIT = Path(__file__).resolve().parent
sys.path.insert(0, str(UNIT))
from cena import IntegralDuplaVolume020

PLAN = UNIT / "timing_final.json"


class PlanejarIntegral020(IntegralDuplaVolume020):
    def construct(self):
        self.operations = []
        self.boundaries = {}
        super().construct()
        destination = Path(config.media_dir) / "operacoes_originais.json"
        destination.write_text(json.dumps({"operations": self.operations, "boundaries": self.boundaries}, indent=2), encoding="utf-8")

    def play(self, *args, **kwargs):
        start = self.time
        super().play(*args, **kwargs)
        self.operations.append(dict(index=len(self.operations), start=start, end=self.time,
                                    duration=self.time - start, pause=len(args) == 1 and isinstance(args[0], Wait),
                                    types=[type(arg).__name__ for arg in args]))

    def mark(self, name):
        self.boundaries[name] = len(self.operations)
        super().mark(name)


class IntegralDuplaVolume020Final(IntegralDuplaVolume020):
    def setup(self):
        super().setup()
        from legenda_final import NativeCaptions
        captions = NativeCaptions(config.pixel_width, config.pixel_height, config.frame_rate)
        writer = self.renderer.file_writer
        original_open, original_write = writer.open_partial_movie_stream, writer.write_frame

        def high_quality(*args, **kwargs):
            original_open(*args, **kwargs)
            # O trabalhador aguarda o primeiro quadro; o codec ainda não foi aberto.
            stream = writer._current_encode_job.stream
            stream.codec_context.options = {**stream.codec_context.options, "crf": "15", "preset": "medium"}

        def captioned(frame, num_frames=1):
            if isinstance(frame, np.ndarray):
                start = round(self.renderer.time * config.frame_rate) - num_frames
                for decorated, count in captions.batches(frame, start, num_frames):
                    original_write(decorated, num_frames=count)
            else:
                original_write(frame, num_frames=num_frames)

        writer.open_partial_movie_stream, writer.write_frame = high_quality, captioned

    def construct(self):
        self.schedule = json.loads(PLAN.read_text(encoding="utf-8"))
        assert config.frame_rate == self.schedule["fps"]
        self.operation_index = 0
        self.pending_frames = 0
        self.actual_operations = []
        super().construct()
        self._flush()
        assert self.operation_index == len(self.schedule["operations"])
        self._pause(self.schedule["tail_frames"])
        assert abs(self.time - self.schedule["total_frames"] / config.frame_rate) < 1e-6
        (Path(config.media_dir) / "operacoes_renderizadas.json").write_text(json.dumps(self.actual_operations, indent=2), encoding="utf-8")

    def _pause(self, frames):
        if frames:
            # Margem fracionária evita floor de 20 quadros virar 19 por arredondamento.
            duration = (frames + 0.001) / config.frame_rate
            start = self.time
            super().play(Wait(run_time=duration, frozen_frame=True))
            expected = start + frames / config.frame_rate
            if self.renderer.skip_animations:
                self.renderer.time = expected
            assert abs(self.time - expected) < 1e-6

    def _flush(self):
        frames, self.pending_frames = self.pending_frames, 0
        self._pause(frames)

    def play(self, *args, **kwargs):
        if self.operation_index == 0:
            self._pause(self.schedule["lead_frames"])
        self._flush()
        operation = self.schedule["operations"][self.operation_index]
        pause = len(args) == 1 and isinstance(args[0], Wait)
        assert pause == operation["pause"], self.operation_index
        start = self.time
        if pause:
            self._pause(operation["frames"])
        else:
            kwargs["run_time"] = (operation["frames"] - 0.001) / config.frame_rate
            super().play(*args, **kwargs)
            expected = start + operation["frames"] / config.frame_rate
            if self.renderer.skip_animations:
                self.renderer.time = expected
            assert abs(self.time - expected) < 1e-6
        self.actual_operations.append(dict(index=self.operation_index, start=start, end=self.time,
                                           pause=pause, frames=operation["frames"], types=operation["types"]))
        self.pending_frames = operation["hold_after"]
        self.operation_index += 1

    def mark(self, name):
        self._flush()
        super().mark(name)
