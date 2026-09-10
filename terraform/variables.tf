# ==============================================================================
# ClinixIQ - Root Module Input Variables
# ==============================================================================

variable "aws_region" {
  description = "AWS primary region for all ClinixIQ cloud resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment tier (dev, staging, prod)"
  type        = string
  default     = "dev"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

variable "project_name" {
  description = "Base name for project resource naming conventions"
  type        = string
  default     = "clinixiq"
}

variable "vpc_cidr" {
  description = "IPv4 CIDR block for the ClinixIQ Virtual Private Cloud"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Target availability zones for multi-AZ high availability"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "enable_single_nat_gateway" {
  description = "Whether to provision a single shared NAT Gateway (cost optimization in dev)"
  type        = bool
  default     = true
}

variable "eks_cluster_version" {
  description = "Target Kubernetes version for the Amazon EKS cluster"
  type        = string
  default     = "1.30"
}

variable "eks_node_instance_types" {
  description = "EC2 instance types for EKS managed node groups"
  type        = list(string)
  default     = ["t3.medium"]
}

variable "eks_node_desired_capacity" {
  description = "Desired number of worker nodes in the primary node group"
  type        = number
  default     = 2
}

variable "eks_node_min_capacity" {
  description = "Minimum number of worker nodes for auto-scaling"
  type        = number
  default     = 1
}

variable "eks_node_max_capacity" {
  description = "Maximum number of worker nodes for auto-scaling capacity"
  type        = number
  default     = 5
}

variable "redis_node_type" {
  description = "ElastiCache Redis node compute classification"
  type        = string
  default     = "cache.t4g.small"
}

variable "redis_num_cache_nodes" {
  description = "Number of cluster replicas for Redis replication group"
  type        = number
  default     = 2
}

variable "redis_multi_az_enabled" {
  description = "Enable automatic multi-AZ failover for Redis replication group"
  type        = bool
  default     = true
}

variable "domain_name" {
  description = "Public domain name for Application Load Balancer ACM TLS certificate"
  type        = string
  default     = "clinixiq.health"
}
