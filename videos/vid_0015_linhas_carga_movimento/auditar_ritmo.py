"""Mede a montagem local sem codificar vídeo; compara blocos com a V3 preservada."""
import ast
import importlib.util
import json
from pathlib import Path
import sys

from manim import tempconfig

UNIT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("cena015_v4", UNIT / "cena.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
rendered = "--renderizado" in sys.argv
if not rendered:
    with tempconfig({"dry_run": True, "pixel_width": 540, "pixel_height": 960,
                     "frame_rate": 15, "media_dir": str(UNIT / "media"),
                     "tex_dir": str(UNIT / "media" / "Tex"),
                     "verbosity": "WARNING"}):
        scene = module.LinhasCarga015(skip_animations=True)
        scene.timing_audit = True
        scene.render()

current = json.loads((UNIT / ("qa_estados_v4.json" if rendered else "qa_ritmo_preflight_v4.json")).read_text(encoding="utf-8"))
current["origem_medicao"] = "render completo" if rendered else "preflight sem codificação"
old = json.loads((UNIT / "qa_estados_v3.json").read_text(encoding="utf-8"))
states = {state["estado"]: state for state in old["estados"]}
ends = [("forcas_coexistindo_abertura",3),("campo_E_d",3),("forca_eletrica",3),
        ("superficie_para_curva",2),("campo_B_d",3),("forca_magnetica",3),
        ("payoff_I_lambda_c",4),("payoff_v_c",4),("razao_final_antes_do_grafico",3),
        ("grafico_beta_0995",1.6)]
boundaries = [0]+[states[name]["tempo_s"]+hold/2 for name,hold in ends]+[old["duracao_cena_s"]]
for i,block in enumerate(current["blocos"]):
    block["duracao_v3_s"] = round(boundaries[i+1]-boundaries[i],3)
    block["duracao_v4_s"] = round(block["fim_s"]-block["inicio_s"],3)
    block["economia_s"] = round(block["duracao_v3_s"]-block["duracao_v4_s"],3)
current["duracao_v3_s"] = old["duracao_cena_s"]
current["economia_total_s"] = round(old["duracao_cena_s"]-current["duracao_cena_s"],3)
def expressions(file):
    tree = ast.parse(file.read_text(encoding="utf-8"))
    return {arg.value for call in ast.walk(tree) if isinstance(call,ast.Call)
            and isinstance(call.func,ast.Name) and call.func.id in ("mt","GlyphEq")
            for arg in call.args if isinstance(arg,ast.Constant) and isinstance(arg.value,str)}
missing = expressions(UNIT / "cena_v3.py")-expressions(UNIT / "cena.py")
assert not missing, f"Expressões da V3 removidas: {missing}"
current["expressoes_V3_preservadas"] = True
old_math = {state["equacao"] for state in old["estados"] if state.get("equacao")}
new_math = {state["equacao"] for state in current["estados"] if state.get("equacao")}
assert old_math <= new_math, f"Passos matemáticos sem estado: {old_math-new_math}"
current["passos_matematicos_preservados"] = len(old_math)
old_holds = {}
tree = ast.parse((UNIT / "cena_v3.py").read_text(encoding="utf-8"))
for node in ast.walk(tree):
    if not isinstance(node,ast.Call) or not isinstance(node.func,ast.Attribute):
        continue
    if node.func.attr == "checkpoint" and node.args and isinstance(node.args[0],ast.Constant):
        name = node.args[0].value
        old_holds[name[3:] if name[:2].isdigit() and name[2:3]=="_" else name] = (
            node.args[1].value if len(node.args)>1 else 2)
    elif node.func.attr == "step" and len(node.args)>2 and isinstance(node.args[2],ast.Constant):
        old_holds[node.args[2].value] = 1.6
for state in old["estados"]:
    if state["estado"].startswith("grafico_") and state["estado"] != "grafico_beta_zero":
        old_holds[state["estado"]] = 1.6
current["waits_v3_s"] = round(sum(old_holds[state["estado"]] for state in old["estados"]),3)
current["waits_v4_s"] = round(sum(beat["duracao_s"] for beat in current["ritmo"] if beat["tipo"]=="wait"),3)
current["maior_wait_v4_s"] = max(beat["duracao_s"] for beat in current["ritmo"] if beat["tipo"]=="wait")
(UNIT / "comparacao_ritmo_v4.json").write_text(json.dumps(current,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"duracao_v3_s":old["duracao_cena_s"],"duracao_v4_s":current["duracao_cena_s"],
                  "blocos":current["blocos"]},ensure_ascii=False,indent=2))
