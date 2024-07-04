from fastapi import FastAPI
from nutrilog.api.routes import router
from nutrilog.config import settings

app = FastAPI(
    title=settings.app_name, docs_url="/api/docs", openapi_url="/api/openapi.json"
)

app.include_router(router, prefix="/api")
