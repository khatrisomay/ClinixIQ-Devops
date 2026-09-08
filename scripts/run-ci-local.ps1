# ClinixIQ Local CI Pipeline Simulator (PowerShell)
$ErrorActionPreference = "Continue"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   ClinixIQ Local CI/CD Pipeline Simulator                " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$results = @{}

# 1. Backend Linting
Write-Host "`n[Stage 1/5] Backend Linting..." -ForegroundColor Yellow
if (Get-Command ruff -ErrorAction SilentlyContinue) {
    ruff check backend/
    $results["Backend Lint"] = if ($LASTEXITCODE -eq 0) { "PASSED" } else { "FAILED" }
} else {
    Write-Host "Ruff not found on PATH; skipping lint step." -ForegroundColor DarkGray
    $results["Backend Lint"] = "SKIPPED"
}

# 2. Pytest Test Suite
Write-Host "`n[Stage 2/5] Backend Pytest Suite with Coverage..." -ForegroundColor Yellow
$py = if (Test-Path "backend/venv/Scripts/pytest.exe") { "backend/venv/Scripts/pytest.exe" } else { "pytest" }
& $py -v --cov=app backend/tests/
$results["Unit Tests"] = if ($LASTEXITCODE -eq 0) { "PASSED" } else { "FAILED" }

# 3. Frontend Build Verification
Write-Host "`n[Stage 3/5] Frontend Production Build..." -ForegroundColor Yellow
Push-Location frontend
npm run build
$results["Frontend Build"] = if ($LASTEXITCODE -eq 0) { "PASSED" } else { "FAILED" }
Pop-Location

# 4. Kubernetes Dry-Run Validation
Write-Host "`n[Stage 4/5] Kubernetes Manifests Dry-Run..." -ForegroundColor Yellow
if (Get-Command kubectl -ErrorAction SilentlyContinue) {
    kubectl apply --dry-run=client -k k8s/base
    $results["K8s Validation"] = if ($LASTEXITCODE -eq 0) { "PASSED" } else { "FAILED" }
} else {
    Write-Host "kubectl not found on PATH; skipping." -ForegroundColor DarkGray
    $results["K8s Validation"] = "SKIPPED"
}

# 5. Helm Chart Linting
Write-Host "`n[Stage 5/5] Helm Chart Linting..." -ForegroundColor Yellow
if (Get-Command helm -ErrorAction SilentlyContinue) {
    helm lint helm/clinixiq
    $results["Helm Lint"] = if ($LASTEXITCODE -eq 0) { "PASSED" } else { "FAILED" }
} else {
    Write-Host "helm not found on PATH; skipping." -ForegroundColor DarkGray
    $results["Helm Lint"] = "SKIPPED"
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host "   CI Simulation Summary Results                          " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
foreach ($key in $results.Keys) {
    $status = $results[$key]
    $color = if ($status -eq "PASSED") { "Green" } elseif ($status -eq "SKIPPED") { "DarkGray" } else { "Red" }
    Write-Host ("{0,-25} : {1}" -f $key, $status) -ForegroundColor $color
}
Write-Host "==========================================================" -ForegroundColor Cyan
