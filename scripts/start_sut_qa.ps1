$ErrorActionPreference = "Stop"

$qaRoot = Split-Path -Parent $PSScriptRoot
$sutRoot = Join-Path (Split-Path -Parent $qaRoot) "dashboard-legal"
$envFile = Join-Path $qaRoot ".env"
$runtime = Join-Path $env:TEMP "ipas-qa-runtime"

if (-not (Test-Path -LiteralPath $envFile)) {
    throw "Falta qa-platform/.env"
}

$settings = @{}
foreach ($line in Get-Content -LiteralPath $envFile) {
    if ($line -match '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)\s*$') {
        $settings[$matches[1]] = $matches[2]
    }
}
if ($settings['QA_DB_NAME'] -ne 'ius_puniendi_qa') {
    throw "Arranque bloqueado: QA_DB_NAME no es ius_puniendi_qa"
}

New-Item -ItemType Directory -Path $runtime -Force | Out-Null

$env:DB_HOST = $settings['QA_DB_HOST']
$env:DB_PORT = $settings['QA_DB_PORT']
$env:DB_DATABASE = $settings['QA_DB_NAME']
$env:DB_NAME = $settings['QA_DB_NAME']
$env:DB_USER = $settings['QA_DB_USER']
$env:DB_PASSWORD = $settings['QA_DB_PASSWORD']
$env:NODE_ENV = 'test'
$env:PORT = '4000'

$backend = Start-Process -FilePath 'node.exe' -ArgumentList 'src/index.js' `
    -WorkingDirectory (Join-Path $sutRoot 'Backend') -WindowStyle Hidden -PassThru `
    -RedirectStandardOutput (Join-Path $runtime 'backend.out.log') `
    -RedirectStandardError (Join-Path $runtime 'backend.err.log')
$backend.Id | Set-Content -LiteralPath (Join-Path $runtime 'backend.pid')

$env:BROWSER = 'none'
$env:PORT = '3000'
$env:REACT_APP_API_URL = 'http://127.0.0.1:4000/api'
$frontend = Start-Process -FilePath 'npm.cmd' -ArgumentList 'start' `
    -WorkingDirectory (Join-Path $sutRoot 'client') -WindowStyle Hidden -PassThru `
    -RedirectStandardOutput (Join-Path $runtime 'frontend.out.log') `
    -RedirectStandardError (Join-Path $runtime 'frontend.err.log')
$frontend.Id | Set-Content -LiteralPath (Join-Path $runtime 'frontend.pid')

Write-Output "SUT QA iniciado: backend PID=$($backend.Id), frontend PID=$($frontend.Id)"
Write-Output "Logs de ejecución: $runtime"

