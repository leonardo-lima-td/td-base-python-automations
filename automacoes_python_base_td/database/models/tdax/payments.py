from sqlalchemy import DateTime, String, Date
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from ..base import BaseModel

class Payment(BaseModel):
    __tablename__ = "pagamentos"
    __table_args__ = {'schema': 'public'}

    # PRIMARY KEY e UNIQUE
    # numero_doc: Mapped[str] = mapped_column(String(50), primary_key=True, nullable=False)
    
    # Outros campos
    tipo_doc: Mapped[str] = mapped_column(String(65), nullable=False)
    periodo: Mapped[date] = mapped_column(Date, nullable=False)
    data_arrecadacao: Mapped[date] = mapped_column(Date, nullable=False)
    data_vencimento: Mapped[date] = mapped_column(Date, nullable=False)
    codigo_receita: Mapped[str] = mapped_column(String(20), nullable=False)
    numero_referencia: Mapped[str] = mapped_column(String(20), nullable=False)
    valor_total: Mapped[str] = mapped_column(String(20), nullable=False)
    cnpj_id: Mapped[str | None] = mapped_column(String(18), nullable=True)
    juros: Mapped[str] = mapped_column(String(50), nullable=False)
    multa: Mapped[str] = mapped_column(String(50), nullable=False)
    principal: Mapped[str] = mapped_column(String(50), nullable=False)
    saldo_total: Mapped[str] = mapped_column(String(20), nullable=False)
    saldo_juros: Mapped[str] = mapped_column(String(20), nullable=False)
    saldo_multa: Mapped[str] = mapped_column(String(20), nullable=False)
    saldo_principal: Mapped[str] = mapped_column(String(20), nullable=False)
    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

