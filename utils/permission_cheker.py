from typing import List

from fastapi import Depends, HTTPException
from starlette import status

from data_types.models import User
from utils.jwt import get_current_user


class PermissionChecker:
    def __init__(self, required_permissions: List[str]) -> None:
        self.required_permissions = required_permissions

    def __call__(self, user: User = Depends(get_current_user)) -> bool:
        for r_perm in self.required_permissions:
            if r_perm not in user.permissions:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Not enough permissions!'
                )
        return True
