from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from extensions import db, bcrypt
from models import User
from flask_jwt_extended import create_access_token
from datetime import datetime

auth_ns = Namespace('auth', description='사용자 인증 및 회원가입 API')

# 모델 정의
login_model = auth_ns.model('LoginRequest', {
    'username': fields.String(
        required=True, 
        description='사용자 아이디 (영문, 숫자, 3-20자)', 
        example='daejeon_user',
        min_length=3,
        max_length=20
    ),
    'password': fields.String(
        required=True, 
        description='비밀번호 (8자 이상, 영문, 숫자, 특수문자 포함)', 
        example='password123!',
        min_length=8
    )
})

register_model = auth_ns.model('RegisterRequest', {
    'username': fields.String(
        required=True, 
        description='사용자 아이디 (영문, 숫자, 3-20자, 중복 불가)', 
        example='daejeon_user',
        min_length=3,
        max_length=20
    ),
    'email': fields.String(
        required=True, 
        description='이메일 주소 (유효한 이메일 형식, 중복 불가)', 
        example='user@daejeon.kr',
        pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    ),
    'password': fields.String(
        required=True, 
        description='비밀번호 (8자 이상, 영문, 숫자, 특수문자 포함)', 
        example='password123!',
        min_length=8
    ),
    'name': fields.String(
        required=True, 
        description='실명 (한글, 영문, 2-10자)', 
        example='홍길동',
        min_length=2,
        max_length=10
    ),
    'nickname': fields.String(
        description='닉네임 (선택사항, 2-10자)', 
        example='대전사업가',
        min_length=2,
        max_length=10
    ),
    'userType': fields.String(
        description='사용자 유형', 
        example='ENTREPRENEUR',
        enum=['ENTREPRENEUR', 'BUSINESS_OWNER', 'INVESTOR']
    ),
    'businessStage': fields.String(
        description='사업 단계', 
        example='PLANNING',
        enum=['PLANNING', 'STARTUP', 'OPERATING']
    ),
    'phone': fields.String(
        description='전화번호 (010-XXXX-XXXX 형식)', 
        example='010-1234-5678',
        pattern=r'^010-\d{4}-\d{4}$'
    ),
    'interestedBusinessTypes': fields.List(
        fields.String, 
        description='관심 업종 목록 (다중 선택 가능)', 
        example=['식음료업', '쇼핑업'],
        enum=['식음료업', '쇼핑업', '숙박업', '여가서비스업', '운송업', '의료업', '교육업', '문화업', '스포츠업', '기타서비스업']
    ),
    'preferredAreas': fields.List(
        fields.String, 
        description='선호 지역 목록 (다중 선택 가능)', 
        example=['중구', '서구'],
        enum=['동구', '중구', '서구', '유성구', '대덕구']
    )
})

success_response = auth_ns.model('SuccessResponse', {
    'success': fields.Boolean(description='성공 여부', example=True),
    'message': fields.String(description='응답 메시지', example='요청이 성공적으로 처리되었습니다.'),
    'data': fields.Raw(description='응답 데이터')
})

error_response = auth_ns.model('ErrorResponse', {
    'success': fields.Boolean(description='성공 여부', example=False),
    'error': fields.Raw(description='에러 정보')
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model)
    @auth_ns.marshal_with(success_response)
    @auth_ns.doc('register', 
        description='''
        ## 사용자 회원가입
        
        새로운 사용자를 시스템에 등록합니다.
        
        ### 요청 파라미터
        - **username**: 사용자 아이디 (필수, 3-20자, 영문/숫자)
        - **email**: 이메일 주소 (필수, 유효한 이메일 형식)
        - **password**: 비밀번호 (필수, 8자 이상)
        - **name**: 실명 (필수, 2-10자)
        - **nickname**: 닉네임 (선택, 2-10자)
        - **userType**: 사용자 유형 (선택, ENTREPRENEUR/BUSINESS_OWNER/INVESTOR)
        - **businessStage**: 사업 단계 (선택, PLANNING/STARTUP/OPERATING)
        - **phone**: 전화번호 (선택, 010-XXXX-XXXX 형식)
        - **interestedBusinessTypes**: 관심 업종 (선택, 배열)
        - **preferredAreas**: 선호 지역 (선택, 배열)
        
        ### 응답 예시
        ```json
        {
            "success": true,
            "message": "회원가입이 완료되었습니다.",
            "data": {
                "user": {
                    "id": 1,
                    "username": "daejeon_user",
                    "email": "user@daejeon.kr",
                    "name": "홍길동",
                    "userType": "ENTREPRENEUR",
                    "businessStage": "PLANNING"
                }
            },
            "timestamp": "2024-01-01T00:00:00Z"
        }
        ```
        
        ### 에러 코드
        - **400**: 필수 파라미터 누락 또는 유효성 검사 실패
        - **409**: 아이디 또는 이메일 중복
        - **500**: 서버 내부 오류
        ''')
    def post(self):
        data = request.get_json() or {}
        username = (data.get("username") or "").strip()
        email = (data.get("email") or "").strip().lower()
        password = (data.get("password") or "").strip()
        name = (data.get("name") or "").strip()
        nickname = (data.get("nickname") or "").strip()
        user_type = data.get("userType", "ENTREPRENEUR")
        business_stage = data.get("businessStage")
        phone = data.get("phone")
        interested_business_types = data.get("interestedBusinessTypes", [])
        preferred_areas = data.get("preferredAreas", [])
        profile_image = data.get("profileImage")

        # 필수 필드 검증
        if not username or not email or not password or not name:
            return jsonify({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "아이디, 이메일, 비밀번호, 이름은 필수입니다.",
                    "details": {}
                }
            }), 400

        # 아이디 중복 검사
        if User.query.filter_by(username=username).first():
            return jsonify({
                "success": False,
                "error": {
                    "code": "CONFLICT",
                    "message": "이미 사용 중인 아이디입니다.",
                    "details": {"field": "username"}
                }
            }), 409

        # 이메일 중복 검사
        if User.query.filter_by(email=email).first():
            return jsonify({
                "success": False,
                "error": {
                    "code": "CONFLICT",
                    "message": "이미 사용 중인 이메일입니다.",
                    "details": {"field": "email"}
                }
            }), 409

        # 비밀번호 길이 검증
        if len(password) < 8:
            return jsonify({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "비밀번호는 8자 이상이어야 합니다.",
                    "details": {"field": "password"}
                }
            }), 400

        pw_hash = bcrypt.generate_password_hash(password).decode()
        user = User(
            username=username,
            email=email,
            name=name,
            nickname=nickname,
            password_hash=pw_hash,
            user_type=user_type,
            business_stage=business_stage,
            phone=phone,
            interested_business_types=interested_business_types,
            preferred_areas=preferred_areas,
            profile_image=profile_image
        )
        
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "success": True,
            "data": {
                "user": user.to_dict()
            },
            "message": "회원가입이 완료되었습니다.",
            "timestamp": datetime.utcnow().isoformat()
        }), 201

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.marshal_with(success_response)
    @auth_ns.doc('login', 
        description='''
        ## 사용자 로그인
        
        사용자 인증을 통해 JWT 액세스 토큰을 발급받습니다.
        
        ### 요청 파라미터
        - **username**: 사용자 아이디 (필수)
        - **password**: 비밀번호 (필수)
        
        ### 응답 예시
        ```json
        {
            "success": true,
            "message": "로그인에 성공했습니다.",
            "data": {
                "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "user": {
                    "id": 1,
                    "username": "daejeon_user",
                    "email": "user@daejeon.kr",
                    "name": "홍길동",
                    "userType": "ENTREPRENEUR",
                    "businessStage": "PLANNING"
                }
            },
            "timestamp": "2024-01-01T00:00:00Z"
        }
        ```
        
        ### JWT 토큰 사용법
        발급받은 토큰을 Authorization 헤더에 포함하여 API 요청:
        ```
        Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
        ```
        
        ### 에러 코드
        - **400**: 아이디 또는 비밀번호 누락
        - **401**: 잘못된 아이디 또는 비밀번호
        - **403**: 비활성화된 계정
        - **500**: 서버 내부 오류
        ''')
    def post(self):
        data = request.get_json() or {}
        username = (data.get("username") or "").strip()  # 아이디로 로그인
        password = (data.get("password") or "").strip()

        if not username or not password:
            return jsonify({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "아이디와 비밀번호를 입력해주세요.",
                    "details": {}
                }
            }), 400

        # 아이디로 사용자 찾기
        user = User.query.filter_by(username=username).first()
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            return jsonify({
                "success": False,
                "error": {
                    "code": "UNAUTHORIZED",
                    "message": "아이디 또는 비밀번호가 올바르지 않습니다.",
                    "details": {}
                }
            }), 401

        # 비활성화된 계정 확인
        if not user.is_active:
            return jsonify({
                "success": False,
                "error": {
                    "code": "FORBIDDEN",
                    "message": "비활성화된 계정입니다.",
                    "details": {}
                }
            }), 403

        # JWT 토큰 생성
        token = create_access_token(identity=user.id)
        
        return jsonify({
            "success": True,
            "data": {
                "accessToken": token,
                "user": user.to_dict()
            },
            "message": "로그인에 성공했습니다.",
            "timestamp": datetime.utcnow().isoformat()
        }), 200
