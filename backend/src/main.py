from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.middlewares.exception_handler import ExceptionHandlerMiddleware

app = FastAPI(
    debug=True,
    title="ClipSync API Server",
    description="Backend Server for serving API to clip sync clients",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/swagger"
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


@app.get(
    path="/ping"
)
def ping():
    return {
        "message":"pong"
    }