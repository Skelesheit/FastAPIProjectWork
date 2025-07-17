from fastapi import FastAPI
from src.auth import AuthMiddleware
app = FastAPI()

app.add_middleware(AuthMiddleware)
