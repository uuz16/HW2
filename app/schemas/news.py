from pydantic import BaseModel, Field
from typing import List

class NewsRequest(BaseModel):
    text: str = Field(..., title="뉴스 기사 본문 원문", min_length=10)

class AnalyzeResponse(BaseModel):
    is_reliable: bool = Field(..., description="신뢰 가능 여부")
    reliability_score: float = Field(..., description="신뢰도 점수 (0 ~ 100%)")
    suspicious_words: List[str] = Field(..., description="하이라이트 처리가 필요한 의심스러운/자극적인 단어 리스트")
    fact_check_sentences: List[str] = Field(..., description="의도나 주장이 강하게 들어가 팩트체크가 필요한 문장 리스트")
