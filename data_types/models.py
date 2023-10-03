from datetime import datetime

from typing import Optional, List
from pydantic import EmailStr
from sqlalchemy import Column, text, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlmodel import Field, SQLModel, Relationship


class UserSkillLink(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    skill_id: Optional[int] = Field(default=None, foreign_key="skill.id", primary_key=True)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: EmailStr = Field(unique=True)
    password: str
    permissions: Optional[List[str]] = Field(default=['read:items', 'write:items'],
                                             sa_column=Column(postgresql.ARRAY(String())))
    created_at: Optional[datetime] = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ))
    updated_at: Optional[datetime] = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    ))
    posts: List["Post"] = Relationship(back_populates="user")
    skills: List["Skill"] = Relationship(back_populates="users", link_model=UserSkillLink)

    class Config:
        schema_extra = {
            "examples": [
                {
                    "user": {
                        "username": "string",
                        "email": "user@example.com",
                        "password": "string",
                        "permissions": [
                            "read:items",
                            "write:items"
                        ],
                        "created_at": "2023-10-03T07:30:38.594Z",
                        "updated_at": "2023-10-03T07:30:38.594Z"
                    },
                    "skills": [
                        {
                            "id": 0,
                            "name": "string"
                        }
                    ]
                }
            ]
        }


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    posts: List["Post"] = Relationship(back_populates="category")

    class Config:
        schema_extra = {
            "examples": [
                {
                    "name": "Foo",
                }
            ]
        }

class Skill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    users: List["User"] = Relationship(back_populates="skills", link_model=UserSkillLink)


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: Optional[datetime] = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ))
    updated_at: Optional[datetime] = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    ))
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="posts")
    category: Optional[Category] = Relationship(back_populates="posts")
