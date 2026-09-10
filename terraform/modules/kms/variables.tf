# ==============================================================================
# ClinixIQ KMS Module - Input Variables
# ==============================================================================

variable "name_prefix" {
  description = "Prefix applied to all KMS key aliases and descriptions"
  type        = string
}

variable "environment" {
  description = "Target deployment environment (dev, staging, prod)"
  type        = string
}

variable "deletion_window_in_days" {
  description = "Waiting period, specified in number of days, before key destruction"
  type        = number
  default     = 30
}

variable "common_tags" {
  description = "Resource tags applied to KMS keys"
  type        = map(string)
  default     = {}
}
