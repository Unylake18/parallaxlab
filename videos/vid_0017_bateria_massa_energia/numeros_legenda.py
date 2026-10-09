"""Grafia numérica da legenda; a narração e seus tempos permanecem originais."""
import re

# Correspondências explícitas: artigos como «uma bateria» continuam por extenso.
SUBSTITUICOES = [
    ("cinquenta e quatro mil setecentos e vinte", "54.720"),
    ("duzentos e cinquenta", "250"),
    ("quinze vírgula dois", "15,2"),
    ("zero vírgula seis", "0,6"),
    ("um vírgula seis", "1,6"),
    ("três vírgula oito", "3,8"),
    ("vinte e cinco", "25"),
    ("cem milhões", "100 milhões"),
    ("quatro mil", "4.000"),
    ("quatro", "4"),
    ("oito horas", "8 horas"),
    ("um nanograma", "1 nanograma"),
    ("um grama", "1 grama"),
    ("um único grama", "1 único grama"),
]


def norm(word):
    return re.sub(r"[^\wáéíóúâêôãõàç]", "", word.lower())


def converter(palavras, inicios, fins):
    """Une cada número com o intervalo inteiro da expressão falada.

    Assim «três / vírgula oito» nunca vira dois números nem cruza cues.
    """
    saida, ini, fim = [], [], []
    regras = [(a.split(), b) for a, b in SUBSTITUICOES]
    normalized = [norm(p) for p in palavras]
    i = 0
    while i < len(palavras):
        for origem, destino in regras:
            n = len(origem)
            if normalized[i:i+n] == origem:
                suffix = re.search(r"[^\wáéíóúâêôãõàç]*$", palavras[i+n-1]).group()
                # Manter unidades/qualificadores juntos ao algarismo no mesmo token.
                saida.append(destino + suffix)
                ini.append(float(inicios[i]))
                fim.append(float(fins[i+n-1]))
                i += n
                break
        else:
            saida.append(palavras[i])
            ini.append(float(inicios[i]))
            fim.append(float(fins[i]))
            i += 1
    return saida, ini, fim
