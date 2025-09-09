#!/usr/bin/env python3
"""
개발 서버 실행 스크립트
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import create_app

if __name__ == "__main__":
    app = create_app()
    
    # 환경 변수에서 포트 설정 (기본값: 5000)
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    
    print(f"서버 시작: http://localhost:{port}")
    print("API 문서:")
    print(f"  - 상권 진단: http://localhost:{port}/api/v1/diagnosis/")
    print(f"  - 리스크 분석: http://localhost:{port}/api/v1/risk/")
    print(f"  - 전략 카드: http://localhost:{port}/api/v1/strategy/")
    print(f"  - 지원 도구: http://localhost:{port}/api/v1/support/")
    
    app.run(host="0.0.0.0", port=port, debug=debug)
