"""yt_0019 v10: gera só os blocos novos do fecho (FIM-1 gancho de colisões, FIM-2 CTA) com a mesma voz/modelo do v9. Saída: audio/voz10/bloco_06 (FIM-1) e bloco_07 (FIM-2).
uso: python gerar_voz_fim.py [--refazer]"""
import os
import sys
from pathlib import Path

import gerar_voz_v9 as g

FIM1 = ("[curious] Lembra da areia na esteira? Metade da energia virou calor, porque o grão bate e escorrega até pegar a velocidade da esteira. "
        "Esse tipo de perda tem um vídeo só dele aqui no canal: o das colisões. Lá a gente vê quando a energia se conserva, quando ela vira calor, "
        "e o que o momento garante nos dois casos.")
FIM2 = "[calm] Se essa conta mudou o jeito como você olha para um foguete, se inscreva no Parallax Lab. E o vídeo de colisões está logo aqui do lado."
g.SAIDA = Path(__file__).resolve().parent / "audio" / "voz10"
ref = "--refazer" in sys.argv
chave = os.environ["ELEVENLABS_API_KEY"]
antes = "E fica um desafio para os comentários: um foguete de um estágio só, sem contar a estrutura, precisa ganhar o dobro da velocidade de exaustão. Que fração da massa inicial tem que ser propelente? Até a próxima!"
for n, aid, tx, ant, dep in ((6, "FIM-1", FIM1, antes, FIM2), (7, "FIM-2", FIM2, FIM1, "")):
    if (g.SAIDA / f"bloco_{n:02d}.mp3").exists() and not ref:
        print(aid, "já existe"); continue
    print(aid, "...", flush=True)
    g.gravar(f"bloco_{n:02d}", tx, [aid], g.chamar(chave, tx, ant, dep))
print("ok")
