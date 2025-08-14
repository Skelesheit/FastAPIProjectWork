from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from src import handlers
from src.handlers.error_handler import register_exception_handlers
from src.logging.access import access_middleware

# from src.auth import AuthMiddleware

app = FastAPI()

# MIDDLEWARE - CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # адрес фронта
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)
# MIDDLEWARE - ACCESS LOGGER
app.middleware("http")(access_middleware)

# ERRORS HANDLER
register_exception_handlers(app)

app.include_router(handlers.auth_router, prefix="/auth", tags=["auth"])
app.include_router(handlers.user_router, prefix="/user", tags=["user"])
app.include_router(handlers.client_router, prefix="/client", tags=["client"])
app.include_router(handlers.enterprise_router, prefix="/enterprise", tags=["enterprise"])

app.include_router(handlers.resource_router, prefix="/resources", )


@app.get('/')
def swagger():
    return RedirectResponse(url="/docs")
