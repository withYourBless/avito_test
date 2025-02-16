from fastapi import FastAPI

from .apis.default_api import router

app = FastAPI()

app.include_router(router)
