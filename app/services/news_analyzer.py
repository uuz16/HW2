import re
from transformers import pipeline
from app.core.config import settings

class NewsAnalyzer:
    def __init__(self):
        print(f"[{settings.PROJECT_NAME}] 모델 로딩 중... ({settings.MODEL_NAME})")
        # 실제 환경 배포시 파인튜닝된 단일 모델이나 더 가벼운 모델로 교체를 권장합니다.
        self.zero_shot_classifier = pipeline(
            "zero-shot-classification",
            model=settings.MODEL_NAME
        )
        print("모델 로딩 완료!")

    def _split_into_sentences(self, text: str):
        """간단한 정규식을 사용한 한국어 문장 분리기"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def analyze(self, text: str) -> dict:
        # 문서 전체의 신뢰도/가짜뉴스 판별
        labels = ["믿을 수 있는 객관적인 뉴스", "자극적이고 허위 사실이 포함된 가짜 뉴스"]
        doc_result = self.zero_shot_classifier(text, labels)
        
        scores = dict(zip(doc_result['labels'], doc_result['scores']))
        
        reliability_score = scores.get('믿을 수 있는 객관적인 뉴스', 0.0) * 100
        is_reliable = reliability_score >= 50.0

        # 카테고리 분류
        category_labels = ["정치", "경제", "사회", "과학", "세계", "문화"]
        cat_result = self.zero_shot_classifier(text, category_labels)
        category = cat_result['labels'][0]

        sentences = self._split_into_sentences(text)
        fact_check_sentences = []
        suspicious_words = set()

        sentence_labels = ["팩트 체크가 필요한 주관적 주장", "단순한 사실 전달"]
        suspicious_keywords = ["충격", "경악", "단독", "절대", "무조건", "폭로", "우수수", "발칵"]

        for sentence in sentences:
            if len(sentence) < 10:
                continue
            
            for word in suspicious_keywords:
                if word in sentence:
                    suspicious_words.add(word)
            
            s_result = self.zero_shot_classifier(sentence, sentence_labels)
            s_scores = dict(zip(s_result['labels'], s_result['scores']))
            
            if s_scores.get('팩트 체크가 필요한 주관적 주장', 0.0) > 0.6:
                fact_check_sentences.append(sentence)

        # 신뢰도 평가 근거 생성
        credibility_reasons = []
        if suspicious_words:
            credibility_reasons.append("클릭베이트, 감정적이거나 과장된 의심스러운 단어가 사용되었습니다.")
        if fact_check_sentences:
            credibility_reasons.append("단순 사실 전달을 넘어선 주관적이거나 과장된 주장이 담긴 문장이 발견되었습니다.")
        if reliability_score < 50.0:
            credibility_reasons.append("전반적인 내용과 표현이 객관적 뉴스 신뢰 기준치(50%)에 미달합니다.")
        if not credibility_reasons:
            credibility_reasons.append("특별히 의심스럽거나 과장된 표현이 발견되지 않은 객관적 성향의 기사입니다.")

        return {
            "is_reliable": is_reliable,
            "reliability_score": round(reliability_score, 2),
            "suspicious_words": list(suspicious_words),
            "fact_check_sentences": fact_check_sentences,
            "category": category,
            "credibility_reasons": credibility_reasons
        }

# 애플리케이션 수명주기 동안 사용할 싱글톤 모델 객체 생성
analyzer = NewsAnalyzer()
