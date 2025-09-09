from flask import Blueprint, request, jsonify
from services.support_tools_service import SupportToolsService
from datetime import datetime
from typing import Dict, List, Any

support_tools_bp = Blueprint('support_tools', __name__, url_prefix='/api/v1/support-tools')

support_tools_service = SupportToolsService()

@support_tools_bp.route('/support-centers', methods=['GET'])
def get_support_centers():
    """소상공인지원센터 정보 조회"""
    try:
        region = request.args.get('region')
        service_type = request.args.get('service_type')
        
        support_centers = support_tools_service.get_support_centers(region, service_type)
        
        return jsonify({
            "success": True,
            "data": support_centers
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        }), 500

@support_tools_bp.route('/expert-consultation', methods=['GET'])
def get_expert_consultation():
    """전문가 상담 예약 정보"""
    try:
        region = request.args.get('region')
        expertise = request.args.get('expertise')
        
        consultation_info = support_tools_service.get_expert_consultation(region, expertise)
        
        return jsonify({
            "success": True,
            "data": consultation_info
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        }), 500

@support_tools_bp.route('/policy-recommendations', methods=['POST'])
def get_policy_recommendations():
    """지역 기반 맞춤 창업 지원 정책 추천"""
    try:
        data = request.get_json() or {}
        
        if not data:
            return jsonify({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "사용자 프로필 정보가 필요합니다."
                }
            }), 400
        
        recommendations = support_tools_service.get_policy_recommendations(data)
        
        return jsonify({
            "success": True,
            "data": recommendations
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        }), 500

@support_tools_bp.route('/success-cases', methods=['GET'])
def get_success_cases_browse():
    """유사 상권 성공 사례 브라우징"""
    try:
        industry = request.args.get('industry')
        region = request.args.get('region')
        strategy_type = request.args.get('strategy_type')
        
        success_cases = support_tools_service.get_success_cases_browse(industry, region, strategy_type)
        
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

@support_tools_bp.route('/consultation-booking', methods=['POST'])
def book_consultation():
    """
    전문가 상담 예약
    
    전문가와의 상담을 예약합니다. 온라인/오프라인 상담이 가능합니다.
    
    ### 요청 본문
    ```json
    {
        "expert_id": "EXP001",
        "consultation_type": "온라인 상담",
        "preferred_date": "2024-01-15",
        "preferred_time": "오후",
        "user_info": {
            "name": "홍길동",
            "phone": "010-1234-5678",
            "email": "user@example.com",
            "business_type": "식음료업",
            "consultation_purpose": "창업 계획 수립"
        }
    }
    ```
    
    ### 필수 파라미터
    - **expert_id**: 전문가 ID
    - **consultation_type**: 상담 유형 (온라인 상담, 오프라인 상담)
    - **preferred_date**: 희망 날짜 (YYYY-MM-DD 형식)
    - **preferred_time**: 희망 시간대 (오전, 오후, 저녁)
    - **user_info**: 사용자 정보
    
    ### 응답 예시
    ```json
    {
        "success": true,
        "data": {
            "message": "상담 예약이 접수되었습니다.",
            "booking_info": {
                "booking_id": "BK20240101120000",
                "expert_id": "EXP001",
                "consultation_type": "온라인 상담",
                "preferred_date": "2024-01-15",
                "preferred_time": "오후",
                "status": "pending",
                "estimated_duration": "30분",
                "cost": "무료"
            },
            "next_steps": [
                "예약 확인을 위해 담당자가 연락드릴 예정입니다.",
                "상담 1일 전에 리마인더 메시지를 발송드립니다.",
                "상담 당일 준비사항을 안내드립니다."
            ]
        }
    }
    ```
    
    ### 상담 유형
    - **온라인 상담**: 화상회의를 통한 상담 (30분, 무료)
    - **오프라인 상담**: 대면 상담 (1시간, 무료)
    
    ### 시간대
    - **오전**: 09:00 - 12:00
    - **오후**: 13:00 - 17:00
    - **저녁**: 18:00 - 21:00
    
    ### 에러 코드
    - **400**: 필수 파라미터 누락
    - **500**: 서버 내부 오류
    """
    try:
        data = request.get_json() or {}
        
        required_fields = ['expert_id', 'consultation_type', 'preferred_date', 'preferred_time', 'user_info']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": f"{field}이 필요합니다."
                    }
                }), 400
        
        # 예약 정보 생성 (실제로는 데이터베이스에 저장)
        booking_info = {
            "booking_id": f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "expert_id": data['expert_id'],
            "consultation_type": data['consultation_type'],
            "preferred_date": data['preferred_date'],
            "preferred_time": data['preferred_time'],
            "user_info": data['user_info'],
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "estimated_duration": "30분" if data['consultation_type'] == "온라인 상담" else "1시간",
            "cost": "무료"
        }
        
        return jsonify({
            "success": True,
            "data": {
                "message": "상담 예약이 접수되었습니다.",
                "booking_info": booking_info,
                "next_steps": [
                    "예약 확인을 위해 담당자가 연락드릴 예정입니다.",
                    "상담 1일 전에 리마인더 메시지를 발송드립니다.",
                    "상담 당일 준비사항을 안내드립니다."
                ]
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

@support_tools_bp.route('/policy-application', methods=['POST'])
def apply_policy():
    """정책 신청"""
    try:
        data = request.get_json() or {}
        
        required_fields = ['policy_id', 'user_info', 'business_info', 'required_documents']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": f"{field}이 필요합니다."
                    }
                }), 400
        
        # 신청 정보 생성 (실제로는 데이터베이스에 저장)
        application_info = {
            "application_id": f"APP{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "policy_id": data['policy_id'],
            "user_info": data['user_info'],
            "business_info": data['business_info'],
            "required_documents": data['required_documents'],
            "status": "submitted",
            "submitted_at": datetime.now().isoformat(),
            "estimated_review_time": "14-30일",
            "contact_info": "042-123-4567"
        }
        
        return jsonify({
            "success": True,
            "data": {
                "message": "정책 신청이 접수되었습니다.",
                "application_info": application_info,
                "next_steps": [
                    "신청서 검토 및 보완 요청 (필요시)",
                    "심사 과정 진행",
                    "선정 결과 통보"
                ]
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

@support_tools_bp.route('/service-types', methods=['GET'])
def get_service_types():
    """지원 서비스 유형 목록"""
    try:
        service_types = [
            {
                "id": "창업상담",
                "name": "창업상담",
                "description": "창업 계획 수립 및 사업계획서 작성 지원",
                "target_users": ["ENTREPRENEUR"],
                "duration": "1-2시간",
                "cost": "무료"
            },
            {
                "id": "자금지원",
                "name": "자금지원",
                "description": "창업 자금 및 운영 자금 지원",
                "target_users": ["ENTREPRENEUR"],
                "duration": "신청 후 심사",
                "cost": "무료"
            },
            {
                "id": "교육프로그램",
                "name": "교육프로그램",
                "description": "창업 및 경영 관련 교육 프로그램",
                "target_users": ["ENTREPRENEUR", "INVESTOR"],
                "duration": "1-3개월",
                "cost": "무료"
            },
            {
                "id": "마케팅지원",
                "name": "마케팅지원",
                "description": "마케팅 전략 수립 및 홍보 지원",
                "target_users": ["ENTREPRENEUR"],
                "duration": "2-4개월",
                "cost": "무료"
            },
            {
                "id": "기술지원",
                "name": "기술지원",
                "description": "기술 개발 및 특허 지원",
                "target_users": ["ENTREPRENEUR"],
                "duration": "3-6개월",
                "cost": "무료"
            }
        ]
        
        return jsonify({
            "success": True,
            "data": {
                "total_service_types": len(service_types),
                "service_types": service_types
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

@support_tools_bp.route('/expertise-areas', methods=['GET'])
def get_expertise_areas():
    """전문 분야 목록"""
    try:
        expertise_areas = [
            {
                "id": "창업상담",
                "name": "창업상담",
                "description": "창업 계획 수립 및 사업계획서 작성",
                "expert_count": 5
            },
            {
                "id": "사업계획서작성",
                "name": "사업계획서작성",
                "description": "투자 유치를 위한 사업계획서 작성 지원",
                "expert_count": 3
            },
            {
                "id": "자금조달",
                "name": "자금조달",
                "description": "창업 자금 및 운영 자금 조달 방법 안내",
                "expert_count": 4
            },
            {
                "id": "마케팅전략",
                "name": "마케팅전략",
                "description": "마케팅 전략 수립 및 실행 방안",
                "expert_count": 6
            },
            {
                "id": "SNS마케팅",
                "name": "SNS마케팅",
                "description": "소셜미디어 마케팅 전략 및 실행",
                "expert_count": 4
            },
            {
                "id": "브랜딩",
                "name": "브랜딩",
                "description": "브랜드 아이덴티티 및 브랜딩 전략",
                "expert_count": 3
            },
            {
                "id": "기술창업",
                "name": "기술창업",
                "description": "기술 기반 창업 및 R&D 전략",
                "expert_count": 2
            },
            {
                "id": "특허상담",
                "name": "특허상담",
                "description": "특허 출원 및 지적재산권 보호",
                "expert_count": 2
            },
            {
                "id": "R&D지원",
                "name": "R&D지원",
                "description": "연구개발 프로젝트 기획 및 실행",
                "expert_count": 3
            }
        ]
        
        return jsonify({
            "success": True,
            "data": {
                "total_expertise_areas": len(expertise_areas),
                "expertise_areas": expertise_areas
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
