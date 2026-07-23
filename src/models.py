from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class AssetStatus(str, Enum):
    pending = "pending"
    downloaded = "downloaded"
    processed = "processed"
    failed = "failed"


class PublishStatus(str, Enum):
    draft = "draft"
    ready = "ready"
    submitted = "submitted"
    failed = "failed"


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    source_platform: Mapped[str] = mapped_column(String(40), nullable=False)
    license_note: Mapped[str] = mapped_column(String(255), nullable=False)
    owner_name: Mapped[str] = mapped_column(String(255), nullable=False)

    raw_path: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    processed_path: Mapped[str | None] = mapped_column(String(1024), nullable=True)

    sha256: Mapped[str | None] = mapped_column(String(64), nullable=True)
    phash: Mapped[str | None] = mapped_column(String(32), nullable=True)

    status: Mapped[AssetStatus] = mapped_column(SqlEnum(AssetStatus), default=AssetStatus.pending)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PublishJob(Base):
    __tablename__ = "publish_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    asset_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    hashtags: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[PublishStatus] = mapped_column(SqlEnum(PublishStatus), default=PublishStatus.draft)
    package_path: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
