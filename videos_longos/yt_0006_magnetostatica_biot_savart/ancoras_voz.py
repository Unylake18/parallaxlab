"""yt_0006 — liga cada unidade da narração (N001..N083) ao evento da cena que ela descreve e grava ancoras.json.

  uv run --no-sync python videos_longos/yt_0006_magnetostatica_biot_savart/ancoras_voz.py

Entradas:
  sync.json              instante de início de cada unidade na voz (sync_voz.py)
  eventos_sync.jsonl     eventos da cena no tempo editorial (cada legenda, fórmula, nome de lei, seção; gerado com QA_EVENTS na passada a seco)
  eventos_calibrados.tsv os mesmos eventos no tempo do preview v4 (para casar com os tempos de referência do roteiro)
  narracao_fonte_24min_gpt.md  cabeçalhos "### N001 | 00:00 | ..." = tempo do preview em que cada unidade deve começar
Saída: ancoras.json  [{unidade, e (tempo editorial), v (tempo na voz), evento, tipo}], estritamente crescentes em e e em v.

A fala começa LEAD s depois do evento? Não: o evento é disparado LEAD s antes de a primeira palavra soar (a imagem aparece
junto da fala, sem a voz esperar por ela).
"""
import json
import re
from pathlib import Path

PASTA = Path(__file__).resolve().parent
RENDERS = PASTA / "renders"
LEAD = 0.10                      # o evento começa 0,10 s antes da primeira palavra da unidade
JANELA = (-3.0, 3.5)             # tolerância em torno do tempo de referência do preview (s)
PREFERENCIA = {"legenda": 0, "section": 0, "caption": 1, "eq": 2, "eq-aux": 3, "name": 4, "cta": 0}


def mm_ss(t):
    a, b = t.split(":")
    return int(a) * 60 + float(b)


def main():
    sync = json.load(open(PASTA / "sync.json", encoding="utf-8"))
    onset = {c["chave"]: c["onset"] for c in sync["celulas"]}
    ev = [json.loads(l) for l in open(PASTA / "eventos_sync.jsonl", encoding="utf-8")]
    # tempo do preview de cada evento: a tabela calibrada (330 linhas) tem os mesmos eventos na mesma ordem; o CTA é novo
    cal = [l.rstrip("\n").split("\t") for l in open(RENDERS / "eventos_calibrados.tsv", encoding="utf-8").read().strip().split("\n")]
    prev, j = [], 0
    for e in ev:
        if e["kind"] == "cta":
            prev.append(mm_ss("17:24.0"))
            continue
        assert cal[j][1] == e["kind"], f"sequência de eventos diferente da tabela calibrada em {j}: {e} x {cal[j]}"
        prev.append(mm_ss(cal[j][0]))
        j += 1
    assert j == len(cal), (j, len(cal))
    # evento sintético: o aviso de notação da espira entra 1,95 s depois da legenda "A corrente I percorre a espira"
    # (0,45 s de entrada da legenda + 1,5 s de espera, ver intervalos 599–601 de intervalos.jsonl)
    c = next(i for i, e in enumerate(ev) if e["kind"] == "caption" and "percorre a espira" in e["text"])
    ev.append({"t": round(ev[c]["t"] + 1.95, 2), "kind": "legenda", "text": "Na espira, a notação muda (R, s, z)"})
    prev.append(mm_ss("11:58.0"))
    ordem = sorted(range(len(ev)), key=lambda i: ev[i]["t"])
    ev, prev = [ev[i] for i in ordem], [prev[i] for i in ordem]
    unidades = re.findall(r"### (N\d{3}) \| (\d\d:\d\d) \|", (PASTA / "narracao_fonte_24min_gpt.md").read_text(encoding="utf-8"))
    out, e_ant, v_ant = [], -1.0, -1.0
    for n, tm in unidades:
        th = mm_ss(tm)
        cand = [i for i, (e, p) in enumerate(zip(ev, prev))
                if e["kind"] in PREFERENCIA and th + JANELA[0] <= p <= th + JANELA[1] and e["t"] > e_ant + 1e-6]
        if not cand:
            raise SystemExit(f"{n}: nenhum evento perto de {tm}")
        i = min(cand, key=lambda k: (abs(prev[k] - th) + 0.9 * PREFERENCIA[ev[k]["kind"]], k))
        v = max(0.0, onset[n] - LEAD)
        if v <= v_ant + 0.05:
            v = v_ant + 0.05
        out.append({"unidade": n, "e": ev[i]["t"], "v": round(v, 3), "evento": ev[i]["text"][:80], "tipo": ev[i]["kind"],
                    "ref_preview": th})
        e_ant, v_ant = ev[i]["t"], v
    json.dump(out, open(PASTA / "ancoras.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(out)} âncoras; e: {out[0]['e']}–{out[-1]['e']} s; v: {out[0]['v']}–{out[-1]['v']} s")
    for a in out:
        print(f"{a['unidade']} ref {a['ref_preview']:7.1f} e={a['e']:8.2f} v={a['v']:8.2f} {a['tipo']:8s} {a['evento'][:56]}")


if __name__ == "__main__":
    main()
