from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends

from database import get_database
from models.user import User
from repository.user import (
    create_user_repo,
    delete_user_repo,
    get_all_users_repo,
    get_user_by_id_repo,
    reset_password_repo,
    update_user_repo,
)
from routes.auth import auth, auth_dep
from schemas.user import UserShow

from . import create_router

user = create_router(tags="User", prefix="user")


@user.post("/create")
async def create_user(user: User, db=Depends(get_database)):
    """Create a new user in the system.

    Args:
        user (User): The data for the new user.
        db: The database connection.

    Returns:
        The newly created user as a dictionary.
    """

    return await create_user_repo(user=user, db=db)


@user.get("/all", response_model=list[UserShow])
async def get_all_users(
    authorize: AuthJWT = Depends(auth_dep), db=Depends(get_database)
):
    """_summary_

    Args:
        db (_type_, optional): _description_. Defaults to Depends(get_database).

    Returns:
        _type_: _description_
    """
    await authorize.jwt_required()
    return await get_all_users_repo(db=db)


@user.get("/get/{id}", response_model=UserShow)
async def get_user_by_id(
    user_id: str,
    authorize: AuthJWT = Depends(auth_dep),
    db=Depends(get_database),
):
    """_summary_

    Args:
        db (_type_, optional): _description_. Defaults to Depends(get_database()).
    """
    await authorize.jwt_required()
    return await get_user_by_id_repo(id=user_id, db=db)


@user.delete("/delete/{id}")
async def delete_user(
    id: str,
    authorize: AuthJWT = Depends(auth_dep),
    db=Depends(get_database),
):
    """_summary_

    Args:
        id (str): _description_
        db (_type_, optional): _description_. Defaults to Depends(get_database).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    await authorize.jwt_required()
    return await delete_user_repo(id=id, db=db)


@user.patch("/update/{id}", response_model=dict)
async def update_user(
    id: str,
    user: User,
    authorize: AuthJWT = Depends(auth_dep),
    db=Depends(get_database),
):
    """Update a user with partial data

    Only updates fields that are provided in the request body.
    Fields that are None/null will retain their existing values.

    Args:
        id (str): ID of the user to be updated
        user (User): Request schema containing fields to update
        db: Database connection

    Raises:
        HTTPException: If the user is not found

    Returns:
        dict: Success message
    """
    await authorize.jwt_required()
    return await update_user_repo(id=id, user=user, db=db)


@user.patch("/reset-password/{id}", response_model=dict)
async def method_name(
    id: str,
    password: str,
    authorize: AuthJWT = Depends(auth_dep),
    db=Depends(get_database),
):
    await authorize.jwt_required()
    return await reset_password_repo(id=id, password=password, db=db)
