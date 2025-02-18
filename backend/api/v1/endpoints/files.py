from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
import json
from datetime import datetime

from backend.db.session import get_db
from backend.core.config import settings
from backend.services import file_service
from backend.models.schemas import file as file_schema

router = APIRouter()

@router.post("/upload", response_model=file_schema.FileResponse)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    上传PDF或JSON文件
    """
    # 验证文件类型
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"文件类型不支持。支持的类型: {settings.ALLOWED_EXTENSIONS}"
        )
    
    return await file_service.save_file(db, file)

@router.get("/", response_model=List[file_schema.FileResponse])
def get_files(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    获取所有文件列表
    """
    return file_service.get_files(db, skip=skip, limit=limit)

@router.get("/{file_id}", response_model=file_schema.FileDetail)
def get_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    """
    获取单个文件的详细信息
    """
    file = file_service.get_file(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="文件未找到")
    return file

@router.delete("/{file_id}")
def delete_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    """
    删除文件
    """
    file = file_service.get_file(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="文件未找到")
    
    file_service.delete_file(db, file_id)
    return {"message": "文件已删除"}

@router.put("/{file_id}/content")
async def update_file_content(
    file_id: int,
    file_content: file_schema.FileContent,
    db: Session = Depends(get_db)
):
    """
    更新文件内容
    """
    file = file_service.get_file(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    if file.file_type != 'json':
        raise HTTPException(status_code=400, detail="只能更新JSON文件内容")
    
    try:
        # 保存新的文件内容
        with open(file.file_path, 'w', encoding='utf-8') as f:
            json.dump(file_content.content, f, indent=2, ensure_ascii=False)
        
        # 更新文件上传时间
        file.upload_time = datetime.utcnow()
        db.commit()
        
        return {"message": "文件内容已更新"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新文件内容时出错: {str(e)}") 