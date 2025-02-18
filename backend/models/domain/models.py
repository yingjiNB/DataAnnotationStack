from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class File(Base):
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    file_type = Column(String)  # "pdf" or "json"
    upload_time = Column(DateTime, default=datetime.utcnow)
    file_path = Column(String)
    
    # 关联
    annotations = relationship("Annotation", back_populates="file")
    versions = relationship("FileVersion", back_populates="file")

class FileVersion(Base):
    __tablename__ = "file_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"))
    version_number = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    file_path = Column(String)
    
    # 关联
    file = relationship("File", back_populates="versions")

class Annotation(Base):
    __tablename__ = "annotations"
    
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"))
    json_path = Column(String)  # JSON路径，例如 "personal_info.name"
    original_value = Column(String)
    corrected_value = Column(String, nullable=True)
    is_correct = Column(Boolean, default=True)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    file = relationship("File", back_populates="annotations") 