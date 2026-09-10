# ==============================================================================
# ClinixIQ Application Load Balancer Module - Input Variables
# ==============================================================================

variable "name_prefix" {
  description = "Prefix applied to all ALB resource names"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID where the ALB and Target Groups are deployed"
  type        = string
}

variable "public_subnet_ids" {
  description = "List of public subnet IDs across multiple AZs"
  type        = list(string)
}

variable "domain_name" {
  description = "Domain name for ACM TLS certificate generation"
  type        = string
  default     = "clinixiq.health"
}

variable "common_tags" {
  description = "Resource tags applied to all ALB components"
  type        = map(string)
  default     = {}
}
