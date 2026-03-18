from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Future Engine Final", version="final")
app.include_router(router)
