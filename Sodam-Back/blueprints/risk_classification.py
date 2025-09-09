from flask import Blueprint, request, jsonify
from services.risk_analysis_service import RiskAnalysisService
from datetime import datetime
from typing import Dict, List, Any

risk_classification_bp = Blueprint('risk_classification', __name__, url_prefix='/api/v1/risk-classification')

risk_analysis_service = RiskAnalysisService()

@risk_classification_bp.route('/classify/<string:market_code>', methods=['POST'])
def classify_risk_type(market_code: str):
    """
    4가지 리스크 유형 자동 분류
    
    상권의 특성을 분석하여 4가지 리스크 유형 중 하나로 자동 분류합니다.
    
    ### 경로 파라미터
    - **market_code**: 상권 코드 (예: DJ001, DJ002)
    
    ### 요청 본문
    ```json
    {
        "industry": "식음료업"
    }
    ```
    
    ### 리스크 유형
    1. **유입 저조형**: 유동인구와 매출 증가율이 낮아 상권 활성화가 저조한 상태
    2. **과포화 경쟁형**: 동일업종 사업체가 과도하게 많아 경쟁이 치열한 상태
    3. **소비력 약형**: 지역 소비력이 부족하여 매출 창출이 어려운 상태
    4. **성장 잠재형**: 성장 잠재력이 제한적이어서 장기적 발전이 어려운 상태
    
    ### 응답 예시
    ```json
    {
        "success": true,
        "data": {
            "market_code": "DJ001",
            "industry": "식음료업",
            "risk_type": "과포화 경쟁형",
            "risk_score": 75.5,
            "health_score": 65.2,
            "confidence": 0.85,
            "analysis_data": {
                "competition_density": 8.5,
                "market_saturation": 7.2,
                "growth_potential": 4.1
            },
            "key_indicators": [
                "동일업종 과밀",
                "가격 경쟁 심화",
                "고객 분산"
            ]
        }
    }
    ```
    
    ### 에러 코드
    - **400**: 필수 파라미터 누락
    - **404**: 상권 데이터를 찾을 수 없음
    - **500**: 서버 내부 오류
    """
    try:
        data = request.get_json() or {}
        industry = data.get('industry')
        
        classification = risk_analysis_service.classify_risk_type(market_code, industry)
        
        return jsonify({
            "success": True,
            "data": classification
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        }), 500

@risk_classification_bp.route('/detailed-analysis/<string:market_code>', methods=['POST'])
def get_detailed_risk_analysis(market_code: str):
    """특정 리스크 유형의 상세 분석"""
    try:
        data = request.get_json() or {}
        risk_type = data.get('risk_type')
        industry = data.get('industry')
        
        if not risk_type:
            return jsonify({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "risk_type이 필요합니다."
                }
            }), 400
        
        analysis = risk_analysis_service.get_detailed_risk_analysis(market_code, risk_type, industry)
        
        if "error" in analysis:
            return jsonify({
                "success": False,
                "error": {
                    "code": "DATA_NOT_FOUND",
                    "message": analysis["error"]
                }
            }), 404
        
        return jsonify({
            "success": True,
            "data": analysis
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        }), 500

@risk_classification_bp.route('/risk-types', methods=['GET'])
def get_risk_types():
    """지원하는 리스크 유형 목록"""
    try:
        risk_types = [
            {
                "type": "유입 저조형",
                "description": "유동인구와 매출 증가율이 낮아 상권 활성화가 저조한 상태",
                "key_indicators": ["유동인구 감소", "매출 증가율 둔화", "접근성 부족"],
                "severity_levels": ["낮음", "보통", "높음", "매우 높음"]
            },
            {
                "type": "과포화 경쟁형",
                "description": "동일업종 사업체가 과도하게 많아 경쟁이 치열한 상태",
                "key_indicators": ["동일업종 과밀", "가격 경쟁 심화", "고객 분산"],
                "severity_levels": ["낮음", "보통", "높음", "매우 높음"]
            },
            {
                "type": "소비력 약형",
                "description": "지역 소비력이 부족하여 매출 창출이 어려운 상태",
                "key_indicators": ["지역 소득 수준 낮음", "소비 패턴 변화", "인구 감소"],
                "severity_levels": ["낮음", "보통", "높음", "매우 높음"]
            },
            {
                "type": "성장 잠재형",
                "description": "성장 잠재력이 제한적이어서 장기적 발전이 어려운 상태",
                "key_indicators": ["성장 동력 부족", "인프라 부족", "정책 지원 부족"],
                "severity_levels": ["낮음", "보통", "높음", "매우 높음"]
            }
        ]
        
        return jsonify({
            "success": True,
            "data": {
                "total_risk_types": len(risk_types),
                "risk_types": risk_types
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

@risk_classification_bp.route('/mitigation-strategies', methods=['GET'])
def get_mitigation_strategies():
    """리스크 완화 전략 목록"""
    try:
        risk_type = request.args.get('risk_type')
        
        strategies = {
            "유입 저조형": [
                {
                    "strategy": "마케팅 강화",
                    "description": "유동인구 증가를 위한 마케팅 전략 수립",
                    "effectiveness": "높음",
                    "cost": "중간",
                    "duration": "2-3개월"
                },
                {
                    "strategy": "이벤트 개최",
                    "description": "상권 활성화를 위한 이벤트 및 프로모션",
                    "effectiveness": "중간",
                    "cost": "낮음",
                    "duration": "1-2개월"
                },
                {
                    "strategy": "접근성 개선",
                    "description": "교통편 확충 및 주차 시설 개선",
                    "effectiveness": "높음",
                    "cost": "높음",
                    "duration": "6-12개월"
                }
            ],
            "과포화 경쟁형": [
                {
                    "strategy": "차별화 전략",
                    "description": "경쟁 우위 확보를 위한 차별화된 상품/서비스 개발",
                    "effectiveness": "높음",
                    "cost": "높음",
                    "duration": "3-6개월"
                },
                {
                    "strategy": "고객 충성도 향상",
                    "description": "고객 충성도 향상 프로그램 도입",
                    "effectiveness": "중간",
                    "cost": "중간",
                    "duration": "2-4개월"
                },
                {
                    "strategy": "가격 경쟁력 강화",
                    "description": "가치 기반 마케팅을 통한 가격 경쟁 회피",
                    "effectiveness": "중간",
                    "cost": "낮음",
                    "duration": "1-2개월"
                }
            ],
            "소비력 약형": [
                {
                    "strategy": "가격 최적화",
                    "description": "소득 수준에 맞는 가격 정책 수립",
                    "effectiveness": "높음",
                    "cost": "낮음",
                    "duration": "1-2개월"
                },
                {
                    "strategy": "온라인 확장",
                    "description": "온라인 판매 채널 구축 및 확대",
                    "effectiveness": "높음",
                    "cost": "중간",
                    "duration": "3-4개월"
                },
                {
                    "strategy": "외부 고객 유치",
                    "description": "관광 상품 개발 및 외부 고객 유치",
                    "effectiveness": "중간",
                    "cost": "높음",
                    "duration": "6-12개월"
                }
            ],
            "성장 잠재형": [
                {
                    "strategy": "혁신 모델 도입",
                    "description": "혁신적 비즈니스 모델 도입 및 신규 수요 창출",
                    "effectiveness": "높음",
                    "cost": "매우 높음",
                    "duration": "6-12개월"
                },
                {
                    "strategy": "지역 상생 참여",
                    "description": "지역 발전 계획 참여 및 상생 프로그램 참여",
                    "effectiveness": "중간",
                    "cost": "중간",
                    "duration": "3-6개월"
                },
                {
                    "strategy": "인프라 개선 요구",
                    "description": "지역 인프라 개선을 위한 정책 제안 및 참여",
                    "effectiveness": "낮음",
                    "cost": "낮음",
                    "duration": "12개월 이상"
                }
            ]
        }
        
        if risk_type and risk_type in strategies:
            return jsonify({
                "success": True,
                "data": {
                    "risk_type": risk_type,
                    "strategies": strategies[risk_type]
                }
            })
        else:
            return jsonify({
                "success": True,
                "data": {
                    "all_strategies": strategies
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
