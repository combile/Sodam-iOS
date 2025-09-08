from typing import Dict, Any

DEFAULT_WEIGHTS = {
    "foot_traffic": 0.35,
    "competitors_500m": -0.25,
    "avg_income": 0.20,
    "rent_cost": -0.10,
    "age_20s_ratio": 0.10,
}

def compute_score(features: Dict[str, float], weights: Dict[str, float] = None) -> Dict[str, Any]:
    w = weights or DEFAULT_WEIGHTS
    total = 0.0
    breakdown = {}

    for k, weight in w.items():
        v = float(features.get(k, 0.0))
        contrib = v * weight
        breakdown[k] = {"value": round(v, 4), "weight": weight, "contrib": round(contrib, 4)}
        total += contrib

    normalized = max(0.0, min(100.0, (total + 1.0) * 50.0))
    return {"score": round(normalized, 2), "breakdown": breakdown}
