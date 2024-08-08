from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import HOST, PORT
from database import Base, engine

from hatm.models import Hatm
from auth.models import User

from hatm.routers import router as hatm_router
from auth.routers import router as auth_router

app = FastAPI(
    title='Hatm API',
    description='Hatm API',
    version='2.0.0',
    docs_url='/docs',
    redoc_url='/redoc',
    openapi_url='/openapi.json'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ToDo: allow only quran.kz
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hatm_router, prefix='/hatm', tags=['hatm'])
app.include_router(auth_router, prefix='/auth', tags=['auth'])

models = [Hatm, User]

Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'main:app',
        host=HOST,
        port=int(PORT)
    )
