from sqlalchemy import create_engine
from backend.models.domain.models import Base
from backend.core.config import settings

def init_db():
    """
    初始化数据库，创建所有表
    """
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(bind=engine) 