"""Aplica os complementos escolhidos (audio/compl_plano.json): regrava só esses parágrafos e emenda no WAV contínuo (sem silêncio inserido
além do respiro natural entre parágrafos). Chave só em ELEVENLABS_API_KEY."""
import json, os, re, shutil, sys, wave
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "videos"))
import gerar_voz_elevenlabs as g

AQUI = Path(__file__).resolve().parent
VOZ = "qw7jgPZWOKrl10GsjQ82"
SR = 44100
plano = json.loads((AQUI / "audio" / "compl_plano.json").read_text(encoding="utf-8"))
comp = dict(json.loads((AQUI / "complemento_v3.json").read_text(encoding="utf-8")))
alin = json.loads((AQUI / "alinhamento_palavras.json").read_text(encoding="utf-8"))
ordem = json.loads((AQUI / "ancoras_v1_nominal.json").read_text(encoding="utf-8"))["ordem"]
escolhidos = plano["escolhidos"]

# 1) texto: complemento no fim do parágrafo (mesma tag) — fonte única narracao_final_fonte.md
fonte = (AQUI / "narracao_final_fonte.md").read_text(encoding="utf-8")
if not (AQUI / "narracao_final_fonte_sem_compl.md").exists():
    (AQUI / "narracao_final_fonte_sem_compl.md").write_text(fonte, encoding="utf-8")
paras = {m.group(1): m.group(2).strip() for m in re.finditer(r"^\{([^}]+)\} (.+)$", fonte, flags=re.M)}
novo = {}
for a in escolhidos:
    novo[a] = paras[a] if comp[a] in paras[a] else paras[a] + " " + comp[a]
    fonte = fonte.replace("{%s} %s" % (a, paras[a]), "{%s} %s" % (a, novo[a]))
(AQUI / "narracao_final_fonte.md").write_text(fonte, encoding="utf-8")

# 2) regrava os parágrafos alterados (um a um)
if not os.environ.get("ELEVENLABS_API_KEY"):
    sys.exit("defina ELEVENLABS_API_KEY")
chave = os.environ["ELEVENLABS_API_KEY"]
(AQUI / "audio" / "compl").mkdir(exist_ok=True)
novos = {}
for a in escolhidos:
    arq = AQUI / "audio" / "compl" / f"{a}.wav"
    if not arq.exists():
        print("gera", a, flush=True)
        pcm = g.decodificar_mp3(g.sintetizar(chave, VOZ, "eleven_v4", "mp3_44100_192", novo[a], "", "", None))
        with wave.open(str(arq), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm)
    with wave.open(str(arq)) as w:
        novos[a] = np.frombuffer(w.readframes(w.getnframes()), np.int16)

# 3) emenda: cortes no ponto mais silencioso entre o fim de uma âncora e o início da seguinte
vel = AQUI / "audio" / "narracao_v3.wav"
bak = AQUI / "audio" / "narracao_v3_semcompl.wav"
if not bak.exists():
    shutil.copy(vel, bak)
with wave.open(str(bak)) as w:
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16)
ini, fim = {}, {}
for w_ in alin:
    ini.setdefault(w_["aid"], w_["start"]); fim[w_["aid"]] = w_["end"]


def corte(a_prev, a_next):
    lo, hi = int(fim[a_prev] * SR), int(ini[a_next] * SR)
    if hi - lo < int(0.06 * SR):
        return (lo + hi) // 2
    j = int(0.02 * SR)
    seg = np.abs(x[lo:hi].astype(np.float32))
    c = np.convolve(seg, np.ones(j) / j, mode="valid")
    return lo + int(np.argmin(c)) + j // 2


cortes = [0] + [corte(ordem[k - 1], ordem[k]) for k in range(1, len(ordem))] + [len(x)]


def apara(y, lim=300):
    idx = np.where(np.abs(y) > lim)[0]
    return y[idx[0]: idx[-1] + 1] if len(idx) else y


pad = np.zeros(int(0.30 * SR), np.int16)
saida = []
antes = {}
for k, a in enumerate(ordem):
    seg = x[cortes[k]: cortes[k + 1]]
    if a in novos:
        n_ = np.concatenate([pad, apara(novos[a]), pad])
        antes[a] = [len(seg) / SR, len(n_) / SR]
        seg = n_
    saida.append(seg)
y = np.concatenate(saida)
with wave.open(str(vel), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.tobytes())
print(f"narracao_v3.wav {len(y) / SR:.1f} s (antes {len(x) / SR:.1f} s)")
for a, (b, d) in antes.items():
    print(f"  {a}: segmento {b:.1f} s -> {d:.1f} s")
json.dump(antes, open(AQUI / "audio" / "compl_resultado.json", "w"), indent=1)
