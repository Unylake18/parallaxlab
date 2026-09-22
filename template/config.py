from pathlib import Path

from manim import config

config.frame_width = 9
config.frame_height = 16

BACKGROUND_COLOR = "#050816"
TEXT_COLOR = "#F5F7FF"
PRIMARY_COLOR = "#35D9FF"
SECONDARY_COLOR = "#745CFF"

WATERMARK_PATH = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "branding"
    / "overlays"
    / "parallax_lab_watermark.png"
)
