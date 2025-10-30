from sqlalchemy import DateTime, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from ..base import BaseModel

class SessionGov(BaseModel):
    __tablename__ = "session_gov"
    schema = "public"

    # id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    site: Mapped[str] = mapped_column(String(50), nullable=False)  # 'esocial' ou 'ecac'
    cookies_data: Mapped[dict] = mapped_column(JSON, nullable=False)  # JSON das cookies
    org_id: Mapped[int | None] = mapped_column(Integer, nullable=True)  # ID da organização
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)