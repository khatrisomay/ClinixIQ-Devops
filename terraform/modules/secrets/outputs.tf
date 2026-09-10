# ==============================================================================
# ClinixIQ Secrets Manager Module - Outputs
# ==============================================================================

output "platform_secret_arn" {
  description = "ARN of the primary platform credentials secret"
  value       = aws_secretsmanager_secret.platform.arn
}

output "platform_secret_name" {
  description = "Name of the primary platform credentials secret"
  value       = aws_secretsmanager_secret.platform.name
}

output "redis_auth_secret_arn" {
  description = "ARN of the Redis AUTH token secret"
  value       = aws_secretsmanager_secret.redis_auth.arn
}

output "redis_auth_token_id" {
  description = "The raw Redis AUTH token string"
  value       = random_password.redis_auth.result
  sensitive   = true
}

output "secrets_reader_policy_arn" {
  description = "ARN of the IAM policy granting pods permission to read application secrets"
  value       = aws_iam_policy.secrets_reader.arn
}
