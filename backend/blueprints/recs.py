from flask import Blueprint, request, jsonify
from ..services.scoring import compute_score

recs_bp = Blueprint("recs", __name__)

@recs_bp.post("/score")
def score():
    data = request.get_json() or {}
    features = data.get("features", {})
    result = compute_score(features)
    return jsonify(result), 200

@recs_bp.get("/sample")
def sample():
    # 샘플 후보지 목록 (프론트엔드 연결 테스트용)
    candidates = [
        {
            "area_id": "S-001",
            "area_name": "서면역 1번 출구",
            "features": {"foot_traffic": 0.75, "competitors_500m": 0.35, "avg_income": 0.6, "rent_cost": 0.45, "age_20s_ratio": 0.65}
        },
        {
            "area_id": "H-002",
            "area_name": "홍대입구 8번 출구",
            "features": {"foot_traffic": 0.82, "competitors_500m": 0.4, "avg_income": 0.7, "rent_cost": 0.55, "age_20s_ratio": 0.8}
        }
    ]
    enriched = []
    for c in candidates:
        result = compute_score(c["features"])
        enriched.append({**c, "score": result["score"], "breakdown": result["breakdown"]})
    return jsonify({"items": enriched}), 200
