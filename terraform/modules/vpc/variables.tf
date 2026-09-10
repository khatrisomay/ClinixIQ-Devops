# ==============================================================================
# ClinixIQ VPC Module - Input Variables
# ==============================================================================

variable "name_prefix" {
  description = "Prefix applied to all VPC resource names"
  type        = string
}

variable "vpc_cidr" {
  description = "Base IPv4 CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of target availability zones"
  type        = list(string)
}

variable "enable_single_nat_gateway" {
  description = "Provision a single shared NAT Gateway for cost-effective dev environments"
  type        = bool
  default     = true
}

variable "kms_key_arn" {
  description = "KMS Key ARN for VPC flow logs encryption"
  type        = string
}

variable "common_tags" {
  description = "Resource tags applied to all VPC components"
  type        = map(string)
  default     = {}
}
