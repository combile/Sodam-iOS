from flask import Blueprint, request, jsonify
from services.map_visualization_service import MapVisualizationService
from datetime import datetime
from typing import Dict, List, Any

map_visualization_bp = Blueprint('map_visualization', __name__, url_prefix='/api/v1/map-visualization')

map_visualization_service = MapVisualizationService()

@map_visualization_bp.route('/heatmap', methods=['GET'])
def get_market_heatmap_data():
    """
    상권 히트맵 데이터 생성
    
    상권별 특정 지표를 히트맵 형태로 시각화할 수 있는 데이터를 생성합니다.
    
    ### 쿼리 파라미터
    - **region**: 지역 필터 (선택사항, 기본값: 전체)
    - **analysis_type**: 분석 유형 (기본값: health_score)
    
    ### 지원 분석 유형
    - **health_score**: 상권 건강 점수 (녹색=우수, 노란색=보통, 빨간색=주의)
    - **foot_traffic**: 유동인구 수준 (진한 색=높음, 연한 색=낮음)
    - **competition**: 경쟁도 (빨간색=높음, 주황색=보통, 녹색=낮음)
    - **growth_potential**: 성장 잠재력 (진한 색=높음, 연한 색=낮음)
    
    ### 응답 예시
    ```json
    {
        "success": true,
        "data": {
            "analysis_type": "health_score",
            "region": "대전광역시",
            "heatmap_data": [
                {
                    "market_code": "DJ001",
                    "market_name": "대전역 상권",
                    "latitude": 36.3326,
                    "longitude": 127.4342,
                    "value": 85.5,
                    "grade": "A",
                    "color_intensity": 0.85
                }
            ],
            "color_scale": {
                "min": 0,
                "max": 100,
                "thresholds": {
                    "excellent": 80,
                    "good": 60,
                    "average": 40,
                    "poor": 0
                }
            }
        }
    }
    ```
    
    ### 히트맵 사용법
    1. 응답 데이터의 `latitude`, `longitude`를 사용하여 지도에 마커 표시
    2. `color_intensity` 값을 사용하여 색상 강도 조절
    3. `value`와 `grade`를 사용하여 툴팁 또는 범례 표시
    
    ### 에러 코드
    - **400**: 지원하지 않는 분석 유형
    - **500**: 서버 내부 오류
    """
    try:
        region = request.args.get('region')
        analysis_type = request.args.get('analysis_type', 'health_score')
        
        # 지원하는 분석 유형 검증
        supported_types = ['health_score', 'foot_traffic', 'competition', 'growth_potential']
        if analysis_type not in supported_types:
            return jsonify({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": f"지원하지 않는 분석 유형입니다. 지원 유형: {', '.join(supported_types)}"
                }
            }), 400
        
        heatmap_data = map_visualization_service.get_market_heatmap_data(region, analysis_type)
        
        return jsonify({
            "success": True,
            "data": heatmap_data
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        }), 500

@map_visualization_bp.route('/radius-analysis', methods=['POST'])
def get_radius_analysis():
    """반경별 분석 결과"""
    try:
        data = request.get_json() or {}
        
        # 필수 파라미터 검증
        required_fields = ['center_lat', 'center_lng', 'radius_km']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": f"{field}이 필요합니다."
                    }
                }), 400
        
        analysis_type = data.get('analysis_type', 'comprehensive')
        
        # 지원하는 분석 유형 검증
        supported_types = ['comprehensive', 'competition', 'opportunity']
        if analysis_type not in supported_types:
            return jsonify({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": f"지원하지 않는 분석 유형입니다. 지원 유형: {', '.join(supported_types)}"
                }
            }), 400
        
        radius_analysis = map_visualization_service.get_radius_analysis(
            data['center_lat'],
            data['center_lng'],
            data['radius_km'],
            analysis_type
        )
        
        if "error" in radius_analysis:
            return jsonify({
                "success": False,
                "error": {
                    "code": "DATA_NOT_FOUND",
                    "message": radius_analysis["error"]
                }
            }), 404
        
        return jsonify({
            "success": True,
            "data": radius_analysis
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        }), 500

@map_visualization_bp.route('/cluster-analysis', methods=['GET'])
def get_market_cluster_analysis():
    """상권 클러스터 분석"""
    try:
        region = request.args.get('region')
        cluster_type = request.args.get('cluster_type', 'performance')
        
        # 지원하는 클러스터 유형 검증
        supported_types = ['performance', 'characteristics', 'growth_stage']
        if cluster_type not in supported_types:
            return jsonify({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": f"지원하지 않는 클러스터 유형입니다. 지원 유형: {', '.join(supported_types)}"
                }
            }), 400
        
        cluster_analysis = map_visualization_service.get_market_cluster_analysis(region, cluster_type)
        
        if "error" in cluster_analysis:
            return jsonify({
                "success": False,
                "error": {
                    "code": "DATA_NOT_FOUND",
                    "message": cluster_analysis["error"]
                }
            }), 404
        
        return jsonify({
            "success": True,
            "data": cluster_analysis
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        }), 500

@map_visualization_bp.route('/traffic-flow/<string:market_code>', methods=['GET'])
def get_traffic_flow_analysis(market_code: str):
    """유동인구 흐름 분석"""
    try:
        time_period = request.args.get('time_period', 'daily')
        
        # 지원하는 시간 주기 검증
        supported_periods = ['daily', 'weekly']
        if time_period not in supported_periods:
            return jsonify({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": f"지원하지 않는 시간 주기입니다. 지원 주기: {', '.join(supported_periods)}"
                }
            }), 400
        
        traffic_analysis = map_visualization_service.get_traffic_flow_analysis(market_code, time_period)
        
        return jsonify({
            "success": True,
            "data": traffic_analysis
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        }), 500

@map_visualization_bp.route('/accessibility/<string:market_code>', methods=['GET'])
def get_accessibility_analysis(market_code: str):
    """접근성 분석"""
    try:
        accessibility_analysis = map_visualization_service.get_accessibility_analysis(market_code)
        
        if "error" in accessibility_analysis:
            return jsonify({
                "success": False,
                "error": {
                    "code": "DATA_NOT_FOUND",
                    "message": accessibility_analysis["error"]
                }
            }), 404
        
        return jsonify({
            "success": True,
            "data": accessibility_analysis
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        }), 500

@map_visualization_bp.route('/analysis-types', methods=['GET'])
def get_analysis_types():
    """지원하는 분석 유형 목록"""
    try:
        analysis_types = {
            "heatmap": [
                {
                    "type": "health_score",
                    "name": "건강 점수",
                    "description": "상권의 종합적인 건강 상태를 점수로 표시",
                    "color_scheme": "녹색(우수) → 노란색(보통) → 빨간색(주의)"
                },
                {
                    "type": "foot_traffic",
                    "name": "유동인구",
                    "description": "상권별 유동인구 수준을 강도로 표시",
                    "color_scheme": "진한 색(높음) → 연한 색(낮음)"
                },
                {
                    "type": "competition",
                    "name": "경쟁도",
                    "description": "상권별 경쟁 수준을 색상으로 표시",
                    "color_scheme": "빨간색(높음) → 주황색(보통) → 녹색(낮음)"
                },
                {
                    "type": "growth_potential",
                    "name": "성장 잠재력",
                    "description": "상권의 성장 가능성을 강도로 표시",
                    "color_scheme": "진한 색(높음) → 연한 색(낮음)"
                }
            ],
            "radius_analysis": [
                {
                    "type": "comprehensive",
                    "name": "종합 분석",
                    "description": "반경 내 상권들의 종합적인 분석 결과"
                },
                {
                    "type": "competition",
                    "name": "경쟁도 분석",
                    "description": "반경 내 상권들의 경쟁 상황 분석"
                },
                {
                    "type": "opportunity",
                    "name": "기회 분석",
                    "description": "반경 내 상권들의 진입 기회 분석"
                }
            ],
            "cluster_analysis": [
                {
                    "type": "performance",
                    "name": "성과별 클러스터",
                    "description": "상권의 성과 수준에 따른 그룹화"
                },
                {
                    "type": "characteristics",
                    "name": "특성별 클러스터",
                    "description": "상권의 특성에 따른 그룹화"
                },
                {
                    "type": "growth_stage",
                    "name": "성장 단계별 클러스터",
                    "description": "상권의 성장 단계에 따른 그룹화"
                }
            ]
        }
        
        return jsonify({
            "success": True,
            "data": {
                "analysis_types": analysis_types
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        }), 500

@map_visualization_bp.route('/regions', methods=['GET'])
def get_supported_regions():
    """지원하는 지역 목록"""
    try:
        regions = [
            {
                "code": "대전광역시",
                "name": "대전광역시",
                "districts": ["동구", "중구", "서구", "유성구", "대덕구"],
                "market_count": 5
            },
            {
                "code": "대전광역시 동구",
                "name": "대전광역시 동구",
                "districts": ["동구"],
                "market_count": 1
            },
            {
                "code": "대전광역시 유성구",
                "name": "대전광역시 유성구",
                "districts": ["유성구"],
                "market_count": 1
            },
            {
                "code": "대전광역시 중구",
                "name": "대전광역시 중구",
                "districts": ["중구"],
                "market_count": 1
            },
            {
                "code": "대전광역시 서구",
                "name": "대전광역시 서구",
                "districts": ["서구"],
                "market_count": 1
            },
            {
                "code": "대전광역시 대덕구",
                "name": "대전광역시 대덕구",
                "districts": ["대덕구"],
                "market_count": 1
            }
        ]
        
        return jsonify({
            "success": True,
            "data": {
                "total_regions": len(regions),
                "regions": regions
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        }), 500
