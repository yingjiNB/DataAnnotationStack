from pydantic import BaseModel, validator
from datetime import datetime
from typing import List, Optional, Dict, Any
from backend.core.config import settings

class FileBase(BaseModel):
    filename: str
    file_type: str
    
    @validator('file_type')
    def validate_file_type(cls, v):
        if v not in settings.ALLOWED_EXTENSIONS:
            raise ValueError(f"不支持的文件类型。支持的类型: {settings.ALLOWED_EXTENSIONS}")
        return v

class FileCreate(FileBase):
    pass

class FileResponse(FileBase):
    id: int
    upload_time: datetime
    file_path: str

    class Config:
        from_attributes = True

class FileDetail(FileResponse):
    annotation_count: int
    version_count: int

    class Config:
        from_attributes = True

class FileContent(BaseModel):
    content: Dict[str, Any]
    
    @validator('content')
    def validate_json_content(cls, v):
        # 这里可以添加更多的JSON格式验证规则
        required_fields = {'name', 'email', 'education', 'experience'}
        missing_fields = required_fields - set(v.keys())
        if missing_fields:
            raise ValueError(f"缺少必要字段: {missing_fields}")
        return v 