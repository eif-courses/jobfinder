from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select
from starlette.exceptions import HTTPException

from data_types.schema import DisplayPost, TokenData
from utils.jwt import get_current_user
from utils.db import get_session
from data_types.models import Post, Category, Skill, User
import logging

from utils.permission_cheker import PermissionChecker

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Posts"], prefix="/api/v1/posts")


@router.post("/", response_model=Post)
async def create_new_post(post: Post,
                          db: AsyncSession = Depends(get_session),
                          current_user: TokenData = Depends(
                              PermissionChecker(required_permissions=["read:items", "create:posts"]))):
    # fetch_category_info = await db.execute(select(Category).where(Category.id == post.category_id))
    # if not fetch_category_info.scalar().first():
    #     raise HTTPException(status_code=400, detail="Category not exists!")

    fetch_user_info = await db.execute(select(User).where(User.email == current_user.email))
    user = fetch_user_info.first()[0] # skaitom pirmą elementą iš eilutės
    if not fetch_user_info:
        raise HTTPException(status_code=400, detail="You not allowed to create post!")

    new_post = Post(title=post.title, content=post.content, user_id=user.id, created_at=post.created_at, updated_at=post.updated_at)

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post


@router.post("/categories", response_model=Category)
async def create_new_category(category: Category,
                              db: AsyncSession = Depends(get_session),
                              current_user: TokenData = Depends(
                                  PermissionChecker(required_permissions=["super:admin"]))):
    fetch_category_info = await db.execute(select(Category).where(Category.id == category.id))
    if fetch_category_info.first():
        raise HTTPException(status_code=400, detail="Category already exists!")
    new_category = Category(name=category.name)
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category


@router.get("/categories", response_model=List[Category])
async def display_categories(skip: int = 0, limit: int = 10,
                             db: AsyncSession = Depends(get_session),
                             current_user: TokenData = Depends(get_current_user)):
    categories_result = await db.execute(select(Category).offset(skip).limit(limit))
    categories = categories_result.scalars().all()
    return categories


@router.get("/", response_model=List[DisplayPost])
async def display_posts(skip: int = 0, limit: int = 10,
                        db: AsyncSession = Depends(get_session),
                        current_user: TokenData = Depends(get_current_user)):
    query = select(Post).options(selectinload(Post.user)).offset(skip).limit(limit)
    result = await db.execute(query)
    posts = result.scalars().all()
    logger.info(posts)
    return posts


@router.post("/skills", response_model=Skill)
async def create_new_skill(skill: Skill,
                           db: AsyncSession = Depends(get_session),
                           current_user: TokenData = Depends(
                               PermissionChecker(required_permissions=["super:admin"]))):
    fetch_skill_info = await db.execute(select(Skill).where(Skill.id == skill.id))
    if fetch_skill_info.first():
        raise HTTPException(status_code=400, detail="Skill already exists!")

    new_skill = Skill(name=skill.name)

    db.add(new_skill)
    await db.commit()
    await db.refresh(new_skill)
    return new_skill


@router.head("/skills", response_model=List[Skill])
@router.get("/skills", response_model=List[Skill])
async def display_skills(skip: int = 0, limit: int = 10,
                         db: AsyncSession = Depends(get_session),
                         current_user: TokenData = Depends(get_current_user)):
    skills_result = await db.execute(select(Skill).offset(skip).limit(limit))
    skills = skills_result.scalars().all()
    return skills
