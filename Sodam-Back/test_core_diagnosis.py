#!/usr/bin/env python3
"""
CoreDiagnosisService 테스트 스크립트
다양한 상권 코드에 대해 다른 결과가 나오는지 확인
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.core_diagnosis_service import CoreDiagnosisService

def test_different_market_codes():
    """다양한 상권 코드에 대해 다른 결과가 나오는지 테스트"""
    service = CoreDiagnosisService()
    
    # 테스트할 상권 코드들
    test_codes = ["DJ001", "DJ002", "DJ003", "DJ004", "DJ005"]
    
    print("=== 상권별 건강 점수 비교 테스트 ===\n")
    
    for market_code in test_codes:
        print(f"상권 코드: {market_code}")
        print("-" * 40)
        
        try:
            # 건강 점수 계산
            result = service.calculate_health_score(market_code, "식음료업")
            
            if "error" in result:
                print(f"오류: {result['error']}")
            else:
                print(f"총 점수: {result['total_score']}")
                print(f"등급: {result['final_grade']}")
                print(f"건강 상태: {result['health_status']}")
                
                # 각 지표별 점수
                breakdown = result['score_breakdown']
                print(f"유동인구 점수: {breakdown['foot_traffic']['score']:.1f} ({breakdown['foot_traffic']['grade']})")
                print(f"카드매출 점수: {breakdown['card_sales']['score']:.1f} ({breakdown['card_sales']['grade']})")
                print(f"창업·폐업 점수: {breakdown['business_rates']['score']:.1f} ({breakdown['business_rates']['grade']})")
                print(f"체류시간 점수: {breakdown['dwell_time']['score']:.1f} ({breakdown['dwell_time']['grade']})")
            
        except Exception as e:
            print(f"예외 발생: {str(e)}")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    test_different_market_codes()
