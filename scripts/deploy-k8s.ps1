# ClinixIQ Kubernetes Deployment Helper Script (PowerShell)
param (
    [ValidateSet("dev", "prod", "base")]
    [string]$Env = "dev",
    [switch]$DryRun,
    [switch]$Delete
)

$targetPath = if ($Env -eq "base") { "k8s/base" } else { "k8s/overlays/$Env" }
$action = if ($Delete) { "delete" } else { "apply" }

Write-Host "==> Executing kubectl $action on target: $targetPath..." -ForegroundColor Cyan

$cmdArgs = @($action, "-k", $targetPath)
if ($DryRun) {
    $cmdArgs += "--dry-run=client"
    Write-Host "-> Dry-run mode enabled (no cluster changes will be made)." -ForegroundColor Yellow
}

kubectl @cmdArgs

Write-Host "==> Execution completed successfully." -ForegroundColor Green
