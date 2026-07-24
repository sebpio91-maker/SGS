from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Norm(Base):
    """Norm, Gesetz oder sonstige Vorgabe, auf die sich ein Prüfpunkt bezieht.

    Beispiele: "EN 71-1:2014" (Norm), "ProdSG §3" (Gesetz),
    "Lidl Kennzeichnungsrichtlinie v3" (Kundenvorgabe).
    """

    __tablename__ = "norms"

    id: Mapped[int] = mapped_column(primary_key=True)
    reference: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    type: Mapped[str] = mapped_column(String(50), default="norm", nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
