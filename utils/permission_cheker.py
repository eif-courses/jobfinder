from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from data_types.models import User
from data_types.schema import TokenData
from utils.db import get_session
from utils.jwt import get_current_user


class PermissionChecker:
    def __init__(self, required_permissions: List[str]) -> None:
        self.required_permissions = required_permissions

    async def __call__(self, token_data: TokenData = Depends(get_current_user),
                       db: AsyncSession = Depends(get_session)) -> TokenData:
        query_result = await db.execute(select(User).where(User.email == token_data.email))
        current_user = query_result.first()[0]

        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='User not found!'
            )

        missing_permissions = [r_perm for r_perm in self.required_permissions if r_perm not in current_user.permissions]

        if missing_permissions:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'Missing permissions: {", ".join(missing_permissions)}'
            )

        return token_data
