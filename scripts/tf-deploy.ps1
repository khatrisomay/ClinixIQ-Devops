# ==============================================================================
# ClinixIQ - Terraform Deployment Lifecycle Automation (PowerShell)
# ==============================================================================
# Usage:
#   .\scripts\tf-deploy.ps1 -Action validate -Environment dev
#   .\scripts\tf-deploy.ps1 -Action plan -Environment dev
#   .\scripts\tf-deploy.ps1 -Action apply -Environment dev
# ==============================================================================

param (
    [Parameter(Mandatory=$false)]
    [ValidateSet("init", "validate", "plan", "apply", "destroy")]
    [string]$Action = "validate",

    [Parameter(Mandatory=$false)]
    [ValidateSet("dev", "prod")]
    [string]$Environment = "dev"
)

$ErrorActionPreference = "Stop"
$TfDir = "terraform"
$VarFile = "environments\$Environment\terraform.tfvars"
$PlanFile = "tfplan-$Environment.binary"

function Write-LogInfo { param($msg) Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-LogSuccess { param($msg) Write-Host "[SUCCESS] $msg" -ForegroundColor Green }
function Write-LogWarn { param($msg) Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-LogError { param($msg) Write-Host "[ERROR] $msg" -ForegroundColor Red }

if (-not (Test-Path $TfDir)) {
    Write-LogError "Terraform directory '$TfDir' not found."
    exit 1
}

switch ($Action) {
    "init" {
        Write-LogInfo "Initializing Terraform modules and provider plugins..."
        terraform -chdir=$TfDir init -backend=false
        Write-LogSuccess "Terraform initialization complete."
    }

    "validate" {
        Write-LogInfo "Verifying HCL formatting and syntax validation..."
        terraform fmt -check -recursive $TfDir
        terraform -chdir=$TfDir init -backend=false
        terraform -chdir=$TfDir validate
        Write-LogSuccess "Terraform validation passed successfully."
    }

    "plan" {
        Write-LogInfo "Generating speculative execution plan for [$Environment]..."
        terraform -chdir=$TfDir plan -var-file=$VarFile -out=$PlanFile
        Write-LogSuccess "Plan saved to $TfDir\$PlanFile"
    }

    "apply" {
        Write-LogInfo "Applying execution plan for [$Environment]..."
        if (-not (Test-Path "$TfDir\$PlanFile")) {
            Write-LogWarn "No saved plan found. Generating new plan..."
            terraform -chdir=$TfDir plan -var-file=$VarFile -out=$PlanFile
        }
        terraform -chdir=$TfDir apply "$PlanFile"
        Remove-Item "$TfDir\$PlanFile" -Force -ErrorAction SilentlyContinue
        Write-LogSuccess "Terraform apply completed for [$Environment]."
    }

    "destroy" {
        Write-LogWarn "CRITICAL WARNING: Initiating infrastructure destruction for [$Environment]!"
        $Confirm = Read-Host "Type the environment name '$Environment' to proceed"
        if ($Confirm -eq $Environment) {
            terraform -chdir=$TfDir destroy -var-file=$VarFile
            Write-LogSuccess "Infrastructure successfully destroyed."
        } else {
            Write-LogError "Confirmation mismatch. Destruction aborted."
        }
    }
}
