from sqlalchemy.orm import Session
from typing import List, Optional

from backend.models.domain.models import Annotation
from backend.models.schemas.annotation import AnnotationCreate, AnnotationUpdate

def create_annotation(db: Session, annotation: AnnotationCreate) -> Annotation:
    """
    创建新的标注
    """
    db_annotation = Annotation(
        file_id=annotation.file_id,
        json_path=annotation.json_path,
        original_value=annotation.original_value,
        is_correct=annotation.is_correct,
        comment=annotation.comment
    )
    db.add(db_annotation)
    db.commit()
    db.refresh(db_annotation)
    return db_annotation

def get_annotation(db: Session, annotation_id: int) -> Optional[Annotation]:
    """
    获取单个标注
    """
    return db.query(Annotation).filter(Annotation.id == annotation_id).first()

def get_file_annotations(db: Session, file_id: int) -> List[Annotation]:
    """
    获取指定文件的所有标注
    """
    return db.query(Annotation).filter(Annotation.file_id == file_id).all()

def update_annotation(
    db: Session,
    db_annotation: Annotation,
    annotation: AnnotationUpdate
) -> Annotation:
    """
    更新标注
    """
    update_data = annotation.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_annotation, field, value)
    
    db.commit()
    db.refresh(db_annotation)
    return db_annotation

def delete_annotation(db: Session, annotation_id: int):
    """
    删除标注
    """
    annotation = get_annotation(db, annotation_id)
    if annotation:
        db.delete(annotation)
        db.commit()
    return annotation 