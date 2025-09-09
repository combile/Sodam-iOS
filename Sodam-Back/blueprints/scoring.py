#!/usr/bin/env python3
"""
종합 점수 계산 API
상권, 업종, 지역 데이터를 종합하여 점수 계산
"""
from flask import Blueprint, request, jsonify
from services.scoring_service import ScoringService
from datetime import datetime

scoring_bp = Blueprint('scoring', __name__, url_prefix='/api/v1/scoring')

# 점수 계산 서비스 인스턴스
scoring_service = ScoringService()

@scoring_bp.route('/')
def scoring():
    """종합 점수 계산 API 메인"""
    return jsonify({
        "success": True,
        "message": "종합 점수 계산 API",
        "endpoints": {
            "calculate_score": "/api/v1/scoring/calculate",
            "compare_locations": "/api/v1/scoring/compare",
            "get_recommendations": "/api/v1/scoring/recommendations"
        },
        "timestamp": datetime.utcnow().isoformat()
    })

@scoring_bp.route('/calculate', methods=['POST'])
def calculate_score():
    """종합 점수 계산"""
    try:
        data = request.get_json() or {}
        
        # 필수 파라미터 검증
        market_code = data.get('market_code')
        industry = data.get('industry')
        region = data.get('region')
        
        if not all([market_code, industry, region]):
            return jsonify({
                "success": False,
                "error": {
                    "code": "MISSING_PARAMETERS",
                    "message": "market_code, industry, region 파라미터가 필요합니다."
                }
            }), 400
        
        # 점수 계산
        result = scoring_service.calculate_market_score(market_code, industry, region)
        
        if "error" in result:
            return jsonify({
                "success": False,
                "error": {
                    "code": "CALCULATION_ERROR",
                    "message": result["error"]
                }
            }), 500
        
        return jsonify({
            "success": True,
            "data": {
                "market_code": market_code,
                "industry": industry,
                "region": region,
                "score_analysis": result
            },
            "message": "종합 점수를 성공적으로 계산했습니다.",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"점수 계산 중 오류가 발생했습니다: {str(e)}"
            }
        }), 500

@scoring_bp.route('/compare', methods=['POST'])
def compare_locations():
    """여러 지역 비교 분석"""
    try:
        data = request.get_json() or {}
        
        # 필수 파라미터 검증
        industry = data.get('industry')
        regions = data.get('regions', [])
        
        if not industry or not regions:
            return jsonify({
                "success": False,
                "error": {
                    "code": "MISSING_PARAMETERS",
                    "message": "industry와 regions 파라미터가 필요합니다."
                }
            }), 400
        
        if len(regions) < 2:
            return jsonify({
                "success": False,
                "error": {
                    "code": "INSUFFICIENT_DATA",
                    "message": "비교를 위해 최소 2개 이상의 지역이 필요합니다."
                }
            }), 400
        
        # 각 지역별 점수 계산
        comparison_results = []
        for region in regions:
            # 각 지역의 대표 상권 코드 사용 (실제로는 더 정교한 로직 필요)
            market_code = f"1000{len(comparison_results)}"  # 임시 상권 코드
            
            result = scoring_service.calculate_market_score(market_code, industry, region)
            
            if "error" not in result:
                comparison_results.append({
                    "region": region,
                    "market_code": market_code,
                    "score_analysis": result
                })
        
        # 점수 순으로 정렬
        comparison_results.sort(key=lambda x: x["score_analysis"]["total_score"], reverse=True)
        
        # 순위 추가
        for i, result in enumerate(comparison_results):
            result["rank"] = i + 1
        
        return jsonify({
            "success": True,
            "data": {
                "industry": industry,
                "comparison_results": comparison_results,
                "best_location": comparison_results[0] if comparison_results else None,
                "summary": {
                    "total_regions": len(comparison_results),
                    "average_score": round(sum(r["score_analysis"]["total_score"] for r in comparison_results) / len(comparison_results), 1) if comparison_results else 0,
                    "score_range": {
                        "highest": comparison_results[0]["score_analysis"]["total_score"] if comparison_results else 0,
                        "lowest": comparison_results[-1]["score_analysis"]["total_score"] if comparison_results else 0
                    }
                }
            },
            "message": "지역 비교 분석을 성공적으로 완료했습니다.",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"지역 비교 분석 중 오류가 발생했습니다: {str(e)}"
            }
        }), 500

@scoring_bp.route('/recommendations', methods=['POST'])
def get_recommendations():
    """점수 기반 맞춤형 권장사항"""
    try:
        data = request.get_json() or {}
        
        # 필수 파라미터 검증
        market_code = data.get('market_code')
        industry = data.get('industry')
        region = data.get('region')
        
        if not all([market_code, industry, region]):
            return jsonify({
                "success": False,
                "error": {
                    "code": "MISSING_PARAMETERS",
                    "message": "market_code, industry, region 파라미터가 필요합니다."
                }
            }), 400
        
        # 점수 계산
        result = scoring_service.calculate_market_score(market_code, industry, region)
        
        if "error" in result:
            return jsonify({
                "success": False,
                "error": {
                    "code": "CALCULATION_ERROR",
                    "message": result["error"]
                }
            }), 500
        
        # 맞춤형 권장사항 생성
        recommendations = _generate_detailed_recommendations(result, industry, region)
        
        return jsonify({
            "success": True,
            "data": {
                "market_code": market_code,
                "industry": industry,
                "region": region,
                "score": result["total_score"],
                "grade": result["grade"],
                "recommendations": recommendations,
                "risk_assessment": result["risk_assessment"]
            },
            "message": "맞춤형 권장사항을 성공적으로 생성했습니다.",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"권장사항 생성 중 오류가 발생했습니다: {str(e)}"
            }
        }), 500

def _generate_detailed_recommendations(score_result: dict, industry: str, region: str) -> dict:
    """상세한 맞춤형 권장사항 생성"""
    total_score = score_result["total_score"]
    market_score = score_result["market_score"]
    industry_score = score_result["industry_score"]
    regional_score = score_result["regional_score"]
    
    recommendations = {
        "overall": [],
        "market_specific": [],
        "industry_specific": [],
        "regional_specific": [],
        "action_plan": []
    }
    
    # 전체 점수 기반 권장사항
    if total_score >= 80:
        recommendations["overall"].append("매우 우수한 사업 환경입니다. 적극적인 투자를 고려하세요.")
        recommendations["overall"].append("시장 진입 시점을 신중히 선택하여 최대 효과를 거두세요.")
    elif total_score >= 60:
        recommendations["overall"].append("양호한 사업 환경입니다. 신중한 계획으로 성공 가능성이 높습니다.")
        recommendations["overall"].append("차별화된 전략으로 경쟁 우위를 확보하세요.")
    else:
        recommendations["overall"].append("신중한 검토가 필요한 환경입니다.")
        recommendations["overall"].append("대안 지역이나 업종을 함께 고려해보세요.")
    
    # 상권 특화 권장사항
    if market_score["competition_level"] < 60:
        recommendations["market_specific"].append("경쟁이 치열한 지역입니다. 차별화된 서비스나 제품 개발이 필수입니다.")
    
    if market_score["rent_cost"] < 60:
        recommendations["market_specific"].append("임대료가 높은 지역입니다. 비용 효율적인 운영 방안을 마련하세요.")
    
    if market_score["accessibility"] < 60:
        recommendations["market_specific"].append("접근성이 떨어집니다. 온라인 마케팅이나 배달 서비스를 고려하세요.")
    
    # 업종 특화 권장사항
    if industry_score["risk_level"] < 60:
        recommendations["industry_specific"].append(f"{industry} 업종의 리스크가 높습니다. 충분한 자본 확보가 필요합니다.")
    
    if industry_score["competition_intensity"] < 60:
        recommendations["industry_specific"].append(f"{industry} 업종 내 경쟁이 치열합니다. 독창적인 비즈니스 모델을 개발하세요.")
    
    # 지역 특화 권장사항
    if regional_score["economic_indicators"] < 60:
        recommendations["regional_specific"].append(f"{region}의 경제 상황을 고려하여 보수적인 사업 계획을 수립하세요.")
    
    # 실행 계획
    if total_score >= 70:
        recommendations["action_plan"].extend([
            "1단계: 상세한 사업 계획서 작성",
            "2단계: 자금 조달 계획 수립",
            "3단계: 입지 선정 및 계약",
            "4단계: 인력 채용 및 교육",
            "5단계: 마케팅 전략 수립 및 실행"
        ])
    else:
        recommendations["action_plan"].extend([
            "1단계: 대안 지역 및 업종 검토",
            "2단계: 리스크 요인 상세 분석",
            "3단계: 보완 방안 모색",
            "4단계: 재검토 후 결정"
        ])
    
    return recommendations
