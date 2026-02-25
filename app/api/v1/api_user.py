from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.schema import get_session
from app.models.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter()

def get_user_service(session: Annotated[AsyncSession, Depends(get_session)]) -> UserService:
    return UserService(session=session)


@router.get("/users", response_model=list[UserRead])
async def get_users(service: Annotated[UserService, Depends(get_user_service)]):
    return await service.list_users()


@router.post("/users", response_model=UserRead)
async def create_user(user: UserCreate, service: Annotated[UserService, Depends(get_user_service)]):
    item_exists = await service.check_name(user.name)
    if item_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists with this name")
    user_new = await service.create_user(user.name)

    return user_new


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int, service: Annotated[UserService, Depends(get_user_service)]):
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user: UserCreate, service: Annotated[UserService, Depends(get_user_service)]):
    updated = await service.update_user(user_id, user.name)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, service: Annotated[UserService, Depends(get_user_service)]):
    success = await service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"success": True}
