from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from src import handlers

# from src.auth import AuthMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware)
# app.add_middleware(AuthMiddleware)

app.include_router(handlers.auth_router, prefix="/auth", tags=["auth"])
app.include_router(handlers.user_router, prefix="/user", tags=["user"])
app.include_router(handlers.client_router, prefix="/client", tags=["client"])
app.include_router(handlers.enterprise_router, prefix="/enterprise", tags=["enterprise"])


@app.get('/')
def swagger():
    return RedirectResponse(url="/docs")
