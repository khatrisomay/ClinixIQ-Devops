# ==============================================================================
# ClinixIQ ElastiCache Redis Module - High-Availability Caching
# ==============================================================================

# Subnet Group for Isolated Database Subnets
resource "aws_elasticache_subnet_group" "this" {
  name        = "${var.name_prefix}-redis-subnet-group"
  description = "Subnet group for ClinixIQ Redis state and caching tier"
  subnet_ids  = var.database_subnet_ids

  tags = var.common_tags
}

# Dedicated Redis Security Group
resource "aws_security_group" "redis" {
  name        = "${var.name_prefix}-redis-sg"
  description = "Strict ingress security group for ClinixIQ ElastiCache Redis"
  vpc_id      = var.vpc_id

  ingress {
    description     = "Allow Redis traffic exclusively from EKS worker nodes"
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [var.eks_security_group_id]
  }

  egress {
    description = "Allow all outbound responses"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    var.common_tags,
    {
      Name = "${var.name_prefix}-redis-sg"
    }
  )
}

# Parameter Group with HIPAA eviction & keepalive tuning
resource "aws_elasticache_parameter_group" "this" {
  name        = "${var.name_prefix}-redis-params"
  family      = "redis7"
  description = "Optimized parameters for ClinixIQ high-throughput triage caching"

  parameter {
    name  = "maxmemory-policy"
    value = "volatile-lru"
  }

  parameter {
    name  = "timeout"
    value = "300"
  }

  parameter {
    name  = "tcp-keepalive"
    value = "60"
  }

  tags = var.common_tags
}

# High-Availability Redis Replication Group
resource "aws_elasticache_replication_group" "this" {
  replication_group_id = "${var.name_prefix}-redis"
  description          = "ClinixIQ distributed triage cache and session store"
  engine               = "redis"
  engine_version       = "7.1"
  node_type            = var.node_type
  num_cache_clusters   = var.num_cache_nodes
  port                 = 6379

  subnet_group_name    = aws_elasticache_subnet_group.this.name
  security_group_ids   = [aws_security_group.redis.id]
  parameter_group_name = aws_elasticache_parameter_group.this.name

  automatic_failover_enabled = var.multi_az_enabled
  multi_az_enabled           = var.multi_az_enabled

  at_rest_encryption_enabled = true
  kms_key_id                 = var.kms_key_arn
  transit_encryption_enabled = true
  auth_token                 = length(var.auth_token_secret_id) >= 16 ? var.auth_token_secret_id : null

  snapshot_retention_limit = 7
  snapshot_window          = "03:00-05:00"
  maintenance_window       = "sun:05:00-sun:07:00"
  auto_minor_version_upgrade = true

  tags = merge(
    var.common_tags,
    {
      Name = "${var.name_prefix}-redis-cluster"
    }
  )
}
