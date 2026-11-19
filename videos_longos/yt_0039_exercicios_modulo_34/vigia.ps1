# yt_0039 · vigia de travas de um lote: enquanto o LOG não tiver o fim do lote ("[tempo] total" ou "Traceback"), se ele ficar parado por mais
# de LIMITE s, encerra só os latex/dvisvgm desta unidade (linha de comando com yt_0039) e anota no log. Sai sozinho no fim do lote ou após 20 min parado.
param([string]$Log, [int]$Limite = 150)
Start-Sleep -Seconds 15
while ($true) {
    Start-Sleep -Seconds 20
    if (-not (Test-Path $Log)) { continue }
    $txt = Get-Content $Log -Tail 30 -ErrorAction SilentlyContinue | Out-String
    if ($txt -match '\[tempo\] total|Traceback|\[render\]') { break }
    $parado = ((Get-Date) - (Get-Item $Log).LastWriteTime).TotalSeconds
    if ($parado -gt 1200) { break }
    if ($parado -gt $Limite) {
        $tr = Get-CimInstance Win32_Process | Where-Object { ($_.Name -match 'latex|dvisvgm') -and $_.CommandLine -match 'yt_0039' }
        foreach ($p in $tr) {
            Add-Content -Path $Log -Value "[vigia] $(Get-Date -Format T) log parado ha $([int]$parado) s: encerrando $($p.Name) $($p.ProcessId)"
            Stop-Process -Id $p.ProcessId -Force -Confirm:$false
        }
    }
}
