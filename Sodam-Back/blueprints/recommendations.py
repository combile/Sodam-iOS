#!/usr/bin/env python3
"""
추천 알고리즘 API
개인화된 추천 서비스
"""
from flask import Blueprint, request, jsonify
from services.recommendation_service import RecommendationService
from datetime import datetime
from typing import Dict, List, Any

recommendations_bp = Blueprint('recommendations', __name__, url_prefix='/api/v1/recommendations')

# 추천 서비스 인스턴스
recommendation_service = RecommendationService()

@recommendations_bp.route('/')
def recommendations():
    """추천 알고리즘 API 메인"""
    return jsonify({
        "success": True,
        "message": "추천 알고리즘 API",
        "endpoints": {
            "personalized": "/api/v1/recommendations/personalized",
            "industry_based": "/api/v1/recommendations/industry-based",
            "region_based": "/api/v1/recommendations/region-based",
            "similar_users": "/api/v1/recommendations/similar-users"
        },
        "timestamp": datetime.utcnow().isoformat()
    })

@recommendations_bp.route('/personalized', methods=['POST'])
def get_personalized_recommendations():
    """개인화된 추천"""
    try:
        data = request.get_json() or {}
        
        # 사용자 프로필 검증
        user_profile = data.get('user_profile', {})
        
        if not user_profile:
            return jsonify({
                "success": False,
                "error": {
                    "code": "MISSING_PARAMETERS",
                    "message": "user_profile 파라미터가 필요합니다."
                }
            }), 400
        
        # 개인화된 추천 생성
        result = recommendation_service.get_personalized_recommendations(user_profile)
        
        if "error" in result:
            return jsonify({
                "success": False,
                "error": {
                    "code": "RECOMMENDATION_ERROR",
                    "message": result["error"]
                }
            }), 500
        
        return jsonify({
            "success": True,
            "data": {
                "recommendations": result,
                "generated_at": datetime.utcnow().isoformat()
            },
            "message": "개인화된 추천을 성공적으로 생성했습니다.",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"추천 생성 중 오류가 발생했습니다: {str(e)}"
            }
        }), 500

@recommendations_bp.route('/industry-based', methods=['POST'])
def get_industry_based_recommendations():
    """업종 기반 추천"""
    try:
        data = request.get_json() or {}
        
        # 파라미터 검증
        industry = data.get('industry')
        user_type = data.get('user_type', 'ENTREPRENEUR')
        business_stage = data.get('business_stage', 'PLANNING')
        
        if not industry:
            return jsonify({
                "success": False,
                "error": {
                    "code": "MISSING_PARAMETERS",
                    "message": "industry 파라미터가 필요합니다."
                }
            }), 400
        
        # 업종 기반 추천 생성
        user_profile = {
            "userType": user_type,
            "businessStage": business_stage,
            "preferences": {
                "interestedBusinessTypes": [industry]
            }
        }
        
        result = recommendation_service.get_personalized_recommendations(user_profile)
        
        if "error" in result:
            return jsonify({
                "success": False,
                "error": {
                    "code": "RECOMMENDATION_ERROR",
                    "message": result["error"]
                }
            }), 500
        
        # 업종 관련 정보만 추출
        industry_info = {
            "target_industry": industry,
            "industry_recommendations": result["industry_recommendations"],
            "region_recommendations": result["region_recommendations"],
            "market_recommendations": [
                market for market in result["market_recommendations"]
                if market["industry"] == industry
            ],
            "comprehensive_recommendations": [
                comp for comp in result["comprehensive_recommendations"]
                if comp["industry"] == industry
            ]
        }
        
        return jsonify({
            "success": True,
            "data": {
                "industry_based_recommendations": industry_info,
                "generated_at": datetime.utcnow().isoformat()
            },
            "message": f"{industry} 업종 기반 추천을 성공적으로 생성했습니다.",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"업종 기반 추천 생성 중 오류가 발생했습니다: {str(e)}"
            }
        }), 500

@recommendations_bp.route('/region-based', methods=['POST'])
def get_region_based_recommendations():
    """지역 기반 추천"""
    try:
        data = request.get_json() or {}
        
        # 파라미터 검증
        region = data.get('region')
        user_type = data.get('user_type', 'ENTREPRENEUR')
        business_stage = data.get('business_stage', 'PLANNING')
        
        if not region:
            return jsonify({
                "success": False,
                "error": {
                    "code": "MISSING_PARAMETERS",
                    "message": "region 파라미터가 필요합니다."
                }
            }), 400
        
        # 지역 기반 추천 생성
        user_profile = {
            "userType": user_type,
            "businessStage": business_stage,
            "preferences": {
                "preferredAreas": [region]
            }
        }
        
        result = recommendation_service.get_personalized_recommendations(user_profile)
        
        if "error" in result:
            return jsonify({
                "success": False,
                "error": {
                    "code": "RECOMMENDATION_ERROR",
                    "message": result["error"]
                }
            }), 500
        
        # 지역 관련 정보만 추출
        region_info = {
            "target_region": region,
            "industry_recommendations": result["industry_recommendations"],
            "region_recommendations": result["region_recommendations"],
            "market_recommendations": [
                market for market in result["market_recommendations"]
                if market["region"] == region
            ],
            "comprehensive_recommendations": [
                comp for comp in result["comprehensive_recommendations"]
                if comp["region"] == region
            ]
        }
        
        return jsonify({
            "success": True,
            "data": {
                "region_based_recommendations": region_info,
                "generated_at": datetime.utcnow().isoformat()
            },
            "message": f"{region} 지역 기반 추천을 성공적으로 생성했습니다.",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"지역 기반 추천 생성 중 오류가 발생했습니다: {str(e)}"
            }
        }), 500

@recommendations_bp.route('/similar-users', methods=['POST'])
def get_similar_users_recommendations():
    """유사 사용자 기반 추천"""
    try:
        data = request.get_json() or {}
        
        # 파라미터 검증
        user_profile = data.get('user_profile', {})
        
        if not user_profile:
            return jsonify({
                "success": False,
                "error": {
                    "code": "MISSING_PARAMETERS",
                    "message": "user_profile 파라미터가 필요합니다."
                }
            }), 400
        
        # 유사 사용자 시뮬레이션 (실제로는 데이터베이스에서 유사 사용자 찾기)
        similar_users = _find_similar_users(user_profile)
        
        # 유사 사용자들의 성공 사례 기반 추천
        similar_recommendations = []
        for similar_user in similar_users:
            user_result = recommendation_service.get_personalized_recommendations(similar_user["profile"])
            
            if "error" not in user_result:
                similar_recommendations.append({
                    "similarity_score": similar_user["similarity_score"],
                    "user_type": similar_user["profile"]["userType"],
                    "business_stage": similar_user["profile"]["businessStage"],
                    "success_story": similar_user["success_story"],
                    "recommendations": user_result["comprehensive_recommendations"][:2]  # 상위 2개만
                })
        
        return jsonify({
            "success": True,
            "data": {
                "similar_users_recommendations": similar_recommendations,
                "generated_at": datetime.utcnow().isoformat()
            },
            "message": "유사 사용자 기반 추천을 성공적으로 생성했습니다.",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"유사 사용자 기반 추천 생성 중 오류가 발생했습니다: {str(e)}"
            }
        }), 500

def _find_similar_users(user_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    """유사 사용자 찾기 (시뮬레이션)"""
    # 실제로는 데이터베이스에서 유사한 프로필의 사용자들을 찾아야 함
    similar_users = [
        {
            "similarity_score": 0.85,
            "profile": {
                "userType": user_profile.get("userType", "ENTREPRENEUR"),
                "businessStage": user_profile.get("businessStage", "PLANNING"),
                "preferences": {
                    "interestedBusinessTypes": ["식음료업", "쇼핑업"],
                    "preferredAreas": ["유성구", "서구"]
                }
            },
            "success_story": {
                "industry": "식음료업",
                "region": "유성구",
                "business_name": "카페 드림",
                "success_factors": ["차별화된 메뉴", "고객 서비스", "위치 선정"],
                "revenue": "월 500만원",
                "period": "6개월"
            }
        },
        {
            "similarity_score": 0.78,
            "profile": {
                "userType": user_profile.get("userType", "ENTREPRENEUR"),
                "businessStage": "STARTUP",
                "preferences": {
                    "interestedBusinessTypes": ["여가서비스업"],
                    "preferredAreas": ["서구"]
                }
            },
            "success_story": {
                "industry": "여가서비스업",
                "region": "서구",
                "business_name": "헬스클럽 피트니스",
                "success_factors": ["전문성", "고객 관리", "마케팅"],
                "revenue": "월 800만원",
                "period": "1년"
            }
        },
        {
            "similarity_score": 0.72,
            "profile": {
                "userType": "BUSINESS_OWNER",
                "businessStage": "OPERATING",
                "preferences": {
                    "interestedBusinessTypes": ["운송업"],
                    "preferredAreas": ["대덕구"]
                }
            },
            "success_story": {
                "industry": "운송업",
                "region": "대덕구",
                "business_name": "대덕택시",
                "success_factors": ["서비스 품질", "고객 만족도", "운영 효율성"],
                "revenue": "월 1200만원",
                "period": "2년"
            }
        }
    ]
    
    return similar_users
