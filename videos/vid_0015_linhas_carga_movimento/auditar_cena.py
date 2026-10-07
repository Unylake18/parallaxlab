"""Auditoria localizada de tipografia e spans LaTeX antes do preview V4."""
import ast
import importlib.util
import json
from pathlib import Path

from manim import tempconfig

UNIT = Path(__file__).resolve().parent
source = UNIT / "cena.py"
tree = ast.parse(source.read_text(encoding="utf-8"))
calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
direct = [node.lineno for node in calls if isinstance(node.func, ast.Name)
          and node.func.id in {"Text", "MarkupText", "Paragraph"}]
assert not direct, f"Textos fora do helper oficial: {direct}"
assert not any(isinstance(node, ast.Constant) and isinstance(node.value, str)
               and r"\text{" in node.value for node in ast.walk(tree)), "Texto de tela em MathTex"
spec = importlib.util.spec_from_file_location("cena015_v4", source)
scene = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scene)
audit = {"fonte_texto_tela": "Space Grotesk Medium via template.fonts.screen_text",
         "construtores_textuais_diretos": direct, "texto_em_MathTex": False,
         "matematica": "MathTex; DecimalNumber para valores numéricos", "spans_verificados": []}
with tempconfig({"media_dir": str(UNIT / "media_preflight_v4"),
                 "tex_dir": str(UNIT / "media_preflight_v4" / "Tex")}):
    for node in calls:
        if not isinstance(node.func, ast.Name) or node.func.id != "GlyphEq":
            continue
        parts = [ast.literal_eval(arg) for arg in node.args]
        kwargs = {kw.arg: getattr(scene, kw.value.id) if isinstance(kw.value, ast.Name)
                  else ast.literal_eval(kw.value) for kw in node.keywords}
        equation = scene.GlyphEq(*parts, **kwargs)
        audit["spans_verificados"].append({"linha": node.lineno, "tex": " ".join(parts),
                                          "glifos": len(equation.mob[0])})
        if parts[-1].startswith((r"\frac{\frac",r"\dfrac{\dfrac")):
            (un,ub,ud),(dn,db,dd),outer = equation.nested_frac(len(parts)-1)
            assert (len(un),len(ud),len(dn),len(dd)) == (4,3,2,5)
    sample = scene.text("Título · rótulo · nota", 28)
    assert sample.font == "Space Grotesk"
audit["fonte_runtime"] = sample.font
(UNIT / "auditoria_v4.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Tipografia oficial conferida; {len(audit['spans_verificados'])} expressões MF-Tools verificadas.")
