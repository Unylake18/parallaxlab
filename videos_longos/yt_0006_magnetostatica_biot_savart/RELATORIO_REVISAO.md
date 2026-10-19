# Relatório — revisão profunda do yt_0006 (v5)

Escopo: cena e preview silencioso 960×540 / 15 fps. Sem voz, sync, SRT, capa, master ou publicação. Avaliação estética/didática pertence ao usuário.

## Infraestrutura (kit.py / base.py)
- `gmap()`: erro claro se dois mapeamentos explícitos têm o mesmo glifo de destino (um proprietário por destino); parâmetros `structure` e `reserved`; troca simples (fade) quando não há termos em comum — antes o MF-Tools desenhava índices de depuração (dígitos soltos na tela).
- `show()`: glifos de destino de `src={...}` ficam reservados (auto-mapeamento não os toca); origem do voo é cópia CONGELADA do rótulo do desenho.
- `caption()`: saída e entrada em sequência (nunca duas frases ao mesmo tempo).
- Layouts locais `split` / `geo` (geometria dominante) / `alg` (álgebra dominante) com `relayout()`; cartões vazios saem (`drop`).
- `drop()` remove também os filhos de grupos montados com FadeIn separado (números que ficavam fantasmas).

## Correções físicas
- Espira: `R` é o raio, `s=√(R²+z²)` é a separação; a lei entra direto com `s²` e `sin90°=1` (nunca R² → s²).
- K/J: cadeia `dI=K dw`, `dℓ=t̂ dℓ`, `K=K t̂`, `da=dw dℓ`, `dI dℓ = K da`; e `dI=J dA⊥`, `J=J t̂`, `dτ=dA⊥ dℓ`, `dI dℓ = J dτ`.
- Circuito: `B_total = B_trecho + B_restante` em negrito (soma vetorial).
- Abertura: sem ⊙/⊗ em vista oblíqua (B₁ tangente ao anel); força entre fios em vista frontal, onde ⊗/⊙ têm sentido inequívoco; inversão de I₂ muda corrente, L e F₂, B₁ permanece.
- Lei vetorial: `sinθ` não vira `R̂`; `|dℓ×R̂| = dℓ sinθ` (paralelogramo) e só então `dℓ×R̂`, com `×` e `R̂` vindos do cartão auxiliar.
- Fusões (R·R→R², s²·s→s³): estado intermediário legível e um único proprietário por destino.

## Seções com refeitura maior
distribuições (K/J), trecho finito (produto vetorial distribuído, triângulo ampliado, α, denominador passo a passo, cancelamentos, limites α_A/α_B), espira (s, projeção axial dinâmica com z, par oposto, integrando por etapas, 2π/4π→1/2), centro (várias contribuições axiais), síntese, fios (vista frontal), clínica (P fora do fio, dB=0, guia 0→180°), geometria (fonte móvel com P fixo), regime (texto enxuto).

## Verificações
- `py_compile -W error` de todos os módulos; execução de toda a cena sem quadros (SEG=nenhuma) sem exceções.
- Preview completo em 8 trechos (memória), juntado com recodificação H.264 yuv420p CRF 16: 16min47s, 15.104 quadros, 960×540 / 15 fps.
- Revisão por folhas de contato de todas as sentinelas e de trecho/infinito/fios após as correções.

## Limitações / pendências
- Captions das seções não-sentinela (abertura, lei, clínica, superposição, método, fios) só foram encurtadas em parte; texto ainda é mais longo que o ideal em alguns pontos.
- Rótulo "vista lateral" e "resto do circuito" foram reposicionados, mas não reverificados visualmente nas margens após o último render.
- Emparelhamentos de glifos aproximados em algumas transições (conferir no vídeo).
- Sem aprovação estética; render completo numa só passada estoura memória: usar `_grupo.sh` por trecho e `juntar.py`.
- `qa_*.py` e `preview_trechos.py` pertencem à estrutura antiga e não funcionam.
- Nenhum sólido Blender integrado (Teste do arsenal: n/a).
