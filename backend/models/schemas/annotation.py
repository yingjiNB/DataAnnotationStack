from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AnnotationBase(BaseModel):
    file_id: int
    json_path: str
    original_value: str
    is_correct: bool = True
    comment: Optional[str] = None

class AnnotationCreate(AnnotationBase):
    pass

class AnnotationUpdate(BaseModel):
    corrected_value: Optional[str] = None
    is_correct: Optional[bool] = None
    comment: Optional[str] = None

class AnnotationResponse(AnnotationBase):
    id: int
    corrected_value: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 