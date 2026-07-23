from pathlib import Path
import hashlib

from PIL import Image
import imagehash


class FingerprintError(Exception):
    pass


def compute_sha256(file_path: str) -> str:
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def compute_phash_from_cover(image_path: str) -> str:
    if not Path(image_path).exists():
        raise FingerprintError("封面图不存在，无法计算 pHash")
    image = Image.open(image_path)
    return str(imagehash.phash(image))
