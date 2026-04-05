import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from app.api.routes import router as api_router
from app.core.config import settings
import uvicorn

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION
)

# API 라우터 등록
app.include_router(api_router, prefix="/api")

@app.get("/", response_class=FileResponse, summary="웹 UI 서빙")
async def serve_ui():
    """메인 웹 UI 페이지를 서빙합니다."""
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail="index.html not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
