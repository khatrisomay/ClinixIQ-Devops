# ==============================================================================
# ClinixIQ - Terraform Remote State & Locking Configuration
# ==============================================================================
# For production deployments, state is maintained in an encrypted S3 bucket with
# DynamoDB table state locking to prevent concurrent apply race conditions.
#
# Production Usage:
# terraform init -backend-config="bucket=clinixiq-tf-state-prod" \
#                -backend-config="key=env/prod/terraform.tfstate" \
#                -backend-config="region=us-east-1" \
#                -backend-config="dynamodb_table=clinixiq-tf-locks"
# ==============================================================================

# terraform {
#   backend "s3" {
#     bucket         = "clinixiq-tf-state-prod"
#     key            = "env/prod/terraform.tfstate"
#     region         = "us-east-1"
#     dynamodb_table = "clinixiq-tf-locks"
#     encrypt        = true
#   }
# }
