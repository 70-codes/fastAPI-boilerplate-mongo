from bson import ObjectId
from fastapi import Depends, HTTPException, status

from repository import fix_id, fix_one_item_id
from security.hash import Hash


async def get_user_by_email(email: str, db):
    return await db.user.find_one({"email": email})


async def get_user_by_phone(phone: str, db):
    return await db.user.find_one({"phone": phone})


async def create_user_repo(user, db):
    if await get_user_by_email(user.email, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User email already exists",
        )
    elif await get_user_by_phone(user.phone, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User phone already exists",
        )
    user.password = Hash.get_password_hash(user.password)
    result = await db.user.insert_one(user.model_dump())
    return {"inserted_id": str(result.inserted_id)}


async def get_all_users_repo(db):
    users = await db.user.find().to_list(length=100)
    users = fix_id(users)
    return users


async def get_user_by_id_repo(id: str, db):
    user_data = await db.user.find_one({"_id": ObjectId(id)})
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user_data = fix_one_item_id(user_data)
    return user_data


async def delete_user_repo(id: str, db):
    user = await db.user.find_one_and_delete({"_id": ObjectId(id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return {"message": "user deleted successfully"}


async def update_user_repo(id: str, user, db):
    try:
        # Get the existing user data first
        existing_user = await db.user.find_one({"_id": ObjectId(id)})
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        update_data = {}
        user_dict = user.model_dump(exclude_unset=True)

        for field, value in user_dict.items():
            if value is not None:
                update_data[field] = value

        if update_data:
            result = await db.user.update_one(
                {"_id": ObjectId(id)}, {"$set": update_data}
            )

            if result.modified_count == 0:
                return {"message": "No changes were made"}

        return {"message": "User updated successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}",
        ) from e


async def reset_password_repo(id, password: str, db):
    try:
        existing_user = await db.user.find_one({"_id": ObjectId(id)})
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        existing_user["password"] = Hash.get_password_hash(password)
        result = await db.user.update_one(
            {"_id": ObjectId(id)}, {"$set": existing_user}
        )
        if result.modified_count == 0:
            return {"message": "Password was not updated"}

        return {"message": "Password updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}",
        ) from e
