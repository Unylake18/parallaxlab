# Quem empurra as cargas?

**Subtítulo:** Campo elétrico, Lei de Ohm e força eletromotriz

- **ID:** yt_0009
- **formato:** longo_horizontal
- **natureza:** teoria_visual
- **macroassunto:** eletromagnetismo
- **modulo:** corrente_resistencia_e_fem
- **solido_3d:** nenhum (controle conceitual de carga superficial, E, J e deriva é melhor em Manim 2.5D; Blender não acrescenta geometria necessária)
- **Rótulo de módulo/série (na tela):** Lei de Ohm e Força Eletromotriz
- **Status:** preview visual silencioso em produção, V3 (960×540 / 15 fps; sem voz, SRT, capa ou final)
- **Classe:** `QuemEmpurraCargasYT009` em `cena.py`

## Pergunta central
Que força age, agora, sobre uma carga num pedaço do fio distante da bateria? Narrativa única:
quem age localmente? → quem estabelece E? → quem repõe a energia?

## Pré-requisitos
Campo elétrico e potencial; corrente, densidade de corrente J e resistência (nível Griffiths 7.1);
divergente (conceito de ∇·J).

## Payoff
A bateria não empurra de longe as cargas no fio. A fonte realiza trabalho não eletrostático e repõe
energia; as cargas superficiais estabelecem o campo elétrico ao longo do circuito, e esse campo atua
localmente nos portadores.

## Física protegida
- J = σf; no trecho resistivo f = E, logo J = σE. Deriva do elétron oposta a J; J ∥ E.
- J = I/A, E = V/L (V = módulo da queda), V = I·L/(σA), R = L/(σA), V = IR.
- ∂ρ/∂t + ∇·J = 0; I_entra > I_sai → acúmulo superficial → E muda → J = σE muda.
- Distribuição superficial estacionária global; estacionário ≠ sem cargas superficiais; estacionário ≠ eletrostático (E ≠ 0 no fio com corrente).
- Na fonte f = E + f_s; ℰ = ∮f·dℓ; circuito DC estacionário (sem indução/movimento) ⇒ ∮E·dℓ = 0 ⇒ ℰ = ∮f_s·dℓ.
- P_fonte = ℰI = I²R = P_dissipada (R = resistência total do modelo ideal).
- Fora do escopo: Faraday, Poynting, propagação de sinal, resistência interna, Kirchhoff, RC, u×B.

## Recorte curricular
Griffiths 7.1.1 (Lei de Ohm) e 7.1.2 (força eletromotriz). A 7.1.3 (FEM de movimento) fica deliberadamente para o vídeo seguinte; este vídeo não cobre a seção 7.1 inteira.
