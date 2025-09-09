#!/usr/bin/env python3
"""
추천 알고리즘 서비스
사용자 프로필과 선호도를 기반으로 한 개인화된 추천
"""
from typing import Dict, List, Any, Optional
from services.data_loader import DataLoader
from services.scoring_service import ScoringService
import random
import math

class RecommendationService:
    def __init__(self):
        self.data_loader = DataLoader()
        self.scoring_service = ScoringService()
        
        # 업종별 특성 매트릭스
        self.industry_characteristics = {
            "식음료업": {
                "capital_requirement": "MEDIUM",
                "skill_level": "LOW",
                "seasonality": "MEDIUM",
                "competition": "HIGH",
                "growth_potential": "MEDIUM",
                "risk_level": "MEDIUM"
            },
            "쇼핑업": {
                "capital_requirement": "HIGH",
                "skill_level": "MEDIUM",
                "seasonality": "HIGH",
                "competition": "HIGH",
                "growth_potential": "LOW",
                "risk_level": "HIGH"
            },
            "숙박업": {
                "capital_requirement": "HIGH",
                "skill_level": "MEDIUM",
                "seasonality": "HIGH",
                "competition": "MEDIUM",
                "growth_potential": "MEDIUM",
                "risk_level": "MEDIUM"
            },
            "여가서비스업": {
                "capital_requirement": "MEDIUM",
                "skill_level": "MEDIUM",
                "seasonality": "MEDIUM",
                "competition": "MEDIUM",
                "growth_potential": "HIGH",
                "risk_level": "MEDIUM"
            },
            "운송업": {
                "capital_requirement": "HIGH",
                "skill_level": "LOW",
                "seasonality": "LOW",
                "competition": "MEDIUM",
                "growth_potential": "MEDIUM",
                "risk_level": "LOW"
            },
            "의료업": {
                "capital_requirement": "HIGH",
                "skill_level": "HIGH",
                "seasonality": "LOW",
                "competition": "LOW",
                "growth_potential": "HIGH",
                "risk_level": "LOW"
            },
            "교육업": {
                "capital_requirement": "MEDIUM",
                "skill_level": "HIGH",
                "seasonality": "MEDIUM",
                "competition": "MEDIUM",
                "growth_potential": "HIGH",
                "risk_level": "LOW"
            },
            "문화업": {
                "capital_requirement": "MEDIUM",
                "skill_level": "HIGH",
                "seasonality": "HIGH",
                "competition": "HIGH",
                "growth_potential": "MEDIUM",
                "risk_level": "HIGH"
            },
            "스포츠업": {
                "capital_requirement": "MEDIUM",
                "skill_level": "MEDIUM",
                "seasonality": "HIGH",
                "competition": "MEDIUM",
                "growth_potential": "HIGH",
                "risk_level": "MEDIUM"
            },
            "기타서비스업": {
                "capital_requirement": "LOW",
                "skill_level": "MEDIUM",
                "seasonality": "LOW",
                "competition": "MEDIUM",
                "growth_potential": "MEDIUM",
                "risk_level": "MEDIUM"
            }
        }
        
        # 지역별 특성 매트릭스
        self.region_characteristics = {
            "동구": {
                "development_level": "MEDIUM",
                "accessibility": "GOOD",
                "rent_cost": "MEDIUM",
                "population_density": "MEDIUM",
                "business_environment": "STABLE"
            },
            "서구": {
                "development_level": "HIGH",
                "accessibility": "EXCELLENT",
                "rent_cost": "HIGH",
                "population_density": "HIGH",
                "business_environment": "GROWING"
            },
            "유성구": {
                "development_level": "HIGH",
                "accessibility": "EXCELLENT",
                "rent_cost": "HIGH",
                "population_density": "MEDIUM",
                "business_environment": "GROWING"
            },
            "중구": {
                "development_level": "HIGH",
                "accessibility": "EXCELLENT",
                "rent_cost": "HIGH",
                "population_density": "HIGH",
                "business_environment": "STABLE"
            },
            "대덕구": {
                "development_level": "MEDIUM",
                "accessibility": "GOOD",
                "rent_cost": "LOW",
                "population_density": "LOW",
                "business_environment": "STABLE"
            }
        }
    
    def get_personalized_recommendations(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """개인화된 추천 생성"""
        try:
            # 사용자 프로필 분석
            user_preferences = self._analyze_user_profile(user_profile)
            
            # 업종 추천
            industry_recommendations = self._recommend_industries(user_preferences)
            
            # 지역 추천
            region_recommendations = self._recommend_regions(user_preferences)
            
            # 상권 추천
            market_recommendations = self._recommend_markets(user_preferences, industry_recommendations, region_recommendations)
            
            # 종합 추천
            comprehensive_recommendations = self._generate_comprehensive_recommendations(
                industry_recommendations, region_recommendations, market_recommendations
            )
            
            return {
                "user_profile_analysis": user_preferences,
                "industry_recommendations": industry_recommendations,
                "region_recommendations": region_recommendations,
                "market_recommendations": market_recommendations,
                "comprehensive_recommendations": comprehensive_recommendations,
                "next_steps": self._generate_next_steps(user_preferences)
            }
            
        except Exception as e:
            return {"error": f"추천 생성 중 오류가 발생했습니다: {str(e)}"}
    
    def _analyze_user_profile(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """사용자 프로필 분석"""
        user_type = user_profile.get("userType", "ENTREPRENEUR")
        business_stage = user_profile.get("businessStage", "PLANNING")
        interested_business_types = user_profile.get("preferences", {}).get("interestedBusinessTypes", [])
        preferred_areas = user_profile.get("preferences", {}).get("preferredAreas", [])
        
        # 사용자 특성 분석
        analysis = {
            "user_type": user_type,
            "business_stage": business_stage,
            "risk_tolerance": self._assess_risk_tolerance(user_type, business_stage),
            "capital_capacity": self._assess_capital_capacity(user_type, business_stage),
            "skill_level": self._assess_skill_level(user_type, business_stage),
            "preferred_industries": interested_business_types,
            "preferred_regions": preferred_areas,
            "business_goals": self._infer_business_goals(user_type, business_stage)
        }
        
        return analysis
    
    def _assess_risk_tolerance(self, user_type: str, business_stage: str) -> str:
        """리스크 허용도 평가"""
        if user_type == "BUSINESS_OWNER" and business_stage == "OPERATING":
            return "LOW"  # 기존 사업자, 안정성 중시
        elif business_stage == "PLANNING":
            return "MEDIUM"  # 신규 진입자, 적당한 리스크
        else:
            return "HIGH"  # 스타트업, 높은 리스크 허용
    
    def _assess_capital_capacity(self, user_type: str, business_stage: str) -> str:
        """자본 능력 평가"""
        if user_type == "BUSINESS_OWNER" and business_stage == "OPERATING":
            return "HIGH"  # 기존 사업자, 자본 여유
        elif business_stage == "STARTUP":
            return "MEDIUM"  # 스타트업, 중간 자본
        else:
            return "LOW"  # 계획 단계, 낮은 자본
    
    def _assess_skill_level(self, user_type: str, business_stage: str) -> str:
        """기술 수준 평가"""
        if user_type == "BUSINESS_OWNER" and business_stage == "OPERATING":
            return "HIGH"  # 기존 사업자, 높은 기술
        elif business_stage == "STARTUP":
            return "MEDIUM"  # 스타트업, 중간 기술
        else:
            return "LOW"  # 계획 단계, 낮은 기술
    
    def _infer_business_goals(self, user_type: str, business_stage: str) -> List[str]:
        """사업 목표 추론"""
        goals = []
        
        if business_stage == "PLANNING":
            goals.extend(["안정적인 수익 창출", "시장 진입", "브랜드 구축"])
        elif business_stage == "STARTUP":
            goals.extend(["성장", "시장 점유율 확대", "수익성 개선"])
        else:  # OPERATING
            goals.extend(["안정성 유지", "수익 최적화", "사업 확장"])
        
        if user_type == "BUSINESS_OWNER":
            goals.append("기존 사업과의 시너지")
        
        return goals
    
    def _recommend_industries(self, user_preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """업종 추천"""
        risk_tolerance = user_preferences["risk_tolerance"]
        capital_capacity = user_preferences["capital_capacity"]
        skill_level = user_preferences["skill_level"]
        preferred_industries = user_preferences["preferred_industries"]
        
        recommendations = []
        
        for industry, characteristics in self.industry_characteristics.items():
            # 매칭 점수 계산
            match_score = self._calculate_industry_match_score(
                characteristics, risk_tolerance, capital_capacity, skill_level
            )
            
            # 선호 업종 보너스
            if industry in preferred_industries:
                match_score += 20
            
            recommendations.append({
                "industry": industry,
                "match_score": round(match_score, 1),
                "characteristics": characteristics,
                "reasons": self._get_industry_recommendation_reasons(
                    characteristics, risk_tolerance, capital_capacity, skill_level
                )
            })
        
        # 점수 순으로 정렬
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        
        return recommendations[:5]  # 상위 5개 반환
    
    def _calculate_industry_match_score(self, characteristics: Dict[str, str], 
                                      risk_tolerance: str, capital_capacity: str, 
                                      skill_level: str) -> float:
        """업종 매칭 점수 계산"""
        score = 50  # 기본 점수
        
        # 리스크 매칭
        risk_level = characteristics["risk_level"]
        if (risk_tolerance == "LOW" and risk_level == "LOW") or \
           (risk_tolerance == "MEDIUM" and risk_level == "MEDIUM") or \
           (risk_tolerance == "HIGH" and risk_level == "HIGH"):
            score += 20
        elif (risk_tolerance == "LOW" and risk_level == "MEDIUM") or \
             (risk_tolerance == "HIGH" and risk_level == "MEDIUM"):
            score += 10
        
        # 자본 매칭
        capital_req = characteristics["capital_requirement"]
        if (capital_capacity == "LOW" and capital_req == "LOW") or \
           (capital_capacity == "MEDIUM" and capital_req == "MEDIUM") or \
           (capital_capacity == "HIGH" and capital_req == "HIGH"):
            score += 20
        elif (capital_capacity == "MEDIUM" and capital_req == "LOW") or \
             (capital_capacity == "HIGH" and capital_req == "MEDIUM"):
            score += 10
        
        # 기술 수준 매칭
        skill_req = characteristics["skill_level"]
        if (skill_level == "LOW" and skill_req == "LOW") or \
           (skill_level == "MEDIUM" and skill_req == "MEDIUM") or \
           (skill_level == "HIGH" and skill_req == "HIGH"):
            score += 20
        elif (skill_level == "MEDIUM" and skill_req == "LOW") or \
             (skill_level == "HIGH" and skill_req == "MEDIUM"):
            score += 10
        
        return min(100, score)
    
    def _get_industry_recommendation_reasons(self, characteristics: Dict[str, str], 
                                           risk_tolerance: str, capital_capacity: str, 
                                           skill_level: str) -> List[str]:
        """업종 추천 이유 생성"""
        reasons = []
        
        if characteristics["growth_potential"] == "HIGH":
            reasons.append("높은 성장 잠재력")
        
        if characteristics["risk_level"] == "LOW":
            reasons.append("낮은 사업 리스크")
        
        if characteristics["competition"] == "LOW":
            reasons.append("경쟁이 상대적으로 적음")
        
        if characteristics["capital_requirement"] == "LOW":
            reasons.append("낮은 초기 자본 요구")
        
        if characteristics["skill_level"] == "LOW":
            reasons.append("기술 진입 장벽이 낮음")
        
        return reasons
    
    def _recommend_regions(self, user_preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """지역 추천"""
        capital_capacity = user_preferences["capital_capacity"]
        preferred_regions = user_preferences["preferred_regions"]
        
        recommendations = []
        
        for region, characteristics in self.region_characteristics.items():
            # 매칭 점수 계산
            match_score = self._calculate_region_match_score(
                characteristics, capital_capacity
            )
            
            # 선호 지역 보너스
            if region in preferred_regions:
                match_score += 20
            
            recommendations.append({
                "region": region,
                "match_score": round(match_score, 1),
                "characteristics": characteristics,
                "reasons": self._get_region_recommendation_reasons(
                    characteristics, capital_capacity
                )
            })
        
        # 점수 순으로 정렬
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        
        return recommendations[:3]  # 상위 3개 반환
    
    def _calculate_region_match_score(self, characteristics: Dict[str, str], 
                                    capital_capacity: str) -> float:
        """지역 매칭 점수 계산"""
        score = 50  # 기본 점수
        
        # 임대료 매칭
        rent_cost = characteristics["rent_cost"]
        if (capital_capacity == "LOW" and rent_cost == "LOW") or \
           (capital_capacity == "MEDIUM" and rent_cost == "MEDIUM") or \
           (capital_capacity == "HIGH" and rent_cost == "HIGH"):
            score += 20
        elif (capital_capacity == "MEDIUM" and rent_cost == "LOW") or \
             (capital_capacity == "HIGH" and rent_cost == "MEDIUM"):
            score += 10
        
        # 접근성 보너스
        if characteristics["accessibility"] == "EXCELLENT":
            score += 15
        elif characteristics["accessibility"] == "GOOD":
            score += 10
        
        # 사업 환경 보너스
        if characteristics["business_environment"] == "GROWING":
            score += 15
        elif characteristics["business_environment"] == "STABLE":
            score += 10
        
        return min(100, score)
    
    def _get_region_recommendation_reasons(self, characteristics: Dict[str, str], 
                                         capital_capacity: str) -> List[str]:
        """지역 추천 이유 생성"""
        reasons = []
        
        if characteristics["accessibility"] == "EXCELLENT":
            reasons.append("우수한 접근성")
        
        if characteristics["business_environment"] == "GROWING":
            reasons.append("성장하는 사업 환경")
        
        if characteristics["development_level"] == "HIGH":
            reasons.append("높은 개발 수준")
        
        if characteristics["rent_cost"] == "LOW":
            reasons.append("낮은 임대료")
        
        return reasons
    
    def _recommend_markets(self, user_preferences: Dict[str, Any], 
                          industry_recommendations: List[Dict[str, Any]], 
                          region_recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """상권 추천"""
        recommendations = []
        
        # 상위 추천 업종과 지역 조합
        top_industries = [rec["industry"] for rec in industry_recommendations[:2]]
        top_regions = [rec["region"] for rec in region_recommendations[:2]]
        
        for industry in top_industries:
            for region in top_regions:
                # 임시 상권 코드 생성
                market_code = f"1000{len(recommendations)}"
                
                # 점수 계산
                score_result = self.scoring_service.calculate_market_score(
                    market_code, industry, region
                )
                
                if "error" not in score_result:
                    recommendations.append({
                        "market_code": market_code,
                        "market_name": f"{region} {industry} 상권",
                        "industry": industry,
                        "region": region,
                        "score": score_result["total_score"],
                        "grade": score_result["grade"],
                        "risk_level": score_result["risk_assessment"]["risk_level"]
                    })
        
        # 점수 순으로 정렬
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        
        return recommendations[:5]  # 상위 5개 반환
    
    def _generate_comprehensive_recommendations(self, industry_recommendations: List[Dict[str, Any]], 
                                              region_recommendations: List[Dict[str, Any]], 
                                              market_recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """종합 추천 생성"""
        comprehensive = []
        
        # 최적 조합 생성
        for i, industry_rec in enumerate(industry_recommendations[:3]):
            for j, region_rec in enumerate(region_recommendations[:3]):
                # 해당 조합의 상권 찾기
                matching_markets = [
                    market for market in market_recommendations
                    if market["industry"] == industry_rec["industry"] and 
                       market["region"] == region_rec["region"]
                ]
                
                if matching_markets:
                    best_market = matching_markets[0]
                    
                    # 종합 점수 계산
                    comprehensive_score = (
                        industry_rec["match_score"] * 0.4 +
                        region_rec["match_score"] * 0.3 +
                        best_market["score"] * 0.3
                    )
                    
                    comprehensive.append({
                        "rank": len(comprehensive) + 1,
                        "industry": industry_rec["industry"],
                        "region": region_rec["region"],
                        "market_code": best_market["market_code"],
                        "market_name": best_market["market_name"],
                        "comprehensive_score": round(comprehensive_score, 1),
                        "industry_score": industry_rec["match_score"],
                        "region_score": region_rec["match_score"],
                        "market_score": best_market["score"],
                        "grade": best_market["grade"],
                        "risk_level": best_market["risk_level"],
                        "recommendation_reasons": (
                            industry_rec["reasons"] + 
                            region_rec["reasons"] + 
                            [f"종합 점수 {best_market['score']}점"]
                        )
                    })
        
        # 종합 점수 순으로 정렬
        comprehensive.sort(key=lambda x: x["comprehensive_score"], reverse=True)
        
        return comprehensive[:3]  # 상위 3개 반환
    
    def _generate_next_steps(self, user_preferences: Dict[str, Any]) -> List[str]:
        """다음 단계 제안"""
        business_stage = user_preferences["business_stage"]
        
        if business_stage == "PLANNING":
            return [
                "1. 상세한 사업 계획서 작성",
                "2. 시장 조사 및 경쟁사 분석",
                "3. 자금 조달 계획 수립",
                "4. 입지 후보지 현장 조사",
                "5. 사업자 등록 및 허가 취득"
            ]
        elif business_stage == "STARTUP":
            return [
                "1. 사업 운영 최적화",
                "2. 고객 확보 전략 수립",
                "3. 마케팅 및 홍보 강화",
                "4. 재무 관리 체계 구축",
                "5. 성장 전략 수립"
            ]
        else:  # OPERATING
            return [
                "1. 기존 사업 성과 분석",
                "2. 확장 가능성 검토",
                "3. 새로운 시장 진출 검토",
                "4. 사업 다각화 방안 모색",
                "5. 장기 전략 수립"
            ]
