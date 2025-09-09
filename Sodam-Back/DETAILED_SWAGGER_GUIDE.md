# 소담(SODAM) 상세 Swagger API 문서 가이드

## 🎯 플랫폼 개요

### 소담(SODAM)이란?

소상공인을 위한 상권 진단 및 사업 추천 플랫폼으로, 창업 및 사업 운영에 필요한 종합적인 분석과 지원을 제공합니다.

### 🚀 주요 특징

- **실제 데이터 기반**: 샘플 데이터가 아닌 실제 상권 데이터 활용
- **종합적 분석**: 5가지 핵심 지표를 통한 정확한 상권 평가
- **개인화 추천**: 사용자 프로필 기반 맞춤형 솔루션 제공
- **실행 중심**: 이론이 아닌 실제 실행 가능한 전략 제시
- **시각화 지원**: 지도 기반 직관적 데이터 표현

## 📊 데이터 소스

- **실제 상권 현황 데이터**: CSV 파일 기반 실제 상권 정보
- **관광 소비액 데이터**: 지역별 관광 소비 트렌드
- **업종별/지역별 지출 데이터**: 업종별 소비 패턴 분석
- **실시간 상권 분석 데이터**: 동적 분석 결과

## 🔧 기술 스택

- **Backend**: Flask, SQLAlchemy, Pandas
- **API**: RESTful API, JWT 인증
- **Documentation**: Swagger/OpenAPI 3.0
- **Data**: CSV 파일 기반 실제 데이터

---

## 🎯 Swagger API 문서 접속 방법

### 1. Swagger UI 접속

- **URL**: `http://localhost:5003/docs/`
- **포트**: 5003 (기존 API 서버와 분리)
- **인터페이스**: 완전한 Swagger UI 인터페이스
- **특징**: 상세한 설명, 예시 코드, 인터랙티브 테스트 기능

### 2. API JSON 스펙 접속

- **URL**: `http://localhost:5003/api/v1/swagger.json`
- **용도**: API 스펙을 JSON 형태로 다운로드
- **형식**: OpenAPI 3.0 표준 준수

### 3. 실제 API 서버

- **URL**: `http://localhost:5000/api/v1/`
- **용도**: 실제 API 호출 및 테스트

---

## 📋 상세 API 네임스페이스 구성

### 🔐 인증 API (`/auth`)

#### 주요 기능

- 사용자 회원가입 (사용자명, 이메일, 비밀번호, 프로필 정보)
- 사용자 로그인 (사용자명 기반)
- JWT 토큰 발급 및 관리

#### API 엔드포인트

- **POST** `/auth/login` - 사용자 로그인
- **POST** `/auth/register` - 사용자 회원가입

#### 사용 방법

1. 먼저 회원가입을 통해 계정을 생성하세요
2. 로그인을 통해 JWT 토큰을 발급받으세요
3. 이후 API 호출 시 Authorization 헤더에 토큰을 포함하세요

### 🏥 상권 진단 핵심 지표 API (`/core-diagnosis`)

#### 5가지 핵심 지표

1. **유동인구 변화량**: 상권 내 유동인구의 변화 추이 분석
2. **카드매출 추이**: 카드 결제 매출의 변화 패턴 분석
3. **동일업종 수**: 경쟁업체 수 및 경쟁 강도 분석
4. **창업·폐업 비율**: 상권 내 사업체의 생존율 및 변화율 분석
5. **체류시간**: 고객의 평균 체류시간 및 시간대별 분석

#### 분석 결과

- 각 지표별 점수 및 등급 (A, B, C, D)
- 종합 건강 점수 및 최종 등급
- 상세한 분석 결과 및 개선 방안 제시

#### API 엔드포인트

- **GET** `/core-diagnosis/foot-traffic/{market_code}` - 유동인구 변화량 분석
- **GET** `/core-diagnosis/card-sales/{market_code}` - 카드매출 추이 분석
- **GET** `/core-diagnosis/same-industry/{market_code}` - 동일업종 수 분석
- **GET** `/core-diagnosis/business-rates/{market_code}` - 창업·폐업 비율 분석
- **GET** `/core-diagnosis/dwell-time/{market_code}` - 체류시간 분석
- **POST** `/core-diagnosis/health-score/{market_code}` - 상권 건강 점수 종합 산정
- **POST** `/core-diagnosis/comprehensive/{market_code}` - 종합 상권 진단

### ⚠️ 리스크 분류 시스템 API (`/risk-classification`)

#### 4가지 리스크 유형

1. **유입 저조형**: 유동인구와 매출 증가율이 낮아 상권 활성화가 저조한 상태
2. **과포화 경쟁형**: 동일업종 사업체가 과도하게 많아 경쟁이 치열한 상태
3. **소비력 약형**: 지역 주민의 소비력이 약해 매출 증대가 어려운 상태
4. **성장 잠재형**: 성장 잠재력은 있지만 현재는 부진한 상태

#### 제공 기능

- 자동 리스크 분류 및 점수 산정
- 리스크별 상세 분석 및 원인 파악
- 완화 전략 및 실행 방안 제시
- 성공 사례 기반 해결책 제안

#### API 엔드포인트

- **POST** `/risk-classification/classify/{market_code}` - 4가지 리스크 유형 자동 분류
- **POST** `/risk-classification/detailed-analysis/{market_code}` - 특정 리스크 유형의 상세 분석
- **GET** `/risk-classification/risk-types` - 지원하는 리스크 유형 목록
- **GET** `/risk-classification/mitigation-strategies` - 리스크 완화 전략 목록

### 🎯 전략 카드 시스템 API (`/strategy-cards`)

#### 전략 카드 구성

- **전략명**: 구체적인 전략 제목
- **카테고리**: 마케팅, 고객관리, 운영, 재무 등
- **난이도**: 초급, 중급, 고급
- **소요 기간**: 1-3개월, 3-6개월, 6개월 이상
- **비용 수준**: 낮음, 중간, 높음
- **예상 효과**: 구체적인 성과 지표
- **성공 확률**: 통계 기반 성공 가능성

#### 제공 기능

- 개인화된 전략 카드 생성
- 단계별 체크리스트 제공
- 실행 팁 및 주의사항 안내
- 성공 사례 및 참고 자료 제공

#### API 엔드포인트

- **POST** `/strategy-cards/generate` - 맞춤형 전략 카드 생성
- **GET** `/strategy-cards/checklist/{strategy_id}` - 전략별 체크리스트 제공
- **GET** `/strategy-cards/success-cases` - 성공 사례 제공
- **GET** `/strategy-cards/templates` - 전략 템플릿 목록
- **GET** `/strategy-cards/categories` - 전략 카테고리 목록

### 🛠️ 실행 지원 도구 API (`/support-tools`)

#### 주요 지원 도구

1. **소상공인지원센터**: 지역별 지원센터 정보 및 서비스 안내
2. **전문가 상담**: 창업 컨설턴트, 경영 전문가 상담 예약
3. **정책 추천**: 맞춤형 창업 지원 정책 및 신청 가이드
4. **성공 사례**: 유사 상권의 성공 사례 및 학습 자료
5. **상담 예약**: 전문가 상담 일정 예약 및 관리
6. **정책 신청**: 지원 정책 신청 및 진행 상황 추적

#### 지원 범위

- 창업 초기 자금 지원
- 경영 컨설팅 및 교육
- 마케팅 지원 및 홍보
- 법무 및 세무 상담

#### API 엔드포인트

- **GET** `/support-tools/support-centers` - 소상공인지원센터 정보 조회
- **GET** `/support-tools/expert-consultation` - 전문가 상담 예약 정보
- **POST** `/support-tools/policy-recommendations` - 지역 기반 맞춤 창업 지원 정책 추천
- **GET** `/support-tools/success-cases` - 유사 상권 성공 사례 브라우징
- **POST** `/support-tools/consultation-booking` - 전문가 상담 예약
- **POST** `/support-tools/policy-application` - 정책 신청

### 🗺️ 지도 기반 시각화 API (`/map-visualization`)

#### 시각화 유형

1. **히트맵**: 상권별 건강도, 유동인구, 경쟁도 등을 색상으로 표현
2. **반경별 분석**: 특정 지점을 중심으로 반경 내 상권 분석
3. **클러스터 분석**: 유사한 특성을 가진 상권들을 그룹화
4. **유동인구 흐름**: 시간대별 유동인구 이동 패턴 분석
5. **접근성 분석**: 교통편, 주차, 보행자 접근성 평가

#### 분석 기능

- 실시간 데이터 기반 시각화
- 인터랙티브 지도 조작
- 다층 데이터 오버레이
- 반경별 필터링 및 분석

#### API 엔드포인트

- **GET** `/map-visualization/heatmap` - 상권 히트맵 데이터 생성
- **POST** `/map-visualization/radius-analysis` - 반경별 분석 결과
- **GET** `/map-visualization/cluster-analysis` - 상권 클러스터 분석
- **GET** `/map-visualization/traffic-flow/{market_code}` - 유동인구 흐름 분석
- **GET** `/map-visualization/accessibility/{market_code}` - 접근성 분석
- **GET** `/map-visualization/analysis-types` - 지원하는 분석 유형 목록

---

## 🔧 Swagger UI 사용법

### 1. API 테스트 방법

1. **Swagger UI 접속**: `http://localhost:5003/docs/`
2. **원하는 API 선택**: 네임스페이스별로 그룹화된 API 목록 확인
3. **API 상세 정보 확인**: 각 API의 파라미터, 요청/응답 형식 확인
4. **"Try it out" 버튼 클릭**: API 테스트 모드 활성화
5. **파라미터 입력**: 필요한 파라미터 값 입력
6. **"Execute" 버튼 클릭**: API 호출 실행
7. **결과 확인**: 응답 코드, 헤더, 바디 확인

### 2. 주요 기능

- **인터랙티브 테스트**: 브라우저에서 직접 API 테스트 가능
- **모델 스키마**: 요청/응답 데이터 구조 확인
- **예제 데이터**: 샘플 요청/응답 데이터 제공
- **에러 코드**: 가능한 에러 코드 및 메시지 확인
- **인증**: JWT 토큰 기반 인증 지원

### 3. 데이터 모델

- **LoginRequest**: 로그인 요청 데이터
- **RegisterRequest**: 회원가입 요청 데이터
- **UserProfile**: 사용자 프로필 데이터
- **StrategyCard**: 전략 카드 데이터
- **SupportCenter**: 지원센터 데이터
- **HeatmapData**: 히트맵 데이터
- **SuccessResponse**: 성공 응답 형식
- **ErrorResponse**: 에러 응답 형식

---

## 🚀 실제 API 서버와의 연동

### 1. 서버 실행

```bash
# Swagger 문서 서버 (포트 5003)
python backend/swagger_docs.py

# 실제 API 서버 (포트 5002)
python backend/run_server.py
```

### 2. API 호출 예시

```bash
# 실제 API 서버로 직접 호출
curl -X GET "http://localhost:5000/api/v1/core-diagnosis/foot-traffic/10000"

# Swagger UI를 통한 테스트
# 브라우저에서 http://localhost:5003/docs/ 접속 후 테스트
```

---

## 📝 API 문서 특징

### ✅ 완전한 문서화

- **50+ API 엔드포인트** 완전 문서화
- **상세한 파라미터 설명** 및 예시
- **요청/응답 스키마** 정의
- **에러 코드** 및 메시지 정의

### ✅ 사용자 친화적

- **네임스페이스별 그룹화**로 쉬운 탐색
- **인터랙티브 테스트** 기능
- **한국어 설명** 및 메시지
- **실제 사용 가능한** API 스펙

### ✅ 개발자 도구

- **OpenAPI 3.0** 표준 준수
- **JSON 스펙 다운로드** 가능
- **코드 생성** 지원 (다양한 언어)
- **API 클라이언트** 자동 생성

---

## 🎯 주요 사용 시나리오

### 1. 개발자 온보딩

- 새로운 개발자가 API 구조를 빠르게 이해
- 각 엔드포인트의 사용법 학습
- 실제 데이터로 테스트하며 학습

### 2. API 테스트

- 프론트엔드 개발 시 API 동작 확인
- 백엔드 개발 시 응답 형식 검증
- 통합 테스트 시 API 호출 검증

### 3. 문서화

- 클라이언트 개발자를 위한 API 가이드
- 외부 파트너사와의 API 연동 가이드
- 팀 내 API 사용법 공유

---

## 🔗 관련 링크

- **Swagger UI**: `http://localhost:5003/docs/`
- **API JSON**: `http://localhost:5003/api/v1/swagger.json`
- **실제 API 서버**: `http://localhost:5000/api/v1/`
- **API 명세서**: `backend/ENHANCED_API_SPECIFICATION.md`

---

## 📞 지원 및 문의

- **개발팀**: SODAM Development Team
- **이메일**: support@sodam.kr
- **문서**: 이 Swagger UI를 통해 모든 API를 테스트할 수 있습니다

---

**🎉 완전한 Swagger API 문서가 준비되었습니다!**

브라우저에서 `http://localhost:5003/docs/`에 접속하여 모든 API를 테스트해보세요!
