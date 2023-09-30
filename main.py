from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from user import router as user_router
from post import router as post_router
app = FastAPI(docs_url="/", title="Find Your Dream Job", version="0.0.1")

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers,
    max_age=3600,
)

app.include_router(router=user_router.router)
app.include_router(router=post_router.router)