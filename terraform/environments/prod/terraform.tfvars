# ==============================================================================
# ClinixIQ - Production Environment Parameters (High-Availability & Fault-Tolerant)
# ==============================================================================

aws_region                 = "us-east-1"
environment                = "prod"
project_name               = "clinixiq"

# Networking (Multi-AZ HA)
vpc_cidr                   = "10.20.0.0/16"
availability_zones         = ["us-east-1a", "us-east-1b", "us-east-1c"]
enable_single_nat_gateway  = false

# Amazon EKS Kubernetes Cluster (Enterprise Workloads)
eks_cluster_version        = "1.30"
eks_node_instance_types    = ["m6i.large", "c6i.large"]
eks_node_desired_capacity  = 3
eks_node_min_capacity      = 2
eks_node_max_capacity      = 10

# ElastiCache Redis (Multi-AZ with Auto-Failover)
redis_node_type            = "cache.m6g.large"
redis_num_cache_nodes      = 3
redis_multi_az_enabled     = true

# Application Load Balancer (Production Apex Domain)
domain_name                = "clinixiq.health"
