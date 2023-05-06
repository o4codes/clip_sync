from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.apps import users, auth
from src.config.middlewares.exception_handler import ExceptionHandlerMiddleware
from src.config.settings import Settings

# project wide settings
settings = Settings()

app = FastAPI(
    debug=True,
    title="ClipSync API Server",
    description="Backend Server for serving API to clip sync clients",
    docs_url=f"/api/{settings.version}/docs",
    redoc_url=f"/api/{settings.version}/swagger",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    ExceptionHandlerMiddleware, some_attribute="Error Handling Middleware"
)


@app.get(path="/ping")
def ping():
    return {"message": "pong"}


app.include_router(auth.router, prefix=f"/api/{settings.version}", tags=["AUTH"])
app.include_router(
    users.device_router, prefix=f"/api/{settings.version}", tags=["DEVICES"]
)
app.include_router(users.user_router, prefix=f"/api/{settings.version}", tags=["USERS"])
