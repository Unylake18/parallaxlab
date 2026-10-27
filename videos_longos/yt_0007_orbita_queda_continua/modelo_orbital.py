"""Gravitação newtoniana em SI; a projeção gráfica pertence à cena.

Executar diretamente para validar a física usada em N01–N18.
"""

from dataclasses import dataclass
import json
import math

import numpy as np

R_T = 6.371e6
MU = 3.986004418e14


def aceleracao(r):
    r = np.asarray(r, dtype=float)
    return -MU * r / np.linalg.norm(r) ** 3


def energia(r, v):
    return float(np.dot(v, v) / 2 - MU / np.linalg.norm(r))


def v_circular(r):
    return math.sqrt(MU / r)


def periodo(r):
    return 2 * math.pi * math.sqrt(r**3 / MU)


def passo_verlet(r, v, dt):
    a = aceleracao(r)
    novo_r = r + v * dt + 0.5 * a * dt**2
    novo_v = v + 0.5 * (a + aceleracao(novo_r)) * dt
    return novo_r, novo_v


@dataclass
class Trajetoria:
    t: np.ndarray
    r: np.ndarray
    v: np.ndarray
    impacto: bool

    def estado(self, t):
        t = float(np.clip(t, self.t[0], self.t[-1]))
        return (np.array([np.interp(t, self.t, self.r[:, i]) for i in range(2)]),
                np.array([np.interp(t, self.t, self.v[:, i]) for i in range(2)]))


def integrar(r0, v0, duracao, dt=1.0):
    """Velocity-Verlet; refina o primeiro cruzamento da superfície por bisseção.

    Nenhuma normalização/correção artificial de raio ou energia é aplicada.
    O último passo de impacto usa o mesmo Verlet com duração fracionária.
    """
    r, v = np.array(r0, dtype=float), np.array(v0, dtype=float)
    assert np.linalg.norm(r) > R_T
    tempos, posicoes, velocidades = [0.0], [r.copy()], [v.copy()]
    impacto = False
    while tempos[-1] < duracao - 1e-9:
        h = min(dt, duracao - tempos[-1])
        nr, nv = passo_verlet(r, v, h)
        if np.linalg.norm(nr) <= R_T:
            lo, hi = 0.0, h
            for _ in range(48):
                meio = (lo + hi) / 2
                teste, _ = passo_verlet(r, v, meio)
                if np.linalg.norm(teste) > R_T:
                    lo = meio
                else:
                    hi = meio
            h = (lo + hi) / 2
            nr, nv = passo_verlet(r, v, h)
            impacto = True
        tempos.append(tempos[-1] + h)
        posicoes.append(nr.copy())
        velocidades.append(nv.copy())
        r, v = nr, nv
        if impacto:
            break
    return Trajetoria(np.array(tempos), np.array(posicoes), np.array(velocidades), impacto)


def lancamento(raio, fator, dt=1.0):
    return integrar([0, raio], [fator * v_circular(raio), 0], periodo(raio), dt)


def conica(raio, fator, fisica=True, alcance=7 * R_T, amostras=650):
    """Cônica tangencial: origem no topo, movimento horário, Terra em um foco.

    q=v0² r0/MU. O sinal de q-1 preserva periastro/apoastro do lançamento.
    A energia classifica ligada/aberta; a colisão é uma propriedade independente.
    """
    q = fator**2
    p = raio * q
    ecc = abs(q - 1)
    eps = energia([0, raio], [fator * v_circular(raio), 0])
    ligada = eps < 0
    periastro = p / (1 + ecc)
    colide = periastro <= R_T and q < 1
    if ligada:
        apoastro = p / (1 - ecc)
        if q > 1 and apoastro > alcance:
            # Só a janela visível da previsão: evita coordenadas gigantes
            # ao aproximar a parábola, sem mudar energia ou classificação.
            limite = math.acos(np.clip((p / alcance - 1) / (q - 1), -1, 1))
        else:
            limite = 2 * math.pi
    else:
        limite = math.acos(np.clip((p / alcance - 1) / (q - 1), -1, 1))
    if fisica and colide:
        limite = math.acos(np.clip((p / R_T - 1) / (q - 1), -1, 1))
    ang = np.linspace(0, limite, amostras)
    rad = p / (1 + (q - 1) * np.cos(ang))
    pontos = np.column_stack([rad * np.sin(ang), rad * np.cos(ang)])
    if colide:
        rotulo = "impacto"
    elif not ligada:
        rotulo = "aberta"
    elif abs(fator - 1) < 0.012:
        rotulo = "circular"
    elif fator > 1:
        rotulo = "elíptica"
    else:
        rotulo = "ligada"
    return pontos, dict(energia=eps, ligada=ligada, colide=colide,
                        periastro=periastro, rotulo=rotulo)


def validar():
    r = R_T + 400e3
    v, g, t = v_circular(r), MU / r**2, periodo(r)
    queda = g / 2
    exata = r * (1 - math.cos(v / r))
    assert abs(v - 7672.6) < 0.1
    assert abs(g - 8.6943) < 0.0001
    assert abs(t / 60 - 92.414) < 0.001
    assert abs(queda - 4.3471) < 0.0001
    assert abs(exata - queda) < 1e-6
    teste = lancamento(r, 1.0)
    raios = np.linalg.norm(teste.r, axis=1)
    energias = np.sum(teste.v**2, axis=1) / 2 - MU / raios
    deriva_r = float(np.max(abs(raios / r - 1)))
    deriva_e = float(np.max(abs(energias / energias[0] - 1)))
    assert not teste.impacto and deriva_r < 1e-6 and deriva_e < 1e-9
    impactos = []
    for fator in (.55, .80, .985, 1.0):
        orb = lancamento(1.06 * R_T, fator)
        assert orb.impacto == (fator < 1)
        assert np.min(np.linalg.norm(orb.r, axis=1)) >= R_T - 1e-5
        if orb.impacto:
            assert abs(np.linalg.norm(orb.r[-1]) - R_T) < 1e-5
            impactos.append(math.degrees(math.atan2(orb.r[-1, 0], orb.r[-1, 1])))
    assert 0 < impactos[0] < impactos[1] < impactos[2]
    assert impactos[2] > 150
    estados = {}
    for fator in (.70, .92, 1.0, 1.20, 1.44):
        pontos, info = conica(1.5 * R_T, fator)
        assert info['ligada'] == (fator < math.sqrt(2))
        assert info['colide'] == (fator == .70)
        assert np.allclose(pontos[0], [0, 1.5 * R_T])
        if info['colide']:
            assert abs(np.linalg.norm(pontos[-1]) - R_T) < 1e-6
        estados[str(fator)] = info
    n14 = lancamento(1.5 * R_T, .70)
    assert n14.impacto and energia(n14.r[0], n14.v[0]) < 0
    assert abs(np.linalg.norm(n14.r[-1]) - R_T) < 1e-5
    return dict(v_400km_m_s=v, g_400km_m_s2=g, periodo_min=t / 60,
                queda_local_m=queda, queda_exata_m=exata,
                diferenca_local_m=abs(exata - queda), deriva_relativa_raio=deriva_r,
                deriva_relativa_energia=deriva_e, angulos_impacto_N01_graus=impactos,
                estados_N13=estados, impacto_N14_erro_m=abs(np.linalg.norm(n14.r[-1]) - R_T))


if __name__ == '__main__':
    print(json.dumps(validar(), indent=2, ensure_ascii=False))
