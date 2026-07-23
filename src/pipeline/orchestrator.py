from sqlalchemy import select

from ..db import SessionLocal
from ..models import Asset, AssetStatus, PublishJob, PublishStatus
from ..services.downloader import DownloadError, download_video
from ..services.fingerprint import compute_phash_from_cover, compute_sha256
from ..services.publisher import create_publish_package
from ..services.video_processor import ProcessError, process_video


def ingest_and_process_asset(asset_id: int) -> tuple[bool, str]:
    with SessionLocal() as db:
        asset = db.get(Asset, asset_id)
        if not asset:
            return False, "asset 不存在"

        try:
            raw_path = download_video(asset.source_url, f"asset_{asset.id}_raw")
            asset.raw_path = raw_path
            asset.status = AssetStatus.downloaded
            db.commit()

            processed_path, cover_path = process_video(raw_path, asset.id)
            asset.processed_path = processed_path
            asset.sha256 = compute_sha256(processed_path)
            asset.phash = compute_phash_from_cover(cover_path)

            existing = db.execute(
                select(Asset).where(
                    Asset.id != asset.id,
                    Asset.sha256 == asset.sha256,
                )
            ).scalars().first()
            if existing:
                asset.status = AssetStatus.failed
                asset.error_message = f"检测到重复素材，重复 asset_id={existing.id}"
                db.commit()
                return False, asset.error_message

            asset.status = AssetStatus.processed
            db.commit()
            return True, "处理成功"

        except (DownloadError, ProcessError, Exception) as exc:
            asset.status = AssetStatus.failed
            asset.error_message = str(exc)
            db.commit()
            return False, str(exc)


def prepare_publish_job(asset_id: int, title: str, hashtags: str) -> tuple[bool, str, int | None]:
    with SessionLocal() as db:
        asset = db.get(Asset, asset_id)
        if not asset:
            return False, "asset 不存在", None
        if asset.status != AssetStatus.processed or not asset.processed_path:
            return False, "asset 未处理完成", None

        package_path = create_publish_package(asset.id, asset.processed_path, title, hashtags)
        job = PublishJob(
            asset_id=asset.id,
            title=title,
            hashtags=hashtags,
            status=PublishStatus.ready,
            package_path=package_path,
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        return True, "发布包已生成", job.id
