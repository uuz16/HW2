import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "News Reliability Analyzer API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "MLOps 기반 파이프라인을 위한 뉴스 신뢰도 분석 API 서버"
    MODEL_NAME: str = "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"

settings = Settings()
