import os
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import numpy as np

class RiskAnalysisService:
    """4가지 리스크 유형 자동 분류 및 분석 서비스"""
    
    def __init__(self):
        self.core_diagnosis = None  # CoreDiagnosisService 인스턴스
        
    def classify_risk_type(self, market_code: str, industry: str = None) -> Dict[str, Any]:
        """4가지 리스크 유형 자동 분류"""
        
        # 임시 샘플 데이터 (실제로는 CoreDiagnosisService에서 가져와야 함)
        sample_data = self._get_sample_market_data(market_code)
        
        # 각 지표별 점수 계산
        foot_traffic_score = self._calculate_foot_traffic_score(sample_data["foot_traffic_change"])
        card_sales_score = self._calculate_card_sales_score(sample_data["card_sales_change"])
        competition_score = self._calculate_competition_score(sample_data["same_industry_ratio"])
        consumption_score = self._calculate_consumption_score(sample_data["average_income"])
        growth_score = self._calculate_growth_score(sample_data["growth_potential"])
        
        # 리스크 유형별 점수 계산
        risk_scores = {
            "유입 저조형": self._calculate_inflow_risk_score(foot_traffic_score, card_sales_score),
            "과포화 경쟁형": self._calculate_competition_risk_score(competition_score, sample_data["same_industry_ratio"]),
            "소비력 약형": self._calculate_consumption_risk_score(consumption_score, card_sales_score),
            "성장 잠재형": self._calculate_growth_risk_score(growth_score, foot_traffic_score, card_sales_score)
        }
        
        # 가장 높은 리스크 유형 결정
        primary_risk = max(risk_scores.items(), key=lambda x: x[1])
        secondary_risks = sorted(risk_scores.items(), key=lambda x: x[1], reverse=True)[1:3]
        
        return {
            "market_code": market_code,
            "industry": industry,
            "primary_risk_type": primary_risk[0],
            "primary_risk_score": round(primary_risk[1], 2),
            "secondary_risks": [
                {"type": risk[0], "score": round(risk[1], 2)} 
                for risk in secondary_risks
            ],
            "risk_breakdown": {
                "유입 저조형": round(risk_scores["유입 저조형"], 2),
                "과포화 경쟁형": round(risk_scores["과포화 경쟁형"], 2),
                "소비력 약형": round(risk_scores["소비력 약형"], 2),
                "성장 잠재형": round(risk_scores["성장 잠재형"], 2)
            },
            "risk_level": self._get_risk_level(primary_risk[1]),
            "analysis": self._get_risk_analysis(primary_risk[0], primary_risk[1]),
            "recommendations": self._get_risk_recommendations(primary_risk[0], primary_risk[1])
        }
    
    def get_detailed_risk_analysis(self, market_code: str, risk_type: str, industry: str = None) -> Dict[str, Any]:
        """특정 리스크 유형의 상세 분석"""
        
        risk_analysis_map = {
            "유입 저조형": self._analyze_inflow_risk,
            "과포화 경쟁형": self._analyze_competition_risk,
            "소비력 약형": self._analyze_consumption_risk,
            "성장 잠재형": self._analyze_growth_risk
        }
        
        if risk_type not in risk_analysis_map:
            return {"error": "지원하지 않는 리스크 유형입니다."}
        
        return risk_analysis_map[risk_type](market_code, industry)
    
    def _get_sample_market_data(self, market_code: str) -> Dict[str, Any]:
        """샘플 시장 데이터 (실제로는 외부 API에서 가져와야 함)"""
        sample_data = {
            "10000": {  # 대전역 상권
                "foot_traffic_change": 5.2,  # 월평균 변화율 (%)
                "card_sales_change": 3.8,    # 월평균 변화율 (%)
                "same_industry_ratio": 25.5, # 동일업종 비율 (%)
                "average_income": 35000000,  # 평균 소득 (원)
                "growth_potential": 85,      # 성장 잠재력 점수
                "population_density": 1500,  # 인구 밀도
                "rent_level": "high",        # 임대료 수준
                "accessibility": 90          # 접근성 점수
            },
            "20000": {  # 유성온천역 상권
                "foot_traffic_change": 2.1,
                "card_sales_change": 1.5,
                "same_industry_ratio": 35.2,
                "average_income": 42000000,
                "growth_potential": 75,
                "population_density": 1200,
                "rent_level": "medium",
                "accessibility": 85
            }
        }
        
        return sample_data.get(market_code, sample_data["10000"])
    
    def _calculate_foot_traffic_score(self, change_rate: float) -> float:
        """유동인구 점수 계산"""
        if change_rate > 5:
            return 100
        elif change_rate > 0:
            return 80
        elif change_rate > -5:
            return 60
        else:
            return 40
    
    def _calculate_card_sales_score(self, change_rate: float) -> float:
        """카드매출 점수 계산"""
        if change_rate > 3:
            return 100
        elif change_rate > 0:
            return 80
        elif change_rate > -3:
            return 60
        else:
            return 40
    
    def _calculate_competition_score(self, ratio: float) -> float:
        """경쟁도 점수 계산 (높을수록 위험)"""
        if ratio > 30:
            return 20  # 매우 위험
        elif ratio > 20:
            return 40  # 위험
        elif ratio > 10:
            return 60  # 보통
        else:
            return 80  # 안전
    
    def _calculate_consumption_score(self, income: float) -> float:
        """소비력 점수 계산"""
        if income > 40000000:
            return 100
        elif income > 30000000:
            return 80
        elif income > 20000000:
            return 60
        else:
            return 40
    
    def _calculate_growth_score(self, potential: float) -> float:
        """성장 잠재력 점수 계산"""
        if potential > 80:
            return 100
        elif potential > 60:
            return 80
        elif potential > 40:
            return 60
        else:
            return 40
    
    def _calculate_inflow_risk_score(self, foot_traffic_score: float, card_sales_score: float) -> float:
        """유입 저조형 리스크 점수 계산"""
        return (100 - foot_traffic_score) * 0.6 + (100 - card_sales_score) * 0.4
    
    def _calculate_competition_risk_score(self, competition_score: float, ratio: float) -> float:
        """과포화 경쟁형 리스크 점수 계산"""
        return (100 - competition_score) * 0.8 + min(ratio * 2, 100) * 0.2
    
    def _calculate_consumption_risk_score(self, consumption_score: float, card_sales_score: float) -> float:
        """소비력 약형 리스크 점수 계산"""
        return (100 - consumption_score) * 0.7 + (100 - card_sales_score) * 0.3
    
    def _calculate_growth_risk_score(self, growth_score: float, foot_traffic_score: float, card_sales_score: float) -> float:
        """성장 잠재형 리스크 점수 계산"""
        return (100 - growth_score) * 0.5 + (100 - foot_traffic_score) * 0.3 + (100 - card_sales_score) * 0.2
    
    def _get_risk_level(self, risk_score: float) -> str:
        """리스크 레벨 결정"""
        if risk_score >= 80:
            return "매우 높음"
        elif risk_score >= 60:
            return "높음"
        elif risk_score >= 40:
            return "보통"
        else:
            return "낮음"
    
    def _get_risk_analysis(self, risk_type: str, risk_score: float) -> str:
        """리스크 분석 텍스트 생성"""
        risk_descriptions = {
            "유입 저조형": f"유동인구와 매출 증가율이 낮아 상권 활성화가 저조한 상태입니다. (리스크 점수: {risk_score:.1f})",
            "과포화 경쟁형": f"동일업종 사업체가 과도하게 많아 경쟁이 치열한 상태입니다. (리스크 점수: {risk_score:.1f})",
            "소비력 약형": f"지역 소비력이 부족하여 매출 창출이 어려운 상태입니다. (리스크 점수: {risk_score:.1f})",
            "성장 잠재형": f"성장 잠재력이 제한적이어서 장기적 발전이 어려운 상태입니다. (리스크 점수: {risk_score:.1f})"
        }
        return risk_descriptions.get(risk_type, "리스크 분석을 수행할 수 없습니다.")
    
    def _get_risk_recommendations(self, risk_type: str, risk_score: float) -> List[str]:
        """리스크별 추천사항 생성"""
        recommendations_map = {
            "유입 저조형": [
                "마케팅 강화를 통한 유동인구 증가 방안 모색",
                "이벤트 및 프로모션을 통한 상권 활성화",
                "접근성 개선을 위한 교통편 확충 검토",
                "대안 상권 검토 권장"
            ],
            "과포화 경쟁형": [
                "차별화된 상품 및 서비스 개발",
                "니치 마켓 타겟팅 전략 수립",
                "고객 충성도 향상 프로그램 도입",
                "경쟁사 분석을 통한 우위 요소 발굴"
            ],
            "소비력 약형": [
                "가격 경쟁력 강화 방안 검토",
                "고객층 확대를 위한 마케팅 전략 수립",
                "온라인 판매 채널 확대 고려",
                "소득 수준에 맞는 상품 구성 조정"
            ],
            "성장 잠재형": [
                "상권 발전 계획 수립 및 참여",
                "지역 상생 프로그램 참여",
                "혁신적 비즈니스 모델 도입",
                "장기적 관점에서의 투자 계획 수립"
            ]
        }
        
        base_recommendations = recommendations_map.get(risk_type, [])
        
        # 리스크 점수에 따른 추가 권고사항
        if risk_score >= 80:
            base_recommendations.insert(0, "⚠️ 높은 리스크로 인해 신중한 검토가 필요합니다.")
        elif risk_score >= 60:
            base_recommendations.insert(0, "⚠️ 중간 리스크로 인해 개선 방안이 필요합니다.")
        
        return base_recommendations
    
    def _analyze_inflow_risk(self, market_code: str, industry: str = None) -> Dict[str, Any]:
        """유입 저조형 리스크 상세 분석"""
        return {
            "risk_type": "유입 저조형",
            "market_code": market_code,
            "industry": industry,
            "risk_factors": [
                {
                    "factor": "유동인구 감소",
                    "impact": "높음",
                    "description": "월평균 유동인구 증가율이 낮아 상권 활성화가 저조합니다.",
                    "mitigation": "마케팅 강화 및 이벤트 개최를 통한 유동인구 증가 방안 모색"
                },
                {
                    "factor": "매출 증가율 둔화",
                    "impact": "높음",
                    "description": "카드매출 증가율이 낮아 소비활동이 위축되고 있습니다.",
                    "mitigation": "프로모션 및 할인 이벤트를 통한 소비 촉진 방안 검토"
                },
                {
                    "factor": "접근성 부족",
                    "impact": "중간",
                    "description": "교통편 부족으로 인한 접근성 문제가 있습니다.",
                    "mitigation": "교통편 확충 및 주차 시설 개선 방안 검토"
                }
            ],
            "success_cases": [
                {
                    "location": "강남역 상권",
                    "solution": "지하철 연결 통로 개선 및 쇼핑몰 리뉴얼",
                    "result": "유동인구 30% 증가, 매출 25% 상승"
                },
                {
                    "location": "홍대 상권",
                    "solution": "야간 경제 활성화 및 문화 이벤트 개최",
                    "result": "야간 유동인구 40% 증가, 체류시간 20% 연장"
                }
            ],
            "action_plan": [
                "1단계: 유동인구 증가를 위한 마케팅 전략 수립 (1개월)",
                "2단계: 이벤트 및 프로모션 기획 및 실행 (2-3개월)",
                "3단계: 접근성 개선 방안 검토 및 실행 (3-6개월)",
                "4단계: 효과 측정 및 개선 방안 수립 (6개월 후)"
            ]
        }
    
    def _analyze_competition_risk(self, market_code: str, industry: str = None) -> Dict[str, Any]:
        """과포화 경쟁형 리스크 상세 분석"""
        return {
            "risk_type": "과포화 경쟁형",
            "market_code": market_code,
            "industry": industry,
            "risk_factors": [
                {
                    "factor": "동일업종 과밀",
                    "impact": "매우 높음",
                    "description": "동일업종 사업체가 과도하게 많아 경쟁이 치열합니다.",
                    "mitigation": "차별화된 상품 및 서비스 개발을 통한 경쟁 우위 확보"
                },
                {
                    "factor": "가격 경쟁 심화",
                    "impact": "높음",
                    "description": "과도한 가격 경쟁으로 인한 수익성 악화가 우려됩니다.",
                    "mitigation": "가치 기반 마케팅을 통한 가격 경쟁 회피"
                },
                {
                    "factor": "고객 분산",
                    "impact": "중간",
                    "description": "고객이 여러 업체로 분산되어 충성도가 낮습니다.",
                    "mitigation": "고객 충성도 향상 프로그램 도입"
                }
            ],
            "success_cases": [
                {
                    "location": "명동 상권",
                    "solution": "브랜드 차별화 및 고급화 전략",
                    "result": "평균 단가 30% 상승, 고객 충성도 40% 향상"
                },
                {
                    "location": "신촌 상권",
                    "solution": "니치 마켓 타겟팅 및 특화 서비스",
                    "result": "전문성 인지도 50% 향상, 재방문율 35% 증가"
                }
            ],
            "action_plan": [
                "1단계: 경쟁사 분석 및 차별화 포인트 발굴 (1개월)",
                "2단계: 차별화 전략 수립 및 실행 (2-3개월)",
                "3단계: 고객 충성도 향상 프로그램 도입 (3-4개월)",
                "4단계: 시장 점유율 확대 및 브랜드 강화 (6개월 후)"
            ]
        }
    
    def _analyze_consumption_risk(self, market_code: str, industry: str = None) -> Dict[str, Any]:
        """소비력 약형 리스크 상세 분석"""
        return {
            "risk_type": "소비력 약형",
            "market_code": market_code,
            "industry": industry,
            "risk_factors": [
                {
                    "factor": "지역 소득 수준 낮음",
                    "impact": "높음",
                    "description": "지역 평균 소득이 낮아 소비력이 제한적입니다.",
                    "mitigation": "소득 수준에 맞는 상품 구성 및 가격 정책 수립"
                },
                {
                    "factor": "소비 패턴 변화",
                    "impact": "중간",
                    "description": "온라인 쇼핑 증가로 인한 오프라인 소비 감소",
                    "mitigation": "온라인 연계 서비스 및 경험 중심 상품 개발"
                },
                {
                    "factor": "인구 감소",
                    "impact": "중간",
                    "description": "지역 인구 감소로 인한 소비 시장 축소",
                    "mitigation": "외부 고객 유치 및 관광 상품 개발"
                }
            ],
            "success_cases": [
                {
                    "location": "부산 자갈치 시장",
                    "solution": "관광 상품화 및 온라인 판매 채널 확대",
                    "result": "외부 고객 60% 증가, 온라인 매출 200% 상승"
                },
                {
                    "location": "전주 한옥마을",
                    "solution": "체험형 관광 상품 개발 및 문화 콘텐츠 강화",
                    "result": "체류시간 50% 연장, 평균 소비액 40% 증가"
                }
            ],
            "action_plan": [
                "1단계: 고객 소득 수준 분석 및 타겟 설정 (1개월)",
                "2단계: 가격 경쟁력 강화 및 상품 구성 조정 (2-3개월)",
                "3단계: 온라인 판매 채널 구축 및 운영 (3-4개월)",
                "4단계: 외부 고객 유치 및 관광 상품 개발 (6개월 후)"
            ]
        }
    
    def _analyze_growth_risk(self, market_code: str, industry: str = None) -> Dict[str, Any]:
        """성장 잠재형 리스크 상세 분석"""
        return {
            "risk_type": "성장 잠재형",
            "market_code": market_code,
            "industry": industry,
            "risk_factors": [
                {
                    "factor": "성장 동력 부족",
                    "impact": "높음",
                    "description": "상권 성장을 이끌 수 있는 동력이 부족합니다.",
                    "mitigation": "혁신적 비즈니스 모델 도입 및 신규 수요 창출"
                },
                {
                    "factor": "인프라 부족",
                    "impact": "중간",
                    "description": "성장을 뒷받침할 인프라가 부족합니다.",
                    "mitigation": "지역 발전 계획 참여 및 인프라 개선 요구"
                },
                {
                    "factor": "정책 지원 부족",
                    "impact": "중간",
                    "description": "상권 발전을 위한 정책적 지원이 부족합니다.",
                    "mitigation": "지역 상생 프로그램 참여 및 정책 제안"
                }
            ],
            "success_cases": [
                {
                    "location": "판교 테크노밸리",
                    "solution": "IT 기업 유치 및 혁신 생태계 구축",
                    "result": "고소득층 유입 300% 증가, 상권 활성화 150% 향상"
                },
                {
                    "location": "제주 중문 관광단지",
                    "solution": "관광 인프라 구축 및 국제 관광객 유치",
                    "result": "관광객 수 200% 증가, 상권 매출 180% 상승"
                }
            ],
            "action_plan": [
                "1단계: 상권 발전 계획 수립 및 이해관계자 모집 (1-2개월)",
                "2단계: 혁신적 비즈니스 모델 도입 및 실행 (3-4개월)",
                "3단계: 지역 상생 프로그램 참여 및 협력 체계 구축 (4-6개월)",
                "4단계: 장기적 투자 계획 수립 및 실행 (6개월 후)"
            ]
        }
