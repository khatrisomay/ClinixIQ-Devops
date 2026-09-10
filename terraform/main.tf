# ==============================================================================
# ClinixIQ - Enterprise Cloud Infrastructure Root Module
# ==============================================================================

locals {
  name_prefix = "${var.project_name}-${var.environment}"
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
    Compliance  = "HIPAA-Security-Rule"
  }
}

# KMS Customer-Managed Encryption Keys Module
module "kms" {
  source      = "./modules/kms"
  name_prefix = local.name_prefix
  environment = var.environment
  common_tags = local.common_tags
}

# Networking & Multi-AZ VPC Module
module "vpc" {
  source                    = "./modules/vpc"
  name_prefix               = local.name_prefix
  vpc_cidr                  = var.vpc_cidr
  availability_zones        = var.availability_zones
  enable_single_nat_gateway = var.enable_single_nat_gateway
  kms_key_arn               = module.kms.kms_key_arn
  common_tags               = local.common_tags
}

# AWS Secrets Manager Module
module "secrets" {
  source      = "./modules/secrets"
  name_prefix = local.name_prefix
  environment = var.environment
  kms_key_arn = module.kms.kms_key_arn
  common_tags = local.common_tags
}

# Managed Amazon EKS Cluster Module
module "eks" {
  source           = "./modules/eks"
  name_prefix      = local.name_prefix
  environment      = var.environment
  vpc_id           = module.vpc.vpc_id
  subnet_ids       = module.vpc.private_subnet_ids
  cluster_version  = var.eks_cluster_version
  instance_types   = var.eks_node_instance_types
  desired_capacity = var.eks_node_desired_capacity
  min_capacity     = var.eks_node_min_capacity
  max_capacity     = var.eks_node_max_capacity
  kms_key_arn      = module.kms.kms_key_arn
  common_tags      = local.common_tags
}

# Managed ElastiCache Redis Replication Group Module
module "redis" {
  source                = "./modules/redis"
  name_prefix           = local.name_prefix
  vpc_id                = module.vpc.vpc_id
  database_subnet_ids   = module.vpc.database_subnet_ids
  eks_security_group_id = module.eks.node_security_group_id
  node_type             = var.redis_node_type
  num_cache_nodes       = var.redis_num_cache_nodes
  multi_az_enabled      = var.redis_multi_az_enabled
  kms_key_arn           = module.kms.kms_key_arn
  auth_token_secret_id  = module.secrets.redis_auth_token_id
  common_tags           = local.common_tags
}

# Application Load Balancer (ALB) Module with ACM TLS
module "alb" {
  source            = "./modules/alb"
  name_prefix       = local.name_prefix
  vpc_id            = module.vpc.vpc_id
  public_subnet_ids = module.vpc.public_subnet_ids
  domain_name       = var.domain_name
  common_tags       = local.common_tags
}
