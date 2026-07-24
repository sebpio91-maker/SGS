from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class TestPlan(Base):
    """Der generierte Prüfplan für ein Produkt.

    Fasst die einzelnen Prüfpositionen (`items`) zusammen, die sich aus
    Normen/Gesetzesvorgaben, Produktspezifikation, Kundenvorgaben und
    (bei Lidl) dem Prüfauftrag ergeben. `program_id` verweist optional auf
    das Prüfprogramm, das als Vorlage für die Erstellung diente.
    """

    __tablename__ = "test_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, index=True
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True
    )
    test_order_id: Mapped[int | None] = mapped_column(
        ForeignKey("test_orders.id", ondelete="SET NULL"), nullable=True
    )
    program_id: Mapped[int | None] = mapped_column(
        ForeignKey("test_programs.id", ondelete="SET NULL"), nullable=True
    )
    created_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[str] = mapped_column(String(50), default="entwurf", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    customer: Mapped["Customer"] = relationship()
    product: Mapped["Product"] = relationship()
    test_order: Mapped["TestOrder | None"] = relationship()
    program: Mapped["TestProgram | None"] = relationship()
    items: Mapped[list["TestPlanItem"]] = relationship(
        back_populates="test_plan", cascade="all, delete-orphan", order_by="TestPlanItem.sort_order"
    )


class TestPlanItem(Base):
    """Einzelne Prüfposition innerhalb eines Prüfplans.

    Name, Kategorie und Normbezug werden beim Erstellen aus dem
    Prüfkatalog übernommen (Snapshot), damit der Prüfplan auch dann
    unverändert bleibt, wenn sich der Katalog später weiterentwickelt.
    """

    __tablename__ = "test_plan_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    test_plan_id: Mapped[int] = mapped_column(
        ForeignKey("test_plans.id", ondelete="CASCADE"), nullable=False, index=True
    )
    catalog_item_id: Mapped[int | None] = mapped_column(
        ForeignKey("test_catalog_items.id", ondelete="SET NULL"), nullable=True
    )
    category_name: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    norm_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    result: Mapped[str | None] = mapped_column(String(50), nullable=True)
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(default=0)

    test_plan: Mapped["TestPlan"] = relationship(back_populates="items")
    catalog_item: Mapped["TestCatalogItem | None"] = relationship()
