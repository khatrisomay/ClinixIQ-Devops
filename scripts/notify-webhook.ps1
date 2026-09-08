# ClinixIQ Webhook Notification Dispatcher (PowerShell)
param (
    [Parameter(Mandatory=$true)]
    [string]$WebhookUrl,
    [ValidateSet("SUCCESS", "FAILURE", "WARNING")]
    [string]$Status = "SUCCESS",
    [string]$BuildNumber = "local",
    [string]$Branch = "main"
)

$color = switch ($Status) {
    "SUCCESS" { 3066993 } # Green
    "FAILURE" { 15158332 } # Red
    "WARNING" { 15105570 } # Orange
}

$payload = @{
    username = "ClinixIQ CI/CD Bot"
    embeds = @(
        @{
            title = "ClinixIQ Deployment Status: $Status"
            color = $color
            fields = @(
                @{ name = "Build"; value = $BuildNumber; inline = $true },
                @{ name = "Branch"; value = $Branch; inline = $true },
                @{ name = "Platform"; value = "Kubernetes / Helm"; inline = $true }
            )
            timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
        }
    )
} | ConvertTo-Json -Depth 4

Write-Host "==> Sending webhook notification to $WebhookUrl..." -ForegroundColor Cyan

try {
    Invoke-RestMethod -Uri $WebhookUrl -Method Post -Body $payload -ContentType "application/json"
    Write-Host "✅ Notification dispatched successfully." -ForegroundColor Green
}
catch {
    Write-Host "⚠️ Failed to send notification: $_" -ForegroundColor Yellow
}
