import os
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import numpy as np
import math

class MapVisualizationService:
    """지도 기반 시각화 서비스"""
    
    def __init__(self):
        self.data_loader = None
        self.sample_market_data = self._init_sample_market_data()
        self.analysis_cache = {}
    
    def get_market_heatmap_data(self, region: str = None, analysis_type: str = "health_score") -> Dict[str, Any]:
        """상권 히트맵 데이터 생성"""
        
        # 분석 유형별 데이터 생성
        if analysis_type == "health_score":
            return self._generate_health_score_heatmap(region)
        elif analysis_type == "foot_traffic":
            return self._generate_foot_traffic_heatmap(region)
        elif analysis_type == "competition":
            return self._generate_competition_heatmap(region)
        elif analysis_type == "growth_potential":
            return self._generate_growth_potential_heatmap(region)
        else:
            return {"error": "지원하지 않는 분석 유형입니다."}
    
    def get_radius_analysis(self, center_lat: float, center_lng: float, radius_km: float, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """반경별 분석 결과"""
        
        # 반경 내 상권 찾기
        nearby_markets = self._find_markets_in_radius(center_lat, center_lng, radius_km)
        
        if not nearby_markets:
            return {"error": "반경 내 상권이 없습니다."}
        
        # 분석 유형별 결과 생성
        if analysis_type == "comprehensive":
            return self._generate_comprehensive_radius_analysis(nearby_markets, center_lat, center_lng, radius_km)
        elif analysis_type == "competition":
            return self._generate_competition_radius_analysis(nearby_markets, center_lat, center_lng, radius_km)
        elif analysis_type == "opportunity":
            return self._generate_opportunity_radius_analysis(nearby_markets, center_lat, center_lng, radius_km)
        else:
            return {"error": "지원하지 않는 분석 유형입니다."}
    
    def get_market_cluster_analysis(self, region: str = None, cluster_type: str = "performance") -> Dict[str, Any]:
        """상권 클러스터 분석"""
        
        markets = self._get_markets_by_region(region)
        
        if cluster_type == "performance":
            return self._cluster_by_performance(markets)
        elif cluster_type == "characteristics":
            return self._cluster_by_characteristics(markets)
        elif cluster_type == "growth_stage":
            return self._cluster_by_growth_stage(markets)
        else:
            return {"error": "지원하지 않는 클러스터 유형입니다."}
    
    def get_traffic_flow_analysis(self, market_code: str, time_period: str = "daily") -> Dict[str, Any]:
        """유동인구 흐름 분석"""
        
        # 시간대별 유동인구 데이터 생성
        traffic_data = self._generate_traffic_flow_data(market_code, time_period)
        
        return {
            "market_code": market_code,
            "time_period": time_period,
            "traffic_flow": traffic_data,
            "peak_hours": self._identify_peak_hours(traffic_data),
            "flow_patterns": self._analyze_flow_patterns(traffic_data),
            "recommendations": self._get_traffic_recommendations(traffic_data)
        }
    
    def get_accessibility_analysis(self, market_code: str) -> Dict[str, Any]:
        """접근성 분석"""
        
        market_info = self._get_market_info(market_code)
        if not market_info:
            return {"error": "상권 정보를 찾을 수 없습니다."}
        
        # 교통편 분석
        transportation = self._analyze_transportation(market_info)
        
        # 주차 시설 분석
        parking = self._analyze_parking(market_info)
        
        # 보행자 접근성 분석
        pedestrian = self._analyze_pedestrian_access(market_info)
        
        # 종합 접근성 점수 계산
        accessibility_score = self._calculate_accessibility_score(transportation, parking, pedestrian)
        
        return {
            "market_code": market_code,
            "accessibility_score": accessibility_score,
            "transportation": transportation,
            "parking": parking,
            "pedestrian": pedestrian,
            "improvement_suggestions": self._get_accessibility_improvements(accessibility_score, transportation, parking, pedestrian)
        }
    
    def _init_sample_market_data(self) -> List[Dict[str, Any]]:
        """샘플 상권 데이터 초기화"""
        return [
            {
                "market_code": "10000",
                "market_name": "대전역 상권",
                "region": "대전광역시 동구",
                "lat": 36.3316,
                "lng": 127.4342,
                "health_score": 85.5,
                "foot_traffic": 195000,
                "competition_level": "high",
                "growth_potential": 80,
                "market_type": "주요상권"
            },
            {
                "market_code": "20000",
                "market_name": "유성온천역 상권",
                "region": "대전광역시 유성구",
                "lat": 36.3536,
                "lng": 127.3450,
                "health_score": 78.2,
                "foot_traffic": 142000,
                "competition_level": "medium",
                "growth_potential": 75,
                "market_type": "주요상권"
            },
            {
                "market_code": "30000",
                "market_name": "중구 상권",
                "region": "대전광역시 중구",
                "lat": 36.3250,
                "lng": 127.4200,
                "health_score": 72.8,
                "foot_traffic": 125000,
                "competition_level": "medium",
                "growth_potential": 70,
                "market_type": "일반상권"
            },
            {
                "market_code": "40000",
                "market_name": "서구 상권",
                "region": "대전광역시 서구",
                "lat": 36.3500,
                "lng": 127.3800,
                "health_score": 68.5,
                "foot_traffic": 98000,
                "competition_level": "low",
                "growth_potential": 65,
                "market_type": "일반상권"
            },
            {
                "market_code": "50000",
                "market_name": "대덕구 상권",
                "region": "대전광역시 대덕구",
                "lat": 36.3800,
                "lng": 127.4500,
                "health_score": 75.3,
                "foot_traffic": 110000,
                "competition_level": "low",
                "growth_potential": 85,
                "market_type": "일반상권"
            }
        ]
    
    def _generate_health_score_heatmap(self, region: str = None) -> Dict[str, Any]:
        """건강 점수 히트맵 데이터 생성"""
        markets = self._get_markets_by_region(region)
        
        heatmap_data = []
        for market in markets:
            # 점수에 따른 색상 결정
            score = market["health_score"]
            if score >= 80:
                color = "#00FF00"  # 녹색
                intensity = 1.0
            elif score >= 70:
                color = "#FFFF00"  # 노란색
                intensity = 0.8
            elif score >= 60:
                color = "#FFA500"  # 주황색
                intensity = 0.6
            else:
                color = "#FF0000"  # 빨간색
                intensity = 0.4
            
            heatmap_data.append({
                "lat": market["lat"],
                "lng": market["lng"],
                "intensity": intensity,
                "color": color,
                "market_code": market["market_code"],
                "market_name": market["market_name"],
                "health_score": score,
                "grade": self._get_grade_from_score(score)
            })
        
        return {
            "analysis_type": "health_score",
            "region": region,
            "total_markets": len(heatmap_data),
            "heatmap_data": heatmap_data,
            "legend": {
                "high": {"color": "#00FF00", "range": "80-100", "description": "매우 건강"},
                "medium": {"color": "#FFFF00", "range": "70-79", "description": "건강"},
                "low": {"color": "#FFA500", "range": "60-69", "description": "보통"},
                "poor": {"color": "#FF0000", "range": "0-59", "description": "주의"}
            }
        }
    
    def _generate_foot_traffic_heatmap(self, region: str = None) -> Dict[str, Any]:
        """유동인구 히트맵 데이터 생성"""
        markets = self._get_markets_by_region(region)
        
        # 유동인구 최대값으로 정규화
        max_traffic = max(market["foot_traffic"] for market in markets)
        
        heatmap_data = []
        for market in markets:
            # 유동인구에 따른 강도 계산
            intensity = market["foot_traffic"] / max_traffic
            
            heatmap_data.append({
                "lat": market["lat"],
                "lng": market["lng"],
                "intensity": intensity,
                "market_code": market["market_code"],
                "market_name": market["market_name"],
                "foot_traffic": market["foot_traffic"],
                "traffic_level": self._get_traffic_level(market["foot_traffic"])
            })
        
        return {
            "analysis_type": "foot_traffic",
            "region": region,
            "total_markets": len(heatmap_data),
            "heatmap_data": heatmap_data,
            "max_traffic": max_traffic
        }
    
    def _generate_competition_heatmap(self, region: str = None) -> Dict[str, Any]:
        """경쟁도 히트맵 데이터 생성"""
        markets = self._get_markets_by_region(region)
        
        heatmap_data = []
        for market in markets:
            # 경쟁도에 따른 색상 결정
            competition = market["competition_level"]
            if competition == "high":
                color = "#FF0000"
                intensity = 1.0
            elif competition == "medium":
                color = "#FFA500"
                intensity = 0.6
            else:
                color = "#00FF00"
                intensity = 0.3
            
            heatmap_data.append({
                "lat": market["lat"],
                "lng": market["lng"],
                "intensity": intensity,
                "color": color,
                "market_code": market["market_code"],
                "market_name": market["market_name"],
                "competition_level": competition
            })
        
        return {
            "analysis_type": "competition",
            "region": region,
            "total_markets": len(heatmap_data),
            "heatmap_data": heatmap_data
        }
    
    def _generate_growth_potential_heatmap(self, region: str = None) -> Dict[str, Any]:
        """성장 잠재력 히트맵 데이터 생성"""
        markets = self._get_markets_by_region(region)
        
        heatmap_data = []
        for market in markets:
            # 성장 잠재력에 따른 강도 계산
            potential = market["growth_potential"]
            intensity = potential / 100
            
            heatmap_data.append({
                "lat": market["lat"],
                "lng": market["lng"],
                "intensity": intensity,
                "market_code": market["market_code"],
                "market_name": market["market_name"],
                "growth_potential": potential,
                "potential_level": self._get_potential_level(potential)
            })
        
        return {
            "analysis_type": "growth_potential",
            "region": region,
            "total_markets": len(heatmap_data),
            "heatmap_data": heatmap_data
        }
    
    def _find_markets_in_radius(self, center_lat: float, center_lng: float, radius_km: float) -> List[Dict[str, Any]]:
        """반경 내 상권 찾기"""
        nearby_markets = []
        
        for market in self.sample_market_data:
            distance = self._calculate_distance(center_lat, center_lng, market["lat"], market["lng"])
            if distance <= radius_km:
                market["distance_km"] = round(distance, 2)
                nearby_markets.append(market)
        
        return nearby_markets
    
    def _generate_comprehensive_radius_analysis(self, markets: List[Dict[str, Any]], center_lat: float, center_lng: float, radius_km: float) -> Dict[str, Any]:
        """종합 반경 분석"""
        
        # 기본 통계
        total_markets = len(markets)
        avg_health_score = sum(m["health_score"] for m in markets) / total_markets
        avg_foot_traffic = sum(m["foot_traffic"] for m in markets) / total_markets
        
        # 경쟁도 분석
        competition_levels = [m["competition_level"] for m in markets]
        competition_distribution = {
            "high": competition_levels.count("high"),
            "medium": competition_levels.count("medium"),
            "low": competition_levels.count("low")
        }
        
        # 성장 잠재력 분석
        growth_potentials = [m["growth_potential"] for m in markets]
        avg_growth_potential = sum(growth_potentials) / len(growth_potentials)
        
        # 추천 상권 (건강 점수 기준 상위 3개)
        top_markets = sorted(markets, key=lambda x: x["health_score"], reverse=True)[:3]
        
        return {
            "center": {"lat": center_lat, "lng": center_lng},
            "radius_km": radius_km,
            "analysis_summary": {
                "total_markets": total_markets,
                "average_health_score": round(avg_health_score, 2),
                "average_foot_traffic": round(avg_foot_traffic),
                "average_growth_potential": round(avg_growth_potential, 2)
            },
            "competition_analysis": {
                "distribution": competition_distribution,
                "dominant_level": max(competition_distribution, key=competition_distribution.get),
                "competition_intensity": self._calculate_competition_intensity(competition_distribution)
            },
            "recommended_markets": [
                {
                    "market_code": m["market_code"],
                    "market_name": m["market_name"],
                    "health_score": m["health_score"],
                    "distance_km": m["distance_km"],
                    "reason": f"건강 점수 {m['health_score']}점으로 우수"
                }
                for m in top_markets
            ],
            "market_opportunities": self._identify_market_opportunities(markets),
            "risk_factors": self._identify_risk_factors(markets)
        }
    
    def _generate_competition_radius_analysis(self, markets: List[Dict[str, Any]], center_lat: float, center_lng: float, radius_km: float) -> Dict[str, Any]:
        """경쟁도 반경 분석"""
        
        # 경쟁도별 상권 분류
        high_competition = [m for m in markets if m["competition_level"] == "high"]
        medium_competition = [m for m in markets if m["competition_level"] == "medium"]
        low_competition = [m for m in markets if m["competition_level"] == "low"]
        
        return {
            "center": {"lat": center_lat, "lng": center_lng},
            "radius_km": radius_km,
            "competition_analysis": {
                "high_competition": {
                    "count": len(high_competition),
                    "markets": [{"name": m["market_name"], "score": m["health_score"]} for m in high_competition]
                },
                "medium_competition": {
                    "count": len(medium_competition),
                    "markets": [{"name": m["market_name"], "score": m["health_score"]} for m in medium_competition]
                },
                "low_competition": {
                    "count": len(low_competition),
                    "markets": [{"name": m["market_name"], "score": m["health_score"]} for m in low_competition]
                }
            },
            "recommendations": self._get_competition_recommendations(high_competition, medium_competition, low_competition)
        }
    
    def _generate_opportunity_radius_analysis(self, markets: List[Dict[str, Any]], center_lat: float, center_lng: float, radius_km: float) -> Dict[str, Any]:
        """기회 분석 반경 분석"""
        
        # 기회 지수 계산 (낮은 경쟁도 + 높은 성장 잠재력)
        opportunities = []
        for market in markets:
            opportunity_score = 0
            
            # 경쟁도 점수 (낮을수록 좋음)
            if market["competition_level"] == "low":
                opportunity_score += 40
            elif market["competition_level"] == "medium":
                opportunity_score += 20
            
            # 성장 잠재력 점수
            opportunity_score += market["growth_potential"] * 0.6
            
            opportunities.append({
                "market_code": market["market_code"],
                "market_name": market["market_name"],
                "opportunity_score": round(opportunity_score, 2),
                "competition_level": market["competition_level"],
                "growth_potential": market["growth_potential"],
                "distance_km": market["distance_km"]
            })
        
        # 기회 점수 순으로 정렬
        opportunities.sort(key=lambda x: x["opportunity_score"], reverse=True)
        
        return {
            "center": {"lat": center_lat, "lng": center_lng},
            "radius_km": radius_km,
            "opportunity_analysis": {
                "total_opportunities": len(opportunities),
                "top_opportunities": opportunities[:5],
                "average_opportunity_score": round(sum(o["opportunity_score"] for o in opportunities) / len(opportunities), 2)
            },
            "opportunity_recommendations": self._get_opportunity_recommendations(opportunities)
        }
    
    def _cluster_by_performance(self, markets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """성과별 클러스터링"""
        
        # 성과 점수 계산 (건강 점수 + 유동인구 정규화)
        max_traffic = max(m["foot_traffic"] for m in markets)
        
        for market in markets:
            performance_score = market["health_score"] * 0.7 + (market["foot_traffic"] / max_traffic) * 100 * 0.3
            market["performance_score"] = round(performance_score, 2)
        
        # 클러스터 분류
        high_performance = [m for m in markets if m["performance_score"] >= 80]
        medium_performance = [m for m in markets if 60 <= m["performance_score"] < 80]
        low_performance = [m for m in markets if m["performance_score"] < 60]
        
        return {
            "cluster_type": "performance",
            "total_markets": len(markets),
            "clusters": {
                "high_performance": {
                    "count": len(high_performance),
                    "markets": high_performance,
                    "characteristics": "높은 건강 점수와 유동인구를 보유한 우수 상권"
                },
                "medium_performance": {
                    "count": len(medium_performance),
                    "markets": medium_performance,
                    "characteristics": "보통 수준의 성과를 보이는 상권"
                },
                "low_performance": {
                    "count": len(low_performance),
                    "markets": low_performance,
                    "characteristics": "개선이 필요한 상권"
                }
            },
            "cluster_insights": self._get_performance_cluster_insights(high_performance, medium_performance, low_performance)
        }
    
    def _cluster_by_characteristics(self, markets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """특성별 클러스터링"""
        
        # 특성별 클러스터
        clusters = {
            "high_traffic_low_competition": [],
            "high_growth_potential": [],
            "stable_markets": [],
            "emerging_markets": []
        }
        
        for market in markets:
            # 높은 유동인구 + 낮은 경쟁도
            if market["foot_traffic"] > 150000 and market["competition_level"] == "low":
                clusters["high_traffic_low_competition"].append(market)
            
            # 높은 성장 잠재력
            if market["growth_potential"] > 80:
                clusters["high_growth_potential"].append(market)
            
            # 안정적인 상권 (건강 점수 70-80)
            if 70 <= market["health_score"] <= 80:
                clusters["stable_markets"].append(market)
            
            # 신흥 상권 (낮은 경쟁도 + 중간 성장 잠재력)
            if market["competition_level"] == "low" and 60 <= market["growth_potential"] <= 80:
                clusters["emerging_markets"].append(market)
        
        return {
            "cluster_type": "characteristics",
            "total_markets": len(markets),
            "clusters": clusters,
            "cluster_analysis": self._analyze_characteristic_clusters(clusters)
        }
    
    def _cluster_by_growth_stage(self, markets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """성장 단계별 클러스터링"""
        
        clusters = {
            "growth": [],      # 성장기
            "mature": [],      # 성숙기
            "decline": [],     # 쇠퇴기
            "emerging": []     # 신흥기
        }
        
        for market in markets:
            if market["growth_potential"] > 80 and market["health_score"] > 75:
                clusters["growth"].append(market)
            elif market["health_score"] > 70 and market["competition_level"] in ["medium", "high"]:
                clusters["mature"].append(market)
            elif market["health_score"] < 60:
                clusters["decline"].append(market)
            else:
                clusters["emerging"].append(market)
        
        return {
            "cluster_type": "growth_stage",
            "total_markets": len(markets),
            "clusters": clusters,
            "growth_recommendations": self._get_growth_stage_recommendations(clusters)
        }
    
    def _generate_traffic_flow_data(self, market_code: str, time_period: str) -> List[Dict[str, Any]]:
        """유동인구 흐름 데이터 생성"""
        
        # 시간대별 샘플 데이터 생성
        if time_period == "daily":
            hours = list(range(24))
            base_traffic = 1000
        elif time_period == "weekly":
            hours = ["월", "화", "수", "목", "금", "토", "일"]
            base_traffic = 5000
        else:
            hours = list(range(24))
            base_traffic = 1000
        
        traffic_data = []
        for i, hour in enumerate(hours):
            # 시간대별 패턴 생성
            if time_period == "daily":
                if 7 <= hour <= 9:  # 출근 시간
                    traffic = base_traffic * 1.5
                elif 12 <= hour <= 14:  # 점심 시간
                    traffic = base_traffic * 2.0
                elif 18 <= hour <= 20:  # 퇴근 시간
                    traffic = base_traffic * 1.8
                elif 21 <= hour <= 23:  # 저녁 시간
                    traffic = base_traffic * 1.2
                else:
                    traffic = base_traffic * 0.5
            else:  # 주간 패턴
                if hour in ["월", "화", "수", "목", "금"]:
                    traffic = base_traffic * 1.0
                elif hour == "토":
                    traffic = base_traffic * 1.3
                else:  # 일요일
                    traffic = base_traffic * 0.8
            
            traffic_data.append({
                "time": hour,
                "traffic": int(traffic),
                "direction": "inbound" if i % 2 == 0 else "outbound"
            })
        
        return traffic_data
    
    def _identify_peak_hours(self, traffic_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """피크 시간 식별"""
        
        # 유동인구가 높은 시간대 찾기
        sorted_traffic = sorted(traffic_data, key=lambda x: x["traffic"], reverse=True)
        peak_hours = sorted_traffic[:3]
        
        return [
            {
                "time": hour["time"],
                "traffic": hour["traffic"],
                "peak_type": "morning" if isinstance(hour["time"], int) and 6 <= hour["time"] <= 10 else "afternoon" if isinstance(hour["time"], int) and 12 <= hour["time"] <= 16 else "evening"
            }
            for hour in peak_hours
        ]
    
    def _analyze_flow_patterns(self, traffic_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """흐름 패턴 분석"""
        
        inbound_traffic = sum(h["traffic"] for h in traffic_data if h["direction"] == "inbound")
        outbound_traffic = sum(h["traffic"] for h in traffic_data if h["direction"] == "outbound")
        
        return {
            "inbound_traffic": inbound_traffic,
            "outbound_traffic": outbound_traffic,
            "net_flow": inbound_traffic - outbound_traffic,
            "flow_balance": "positive" if inbound_traffic > outbound_traffic else "negative",
            "peak_inbound_time": max([h for h in traffic_data if h["direction"] == "inbound"], key=lambda x: x["traffic"])["time"],
            "peak_outbound_time": max([h for h in traffic_data if h["direction"] == "outbound"], key=lambda x: x["traffic"])["time"]
        }
    
    def _get_traffic_recommendations(self, traffic_data: List[Dict[str, Any]]) -> List[str]:
        """유동인구 기반 추천사항"""
        
        peak_hours = self._identify_peak_hours(traffic_data)
        recommendations = []
        
        for peak in peak_hours:
            if peak["peak_type"] == "morning":
                recommendations.append("아침 시간대 유동인구가 높으므로 조식 메뉴나 커피 서비스를 고려하세요.")
            elif peak["peak_type"] == "afternoon":
                recommendations.append("오후 시간대 유동인구가 높으므로 점심 메뉴나 쇼핑 서비스를 강화하세요.")
            elif peak["peak_type"] == "evening":
                recommendations.append("저녁 시간대 유동인구가 높으므로 저녁 메뉴나 엔터테인먼트 서비스를 고려하세요.")
        
        return recommendations
    
    def _analyze_transportation(self, market_info: Dict[str, Any]) -> Dict[str, Any]:
        """교통편 분석"""
        
        # 샘플 교통편 데이터
        transportation = {
            "subway": {
                "available": True,
                "stations": ["대전역", "중앙로역"],
                "walking_time": "5분",
                "frequency": "3-5분"
            },
            "bus": {
                "available": True,
                "routes": ["101", "102", "201", "202"],
                "walking_time": "2분",
                "frequency": "5-10분"
            },
            "taxi": {
                "available": True,
                "waiting_time": "2-5분",
                "accessibility": "high"
            },
            "parking": {
                "available": True,
                "capacity": 200,
                "cost": "시간당 1,000원",
                "accessibility": "medium"
            }
        }
        
        return transportation
    
    def _analyze_parking(self, market_info: Dict[str, Any]) -> Dict[str, Any]:
        """주차 시설 분석"""
        
        parking = {
            "public_parking": {
                "available": True,
                "capacity": 150,
                "cost": "시간당 1,000원",
                "distance": "100m"
            },
            "private_parking": {
                "available": True,
                "capacity": 50,
                "cost": "시간당 2,000원",
                "distance": "50m"
            },
            "street_parking": {
                "available": False,
                "reason": "주차 금지 구역"
            },
            "accessibility_score": 75
        }
        
        return parking
    
    def _analyze_pedestrian_access(self, market_info: Dict[str, Any]) -> Dict[str, Any]:
        """보행자 접근성 분석"""
        
        pedestrian = {
            "sidewalks": {
                "available": True,
                "width": "3m",
                "condition": "good"
            },
            "crosswalks": {
                "available": True,
                "count": 4,
                "signal_controlled": True
            },
            "pedestrian_zones": {
                "available": True,
                "area": "500m²",
                "restrictions": "차량 통행 금지"
            },
            "accessibility_features": {
                "wheelchair_accessible": True,
                "elevator_available": True,
                "ramp_available": True
            },
            "accessibility_score": 85
        }
        
        return pedestrian
    
    def _calculate_accessibility_score(self, transportation: Dict[str, Any], parking: Dict[str, Any], pedestrian: Dict[str, Any]) -> float:
        """종합 접근성 점수 계산"""
        
        # 각 요소별 가중치
        weights = {
            "transportation": 0.4,
            "parking": 0.3,
            "pedestrian": 0.3
        }
        
        # 교통편 점수
        transport_score = 80 if transportation["subway"]["available"] else 60
        if transportation["bus"]["available"]:
            transport_score += 10
        
        # 주차 점수
        parking_score = parking["accessibility_score"]
        
        # 보행자 점수
        pedestrian_score = pedestrian["accessibility_score"]
        
        # 종합 점수 계산
        total_score = (
            transport_score * weights["transportation"] +
            parking_score * weights["parking"] +
            pedestrian_score * weights["pedestrian"]
        )
        
        return round(total_score, 2)
    
    def _get_accessibility_improvements(self, accessibility_score: float, transportation: Dict[str, Any], parking: Dict[str, Any], pedestrian: Dict[str, Any]) -> List[str]:
        """접근성 개선 제안"""
        
        improvements = []
        
        if accessibility_score < 70:
            improvements.append("전반적인 접근성 개선이 필요합니다.")
        
        if not transportation["subway"]["available"]:
            improvements.append("지하철 접근성 개선을 위한 교통편 확충이 필요합니다.")
        
        if parking["accessibility_score"] < 70:
            improvements.append("주차 시설 확충 및 접근성 개선이 필요합니다.")
        
        if pedestrian["accessibility_score"] < 80:
            improvements.append("보행자 접근성 개선을 위한 인프라 구축이 필요합니다.")
        
        return improvements
    
    # 헬퍼 메서드들
    def _get_markets_by_region(self, region: str = None) -> List[Dict[str, Any]]:
        """지역별 상권 조회"""
        if region:
            return [m for m in self.sample_market_data if region in m["region"]]
        return self.sample_market_data
    
    def _get_market_info(self, market_code: str) -> Optional[Dict[str, Any]]:
        """상권 정보 조회"""
        for market in self.sample_market_data:
            if market["market_code"] == market_code:
                return market
        return None
    
    def _calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """두 지점 간 거리 계산 (km)"""
        R = 6371  # 지구 반지름 (km)
        
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2) * math.sin(dlng/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def _get_grade_from_score(self, score: float) -> str:
        """점수에서 등급 변환"""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        else:
            return "D"
    
    def _get_traffic_level(self, traffic: int) -> str:
        """유동인구 수준 판단"""
        if traffic >= 150000:
            return "매우 높음"
        elif traffic >= 100000:
            return "높음"
        elif traffic >= 50000:
            return "보통"
        else:
            return "낮음"
    
    def _get_potential_level(self, potential: int) -> str:
        """성장 잠재력 수준 판단"""
        if potential >= 80:
            return "매우 높음"
        elif potential >= 60:
            return "높음"
        elif potential >= 40:
            return "보통"
        else:
            return "낮음"
    
    def _calculate_competition_intensity(self, competition_distribution: Dict[str, int]) -> str:
        """경쟁 강도 계산"""
        total = sum(competition_distribution.values())
        high_ratio = competition_distribution["high"] / total
        
        if high_ratio > 0.5:
            return "매우 높음"
        elif high_ratio > 0.3:
            return "높음"
        elif high_ratio > 0.1:
            return "보통"
        else:
            return "낮음"
    
    def _identify_market_opportunities(self, markets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """시장 기회 식별"""
        opportunities = []
        
        for market in markets:
            if market["competition_level"] == "low" and market["growth_potential"] > 70:
                opportunities.append({
                    "market_code": market["market_code"],
                    "market_name": market["market_name"],
                    "opportunity_type": "저경쟁 고성장",
                    "reason": "경쟁이 낮고 성장 잠재력이 높음"
                })
        
        return opportunities
    
    def _identify_risk_factors(self, markets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """리스크 요인 식별"""
        risks = []
        
        for market in markets:
            if market["competition_level"] == "high" and market["health_score"] < 70:
                risks.append({
                    "market_code": market["market_code"],
                    "market_name": market["market_name"],
                    "risk_type": "고경쟁 저성과",
                    "reason": "경쟁이 치열하고 성과가 낮음"
                })
        
        return risks
    
    def _get_competition_recommendations(self, high_comp: List, medium_comp: List, low_comp: List) -> List[str]:
        """경쟁도 기반 추천사항"""
        recommendations = []
        
        if len(high_comp) > len(medium_comp) + len(low_comp):
            recommendations.append("고경쟁 지역이 많으므로 차별화 전략이 필수입니다.")
        
        if len(low_comp) > 0:
            recommendations.append("저경쟁 지역이 있어 진입 기회가 있습니다.")
        
        return recommendations
    
    def _get_opportunity_recommendations(self, opportunities: List[Dict[str, Any]]) -> List[str]:
        """기회 기반 추천사항"""
        recommendations = []
        
        if opportunities:
            top_opportunity = opportunities[0]
            recommendations.append(f"{top_opportunity['market_name']}이 가장 높은 기회를 제공합니다.")
        
        return recommendations
    
    def _get_performance_cluster_insights(self, high: List, medium: List, low: List) -> List[str]:
        """성과 클러스터 인사이트"""
        insights = []
        
        if len(high) > 0:
            insights.append("고성과 상권들의 공통점을 분석하여 성공 요인을 파악하세요.")
        
        if len(low) > 0:
            insights.append("저성과 상권들의 개선점을 분석하여 발전 방안을 모색하세요.")
        
        return insights
    
    def _analyze_characteristic_clusters(self, clusters: Dict[str, List]) -> Dict[str, Any]:
        """특성 클러스터 분석"""
        return {
            "high_traffic_low_competition": "유동인구는 많지만 경쟁이 낮은 이상적인 상권",
            "high_growth_potential": "성장 잠재력이 높아 미래 발전 가능성이 큰 상권",
            "stable_markets": "안정적인 성과를 보이는 신뢰할 수 있는 상권",
            "emerging_markets": "새롭게 떠오르는 기회가 많은 상권"
        }
    
    def _get_growth_stage_recommendations(self, clusters: Dict[str, List]) -> Dict[str, List[str]]:
        """성장 단계별 추천사항"""
        return {
            "growth": ["성장기에 집중하여 시장 점유율을 확대하세요.", "브랜드 인지도 향상에 투자하세요."],
            "mature": ["기존 고객 유지에 집중하세요.", "차별화 전략으로 경쟁 우위를 확보하세요."],
            "decline": ["신규 고객 유치 전략이 필요합니다.", "사업 모델 혁신을 고려하세요."],
            "emerging": ["초기 투자와 마케팅에 집중하세요.", "고객 피드백을 적극 수집하세요."]
        }
