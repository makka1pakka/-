from fastapi import FastAPI, HTTPException
from sqlalchemy import select

from .db import SessionLocal, init_db
from .models import Asset, PublishJob
from .pipeline.orchestrator import ingest_and_process_asset, prepare_publish_job
from .schemas import IngestRequest, ProcessResponse, PublishRequest

app = FastAPI(title="Compliant Video Ops", version="0.1.0")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.post("/assets/ingest", response_model=ProcessResponse)
def ingest_asset(payload: IngestRequest) -> ProcessResponse:
    with SessionLocal() as db:
        asset = Asset(
            source_url=payload.source_url,
            source_platform=payload.source_platform,
            license_note=payload.license_note,
            owner_name=payload.owner_name,
        )
        db.add(asset)
        db.commit()
        db.refresh(asset)

    ok, message = ingest_and_process_asset(asset.id)
    return ProcessResponse(asset_id=asset.id, status="success" if ok else "failed", message=message)


@app.get("/assets")
def list_assets() -> list[dict]:
    with SessionLocal() as db:
        rows = db.execute(select(Asset).order_by(Asset.id.desc())).scalars().all()
        return [
            {
                "id": a.id,
                "source_platform": a.source_platform,
                "owner_name": a.owner_name,
                "status": a.status.value,
                "sha256": a.sha256,
                "processed_path": a.processed_path,
                "error_message": a.error_message,
            }
            for a in rows
        ]


@app.post("/publish/prepare")
def publish_prepare(payload: PublishRequest) -> dict:
    ok, message, job_id = prepare_publish_job(payload.asset_id, payload.title, payload.hashtags)
    if not ok:
        raise HTTPException(status_code=400, detail=message)
    return {"ok": True, "job_id": job_id, "message": message}


@app.get("/publish/jobs")
def list_publish_jobs() -> list[dict]:
    with SessionLocal() as db:
        rows = db.execute(select(PublishJob).order_by(PublishJob.id.desc())).scalars().all()
        return [
            {
                "id": j.id,
                "asset_id": j.asset_id,
                "title": j.title,
                "hashtags": j.hashtags,
                "status": j.status.value,
                "package_path": j.package_path,
            }
            for j in rows
        ]
