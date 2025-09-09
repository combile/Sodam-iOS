# 소담(SODAM) Backend 배포 가이드

## 🚀 배포 준비 완료

백엔드 코드가 배포 준비가 완료되었습니다. 모든 불필요한 파일들이 정리되고, 파일명이 표준화되었습니다.

## 📁 정리된 파일 구조

### ✅ 유지된 핵심 파일들

```
backend/
├── app.py                          # Flask 애플리케이션 메인
├── run_server.py                   # 서버 실행 스크립트
├── wsgi.py                         # WSGI 진입점
├── config.py                       # 설정 파일
├── extensions.py                   # Flask 확장 설정
├── models.py                       # 데이터베이스 모델
├── requirements.txt                # Python 의존성
├── README.md                       # 프로젝트 문서
├── Dockerfile                      # Docker 이미지 빌드
├── docker-compose.yml              # Docker Compose 설정
├── .dockerignore                   # Docker 빌드 제외 파일
├── DEPLOYMENT_GUIDE.md             # 배포 가이드
├── ENHANCED_API_SPECIFICATION.md   # API 명세서
├── DETAILED_SWAGGER_GUIDE.md       # Swagger 가이드
├── swagger_docs.py                 # Swagger 문서 서버
├── blueprints/                     # API 블루프린트
│   ├── auth.py                     # 인증 API
│   ├── market_diagnosis.py         # 상권 진단 API
│   ├── industry_analysis.py        # 업종별 분석 API
│   ├── regional_analysis.py        # 지역별 분석 API
│   ├── scoring.py                  # 점수 계산 API
│   ├── recommendations.py          # 추천 시스템 API
│   ├── core_diagnosis.py           # 핵심 진단 API
│   ├── risk_classification.py      # 리스크 분류 API
│   ├── strategy_cards.py           # 전략 카드 API
│   ├── support_tools.py            # 지원 도구 API
│   └── map_visualization.py        # 지도 시각화 API
├── services/                       # 비즈니스 로직 서비스
│   ├── data_loader.py              # 데이터 로더
│   ├── core_diagnosis_service.py   # 핵심 진단 서비스
│   ├── risk_analysis_service.py    # 리스크 분석 서비스
│   ├── strategy_card_service.py    # 전략 카드 서비스
│   ├── support_tools_service.py    # 지원 도구 서비스
│   ├── map_visualization_service.py # 지도 시각화 서비스
│   ├── recommendation_service.py   # 추천 서비스
│   └── scoring_service.py          # 점수 계산 서비스
├── csv/                            # 데이터 파일들
│   ├── market_data.csv             # 상권 데이터
│   ├── tourism_consumption.csv     # 관광 소비 데이터
│   ├── tourism_heatmap.csv         # 관광 히트맵 데이터
│   ├── industry_expenditure.csv    # 업종별 지출 데이터
│   ├── regional_expenditure.csv    # 지역별 지출 데이터
│   ├── regional_population.xlsx    # 지역별 인구 데이터
│   ├── regional_rent.xlsx          # 지역별 임대료 데이터
│   └── market_classification.xlsx  # 상권 분류 데이터
├── migrations/                     # 데이터베이스 마이그레이션
└── instance/                       # 데이터베이스 파일
```

### ❌ 제거된 불필요한 파일들

- `blueprints/api.py` - 중복된 API 블루프린트
- `blueprints/community.py` - 사용하지 않는 커뮤니티 API
- `blueprints/diagnosis.py` - 중복된 진단 API
- `blueprints/recs.py` - 중복된 추천 API
- `blueprints/risk_analysis.py` - 중복된 리스크 분석 API
- `blueprints/strategy.py` - 중복된 전략 API
- `blueprints/success_cases.py` - 중복된 성공 사례 API
- `blueprints/support_centers.py` - 중복된 지원센터 API
- `blueprints/support.py` - 중복된 지원 API
- `services/recs_profiles.py` - 사용하지 않는 추천 프로필 서비스
- `services/recsys.py` - 사용하지 않는 추천 시스템 서비스
- `services/scoring.py` - 중복된 점수 계산 서비스
- `create_db.py` - 임시 데이터베이스 생성 스크립트
- `scripts/init_data.py` - 사용하지 않는 초기화 스크립트
- `API_DOCUMENTATION.md` - 중복된 API 문서
- `COMPLETE_API_SPECIFICATION.md` - 중복된 API 명세서
- `SWAGGER_GUIDE.md` - 중복된 Swagger 가이드

## 🔧 배포 방법

### 1. Docker를 사용한 배포

#### 단일 서비스 배포

```bash
# Docker 이미지 빌드
docker build -t sodam-backend .

# 컨테이너 실행
docker run -p 5000:5000 sodam-backend
```

#### Docker Compose를 사용한 배포

```bash
# 모든 서비스 실행 (API 서버 + Swagger 문서)
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 서비스 중지
docker-compose down
```

### 2. 직접 배포

#### 의존성 설치

```bash
pip install -r requirements.txt
```

#### 환경 변수 설정

```bash
export FLASK_ENV=production
export JWT_SECRET_KEY=your-production-secret-key
export DATABASE_URL=sqlite:///instance/app.db
```

#### 데이터베이스 초기화

```bash
flask db upgrade
```

#### 서버 실행

```bash
python run_server.py
```

## 🌐 서비스 접속

### API 서버

**로컬 개발 환경:**

- **URL**: `http://localhost:5000`
- **API 엔드포인트**: `http://localhost:5000/api/v1/`

**배포된 서버:**

- **URL**: `https://port-0-sodam-back-lyo9x8ghce54051e.sel5.cloudtype.app`
- **API 엔드포인트**: `https://port-0-sodam-back-lyo9x8ghce54051e.sel5.cloudtype.app/api/v1/`

### Swagger 문서 서버

- **URL**: `http://localhost:5003/docs/`
- **API JSON**: `http://localhost:5003/api/v1/swagger.json`

## 📊 주요 API 엔드포인트

### 인증

- `POST /api/v1/auth/login` - 로그인
- `POST /api/v1/auth/register` - 회원가입

### 상권 진단

- `GET /api/v1/core-diagnosis/foot-traffic/{market_code}` - 유동인구 분석
- `GET /api/v1/core-diagnosis/card-sales/{market_code}` - 카드매출 분석
- `GET /api/v1/core-diagnosis/same-industry/{market_code}` - 동일업종 분석
- `GET /api/v1/core-diagnosis/business-rates/{market_code}` - 창업·폐업 분석
- `GET /api/v1/core-diagnosis/dwell-time/{market_code}` - 체류시간 분석
- `POST /api/v1/core-diagnosis/health-score/{market_code}` - 건강 점수
- `POST /api/v1/core-diagnosis/comprehensive/{market_code}` - 종합 진단

### 리스크 분류

- `POST /api/v1/risk-classification/classify/{market_code}` - 리스크 분류
- `POST /api/v1/risk-classification/detailed-analysis/{market_code}` - 상세 분석
- `GET /api/v1/risk-classification/risk-types` - 리스크 유형 목록
- `GET /api/v1/risk-classification/mitigation-strategies` - 완화 전략

### 전략 카드

- `POST /api/v1/strategy-cards/generate` - 전략 카드 생성
- `GET /api/v1/strategy-cards/checklist/{strategy_id}` - 체크리스트
- `GET /api/v1/strategy-cards/success-cases` - 성공 사례
- `GET /api/v1/strategy-cards/templates` - 템플릿 목록
- `GET /api/v1/strategy-cards/categories` - 카테고리 목록

### 지원 도구

- `GET /api/v1/support-tools/support-centers` - 지원센터 정보
- `GET /api/v1/support-tools/expert-consultation` - 전문가 상담
- `POST /api/v1/support-tools/policy-recommendations` - 정책 추천
- `GET /api/v1/support-tools/success-cases` - 성공 사례
- `POST /api/v1/support-tools/consultation-booking` - 상담 예약
- `POST /api/v1/support-tools/policy-application` - 정책 신청

### 지도 시각화

- `GET /api/v1/map-visualization/heatmap` - 히트맵 데이터
- `POST /api/v1/map-visualization/radius-analysis` - 반경별 분석
- `GET /api/v1/map-visualization/cluster-analysis` - 클러스터 분석
- `GET /api/v1/map-visualization/traffic-flow/{market_code}` - 유동인구 흐름
- `GET /api/v1/map-visualization/accessibility/{market_code}` - 접근성 분석
- `GET /api/v1/map-visualization/analysis-types` - 분석 유형 목록

## 🔒 보안 설정

### 환경 변수

- `JWT_SECRET_KEY`: 강력한 비밀키 설정
- `FLASK_ENV`: production으로 설정
- `DATABASE_URL`: 보안된 데이터베이스 URL

### CORS 설정

- 허용된 오리진만 설정
- 필요한 HTTP 메서드만 허용
- 인증 헤더 포함

## 📈 모니터링

### 헬스 체크

```bash
# 로컬 환경
curl -f http://localhost:5000/api/v1/market-diagnosis/markets

# 배포된 서버
curl -f https://port-0-sodam-back-lyo9x8ghce54051e.sel5.cloudtype.app/api/v1/market-diagnosis/markets
```

### 로그 모니터링

```bash
# Docker 로그
docker-compose logs -f sodam-backend

# 직접 실행 로그
tail -f app.log
```

## 🚀 배포 완료!

모든 준비가 완료되었습니다. 이제 프로덕션 환경에 배포할 수 있습니다.

### 다음 단계

1. 환경 변수 설정
2. 데이터베이스 설정
3. 도메인 및 SSL 설정
4. 로드 밸런서 설정 (필요시)
5. 모니터링 시스템 구축

### 지원

- **문서**: `README.md`, `ENHANCED_API_SPECIFICATION.md`, `DETAILED_SWAGGER_GUIDE.md`
- **API 테스트**: Swagger UI (`http://localhost:5003/docs/`)
- **문제 해결**: 로그 확인 및 헬스 체크
