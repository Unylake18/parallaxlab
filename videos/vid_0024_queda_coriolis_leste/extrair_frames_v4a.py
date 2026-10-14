import os
from pathlib import Path
import av
from PIL import Image

video_path = Path("videos/vid_0024_queda_coriolis_leste/media/QuedaCoriolisV4A.mp4")
out_dir = Path("videos/vid_0024_queda_coriolis_leste/frames_v4a")
out_dir.mkdir(parents=True, exist_ok=True)

timestamps = {
    "01_hook_pergunta": 4.0,
    "02_terra_25d": 11.5,
    "03_terra_rotacao": 14.5,
    "04_transicao_haste": 19.5,
    "05_haste_inicio": 25.0,
    "06_efeito1_dr": 28.5,
    "07_efeito1_algebra": 34.0,
    "08_efeito2_geometria": 42.0,
    "09_efeito2_algebra": 46.5,
    "10_fator2_soma": 53.0,
    "11_vista_inercial": 58.5,
    "12_troca_referencial": 63.5,
    "13_coriolis_nascimento": 66.5,
    "14_formula_completa": 69.0,
}

container = av.open(str(video_path))
stream = container.streams.video[0]

# Mapear timestamps ordenados
sorted_targets = sorted(timestamps.items(), key=lambda x: x[1])
target_idx = 0

for frame in container.decode(stream):
    if target_idx >= len(sorted_targets):
        break
    curr_time = float(frame.pts * stream.time_base)
    name, target_ts = sorted_targets[target_idx]
    if curr_time >= target_ts:
        img = frame.to_image()
        img_path = out_dir / f"frame_{name}.png"
        img.save(img_path)
        print(f"Salvo: {img_path.name} em t={curr_time:.2f}s (alvo={target_ts}s)")
        target_idx += 1

print("Extração sequencial concluída!")
