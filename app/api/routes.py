from fastapi import APIRouter, HTTPException
from app.schemas.news import NewsRequest, AnalyzeResponse
from app.services.news_analyzer import analyzer

router = APIRouter()

@router.get("/health", summary="서버 헬스 체크용 (MLOps Liveness Probe 지정용)")
async def health_check():
    return {"status": "healthy", "model_loaded": True}

@router.post("/analyze", response_model=AnalyzeResponse, summary="뉴스 텍스트 신뢰도 분석")
async def analyze_news(request: NewsRequest):
    """
    들어온 뉴스 텍스트를 허깅페이스 모델을 통해 분석하고,
    신뢰도, 의심 단어, 팩트체크 대상 문장을 반환합니다.
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    
    try:
        # 모델 추론 진행
        result = analyzer.analyze(request.text.strip())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")
