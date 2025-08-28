from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Text,
    ForeignKey,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship
from .db import Base

class Target(Base):
    __tablename__ = "targets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)  # usado na API Blizzard
    region = Column(String, nullable=False)  # ex: us/eu/br
    enabled = Column(Boolean, default=True, nullable=False)
    population = Column(Integer, nullable=True)  # Tamanho da população do servidor
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    checks = relationship("Check", back_populates="target", cascade="all, delete-orphan")

class Check(Base):
    __tablename__ = "checks"

    id = Column(Integer, primary_key=True, index=True)
    target_id = Column(Integer, ForeignKey("targets.id", ondelete="CASCADE"), index=True, nullable=False)
    ts = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status = Column(String, nullable=False)  # “online”/“offline” ou código interpretado
    latency_ms = Column(Integer)
    error = Column(Text)

    target = relationship("Target", back_populates="checks")

class ApiError(Base):
    __tablename__ = "api_errors"

    id = Column(Integer, primary_key=True, index=True)
    ts = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    endpoint = Column(String, nullable=False)  # endpoint chamado
    message = Column(Text, nullable=False)     # mensagem de erro
    details = Column(Text)                     # detalhes adicionais (opcional)

