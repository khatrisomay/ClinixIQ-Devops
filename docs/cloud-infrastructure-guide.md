# ClinixIQ - Cloud Infrastructure & Terraform Architecture Guide

## 1. Architectural Overview

ClinixIQ deploys a fault-tolerant, multi-tier, multi-AZ cloud architecture on Amazon Web Services (AWS) using modular Terraform (HCL). The infrastructure adheres to the **AWS Well-Architected Framework** and satisfies **HIPAA Security Rule** compliance requirements for safeguarding Protected Health Information (PHI).

```
                      INTERNET / CLIENT TRAFFIC
                                 │
                                 │ HTTPS (Port 443 / TLS 1.3)
                                 ▼
                     [ Application Load Balancer ]
                        (Public Subnets 10.0.1.0/24, etc.)
                                 │
                 ┌───────────────┴───────────────┐
                 │ Path: /*                      │ Path: /api/*, /metrics
                 ▼                               ▼
       [ Frontend Target Group ]       [ Backend Target Group ]
                 │                               │
═════════════════╪═══════════════════════════════╪══════════════════════════════
  PRIVATE VPC    │                               │
                 ▼                               ▼
       [ React UI Pods ]               [ FastAPI ML Microservice Pods ]
         (EKS Node Group)                 (EKS Node Group with IRSA)
                                                 │
                                                 │ Port 6379 (TLS 1.3 + AUTH)
                                                 ▼
                                    [ ElastiCache Redis Cluster ]
                                      (Isolated Database Subnets)
                                                 │
                                                 ▼
                                     [ KMS Customer-Managed Key ]
                                       (Hardware Envelope Encryption)
```

---

## 2. Infrastructure as Code Module Matrix

| Module | Location | Purpose | Key Resources |
|---|---|---|---|
| **Root** | `terraform/` | Module composition & environment inputs | `aws_provider`, backend state, global tags |
| **VPC** | `terraform/modules/vpc` | 3-Tier Multi-AZ networking | `aws_vpc`, `aws_subnet`, `aws_nat_gateway`, `aws_flow_log` |
| **EKS** | `terraform/modules/eks` | Managed Kubernetes compute | `aws_eks_cluster`, `aws_eks_node_group`, OIDC IRSA, add-ons |
| **Redis** | `terraform/modules/redis` | Distributed caching & session store | `aws_elasticache_replication_group`, `aws_elasticache_subnet_group` |
| **ALB** | `terraform/modules/alb` | Ingress traffic routing & TLS | `aws_lb`, `aws_lb_target_group`, `aws_acm_certificate`, rules |
| **KMS** | `terraform/modules/kms` | Hardware envelope encryption | `aws_kms_key`, `aws_kms_alias`, rotation policies |
| **Secrets** | `terraform/modules/secrets` | HIPAA credential management | `aws_secretsmanager_secret`, IRSA retrieval IAM policies |

---

## 3. Network Subnet Allocations

The VPC allocates CIDRs across three Availability Zones to prevent single-datacenter failure:

| Tier | Availability Zone | CIDR Block | Routing / Ingress |
|---|---|---|---|
| **Public A** | `us-east-1a` | `10.0.1.0/24` | Internet Gateway, ALB Ingress, NAT Gateway 1 |
| **Public B** | `us-east-1b` | `10.0.2.0/24` | Internet Gateway, ALB Ingress, NAT Gateway 2 |
| **Public C** | `us-east-1c` | `10.0.3.0/24` | Internet Gateway, ALB Ingress, NAT Gateway 3 |
| **Private Compute A** | `us-east-1a` | `10.0.10.0/24` | EKS Managed Node Group (Worker Nodes) |
| **Private Compute B** | `us-east-1b` | `10.0.11.0/24` | EKS Managed Node Group (Worker Nodes) |
| **Private Compute C** | `us-east-1c` | `10.0.12.0/24` | EKS Managed Node Group (Worker Nodes) |
| **Database A** | `us-east-1a` | `10.0.20.0/24` | ElastiCache Redis Node 1 (Isolated, No IGW) |
| **Database B** | `us-east-1b` | `10.0.21.0/24` | ElastiCache Redis Node 2 (Replica) |
| **Database C** | `us-east-1c` | `10.0.22.0/24` | ElastiCache Redis Node 3 (Replica) |

---

## 4. Multi-Environment Sizing & Cost Matrix

| Feature | Development (`dev`) | Production (`prod`) |
|---|---|---|
| **NAT Gateways** | 1 (Shared across AZs for cost savings) | 3 (1 per AZ for high availability) |
| **EKS Nodes** | 2 x `t3.medium` (Min 1, Max 3) | 3 x `m6i.large` (Min 2, Max 10) |
| **Redis Cache** | 1 Node (`cache.t4g.small`) | 3 Nodes (`cache.m6g.large`, Multi-AZ) |
| **Multi-AZ Failover** | Disabled | Enabled (Automatic failover < 30s) |
| **Audit Logs Retention** | 30 Days | 365 Days (HIPAA compliance) |

---

## 5. Security & HIPAA Safeguards

1. **Envelope Encryption at Rest**:
   - Every sensitive data store (EKS Kubernetes Secrets, ElastiCache Redis state, CloudWatch audit logs, S3 backup bundles) is encrypted with Customer-Managed Keys (CMKs) configured with mandatory annual rotation.
2. **Strict In-Transit Encryption**:
   - ALB terminates TLS 1.3/1.2 using modern cipher suites (`ELBSecurityPolicy-TLS13-1-2-2021-06`).
   - Redis cluster enforces `transit_encryption_enabled = true` and `auth_token` verification.
3. **IAM Roles for Service Accounts (IRSA)**:
   - Pods assume least-privilege AWS IAM roles via OpenID Connect (OIDC) federation, eliminating static AWS access keys on worker nodes.
4. **VPC Flow Logs**:
   - Continuous network traffic capture stored in KMS-encrypted CloudWatch log groups for security forensics.

---

## 6. Disaster Recovery & Backup Runbook

- **Recovery Point Objective (RPO)**: < 15 minutes.
- **Recovery Time Objective (RTO)**: < 30 minutes.

### Triggering Automated Backup
```bash
# Linux / macOS
./scripts/backup-restore.sh backup prod

# Windows PowerShell
.\scripts\backup-restore.ps1 -Action backup -Environment prod
```

### Validating Recovery Snapshots
```bash
# Linux / macOS
./scripts/backup-restore.sh verify-snapshots prod

# Windows PowerShell
.\scripts\backup-restore.ps1 -Action verify-snapshots -Environment prod
```

---

## 7. Terraform Deployment Procedures

### Pre-requisites
- Terraform CLI `v1.5.0+`
- AWS CLI configured with administrator or deployment role

### Validation & Planning
```bash
# Validate HCL and syntax
./scripts/tf-deploy.sh validate dev

# Generate speculative plan
./scripts/tf-deploy.sh plan dev
```

### Applying Changes
```bash
./scripts/tf-deploy.sh apply dev
```
