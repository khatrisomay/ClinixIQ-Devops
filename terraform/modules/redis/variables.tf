# ==============================================================================
# ClinixIQ ElastiCache Redis Module - Input Variables
# ==============================================================================

variable "name_prefix" {
  description = "Prefix applied to all Redis resource names"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID where Redis is deployed"
  type        = string
}

variable "database_subnet_ids" {
  description = "Isolated database subnet IDs for Redis subnet group"
  type        = list(string)
}

variable "eks_security_group_id" {
  description = "Security group ID of EKS worker nodes to authorize ingress"
  type        = string
}

variable "node_type" {
  description = "Instance compute class for ElastiCache Redis nodes"
  type        = string
  default     = "cache.t4g.small"
}

variable "num_cache_nodes" {
  description = "Total number of nodes (1 primary + replicas) in the replication group"
  type        = number
  default     = 2
}

variable "multi_az_enabled" {
  description = "Enable automatic multi-AZ failover"
  type        = bool
  default     = true
}

variable "kms_key_arn" {
  description = "KMS Customer-Managed Key ARN for encryption-at-rest"
  type        = string
}

variable "auth_token_secret_id" {
  description = "Authentication token for Redis in-transit TLS AUTH"
  type        = string
  default     = ""
  sensitive   = true
}

variable "common_tags" {
  description = "Resource tags applied to all Redis components"
  type        = map(string)
  default     = {}
}
