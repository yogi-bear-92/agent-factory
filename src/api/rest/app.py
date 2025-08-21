from __future__ import annotations

from fastapi import FastAPI

from config.settings import settings

app = FastAPI(title="Agent Factory API", version="0.1.0")


@app.get("/healthz")
async def healthz():
    return {
        "status": "ok",
        "environment": settings.environment,
        "version": "0.1.0",
    }
