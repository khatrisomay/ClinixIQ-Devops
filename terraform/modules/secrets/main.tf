# ==============================================================================
# ClinixIQ Secrets Manager Module - HIPAA Secrets & Encryption
# ==============================================================================

# Cryptographically strong random password for Redis in-transit AUTH
resource "random_password" "redis_auth" {
  length  = 32
  special = false # Redis AUTH token alphanumeric compatibility
}

# Cryptographically strong random secret for JWT token signing
resource "random_password" "jwt_secret" {
  length  = 64
  special = false
}

# ------------------------------------------------------------------------------
# 1. Dedicated Redis Auth Token Secret
# ------------------------------------------------------------------------------
resource "aws_secretsmanager_secret" "redis_auth" {
  name                    = "${var.name_prefix}-redis-auth-token"
  description             = "ClinixIQ ElastiCache Redis replication group auth token"
  kms_key_id              = var.kms_key_arn
  recovery_window_in_days = 0

  tags = var.common_tags
}

resource "aws_secretsmanager_secret_version" "redis_auth" {
  secret_id     = aws_secretsmanager_secret.redis_auth.id
  secret_string = random_password.redis_auth.result
}

# ------------------------------------------------------------------------------
# 2. Main Platform Secret Container (Stripe, JWT, App Config)
# ------------------------------------------------------------------------------
resource "aws_secretsmanager_secret" "platform" {
  name                    = "${var.name_prefix}-platform-credentials"
  description             = "ClinixIQ application secrets including JWT, Stripe API, and Redis credentials"
  kms_key_id              = var.kms_key_arn
  recovery_window_in_days = 0

  tags = var.common_tags
}

resource "aws_secretsmanager_secret_version" "platform" {
  secret_id = aws_secretsmanager_secret.platform.id
  secret_string = jsonencode({
    ENVIRONMENT           = var.environment
    JWT_SECRET_KEY        = random_password.jwt_secret.result
    REDIS_PASSWORD        = random_password.redis_auth.result
    STRIPE_SECRET_KEY     = "clinixiq-mock-stripe-secret-token"
    STRIPE_WEBHOOK_SECRET = "whsec_clinixiq_mock_webhook_secret"
  })
}

# ------------------------------------------------------------------------------
# 3. Least-Privilege IAM Policy for Pods / IRSA Secrets Access
# ------------------------------------------------------------------------------
resource "aws_iam_policy" "secrets_reader" {
  name        = "${var.name_prefix}-secrets-reader-policy"
  description = "Allows ClinixIQ Kubernetes pods to retrieve platform credentials from Secrets Manager"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowSecretFetch"
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resource = [
          aws_secretsmanager_secret.platform.arn,
          aws_secretsmanager_secret.redis_auth.arn
        ]
      },
      {
        Sid    = "AllowKmsDecrypt"
        Effect = "Allow"
        Action = [
          "kms:Decrypt",
          "kms:DescribeKey"
        ]
        Resource = var.kms_key_arn
      }
    ]
  })

  tags = var.common_tags
}
