from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship

from .database import Base

STATUS_OPTIONEN = ["aktiv", "in Überarbeitung", "zurückgezogen", "Entwurf"]
RELEVANZ_OPTIONEN = ["Ja", "Nein", "Indirekt"]


class Norm(Base):
    __tablename__ = "normen"

    id = Column(Integer, primary_key=True)
    kurzbezeichnung = Column(String(100), nullable=False)
    vollbezeichnung = Column(String(255))
    titel = Column(Text)
    status = Column(String(50), default="aktiv")
    kategorie = Column(String(150))
    notiz = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    pruefpunkte = relationship(
        "Pruefpunkt",
        back_populates="norm",
        cascade="all, delete-orphan",
        order_by="Pruefpunkt.sortierung",
    )

    @property
    def anzahl_pruefpunkte(self):
        return len(self.pruefpunkte)

    @property
    def anzahl_relevant(self):
        return sum(1 for p in self.pruefpunkte if p.pruefungsrelevant == "Ja")


class Pruefpunkt(Base):
    __tablename__ = "pruefpunkte"

    id = Column(Integer, primary_key=True)
    norm_id = Column(Integer, ForeignKey("normen.id"), nullable=False)
    kapitel = Column(String(50))
    ueberschrift = Column(String(500))
    pruefungsrelevant = Column(String(20), default="Nein")
    inhalt = Column(Text)
    sortierung = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    norm = relationship("Norm", back_populates="pruefpunkte")
