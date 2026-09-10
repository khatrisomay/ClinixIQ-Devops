# ==============================================================================
# ClinixIQ ElastiCache Redis Module - Outputs
# ==============================================================================

output "primary_endpoint" {
  description = "Primary write endpoint address for Redis cluster"
  value       = aws_elasticache_replication_group.this.primary_endpoint_address
}

output "reader_endpoint" {
  description = "Reader load-balanced endpoint address for read-scaling"
  value       = aws_elasticache_replication_group.this.reader_endpoint_address
}

output "port" {
  description = "Port number on which the Redis cluster accepts connections"
  value       = aws_elasticache_replication_group.this.port
}

output "security_group_id" {
  description = "Security group ID guarding the Redis cluster"
  value       = aws_security_group.redis.id
}

output "replication_group_id" {
  description = "Identifier of the ElastiCache Replication Group"
  value       = aws_elasticache_replication_group.this.id
}
