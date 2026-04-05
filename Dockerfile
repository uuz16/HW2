FROM python:3.11-slim

# 파이썬 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Windows 환경에서 작성된 파일의 CRLF(줄바꿈) 문제를 방지하기 위해 필요한 경우 활용
# 주로 쉘 스크립트(.sh)를 실행할 때 문제가 생기지만, 파이썬 파일에서는 큰 문제 없이 작동합니다.

WORKDIR /app

# 시스템 빌드 도구 설치 (C extension 등을 컴파일할 때 필요)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 패키지 요구사항 파일 복사 및 설치
COPY requirements.txt .

# PyTorch 등 무거운 라이브러리가 있으므로 캐시를 사용하지 않고 CPU 전용 버전을 설치하도록 최적화 할 수도 있습니다.
# requirements.txt에 torch가 명시되어 있으므로 그대로 설치합니다.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 전체 애플리케이션 코드 복사
COPY . .

# FastAPI가 사용할 8000번 포트 노출
EXPOSE 8000

# 애플리케이션 실행 (명령어)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
