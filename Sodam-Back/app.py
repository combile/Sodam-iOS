from flask import Flask, request
from datetime import datetime
from flask_restx import Api, Resource, fields
from config import Config
from extensions import db, migrate, bcrypt, jwt, cors
from models import User
from blueprints.auth import auth_ns
from blueprints.market_diagnosis import market_diagnosis_bp
from blueprints.industry_analysis import industry_analysis_bp
from blueprints.regional_analysis import regional_analysis_bp
from blueprints.scoring import scoring_bp
from blueprints.recommendations import recommendations_bp
from blueprints.core_diagnosis import core_diagnosis_ns
from blueprints.risk_classification import risk_classification_bp
from blueprints.strategy_cards import strategy_cards_bp
from blueprints.support_tools import support_tools_bp
from blueprints.map_visualization import map_visualization_bp

def create_app(config_object: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Extensions 초기화
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Flask-RESTX API 설정
    api = Api(
        app,
        version='1.0',
        title='소담(SODAM) API',
        description='''
        # 소담(SODAM) - 소상공인 상권 진단 및 사업 추천 플랫폼 API
        
        ## 개요
        소담(SODAM)은 소상공인을 위한 종합적인 상권 진단 및 사업 추천 플랫폼입니다.
        대전광역시를 중심으로 한 상권 데이터를 기반으로 다음과 같은 서비스를 제공합니다:
        
        ## 주요 기능
        - **상권 진단**: 유동인구, 매출, 경쟁도 등 종합 분석
        - **업종별 분석**: 생존율, 폐업율, 리스크 분석
        - **지역별 분석**: 인구, 임대료, 경제 지표 분석
        - **리스크 분류**: 4가지 리스크 유형 자동 분류
        - **전략 카드**: 맞춤형 사업 전략 제안
        - **지원 도구**: 정책 지원, 전문가 상담 연결
        - **지도 시각화**: 히트맵, 클러스터 분석
        
        ## API 사용법
        1. **인증**: JWT 토큰 기반 인증 (회원가입/로그인 필요)
        2. **요청**: JSON 형태로 데이터 전송
        3. **응답**: 표준화된 JSON 응답 형식
        4. **에러 처리**: HTTP 상태 코드와 상세 에러 메시지
        
        ## 환경별 접속 정보
        - **개발 환경**: 로컬 개발 시 사용
        - **배포 환경**: 실제 서비스 운영 환경 (권장)
        
        ## 기본 URL
        - 개발 서버: `http://localhost:5000`
        - 배포 서버: `https://port-0-sodam-back-lyo9x8ghce54051e.sel5.cloudtype.app`
        - API 엔드포인트: `https://port-0-sodam-back-lyo9x8ghce54051e.sel5.cloudtype.app/api/v1`
        - Swagger 문서: `https://port-0-sodam-back-lyo9x8ghce54051e.sel5.cloudtype.app/docs/`
        
        ## 지원 지역
        - 대전광역시 (동구, 중구, 서구, 유성구, 대덕구)
        
        ## 지원 업종
        - 식음료업, 쇼핑업, 숙박업, 여가서비스업, 운송업
        - 의료업, 교육업, 문화업, 스포츠업, 기타서비스업
        ''',
        doc='/docs/',  # Swagger UI 경로
        prefix='/api/v1',
        catch_all_404s=True,  # 404 에러를 API에서 처리
        contact='SODAM Development Team',
        contact_email='sodam@example.com',
        license='MIT',
        license_url='https://opensource.org/licenses/MIT'
    )
    
    # CORS 설정
    cors.init_app(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
            "supports_credentials": True
        }
    })
    
    # CORS 헤더를 모든 응답에 추가
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    # 기본 엔드포인트들 (Flask-RESTX와 충돌 방지)
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'SODAM Backend API is running'}, 200

    # Swagger 네임스페이스 정의
    ns = api.namespace('sodam', description='SODAM API operations')
    
    # Swagger 모델 정의
    market_model = api.model('Market', {
        'id': fields.Integer(required=True, description='상권 ID'),
        'name': fields.String(required=True, description='상권명'),
        'area': fields.String(required=True, description='지역'),
        'code': fields.String(description='상권 코드')
    })
    
    # Swagger 엔드포인트 추가
    @ns.route('/')
    class APIInfo(Resource):
        @ns.doc('api_info')
        def get(self):
            """API 기본 정보"""
            return {
                'message': 'SODAM Backend API', 
                'version': '1.0.0',
                'status': 'running',
                'endpoints': {
                    'health': '/health',
                    'swagger': '/swagger/',
                    'docs': '/docs/'
                },
                'available_apis': [
                    'auth', 'market-diagnosis', 'industry-analysis', 
                    'regional-analysis', 'scoring', 'recommendations',
                    'core-diagnosis', 'risk-classification', 'strategy-cards',
                    'support-tools', 'map-visualization'
                ]
            }, 200
    
    @ns.route('/markets')
    class MarketList(Resource):
        @ns.doc('get_markets')
        @ns.marshal_list_with(market_model)
        def get(self):
            """상권 목록 조회 (실제 CSV 데이터)"""
            try:
                from services.data_loader import DataLoader
                data_loader = DataLoader()
                markets = data_loader.get_market_list()
                return markets[:20], 200  # 처음 20개만 반환
            except Exception as e:
                api.abort(500, f'CSV 데이터 로드 실패: {str(e)}')
    
    @ns.route('/test')
    class TestAPI(Resource):
        @ns.doc('test_api')
        def get(self):
            """API 테스트"""
            return {
                'message': 'SODAM API 정상 작동',
                'timestamp': datetime.now().isoformat(),
                'status': 'success'
            }, 200
    
    @ns.route('/test-real-apis')
    class TestRealAPIs(Resource):
        @ns.doc('test_real_apis')
        def get(self):
            """실제 블루프린트 API 테스트"""
            import requests
            base_url = request.host_url.rstrip('/')
            
            test_results = {}
            
            # 실제 API 엔드포인트들 테스트
            test_endpoints = [
                '/api/v1/auth/',
                '/api/v1/market-diagnosis/',
                '/api/v1/core-diagnosis/foot-traffic/10000',
                '/api/v1/industry-analysis/',
                '/api/v1/regional-analysis/',
                '/api/v1/scoring/',
                '/api/v1/recommendations/',
                '/api/v1/risk-classification/',
                '/api/v1/strategy-cards/',
                '/api/v1/support-tools/',
                '/api/v1/map-visualization/'
            ]
            
            for endpoint in test_endpoints:
                try:
                    # 내부에서 직접 호출
                    with app.test_client() as client:
                        response = client.get(endpoint)
                        test_results[endpoint] = {
                            'status_code': response.status_code,
                            'success': response.status_code < 400,
                            'message': 'OK' if response.status_code < 400 else 'Error'
                        }
                except Exception as e:
                    test_results[endpoint] = {
                        'status_code': 500,
                        'success': False,
                        'message': str(e)
                    }
            
            return {
                'message': '실제 블루프린트 API 테스트 결과',
                'timestamp': datetime.now().isoformat(),
                'test_results': test_results
            }, 200
    
    @ns.route('/supported-industries')
    class SupportedIndustries(Resource):
        @ns.doc('supported_industries', 
            description='''
            ## 지원 업종 목록
            
            SODAM 플랫폼에서 지원하는 모든 업종 목록을 조회합니다.
            프론트엔드에서 드롭다운, 체크박스 등의 UI 컴포넌트 생성 시 사용할 수 있습니다.
            
            ### 응답 예시
            ```json
            {
                "success": true,
                "data": {
                    "total_industries": 10,
                    "industries": [
                        {
                            "code": "food_beverage",
                            "name": "식음료업",
                            "description": "음식점, 카페, 베이커리 등",
                            "category": "서비스업"
                        }
                    ],
                    "categories": {
                        "서비스업": ["식음료업", "쇼핑업", "숙박업", "여가서비스업", "운송업"],
                        "전문업": ["의료업", "교육업", "문화업", "스포츠업", "기타서비스업"]
                    }
                }
            }
            ```
            ''')
        def get(self):
            """지원 업종 목록 조회"""
            industries = [
                {
                    "code": "food_beverage",
                    "name": "식음료업",
                    "description": "음식점, 카페, 베이커리, 주점 등",
                    "category": "서비스업",
                    "icon": "🍽️"
                },
                {
                    "code": "retail",
                    "name": "쇼핑업",
                    "description": "소매업, 도매업, 온라인 쇼핑몰 등",
                    "category": "서비스업",
                    "icon": "🛍️"
                },
                {
                    "code": "accommodation",
                    "name": "숙박업",
                    "description": "호텔, 펜션, 게스트하우스 등",
                    "category": "서비스업",
                    "icon": "🏨"
                },
                {
                    "code": "leisure",
                    "name": "여가서비스업",
                    "description": "헬스클럽, 노래방, PC방, 게임장 등",
                    "category": "서비스업",
                    "icon": "🎮"
                },
                {
                    "code": "transportation",
                    "name": "운송업",
                    "description": "택시, 배달, 물류, 운송 서비스 등",
                    "category": "서비스업",
                    "icon": "🚗"
                },
                {
                    "code": "medical",
                    "name": "의료업",
                    "description": "병원, 약국, 의료기기, 헬스케어 등",
                    "category": "전문업",
                    "icon": "🏥"
                },
                {
                    "code": "education",
                    "name": "교육업",
                    "description": "학원, 과외, 온라인 교육, 교육 콘텐츠 등",
                    "category": "전문업",
                    "icon": "📚"
                },
                {
                    "code": "culture",
                    "name": "문화업",
                    "description": "영화관, 전시관, 공연장, 문화센터 등",
                    "category": "전문업",
                    "icon": "🎭"
                },
                {
                    "code": "sports",
                    "name": "스포츠업",
                    "description": "체육관, 스포츠 용품, 스포츠 교육 등",
                    "category": "전문업",
                    "icon": "⚽"
                },
                {
                    "code": "other_services",
                    "name": "기타서비스업",
                    "description": "미용실, 세탁소, 수리업, 기타 서비스 등",
                    "category": "전문업",
                    "icon": "🔧"
                }
            ]
            
            # 카테고리별 분류
            categories = {}
            for industry in industries:
                category = industry["category"]
                if category not in categories:
                    categories[category] = []
                categories[category].append(industry["name"])
            
            return {
                "success": True,
                "data": {
                    "total_industries": len(industries),
                    "industries": industries,
                    "categories": categories,
                    "last_updated": "2024-01-01"
                },
                "message": "지원 업종 목록을 성공적으로 조회했습니다.",
                "timestamp": datetime.now().isoformat()
            }, 200
    
    @ns.route('/supported-regions')
    class SupportedRegions(Resource):
        @ns.doc('supported_regions',
            description='''
            ## 지원 지역 목록
            
            SODAM 플랫폼에서 지원하는 모든 지역 목록을 조회합니다.
            대전광역시를 중심으로 한 지역 정보를 제공합니다.
            
            ### 응답 예시
            ```json
            {
                "success": true,
                "data": {
                    "total_regions": 5,
                    "regions": [
                        {
                            "code": "dong_gu",
                            "name": "동구",
                            "full_name": "대전광역시 동구",
                            "population": 95000,
                            "area_km2": 136.5,
                            "market_count": 4
                        }
                    ],
                    "city_info": {
                        "name": "대전광역시",
                        "total_population": 1440000,
                        "total_area": 539.2,
                        "total_markets": 26
                    }
                }
            }
            ```
            ''')
        def get(self):
            """지원 지역 목록 조회"""
            regions = [
                {
                    "code": "dong_gu",
                    "name": "동구",
                    "full_name": "대전광역시 동구",
                    "population": 95000,
                    "area_km2": 136.5,
                    "market_count": 4,
                    "description": "대전의 동쪽 지역, 주거지역 중심"
                },
                {
                    "code": "jung_gu",
                    "name": "중구",
                    "full_name": "대전광역시 중구",
                    "population": 120000,
                    "area_km2": 62.1,
                    "market_count": 2,
                    "description": "대전의 중심가, 상업지역 중심"
                },
                {
                    "code": "seo_gu",
                    "name": "서구",
                    "full_name": "대전광역시 서구",
                    "population": 180000,
                    "area_km2": 95.2,
                    "market_count": 11,
                    "description": "대전의 서쪽 지역, 신도시 개발지역"
                },
                {
                    "code": "yuseong_gu",
                    "name": "유성구",
                    "full_name": "대전광역시 유성구",
                    "population": 220000,
                    "area_km2": 177.0,
                    "market_count": 6,
                    "description": "대덕연구개발특구, 대학가 지역"
                },
                {
                    "code": "daedeok_gu",
                    "name": "대덕구",
                    "full_name": "대전광역시 대덕구",
                    "population": 75000,
                    "area_km2": 68.4,
                    "market_count": 3,
                    "description": "대덕연구개발특구, 산업단지 지역"
                }
            ]
            
            city_info = {
                "name": "대전광역시",
                "total_population": sum(region["population"] for region in regions),
                "total_area": sum(region["area_km2"] for region in regions),
                "total_markets": sum(region["market_count"] for region in regions),
                "description": "대한민국 중부에 위치한 광역시, 과학기술 특화 도시"
            }
            
            return {
                "success": True,
                "data": {
                    "total_regions": len(regions),
                    "regions": regions,
                    "city_info": city_info,
                    "last_updated": "2024-01-01"
                },
                "message": "지원 지역 목록을 성공적으로 조회했습니다.",
                "timestamp": datetime.now().isoformat()
            }, 200
    
    # 실제 블루프린트 엔드포인트들을 Swagger에 등록
    
    # 인증 API
    @ns.route('/auth/login')
    class AuthLogin(Resource):
        @ns.doc('auth_login')
        def post(self):
            """사용자 로그인"""
            data = request.get_json()
            
            if not data:
                return {'message': 'No data provided'}, 400
                
            username = data.get('username')
            password = data.get('password')
            
            if not all([username, password]):
                return {'message': 'Missing username or password'}, 400
                
            try:
                # 사용자 찾기
                user = User.query.filter_by(username=username).first()
                if not user or not bcrypt.check_password_hash(user.password_hash, password):
                    return {'message': 'Invalid username or password'}, 401
                
                # JWT 토큰 생성 (간단한 더미 토큰)
                from flask_jwt_extended import create_access_token
                token = create_access_token(identity=user.id)
                
                return {
                    'message': 'Login successful',
                    'access_token': token,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'name': user.name
                    }
                }, 200
                
            except Exception as e:
                return {'message': str(e)}, 500
    
    @ns.route('/auth/register')
    class AuthRegister(Resource):
        @ns.doc('auth_register')
        def post(self):
            """사용자 회원가입"""
            data = request.get_json()
            
            if not data:
                return {'message': 'No data provided'}, 400
                
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            name = data.get('name')
            
            if not all([username, email, password, name]):
                return {'message': 'Missing required fields'}, 400
                
            try:
                # 아이디 중복 검사
                if User.query.filter_by(username=username).first():
                    return {'message': 'Username already exists'}, 409
                
                # 이메일 중복 검사
                if User.query.filter_by(email=email).first():
                    return {'message': 'Email already exists'}, 409
                
                # 비밀번호 해싱
                pw_hash = bcrypt.generate_password_hash(password).decode()
                
                # 사용자 생성
                user = User(
                    username=username,
                    email=email,
                    name=name,
                    password_hash=pw_hash
                )
                
                # 데이터베이스에 저장
                db.session.add(user)
                db.session.commit()
                
                return {
                    'message': 'User registered successfully',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'name': user.name
                    }
                }, 201
                
            except Exception as e:
                db.session.rollback()
                return {'message': str(e)}, 500
    
    # 상권 진단 API
    @ns.route('/market-diagnosis/markets')
    class MarketDiagnosisMarkets(Resource):
        @ns.doc('market_diagnosis_markets')
        def get(self):
            """상권 목록 조회"""
            try:
                # 실제 상권 목록 조회 로직 구현
                # TODO: 데이터베이스에서 상권 목록 조회
                
                return {
                    'markets': [
                        {'code': 'GANGNAM', 'name': '강남구', 'region': '서울'},
                        {'code': 'HONGDAE', 'name': '홍대', 'region': '서울'},
                        {'code': 'MYEONGDONG', 'name': '명동', 'region': '서울'}
                    ]
                }, 200
                
            except Exception as e:
                return {'message': str(e)}, 500
    
    @ns.route('/market-diagnosis/markets/<string:market_code>')
    class MarketDiagnosisMarketDetail(Resource):
        @ns.doc('market_diagnosis_market_detail')
        def get(self, market_code):
            """상권 상세 정보"""
            try:
                # 실제 상권 상세 정보 조회 로직 구현
                # TODO: 데이터베이스에서 상권 상세 정보 조회
                
                return {
                    'market_code': market_code,
                    'name': f'{market_code} 상권',
                    'region': '서울',
                    'description': '상권 상세 정보',
                    'coordinates': {'lat': 37.5665, 'lng': 126.9780}
                }, 200
                
            except Exception as e:
                return {'message': str(e)}, 500
    
    # 핵심 진단 API
    @ns.route('/core-diagnosis/foot-traffic/<string:market_code>')
    class CoreDiagnosisFootTraffic(Resource):
        @ns.doc('core_diagnosis_foot_traffic')
        def get(self, market_code):
            """유동인구 변화량 분석"""
            try:
                # 실제 유동인구 분석 로직 구현
                # TODO: 데이터베이스에서 유동인구 데이터 조회 및 분석
                
                return {
                    'market_code': market_code,
                    'foot_traffic_change': 15.5,
                    'trend': 'increasing',
                    'period': '2024-09',
                    'data': {
                        'current': 1250,
                        'previous': 1080,
                        'change_rate': 15.5
                    }
                }, 200
                
            except Exception as e:
                return {'message': str(e)}, 500
    
    @ns.route('/core-diagnosis/card-sales/<string:market_code>')
    class CoreDiagnosisCardSales(Resource):
        @ns.doc('core_diagnosis_card_sales')
        def get(self, market_code):
            """카드매출 추이 분석"""
            try:
                # 실제 카드매출 분석 로직 구현
                # TODO: 데이터베이스에서 카드매출 데이터 조회 및 분석
                
                return {
                    'market_code': market_code,
                    'sales_trend': 8.2,
                    'growth_rate': 12.5,
                    'period': '2024-09',
                    'data': {
                        'current_month': 2500000,
                        'previous_month': 2300000,
                        'growth_rate': 8.2
                    }
                }, 200
                
            except Exception as e:
                return {'message': str(e)}, 500
    
    @ns.route('/core-diagnosis/same-industry/<string:market_code>')
    class CoreDiagnosisSameIndustry(Resource):
        @ns.doc('core_diagnosis_same_industry')
        def get(self, market_code):
            """동일업종 수 분석"""
            try:
                # 실제 동일업종 분석 로직 구현
                # TODO: 데이터베이스에서 동일업종 데이터 조회 및 분석
                
                return {
                    'market_code': market_code,
                    'same_industry_count': 45,
                    'density': 0.8,
                    'competition_level': 'high',
                    'data': {
                        'total_businesses': 120,
                        'same_industry': 45,
                        'density_score': 0.8
                    }
                }, 200
                
            except Exception as e:
                return {'message': str(e)}, 500
    
    @ns.route('/core-diagnosis/business-rates/<string:market_code>')
    class CoreDiagnosisBusinessRates(Resource):
        @ns.doc('core_diagnosis_business_rates')
        def get(self, market_code):
            """창업·폐업 비율 분석"""
            try:
                # 실제 창업·폐업 비율 분석 로직 구현
                # TODO: 데이터베이스에서 창업·폐업 데이터 조회 및 분석
                
                return {
                    'market_code': market_code,
                    'startup_rate': 12.5,
                    'closure_rate': 8.3,
                    'net_growth': 4.2,
                    'data': {
                        'new_businesses': 15,
                        'closed_businesses': 10,
                        'net_growth': 5
                    }
                }, 200
                
            except Exception as e:
                return {'message': str(e)}, 500
    
    @ns.route('/core-diagnosis/dwell-time/<string:market_code>')
    class CoreDiagnosisDwellTime(Resource):
        @ns.doc('core_diagnosis_dwell_time')
        def get(self, market_code):
            """체류시간 분석"""
            try:
                # 실제 체류시간 분석 로직 구현
                # TODO: 데이터베이스에서 체류시간 데이터 조회 및 분석
                
                return {
                    'market_code': market_code,
                    'average_dwell_time': 45.5,
                    'trend': 'stable',
                    'period': '2024-09',
                    'data': {
                        'current': 45.5,
                        'previous': 43.2,
                        'change_rate': 5.3
                    }
                }, 200
                
            except Exception as e:
                return {'message': str(e)}, 500
    
    @ns.route('/core-diagnosis/health-score/<string:market_code>')
    class CoreDiagnosisHealthScore(Resource):
        @ns.doc('core_diagnosis_health_score')
        def get(self, market_code):
            """상권 건강 점수 종합 산정 (GET)"""
            try:
                # 쿼리 파라미터에서 정보 가져오기
                industry = request.args.get('industry')
                category = request.args.get('category')
                sub_category = request.args.get('sub_category')
                
                # 실제 CoreDiagnosisService 사용
                from services.core_diagnosis_service import CoreDiagnosisService
                service = CoreDiagnosisService()
                result = service.calculate_health_score(market_code, industry, category, sub_category)
                
                if "error" in result:
                    return {'message': result['error']}, 400
                
                return {
                    'market_code': result['market_code'],
                    'health_score': result['total_score'],
                    'factors': {
                        'foot_traffic': result['score_breakdown']['foot_traffic']['score'],
                        'card_sales': result['score_breakdown']['card_sales']['score'],
                        'competition': result['score_breakdown'].get('competition', {}).get('score', 0),
                        'business_rates': result['score_breakdown']['business_rates']['score'],
                        'dwell_time': result['score_breakdown']['dwell_time']['score']
                    },
                    'recommendation': result['health_status']
                }, 200
                
            except Exception as e:
                return {'message': str(e)}, 500
        
        def post(self, market_code):
            """상권 건강 점수 종합 산정"""
            try:
                data = request.get_json() or {}
                industry = data.get('industry')
                category = data.get('category')
                sub_category = data.get('sub_category')
                
                # 실제 CoreDiagnosisService 사용
                from services.core_diagnosis_service import CoreDiagnosisService
                service = CoreDiagnosisService()
                result = service.calculate_health_score(market_code, industry, category, sub_category)
                
                if "error" in result:
                    return {'message': result['error']}, 400
                
                return {
                    'market_code': result['market_code'],
                    'health_score': result['total_score'],
                    'factors': {
                        'foot_traffic': result['score_breakdown']['foot_traffic']['score'],
                        'card_sales': result['score_breakdown']['card_sales']['score'],
                        'competition': result['score_breakdown'].get('competition', {}).get('score', 0),
                        'business_rates': result['score_breakdown']['business_rates']['score'],
                        'dwell_time': result['score_breakdown']['dwell_time']['score']
                    },
                    'recommendation': result['health_status']
                }, 200
                
            except Exception as e:
                return {'message': str(e)}, 500
    
    @ns.route('/core-diagnosis/comprehensive/<string:market_code>')
    class CoreDiagnosisComprehensive(Resource):
        @ns.doc('core_diagnosis_comprehensive')
        def post(self, market_code):
            """종합 상권 진단"""
            try:
                data = request.get_json() or {}
                
                # 프론트엔드에서 보내는 category, sub_category를 industry로 변환
                category = data.get('category', '')
                sub_category = data.get('sub_category', '')
                
                # 업종 정보 결정 (sub_category가 있으면 우선, 없으면 category 사용)
                industry = sub_category if sub_category else category
                
                # 실제 CoreDiagnosisService 사용
                from services.core_diagnosis_service import CoreDiagnosisService
                service = CoreDiagnosisService()
                result = service.calculate_health_score(market_code, industry, category, sub_category)
                
                if "error" in result:
                    return {'message': result['error']}, 400
                
                # 상세 분석 데이터도 가져오기
                foot_traffic = service.get_foot_traffic_analysis(market_code)
                card_sales = service.get_card_sales_analysis(market_code)
                business_rates = service.get_business_rates_analysis(market_code)
                dwell_time = service.get_dwell_time_analysis(market_code)
                
                # 강점과 약점 분석
                strengths = []
                weaknesses = []
                
                if result['score_breakdown']['foot_traffic']['score'] >= 80:
                    strengths.append('유동인구 증가')
                elif result['score_breakdown']['foot_traffic']['score'] < 60:
                    weaknesses.append('유동인구 감소')
                
                if result['score_breakdown']['card_sales']['score'] >= 80:
                    strengths.append('카드매출 증가')
                elif result['score_breakdown']['card_sales']['score'] < 60:
                    weaknesses.append('카드매출 감소')
                
                if result['score_breakdown']['business_rates']['score'] >= 80:
                    strengths.append('창업 활성화')
                elif result['score_breakdown']['business_rates']['score'] < 60:
                    weaknesses.append('창업 부진')
                
                if result['score_breakdown']['dwell_time']['score'] >= 80:
                    strengths.append('체류시간 양호')
                elif result['score_breakdown']['dwell_time']['score'] < 60:
                    weaknesses.append('체류시간 부족')
                
                return {
                    'market_code': market_code,
                    'overall_score': result['total_score'],
                    'indicators': {
                        'foot_traffic': result['score_breakdown']['foot_traffic']['score'],
                        'card_sales': result['score_breakdown']['card_sales']['score'],
                        'competition': result['score_breakdown'].get('competition', {}).get('score', 0),
                        'business_rates': result['score_breakdown']['business_rates']['score'],
                        'dwell_time': result['score_breakdown']['dwell_time']['score']
                    },
                    'strengths': strengths,
                    'weaknesses': weaknesses,
                    'recommendations': result.get('recommendations', [])
                }, 200
                
            except Exception as e:
                return {'message': str(e)}, 500

    # Blueprints 등록
    api.add_namespace(auth_ns, path="/sodam/auth")
    app.register_blueprint(market_diagnosis_bp, url_prefix="/api/v1/market-diagnosis")
    app.register_blueprint(industry_analysis_bp, url_prefix="/api/v1/industry-analysis")
    app.register_blueprint(regional_analysis_bp, url_prefix="/api/v1/regional-analysis")
    app.register_blueprint(scoring_bp, url_prefix="/api/v1/scoring")
    app.register_blueprint(recommendations_bp, url_prefix="/api/v1/recommendations")
    api.add_namespace(core_diagnosis_ns, path="/sodam/core-diagnosis")
    app.register_blueprint(risk_classification_bp, url_prefix="/api/v1/risk-classification")
    app.register_blueprint(strategy_cards_bp, url_prefix="/api/v1/strategy-cards")
    app.register_blueprint(support_tools_bp, url_prefix="/api/v1/support-tools")
    app.register_blueprint(map_visualization_bp, url_prefix="/api/v1/map-visualization")
    
    return app
