from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.models import User
from auth.routers import router as auth_router
from config import HOST, PORT
from database import Base, engine
from hatm.models import Hatm
from hatm.routers import router as hatm_router
from juz.routers import router as juz_router

app = FastAPI(
    title="Hatm API",
    description="Hatm API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # todo: allow only quran.kz pylint: disable=W0511
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hatm_router, prefix="/hatm", tags=["hatm"])
app.include_router(juz_router, prefix="/juzs", tags=["juz"])
app.include_router(auth_router, prefix="", tags=["auth"])

models = [Hatm, User]

Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=HOST, port=int(PORT))
