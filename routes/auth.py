from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer
from fastapi import Depends, HTTPException, status

from database import get_database
from models.auth import UserLogin
from models.user import User
from security.hash import Hash

from . import create_router

auth = create_router(tags="Auth", prefix="auth")

auth_dep = AuthJWTBearer()

@auth.post("/login")
async def method_name():
    pass


@auth.post("/refresh-token")
async def refresh_token():
    pass
