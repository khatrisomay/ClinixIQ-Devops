# ClinixIQ Chaos Load Generator Wrapper (PowerShell)
param (
    [string]$Url = "http://localhost:8000",
    [int]$Requests = 100,
    [double]$Delay = 0.05
)

$py = if (Test-Path "backend/venv/Scripts/python.exe") { "backend/venv/Scripts/python.exe" } else { "python" }

Write-Host "==> Starting ClinixIQ Synthetic Load Generator..." -ForegroundColor Cyan
& $py scripts/generate-load.py --url $Url --requests $Requests --delay $Delay
