$runtime = Join-Path $env:TEMP "ipas-qa-runtime"
foreach ($name in 'frontend', 'backend') {
    $pidFile = Join-Path $runtime "$name.pid"
    if (Test-Path -LiteralPath $pidFile) {
        $processId = [int](Get-Content -LiteralPath $pidFile)
        Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue
        Write-Output "$name detenido (PID=$processId)"
    }
}

