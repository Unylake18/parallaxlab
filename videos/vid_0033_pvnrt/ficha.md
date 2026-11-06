# De onde vem PV = nRT?

formato: curto_vertical

Série pública: **POR TRÁS DA FÓRMULA · EP. 10** (confirmado pelo Kaio em 2026-11-05; último EP. publicado da série: 09 em `vid_0029`)

Fase: **final entregue (2026-11-06)**: voz ElevenLabs `eleven_v4` (voz `qw7jgPZWOKrl10GsjQ82`, 1 tomada, 171,04 s) sobre `narracao_tags.md`; cena sincronizada pelo alinhamento forçado (75 eventos × palavra, atraso ≤ 0,2 s); master e legendado 1080×1920 / 30 fps, H.264 CRF 14, 174,07 s; `legenda.srt` (81 blocos). Sem publicação.

disciplina: Física II
bloco: Termodinâmica
modulo: 5.8 Temperatura, calor e teoria cinética (docs/mapa_curricular.md)
referencia: Moysés vol. 2 e Sears Física II, teoria cinética do gás ideal (seções a conferir)

- Unidade: `vid_0033`. Duração-alvo ~185 s (teto de 180 s a confirmar).
- Mapa curricular: teoria cinética dos gases; posição a conferir em `docs/mapa_curricular.md`.
- 3d_threejs: C01 hook (patch de 1 cm² na parede, esferas batendo cada vez mais rápido, depois pull-back); C02–C03 câmera frontal com molécula acompanhada, vetores e batidas; C04–C06 caixa recuada ao fundo; C07 um recipiente com pistão entre dois estados de equilíbrio (V → V/2)
- solido_3d: nenhum do arsenal Blender

**Uma ideia:** pressão é a taxa de transferência de momento das moléculas à parede, por unidade de área. Temperatura e n entram por cima disso.

## Física (especificação)

Modelo: gás ideal, N partículas de massa m em cubo de lado L (V = L³), colisões elásticas com paredes fixas, interações desprezíveis, velocidades isotrópicas em equilíbrio.

- A. Parede ⟂ x: molécula Δpₓ = −2mvₓ (vₓ > 0); parede recebe +2m|vₓ|. Duas setas opostas, a da parede em destaque.
- B. Volta à mesma parede a cada 2L/|vₓ| (demonstração de uma partícula). Fmed = mvₓ²/L; P₁ = mvₓ²/V.
- C. PV = N m ⟨vₓ²⟩; isotropia ⇒ ⟨vₓ²⟩ = ⟨v²⟩/3 (vale para a média, não molécula a molécula). **PV = ⅓ N m ⟨v²⟩.**
- D. ⟨E_trans⟩ = ½m⟨v²⟩ ⇒ **PV = ⅔ N ⟨E_trans⟩.**
- E. Ponte da temperatura (informação experimental, dita como tal): PV ∝ T no gás ideal ⇒ ⟨E_trans⟩ = (3/2)k_BT, k_B = 1,380649·10⁻²³ J/K. Só translação. PV = N k_B T.
- F. N = nN_A, R = N_A k_B = 8,314 J/(mol·K) ⇒ **PV = nRT.**
- Não dizer que as leis de Newton deduzem a temperatura termodinâmica; não dizer "constante é escolha de unidade" nem "T é a energia média".

## Verificação (Python, já rodada)

N₂ a 300 K: v_rms = 517 m/s (média ≈ 476). Monte Carlo 200 mil: ⟨vₓ²⟩/⟨v²⟩ = 0,3336; P = 101 400 Pa. ⟨E_trans⟩ = 6,2·10⁻²¹ J (3 741 J/mol). Mesma T: He 1 367 m/s, O₂ 484 m/s. 1 mol, 300 K, 1 atm: 24,6 L. Espaçamento no ar ≈ 3,4 nm.
QA extra no preview: somar o impulso das colisões simuladas, dividir por área e tempo e comparar com N k_B T / V.

## Estrutura (~185 s, tempos editoriais)

| Tempo | Momento | Visual |
|---|---|---|
| 0–15 | Gancho | Caixa com moléculas batendo; PV = nRT como pergunta |
| 15–45 | Uma batida | Close numa molécula; componente normal inverte; duas setas de impulso |
| 45–75 | Nasce a pressão | Ida e volta, 2L/vₓ, força média, área |
| 75–115 | **O 1/3** | Muitas moléculas; decomposição 3D; três indicadores de ⟨vₓ²⟩, ⟨v_y²⟩, ⟨v_z²⟩ convergem; PV = ⅓Nm⟨v²⟩ |
| 115–145 | Energia e T | ⅔N⟨E⟩; termômetro de gás; ⟨E⟩ = (3/2)k_BT |
| 145–167 | Fórmula | ⅔·3/2 cancela; N → nN_A; R = N_A k_B; PV = nRT |
| 167–185 | Fecho | Pistão isotérmico, dois estados (selo TEMPERATURA CONSTANTE); 517 m/s do N₂; CTA |

Selos `MODELO IDEAL` e `CÂMERA LENTA` (517 m/s numa caixa de 29 cm ≈ 1 800 travessias/s; cena ~×1 000 mais lenta). Sem bloco separado para Maxwell, Boyle ou termodinâmica. Não mostrar cada molécula com três componentes iguais.

## Cores

Velocidade **e temperatura T**: violeta (decisão do Kaio, 2026-11-05: T em violeta por representar a velocidade das partículas). Momento: magenta. Força: azul-claro `#5AA2FF`. Impulso J: azul clareado `#9CC7FF` (não magenta). Energia cinética / energia fornecida: ciano `#35D9FF` (`CYAN`). Laranja só para calor/dissipação. Moléculas em aço `#7A8696`, molécula acompanhada destacada.

## Limites

Pressão é média estatística. 2L/vₓ é só da demonstração de uma partícula. T → 0 e V → ∞ são extrapolações do modelo ideal.
