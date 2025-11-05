from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class UserRead(UserCreate):
    id: int
