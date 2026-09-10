# ==============================================================================
# ClinixIQ EKS Module - Input Variables
# ==============================================================================

variable "name_prefix" {
  description = "Prefix applied to all EKS resource names"
  type        = string
}

variable "environment" {
  description = "Environment tier (dev, staging, prod)"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID where the cluster and nodes reside"
  type        = string
}

variable "subnet_ids" {
  description = "Private subnet IDs for EKS worker nodes"
  type        = list(string)
}

variable "cluster_version" {
  description = "Target Kubernetes control plane version"
  type        = string
  default     = "1.30"
}

variable "instance_types" {
  description = "EC2 instance types for the managed worker node group"
  type        = list(string)
  default     = ["t3.medium"]
}

variable "desired_capacity" {
  description = "Desired number of worker nodes in node group"
  type        = number
  default     = 2
}

variable "min_capacity" {
  description = "Minimum number of worker nodes"
  type        = number
  default     = 1
}

variable "max_capacity" {
  description = "Maximum number of worker nodes"
  type        = number
  default     = 5
}

variable "kms_key_arn" {
  description = "KMS Key ARN for Kubernetes envelope encryption (secrets)"
  type        = string
}

variable "common_tags" {
  description = "Resource tags applied to all EKS components"
  type        = map(string)
  default     = {}
}
