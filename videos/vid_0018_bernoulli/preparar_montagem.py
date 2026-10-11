"""Agenda quantizada: ações da V5 ancoradas nas frases do WAV recebido."""
import hashlib
import json
from pathlib import Path
import numpy as np

UNIT = Path(__file__).resolve().parent


def main():
    native = json.loads((UNIT / "native.json").read_text(encoding="utf-8"))
    timeline = json.loads((UNIT / "tempos_native.json").read_text(encoding="utf-8"))
    sync = json.loads((UNIT / "sync.json").read_text(encoding="utf-8"))
    timing = json.loads((UNIT / "palavras_tempos.json").read_text(encoding="utf-8"))
    audio_offset, tail = .4, .9
    speech = {name: at + audio_offset for name, at in sync["anchors"]}
    points = {0: 0.0, len(native["cues"]): timing["audio_s"] + audio_offset + tail}
    selected = []

    def event(kind, name, at):
        row = next(e for e in native["eventos"] if e["tipo"] == kind and e["nome"] == name)
        assert row["cue"] not in points, (kind, name)
        points[row["cue"]] = at
        selected.append({"tipo": kind, "nome": name, "cue": row["cue"], "alvo_s": at})

    event("fase", "Um mesmo volume de fluido", speech["mesmo_volume"])
    event("fase", "A pressão empurra o fluido", speech["forca"])
    event("estado", "forca_entrada", speech["trabalho"] - .9)
    event("estado", "avanco_entrada", speech["volume_varrido"])
    event("estado", "volume_varrido", speech["trabalho_entrada"] - 1.4)
    event("estado", "trabalho_entrada", speech["trabalho_entrada"] + 1.5)
    event("fase", "Da entrada à saída", speech["saida"] - 2.0)
    event("fase", "Na saída, a pressão resiste", speech["saida"])
    event("estado", "saida_sinal_negativo", speech["sinal_negativo"] + .3)
    event("estado", "trabalho_saida", speech["liquido"] - 1.0)
    event("fase", "As duas pressões fazem trabalho", speech["liquido"])
    event("estado", "trabalho_liquido", speech["energia"] - 1.8)
    event("fase", "O trabalho muda a energia mecânica", speech["energia"])
    event("estado", "massa_volume", speech["massa"] + 2.3)
    event("estado", "energias_dos_estados", speech["cinetica"] + 1.0)
    event("estado", "variacao_cinetica", speech["gravitacional"] - .5)
    event("estado", "variacao_gravitacional", speech["balanco"] - .7)
    event("fase", "Um balanço de energia", speech["balanco"])
    event("estado", "balanco_simbolico", speech["balanco"] + 1.8)
    event("estado", "balanco_completo", speech["cancelar"] - 2.0)
    event("fase", "Um balanço por unidade de volume", speech["cancelar"])
    event("estado", "cancelamento_volume", speech["volume_comum"] + .5)
    event("estado", "balanco_por_volume", speech["por_volume"] + 1.4)
    event("estado", "diferencas_abertas", speech["por_volume"] + 2.4)
    event("estado", "agrupamento_por_estado", speech["reorganizar"] + .27)
    event("fase", "A mesma combinação ao longo da linha de corrente", speech["reorganizar"] + .67)
    event("estado", "bernoulli", speech["reorganizar"] + 1.87)
    event("fase", "Três termos, uma unidade", speech["reorganizar"] + 1.97)
    event("estado", "significado_pressao", speech["reorganizar"] + 2.57)
    event("estado", "significado_cinetica", speech["reorganizar"] + 3.77)
    event("estado", "significado_gravitacional", speech["reorganizar"] + 6.97)
    event("estado", "unidades", speech["unidades"] + .8)
    event("extra", "pressao_apos_unidades", speech["pressao_significado"])
    event("fase", "Duas leis no estreitamento", speech["estreitamento"])
    event("estado", "continuidade_2d", speech["velocidade_aumenta"] + 1.2)
    # Início da retirada das parcelas gravitacionais iguais.
    horizontal = timeline["glyph_maps"][-1]["tempo"] - .8
    row = min(native["cues"], key=lambda cue: abs(cue["inicio"] - horizontal))
    points[row["indice"]] = speech["altura_igual"] + 3.8
    selected.append({"tipo": "morf", "nome": "alturas_iguais", "cue": row["indice"],
                     "alvo_s": points[row["indice"]]})
    event("estado", "bernoulli_estreitamento", speech["conclusao"] + .7)
    event("fase", "Quando Bernoulli vale?", speech["hipoteses"])
    event("estado", "hipoteses_finais", speech["condicoes"] + .7)
    event("estado", "cta_final", speech["CTA"] + .6)
    ordered = sorted(points.items())
    assert all(a[1] < b[1] for a, b in zip(ordered, ordered[1:])), ordered
    agenda = []
    for (i0, t0), (i1, t1) in zip(ordered, ordered[1:]):
        rows = native["cues"][i0:i1]
        durations = np.array([r["nativo"] for r in rows])
        boundaries = t0 + np.concatenate([[0], np.cumsum(durations)]) / durations.sum() * (t1 - t0)
        for row, start, end in zip(rows, boundaries[:-1], boundaries[1:]):
            # Grade comum a 15 e 30 fps; nenhuma perda cumulativa de quadros.
            start, end = round(start * 15) / 15, round(end * 15) / 15
            assert end > start, (row, start, end)
            agenda.append({"indice": row["indice"], "inicio": start, "fim": end,
                           "animacao_max_s": max(1 / 15, row["nativo"]), "pausa": row["pausa"]})
    assert len(agenda) == len(native["cues"])
    sync.update({"agenda": agenda, "audio_offset_s": audio_offset, "audio_s": timing["audio_s"],
                 "video_s": agenda[-1]["fim"], "audio_sha256": hashlib.sha256((UNIT / "audio/narracao_final.wav").read_bytes()).hexdigest(),
                 "metodo": timing["metodo"], "pontos_visuais": selected,
                 "voz_preservada": True, "variacao_velocidade_voz": 1.0})
    (UNIT / "sync.json").write_text(json.dumps(sync, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f'{len(agenda)} ações, {len(selected)} pontos visuais, vídeo {sync["video_s"]:.3f}s')


if __name__ == "__main__":
    main()
