# ClinixIQ Deployment & Rollback Verification Script (PowerShell)
param (
    [string]$Namespace = "clinixiq",
    [string]$EndpointUrl = "http://localhost:8000/healthz",
    [int]$TimeoutSeconds = 90
)

$ErrorActionPreference = "Stop"

Write-Host "==> Verifying Kubernetes Rollout in namespace '$Namespace'..." -ForegroundColor Cyan

try {
    Write-Host "-> Checking Backend Deployment rollout..." -ForegroundColor Yellow
    kubectl rollout status deployment/clinixiq-backend -n $Namespace --timeout="${TimeoutSeconds}s"

    Write-Host "-> Checking Frontend Deployment rollout..." -ForegroundColor Yellow
    kubectl rollout status deployment/clinixiq-frontend -n $Namespace --timeout="${TimeoutSeconds}s"

    Write-Host "-> Probing Application Health Endpoint ($EndpointUrl)..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri $EndpointUrl -TimeoutSec 10
    if ($response.status -ne "healthy") {
        throw "Health probe returned non-healthy payload: $($response | ConvertTo-Json)"
    }

    Write-Host "✅ Deployment verified: All pods healthy and responding." -ForegroundColor Green
}
catch {
    Write-Host "❌ Rollout or Health Verification Failed: $_" -ForegroundColor Red
    Write-Host "⚠️ Initiating Automatic Rollback to previous revision..." -ForegroundColor Yellow
    
    kubectl rollout undo deployment/clinixiq-backend -n $Namespace
    kubectl rollout undo deployment/clinixiq-frontend -n $Namespace
    
    Write-Host "⚠️ Rollback dispatched. Pod status:" -ForegroundColor Yellow
    kubectl get pods -n $Namespace
    exit 1
}
