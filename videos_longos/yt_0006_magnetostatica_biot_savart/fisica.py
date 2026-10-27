"""Estados físicos do 5.2. SI sem o fator comum μ₀I/(4π), quando indicado."""
import math
import numpy as np


def clinica(theta_local, R=2.6, dl=0.65):
    fonte = np.zeros(3)
    P = R * np.array([math.cos(theta_local), math.sin(theta_local), 0.0])
    dl_vec = np.array([dl, 0.0, 0.0])
    dB = np.cross(dl_vec, P) / R**3
    return fonte, P, dl_vec, P - fonte, dB


def trecho(x_src, a=2.1, dl=0.55):
    fonte = np.array([x_src, 0.0, 0.0])
    P = np.array([0.0, a, 0.0])
    R_vec = P - fonte
    R_mag = np.linalg.norm(R_vec)
    dl_vec = np.array([dl, 0.0, 0.0])
    theta = math.acos(np.dot(dl_vec, R_vec) / (dl * R_mag))
    alpha = math.atan2(x_src, a)
    dB = np.cross(dl_vec, R_vec) / R_mag**3
    return fonte, P, dl_vec, R_vec, R_mag, theta, alpha, dB


def campo_trecho(xA, xB, a):
    """B/(μ₀I/(4π)), para corrente +x e observador (0,a), a > 0."""
    return (math.sin(math.atan2(xB, a)) - math.sin(math.atan2(xA, a))) / a


def fios(I1=1.0, I2=1.0, d=3.8):
    """Fios em x=±d/2, corrente em ±y; fatores positivos comuns omitidos."""
    B1 = np.array([0.0, 0.0, -I1 / d])  # campo do fio esquerdo no direito
    B2 = np.array([0.0, 0.0, I2 / d])
    F2 = np.cross(np.array([0.0, I2, 0.0]), B1)
    F1 = np.cross(np.array([0.0, I1, 0.0]), B2)
    return B1, B2, F1, F2


def espira(phi_src, z_obs, loop_radius=1.65):
    R = loop_radius
    fonte = R * np.array([math.cos(phi_src), math.sin(phi_src), 0.0])
    dl_dphi = R * np.array([-math.sin(phi_src), math.cos(phi_src), 0.0])
    P = np.array([0.0, 0.0, z_obs])
    R_vec = P - fonte
    dB_dphi = np.cross(dl_dphi, R_vec) / np.linalg.norm(R_vec)**3
    axial = np.array([0.0, 0.0, dB_dphi[2]])
    return fonte, P, dl_dphi, R_vec, dB_dphi, dB_dphi - axial, axial


def campo_espira(z_obs, loop_radius=1.65):
    """Bz/(μ₀I), com sentido +z para corrente anti-horária vista de +z."""
    return loop_radius**2 / (2 * (loop_radius**2 + z_obs**2)**1.5)
