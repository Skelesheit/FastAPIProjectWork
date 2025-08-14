import time, uuid, logging
from fastapi import Request

alog = logging.getLogger("access")

async def access_middleware(request: Request, call_next):
    rid = request.headers.get("X-Request-Id") or str(uuid.uuid4())
    request.state.request_id = rid

    t0 = time.perf_counter()
    resp = await call_next(request)
    dur_ms = int((time.perf_counter() - t0) * 1000)

    alog.info("access", extra=dict(
        request_id=rid,
        user_id=getattr(request.state, "user_id", None),
        method=request.method,
        path=str(request.url.path),
        status=resp.status_code,
        details={"duration_ms": dur_ms},
    ))
    resp.headers["X-Request-Id"] = rid
    return resp
