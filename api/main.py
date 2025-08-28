from fastapi import FastAPI
from .routes.targets import router as targets_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(targets_router)

