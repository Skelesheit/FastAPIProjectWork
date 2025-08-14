from fastapi import Request

def common_extra(request: Request, **extra):
    return dict(extra=dict(
        request_id=getattr(request.state, "request_id", None),
        user_id=getattr(request.state, "user_id", None),
        path=str(request.url.path),
        method=request.method,
        **extra
    ))
