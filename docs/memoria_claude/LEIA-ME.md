# Memória do Claude Code (espelho versionado)

O Claude Code guarda memória **por computador** em `C:\Users\<usuário>\.claude\projects\<pasta-do-projeto>\memory\`, fora do Git. Esta pasta é uma cópia
desses arquivos (índice em `MEMORY.md`), para que a memória viaje junto com o repositório. Última cópia: 2026-10-11, PC `Pichau`.

Restaurar em outro PC (PowerShell, na raiz do repositório; ajuste o nome da pasta do projeto, que muda com o caminho e o usuário):

```powershell
$dest = "$env:USERPROFILE\.claude\projects\C--Users-$env:USERNAME-PycharmProjects-manim-fisica\memory"
New-Item -ItemType Directory -Force $dest | Out-Null
Copy-Item docs\memoria_claude\*.md $dest -Exclude LEIA-ME.md
```

Notas: a memória é só apoio; a fonte de verdade do estado do projeto continua sendo `AGENTS.md` e `docs/estado_atual.md`. Antes de agir por uma memória,
confira se o arquivo, a função ou o parâmetro citado ainda existe.
