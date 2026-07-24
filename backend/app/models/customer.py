from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Customer(Base):
    """Kunde, für den Prüfpläne erstellt werden (z. B. Lidl).

    `code` identifiziert Kunden mit Sonderbehandlung (z. B. fester
    Prüfpunkt-Baum und Prüfauftrags-Import bei Lidl) eindeutig im Code.
    """

    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    products: Mapped[list["Product"]] = relationship(back_populates="customer")
