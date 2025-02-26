from __future__ import annotations

from shared.base import BaseModel


class AWSBedrockSettings(BaseModel):
    service_name: str
    model_id: str
    region: str
    access_key: str
    secret_access_key: str
    max_tokens: int
    temperature: float
    top_p: float
