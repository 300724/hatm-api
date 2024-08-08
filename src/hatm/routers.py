from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from auth.models import User
from auth.routers import get_current_user
from database import get_db

router = APIRouter()


@router.post("/create_hatm")
async def create_hatm(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print(request, db, current_user)
