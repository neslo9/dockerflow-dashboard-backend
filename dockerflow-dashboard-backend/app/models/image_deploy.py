from sqlalchemy import Column, Integer, String, TIMESTAMP
from ..database import Base

class ImageDeploy(Base):
    __tablename__ = 'image_deploy'

    id = Column(Integer, primary_key=True, index=True)
    repo_name = Column(String)
    timestamp = Column(TIMESTAMP, server_default='now()')
    status = Column(String)
    project = Column(String)
