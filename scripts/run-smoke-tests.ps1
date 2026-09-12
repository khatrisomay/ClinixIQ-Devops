# ==============================================================================
# ClinixIQ - Production Smoke Testing Automation (PowerShell)
# ==============================================================================
# Usage:
#   .\scripts\run-smoke-tests.ps1 -TargetUrl "http://localhost:8000"
# ==============================================================================

param (
    [Parameter(Mandatory=$false)]
    [string]$TargetUrl = "http://localhost:8000"
)

$ErrorActionPreference = "Continue"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$ReportDir = "reports\smoke_${Timestamp}"
New-Item -ItemType Directory -Force -Path $ReportDir | Out-Null

function Write-LogInfo { param($msg) Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-LogSuccess { param($msg) Write-Host "[SUCCESS] $msg" -ForegroundColor Green }
function Write-LogError { param($msg) Write-Host "[ERROR] $msg" -ForegroundColor Red }

Write-LogInfo "Starting ClinixIQ End-to-End Smoke Test Suite against: $TargetUrl"

$pythonExe = "python"
if (Test-Path "backend\venv\Scripts\python.exe") {
    $pythonExe = "backend\venv\Scripts\python.exe"
}

# 1. Run Core Smoke Probes
Write-LogInfo "Running Phase 1: Core API & Liveness Probes..."
& $pythonExe tests\smoke\smoke_runner.py --url $TargetUrl --report "$ReportDir\core_smoke.json"

# 2. Run Synthetic Patient Journey
Write-LogInfo "Running Phase 2: Synthetic Patient Diagnostic Journey..."
& $pythonExe tests\smoke\test_patient_journey.py --url $TargetUrl

# 3. Run Synthetic Billing Journey
Write-LogInfo "Running Phase 3: Synthetic Commercial Billing Journey..."
& $pythonExe tests\smoke\test_billing_journey.py --url $TargetUrl

Write-LogSuccess "All smoke test phases executed. Results saved to $ReportDir"
