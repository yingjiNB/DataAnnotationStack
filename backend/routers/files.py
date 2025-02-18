from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os

from backend.models.domain.models import File as FileModel
from backend.services import file_service
from backend.db.session import get_db

router = APIRouter()

@router.get("/{file_id}/content")
async def get_file_content(file_id: int, db: Session = Depends(get_db)):
    """
    获取文件内容
    """
    file = file_service.get_file(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    if not os.path.exists(file.file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return FileResponse(file.file_path) 