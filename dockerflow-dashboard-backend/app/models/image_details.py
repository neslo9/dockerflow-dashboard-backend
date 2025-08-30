from sqlalchemy import Column, Integer, String, ForeignKey, JSON, TIMESTAMP
from sqlalchemy.orm import relationship
from ..database import Base

class ImageDetails(Base):
    __tablename__ = 'image_details'

    id = Column(Integer, primary_key=True, index=True)
    repo_name = Column(String, nullable=False)
    image_deploy_id = Column(Integer, ForeignKey('image_deploy.id'), nullable=False)
    build_status = Column(String, nullable=False)
    deploy_status = Column(String, nullable=False)
    security_checks = Column(JSON)
    vulnerabilities = Column(JSON)
    project = Column(String)
    image_name = Column(String, nullable=False)
    image_tag = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

    project_rel = relationship('Project', back_populates='images')
