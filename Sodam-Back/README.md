d# 소담(SODAM) Backend API

소상공인을 위한 상권 진단 및 사업 추천 플랫폼의 백엔드 API 서버입니다.

## 🚀 주요 기능

- **상권 진단**: 5가지 핵심 지표를 통한 상권 건강도 분석
- **리스크 분류**: 4가지 리스크 유형 자동 분류 및 완화 전략 제시
- **전략 카드**: 맞춤형 사업 전략 및 실행 가이드 제공
- **지원 도구**: 전문가 상담, 정책 추천, 성공 사례 브라우징
- **지도 시각화**: 상권 데이터의 지도상 시각화 및 분석

## 📋 API 엔드포인트

### 🔐 인증 API (`/api/v1/sodam/auth/`)

- `POST /api/v1/sodam/auth/register` - 사용자 회원가입
- `POST /api/v1/sodam/auth/login` - 사용자 로그인

### 🏪 상권 진단 핵심 지표 API (`/api/v1/sodam/core-diagnosis/`)

- `GET /api/v1/sodam/core-diagnosis/foot-traffic/{market_code}` - 유동인구 변화량 분석
- `GET /api/v1/sodam/core-diagnosis/card-sales/{market_code}` - 카드매출 추이 분석
- `GET /api/v1/sodam/core-diagnosis/same-industry/{market_code}` - 동일업종 수 분석
- `GET /api/v1/sodam/core-diagnosis/business-rates/{market_code}` - 창업·폐업 비율 분석
- `GET /api/v1/sodam/core-diagnosis/dwell-time/{market_code}` - 체류시간 분석
- `GET/POST /api/v1/sodam/core-diagnosis/health-score/{market_code}` - 상권 건강 점수 종합 산정
- `POST /api/v1/sodam/core-diagnosis/comprehensive/{market_code}` - 종합 상권 진단

### 🏢 업종별 분석 API (`/api/v1/industry-analysis/`)

- `GET /api/v1/industry-analysis/` - 업종별 분석 메인
- `GET /api/v1/industry-analysis/survival-rates` - 업종별 생존율 분석
- `GET /api/v1/industry-analysis/closure-rates` - 업종별 폐업율 분석
- `GET /api/v1/industry-analysis/risk-analysis` - 업종별 리스크 분석
- `GET /api/v1/industry-analysis/trends` - 업종별 트렌드 분석
- `GET /api/v1/industry-analysis/competition` - 업종별 경쟁 분석

### 🏘️ 지역별 분석 API (`/api/v1/regional-analysis/`)

- `GET /api/v1/regional-analysis/` - 지역별 분석 메인
- `GET /api/v1/regional-analysis/population` - 지역별 인구 분석
- `GET /api/v1/regional-analysis/rent-rates` - 지역별 임대료 분석
- `GET /api/v1/regional-analysis/market-density` - 지역별 상권 밀도 분석
- `GET /api/v1/regional-analysis/demographics` - 지역별 인구통계 분석
- `GET /api/v1/regional-analysis/economic-indicators` - 지역별 경제 지표 분석

### 📊 종합 점수 계산 API (`/api/v1/scoring/`)

- `GET /api/v1/scoring/` - 점수 계산 메인
- `POST /api/v1/scoring/calculate` - 종합 점수 계산
- `POST /api/v1/scoring/compare` - 점수 비교 분석
- `POST /api/v1/scoring/recommendations` - 점수 기반 추천

### 🎯 추천 시스템 API (`/api/v1/recommendations/`)

- `GET /api/v1/recommendations/` - 추천 시스템 메인
- `POST /api/v1/recommendations/personalized` - 개인화 추천
- `POST /api/v1/recommendations/industry-based` - 업종 기반 추천
- `POST /api/v1/recommendations/region-based` - 지역 기반 추천
- `POST /api/v1/recommendations/similar-users` - 유사 사용자 기반 추천

### ⚠️ 리스크 분류 시스템 API (`/api/v1/risk-classification/`)

- `POST /api/v1/risk-classification/classify/{market_code}` - 4가지 리스크 유형 자동 분류
- `POST /api/v1/risk-classification/detailed-analysis/{market_code}` - 특정 리스크 유형의 상세 분석
- `GET /api/v1/risk-classification/risk-types` - 지원하는 리스크 유형 목록
- `GET /api/v1/risk-classification/mitigation-strategies` - 리스크 완화 전략 목록

### 🃏 전략 카드 시스템 API (`/api/v1/strategy-cards/`)

- `POST /api/v1/strategy-cards/generate` - 맞춤형 전략 카드 생성
- `GET /api/v1/strategy-cards/checklist/{strategy_id}` - 전략별 체크리스트 제공
- `GET /api/v1/strategy-cards/success-cases` - 성공 사례 제공
- `GET /api/v1/strategy-cards/templates` - 전략 템플릿 목록
- `GET /api/v1/strategy-cards/categories` - 전략 카테고리 목록
- `GET /api/v1/strategy-cards/difficulty-levels` - 난이도별 전략 목록

### 🛠️ 실행 지원 도구 API (`/api/v1/support-tools/`)

- `GET /api/v1/support-tools/support-centers` - 소상공인지원센터 정보 조회
- `GET /api/v1/support-tools/expert-consultation` - 전문가 상담 예약 정보
- `POST /api/v1/support-tools/policy-recommendations` - 지역 기반 맞춤 창업 지원 정책 추천
- `GET /api/v1/support-tools/success-cases` - 유사 상권 성공 사례 브라우징
- `POST /api/v1/support-tools/consultation-booking` - 전문가 상담 예약
- `POST /api/v1/support-tools/policy-application` - 정책 신청
- `GET /api/v1/support-tools/service-types` - 지원 서비스 유형 목록
- `GET /api/v1/support-tools/expertise-areas` - 전문가 전문 분야 목록

### 🗺️ 지도 기반 시각화 API (`/api/v1/map-visualization/`)

- `GET /api/v1/map-visualization/heatmap` - 상권 히트맵 데이터 생성
- `POST /api/v1/map-visualization/radius-analysis` - 반경별 분석 결과
- `GET /api/v1/map-visualization/cluster-analysis` - 상권 클러스터 분석
- `GET /api/v1/map-visualization/traffic-flow/{market_code}` - 유동인구 흐름 분석
- `GET /api/v1/map-visualization/accessibility/{market_code}` - 접근성 분석
- `GET /api/v1/map-visualization/analysis-types` - 지원하는 분석 유형 목록
- `GET /api/v1/map-visualization/regions` - 지원 지역 목록

### 🏪 상권 진단 API (`/api/v1/market-diagnosis/`)

- `GET /api/v1/market-diagnosis/` - 상권 진단 메인
- `GET /api/v1/market-diagnosis/markets` - 상권 목록 조회
- `GET /api/v1/market-diagnosis/markets/{market_code}` - 특정 상권 상세 정보
- `GET /api/v1/market-diagnosis/districts` - 구/군별 상권 분석
- `GET /api/v1/market-diagnosis/tourism-trend` - 관광 트렌드 분석
- `GET /api/v1/market-diagnosis/industry-analysis` - 상권별 업종 분석
- `GET /api/v1/market-diagnosis/regional-analysis` - 상권별 지역 분석

### 📋 기타 API

#### 시스템 API

- `GET /health` - 서버 상태 확인
- `GET /api/v1/sodam/` - API 기본 정보
- `GET /api/v1/sodam/markets` - 상권 목록 (실제 CSV 데이터)
- `GET /api/v1/sodam/test` - API 테스트
- `GET /api/v1/sodam/test-real-apis` - 실제 블루프린트 API 테스트
- `GET /api/v1/sodam/supported-industries` - 지원 업종 목록
- `GET /api/v1/sodam/supported-regions` - 지원 지역 목록

#### Swagger 문서

- `GET /docs/` - Swagger UI 문서
- `GET /api/v1/swagger.json` - API 스펙 JSON

## 🛠️ 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

```bash
export FLASK_APP=run_server.py
export FLASK_ENV=development
export JWT_SECRET_KEY=your-secret-key
export DATABASE_URL=sqlite:///instance/app.db
```

### 3. 데이터베이스 초기화

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 4. 서버 실행

```bash
python run_server.py
```

서버가 `http://localhost:5000`에서 실행됩니다.
배포 서버: `https://port-0-sodam-back-lyo9x8ghce54051e.sel5.cloudtype.app`

**배포된 서버**: `https://port-0-sodam-back-lyo9x8ghce54051e.sel5.cloudtype.app`

## 📊 데이터 소스

- **market_data.csv**: 상권 현황 데이터
- **tourism_consumption.csv**: 관광 소비 데이터
- **tourism_heatmap.csv**: 관광 소비 히트맵 데이터
- **industry_expenditure.csv**: 업종별 지출액 데이터
- **regional_expenditure.csv**: 지역별 지출액 데이터
- **regional_population.xlsx**: 지역별 인구수 데이터
- **regional_rent.xlsx**: 지역별 임대료 데이터
- **market_classification.xlsx**: 상권 분류 데이터

## 🔧 기술 스택

- **Framework**: Flask 3.0.3
- **Database**: SQLAlchemy 2.0.30
- **Authentication**: Flask-JWT-Extended 4.6.0
- **Data Processing**: Pandas 2.2.2
- **API Documentation**: Flask-RESTX 1.3.0
- **CORS**: Flask-CORS 4.0.0

## 📝 API 문서

Swagger UI를 통해 API 문서를 확인할 수 있습니다:

**로컬 개발 환경:**

- **Swagger UI**: `http://localhost:5003/docs/`
- **API JSON**: `http://localhost:5003/api/v1/swagger.json`

**배포된 서버:**

- **Swagger UI**: `https://port-0-sodam-back-lyo9x8ghce54051e.sel5.cloudtype.app/docs/`
- **API JSON**: `https://port-0-sodam-back-lyo9x8ghce54051e.sel5.cloudtype.app/api/v1/swagger.json`

## 🚀 배포

### Docker 배포

```bash
docker build -t sodam-backend .
docker run -p 5000:5000 sodam-backend
```

### 환경 변수

- `FLASK_ENV`: development/production
- `JWT_SECRET_KEY`: JWT 토큰 암호화 키
- `DATABASE_URL`: 데이터베이스 연결 URL
- `CORS_ORIGINS`: 허용할 CORS 오리진

## 📞 지원

- **개발팀**: SODAM Development Team
- **이메일**: support@sodam.kr
- **문서**: `DETAILED_SWAGGER_GUIDE.md` 참조
