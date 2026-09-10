# ==============================================================================
# ClinixIQ Secrets Manager Module - Input Variables
# ==============================================================================

variable "name_prefix" {
  description = "Prefix applied to all Secrets Manager resources"
  type        = string
}

variable "environment" {
  description = "Target deployment environment (dev, staging, prod)"
  type        = string
}

variable "kms_key_arn" {
  description = "Customer-Managed KMS Key ARN used to encrypt Secrets Manager payloads"
  type        = string
}

variable "common_tags" {
  description = "Resource tags applied to Secrets Manager resources"
  type        = map(string)
  default     = {}
}
