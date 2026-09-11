# ClinixIQ - Commercial Monetization, Stripe Integration & Billing Guide

## 1. Executive Summary & Monetization Architecture

ClinixIQ features a production-grade, PCI-DSS compliant commercial monetization engine. The billing subsystem enables subscription lifecycle management, self-service Stripe Checkout sessions, customer billing portals, asynchronous webhook processing with HMAC-SHA256 signature verification, and usage-based clinical quota metering.

```
 [ Patient / Clinician ]
           │
           │ 1. Select Plan (Starter / Pro / Enterprise)
           ▼
 [ ClinixIQ React UI ]
           │
           │ 2. POST /api/billing/create-checkout-session
           ▼
 [ FastAPI Billing Engine ]
           │
           │ 3. Initialize Stripe Checkout Session
           ▼
     [ Stripe API ] ────────────────────────────────┐
           │                                        │
           │ 4. Redirect User to Hosted Payment UI  │
           ▼                                        │ 5. Asynchronous Webhook
 [ Patient Completes Checkout ]                     │    (checkout.session.completed)
           │                                        ▼
           │ 6. Redirect back to ClinixIQ   [ Webhook Endpoint ]
           ▼      (?status=success)          (/api/webhooks/stripe)
 [ Pro Features Unlocked ]                          │
                                                    ├─ HMAC-SHA256 Sig Check
                                                    ├─ Redis Idempotency Lock
                                                    ▼
                                            [ Billing Repository ]
                                              (Redis Multi-AZ Store)
```

---

## 2. Clinical SaaS Plan Catalog

| Plan Tier | Monthly Price | Annual Rate (Save 20%) | Monthly Triage Quota | Core Capabilities |
|---|---|---|---|---|
| **Starter** | **$0.00** | $0.00 | 5 evaluations / mo | Basic acute symptom triage, top 3 differentials, home-care guidance |
| **Pro** | **$9.99 / mo** | $7.99 / mo | **Unlimited** | Doctor-ready SBAR PDF export, longitudinal risk curves, priority ML queue (<50ms) |
| **Enterprise** | **$149.00 / mo** | $119.00 / mo | 10,000 queries / mo | Dedicated Kubernetes ingress endpoint, custom disease weighting, 99.9% uptime SLA |

---

## 3. Webhook Event Processing Matrix

All asynchronous state transitions are driven by cryptographically verified Stripe Webhook events:

| Stripe Event Name | Handled In | State Transition / Business Action |
|---|---|---|
| `checkout.session.completed` | `webhook_dispatcher.py` | Activates customer subscription, saves `sub_id`, and sets status to `active` |
| `customer.subscription.created` | `webhook_dispatcher.py` | Associates Stripe subscription ID with customer profile |
| `customer.subscription.updated` | `webhook_dispatcher.py` | Synchronizes status (`active`, `past_due`, `canceled`) and renewal dates |
| `customer.subscription.deleted` | `webhook_dispatcher.py` | Downgrades customer to `starter` tier and marks subscription `canceled` |
| `invoice.payment_succeeded` | `webhook_dispatcher.py` | Confirms payment, maintains active state, and resets monthly usage quota |
| `invoice.payment_failed` | `webhook_dispatcher.py` | Marks subscription status `past_due` and logs financial audit alert |

---

## 4. Security, Idempotency & Compliance

### 4.1. HMAC-SHA256 Cryptographic Verification
Webhooks require signature validation against `STRIPE_WEBHOOK_SECRET`:
```python
event = stripe.Webhook.construct_event(
    payload=raw_bytes,
    sig_header=stripe_signature,
    secret=billing_settings.STRIPE_WEBHOOK_SECRET
)
```

### 4.2. Redis-Backed Idempotency Guard
To defend against duplicate webhook deliveries and network replays:
- Every Stripe `event.id` is claimed atomically using Redis `SET clinixiq:idempotency:stripe:<event_id> "processed" EX 86400 NX`.
- If key already exists, the event is immediately acknowledged (`HTTP 200`) without redundant execution.

### 4.3. Quota Guard & HTTP 402 Enforcement
The clinical inference pipeline checks quota before executing ML models:
```
GET /api/v1/triage/predict
├── Look up active plan tier
├── Check monthly usage: count >= quota_limit
│   ├── YES: Reject with HTTP 402 Payment Required
│   └── NO:  Increment counter & proceed to inference
```

---

## 5. Local Development & Stripe CLI Runbook

### Testing with Offline Mock Mode (Default)
When `STRIPE_SECRET_KEY` is not provided or starts with `clinixiq-`:
- System automatically runs in **resilient mock mode**.
- Checkout sessions generate instant mock redirect URLs (`cs_mock_*`).
- Customer portal generates local mock URLs (`?portal=active`).
- 100% test pass rate in CI without external network access.

### Testing with Live Stripe CLI
To test live webhooks locally:
```bash
# 1. Install & Authenticate Stripe CLI
stripe login

# 2. Forward Webhooks to Local FastAPI Backend
stripe listen --forward-to localhost:8000/api/webhooks/stripe

# 3. Trigger Synthetic Test Events
stripe trigger checkout.session.completed
stripe trigger invoice.payment_succeeded
stripe trigger customer.subscription.deleted
```

---

## 6. Financial Telemetry & Observability

Prometheus metrics exposed at `/metrics`:
- `active_subscriptions_total{tier="pro|enterprise"}`: Active paying customer gauge.
- `monthly_recurring_revenue_dollars{tier="pro|enterprise"}`: Estimated MRR.
- `stripe_webhook_events_total{event_type, status}`: Webhook delivery reliability counter.
- `stripe_checkout_sessions_total{tier, billing_cycle}`: Checkout conversion funnel tracking.
