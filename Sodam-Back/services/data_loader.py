#!/usr/bin/env python3
"""
데이터 로더 서비스
CSV 파일들을 로드하고 전처리하는 서비스
"""
import pandas as pd
import os
import json
from typing import Dict, List, Any, Optional

class DataLoader:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'csv')
        self._cache = {}
    
    def load_market_data(self) -> pd.DataFrame:
        """상권 데이터 로드"""
        if 'market_data' in self._cache:
            return self._cache['market_data']
        
        file_path = os.path.join(self.data_dir, 'market_data.csv')
        try:
            # CSV 파일 로드 (인코딩 문제 해결)
            encodings = ['utf-8', 'cp949', 'euc-kr', 'latin1']
            df = None
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                raise Exception("모든 인코딩 시도 실패")
            
            # 컬럼명 정리 (실제 CSV 구조에 맞게)
            df.columns = ['market_code', 'market_name', 'market_type', 'city_code', 
                         'city_name', 'district_code', 'district_name', 
                         'coordinate_count', 'coordinates', 'data_date']
            
            # 좌표 데이터 파싱
            df['coordinates'] = df['coordinates'].apply(self._parse_coordinates)
            
            self._cache['market_data'] = df
            return df
        except Exception as e:
            print(f"상권 데이터 로드 실패: {e}")
            return pd.DataFrame()
    
    def load_tourism_consumption(self) -> pd.DataFrame:
        """관광 소비 데이터 로드"""
        if 'tourism_consumption' in self._cache:
            return self._cache['tourism_consumption']
        
        file_path = os.path.join(self.data_dir, 'tourism_consumption.csv')
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            
            # 컬럼명 정리 (실제 CSV 구조에 맞게)
            df.columns = ['year_month', 'region', 'category', 'consumption_amount']
            
            # 소비액을 숫자로 변환
            df['consumption_amount'] = pd.to_numeric(df['consumption_amount'], errors='coerce')
            
            self._cache['tourism_consumption'] = df
            return df
        except Exception as e:
            print(f"관광 소비 데이터 로드 실패: {e}")
            return pd.DataFrame()
    
    def load_industry_expenditure(self) -> pd.DataFrame:
        """업종별 지출액 데이터 로드"""
        if 'industry_expenditure' in self._cache:
            return self._cache['industry_expenditure']
        
        file_path = os.path.join(self.data_dir, 'industry_expenditure.csv')
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            
            # 컬럼명 정리 (실제 CSV 구조에 맞게)
            df.columns = ['major_category', 'minor_category', 'major_ratio', 'minor_ratio']
            
            # 비율을 숫자로 변환
            df['major_ratio'] = pd.to_numeric(df['major_ratio'], errors='coerce')
            df['minor_ratio'] = pd.to_numeric(df['minor_ratio'], errors='coerce')
            
            self._cache['industry_expenditure'] = df
            return df
        except Exception as e:
            print(f"업종별 지출액 데이터 로드 실패: {e}")
            return pd.DataFrame()
    
    def load_regional_expenditure(self) -> pd.DataFrame:
        """지역별 지출액 데이터 로드"""
        if 'regional_expenditure' in self._cache:
            return self._cache['regional_expenditure']
        
        file_path = os.path.join(self.data_dir, 'regional_expenditure.csv')
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            
            # 컬럼명 정리 (실제 CSV 구조에 맞게)
            df.columns = ['region', 'expenditure_ratio']
            
            # 비율을 숫자로 변환
            df['expenditure_ratio'] = pd.to_numeric(df['expenditure_ratio'], errors='coerce')
            
            self._cache['regional_expenditure'] = df
            return df
        except Exception as e:
            print(f"지역별 지출액 데이터 로드 실패: {e}")
            return pd.DataFrame()
    
    def _parse_coordinates(self, coord_string: str) -> List[Dict[str, float]]:
        """좌표 문자열을 파싱하여 좌표 리스트로 변환"""
        try:
            if pd.isna(coord_string) or not coord_string:
                return []
            
            # 좌표 문자열 파싱 (예: "126.858956602584|37.5264695116541...")
            coord_string = str(coord_string)
            coords = coord_string.split('|')
            coordinate_pairs = []
            
            for i in range(0, len(coords), 2):
                if i + 1 < len(coords):
                    try:
                        lng = float(coords[i])
                        lat = float(coords[i + 1])
                        coordinate_pairs.append({'lng': lng, 'lat': lat})
                    except ValueError:
                        continue
            
            return coordinate_pairs
        except Exception as e:
            print(f"좌표 파싱 실패: {e}")
            return []
    
    def get_market_by_code(self, market_code: str) -> Optional[Dict[str, Any]]:
        """상권 코드로 상권 정보 조회"""
        df = self.load_market_data()
        if df.empty:
            return None
        
        market = df[df['market_code'].astype(str) == str(market_code)]
        if market.empty:
            return None
        
        market_info = market.iloc[0].to_dict()
        return {
            'market_code': market_info['market_code'],
            'market_name': market_info['market_name'],
            'city_name': market_info['city_name'],
            'district_name': market_info['district_name'],
            'market_type': market_info['market_type'],
            'coordinates': market_info['coordinates']
        }
    
    def get_markets_by_district(self, district: str) -> List[Dict[str, Any]]:
        """지역구별 상권 목록 조회"""
        df = self.load_market_data()
        if df.empty:
            return []
        
        markets = df[df['district_name'] == district]
        return markets.to_dict('records')
    
    def get_tourism_trend(self, region: str = "대전광역시") -> List[Dict[str, Any]]:
        """관광 소비 트렌드 조회 - 위치별 실제 데이터"""
        df = self.load_tourism_consumption()
        if df.empty:
            return []
        
        # 해당 지역의 관광총소비 데이터만 필터링
        tourism_data = df[(df['region'] == region) & (df['category'] == '관광총소비')]
        
        # 최신 12개월 데이터
        trend_data = tourism_data.tail(12).to_dict('records')
        
        return trend_data
    
    def get_tourism_trend_by_industry(self, region: str, industry: str) -> List[Dict[str, Any]]:
        """업종별 관광 소비 트렌드 조회 - 위치별, 업종별 실제 데이터"""
        df = self.load_tourism_consumption()
        if df.empty:
            return []
        
        # 업종 매핑 (실제 데이터의 카테고리명 사용)
        industry_mapping = {
            "쇼핑업": "대형쇼핑몰",  # 쇼핑업의 대표 카테고리
            "숙박업": "호텔",  # 숙박업의 대표 카테고리
            "식음료업": "식음료",
            "여가서비스업": "관광유원시설",  # 여가서비스업의 대표 카테고리
            "여행업": "여행업",
            "운송업": "육상운송"  # 운송업의 대표 카테고리
        }
        
        category = industry_mapping.get(industry, "관광총소비")
        
        # 해당 지역과 업종의 데이터 필터링
        tourism_data = df[(df['region'] == region) & (df['category'] == category)]
        
        # 최신 12개월 데이터
        trend_data = tourism_data.tail(12).to_dict('records')
        
        return trend_data
    
    def get_industry_ratios(self) -> List[Dict[str, Any]]:
        """업종별 지출액 비율 조회"""
        df = self.load_industry_expenditure()
        if df.empty:
            return []
        
        return df.to_dict('records')
    
    def get_industry_ratio_by_category(self, major_category: str, minor_category: str = None) -> Dict[str, float]:
        """특정 업종의 지출액 비율 조회"""
        df = self.load_industry_expenditure()
        if df.empty:
            return {"major_ratio": 0.0, "minor_ratio": 0.0}
        
        # 대분류 필터링
        major_data = df[df['major_category'] == major_category]
        if major_data.empty:
            return {"major_ratio": 0.0, "minor_ratio": 0.0}
        
        major_ratio = major_data.iloc[0]['major_ratio'] if not major_data.empty else 0.0
        
        # 중분류 필터링 (있는 경우)
        minor_ratio = 0.0
        if minor_category:
            minor_data = major_data[major_data['minor_category'] == minor_category]
            if not minor_data.empty:
                minor_ratio = minor_data.iloc[0]['minor_ratio']
        
        return {
            "major_ratio": major_ratio,
            "minor_ratio": minor_ratio
        }
    
    def get_regional_ratios(self) -> List[Dict[str, Any]]:
        """지역별 지출액 비율 조회"""
        df = self.load_regional_expenditure()
        if df.empty:
            return []
        
        return df.to_dict('records')
    
    def get_regional_ratio_by_region(self, region: str) -> float:
        """특정 지역의 지출액 비율 조회"""
        df = self.load_regional_expenditure()
        if df.empty:
            return 0.0
        
        region_data = df[df['region'] == region]
        if region_data.empty:
            return 0.0
        
        return region_data.iloc[0]['expenditure_ratio']
    
    def clear_cache(self):
        """캐시 초기화"""
        self._cache.clear()
