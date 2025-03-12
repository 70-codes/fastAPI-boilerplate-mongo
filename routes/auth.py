from datetime import timedelta

from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer
from fastapi import Depends, HTTPException, status

from database import get_database
from models.auth import UserLogin
from repository.user import get_user_by_email
from security.hash import Hash

from . import create_router

auth = create_router(tags="Auth", prefix="auth")

auth_dep = AuthJWTBearer()


@auth.post("/login")
async def login(
    request: UserLogin,
    auth: AuthJWT = Depends(),
    db=Depends(get_database),
):
    """_summary_

    Args:
        request (UserLogin): email and password
        auth (AuthJWT, optional): authorization. Defaults to Depends().
        db (_type_, optional): _description_. Defaults to Depends(get_database).

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """

    user = await get_user_by_email(db=db, email=request.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid username or password",
        )
    if not Hash.verify_password(
        plain_password=request.password,
        hashed_password=user["password"],  # Access using dictionary key
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid username or password",
        )

    expiration_time = 20
    expires = timedelta(minutes=expiration_time)

    access_token = await auth.create_access_token(
        subject=str(user["_id"]), expires_time=expires
    )
    refresh_token = await auth.create_refresh_token(subject=str(user["_id"]))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "access_token_expiration_time": expiration_time,
    }


@auth.post("/refresh")
async def refresh(authorize: AuthJWT = Depends(auth_dep)):
    """_summary_

    Args:
        authorize (AuthJWT, optional): _description_. Defaults to Depends(auth_dep).

    Returns:
        _type_: _description_
    """
    await authorize.jwt_refresh_token_required()

    current_user = await authorize.get_jwt_subject()
    new_access_token = await authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}
