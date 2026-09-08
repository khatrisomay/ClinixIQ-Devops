# Security Policy & HIPAA Safeguards

## 🛡️ Supported Versions

ClinixIQ provides continuous security patches, vulnerability scans, and bug fixes for the following release tracks:

| Version Track | Supported          | Container Scans (Trivy) | Dependency Audits |
| :------------ | :----------------- | :---------------------- | :---------------- |
| `1.2.x`       | :white_check_mark: | Weekly / CI Trigger     | Daily             |
| `1.1.x`       | :white_check_mark: | Weekly                  | Weekly            |
| `< 1.0.0`     | :x:                | Deprecated              | Deprecated        |

---

## 🏥 Healthcare Data Safeguards & HIPAA Compliance

ClinixIQ is engineered with strict technical controls adhering to the **HIPAA Security Rule (45 CFR Part 160 and Part 164)**:

1. **De-Identification & Safe Harbor**:
   - Free-text symptom submissions are scrubbed of 18 direct HIPAA identifiers (names, MRNs, phone numbers, exact addresses) prior to ingestion by backend classification models.
2. **Encryption in Transit & at Rest**:
   - All external HTTP ingress traffic is terminated via **TLS 1.3**.
   - Intra-cluster container communication is partitioned using Kubernetes **NetworkPolicies** following a zero-trust model.
3. **Audit Logging & Cryptographic Integrity**:
   - Triage evaluations generate a deterministic SHA-256 MD verification hash for EHR audit verification.
   - Logs omit Personally Identifiable Information (PII) and Protected Health Information (PHI).

---

## 🔍 DevSecOps & Supply Chain Security

- **Container Image Scanning**: Every container build is audited using **Aqua Security Trivy** to block images containing `CRITICAL` or `HIGH` CVEs.
- **Secret Detection**: Git commits are validated by **Gitleaks** to prevent tokens or private keys from entering version control.
- **Non-Root Execution**: Container runtimes execute under unprivileged system users (`UID 10001` in Backend, `UID 101` in Frontend).

---

## 🚨 Reporting a Vulnerability

If you identify a security defect or vulnerability within the ClinixIQ platform:

1. **Do not create a public GitHub issue.**
2. Send a coordinated disclosure report to `security@clinixiq.io` with:
   - Detailed description of the vulnerability and attack vector.
   - Proof of Concept (PoC) or reproduction steps.
   - Affected service component (`backend`, `frontend`, `gateway`, `k8s`).
3. The ClinixIQ security team will acknowledge receipt within **24 hours** and provide a patch timeline within **72 hours**.
