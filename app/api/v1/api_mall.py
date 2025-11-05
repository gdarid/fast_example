from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.schema import get_session
from app.models.account import MallCreate, MallRead, MallUpdate
from app.services.mall_service import MallService

router = APIRouter()

def get_mall_service(session: Session = Depends(get_session)) -> MallService:
    return MallService(session=session)


@router.get("/malls", response_model=list[MallRead])
def get_malls(service: MallService = Depends(get_mall_service)):
    return service.list_malls()


@router.post("/malls", response_model=MallRead)
def create_mall(mall: MallCreate, service: MallService = Depends(get_mall_service)):
    item_exists = service.check_name(mall.name)
    if item_exists:
        raise HTTPException(status_code=409, detail="Mall already exists with this name")
    mall = service.create_mall(mall.name, mall.owner_id)
    if not mall:
        raise HTTPException(status_code=409, detail="Mall can't be created")
    return mall


@router.get("/malls/{mall_id}", response_model=MallRead)
def get_mall(mall_id: int, service: MallService = Depends(get_mall_service)):
    mall = service.get_mall(mall_id)
    if not mall:
        raise HTTPException(status_code=404, detail="Mall not found")
    return mall


@router.put("/malls/{mall_id}", response_model=MallRead)
def update_mall(mall_id: int, mall: MallUpdate, service: MallService = Depends(get_mall_service)):
    updated = service.update_mall(mall_id, mall.name, mall.owner_id)
    if updated is None:
        raise HTTPException(status_code=404, detail="Mall not found")
    return updated


@router.delete("/malls/{mall_id}")
def delete_mall(mall_id: int, service: MallService = Depends(get_mall_service)):
    success = service.delete_mall(mall_id)
    if not success:
        raise HTTPException(status_code=404, detail="Mall not found")
    return {"success": True}
