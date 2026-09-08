# ClinixIQ Semantic Version Release Helper (PowerShell)
param (
    [Parameter(Mandatory=$true)]
    [string]$Version,
    [string]$Message = "Release $Version"
)

$ErrorActionPreference = "Stop"

if ($Version -notmatch "^v\d+\.\d+\.\d+$") {
    Write-Host "❌ Version must follow semantic versioning tag format (e.g., v1.2.0)" -ForegroundColor Red
    exit 1
}

Write-Host "==> Creating Release Tag: $Version..." -ForegroundColor Cyan

# Verify working tree is clean
$status = git status --porcelain
if ($status) {
    Write-Host "❌ Working directory is not clean. Please commit changes first." -ForegroundColor Red
    exit 1
}

git tag -a $Version -m $Message
Write-Host "✅ Created Git tag '$Version'." -ForegroundColor Green
Write-Host "-> To push release: git push origin $Version" -ForegroundColor Yellow
