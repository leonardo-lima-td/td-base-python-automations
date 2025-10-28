"""
Models do banco Automations

Adicione seus models de automações aqui.

Exemplo:
    from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey
    from sqlalchemy.orm import relationship
    from ...base import BaseModel
    
    class AutomationJob(BaseModel):
        __tablename__ = "automation_jobs"
        
        name = Column(String(100), nullable=False)
        description = Column(Text)
        status = Column(String(20), default="pending")
        cron_expression = Column(String(50))
        last_run = Column(DateTime)
        next_run = Column(DateTime)
        active = Column(Boolean, default=True)
    
    class AutomationLog(BaseModel):
        __tablename__ = "automation_logs"
        
        job_id = Column(Integer, ForeignKey("automation_jobs.id"))
        level = Column(String(20), nullable=False)  # INFO, WARNING, ERROR
        message = Column(Text, nullable=False)
        execution_time = Column(Integer)  # em segundos
        
        # Relationship
        job = relationship("AutomationJob", backref="logs")
    
    class AutomationConfig(BaseModel):
        __tablename__ = "automation_configs"
        
        key = Column(String(100), unique=True, nullable=False)
        value = Column(Text)
        description = Column(String(200))
        is_encrypted = Column(Boolean, default=False)
"""

# Importe seus models de Automations aqui
# from .automation_job import AutomationJob
# from .automation_log import AutomationLog
# from .automation_config import AutomationConfig

__all__ = []

