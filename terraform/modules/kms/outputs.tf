# ==============================================================================
# ClinixIQ KMS Module - Outputs
# ==============================================================================

output "kms_key_arn" {
  description = "ARN of the platform master encryption key"
  value       = aws_kms_key.platform.arn
}

output "kms_key_id" {
  description = "Key ID of the platform master encryption key"
  value       = aws_kms_key.platform.key_id
}

output "kms_alias_arn" {
  description = "ARN of the platform key alias"
  value       = aws_kms_alias.platform.arn
}

output "storage_kms_key_arn" {
  description = "ARN of the dedicated S3 and DR backup encryption key"
  value       = aws_kms_key.storage.arn
}

output "storage_kms_key_id" {
  description = "Key ID of the storage encryption key"
  value       = aws_kms_key.storage.key_id
}
