from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


from routers import posts_router, users_router

app = FastAPI(docs_url="/", title="Find Your Dream Job", version="0.0.2")

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

app.include_router(router=posts_router.router)
app.include_router(router=users_router.router)