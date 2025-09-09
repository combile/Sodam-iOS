#!/usr/bin/env python3
"""
상권 진단 API (CSV 데이터 기반)
"""
from flask import Blueprint, request, jsonify
from services.data_loader import DataLoader
from datetime import datetime

market_diagnosis_bp = Blueprint('market_diagnosis', __name__, url_prefix='/api/v1/market-diagnosis')

# 데이터 로더 인스턴스
data_loader = DataLoader()

@market_diagnosis_bp.route('/')
def market_diagnosis():
    """상권 진단 API 메인"""
    return jsonify({
        "success": True,
        "message": "상권 진단 API (CSV 데이터 기반)",
        "endpoints": {
            "markets": "/api/v1/market-diagnosis/markets",
            "market_detail": "/api/v1/market-diagnosis/markets/<market_code>",
            "districts": "/api/v1/market-diagnosis/districts",
            "tourism_trend": "/api/v1/market-diagnosis/tourism-trend",
            "industry_analysis": "/api/v1/market-diagnosis/industry-analysis",
            "regional_analysis": "/api/v1/market-diagnosis/regional-analysis"
        },
        "timestamp": datetime.utcnow().isoformat()
    })

@market_diagnosis_bp.route('/markets', methods=['GET'])
def get_markets():
    """
    상권 목록 조회
    
    대전광역시 내 상권 목록을 조회합니다. 지역구, 상권 유형별로 필터링이 가능합니다.
    
    ### 쿼리 파라미터
    - **district**: 지역구 필터 (동구, 중구, 서구, 유성구, 대덕구)
    - **market_type**: 상권 유형 필터 (상업지구, 주거지구, 혼합지구)
    - **limit**: 페이지당 결과 수 (기본값: 50, 최대: 100)
    - **offset**: 페이지 오프셋 (기본값: 0)
    
    ### 응답 예시
    ```json
    {
        "success": true,
        "data": {
            "markets": [
                {
                    "market_code": "DJ001",
                    "market_name": "대전역 상권",
                    "city_name": "대전광역시",
                    "district_name": "동구",
                    "market_type": "상업지구",
                    "coordinates": "36.3326,127.4342"
                }
            ],
            "pagination": {
                "total": 26,
                "limit": 50,
                "offset": 0,
                "has_more": false
            }
        },
        "message": "상권 목록을 성공적으로 조회했습니다.",
        "timestamp": "2024-01-01T00:00:00Z"
    }
    ```
    
    ### 에러 코드
    - **404**: 상권 데이터를 찾을 수 없음
    - **500**: 서버 내부 오류
    """
    try:
        # 쿼리 파라미터
        district = request.args.get('district')
        market_type = request.args.get('market_type')
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        # 상권 데이터 로드
        df = data_loader.load_market_data()
        if df.empty:
            return jsonify({
                "success": False,
                "error": {
                    "code": "NO_DATA",
                    "message": "상권 데이터를 찾을 수 없습니다."
                }
            }), 404
        
        # 필터링
        filtered_df = df.copy()
        
        if district:
            filtered_df = filtered_df[filtered_df['district_name'] == district]
        
        if market_type:
            filtered_df = filtered_df[filtered_df['market_type'] == market_type]
        
        # 페이징
        total_count = len(filtered_df)
        paginated_df = filtered_df.iloc[offset:offset + limit]
        
        # 결과 변환
        markets = []
        for _, row in paginated_df.iterrows():
            market = {
                "market_code": row['market_code'],
                "market_name": row['market_name'],
                "city_name": row['city_name'],
                "district_name": row['district_name'],
                "market_type": row['market_type'],
                "coordinates": row['coordinates']
            }
            markets.append(market)
        
        return jsonify({
            "success": True,
            "data": {
                "markets": markets,
                "pagination": {
                    "total": total_count,
                    "limit": limit,
                    "offset": offset,
                    "has_more": offset + limit < total_count
                }
            },
            "message": "상권 목록을 성공적으로 조회했습니다.",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"상권 목록 조회 중 오류가 발생했습니다: {str(e)}"
            }
        }), 500

@market_diagnosis_bp.route('/markets/<market_code>', methods=['GET'])
def get_market_detail(market_code):
    """상권 상세 정보 조회"""
    try:
        market = data_loader.get_market_by_code(market_code)
        
        if not market:
            return jsonify({
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": "해당 상권을 찾을 수 없습니다."
                }
            }), 404
        
        return jsonify({
            "success": True,
            "data": {
                "market": market
            },
            "message": "상권 상세 정보를 성공적으로 조회했습니다.",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"상권 상세 정보 조회 중 오류가 발생했습니다: {str(e)}"
            }
        }), 500

@market_diagnosis_bp.route('/districts', methods=['GET'])
def get_districts():
    """지역구 목록 조회"""
    try:
        df = data_loader.load_market_data()
        if df.empty:
            return jsonify({
                "success": False,
                "error": {
                    "code": "NO_DATA",
                    "message": "상권 데이터를 찾을 수 없습니다."
                }
            }), 404
        
        # 지역구별 상권 수 집계
        district_stats = df.groupby('district_name').agg({
            'market_code': 'count',
            'market_type': 'nunique'
        }).reset_index()
        
        district_stats.columns = ['district_name', 'market_count', 'market_type_count']
        
        districts = district_stats.to_dict('records')
        
        return jsonify({
            "success": True,
            "data": {
                "districts": districts
            },
            "message": "지역구 목록을 성공적으로 조회했습니다.",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"지역구 목록 조회 중 오류가 발생했습니다: {str(e)}"
            }
        }), 500

@market_diagnosis_bp.route('/tourism-trend', methods=['GET'])
def get_tourism_trend():
    """관광 소비 트렌드 조회"""
    try:
        region = request.args.get('region', '대전광역시')
        
        trend_data = data_loader.get_tourism_trend(region)
        
        if not trend_data:
            return jsonify({
                "success": False,
                "error": {
                    "code": "NO_DATA",
                    "message": "관광 소비 데이터를 찾을 수 없습니다."
                }
            }), 404
        
        return jsonify({
            "success": True,
            "data": {
                "region": region,
                "trend": trend_data
            },
            "message": "관광 소비 트렌드를 성공적으로 조회했습니다.",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"관광 소비 트렌드 조회 중 오류가 발생했습니다: {str(e)}"
            }
        }), 500

@market_diagnosis_bp.route('/industry-analysis', methods=['GET'])
def get_industry_analysis():
    """업종별 분석 조회"""
    try:
        industry_data = data_loader.get_industry_ratios()
        
        if not industry_data:
            return jsonify({
                "success": False,
                "error": {
                    "code": "NO_DATA",
                    "message": "업종별 분석 데이터를 찾을 수 없습니다."
                }
            }), 404
        
        return jsonify({
            "success": True,
            "data": {
                "industry_analysis": industry_data
            },
            "message": "업종별 분석을 성공적으로 조회했습니다.",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"업종별 분석 조회 중 오류가 발생했습니다: {str(e)}"
            }
        }), 500

@market_diagnosis_bp.route('/regional-analysis', methods=['GET'])
def get_regional_analysis():
    """지역별 분석 조회"""
    try:
        regional_data = data_loader.get_regional_ratios()
        
        if not regional_data:
            return jsonify({
                "success": False,
                "error": {
                    "code": "NO_DATA",
                    "message": "지역별 분석 데이터를 찾을 수 없습니다."
                }
            }), 404
        
        return jsonify({
            "success": True,
            "data": {
                "regional_analysis": regional_data
            },
            "message": "지역별 분석을 성공적으로 조회했습니다.",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"지역별 분석 조회 중 오류가 발생했습니다: {str(e)}"
            }
        }), 500
