from flask import Blueprint, request, jsonify
from services.strategy_card_service import StrategyCardService
from datetime import datetime
from typing import Dict, List, Any

strategy_cards_bp = Blueprint('strategy_cards', __name__, url_prefix='/api/v1/strategy-cards')

strategy_card_service = StrategyCardService()

@strategy_cards_bp.route('/generate', methods=['POST'])
def generate_strategy_cards():
    """
    맞춤형 전략 카드 생성
    
    상권, 업종, 리스크 유형, 사용자 프로필을 기반으로 맞춤형 사업 전략 카드를 생성합니다.
    
    ### 요청 본문
    ```json
    {
        "market_code": "DJ001",
        "industry": "식음료업",
        "risk_type": "과포화 경쟁형",
        "user_profile": {
            "userType": "ENTREPRENEUR",
            "businessStage": "PLANNING",
            "experience": "초보",
            "budget": "중간"
        }
    }
    ```
    
    ### 필수 파라미터
    - **market_code**: 상권 코드
    - **industry**: 업종
    - **risk_type**: 리스크 유형 (유입 저조형, 과포화 경쟁형, 소비력 약형, 성장 잠재형)
    - **user_profile**: 사용자 프로필 정보
    
    ### 응답 예시
    ```json
    {
        "success": true,
        "data": {
            "strategy_cards": [
                {
                    "id": "STR001",
                    "category": "마케팅",
                    "title": "차별화된 브랜딩 전략",
                    "description": "경쟁이 치열한 환경에서 차별화된 브랜드 아이덴티티 구축",
                    "difficulty": "중간",
                    "estimated_time": "2-3개월",
                    "success_rate": "70%",
                    "checklist": [
                        "브랜드 컨셉 정의",
                        "로고 및 디자인 제작",
                        "마케팅 메시지 개발"
                    ],
                    "tips": [
                        "고유한 스토리텔링 활용",
                        "타겟 고객층 명확히 정의"
                    ]
                }
            ],
            "total_cards": 5,
            "generated_at": "2024-01-01T00:00:00Z"
        }
    }
    ```
    
    ### 전략 카테고리
    - **마케팅**: 브랜딩, 홍보, 고객 유치
    - **경쟁력**: 차별화, 품질 향상, 서비스 개선
    - **운영**: 효율성, 비용 절감, 프로세스 개선
    - **혁신**: 신기술 도입, 새로운 비즈니스 모델
    - **채널**: 판매 채널 확대, 온라인 진출
    - **고객관리**: 고객 충성도, 관계 관리
    
    ### 에러 코드
    - **400**: 필수 파라미터 누락
    - **500**: 서버 내부 오류
    """
    try:
        data = request.get_json() or {}
        
        # 필수 파라미터 검증
        required_fields = ['market_code', 'industry', 'risk_type', 'user_profile']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": f"{field}이 필요합니다."
                    }
                }), 400
        
        strategy_cards = strategy_card_service.generate_strategy_cards(
            data['market_code'],
            data['industry'],
            data['risk_type'],
            data['user_profile']
        )
        
        return jsonify({
            "success": True,
            "data": strategy_cards
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        }), 500

@strategy_cards_bp.route('/checklist/<string:strategy_id>', methods=['GET'])
def get_strategy_checklist(strategy_id: str):
    """전략별 체크리스트 제공"""
    try:
        checklist = strategy_card_service.get_strategy_checklist(strategy_id)
        
        if "error" in checklist:
            return jsonify({
                "success": False,
                "error": {
                    "code": "DATA_NOT_FOUND",
                    "message": checklist["error"]
                }
            }), 404
        
        return jsonify({
            "success": True,
            "data": checklist
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        }), 500

@strategy_cards_bp.route('/success-cases', methods=['GET'])
def get_success_cases():
    """성공 사례 제공"""
    try:
        industry = request.args.get('industry')
        strategy_type = request.args.get('strategy_type')
        
        success_cases = strategy_card_service.get_success_cases(industry, strategy_type)
        
        return jsonify({
            "success": True,
            "data": success_cases
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        }), 500

@strategy_cards_bp.route('/templates', methods=['GET'])
def get_strategy_templates():
    """전략 템플릿 목록"""
    try:
        category = request.args.get('category')
        difficulty = request.args.get('difficulty')
        
        # 모든 전략 템플릿 가져오기
        templates = strategy_card_service.strategy_templates
        
        # 필터링
        filtered_templates = []
        for template_id, template in templates.items():
            if category and template['category'] != category:
                continue
            if difficulty and template['difficulty'] != difficulty:
                continue
            filtered_templates.append({
                "id": template_id,
                **template
            })
        
        return jsonify({
            "success": True,
            "data": {
                "total_templates": len(filtered_templates),
                "templates": filtered_templates,
                "filters": {
                    "category": category,
                    "difficulty": difficulty
                }
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        }), 500

@strategy_cards_bp.route('/categories', methods=['GET'])
def get_strategy_categories():
    """전략 카테고리 목록"""
    try:
        categories = [
            {
                "id": "marketing",
                "name": "마케팅",
                "description": "유동인구 증가 및 브랜드 인지도 향상",
                "template_count": 2
            },
            {
                "id": "competition",
                "name": "경쟁력",
                "description": "경쟁 우위 확보 및 차별화",
                "template_count": 1
            },
            {
                "id": "operations",
                "name": "운영",
                "description": "운영 효율성 및 비용 최적화",
                "template_count": 1
            },
            {
                "id": "innovation",
                "name": "혁신",
                "description": "혁신적 비즈니스 모델 도입",
                "template_count": 1
            },
            {
                "id": "channels",
                "name": "채널",
                "description": "판매 채널 확대 및 다각화",
                "template_count": 1
            },
            {
                "id": "customer_management",
                "name": "고객관리",
                "description": "고객 충성도 향상 및 관계 관리",
                "template_count": 1
            }
        ]
        
        return jsonify({
            "success": True,
            "data": {
                "total_categories": len(categories),
                "categories": categories
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        }), 500

@strategy_cards_bp.route('/difficulty-levels', methods=['GET'])
def get_difficulty_levels():
    """난이도 레벨 정보"""
    try:
        difficulty_levels = [
            {
                "level": "낮음",
                "description": "초보자도 쉽게 실행할 수 있는 전략",
                "required_experience": "경험 불필요",
                "estimated_time": "1-2개월",
                "success_rate": "80-90%"
            },
            {
                "level": "중간",
                "description": "일정한 경험과 자원이 필요한 전략",
                "required_experience": "1-3년",
                "estimated_time": "2-4개월",
                "success_rate": "60-80%"
            },
            {
                "level": "높음",
                "description": "상당한 전문성과 자원이 필요한 전략",
                "required_experience": "3-5년",
                "estimated_time": "3-6개월",
                "success_rate": "40-60%"
            },
            {
                "level": "매우 높음",
                "description": "높은 전문성과 상당한 자원이 필요한 전략",
                "required_experience": "5년 이상",
                "estimated_time": "6-12개월",
                "success_rate": "20-40%"
            }
        ]
        
        return jsonify({
            "success": True,
            "data": {
                "difficulty_levels": difficulty_levels
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        }), 500
