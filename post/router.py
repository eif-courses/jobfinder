from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from starlette.exceptions import HTTPException

from auth.jwt import get_current_user
from db import get_session
from post.models import Post, Category
from user.models import User

router = APIRouter(tags=["Posts"], prefix="/api/v1/posts")


@router.post("/", response_model=Post)
async def create_post(post: Post, db: AsyncSession = Depends(get_session),
                      current_user: User = Depends(get_current_user)):

    fetch_category_info = await db.execute(select(Category).where(Category.id == post.category_id))
    if not fetch_category_info.scalar():
        raise HTTPException(status_code=400, detail="Category not exists!")

    fetch_user_info = await db.execute(select(User).where(User.email == current_user.email))
    user = fetch_user_info.fetchone()[0]
    if not fetch_user_info:
        raise HTTPException(status_code=400, detail="You not allowed to create post!")

    new_post = Post(title=post.title, content=post.content, user_id=user.id, category_id=post.category_id)

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post
