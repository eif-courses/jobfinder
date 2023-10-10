from bcrypt import checkpw
from fastapi import APIRouter, Request, Depends, HTTPException, Form, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from starlette.responses import HTMLResponse, RedirectResponse, Response
from starlette.templating import Jinja2Templates

import utils
from data_types.models import User
from utils.db import get_session
from utils.jwt import create_access_token

templates = Jinja2Templates(directory="templates")

router = APIRouter(tags=["Website"], prefix="/api/v1/website")


@router.get("/", response_class=HTMLResponse)
@router.post("/", response_class=HTMLResponse)
async def home(request: Request):
    cookie = request.cookies.get("access_token")
    if not cookie:
        redirect_url = "/api/v1/website/login"
        return RedirectResponse(url=redirect_url)

    current_user = utils.jwt.verify_token(cookie,
                                          HTTPException(status_code=401, detail="Wrong Credentials!"))

    if not current_user:
        redirect_url = "/api/v1/website/login"  # Change this to the login page or any other desired page
        return RedirectResponse(url=redirect_url)
    return templates.TemplateResponse("index.html", {"request": request, "user": current_user})


@router.get("/login", response_class=HTMLResponse)
async def show_login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login(username: str = Form(...), password: str = Form(...),
                db: AsyncSession = Depends(get_session)):
    # Formos objekto duomenys
    # print(username, password)

    result = await db.execute(select(User).where(User.email == username))
    user = result.first()[0]
    if user is None:
        raise HTTPException(status_code=401, detail="Wrong Credentials!")
    # Check if the entered password matches the stored hashed password
    if not checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Wrong Credentials!")

    # Create access token
    access_token = create_access_token(data={"sub": user.email})

    # Redirect to the home page or any other desired page
    redirect_url = "/api/v1/website"  # Change this to your desired page
    response = RedirectResponse(url=redirect_url, status_code=303)

    # Set the access token as a cookie (optional, depending on your authentication mechanism)
    response.set_cookie(key="access_token", value=access_token, httponly=True)

    return response
