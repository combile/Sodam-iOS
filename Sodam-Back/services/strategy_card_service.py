import os
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import numpy as np

class StrategyCardService:
    """맞춤형 전략 카드 시스템"""
    
    def __init__(self):
        self.strategy_templates = self._init_strategy_templates()
        self.checklist_templates = self._init_checklist_templates()
        self.success_cases = self._init_success_cases()
    
    def generate_strategy_cards(self, market_code: str, industry: str, risk_type: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """맞춤형 전략 카드 생성"""
        
        # 사용자 프로필 기반 전략 선택
        strategies = self._select_strategies(industry, risk_type, user_profile)
        
        # 전략 카드 생성
        strategy_cards = []
        for strategy in strategies:
            card = self._create_strategy_card(strategy, market_code, industry, user_profile)
            strategy_cards.append(card)
        
        return {
            "market_code": market_code,
            "industry": industry,
            "risk_type": risk_type,
            "user_profile": user_profile,
            "strategy_cards": strategy_cards,
            "total_strategies": len(strategy_cards),
            "priority_order": self._get_priority_order(strategy_cards)
        }
    
    def get_strategy_checklist(self, strategy_id: str) -> Dict[str, Any]:
        """전략별 체크리스트 제공"""
        if strategy_id not in self.checklist_templates:
            return {"error": "해당 전략의 체크리스트가 없습니다."}
        
        checklist = self.checklist_templates[strategy_id]
        return {
            "strategy_id": strategy_id,
            "strategy_name": checklist["name"],
            "checklist": checklist["items"],
            "estimated_duration": checklist["duration"],
            "difficulty": checklist["difficulty"],
            "required_resources": checklist["resources"]
        }
    
    def get_success_cases(self, industry: str = None, strategy_type: str = None) -> Dict[str, Any]:
        """성공 사례 제공"""
        filtered_cases = self.success_cases
        
        if industry:
            filtered_cases = [case for case in filtered_cases if case["industry"] == industry]
        
        if strategy_type:
            filtered_cases = [case for case in filtered_cases if case["strategy_type"] == strategy_type]
        
        return {
            "total_cases": len(filtered_cases),
            "success_cases": filtered_cases[:10],  # 최대 10개
            "filters": {
                "industry": industry,
                "strategy_type": strategy_type
            }
        }
    
    def _init_strategy_templates(self) -> Dict[str, Any]:
        """전략 템플릿 초기화"""
        return {
            "marketing_boost": {
                "id": "marketing_boost",
                "name": "마케팅 부스터",
                "category": "마케팅",
                "description": "유동인구 증가를 위한 마케팅 전략",
                "target_risks": ["유입 저조형"],
                "target_industries": ["식음료업", "의류업", "생활용품"],
                "difficulty": "중간",
                "duration": "2-3개월",
                "cost_level": "중간",
                "expected_impact": "유동인구 20-30% 증가"
            },
            "differentiation": {
                "id": "differentiation",
                "name": "차별화 전략",
                "category": "경쟁력",
                "description": "경쟁 우위 확보를 위한 차별화 전략",
                "target_risks": ["과포화 경쟁형"],
                "target_industries": ["식음료업", "의류업", "화장품"],
                "difficulty": "높음",
                "duration": "3-6개월",
                "cost_level": "높음",
                "expected_impact": "고객 충성도 30-40% 향상"
            },
            "price_optimization": {
                "id": "price_optimization",
                "name": "가격 최적화",
                "category": "운영",
                "description": "소비력에 맞는 가격 정책 수립",
                "target_risks": ["소비력 약형"],
                "target_industries": ["식음료업", "생활용품", "전자제품"],
                "difficulty": "낮음",
                "duration": "1-2개월",
                "cost_level": "낮음",
                "expected_impact": "매출 15-25% 증가"
            },
            "innovation": {
                "id": "innovation",
                "name": "혁신 모델",
                "category": "혁신",
                "description": "혁신적 비즈니스 모델 도입",
                "target_risks": ["성장 잠재형"],
                "target_industries": ["전자제품", "화장품", "생활용품"],
                "difficulty": "매우 높음",
                "duration": "6-12개월",
                "cost_level": "매우 높음",
                "expected_impact": "시장 점유율 50% 이상 확대"
            },
            "online_expansion": {
                "id": "online_expansion",
                "name": "온라인 확장",
                "category": "채널",
                "description": "온라인 판매 채널 구축 및 확대",
                "target_risks": ["소비력 약형", "유입 저조형"],
                "target_industries": ["의류업", "화장품", "전자제품"],
                "difficulty": "중간",
                "duration": "3-4개월",
                "cost_level": "중간",
                "expected_impact": "온라인 매출 100-200% 증가"
            },
            "customer_loyalty": {
                "id": "customer_loyalty",
                "name": "고객 충성도",
                "category": "고객관리",
                "description": "고객 충성도 향상 프로그램",
                "target_risks": ["과포화 경쟁형", "유입 저조형"],
                "target_industries": ["식음료업", "화장품", "생활용품"],
                "difficulty": "중간",
                "duration": "2-4개월",
                "cost_level": "중간",
                "expected_impact": "재방문율 40-50% 향상"
            }
        }
    
    def _init_checklist_templates(self) -> Dict[str, Any]:
        """체크리스트 템플릿 초기화"""
        return {
            "marketing_boost": {
                "name": "마케팅 부스터",
                "duration": "2-3개월",
                "difficulty": "중간",
                "resources": ["마케팅 예산", "디자인 리소스", "SNS 계정"],
                "items": [
                    {"step": 1, "task": "타겟 고객 분석 및 페르소나 설정", "duration": "1주", "status": "pending"},
                    {"step": 2, "task": "브랜드 아이덴티티 및 메시지 개발", "duration": "2주", "status": "pending"},
                    {"step": 3, "task": "SNS 마케팅 채널 구축 및 콘텐츠 기획", "duration": "2주", "status": "pending"},
                    {"step": 4, "task": "지역 이벤트 및 프로모션 기획", "duration": "1주", "status": "pending"},
                    {"step": 5, "task": "온라인 광고 캠페인 실행", "duration": "4주", "status": "pending"},
                    {"step": 6, "task": "오프라인 이벤트 개최", "duration": "2주", "status": "pending"},
                    {"step": 7, "task": "성과 측정 및 개선 방안 수립", "duration": "1주", "status": "pending"}
                ]
            },
            "differentiation": {
                "name": "차별화 전략",
                "duration": "3-6개월",
                "difficulty": "높음",
                "resources": ["R&D 예산", "전문 인력", "시장 조사 리소스"],
                "items": [
                    {"step": 1, "task": "경쟁사 분석 및 시장 포지셔닝", "duration": "2주", "status": "pending"},
                    {"step": 2, "task": "차별화 포인트 발굴 및 검증", "duration": "3주", "status": "pending"},
                    {"step": 3, "task": "고유 상품/서비스 개발", "duration": "8주", "status": "pending"},
                    {"step": 4, "task": "브랜드 스토리 및 메시지 개발", "duration": "2주", "status": "pending"},
                    {"step": 5, "task": "차별화 요소 마케팅 전략 수립", "duration": "2주", "status": "pending"},
                    {"step": 6, "task": "고객 피드백 수집 및 개선", "duration": "4주", "status": "pending"}
                ]
            },
            "price_optimization": {
                "name": "가격 최적화",
                "duration": "1-2개월",
                "difficulty": "낮음",
                "resources": ["가격 분석 도구", "시장 조사 데이터"],
                "items": [
                    {"step": 1, "task": "현재 가격 구조 분석", "duration": "3일", "status": "pending"},
                    {"step": 2, "task": "경쟁사 가격 조사", "duration": "1주", "status": "pending"},
                    {"step": 3, "task": "고객 가격 민감도 분석", "duration": "1주", "status": "pending"},
                    {"step": 4, "task": "최적 가격 모델 수립", "duration": "3일", "status": "pending"},
                    {"step": 5, "task": "가격 정책 적용 및 모니터링", "duration": "2주", "status": "pending"}
                ]
            }
        }
    
    def _init_success_cases(self) -> List[Dict[str, Any]]:
        """성공 사례 초기화"""
        return [
            {
                "id": "case_001",
                "title": "강남역 카페 '커피앤북' 성공 사례",
                "industry": "식음료업",
                "strategy_type": "differentiation",
                "location": "강남역 상권",
                "challenge": "과포화된 카페 시장에서 차별화 필요",
                "solution": "독서 카페 컨셉으로 전환, 도서 대여 서비스 추가",
                "results": {
                    "revenue_increase": "45%",
                    "customer_retention": "60%",
                    "average_dwell_time": "90분"
                },
                "key_factors": ["독특한 컨셉", "고객 체류시간 연장", "부가 서비스"],
                "duration": "6개월",
                "investment": "500만원"
            },
            {
                "id": "case_002",
                "title": "홍대 의류점 '스타일랩' 성공 사례",
                "industry": "의류업",
                "strategy_type": "online_expansion",
                "location": "홍대 상권",
                "challenge": "오프라인 매출 감소, 온라인 진출 필요",
                "solution": "인스타그램 쇼핑몰 구축, 인플루언서 마케팅",
                "results": {
                    "online_revenue": "200%",
                    "total_revenue": "80%",
                    "new_customers": "150%"
                },
                "key_factors": ["SNS 마케팅", "인플루언서 협업", "온라인 쇼핑몰"],
                "duration": "4개월",
                "investment": "300만원"
            },
            {
                "id": "case_003",
                "title": "명동 화장품점 '뷰티허브' 성공 사례",
                "industry": "화장품",
                "strategy_type": "customer_loyalty",
                "location": "명동 상권",
                "challenge": "고객 충성도 부족, 재방문율 저조",
                "solution": "맞춤형 뷰티 컨설팅 서비스, 멤버십 프로그램",
                "results": {
                    "customer_retention": "70%",
                    "average_purchase": "35%",
                    "repeat_customers": "85%"
                },
                "key_factors": ["개인 맞춤 서비스", "멤버십 혜택", "전문 컨설팅"],
                "duration": "3개월",
                "investment": "200만원"
            }
        ]
    
    def _select_strategies(self, industry: str, risk_type: str, user_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """사용자 프로필 기반 전략 선택"""
        selected_strategies = []
        
        # 리스크 유형별 우선 전략
        risk_strategy_map = {
            "유입 저조형": ["marketing_boost", "online_expansion", "customer_loyalty"],
            "과포화 경쟁형": ["differentiation", "customer_loyalty", "price_optimization"],
            "소비력 약형": ["price_optimization", "online_expansion", "marketing_boost"],
            "성장 잠재형": ["innovation", "differentiation", "marketing_boost"]
        }
        
        # 업종별 적합한 전략
        industry_strategy_map = {
            "식음료업": ["marketing_boost", "customer_loyalty", "differentiation"],
            "의류업": ["online_expansion", "differentiation", "marketing_boost"],
            "화장품": ["customer_loyalty", "differentiation", "online_expansion"],
            "생활용품": ["price_optimization", "online_expansion", "marketing_boost"],
            "전자제품": ["innovation", "online_expansion", "price_optimization"]
        }
        
        # 사용자 프로필 고려
        user_type = user_profile.get("userType", "ENTREPRENEUR")
        business_stage = user_profile.get("businessStage", "PLANNING")
        capital = user_profile.get("capital", 0)
        
        # 전략 우선순위 결정
        priority_strategies = risk_strategy_map.get(risk_type, [])
        industry_strategies = industry_strategy_map.get(industry, [])
        
        # 교집합 우선, 그 다음 리스크 기반 전략
        common_strategies = list(set(priority_strategies) & set(industry_strategies))
        remaining_strategies = [s for s in priority_strategies if s not in common_strategies]
        
        final_strategies = common_strategies + remaining_strategies[:2]  # 최대 3개
        
        # 자본 규모에 따른 필터링
        for strategy_id in final_strategies:
            strategy = self.strategy_templates[strategy_id]
            if self._is_affordable(strategy, capital, business_stage):
                selected_strategies.append(strategy)
        
        return selected_strategies[:3]  # 최대 3개 전략
    
    def _is_affordable(self, strategy: Dict[str, Any], capital: int, business_stage: str) -> bool:
        """자본 규모에 따른 전략 적합성 판단"""
        cost_levels = {"낮음": 1000000, "중간": 5000000, "높음": 15000000, "매우 높음": 30000000}
        required_capital = cost_levels.get(strategy["cost_level"], 5000000)
        
        # 계획 단계에서는 낮은 비용 전략만
        if business_stage == "PLANNING" and strategy["cost_level"] in ["높음", "매우 높음"]:
            return False
        
        return capital >= required_capital * 0.3  # 자본의 30% 이상이면 실행 가능
    
    def _create_strategy_card(self, strategy: Dict[str, Any], market_code: str, industry: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """전략 카드 생성"""
        return {
            "strategy_id": strategy["id"],
            "strategy_name": strategy["name"],
            "category": strategy["category"],
            "description": strategy["description"],
            "difficulty": strategy["difficulty"],
            "duration": strategy["duration"],
            "cost_level": strategy["cost_level"],
            "expected_impact": strategy["expected_impact"],
            "priority": self._calculate_priority(strategy, market_code, industry, user_profile),
            "action_tips": self._get_action_tips(strategy["id"]),
            "success_probability": self._calculate_success_probability(strategy, user_profile),
            "next_steps": self._get_next_steps(strategy["id"])
        }
    
    def _calculate_priority(self, strategy: Dict[str, Any], market_code: str, industry: str, user_profile: Dict[str, Any]) -> int:
        """전략 우선순위 계산 (1-5, 5가 최고)"""
        priority = 3  # 기본값
        
        # 리스크 유형과의 매칭도
        risk_type = user_profile.get("riskType", "유입 저조형")
        if risk_type in strategy.get("target_risks", []):
            priority += 1
        
        # 업종과의 매칭도
        if industry in strategy.get("target_industries", []):
            priority += 1
        
        # 자본 규모 고려
        capital = user_profile.get("capital", 0)
        if strategy["cost_level"] == "낮음" and capital < 5000000:
            priority += 1
        elif strategy["cost_level"] == "중간" and 5000000 <= capital < 20000000:
            priority += 1
        elif strategy["cost_level"] in ["높음", "매우 높음"] and capital >= 20000000:
            priority += 1
        
        return min(priority, 5)
    
    def _get_action_tips(self, strategy_id: str) -> List[str]:
        """전략별 실행 팁"""
        tips_map = {
            "marketing_boost": [
                "SNS 계정을 활발히 운영하여 브랜드 인지도 향상",
                "지역 이벤트에 참여하여 커뮤니티와의 관계 구축",
                "인플루언서와의 협업을 통한 타겟 고객 접근"
            ],
            "differentiation": [
                "고객 피드백을 적극 수집하여 차별화 포인트 발굴",
                "경쟁사와 다른 독특한 서비스나 상품 개발",
                "브랜드 스토리를 강화하여 감정적 연결 구축"
            ],
            "price_optimization": [
                "고객 가격 민감도를 정확히 파악",
                "가격 변경 시 고객에게 충분한 설명 제공",
                "할인 정책보다는 가치 제공에 집중"
            ]
        }
        return tips_map.get(strategy_id, ["전략 실행을 위한 구체적인 계획 수립이 필요합니다."])
    
    def _calculate_success_probability(self, strategy: Dict[str, Any], user_profile: Dict[str, Any]) -> int:
        """성공 확률 계산 (0-100%)"""
        base_probability = 60  # 기본 성공 확률
        
        # 경험 수준 고려
        experience = user_profile.get("experience", "beginner")
        if experience == "expert":
            base_probability += 20
        elif experience == "intermediate":
            base_probability += 10
        
        # 자본 규모 고려
        capital = user_profile.get("capital", 0)
        if capital >= 20000000:
            base_probability += 15
        elif capital >= 10000000:
            base_probability += 10
        elif capital >= 5000000:
            base_probability += 5
        
        # 사업 단계 고려
        business_stage = user_profile.get("businessStage", "PLANNING")
        if business_stage in ["GROWTH", "MATURE"]:
            base_probability += 10
        
        return min(base_probability, 95)  # 최대 95%
    
    def _get_next_steps(self, strategy_id: str) -> List[str]:
        """다음 단계 안내"""
        steps_map = {
            "marketing_boost": [
                "1. 타겟 고객 분석 및 페르소나 설정",
                "2. 마케팅 예산 계획 수립",
                "3. SNS 계정 개설 및 브랜드 아이덴티티 개발"
            ],
            "differentiation": [
                "1. 경쟁사 분석 및 시장 조사",
                "2. 차별화 포인트 발굴 및 검증",
                "3. 고유 상품/서비스 개발 계획 수립"
            ],
            "price_optimization": [
                "1. 현재 가격 구조 분석",
                "2. 경쟁사 가격 조사",
                "3. 고객 가격 민감도 분석"
            ]
        }
        return steps_map.get(strategy_id, ["전략 실행을 위한 상세 계획 수립이 필요합니다."])
    
    def _get_priority_order(self, strategy_cards: List[Dict[str, Any]]) -> List[str]:
        """전략 우선순위 정렬"""
        sorted_cards = sorted(strategy_cards, key=lambda x: x["priority"], reverse=True)
        return [card["strategy_id"] for card in sorted_cards]
