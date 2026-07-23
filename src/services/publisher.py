from pathlib import Path
import json
import shutil

from ..config import settings


def create_publish_package(asset_id: int, video_path: str, title: str, hashtags: str) -> str:
    """
    生成发布包（视频+metadata），用于手动或后续 API 自动提交。
    """
    publish_root = Path(settings.publish_dir) / f"job_{asset_id}"
    publish_root.mkdir(parents=True, exist_ok=True)

    target_video = publish_root / "video.mp4"
    shutil.copy2(video_path, target_video)

    metadata = {
        "asset_id": asset_id,
        "title": title,
        "hashtags": hashtags,
        "platform": "douyin",
        "mode": "assistant_publish",
        "note": "请在发布前人工复核版权和文案",
    }
    meta_path = publish_root / "metadata.json"
    meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(publish_root)
