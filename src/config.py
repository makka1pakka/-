from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Compliant Video Ops"
    env: str = "dev"
    database_url: str = "sqlite:///./data/app.db"
    raw_dir: str = "./data/raw"
    processed_dir: str = "./output/processed"
    publish_dir: str = "./output/publish"
    ffmpeg_bin: str = "ffmpeg"
    ffprobe_bin: str = "ffprobe"
    brand_text: str = "@your_brand"


settings = Settings()

for folder in [settings.raw_dir, settings.processed_dir, settings.publish_dir]:
    Path(folder).mkdir(parents=True, exist_ok=True)
