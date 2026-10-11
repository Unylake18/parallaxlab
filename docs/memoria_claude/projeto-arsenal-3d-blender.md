---
name: projeto-arsenal-3d-blender
description: "Estado do arsenal de sólidos 3D em Blender (experimentos/blender/arsenal), da ponte com o Manim e armadilhas medidas"
metadata:
  node_type: memory
  type: project
  originSessionId: 52a8776a-3165-4130-b609-47a0583f1cd4
  modified: 2026-10-07T17:21:08.816Z
---

Arsenal de sólidos 3D em `experimentos/blender/arsenal/` (fichas JSON em `solidos/`, `catalogo.md` e `cobertura.md` gerados, padrão visual em `estilo.json`). Trilha paralela ao yt_0002; só mexe em `experimentos/` (e registros autorizados em AGENTS.md/docs/formatos.md/docs/estado_atual.md). Ponte com o Manim: `ponte.py` (cache em `renders/arsenal3d/`) + `manim_solido3d.py` (`Solido3D(id).mobject(cena=self, ...)`).

Estado (2026-10-07): 88 sólidos, todos aprovados (fila A e B; B em `otica_b.py`, `calculo_b.py` etc.). Commits na `main`, sem push; últimos: 6072000 (fila B + `abrir/` + limpeza do sandbox: sem .blend, out/ nem orbita_alpha.py) e 2dd3fdd (docs). Atalhos `arsenal/abrir/<id>.bat` + `abrir_no_blender.py` + `gerar_atalhos.py` (testado em GUI). Registrado em `docs/formatos.md`, AGENTS.md e estado_atual que o arsenal deve ser TESTADO nos próximos vídeos curtos e longos (campo `solido_3d:`, anotar o encaixe depois). Só restam 2 lacunas 3D (centro de massa, campos conservativos), ver `cobertura.md`. O usuário disse "sem Co-Authored-By" nos commits do arsenal: seguir isso.

**Why:** o usuário quer um arsenal reutilizável que qualquer vídeo consulte e que o Manim use quando precisar; padrão segue a Lei de Gauss ([[feedback-arsenal-padrao-gauss]]) e as decisões em [[feedback-arsenal-decisoes-visuais]].

**How to apply:** não commitar sem pedido; commits só com caminhos explícitos (outro chat edita `videos*/` e a linha 7 de `docs/estado_atual.md`: usar patch parcial `git apply --cached --unidiff-zero`). Armadilhas medidas: (1) o Manim chama o updater 2x por quadro durante FadeIn/FadeOut no próprio mobject: fase deve vir de `cena.time`; (2) comparar loops só sem codec (`--save_pngs`); (3) o tool Bash processa `\` dentro de heredocs (viram `\b`/`\n`/`\a` reais): para código/docs com barras use Write/Edit e varra caracteres de controle; (4) material de malha compartilhada vale para todas as instâncias: usar material por objeto (`material_slots[0].link = "OBJECT"`); (5) conferir contas de peso/tempo; (7) `osc._caixa` grava a posição nos vértices em alguns casos: para peças que `atualizar` move use `_movel` (nasce na origem e `location` carrega a posição); (8) na GUI do Blender `co.limpar_cena` (read_factory_settings) derruba a interface, o contexto exige `temp_override` de janela/área e, com a interface em português, os nós nascem como "BSDF Principled" (desligar `use_translate_new_dataname` durante a montagem); (6) glifo esculpido precisa ficar com a face da frente ACIMA da esfera, e só encara a câmera depois de `orientar_glifos` (gancho `apos_camera`).
