# ==============================================================================
# ClinixIQ KMS Module - Customer-Managed Keys & Envelope Encryption
# ==============================================================================

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# ------------------------------------------------------------------------------
# 1. Platform Master Encryption Key (EKS Secrets, Redis, Logs)
# ------------------------------------------------------------------------------
resource "aws_kms_key" "platform" {
  description             = "ClinixIQ Platform Master Envelope Encryption Key (HIPAA Compliant)"
  deletion_window_in_days = var.deletion_window_in_days
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Id      = "ClinixIQPlatformKmsPolicy"
    Statement = [
      # Account Root Administration
      {
        Sid    = "EnableRootIAMAccess"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      # CloudWatch Logs Encryption Permission
      {
        Sid    = "AllowCloudWatchLogs"
        Effect = "Allow"
        Principal = {
          Service = "logs.${data.aws_region.current.name}.amazonaws.com"
        }
        Action = [
          "kms:Encrypt*",
          "kms:Decrypt*",
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:Describe*"
        ]
        Resource = "*"
      },
      # ElastiCache Redis Encryption Permission
      {
        Sid    = "AllowElastiCacheEncryption"
        Effect = "Allow"
        Principal = {
          Service = "elasticache.amazonaws.com"
        }
        Action = [
          "kms:Encrypt*",
          "kms:Decrypt*",
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:Describe*"
        ]
        Resource = "*"
      },
      # Secrets Manager Integration
      {
        Sid    = "AllowSecretsManagerEncryption"
        Effect = "Allow"
        Principal = {
          Service = "secretsmanager.amazonaws.com"
        }
        Action = [
          "kms:Encrypt*",
          "kms:Decrypt*",
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:Describe*"
        ]
        Resource = "*"
      }
    ]
  })

  tags = merge(
    var.common_tags,
    {
      Name    = "${var.name_prefix}-platform-kms"
      Purpose = "Envelope-Encryption"
    }
  )
}

resource "aws_kms_alias" "platform" {
  name          = "alias/${var.name_prefix}-platform-key"
  target_key_id = aws_kms_key.platform.key_id
}

# ------------------------------------------------------------------------------
# 2. S3 Backup & Audit Log Dedicated KMS Key
# ------------------------------------------------------------------------------
resource "aws_kms_key" "storage" {
  description             = "ClinixIQ S3 Backup, DR Snapshots, and Audit Trail Encryption Key"
  deletion_window_in_days = var.deletion_window_in_days
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Id      = "ClinixIQStorageKmsPolicy"
    Statement = [
      {
        Sid    = "EnableRootIAMAccess"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "AllowS3ServiceUse"
        Effect = "Allow"
        Principal = {
          Service = "s3.amazonaws.com"
        }
        Action = [
          "kms:Encrypt*",
          "kms:Decrypt*",
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:Describe*"
        ]
        Resource = "*"
      }
    ]
  })

  tags = merge(
    var.common_tags,
    {
      Name    = "${var.name_prefix}-storage-kms"
      Purpose = "S3-DR-Storage-Encryption"
    }
  )
}

resource "aws_kms_alias" "storage" {
  name          = "alias/${var.name_prefix}-storage-key"
  target_key_id = aws_kms_key.storage.key_id
}
