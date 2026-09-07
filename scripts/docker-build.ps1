# ClinixIQ Docker Build Script (PowerShell)
param (
    [string]$Tag = "latest",
    [switch]$NoCache
)

$ErrorActionPreference = "Stop"

Write-Host "==> Building ClinixIQ Multi-Service Images [tag: $Tag]..." -ForegroundColor Cyan

$buildArgs = @()
if ($NoCache) {
    $buildArgs += "--no-cache"
}

Write-Host "-> Building Backend Image..." -ForegroundColor Yellow
docker build @buildArgs -t "clinixiq-backend:$Tag" -f backend/Dockerfile ./backend

Write-Host "-> Building Frontend Image..." -ForegroundColor Yellow
docker build @buildArgs -t "clinixiq-frontend:$Tag" -f frontend/Dockerfile ./frontend

Write-Host "-> Building Gateway Image..." -ForegroundColor Yellow
docker build @buildArgs -t "clinixiq-gateway:$Tag" -f gateway/Dockerfile ./gateway

Write-Host "==> All images built successfully!" -ForegroundColor Green
docker images | Select-String "clinixiq"
