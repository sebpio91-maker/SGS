from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class TestOrder(Base):
    """Prüfauftrag als Ausgangsdokument für einen Prüfplan.

    Bei Lidl wird dies aus einem hochgeladenen Prüfauftrags-Dokument
    importiert (`source="upload_lidl"`, `raw_data` enthält die geparsten
    Rohdaten); bei anderen Kunden kann ein Prüfauftrag auch manuell
    angelegt werden (`source="manual"`), bevor die Prüfungen im Menü
    ausgewählt werden.
    """

    __tablename__ = "test_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, index=True
    )
    product_id: Mapped[int | None] = mapped_column(
        ForeignKey("products.id", ondelete="SET NULL"), nullable=True, index=True
    )
    order_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source: Mapped[str] = mapped_column(String(50), default="manual", nullable=False)
    original_filename: Mapped[str | None] = mapped_column(String(500), nullable=True)
    raw_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="neu", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    customer: Mapped["Customer"] = relationship()
    product: Mapped["Product | None"] = relationship()
