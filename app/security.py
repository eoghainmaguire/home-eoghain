import hashlib
import time
from collections import defaultdict, deque

from flask import request


RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_REQUESTS = 20
_command_requests = defaultdict(deque)


def add_security_headers(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none'"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response


def hash_value(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def request_fingerprint():
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr or "unknown")
    first_ip = ip_address.split(",")[0].strip()
    user_agent = request.headers.get("User-Agent", "unknown")
    return hash_value(first_ip), hash_value(user_agent)


def is_rate_limited(ip_hash):
    now = time.time()
    requests = _command_requests[ip_hash]

    while requests and requests[0] <= now - RATE_LIMIT_WINDOW_SECONDS:
        requests.popleft()

    if len(requests) >= RATE_LIMIT_MAX_REQUESTS:
        return True

    requests.append(now)
    return False
