from fastapi import UploadFile
from sqlalchemy.orm import Session
import os
import shutil
from datetime import datetime

from backend.models.domain.models import File
from backend.core.config import settings

async def save_file(db: Session, file: UploadFile) -> File:
    """
    保存上传的文件并创建数据库记录
    """
    # 确保上传目录存在
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # 检查是否存在同名文件
    existing_file = db.query(File).filter(File.filename == file.filename).first()
    
    # 生成文件路径
    file_extension = file.filename.split(".")[-1].lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, safe_filename)
    
    # 保存文件
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    if existing_file:
        # 如果文件已存在，更新文件路径和上传时间
        if os.path.exists(existing_file.file_path):
            try:
                os.remove(existing_file.file_path)
            except OSError:
                pass
        existing_file.file_path = file_path
        existing_file.upload_time = datetime.utcnow()
        db_file = existing_file
    else:
        # 创建新的数据库记录
        db_file = File(
            filename=file.filename,
            file_type=file_extension,
            file_path=file_path
        )
        db.add(db_file)
    
    db.commit()
    db.refresh(db_file)
    return db_file

def get_files(db: Session, skip: int = 0, limit: int = 100):
    """
    获取文件列表
    """
    return db.query(File).offset(skip).limit(limit).all()

def get_file(db: Session, file_id: int):
    """
    获取单个文件
    """
    return db.query(File).filter(File.id == file_id).first()

def delete_file(db: Session, file_id: int):
    """
    删除文件及其数据库记录
    """
    file = get_file(db, file_id)
    if file:
        # 删除物理文件
        if os.path.exists(file.file_path):
            try:
                os.remove(file.file_path)
            except OSError:
                pass
        
        # 删除数据库记录
        db.delete(file)
        db.commit()
        
    return file 