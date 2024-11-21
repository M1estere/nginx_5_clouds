from pydantic import BaseModel
from typing import List


class UsersResponse(BaseModel):
    """Scheme for get user route"""
    id: int
    username: str
    email: str
