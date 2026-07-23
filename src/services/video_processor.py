from pathlib import Path
import subprocess

from ..config import settings


class ProcessError(Exception):
    pass


def process_video(input_path: str, asset_id: int) -> tuple[str, str]:
    """
    生成处理后视频和封面图。
    处理逻辑：转为 1080x1920，叠加品牌文字。
    """
    processed_dir = Path(settings.processed_dir)
    processed_dir.mkdir(parents=True, exist_ok=True)

    output_video = processed_dir / f"asset_{asset_id}_processed.mp4"
    output_cover = processed_dir / f"asset_{asset_id}_cover.jpg"

    vf = (
        "scale=1080:1920:force_original_aspect_ratio=decrease,"
        "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,"
        f"drawtext=text='{settings.brand_text}':x=40:y=h-80:fontsize=36:fontcolor=white"
    )

    cmd_video = [
        settings.ffmpeg_bin,
        "-y",
        "-i",
        input_path,
        "-vf",
        vf,
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "22",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        str(output_video),
    ]

    cmd_cover = [
        settings.ffmpeg_bin,
        "-y",
        "-i",
        str(output_video),
        "-ss",
        "00:00:01",
        "-vframes",
        "1",
        str(output_cover),
    ]

    try:
        subprocess.run(cmd_video, check=True, capture_output=True, text=True)
        subprocess.run(cmd_cover, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        raise ProcessError(exc.stderr or "FFmpeg 处理失败") from exc

    return str(output_video), str(output_cover)
