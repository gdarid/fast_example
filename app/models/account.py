from pydantic import BaseModel, ConfigDict


class MallInit(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class MallCreate(MallInit):
    owner_id: int

class MallUpdate(MallInit):
    owner_id: int | None = None

class MallRead(MallInit):
    id: int
    owner_id: int

class AccountCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str

class AccountRead(AccountCreate):
    id: int

class AccountReadDetail(AccountRead):
    malls_ids: list[int]
