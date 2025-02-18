from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.db.session import get_db
from backend.services import annotation_service
from backend.models.schemas import annotation as annotation_schema

router = APIRouter()

@router.post("/", response_model=annotation_schema.AnnotationResponse)
def create_annotation(
    annotation: annotation_schema.AnnotationCreate,
    db: Session = Depends(get_db)
):
    """
    创建新的标注
    """
    return annotation_service.create_annotation(db, annotation)

@router.get("/file/{file_id}", response_model=List[annotation_schema.AnnotationResponse])
def get_file_annotations(
    file_id: int,
    db: Session = Depends(get_db)
):
    """
    获取指定文件的所有标注
    """
    annotations = annotation_service.get_file_annotations(db, file_id)
    if not annotations:
        raise HTTPException(status_code=404, detail="未找到标注")
    return annotations

@router.put("/{annotation_id}", response_model=annotation_schema.AnnotationResponse)
def update_annotation(
    annotation_id: int,
    annotation: annotation_schema.AnnotationUpdate,
    db: Session = Depends(get_db)
):
    """
    更新标注
    """
    db_annotation = annotation_service.get_annotation(db, annotation_id)
    if not db_annotation:
        raise HTTPException(status_code=404, detail="标注未找到")
    return annotation_service.update_annotation(db, db_annotation, annotation)

@router.delete("/{annotation_id}")
def delete_annotation(
    annotation_id: int,
    db: Session = Depends(get_db)
):
    """
    删除标注
    """
    db_annotation = annotation_service.get_annotation(db, annotation_id)
    if not db_annotation:
        raise HTTPException(status_code=404, detail="标注未找到")
    annotation_service.delete_annotation(db, annotation_id)
    return {"message": "标注已删除"} 