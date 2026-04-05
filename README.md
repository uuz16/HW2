# 📰 뉴스 신뢰도 분석기 (News Reliability Analyzer)

머신러닝(HuggingFace)을 활용하여 뉴스 기사의 신뢰도를 분석하는 FastAPI 기반 서버 애플리케이션입니다. 
MLOps 파이프라인의 핵심 컴포넌트로 활용될 수 있도록 설계되었으며, 분석된 데이터를 프론트엔드 UI를 통해 직관적으로 확인할 수 있습니다.

## ✨ 주요 기능
- **신뢰도 판별 (%)**: 분석된 텍스트의 신뢰도를 퍼센트로 반환
- **의심 단어 하이라이트**: 자극적이거나 어그로성 짙은 단어를 잡아내어 추출
- **팩트 체크 구문 추출**: 확신성이 부족하거나 강한 주장이 섞인 문장을 감지

## 📂 프로젝트 구조
```text
news_analyzer/
├── main.py              # 애플리케이션 진입점 및 FastAPI 앱 초기화
├── requirements.txt     # 프로젝트 패키지 의존성 목록
├── README.md            # 프로젝트 설명 문서
├── index.html           # 메인 웹 대시보드 UI
└── app/                 # 앱 메인 로직 디렉토리
    ├── api/
    │   └── routes.py    # API 엔드포인트 라우팅
    ├── core/
    │   └── config.py    # 환경 설정 및 설정값 관리
    ├── schemas/
    │   └── news.py      # Pydantic 기반 요청/응답 데이터 검증 모델
    └── services/
        └── news_analyzer.py  # HuggingFace 머신러닝 모델 추론 로직
```

## 🚀 실행 방법

### 1. 패키지 설치
Windows 환경의 파이썬 터미널에서 애플리케이션 구동에 필요한 의존성 패키지를 설치합니다.
```bash
pip install -r requirements.txt
```

### 2. 서버 구동
명령어를 통해 로컬 서버를 실행합니다. 처음 서버가 켜질 때, HuggingFace 사전학습 모델 가중치를 자동으로 다운로드하므로 약간의 시간이 소요될 수 있습니다.
```bash
python main.py
```

### 3. 접속
- **웹 UI (추천)**: 서버 구동 후 인터넷 브라우저로 `http://localhost:8000/` 에 접속하시면 글래스모피즘 스타일의 대시보드에서 직접 뉴스를 테스트할 수 있습니다.
- **API 문서(Swagger)**: 브라우저에서 `http://localhost:8000/docs` 경로로 접속 시 자동으로 생성된 API 명세서를 확인할 수 있습니다.

## 📡 API 사용 예시

### `POST /api/analyze`
뉴스 기사 원문을 분석하여 결과를 반환합니다.

**Request Body (JSON)**:
```json
{
  "text": "충격! 단독 보도입니다. 아무거나 넣어도 검출되는 시스템 폭로."
}
```

**Response (JSON)**:
```json
{
  "is_reliable": false,
  "reliability_score": 15.3,
  "suspicious_words": [
    "충격",
    "단독",
    "폭로"
  ],
  "fact_check_sentences": [
    "아무거나 넣어도 검출되는 시스템 폭로."
  ]
}
```
