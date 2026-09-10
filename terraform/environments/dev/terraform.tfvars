# ==============================================================================
# ClinixIQ - Development Environment Parameters (Cost-Optimized)
# ==============================================================================

aws_region                 = "us-east-1"
environment                = "dev"
project_name               = "clinixiq"

# Networking
vpc_cidr                   = "10.10.0.0/16"
availability_zones         = ["us-east-1a", "us-east-1b"]
enable_single_nat_gateway  = true

# Amazon EKS Kubernetes Cluster
eks_cluster_version        = "1.30"
eks_node_instance_types    = ["t3.medium"]
eks_node_desired_capacity  = 2
eks_node_min_capacity      = 1
eks_node_max_capacity      = 3

# ElastiCache Redis
redis_node_type            = "cache.t4g.small"
redis_num_cache_nodes      = 1
redis_multi_az_enabled     = false

# Application Load Balancer
domain_name                = "dev.clinixiq.health"
