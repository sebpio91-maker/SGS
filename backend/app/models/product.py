from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Product(Base):
    """Zu prüfendes Produkt eines Kunden.

    `specification` hält physikalische Produktspezifikationen als
    flexible Schlüssel-Wert-Struktur (Maße, Material, Farbe, ...), da sich
    die relevanten Merkmale je nach Produktart stark unterscheiden.
    `has_battery` / `has_manual` steuern die Anzeige bedingter Prüfpunkte
    (z. B. Akkusicherheitskurzcheck, Bedienungsanleitungsprüfung).
    """

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, index=True
    )
    article_number: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str | None] = mapped_column(String(255), nullable=True)
    has_battery: Mapped[bool] = mapped_column(Boolean, default=False)
    has_manual: Mapped[bool] = mapped_column(Boolean, default=False)
    specification: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    customer: Mapped["Customer"] = relationship(back_populates="products")
