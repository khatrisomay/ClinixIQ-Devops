# ClinixIQ Teardown & Purge Script (PowerShell)
param (
    [switch]$All
)

Write-Host "==> Stopping Docker Compose services..." -ForegroundColor Yellow
docker compose down -v --remove-orphans

if ($All) {
    Write-Host "==> Pruning dangling ClinixIQ images..." -ForegroundColor Red
    docker image prune -f --filter "label=project=clinixiq"
}

Write-Host "==> Environment clean." -ForegroundColor Green
