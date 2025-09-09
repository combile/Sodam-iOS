from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from services.core_diagnosis_service import CoreDiagnosisService
from datetime import datetime
from typing import Dict, List, Any

core_diagnosis_ns = Namespace('core-diagnosis', description='상권 진단 핵심 지표 API')

core_diagnosis_service = CoreDiagnosisService()

# 모델 정의
foot_traffic_response = core_diagnosis_ns.model('FootTrafficResponse', {
    'market_code': fields.String(description='상권 코드', example='DJ001'),
    'market_name': fields.String(description='상권명', example='대전역 상권'),
    'current_monthly_traffic': fields.Integer(description='현재 월 유동인구 (명)', example=150000),
    'previous_monthly_traffic': fields.Integer(description='이전 월 유동인구 (명)', example=145000),
    'average_monthly_change': fields.Float(description='월평균 변화율 (%)', example=3.4),
    'total_change_period': fields.Float(description='기간 총 변화율 (%)', example=12.5),
    'trend': fields.String(description='트렌드', example='상승', enum=['상승', '하락', '보합']),
    'grade': fields.String(description='등급', example='A', enum=['A', 'B', 'C', 'D']),
    'score': fields.Integer(description='점수 (0-100)', example=85),
    'analysis': fields.String(description='분석 결과', example='유동인구가 지속적으로 증가하고 있어 상권 활성화가 우수한 상태입니다.'),
    'recommendations': fields.List(fields.String, description='개선 권장사항', example=['고객 유입 증대를 위한 마케팅 강화', '체류시간 연장을 위한 서비스 개선'])
})

success_response = core_diagnosis_ns.model('SuccessResponse', {
    'success': fields.Boolean(description='성공 여부', example=True),
    'message': fields.String(description='응답 메시지', example='요청이 성공적으로 처리되었습니다.'),
    'data': fields.Raw(description='응답 데이터')
})

@core_diagnosis_ns.route('/foot-traffic/<string:market_code>')
class FootTrafficAnalysis(Resource):
    @core_diagnosis_ns.marshal_with(success_response)
    @core_diagnosis_ns.doc('foot_traffic', 
        description='''
        ## 유동인구 변화량 분석
        
        특정 상권의 유동인구 변화량을 분석하여 상권 활성화 상태를 진단합니다.
        
        ### 경로 파라미터
        - **market_code**: 상권 코드 (예: DJ001, DJ002)
        
        ### 쿼리 파라미터
        - **period_months**: 분석 기간 (월 단위, 기본값: 12)
        
        ### 응답 예시
        ```json
        {
            "success": true,
            "data": {
                "market_code": "DJ001",
                "market_name": "대전역 상권",
                "current_monthly_traffic": 150000,
                "previous_monthly_traffic": 145000,
                "average_monthly_change": 3.4,
                "total_change_period": 12.5,
                "trend": "상승",
                "grade": "A",
                "score": 85,
                "analysis": "유동인구가 지속적으로 증가하고 있어 상권 활성화가 우수한 상태입니다.",
                "recommendations": [
                    "고객 유입 증대를 위한 마케팅 강화",
                    "체류시간 연장을 위한 서비스 개선"
                ]
            }
        }
        ```
        
        ### 등급 기준
        - **A**: 80점 이상 (우수)
        - **B**: 60-79점 (양호)
        - **C**: 40-59점 (보통)
        - **D**: 40점 미만 (주의)
        
        ### 에러 코드
        - **404**: 상권 데이터를 찾을 수 없음
        - **500**: 서버 내부 오류
        ''')
    def get(self, market_code):
        """유동인구 변화량 분석"""
        try:
            period_months = request.args.get('period_months', 12, type=int)
            analysis = core_diagnosis_service.get_foot_traffic_analysis(market_code, period_months)
            
            if "error" in analysis:
                return jsonify({
                    "success": False,
                    "error": {
                        "code": "DATA_NOT_FOUND",
                        "message": analysis["error"]
                    }
                }), 404
            
            return jsonify({
                "success": True,
                "data": analysis
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": str(e)
                }
            }), 500

@core_diagnosis_ns.route('/card-sales/<string:market_code>')
class CardSalesAnalysis(Resource):
    @core_diagnosis_ns.marshal_with(success_response)
    @core_diagnosis_ns.doc('card_sales', description='카드매출 추이 분석')
    def get(self, market_code):
        """카드매출 추이 분석"""
        try:
            period_months = request.args.get('period_months', 12, type=int)
            analysis = core_diagnosis_service.get_card_sales_analysis(market_code, period_months)
            
            if "error" in analysis:
                return jsonify({
                    "success": False,
                    "error": {
                        "code": "DATA_NOT_FOUND",
                        "message": analysis["error"]
                    }
                }), 404
            
            return jsonify({
                "success": True,
                "data": analysis
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": str(e)
                }
            }), 500

@core_diagnosis_ns.route('/same-industry/<string:market_code>')
class SameIndustryAnalysis(Resource):
    @core_diagnosis_ns.marshal_with(success_response)
    @core_diagnosis_ns.doc('same_industry', description='동일업종 수 분석')
    def get(self, market_code):
        """동일업종 수 분석"""
        try:
            industry = request.args.get('industry')
            analysis = core_diagnosis_service.get_same_industry_analysis(market_code, industry)
            
            if "error" in analysis:
                return jsonify({
                    "success": False,
                    "error": {
                        "code": "DATA_NOT_FOUND",
                        "message": analysis["error"]
                    }
                }), 404
            
            return jsonify({
                "success": True,
                "data": analysis
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": str(e)
                }
            }), 500

@core_diagnosis_ns.route('/business-rates/<string:market_code>')
class BusinessRatesAnalysis(Resource):
    @core_diagnosis_ns.marshal_with(success_response)
    @core_diagnosis_ns.doc('business_rates', description='창업·폐업 비율 분석')
    def get(self, market_code):
        """창업·폐업 비율 분석"""
        try:
            analysis = core_diagnosis_service.get_business_rates_analysis(market_code)
            
            if "error" in analysis:
                return jsonify({
                    "success": False,
                    "error": {
                        "code": "DATA_NOT_FOUND",
                        "message": analysis["error"]
                    }
                }), 404
            
            return jsonify({
                "success": True,
                "data": analysis
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": str(e)
                }
            }), 500

@core_diagnosis_ns.route('/dwell-time/<string:market_code>')
class DwellTimeAnalysis(Resource):
    @core_diagnosis_ns.marshal_with(success_response)
    @core_diagnosis_ns.doc('dwell_time', description='체류시간 분석')
    def get(self, market_code):
        """체류시간 분석"""
        try:
            analysis = core_diagnosis_service.get_dwell_time_analysis(market_code)
            
            if "error" in analysis:
                return jsonify({
                    "success": False,
                    "error": {
                        "code": "DATA_NOT_FOUND",
                        "message": analysis["error"]
                    }
                }), 404
            
            return jsonify({
                "success": True,
                "data": analysis
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": str(e)
                }
            }), 500

@core_diagnosis_ns.route('/health-score/<string:market_code>')
class HealthScoreAnalysis(Resource):
    @core_diagnosis_ns.marshal_with(success_response)
    @core_diagnosis_ns.doc('health_score', description='상권 건강 점수 종합 산정')
    def post(self, market_code):
        """상권 건강 점수 종합 산정"""
        try:
            data = request.get_json() or {}
            industry = data.get('industry')
            
            analysis = core_diagnosis_service.calculate_health_score(market_code, industry)
            
            if "error" in analysis:
                return jsonify({
                    "success": False,
                    "error": {
                        "code": "DATA_NOT_FOUND",
                        "message": analysis["error"]
                    }
                }), 404
            
            return jsonify({
                "success": True,
                "data": analysis
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": str(e)
                }
            }), 500

@core_diagnosis_ns.route('/comprehensive/<string:market_code>')
class ComprehensiveAnalysis(Resource):
    @core_diagnosis_ns.marshal_with(success_response)
    @core_diagnosis_ns.doc('comprehensive', description='종합 상권 진단')
    def post(self, market_code):
        """종합 상권 진단"""
        try:
            data = request.get_json() or {}
            category = data.get('category', '전체')
            
            # 모든 지표 분석
            foot_traffic = core_diagnosis_service.get_foot_traffic_analysis(market_code, category)
            card_sales = core_diagnosis_service.get_card_sales_analysis(market_code, category)
            same_industry = core_diagnosis_service.get_same_industry_analysis(market_code, category)
            business_rates = core_diagnosis_service.get_business_rates_analysis(market_code)
            dwell_time = core_diagnosis_service.get_dwell_time_analysis(market_code)
            health_score = core_diagnosis_service.calculate_health_score(market_code, industry=category)
            
            comprehensive_analysis = {
                "market_code": market_code,
                "overall_score": health_score.get("total_score", 70),
                "indicators": {
                    "foot_traffic": foot_traffic.get("score", 0),
                    "card_sales": card_sales.get("score", 0),
                    "competition": same_industry.get("score", 0) if same_industry else 0,
                    "business_rates": business_rates.get("score", 0),
                    "dwell_time": dwell_time.get("score", 0)
                },
                "strengths": health_score.get("strengths", []),
                "weaknesses": health_score.get("weaknesses", []),
                "recommendations": health_score.get("recommendations", [])
            }
            
            return jsonify(comprehensive_analysis)
        except Exception as e:
            return jsonify({
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": str(e)
                }
            }), 500
