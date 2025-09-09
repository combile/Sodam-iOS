import os
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import numpy as np

class SupportToolsService:
    """실행 지원 도구 서비스"""
    
    def __init__(self):
        self.support_centers = self._init_support_centers()
        self.policies = self._init_policies()
        self.experts = self._init_experts()
        self.success_cases = self._init_success_cases()
    
    def get_support_centers(self, region: str = None, service_type: str = None) -> Dict[str, Any]:
        """소상공인지원센터 정보 조회"""
        filtered_centers = self.support_centers
        
        if region:
            filtered_centers = [center for center in filtered_centers if region in center["region"]]
        
        if service_type:
            filtered_centers = [center for center in filtered_centers if service_type in center["services"]]
        
        return {
            "total_centers": len(filtered_centers),
            "support_centers": filtered_centers,
            "filters": {
                "region": region,
                "service_type": service_type
            }
        }
    
    def get_expert_consultation(self, region: str = None, expertise: str = None) -> Dict[str, Any]:
        """전문가 상담 예약 정보"""
        filtered_experts = self.experts
        
        if region:
            filtered_experts = [expert for expert in filtered_experts if region in expert["region"]]
        
        if expertise:
            filtered_experts = [expert for expert in filtered_experts if expertise in expert["expertise"]]
        
        return {
            "total_experts": len(filtered_experts),
            "experts": filtered_experts,
            "consultation_types": [
                {"type": "온라인 상담", "duration": "30분", "cost": "무료"},
                {"type": "방문 상담", "duration": "1시간", "cost": "무료"},
                {"type": "전화 상담", "duration": "20분", "cost": "무료"}
            ],
            "filters": {
                "region": region,
                "expertise": expertise
            }
        }
    
    def get_policy_recommendations(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """지역 기반 맞춤 창업 지원 정책 추천"""
        region = user_profile.get("preferredAreas", ["대전광역시"])[0] if user_profile.get("preferredAreas") else "대전광역시"
        business_type = user_profile.get("interestedBusinessTypes", ["식음료업"])[0] if user_profile.get("interestedBusinessTypes") else "식음료업"
        user_type = user_profile.get("userType", "ENTREPRENEUR")
        business_stage = user_profile.get("businessStage", "PLANNING")
        
        # 정책 필터링
        recommended_policies = []
        for policy in self.policies:
            if self._is_policy_relevant(policy, region, business_type, user_type, business_stage):
                recommended_policies.append(policy)
        
        # 우선순위 정렬
        recommended_policies.sort(key=lambda x: x["priority"], reverse=True)
        
        return {
            "user_profile": user_profile,
            "total_policies": len(recommended_policies),
            "recommended_policies": recommended_policies[:10],  # 상위 10개
            "application_guide": self._get_application_guide(),
            "deadline_alerts": self._get_deadline_alerts(recommended_policies)
        }
    
    def get_success_cases_browse(self, industry: str = None, region: str = None, strategy_type: str = None) -> Dict[str, Any]:
        """유사 상권 성공 사례 브라우징"""
        filtered_cases = self.success_cases
        
        if industry:
            filtered_cases = [case for case in filtered_cases if case["industry"] == industry]
        
        if region:
            filtered_cases = [case for case in filtered_cases if region in case["region"]]
        
        if strategy_type:
            filtered_cases = [case for case in filtered_cases if case["strategy_type"] == strategy_type]
        
        # 관련도 점수 계산
        for case in filtered_cases:
            case["relevance_score"] = self._calculate_relevance_score(case, industry, region, strategy_type)
        
        # 관련도 순으로 정렬
        filtered_cases.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return {
            "total_cases": len(filtered_cases),
            "success_cases": filtered_cases[:20],  # 상위 20개
            "filters": {
                "industry": industry,
                "region": region,
                "strategy_type": strategy_type
            },
            "case_categories": self._get_case_categories()
        }
    
    def _init_support_centers(self) -> List[Dict[str, Any]]:
        """지원센터 데이터 초기화"""
        return [
            {
                "id": "center_001",
                "name": "대전광역시 소상공인지원센터",
                "region": "대전광역시",
                "address": "대전광역시 중구 중앙로 101",
                "phone": "042-123-4567",
                "email": "daejeon@sbc.or.kr",
                "website": "https://daejeon.sbc.or.kr",
                "services": ["창업상담", "자금지원", "교육프로그램", "마케팅지원"],
                "operating_hours": "평일 09:00-18:00",
                "specialties": ["창업지원", "자금조달", "경영컨설팅"]
            },
            {
                "id": "center_002",
                "name": "유성구 소상공인지원센터",
                "region": "대전광역시 유성구",
                "address": "대전광역시 유성구 대학로 291",
                "phone": "042-234-5678",
                "email": "yuseong@sbc.or.kr",
                "website": "https://yuseong.sbc.or.kr",
                "services": ["창업상담", "자금지원", "교육프로그램", "기술지원"],
                "operating_hours": "평일 09:00-18:00",
                "specialties": ["기술창업", "R&D지원", "특허상담"]
            },
            {
                "id": "center_003",
                "name": "동구 소상공인지원센터",
                "region": "대전광역시 동구",
                "address": "대전광역시 동구 중앙로 200",
                "phone": "042-345-6789",
                "email": "donggu@sbc.or.kr",
                "website": "https://donggu.sbc.or.kr",
                "services": ["창업상담", "자금지원", "교육프로그램", "마케팅지원"],
                "operating_hours": "평일 09:00-18:00",
                "specialties": ["전통시장활성화", "관광상품개발", "지역특화상품"]
            }
        ]
    
    def _init_policies(self) -> List[Dict[str, Any]]:
        """지원 정책 데이터 초기화"""
        return [
            {
                "id": "policy_001",
                "name": "대전광역시 창업지원금",
                "region": "대전광역시",
                "organization": "대전광역시청",
                "support_amount": "최대 1000만원",
                "support_type": "자금지원",
                "target_business": ["식음료업", "의류업", "생활용품"],
                "target_stage": ["PLANNING", "STARTUP"],
                "target_user": ["ENTREPRENEUR"],
                "application_period": "2024-01-01 ~ 2024-12-31",
                "priority": 95,
                "description": "창업 초기 자금 지원을 위한 정책",
                "requirements": ["사업자등록증", "사업계획서", "재정상태증명서"],
                "contact": "042-123-4567"
            },
            {
                "id": "policy_002",
                "name": "유성구 기술창업 지원사업",
                "region": "대전광역시 유성구",
                "organization": "유성구청",
                "support_amount": "최대 2000만원",
                "support_type": "자금지원",
                "target_business": ["전자제품", "화장품"],
                "target_stage": ["PLANNING", "STARTUP"],
                "target_user": ["ENTREPRENEUR"],
                "application_period": "2024-03-01 ~ 2024-11-30",
                "priority": 90,
                "description": "기술 기반 창업을 위한 지원사업",
                "requirements": ["기술개발계획서", "특허출원서", "사업계획서"],
                "contact": "042-234-5678"
            },
            {
                "id": "policy_003",
                "name": "대전광역시 마케팅 지원사업",
                "region": "대전광역시",
                "organization": "대전광역시청",
                "support_amount": "최대 500만원",
                "support_type": "마케팅지원",
                "target_business": ["식음료업", "의류업", "화장품", "생활용품"],
                "target_stage": ["STARTUP", "GROWTH"],
                "target_user": ["ENTREPRENEUR"],
                "application_period": "2024-02-01 ~ 2024-10-31",
                "priority": 85,
                "description": "온라인 마케팅 및 홍보 지원",
                "requirements": ["마케팅계획서", "사업자등록증", "매출증빙서류"],
                "contact": "042-123-4567"
            },
            {
                "id": "policy_004",
                "name": "동구 전통시장 활성화 지원",
                "region": "대전광역시 동구",
                "organization": "동구청",
                "support_amount": "최대 300만원",
                "support_type": "자금지원",
                "target_business": ["식음료업", "생활용품"],
                "target_stage": ["STARTUP", "GROWTH"],
                "target_user": ["ENTREPRENEUR"],
                "application_period": "2024-04-01 ~ 2024-09-30",
                "priority": 80,
                "description": "전통시장 내 창업 및 사업 확장 지원",
                "requirements": ["전통시장 입점계약서", "사업계획서", "재정상태증명서"],
                "contact": "042-345-6789"
            }
        ]
    
    def _init_experts(self) -> List[Dict[str, Any]]:
        """전문가 데이터 초기화"""
        return [
            {
                "id": "expert_001",
                "name": "김창업",
                "title": "창업컨설턴트",
                "organization": "대전광역시 소상공인지원센터",
                "region": "대전광역시",
                "expertise": ["창업상담", "사업계획서작성", "자금조달"],
                "experience": "15년",
                "specialties": ["식음료업", "의류업"],
                "consultation_available": True,
                "next_available": "2024-01-15 14:00",
                "rating": 4.8,
                "consultation_count": 150
            },
            {
                "id": "expert_002",
                "name": "이마케팅",
                "title": "마케팅전문가",
                "organization": "유성구 소상공인지원센터",
                "region": "대전광역시 유성구",
                "expertise": ["마케팅전략", "SNS마케팅", "브랜딩"],
                "experience": "12년",
                "specialties": ["화장품", "생활용품"],
                "consultation_available": True,
                "next_available": "2024-01-16 10:00",
                "rating": 4.9,
                "consultation_count": 200
            },
            {
                "id": "expert_003",
                "name": "박기술",
                "title": "기술컨설턴트",
                "organization": "대전테크노파크",
                "region": "대전광역시",
                "expertise": ["기술창업", "특허상담", "R&D지원"],
                "experience": "20년",
                "specialties": ["전자제품", "화장품"],
                "consultation_available": True,
                "next_available": "2024-01-17 15:00",
                "rating": 4.7,
                "consultation_count": 120
            }
        ]
    
    def _init_success_cases(self) -> List[Dict[str, Any]]:
        """성공 사례 데이터 초기화"""
        return [
            {
                "id": "case_001",
                "title": "대전역 카페 '커피앤북' 성공 사례",
                "industry": "식음료업",
                "region": "대전광역시 동구",
                "strategy_type": "differentiation",
                "market_code": "10000",
                "challenge": "과포화된 카페 시장에서 차별화 필요",
                "solution": "독서 카페 컨셉으로 전환, 도서 대여 서비스 추가",
                "results": {
                    "revenue_increase": "45%",
                    "customer_retention": "60%",
                    "average_dwell_time": "90분"
                },
                "key_factors": ["독특한 컨셉", "고객 체류시간 연장", "부가 서비스"],
                "duration": "6개월",
                "investment": "500만원",
                "lessons_learned": "차별화된 컨셉이 고객 유치의 핵심",
                "contact_info": "owner@coffeeandbook.com"
            },
            {
                "id": "case_002",
                "title": "유성온천역 의류점 '스타일랩' 성공 사례",
                "industry": "의류업",
                "region": "대전광역시 유성구",
                "strategy_type": "online_expansion",
                "market_code": "20000",
                "challenge": "오프라인 매출 감소, 온라인 진출 필요",
                "solution": "인스타그램 쇼핑몰 구축, 인플루언서 마케팅",
                "results": {
                    "online_revenue": "200%",
                    "total_revenue": "80%",
                    "new_customers": "150%"
                },
                "key_factors": ["SNS 마케팅", "인플루언서 협업", "온라인 쇼핑몰"],
                "duration": "4개월",
                "investment": "300만원",
                "lessons_learned": "온라인 채널 확장이 매출 증대의 핵심",
                "contact_info": "owner@stylelab.com"
            },
            {
                "id": "case_003",
                "title": "중구 화장품점 '뷰티허브' 성공 사례",
                "industry": "화장품",
                "region": "대전광역시 중구",
                "strategy_type": "customer_loyalty",
                "market_code": "30000",
                "challenge": "고객 충성도 부족, 재방문율 저조",
                "solution": "맞춤형 뷰티 컨설팅 서비스, 멤버십 프로그램",
                "results": {
                    "customer_retention": "70%",
                    "average_purchase": "35%",
                    "repeat_customers": "85%"
                },
                "key_factors": ["개인 맞춤 서비스", "멤버십 혜택", "전문 컨설팅"],
                "duration": "3개월",
                "investment": "200만원",
                "lessons_learned": "고객 맞춤 서비스가 충성도 향상의 핵심",
                "contact_info": "owner@beautyhub.com"
            }
        ]
    
    def _is_policy_relevant(self, policy: Dict[str, Any], region: str, business_type: str, user_type: str, business_stage: str) -> bool:
        """정책 관련성 판단"""
        # 지역 매칭
        if region not in policy["region"]:
            return False
        
        # 업종 매칭
        if business_type not in policy["target_business"]:
            return False
        
        # 사용자 유형 매칭
        if user_type not in policy["target_user"]:
            return False
        
        # 사업 단계 매칭
        if business_stage not in policy["target_stage"]:
            return False
        
        return True
    
    def _get_application_guide(self) -> List[Dict[str, Any]]:
        """정책 신청 가이드"""
        return [
            {
                "step": 1,
                "title": "정책 조회 및 검토",
                "description": "본인에게 해당하는 정책을 찾고 자격 요건을 확인합니다.",
                "duration": "1-2일"
            },
            {
                "step": 2,
                "title": "필요 서류 준비",
                "description": "신청에 필요한 서류들을 미리 준비합니다.",
                "duration": "3-7일"
            },
            {
                "step": 3,
                "title": "온라인 신청",
                "description": "정책 담당 기관 홈페이지에서 온라인 신청을 진행합니다.",
                "duration": "1일"
            },
            {
                "step": 4,
                "title": "서류 제출",
                "description": "필요한 서류를 제출하고 심사 결과를 기다립니다.",
                "duration": "7-14일"
            },
            {
                "step": 5,
                "title": "심사 및 선정",
                "description": "심사 과정을 거쳐 선정 여부가 결정됩니다.",
                "duration": "14-30일"
            }
        ]
    
    def _get_deadline_alerts(self, policies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """마감일 알림"""
        alerts = []
        for policy in policies:
            # 마감일이 30일 이내인 정책들
            if "2024-12-31" in policy["application_period"]:  # 임시 로직
                alerts.append({
                    "policy_name": policy["name"],
                    "deadline": "2024-12-31",
                    "days_remaining": 30,
                    "urgency": "high" if 30 <= 7 else "medium"
                })
        return alerts
    
    def _calculate_relevance_score(self, case: Dict[str, Any], industry: str = None, region: str = None, strategy_type: str = None) -> int:
        """성공 사례 관련도 점수 계산"""
        score = 0
        
        if industry and case["industry"] == industry:
            score += 40
        
        if region and region in case["region"]:
            score += 30
        
        if strategy_type and case["strategy_type"] == strategy_type:
            score += 30
        
        return score
    
    def _get_case_categories(self) -> List[Dict[str, Any]]:
        """성공 사례 카테고리"""
        return [
            {"category": "업종별", "count": 5, "description": "업종별 성공 사례"},
            {"category": "지역별", "count": 3, "description": "지역별 성공 사례"},
            {"category": "전략별", "count": 4, "description": "전략별 성공 사례"},
            {"category": "투자규모별", "count": 3, "description": "투자 규모별 성공 사례"}
        ]
