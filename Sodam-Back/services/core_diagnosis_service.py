import os
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import numpy as np
from .data_loader import DataLoader

class CoreDiagnosisService:
    """상권 진단 핵심 지표 분석 서비스"""
    
    def __init__(self):
        self.data_loader = DataLoader()
        # 실제 데이터를 사용하므로 샘플 데이터 제거
        # self.sample_data = self._init_sample_data()
        
        # 실제 데이터와 일치하는 카테고리 정의
        self.categories = {
            "쇼핑업": {
                "관광기념품": {"weight": 0.8, "traffic_factor": 1.2, "competition_factor": 0.9},
                "대형쇼핑몰": {"weight": 1.3, "traffic_factor": 1.4, "competition_factor": 1.2},
                "레저용품쇼핑": {"weight": 1.0, "traffic_factor": 1.1, "competition_factor": 1.0}
            },
            "숙박업": {
                "기타숙박": {"weight": 1.0, "traffic_factor": 0.8, "competition_factor": 0.9},
                "캠핑장/펜션": {"weight": 0.7, "traffic_factor": 0.6, "competition_factor": 0.8},
                "콘도": {"weight": 0.8, "traffic_factor": 0.7, "competition_factor": 0.8},
                "호텔": {"weight": 1.2, "traffic_factor": 1.0, "competition_factor": 0.9}
            },
            "식음료업": {
                "식음료": {"weight": 1.2, "traffic_factor": 1.3, "competition_factor": 1.1}
            },
            "여가서비스업": {
                "골프장": {"weight": 0.9, "traffic_factor": 0.7, "competition_factor": 0.8},
                "관광유원시설": {"weight": 1.1, "traffic_factor": 1.2, "competition_factor": 1.0},
                "기타레저": {"weight": 1.0, "traffic_factor": 1.0, "competition_factor": 1.0},
                "문화서비스": {"weight": 1.0, "traffic_factor": 0.9, "competition_factor": 1.0}
            },
            "여행업": {
                "여행업": {"weight": 1.0, "traffic_factor": 0.8, "competition_factor": 1.0}
            },
            "운송업": {
                "렌터카": {"weight": 0.8, "traffic_factor": 0.7, "competition_factor": 0.9},
                "수상운송": {"weight": 0.7, "traffic_factor": 0.6, "competition_factor": 0.8},
                "육상운송": {"weight": 1.1, "traffic_factor": 1.0, "competition_factor": 1.0}
            }
        }
    
    def _get_market_adjustment(self, market_code: str) -> float:
        """상권 코드에 따른 조정 계수 반환"""
        # 상권 코드의 해시값을 기반으로 일관된 조정 계수 생성
        hash_value = hash(market_code) % 1000
        # 0.5 ~ 1.5 범위의 조정 계수
        adjustment = 0.5 + (hash_value / 1000) * 1.0
        return adjustment
    
    def _get_category_info(self, category: str, sub_category: str = None) -> dict:
        """카테고리 정보 조회"""
        if not category or category == "전체":
            return {"weight": 1.0, "traffic_factor": 1.0, "competition_factor": 1.0}
        
        if category in self.categories:
            if sub_category and sub_category in self.categories[category]:
                return self.categories[category][sub_category]
            else:
                # 하위 카테고리가 없으면 상위 카테고리의 평균값 사용
                sub_categories = self.categories[category]
                avg_weight = sum(info["weight"] for info in sub_categories.values()) / len(sub_categories)
                avg_traffic = sum(info["traffic_factor"] for info in sub_categories.values()) / len(sub_categories)
                avg_competition = sum(info["competition_factor"] for info in sub_categories.values()) / len(sub_categories)
                return {"weight": avg_weight, "traffic_factor": avg_traffic, "competition_factor": avg_competition}
        
        # 기본값
        return {"weight": 1.0, "traffic_factor": 1.0, "competition_factor": 1.0}
    
    def get_foot_traffic_analysis(self, market_code: str, industry: str = None, period_months: int = 12) -> Dict[str, Any]:
        """유동인구 변화량 분석 - 위치별, 업종별 실제 데이터 사용"""
        try:
            # 상권 정보에서 지역 추출
            market_info = self.data_loader.get_market_by_code(market_code)
            if not market_info:
                return {"error": "상권 정보를 가져올 수 없습니다."}
            
            region = market_info.get('city_name', '대전광역시')
            
            # 업종별 관광 데이터 사용
            if industry and industry != "전체":
                tourism_data = self.data_loader.get_tourism_trend_by_industry(region, industry)
            else:
                tourism_data = self.data_loader.get_tourism_trend(region)
            
            if not tourism_data:
                return {"error": "관광 소비 데이터를 가져올 수 없습니다."}
            
            # 최근 N개월 데이터 추출
            recent_data = tourism_data[-period_months:] if len(tourism_data) >= period_months else tourism_data
            
            # 소비액을 유동인구 지표로 변환 (소비액이 높을수록 유동인구가 많다고 가정)
            base_values = [float(data['consumption_amount']) for data in recent_data]
            months = [data['year_month'] for data in recent_data]
            
            # 지역별 지출 비율 적용
            regional_ratio = self.data_loader.get_regional_ratio_by_region(region)
            regional_adjustment = regional_ratio / 100.0 if regional_ratio > 0 else 1.0
            
            # 업종별 가중치 적용
            industry_weight = 1.0
            if industry and industry != "전체":
                industry_ratio = self.data_loader.get_industry_ratio_by_category(industry)
                industry_weight = industry_ratio.get('major_ratio', 1.0) / 100.0 if industry_ratio.get('major_ratio', 0) > 0 else 1.0
            
            # 최종 조정된 값
            values = [v * regional_adjustment * industry_weight for v in base_values]
            
            # 변화량 계산
            if len(values) >= 2:
                monthly_changes = []
                for i in range(1, len(values)):
                    change = ((values[i] - values[i-1]) / values[i-1]) * 100
                    monthly_changes.append(change)
                
                avg_monthly_change = np.mean(monthly_changes)
                total_change = ((values[-1] - values[0]) / values[0]) * 100
                trend = "증가" if avg_monthly_change > 0 else "감소"
            else:
                avg_monthly_change = 0
                total_change = 0
                trend = "안정"
            
            # 등급 산정
            if avg_monthly_change > 5:
                grade = "A"
            elif avg_monthly_change > 0:
                grade = "B"
            elif avg_monthly_change > -5:
                grade = "C"
            else:
                grade = "D"
            
            return {
                "market_code": market_code,
                "current_monthly_traffic": int(values[-1] / 1000),  # 천원 단위로 변환
                "average_monthly_change": round(avg_monthly_change, 2),
                "total_change_period": round(total_change, 2),
                "trend": trend,
                "grade": grade,
                "monthly_data": [
                    {"month": month, "traffic": int(value / 1000)} 
                    for month, value in zip(months, values)
                ],
                "analysis": self._get_foot_traffic_analysis_text(avg_monthly_change, grade)
            }
        except Exception as e:
            return {"error": f"유동인구 분석 중 오류가 발생했습니다: {str(e)}"}
    
    def get_card_sales_analysis(self, market_code: str, industry: str = None, period_months: int = 12) -> Dict[str, Any]:
        """카드매출 추이 분석 - 위치별, 업종별 실제 데이터 사용"""
        try:
            # 상권 정보에서 지역 추출
            market_info = self.data_loader.get_market_by_code(market_code)
            if not market_info:
                return {"error": "상권 정보를 가져올 수 없습니다."}
            
            region = market_info.get('city_name', '대전광역시')
            
            # 업종별 관광 데이터 사용
            if industry and industry != "전체":
                tourism_data = self.data_loader.get_tourism_trend_by_industry(region, industry)
            else:
                tourism_data = self.data_loader.get_tourism_trend(region)
            
            if not tourism_data:
                return {"error": "관광 소비 데이터를 가져올 수 없습니다."}
            
            # 최근 N개월 데이터 추출
            recent_data = tourism_data[-period_months:] if len(tourism_data) >= period_months else tourism_data
            
            # 소비액을 카드매출로 사용
            base_values = [float(data['consumption_amount']) for data in recent_data]
            months = [data['year_month'] for data in recent_data]
            
            # 지역별 지출 비율 적용
            regional_ratio = self.data_loader.get_regional_ratio_by_region(region)
            regional_adjustment = regional_ratio / 100.0 if regional_ratio > 0 else 1.0
            
            # 업종별 가중치 적용
            industry_weight = 1.0
            if industry and industry != "전체":
                industry_ratio = self.data_loader.get_industry_ratio_by_category(industry)
                industry_weight = industry_ratio.get('major_ratio', 1.0) / 100.0 if industry_ratio.get('major_ratio', 0) > 0 else 1.0
            
            # 최종 조정된 값
            values = [v * regional_adjustment * industry_weight for v in base_values]
            
            # 변화량 계산
            if len(values) >= 2:
                monthly_changes = []
                for i in range(1, len(values)):
                    change = ((values[i] - values[i-1]) / values[i-1]) * 100
                    monthly_changes.append(change)
                
                avg_monthly_change = np.mean(monthly_changes)
                total_change = ((values[-1] - values[0]) / values[0]) * 100
                trend = "증가" if avg_monthly_change > 0 else "감소"
            else:
                avg_monthly_change = 0
                total_change = 0
                trend = "안정"
            
            # 등급 산정
            if avg_monthly_change > 3:
                grade = "A"
            elif avg_monthly_change > 0:
                grade = "B"
            elif avg_monthly_change > -3:
                grade = "C"
            else:
                grade = "D"
            
            return {
                "market_code": market_code,
                "current_monthly_sales": int(values[-1]),
                "average_monthly_change": round(avg_monthly_change, 2),
                "total_change_period": round(total_change, 2),
                "trend": trend,
                "grade": grade,
                "monthly_data": [
                    {"month": month, "sales": int(value)} 
                    for month, value in zip(months, values)
                ],
                "analysis": self._get_card_sales_analysis_text(avg_monthly_change, grade)
            }
        except Exception as e:
            return {"error": f"카드매출 분석 중 오류가 발생했습니다: {str(e)}"}
    
    def get_same_industry_analysis(self, market_code: str, industry: str = None) -> Dict[str, Any]:
        """동일업종 수 분석"""
        try:
            # 실제 업종별 지출액 데이터 사용
            industry_data = self.data_loader.get_industry_ratios()
            
            if not industry_data:
                return {"error": "업종별 데이터를 가져올 수 없습니다."}
            
            if industry:
                # 특정 업종 분석
                matching_industry = None
                for data in industry_data:
                    if data['minor_category'] == industry or data['major_category'] == industry:
                        matching_industry = data
                        break
                
                if not matching_industry:
                    return {"error": f"해당 업종 '{industry}'의 데이터를 찾을 수 없습니다."}
                
                ratio = matching_industry['minor_ratio']
                
                # 경쟁도 등급 (지출액 비율이 높을수록 경쟁이 치열)
                if ratio > 30:
                    competition_level = "매우 높음"
                    grade = "D"
                elif ratio > 20:
                    competition_level = "높음"
                    grade = "C"
                elif ratio > 10:
                    competition_level = "보통"
                    grade = "B"
                else:
                    competition_level = "낮음"
                    grade = "A"
                
                return {
                    "market_code": market_code,
                    "industry": industry,
                    "business_count": int(ratio * 10),  # 추정 사업체 수
                    "total_businesses": 100,  # 전체 사업체 수 (추정)
                    "industry_ratio": round(ratio, 2),
                    "competition_level": competition_level,
                    "grade": grade,
                    "analysis": self._get_competition_analysis_text(ratio, competition_level)
                }
            else:
                # 전체 업종 분석
                return {
                    "market_code": market_code,
                    "industry_breakdown": {data['minor_category']: data['minor_ratio'] for data in industry_data},
                    "total_businesses": 100,  # 전체 사업체 수 (추정)
                    "analysis": "전체 업종별 지출액 비율 현황입니다."
                }
        except Exception as e:
            return {"error": f"동일업종 분석 중 오류가 발생했습니다: {str(e)}"}
    
    def get_business_rates_analysis(self, market_code: str) -> Dict[str, Any]:
        """창업·폐업 비율 분석"""
        try:
            # 관광 소비 데이터의 변동성을 기반으로 창업·폐업 비율 추정
            tourism_data = self.data_loader.get_tourism_trend()
            
            if not tourism_data:
                return {"error": "관광 소비 데이터를 가져올 수 없습니다."}
            
            # 최근 12개월 데이터의 변동성 계산
            recent_data = tourism_data[-12:] if len(tourism_data) >= 12 else tourism_data
            values = [float(data['consumption_amount']) for data in recent_data]
            
            # 변동성 기반으로 창업·폐업 비율 추정
            if len(values) >= 2:
                # 변동성 계산 (표준편차)
                std_dev = np.std(values)
                mean_value = np.mean(values)
                coefficient_of_variation = (std_dev / mean_value) * 100
                
                # 상권별 조정 계수 적용
                market_adjustment = self._get_market_adjustment(market_code)
                
                # 변동성이 높을수록 창업·폐업이 활발하다고 가정
                startup_rate = min(coefficient_of_variation * 0.5 * market_adjustment, 20)  # 최대 20%
                closure_rate = min(coefficient_of_variation * 0.3 * market_adjustment, 15)  # 최대 15%
                survival_rate = max(100 - closure_rate, 70)  # 최소 70%
            else:
                # 기본값 (상권별 조정 적용)
                market_adjustment = self._get_market_adjustment(market_code)
                startup_rate = 12.0 * market_adjustment
                closure_rate = 8.0 * market_adjustment
                survival_rate = max(100 - closure_rate, 70)
            
            # 종합 등급 산정
            startup_score = min(startup_rate / 15 * 100, 100)  # 15% 이상이면 100점
            closure_score = max(100 - closure_rate / 10 * 100, 0)  # 10% 이상이면 0점
            survival_score = survival_rate
            
            total_score = (startup_score * 0.3 + closure_score * 0.3 + survival_score * 0.4)
            
            if total_score >= 90:
                grade = "A"
                health_status = "매우 양호"
            elif total_score >= 80:
                grade = "B"
                health_status = "양호"
            elif total_score >= 70:
                grade = "C"
                health_status = "보통"
            else:
                grade = "D"
                health_status = "우려"
            
            return {
                "market_code": market_code,
                "startup_rate": round(startup_rate, 2),
                "closure_rate": round(closure_rate, 2),
                "survival_rate": round(survival_rate, 2),
                "total_score": round(total_score, 2),
                "grade": grade,
                "health_status": health_status,
                "analysis": self._get_business_rates_analysis_text(total_score, health_status)
            }
        except Exception as e:
            return {"error": f"창업·폐업 비율 분석 중 오류가 발생했습니다: {str(e)}"}
    
    def get_dwell_time_analysis(self, market_code: str) -> Dict[str, Any]:
        """체류시간 분석"""
        try:
            # 관광 소비 데이터의 패턴을 기반으로 체류시간 추정
            tourism_data = self.data_loader.get_tourism_trend()
            
            if not tourism_data:
                return {"error": "관광 소비 데이터를 가져올 수 없습니다."}
            
            # 최근 12개월 데이터 분석
            recent_data = tourism_data[-12:] if len(tourism_data) >= 12 else tourism_data
            values = [float(data['consumption_amount']) for data in recent_data]
            
            # 소비액 패턴을 기반으로 체류시간 추정
            if len(values) >= 2:
                # 소비액의 안정성을 체류시간 지표로 사용
                mean_value = np.mean(values)
                std_dev = np.std(values)
                stability = 1 - (std_dev / mean_value)  # 안정성 지수 (0-1)
                
                # 상권별 조정 계수 적용
                market_adjustment = self._get_market_adjustment(market_code)
                
                # 안정성이 높을수록 체류시간이 길다고 가정
                base_time = 30 + (stability * 30)  # 30-60분 범위
                avg_time = base_time * market_adjustment  # 상권별 조정
            else:
                # 기본값 (상권별 조정 적용)
                market_adjustment = self._get_market_adjustment(market_code)
                avg_time = 45 * market_adjustment
            
            # 체류시간 등급 산정
            if avg_time >= 60:
                grade = "A"
                time_quality = "매우 우수"
            elif avg_time >= 45:
                grade = "B"
                time_quality = "우수"
            elif avg_time >= 30:
                grade = "C"
                time_quality = "보통"
            else:
                grade = "D"
                time_quality = "부족"
            
            return {
                "market_code": market_code,
                "average_dwell_time": round(avg_time, 1),
                "peak_hours": ["12:00-14:00", "18:00-20:00"],  # 기본 피크 시간
                "weekend_ratio": 1.3,  # 기본 주말 비율
                "grade": grade,
                "time_quality": time_quality,
                "analysis": self._get_dwell_time_analysis_text(avg_time, time_quality)
            }
        except Exception as e:
            return {"error": f"체류시간 분석 중 오류가 발생했습니다: {str(e)}"}
    
    def calculate_health_score(self, market_code: str, industry: str = None, category: str = None, sub_category: str = None) -> Dict[str, Any]:
        """상권 건강 점수 종합 산정 - 카테고리 정보 활용"""
        # 카테고리 정보 조회
        category_info = self._get_category_info(category, sub_category)
        
        # 각 지표별 점수 계산 (industry 파라미터 전달)
        foot_traffic = self.get_foot_traffic_analysis(market_code, industry)
        card_sales = self.get_card_sales_analysis(market_code, industry)
        business_rates = self.get_business_rates_analysis(market_code)
        dwell_time = self.get_dwell_time_analysis(market_code)
        
        # 에러 체크
        if "error" in foot_traffic or "error" in card_sales or "error" in business_rates or "error" in dwell_time:
            return {"error": "일부 데이터를 가져올 수 없습니다."}
        
        # 동일업종 분석 (업종이 지정된 경우)
        same_industry = None
        if industry:
            same_industry = self.get_same_industry_analysis(market_code, industry)
            if "error" in same_industry:
                same_industry = None
        
        # 점수 변환 (A=100, B=80, C=60, D=40)
        grade_scores = {"A": 100, "B": 80, "C": 60, "D": 40}
        
        # 기본 점수 계산
        foot_traffic_score = grade_scores.get(foot_traffic["grade"], 60)
        card_sales_score = grade_scores.get(card_sales["grade"], 60)
        business_rates_score = business_rates["total_score"]
        dwell_time_score = grade_scores.get(dwell_time["grade"], 60)
        
        # 카테고리별 가중치 적용
        foot_traffic_score *= category_info["traffic_factor"]
        card_sales_score *= category_info["weight"]
        business_rates_score *= category_info["weight"]
        dwell_time_score *= category_info["weight"]
        
        # 가중치 적용
        weights = {
            "foot_traffic": 0.25,
            "card_sales": 0.25,
            "business_rates": 0.25,
            "dwell_time": 0.15,
            "competition": 0.10
        }
        
        total_score = (
            foot_traffic_score * weights["foot_traffic"] +
            card_sales_score * weights["card_sales"] +
            business_rates_score * weights["business_rates"] +
            dwell_time_score * weights["dwell_time"]
        )
        
        # 경쟁도 점수 추가 (업종이 지정된 경우)
        if same_industry:
            competition_score = grade_scores.get(same_industry["grade"], 60)
            competition_score *= category_info["competition_factor"]  # 카테고리별 경쟁도 가중치 적용
            total_score += competition_score * weights["competition"]
        else:
            total_score = total_score / (1 - weights["competition"])  # 가중치 재조정
        
        # 최종 등급 산정
        if total_score >= 90:
            final_grade = "A"
            health_status = "매우 건강"
        elif total_score >= 80:
            final_grade = "B"
            health_status = "건강"
        elif total_score >= 70:
            final_grade = "C"
            health_status = "보통"
        elif total_score >= 60:
            final_grade = "D"
            health_status = "주의"
        else:
            final_grade = "F"
            health_status = "위험"
        
        return {
            "market_code": market_code,
            "industry": industry,
            "total_score": round(total_score, 2),
            "final_grade": final_grade,
            "health_status": health_status,
            "score_breakdown": {
                "foot_traffic": {
                    "score": foot_traffic_score,
                    "grade": foot_traffic["grade"],
                    "weight": weights["foot_traffic"]
                },
                "card_sales": {
                    "score": card_sales_score,
                    "grade": card_sales["grade"],
                    "weight": weights["card_sales"]
                },
                "business_rates": {
                    "score": business_rates_score,
                    "grade": business_rates["grade"],
                    "weight": weights["business_rates"]
                },
                "dwell_time": {
                    "score": dwell_time_score,
                    "grade": dwell_time["grade"],
                    "weight": weights["dwell_time"]
                }
            },
            "detailed_analysis": {
                "foot_traffic": foot_traffic,
                "card_sales": card_sales,
                "business_rates": business_rates,
                "dwell_time": dwell_time,
                "same_industry": same_industry
            },
            "recommendations": self._get_health_score_recommendations(total_score, final_grade)
        }
    
    def _get_foot_traffic_analysis_text(self, change_rate: float, grade: str) -> str:
        """유동인구 분석 텍스트 생성"""
        if grade == "A":
            return f"유동인구가 월평균 {change_rate:.1f}% 증가하여 매우 활발한 상권입니다."
        elif grade == "B":
            return f"유동인구가 월평균 {change_rate:.1f}% 증가하여 양호한 성장세를 보입니다."
        elif grade == "C":
            return f"유동인구가 월평균 {change_rate:.1f}% 변화하여 안정적인 상태입니다."
        else:
            return f"유동인구가 월평균 {change_rate:.1f}% 감소하여 주의가 필요합니다."
    
    def _get_card_sales_analysis_text(self, change_rate: float, grade: str) -> str:
        """카드매출 분석 텍스트 생성"""
        if grade == "A":
            return f"카드매출이 월평균 {change_rate:.1f}% 증가하여 소비활동이 매우 활발합니다."
        elif grade == "B":
            return f"카드매출이 월평균 {change_rate:.1f}% 증가하여 양호한 소비 트렌드를 보입니다."
        elif grade == "C":
            return f"카드매출이 월평균 {change_rate:.1f}% 변화하여 안정적인 소비 패턴입니다."
        else:
            return f"카드매출이 월평균 {change_rate:.1f}% 감소하여 소비력 저하가 우려됩니다."
    
    def _get_competition_analysis_text(self, ratio: float, level: str) -> str:
        """경쟁도 분석 텍스트 생성"""
        if level == "매우 높음":
            return f"동일업종 비율이 {ratio:.1f}%로 경쟁이 매우 치열합니다. 차별화 전략이 필수입니다."
        elif level == "높음":
            return f"동일업종 비율이 {ratio:.1f}%로 경쟁이 치열한 편입니다. 차별화가 필요합니다."
        elif level == "보통":
            return f"동일업종 비율이 {ratio:.1f}%로 적당한 경쟁 수준입니다."
        else:
            return f"동일업종 비율이 {ratio:.1f}%로 경쟁이 낮아 진입 기회가 좋습니다."
    
    def _get_business_rates_analysis_text(self, score: float, status: str) -> str:
        """창업·폐업 비율 분석 텍스트 생성"""
        if status == "매우 양호":
            return f"창업·폐업 비율이 매우 양호하여 상권 활력이 높습니다."
        elif status == "양호":
            return f"창업·폐업 비율이 양호하여 상권이 안정적으로 성장하고 있습니다."
        elif status == "보통":
            return f"창업·폐업 비율이 보통 수준으로 상권이 안정적입니다."
        else:
            return f"창업·폐업 비율에 우려가 있어 상권 활력 제고가 필요합니다."
    
    def _get_dwell_time_analysis_text(self, avg_time: float, quality: str) -> str:
        """체류시간 분석 텍스트 생성"""
        if quality == "매우 우수":
            return f"평균 체류시간이 {avg_time}분으로 매우 우수하여 고객 만족도가 높습니다."
        elif quality == "우수":
            return f"평균 체류시간이 {avg_time}분으로 우수한 편입니다."
        elif quality == "보통":
            return f"평균 체류시간이 {avg_time}분으로 보통 수준입니다."
        else:
            return f"평균 체류시간이 {avg_time}분으로 부족하여 고객 유치 전략이 필요합니다."
    
    def _get_health_score_recommendations(self, score: float, grade: str) -> List[str]:
        """건강 점수 기반 추천사항 생성"""
        recommendations = []
        
        if grade in ["A", "B"]:
            recommendations.extend([
                "현재 상권 상태가 양호합니다. 지속적인 모니터링을 권장합니다.",
                "기존 고객 유지와 신규 고객 확보에 집중하세요.",
                "상권 내 경쟁력을 유지하기 위한 차별화 전략을 수립하세요."
            ])
        elif grade == "C":
            recommendations.extend([
                "상권 상태가 보통 수준입니다. 개선 여지가 있습니다.",
                "유동인구 증가를 위한 마케팅 전략을 검토하세요.",
                "고객 체류시간 연장을 위한 서비스 개선을 고려하세요."
            ])
        else:
            recommendations.extend([
                "상권 상태에 주의가 필요합니다. 신중한 진입을 권장합니다.",
                "상권 활성화 방안을 면밀히 검토하세요.",
                "대안 상권 검토를 권장합니다."
            ])
        
        return recommendations
