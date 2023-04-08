from fastapi import FastAPI

app = FastAPI(
    debug=True,
    title="ClipSync API Server",
    description="Backend Server for serving API to clip sync clients",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/swagger"
)

@app.get(
    path="/ping"
)
def ping():
    return {
        "message":"pong"
    }