from pathlib import Path
import shutil
import subprocess

from ..config import settings


class DownloadError(Exception):
    pass


def download_video(source_url: str, target_name: str) -> str:
    """
    合规说明：此下载器仅用于你有版权/授权的视频地址。
    默认尝试 yt-dlp；如果不可用则将 source_url 视为本地文件路径复制。
    """
    raw_dir = Path(settings.raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    out_path = raw_dir / f"{target_name}.mp4"

    ytdlp_cmd = [
        "yt-dlp",
        "-o",
        str(out_path),
        source_url,
    ]

    try:
        subprocess.run(ytdlp_cmd, check=True, capture_output=True, text=True)
        return str(out_path)
    except (subprocess.CalledProcessError, FileNotFoundError):
        src_path = Path(source_url)
        if src_path.exists() and src_path.is_file():
            shutil.copy2(src_path, out_path)
            return str(out_path)
        raise DownloadError("下载失败：请安装 yt-dlp 或提供本地可访问文件路径")
