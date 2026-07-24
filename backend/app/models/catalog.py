from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class TestCategory(Base):
    """Prüfkategorie im Prüfkatalog (z. B. "Sicherheit & Norm / Sonder- &
    Funktionsparameter", "FFU/Fitting").

    Über `parent_id` können Unterkategorien gebildet werden. Ist
    `customer_id` gesetzt, gehört die Kategorie zum festen Baum eines
    bestimmten Kunden (z. B. Lidl); ist es NULL, steht sie im generischen
    Menü-Katalog für alle anderen Kunden zur Auswahl.
    """

    __tablename__ = "test_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int | None] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE"), nullable=True, index=True
    )
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("test_categories.id", ondelete="CASCADE"), nullable=True, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sort_order: Mapped[int] = mapped_column(default=0)

    parent: Mapped["TestCategory | None"] = relationship(
        remote_side="TestCategory.id", back_populates="children"
    )
    children: Mapped[list["TestCategory"]] = relationship(back_populates="parent")
    items: Mapped[list["TestCatalogItem"]] = relationship(back_populates="category")


class TestCatalogItem(Base):
    """Einzelner Prüfpunkt innerhalb einer Prüfkategorie (z. B.
    "Akkusicherheitskurzcheck", "Kennzeichnungsprüfung").

    `applicability_condition` markiert Prüfpunkte, die nur unter einer
    Bedingung relevant sind (z. B. "has_battery" für den
    Akkusicherheitskurzcheck bei elektrischen Produkten mit Batterie-/
    Akkukomponente, "has_manual" für die Bedienungsanleitungsprüfung).
    NULL bedeutet: immer zur Auswahl verfügbar.
    """

    __tablename__ = "test_catalog_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("test_categories.id", ondelete="CASCADE"), nullable=False, index=True
    )
    norm_id: Mapped[int | None] = mapped_column(
        ForeignKey("norms.id", ondelete="SET NULL"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    applicability_condition: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_default_selected: Mapped[bool] = mapped_column(default=False)
    sort_order: Mapped[int] = mapped_column(default=0)

    category: Mapped["TestCategory"] = relationship(back_populates="items")
    norm: Mapped["Norm | None"] = relationship()
