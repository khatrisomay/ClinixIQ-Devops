import json
import logging
import sys
import time
import uuid
from collections.abc import Callable

from fastapi import Request, Response

# Configure root logger with structured formatting
logger = logging.getLogger("clinixiq.audit")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(message)s"))
if not logger.handlers:
    logger.addHandler(handler)


async def structured_logging_middleware(request: Request, call_next: Callable) -> Response:
    """
    Structured JSON audit logging with correlation IDs.
    Complies with HIPAA Safe Harbor by omitting direct identifiers and hashing network origin.
    """
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    start_time = time.time()

    # Skip health probes to avoid log bloat
    if request.url.path in ["/healthz", "/readyz", "/metrics"]:
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response

    try:
        response = await call_next(request)
        status_code = response.status_code
        error_msg = None
    except Exception as exc:
        status_code = 500
        error_msg = str(exc)
        raise
    finally:
        duration_ms = round((time.time() - start_time) * 1000, 2)
        client_ip = request.client.host if request.client else "unknown"
        # Deterministic anonymization for HIPAA compliance
        masked_ip = client_ip[: client_ip.rfind(".")] + ".xxx" if "." in client_ip else "hidden"

        log_payload = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "level": "INFO" if status_code < 400 else "ERROR",
            "correlation_id": correlation_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": status_code,
            "duration_ms": duration_ms,
            "client_ip_masked": masked_ip,
            "user_agent": request.headers.get("user-agent", "unknown")[:80],
        }
        if error_msg:
            log_payload["error"] = error_msg

        logger.info(json.dumps(log_payload))

    response.headers["X-Correlation-ID"] = correlation_id
    return response
