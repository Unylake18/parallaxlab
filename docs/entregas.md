# Entregas finais: uma pasta só

Todo arquivo final de vídeo (Codex ou Claude) vai para **`entregas/`**, na raiz do repositório, uma pasta por vídeo:

```
entregas/
  Da Equação ao Fenômeno - EP 05 - Torricelli, onde furar para o jato ir mais longe - 0016/
    master - 0016.mp4          versão final limpa, com a voz
    legendado - 0016.mp4       versão final com legendas coloridas
    legenda - 0016.srt         legendas, no tempo do vídeo final
    capa - 0016.png            só a capa escolhida (quando houver); propostas não entram
    audio/                     voz final (narracao_final - 0016.*, narracao_montagem - 0016.* se existir)
    texto/                     ficha, roteiro, publicação, revisão e texto da narração
    manifesto - 0016.json      origem de cada arquivo, tamanho, SHA-256 e dados do vídeo (resolução, fps, duração)
```

Nome da pasta: **`Série - EP NN - Assunto - NNNN`**; o número do vídeo (`0001` em diante, o mesmo de `vid_NNNN`) também vai no fim de
todo nome de arquivo, antes da extensão (`master - 0016.mp4`). Vídeos longos usam `yt0001`. Séries públicas: Por Trás da Fórmula, Da Equação ao Fenômeno,
Exercício Resolvido, Absurdo Calculável. A pasta `entregas/` fica fora do Git (`.gitignore`); trocar o local com a variável de
ambiente `PARALLAX_ENTREGAS`.

## Como entregar

```
uv run python videos/entregar.py vid_NNNN             # copia o que está pronto da unidade
uv run python videos/entregar.py vid_NNNN --dry-run   # só mostra o que seria copiado
uv run python videos/entregar.py --listar             # o que cada unidade tem de master/legendado
uv run python videos/entregar.py --todos              # refaz todas (copia só o que mudou)
```

- É sempre **cópia**: nada é movido nem apagado nas pastas de origem. Rodar de novo atualiza só o que mudou.
- O script escolhe, em `videos/vid_NNNN/renders/` e em `renders/`, o master e o legendado finais mais recentes (ignora
  `preview` e `sem_audio`). Quando existe mais de uma versão final, as outras ficam listadas em
  `versoes_finais_nao_copiadas` no manifesto; para fixar uma, use `master`/`legendado`/`capa` em
  `videos/entregas_registro.json`.
- Série, episódio e assunto: `videos/entregas_registro.json` ou, para unidades novas, a `ficha.md`
  (`Série pública: **NOME · EP. N**` e um título `# Assunto`).
- `"inferido": true` no registro = série/EP deduzidos, para confirmar (hoje: vid_0001 e vid_0002).

## Regra de trabalho

Ao fechar uma versão final, rodar `entregar.py` e informar no relatório o caminho da pasta em `entregas/`.
Não deixar finais soltos em `renders/` ou nas pastas das unidades como destino definitivo; previews e intermediários
continuam onde estão.
