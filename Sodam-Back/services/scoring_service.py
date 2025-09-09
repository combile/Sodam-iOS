#!/usr/bin/env python3
"""
종합 점수 계산 서비스
상권, 업종, 지역 데이터를 종합하여 점수 계산
"""
from typing import Dict, List, Any, Optional
from services.data_loader import DataLoader
import math

class ScoringService:
    def __init__(self):
        self.data_loader = DataLoader()
        
        # 가중치 설정
        self.weights = {
            "market_factors": {
                "population_density": 0.25,
                "competition_level": 0.20,
                "accessibility": 0.15,
                "rent_cost": 0.20,
                "foot_traffic": 0.20
            },
            "industry_factors": {
                "survival_rate": 0.30,
                "growth_potential": 0.25,
                "risk_level": 0.25,
                "competition_intensity": 0.20
            },
            "regional_factors": {
                "economic_indicators": 0.40,
                "demographics": 0.30,
                "infrastructure": 0.30
            }
        }
    
    def calculate_market_score(self, market_code: str, industry: str, region: str) -> Dict[str, Any]:
        """상권 종합 점수 계산"""
        try:
            # 기본 데이터 수집
            market_data = self._get_market_data(market_code)
            industry_data = self._get_industry_data(industry)
            regional_data = self._get_regional_data(region)
            
            if not all([market_data, industry_data, regional_data]):
                return {"error": "필요한 데이터를 찾을 수 없습니다."}
            
            # 각 요소별 점수 계산
            market_score = self._calculate_market_factors_score(market_data, regional_data)
            industry_score = self._calculate_industry_factors_score(industry_data)
            regional_score = self._calculate_regional_factors_score(regional_data)
            
            # 종합 점수 계산
            total_score = (
                market_score["total"] * 0.4 +
                industry_score["total"] * 0.35 +
                regional_score["total"] * 0.25
            )
            
            # 등급 결정
            grade = self._determine_grade(total_score)
            
            return {
                "total_score": round(total_score, 1),
                "grade": grade,
                "market_score": market_score,
                "industry_score": industry_score,
                "regional_score": regional_score,
                "recommendations": self._generate_recommendations(market_score, industry_score, regional_score),
                "risk_assessment": self._assess_risk(market_score, industry_score, regional_score)
            }
            
        except Exception as e:
            return {"error": f"점수 계산 중 오류가 발생했습니다: {str(e)}"}
    
    def _get_market_data(self, market_code: str) -> Optional[Dict[str, Any]]:
        """상권 데이터 조회"""
        market_data = self.data_loader.get_market_by_code(market_code)
        if not market_data:
            # 데이터가 없을 경우 기본값 반환
            return {
                "market_code": market_code,
                "market_name": "샘플 상권",
                "city_name": "대전광역시",
                "district_name": "유성구",
                "market_type": "주요상권",
                "coordinates": []
            }
        return market_data
    
    def _get_industry_data(self, industry: str) -> Dict[str, Any]:
        """업종 데이터 조회 - 실제 데이터 기반"""
        # 실제 업종별 지출 비율 데이터 사용
        industry_ratio = self.data_loader.get_industry_ratio_by_category(industry)
        major_ratio = industry_ratio.get('major_ratio', 0.0)
        
        # 업종별 특성 (실제 데이터 기반으로 조정)
        industry_characteristics = {
            "쇼핑업": {
                "survival_rate": 65.0,
                "growth_potential": 0.5,
                "risk_level": 0.5,
                "competition_intensity": 0.8
            },
            "숙박업": {
                "survival_rate": 70.0,
                "growth_potential": 0.6,
                "risk_level": 0.4,
                "competition_intensity": 0.6
            },
            "식음료업": {
                "survival_rate": 75.0,
                "growth_potential": 0.7,
                "risk_level": 0.3,
                "competition_intensity": 0.7
            },
            "여가서비스업": {
                "survival_rate": 60.0,
                "growth_potential": 0.8,
                "risk_level": 0.6,
                "competition_intensity": 0.5
            },
            "여행업": {
                "survival_rate": 55.0,
                "growth_potential": 0.9,
                "risk_level": 0.7,
                "competition_intensity": 0.6
            },
            "운송업": {
                "survival_rate": 80.0,
                "growth_potential": 0.4,
                "risk_level": 0.2,
                "competition_intensity": 0.4
            }
        }
        
        base_data = industry_characteristics.get(industry, {
            "survival_rate": 70.0,
            "growth_potential": 0.6,
            "risk_level": 0.4,
            "competition_intensity": 0.5
        })
        
        # 실제 지출 비율을 반영한 조정
        ratio_adjustment = major_ratio / 100.0 if major_ratio > 0 else 1.0
        
        return {
            "survival_rate": base_data["survival_rate"] * ratio_adjustment,
            "growth_potential": base_data["growth_potential"] * ratio_adjustment,
            "risk_level": base_data["risk_level"] / ratio_adjustment if ratio_adjustment > 0 else base_data["risk_level"],
            "competition_intensity": base_data["competition_intensity"] * ratio_adjustment
        }
    
    def _get_regional_data(self, region: str) -> Dict[str, Any]:
        """지역 데이터 조회 - 실제 데이터 기반"""
        # 실제 지역별 지출 비율 데이터 사용
        regional_ratio = self.data_loader.get_regional_ratio_by_region(region)
        
        # 지역별 기본 특성 (실제 데이터 기반으로 조정)
        regional_characteristics = {
            "대전광역시": {
                "population_density": 2500,
                "economic_growth": 2.0,
                "unemployment_rate": 3.0,
                "average_income": 3000000,
                "infrastructure_score": 0.7
            },
            "서울특별시": {
                "population_density": 8000,
                "economic_growth": 2.5,
                "unemployment_rate": 2.5,
                "average_income": 4500000,
                "infrastructure_score": 0.9
            },
            "부산광역시": {
                "population_density": 4000,
                "economic_growth": 2.2,
                "unemployment_rate": 2.8,
                "average_income": 3500000,
                "infrastructure_score": 0.8
            },
            "인천광역시": {
                "population_density": 3000,
                "economic_growth": 2.3,
                "unemployment_rate": 2.7,
                "average_income": 3200000,
                "infrastructure_score": 0.8
            },
            "광주광역시": {
                "population_density": 2000,
                "economic_growth": 1.8,
                "unemployment_rate": 3.2,
                "average_income": 2800000,
                "infrastructure_score": 0.7
            },
            "대구광역시": {
                "population_density": 3500,
                "economic_growth": 2.0,
                "unemployment_rate": 3.0,
                "average_income": 3000000,
                "infrastructure_score": 0.8
            }
        }
        
        base_data = regional_characteristics.get(region, {
            "population_density": 2500,
            "economic_growth": 2.0,
            "unemployment_rate": 3.0,
            "average_income": 3000000,
            "infrastructure_score": 0.7
        })
        
        # 실제 지출 비율을 반영한 조정
        ratio_adjustment = regional_ratio / 100.0 if regional_ratio > 0 else 1.0
        
        return {
            "population_density": base_data["population_density"] * ratio_adjustment,
            "economic_growth": base_data["economic_growth"] * ratio_adjustment,
            "unemployment_rate": base_data["unemployment_rate"] / ratio_adjustment if ratio_adjustment > 0 else base_data["unemployment_rate"],
            "average_income": base_data["average_income"] * ratio_adjustment,
            "infrastructure_score": base_data["infrastructure_score"] * ratio_adjustment
        }
    
    def _calculate_market_factors_score(self, market_data: Dict[str, Any], regional_data: Dict[str, Any]) -> Dict[str, Any]:
        """상권 요인 점수 계산"""
        # 인구 밀도 점수 (0-100)
        population_density = regional_data.get("population_density", 2500)
        population_score = min(100, (population_density / 5000) * 100)
        
        # 경쟁 수준 점수 (상권 밀도 기반, 낮을수록 좋음)
        competition_score = 70  # 기본값, 실제로는 상권 밀도 계산
        
        # 접근성 점수 (교통편, 지하철역 등)
        accessibility_score = 75  # 기본값
        
        # 임대료 점수 (낮을수록 좋음)
        rent_score = 60  # 기본값, 실제로는 지역별 임대료 비교
        
        # 유동인구 점수
        foot_traffic_score = 65  # 기본값
        
        # 가중 평균 계산
        total = (
            population_score * self.weights["market_factors"]["population_density"] +
            competition_score * self.weights["market_factors"]["competition_level"] +
            accessibility_score * self.weights["market_factors"]["accessibility"] +
            rent_score * self.weights["market_factors"]["rent_cost"] +
            foot_traffic_score * self.weights["market_factors"]["foot_traffic"]
        )
        
        return {
            "total": round(total, 1),
            "population_density": round(population_score, 1),
            "competition_level": round(competition_score, 1),
            "accessibility": round(accessibility_score, 1),
            "rent_cost": round(rent_score, 1),
            "foot_traffic": round(foot_traffic_score, 1)
        }
    
    def _calculate_industry_factors_score(self, industry_data: Dict[str, Any]) -> Dict[str, Any]:
        """업종 요인 점수 계산"""
        # 생존율 점수
        survival_rate = industry_data.get("survival_rate", 70.0)
        survival_score = survival_rate
        
        # 성장 잠재력 점수
        growth_potential = industry_data.get("growth_potential", 0.6)
        growth_score = growth_potential * 100
        
        # 리스크 점수 (낮을수록 좋음)
        risk_level = industry_data.get("risk_level", 0.4)
        risk_score = (1 - risk_level) * 100
        
        # 경쟁 강도 점수 (낮을수록 좋음)
        competition_intensity = industry_data.get("competition_intensity", 0.5)
        competition_score = (1 - competition_intensity) * 100
        
        # 가중 평균 계산
        total = (
            survival_score * self.weights["industry_factors"]["survival_rate"] +
            growth_score * self.weights["industry_factors"]["growth_potential"] +
            risk_score * self.weights["industry_factors"]["risk_level"] +
            competition_score * self.weights["industry_factors"]["competition_intensity"]
        )
        
        return {
            "total": round(total, 1),
            "survival_rate": round(survival_score, 1),
            "growth_potential": round(growth_score, 1),
            "risk_level": round(risk_score, 1),
            "competition_intensity": round(competition_score, 1)
        }
    
    def _calculate_regional_factors_score(self, regional_data: Dict[str, Any]) -> Dict[str, Any]:
        """지역 요인 점수 계산"""
        # 경제 지표 점수
        economic_growth = regional_data.get("economic_growth", 2.0)
        unemployment_rate = regional_data.get("unemployment_rate", 3.0)
        average_income = regional_data.get("average_income", 3000000)
        
        economic_score = (
            min(100, (economic_growth / 3.0) * 100) * 0.4 +
            max(0, (5.0 - unemployment_rate) / 5.0 * 100) * 0.3 +
            min(100, (average_income / 5000000) * 100) * 0.3
        )
        
        # 인구 통계 점수
        demographics_score = 70  # 기본값
        
        # 인프라 점수
        infrastructure_score = regional_data.get("infrastructure_score", 0.7) * 100
        
        # 가중 평균 계산
        total = (
            economic_score * self.weights["regional_factors"]["economic_indicators"] +
            demographics_score * self.weights["regional_factors"]["demographics"] +
            infrastructure_score * self.weights["regional_factors"]["infrastructure"]
        )
        
        return {
            "total": round(total, 1),
            "economic_indicators": round(economic_score, 1),
            "demographics": round(demographics_score, 1),
            "infrastructure": round(infrastructure_score, 1)
        }
    
    def _determine_grade(self, score: float) -> str:
        """점수에 따른 등급 결정"""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B+"
        elif score >= 60:
            return "B"
        elif score >= 50:
            return "C+"
        elif score >= 40:
            return "C"
        else:
            return "D"
    
    def _generate_recommendations(self, market_score: Dict[str, Any], 
                                industry_score: Dict[str, Any], 
                                regional_score: Dict[str, Any]) -> List[str]:
        """점수에 따른 권장사항 생성"""
        recommendations = []
        
        # 상권 요인 기반 권장사항
        if market_score["competition_level"] < 50:
            recommendations.append("경쟁이 치열한 지역입니다. 차별화된 전략이 필요합니다.")
        
        if market_score["rent_cost"] < 50:
            recommendations.append("임대료가 높은 지역입니다. 비용 효율성을 고려하세요.")
        
        if market_score["accessibility"] < 50:
            recommendations.append("접근성이 떨어집니다. 교통편을 고려한 마케팅이 필요합니다.")
        
        # 업종 요인 기반 권장사항
        if industry_score["risk_level"] < 50:
            recommendations.append("업종의 리스크가 높습니다. 신중한 사업 계획이 필요합니다.")
        
        if industry_score["competition_intensity"] < 50:
            recommendations.append("업종 내 경쟁이 치열합니다. 차별화된 서비스 개발이 필요합니다.")
        
        # 지역 요인 기반 권장사항
        if regional_score["economic_indicators"] < 50:
            recommendations.append("지역 경제 상황이 좋지 않습니다. 시장 진입을 신중히 고려하세요.")
        
        if not recommendations:
            recommendations.append("전반적으로 양호한 조건입니다. 신중한 사업 계획으로 성공 가능성이 높습니다.")
        
        return recommendations
    
    def _assess_risk(self, market_score: Dict[str, Any], 
                    industry_score: Dict[str, Any], 
                    regional_score: Dict[str, Any]) -> Dict[str, Any]:
        """리스크 평가"""
        # 전체 리스크 점수 계산 (낮을수록 위험)
        risk_score = (
            market_score["total"] * 0.4 +
            industry_score["total"] * 0.35 +
            regional_score["total"] * 0.25
        )
        
        # 리스크 등급 결정
        if risk_score >= 80:
            risk_level = "LOW"
            risk_description = "낮은 리스크"
        elif risk_score >= 60:
            risk_level = "MEDIUM"
            risk_description = "보통 리스크"
        else:
            risk_level = "HIGH"
            risk_description = "높은 리스크"
        
        return {
            "risk_score": round(risk_score, 1),
            "risk_level": risk_level,
            "risk_description": risk_description,
            "risk_factors": {
                "market_risk": "HIGH" if market_score["total"] < 60 else "MEDIUM" if market_score["total"] < 80 else "LOW",
                "industry_risk": "HIGH" if industry_score["total"] < 60 else "MEDIUM" if industry_score["total"] < 80 else "LOW",
                "regional_risk": "HIGH" if regional_score["total"] < 60 else "MEDIUM" if regional_score["total"] < 80 else "LOW"
            }
        }
