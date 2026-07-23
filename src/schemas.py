from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    source_url: str = Field(..., min_length=10)
    source_platform: str = Field(..., min_length=2)
    license_note: str = Field(..., min_length=2, description="授权说明，例如 self-owned 或 license-id")
    owner_name: str = Field(..., min_length=1)


class PublishRequest(BaseModel):
    asset_id: int
    title: str = Field(..., min_length=2, max_length=200)
    hashtags: str = Field(default="#原创 #二创")


class ProcessResponse(BaseModel):
    asset_id: int
    status: str
    message: str
