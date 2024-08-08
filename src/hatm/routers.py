import hashlib
import os
import subprocess
import uuid
from datetime import datetime

from click import File
from fastapi import (APIRouter, Depends, Form, HTTPException, Request,
                     Response, UploadFile)
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import UUID4
from sqlalchemy.orm import Session, joinedload

from auth.models import User
from auth.routers import get_current_user
from database import get_db
from logger import logger

router = APIRouter()


@router.post("/create_hatm")
async def create_hatm(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pass