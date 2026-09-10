# ==============================================================================
# ClinixIQ - Root Module Outputs
# ==============================================================================

output "vpc_id" {
  description = "The ID of the provisioned ClinixIQ VPC"
  value       = module.vpc.vpc_id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets across availability zones"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "IDs of the private subnets for EKS compute workloads"
  value       = module.vpc.private_subnet_ids
}

output "database_subnet_ids" {
  description = "IDs of the isolated database subnets for Redis state caching"
  value       = module.vpc.database_subnet_ids
}

output "eks_cluster_id" {
  description = "The ID and identifier of the Amazon EKS cluster"
  value       = module.eks.cluster_id
}

output "eks_cluster_endpoint" {
  description = "Kubernetes API server endpoint for cluster interaction"
  value       = module.eks.cluster_endpoint
}

output "eks_oidc_issuer_url" {
  description = "OIDC issuer URL for IAM Roles for Service Accounts (IRSA)"
  value       = module.eks.oidc_issuer_url
}

output "redis_primary_endpoint" {
  description = "Primary write endpoint address for ElastiCache Redis cluster"
  value       = module.redis.primary_endpoint
}

output "redis_reader_endpoint" {
  description = "Reader load-balanced endpoint address for read-heavy triage analytics"
  value       = module.redis.reader_endpoint
}

output "alb_dns_name" {
  description = "Public DNS name of the Application Load Balancer"
  value       = module.alb.alb_dns_name
}

output "kms_key_arn" {
  description = "ARN of the Customer-Managed KMS CMK used for platform envelope encryption"
  value       = module.kms.kms_key_arn
}

output "secrets_manager_secret_arn" {
  description = "ARN of the platform credentials secret in AWS Secrets Manager"
  value       = module.secrets.platform_secret_arn
}
