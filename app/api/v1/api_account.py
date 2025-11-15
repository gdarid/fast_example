from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.schema import get_session
from app.models.account import AccountCreate, AccountRead, AccountReadDetail
from app.services.account_service import AccountService

router = APIRouter()

def get_account_service(session: Session = Depends(get_session)) -> AccountService:
    return AccountService(session=session)


@router.get("/accounts", response_model=list[AccountRead])
def get_accounts(service: AccountService = Depends(get_account_service)):
    return service.list_accounts()


@router.post("/accounts", response_model=AccountRead)
def create_account(account: AccountCreate, service: AccountService = Depends(get_account_service)):
    item_exists = service.check_name(account.name)
    if item_exists:
        raise HTTPException(status_code=409, detail="Account already exists with this name")
    account_new = service.create_account(account.name)
    if not account_new:
        raise HTTPException(status_code=409, detail="Account can't be created")
    return account_new


@router.get("/accounts/{account_id}", response_model=AccountReadDetail)
def get_account(account_id: int, service: AccountService = Depends(get_account_service)):
    account = service.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    detail_account = AccountReadDetail(id=account.id, name=account.name, malls_ids=[mall.id for mall in account.malls])
    return detail_account


@router.put("/accounts/{account_id}", response_model=AccountRead)
def update_account(account_id: int, account: AccountCreate, service: AccountService = Depends(get_account_service)):
    updated = service.update_account(account_id, account.name)
    if updated is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return updated


@router.delete("/accounts/{account_id}")
def delete_account(account_id: int, service: AccountService = Depends(get_account_service)):
    success = service.delete_account(account_id)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"success": True}
