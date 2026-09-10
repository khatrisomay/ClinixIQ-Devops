# ==============================================================================
# ClinixIQ Application Load Balancer Module - Outputs
# ==============================================================================

output "alb_arn" {
  description = "The ARN of the Application Load Balancer"
  value       = aws_lb.this.arn
}

output "alb_dns_name" {
  description = "The public DNS name of the Application Load Balancer"
  value       = aws_lb.this.dns_name
}

output "alb_zone_id" {
  description = "The canonical hosted zone ID of the load balancer"
  value       = aws_lb.this.zone_id
}

output "frontend_target_group_arn" {
  description = "Target group ARN for ClinixIQ React frontend"
  value       = aws_lb_target_group.frontend.arn
}

output "backend_target_group_arn" {
  description = "Target group ARN for ClinixIQ FastAPI backend"
  value       = aws_lb_target_group.backend.arn
}

output "security_group_id" {
  description = "Security group ID attached to the ALB"
  value       = aws_security_group.alb.id
}

output "acm_certificate_arn" {
  description = "ARN of the provisioned ACM TLS certificate"
  value       = aws_acm_certificate.this.arn
}
