import functools
import logging
from collections.abc import Callable
from contextlib import contextmanager
from typing import Any

logger = logging.getLogger("clinixiq.tracing")

# Try initializing OpenTelemetry; fallback gracefully if not present
try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider

    provider = TracerProvider()
    trace.set_tracer_provider(provider)
    _tracer = trace.get_tracer("clinixiq-tracer", "1.0.0")
    HAS_OTEL = True
except Exception as e:
    logger.debug("OpenTelemetry SDK not initialized (%s). Using no-op tracer.", e)
    _tracer = None
    HAS_OTEL = False


@contextmanager
def trace_span(name: str, attributes: dict[str, Any] | None = None):
    """Context manager creating OpenTelemetry trace spans with metadata."""
    if HAS_OTEL and _tracer:
        with _tracer.start_as_current_span(name) as span:
            if attributes:
                for k, v in attributes.items():
                    span.set_attribute(k, str(v))
            yield span
    else:
        yield None


def traced(span_name: str):
    """Function decorator creating an execution span."""

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with trace_span(span_name):
                return func(*args, **kwargs)

        return wrapper

    return decorator
