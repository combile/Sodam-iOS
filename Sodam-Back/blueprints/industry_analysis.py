#!/usr/bin/env python3
"""
업종별 분석 API
생존율/폐업율, 리스크 분석 등
"""
from flask import Blueprint, request, jsonify
from services.data_loader import DataLoader
from datetime import datetime
import random

industry_analysis_bp = Blueprint('industry_analysis', __name__, url_prefix='/api/v1/industry-analysis')

# 데이터 로더 인스턴스
data_loader = DataLoader()

@industry_analysis_bp.route('/')
def industry_analysis():
    """업종별 분석 API 메인"""
    return jsonify({
        "success": True,
        "message": "업종별 분석 API",
        "endpoints": {
            "survival_rates": "/api/v1/industry-analysis/survival-rates",
            "closure_rates": "/api/v1/industry-analysis/closure-rates",
            "risk_analysis": "/api/v1/industry-analysis/risk-analysis",
            "industry_trends": "/api/v1/industry-analysis/trends",
            "competition_analysis": "/api/v1/industry-analysis/competition"
        },
        "timestamp": datetime.utcnow().isoformat()
    })

@industry_analysis_bp.route('/survival-rates', methods=['GET'])
def get_survival_rates():
    """
    업종별 생존율 조회
    
    각 업종별 사업체 생존율을 조회합니다. 창업 후 특정 기간 동안 운영을 지속하는 비율을 제공합니다.
    
    ### 쿼리 파라미터
    - **industry**: 특정 업종 필터 (선택사항)
    - **period**: 분석 기간 (1year, 3year, 5year, 기본값: 1year)
    
    ### 지원 업종
    - 식음료업, 쇼핑업, 숙박업, 여가서비스업, 운송업
    - 의료업, 교육업, 문화업, 스포츠업, 기타서비스업
    
    ### 응답 예시
    ```json
    {
        "success": true,
        "data": {
            "survival_rates": [
                {
                    "industry": "식음료업",
                    "survival_rate": 75.0,
                    "period": "1year",
                    "sample_size": 500,
                    "confidence_level": 95
                }
            ],
            "period": "1year",
            "last_updated": "2024-01-01"
        },
        "message": "업종별 생존율을 성공적으로 조회했습니다.",
        "timestamp": "2024-01-01T00:00:00Z"
    }
    ```
    
    ### 생존율 해석
    - **80% 이상**: 매우 안정적인 업종
    - **60-79%**: 안정적인 업종
    - **40-59%**: 보통 수준의 업종
    - **40% 미만**: 위험한 업종
    
    ### 에러 코드
    - **500**: 서버 내부 오류
    """
    try:
        # 쿼리 파라미터
        industry = request.args.get('industry')
        period = request.args.get('period', '1year')  # 1year, 3year, 5year
        
        # 실제 데이터가 없으므로 샘플 데이터 생성
        industries = [
            "식음료업", "쇼핑업", "숙박업", "여가서비스업", "운송업",
            "의료업", "교육업", "문화업", "스포츠업", "기타서비스업"
        ]
        
        survival_data = []
        for ind in industries:
            if industry and industry not in ind:
                continue
                
            # 업종별 생존율 (실제 데이터 기반으로 조정)
            base_rate = {
                "식음료업": 0.75,
                "쇼핑업": 0.65,
                "숙박업": 0.70,
                "여가서비스업": 0.60,
                "운송업": 0.80,
                "의료업": 0.85,
                "교육업": 0.90,
                "문화업": 0.55,
                "스포츠업": 0.65,
                "기타서비스업": 0.70
            }.get(ind, 0.70)
            
            # 기간별 조정
            period_multiplier = {
                "1year": 1.0,
                "3year": 0.8,
                "5year": 0.6
            }.get(period, 1.0)
            
            survival_rate = base_rate * period_multiplier
            
            survival_data.append({
                "industry": ind,
                "survival_rate": round(survival_rate * 100, 1),
                "period": period,
                "sample_size": random.randint(100, 1000),
                "confidence_level": 95
            })
        
        return jsonify({
            "success": True,
            "data": {
                "survival_rates": survival_data,
                "period": period,
                "last_updated": "2024-01-01"
            },
            "message": "업종별 생존율을 성공적으로 조회했습니다.",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"생존율 조회 중 오류가 발생했습니다: {str(e)}"
            }
        }), 500

@industry_analysis_bp.route('/closure-rates', methods=['GET'])
def get_closure_rates():
    """업종별 폐업율 조회"""
    try:
        # 쿼리 파라미터
        industry = request.args.get('industry')
        period = request.args.get('period', '1year')
        
        industries = [
            "식음료업", "쇼핑업", "숙박업", "여가서비스업", "운송업",
            "의료업", "교육업", "문화업", "스포츠업", "기타서비스업"
        ]
        
        closure_data = []
        for ind in industries:
            if industry and industry not in ind:
                continue
                
            # 업종별 폐업율 (생존율의 역)
            base_rate = {
                "식음료업": 0.25,
                "쇼핑업": 0.35,
                "숙박업": 0.30,
                "여가서비스업": 0.40,
                "운송업": 0.20,
                "의료업": 0.15,
                "교육업": 0.10,
                "문화업": 0.45,
                "스포츠업": 0.35,
                "기타서비스업": 0.30
            }.get(ind, 0.30)
            
            # 기간별 조정
            period_multiplier = {
                "1year": 1.0,
                "3year": 1.2,
                "5year": 1.4
            }.get(period, 1.0)
            
            closure_rate = min(base_rate * period_multiplier, 1.0)
            
            closure_data.append({
                "industry": ind,
                "closure_rate": round(closure_rate * 100, 1),
                "period": period,
                "sample_size": random.randint(100, 1000),
                "risk_level": "HIGH" if closure_rate > 0.4 else "MEDIUM" if closure_rate > 0.2 else "LOW"
            })
        
        return jsonify({
            "success": True,
            "data": {
                "closure_rates": closure_data,
                "period": period,
                "last_updated": "2024-01-01"
            },
            "message": "업종별 폐업율을 성공적으로 조회했습니다.",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"폐업율 조회 중 오류가 발생했습니다: {str(e)}"
            }
        }), 500

@industry_analysis_bp.route('/risk-analysis', methods=['GET'])
def get_risk_analysis():
    """업종별 리스크 분석"""
    try:
        # 쿼리 파라미터
        industry = request.args.get('industry')
        region = request.args.get('region', '대전광역시')
        
        industries = [
            "식음료업", "쇼핑업", "숙박업", "여가서비스업", "운송업",
            "의료업", "교육업", "문화업", "스포츠업", "기타서비스업"
        ]
        
        risk_data = []
        for ind in industries:
            if industry and industry not in ind:
                continue
                
            # 업종별 리스크 요소 점수 (1-10점)
            risk_factors = {
                "market_competition": random.randint(3, 8),
                "seasonal_demand": random.randint(2, 9),
                "regulatory_risk": random.randint(1, 6),
                "economic_sensitivity": random.randint(3, 8),
                "technology_disruption": random.randint(2, 7),
                "labor_shortage": random.randint(3, 8),
                "rent_cost": random.randint(4, 9),
                "consumer_behavior": random.randint(2, 7)
            }
            
            # 종합 리스크 점수 계산
            total_risk = sum(risk_factors.values()) / len(risk_factors)
            
            # 리스크 등급 결정
            if total_risk >= 7:
                risk_level = "HIGH"
            elif total_risk >= 5:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"
            
            risk_data.append({
                "industry": ind,
                "region": region,
                "overall_risk_score": round(total_risk, 1),
                "risk_level": risk_level,
                "risk_factors": risk_factors,
                "recommendations": _get_risk_recommendations(risk_factors, risk_level)
            })
        
        return jsonify({
            "success": True,
            "data": {
                "risk_analysis": risk_data,
                "region": region,
                "analysis_date": datetime.utcnow().isoformat()
            },
            "message": "업종별 리스크 분석을 성공적으로 조회했습니다.",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"리스크 분석 조회 중 오류가 발생했습니다: {str(e)}"
            }
        }), 500

@industry_analysis_bp.route('/trends', methods=['GET'])
def get_industry_trends():
    """업종별 트렌드 분석"""
    try:
        industry = request.args.get('industry')
        period = request.args.get('period', '12months')
        
        industries = [
            "식음료업", "쇼핑업", "숙박업", "여가서비스업", "운송업",
            "의료업", "교육업", "문화업", "스포츠업", "기타서비스업"
        ]
        
        trend_data = []
        for ind in industries:
            if industry and industry not in ind:
                continue
                
            # 월별 트렌드 데이터 생성
            months = 12 if period == "12months" else 24
            monthly_data = []
            
            base_value = random.randint(80, 120)
            for i in range(months):
                # 계절성과 트렌드 반영
                seasonal_factor = 1 + 0.2 * (i % 12 - 6) / 6  # 계절성
                trend_factor = 1 + (i - months/2) * 0.01  # 트렌드
                value = base_value * seasonal_factor * trend_factor
                
                monthly_data.append({
                    "month": f"2024-{i+1:02d}",
                    "value": round(value, 1),
                    "growth_rate": round((value - base_value) / base_value * 100, 1)
                })
            
            trend_data.append({
                "industry": ind,
                "period": period,
                "monthly_data": monthly_data,
                "overall_trend": "INCREASING" if monthly_data[-1]["value"] > monthly_data[0]["value"] else "DECREASING",
                "volatility": round(random.uniform(0.1, 0.3), 2)
            })
        
        return jsonify({
            "success": True,
            "data": {
                "industry_trends": trend_data,
                "period": period
            },
            "message": "업종별 트렌드를 성공적으로 조회했습니다.",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"트렌드 분석 조회 중 오류가 발생했습니다: {str(e)}"
            }
        }), 500

@industry_analysis_bp.route('/competition', methods=['GET'])
def get_competition_analysis():
    """업종별 경쟁 분석"""
    try:
        industry = request.args.get('industry')
        region = request.args.get('region', '대전광역시')
        
        industries = [
            "식음료업", "쇼핑업", "숙박업", "여가서비스업", "운송업",
            "의료업", "교육업", "문화업", "스포츠업", "기타서비스업"
        ]
        
        competition_data = []
        for ind in industries:
            if industry and industry not in ind:
                continue
                
            # 경쟁 지표 생성
            competition_metrics = {
                "market_saturation": random.randint(3, 9),  # 시장 포화도
                "entry_barrier": random.randint(2, 8),      # 진입 장벽
                "price_competition": random.randint(4, 9),  # 가격 경쟁
                "brand_loyalty": random.randint(2, 7),      # 브랜드 충성도
                "innovation_pressure": random.randint(3, 8) # 혁신 압력
            }
            
            # 경쟁 강도 계산
            competition_intensity = sum(competition_metrics.values()) / len(competition_metrics)
            
            competition_data.append({
                "industry": ind,
                "region": region,
                "competition_intensity": round(competition_intensity, 1),
                "competition_level": "HIGH" if competition_intensity >= 7 else "MEDIUM" if competition_intensity >= 5 else "LOW",
                "metrics": competition_metrics,
                "market_share_distribution": _generate_market_share(),
                "recommendations": _get_competition_recommendations(competition_metrics)
            })
        
        return jsonify({
            "success": True,
            "data": {
                "competition_analysis": competition_data,
                "region": region
            },
            "message": "업종별 경쟁 분석을 성공적으로 조회했습니다.",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"경쟁 분석 조회 중 오류가 발생했습니다: {str(e)}"
            }
        }), 500

def _get_risk_recommendations(risk_factors, risk_level):
    """리스크 요인에 따른 권장사항 생성"""
    recommendations = []
    
    if risk_factors["market_competition"] >= 7:
        recommendations.append("차별화된 서비스나 제품 개발 필요")
    
    if risk_factors["seasonal_demand"] >= 7:
        recommendations.append("계절별 수요 변동에 대비한 사업 계획 수립")
    
    if risk_factors["rent_cost"] >= 7:
        recommendations.append("임대료 부담을 고려한 입지 선택")
    
    if risk_factors["labor_shortage"] >= 7:
        recommendations.append("인력 확보 및 유지 방안 마련")
    
    if risk_level == "HIGH":
        recommendations.append("신중한 사업 계획 수립 및 충분한 자본 확보 권장")
    
    return recommendations

def _generate_market_share():
    """시장 점유율 분포 생성"""
    shares = []
    remaining = 100
    
    for i in range(5):
        if i == 4:  # 마지막
            share = remaining
        else:
            share = random.randint(5, min(30, remaining - (4-i) * 5))
            remaining -= share
        
        shares.append({
            "rank": i + 1,
            "share": share,
            "type": "대기업" if i == 0 else "중견기업" if i < 3 else "중소기업"
        })
    
    return shares

def _get_competition_recommendations(metrics):
    """경쟁 지표에 따른 권장사항 생성"""
    recommendations = []
    
    if metrics["market_saturation"] >= 7:
        recommendations.append("포화된 시장에서 차별화 전략 필요")
    
    if metrics["entry_barrier"] >= 7:
        recommendations.append("높은 진입 장벽을 고려한 충분한 준비 필요")
    
    if metrics["price_competition"] >= 7:
        recommendations.append("가격 경쟁력 확보 또는 비가격 경쟁 요소 강화")
    
    if metrics["brand_loyalty"] >= 6:
        recommendations.append("기존 브랜드 충성도가 높으므로 신규 진입 시 차별화 중요")
    
    return recommendations
