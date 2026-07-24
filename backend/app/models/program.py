from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class TestProgram(Base):
    """Wiederverwendbare Vorlage aus mehreren Prüfpunkten für sich
    wiederholende Produkte mit ähnlichen Prüfanforderungen.

    Ist `customer_id` gesetzt, ist das Programm nur für diesen Kunden
    gedacht; ist es NULL, kann es kundenübergreifend verwendet werden.
    """

    __tablename__ = "test_programs"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int | None] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE"), nullable=True, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    items: Mapped[list["TestProgramItem"]] = relationship(
        back_populates="program", cascade="all, delete-orphan"
    )


class TestProgramItem(Base):
    """Zuordnung eines Prüfkatalog-Punkts zu einem Prüfprogramm."""

    __tablename__ = "test_program_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("test_programs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    catalog_item_id: Mapped[int] = mapped_column(
        ForeignKey("test_catalog_items.id", ondelete="CASCADE"), nullable=False, index=True
    )

    program: Mapped["TestProgram"] = relationship(back_populates="items")
    catalog_item: Mapped["TestCatalogItem"] = relationship()
