from datetime import datetime
from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)  # 아이디
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(80), nullable=False)
    nickname = db.Column(db.String(50), nullable=True)  # 닉네임
    password_hash = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.String(20), nullable=False, default='ENTREPRENEUR')  # ENTREPRENEUR, BUSINESS_OWNER
    business_stage = db.Column(db.String(20), nullable=True)  # PLANNING, STARTUP, OPERATING
    phone = db.Column(db.String(20), nullable=True)  # 전화번호
    interested_business_types = db.Column(db.JSON, nullable=True)  # 관심 업종들
    preferred_areas = db.Column(db.JSON, nullable=True)  # 선호 지역들
    profile_image = db.Column(db.String(500), nullable=True)  # 프로필 이미지 URL
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "nickname": self.nickname,
            "userType": self.user_type,
            "businessStage": self.business_stage,
            "phone": self.phone,
            "preferences": {
                "interestedBusinessTypes": self.interested_business_types or [],
                "preferredAreas": self.preferred_areas or []
            },
            "profileImage": self.profile_image,
            "isActive": self.is_active,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat()
        }

# 상권 진단 관련 모델들
class CommercialArea(db.Model):
    """상권 정보"""
    id = db.Column(db.Integer, primary_key=True)
    area_code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    area_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    radius = db.Column(db.Integer, default=500)  # 분석 반경 (미터)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    foot_traffic_data = db.relationship('FootTrafficData', backref='commercial_area', lazy=True, cascade='all, delete-orphan')
    sales_data = db.relationship('SalesData', backref='commercial_area', lazy=True, cascade='all, delete-orphan')
    business_data = db.relationship('BusinessData', backref='commercial_area', lazy=True, cascade='all, delete-orphan')
    risk_analyses = db.relationship('RiskAnalysis', backref='commercial_area', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "area_code": self.area_code,
            "area_name": self.area_name,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "radius": self.radius,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class FootTrafficData(db.Model):
    """유동인구 데이터"""
    id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey('commercial_area.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=월요일, 6=일요일
    hour = db.Column(db.Integer, nullable=False)  # 0-23
    foot_traffic_count = db.Column(db.Integer, nullable=False)
    age_20s = db.Column(db.Integer, default=0)
    age_30s = db.Column(db.Integer, default=0)
    age_40s = db.Column(db.Integer, default=0)
    age_50s = db.Column(db.Integer, default=0)
    age_60s = db.Column(db.Integer, default=0)
    male_count = db.Column(db.Integer, default=0)
    female_count = db.Column(db.Integer, default=0)
    dwell_time_avg = db.Column(db.Float, default=0.0)  # 평균 체류시간 (분)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "area_id": self.area_id,
            "date": self.date.isoformat(),
            "day_of_week": self.day_of_week,
            "hour": self.hour,
            "foot_traffic_count": self.foot_traffic_count,
            "age_20s": self.age_20s,
            "age_30s": self.age_30s,
            "age_40s": self.age_40s,
            "age_50s": self.age_50s,
            "age_60s": self.age_60s,
            "male_count": self.male_count,
            "female_count": self.female_count,
            "dwell_time_avg": self.dwell_time_avg,
            "created_at": self.created_at.isoformat()
        }

class SalesData(db.Model):
    """카드 매출 데이터"""
    id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey('commercial_area.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    business_type = db.Column(db.String(50), nullable=False)  # 업종
    total_sales = db.Column(db.BigInteger, nullable=False)  # 총 매출액
    transaction_count = db.Column(db.Integer, nullable=False)  # 거래 건수
    avg_transaction_amount = db.Column(db.Float, nullable=False)  # 평균 거래액
    age_20s_sales = db.Column(db.BigInteger, default=0)
    age_30s_sales = db.Column(db.BigInteger, default=0)
    age_40s_sales = db.Column(db.BigInteger, default=0)
    age_50s_sales = db.Column(db.BigInteger, default=0)
    age_60s_sales = db.Column(db.BigInteger, default=0)
    male_sales = db.Column(db.BigInteger, default=0)
    female_sales = db.Column(db.BigInteger, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "area_id": self.area_id,
            "date": self.date.isoformat(),
            "business_type": self.business_type,
            "total_sales": self.total_sales,
            "transaction_count": self.transaction_count,
            "avg_transaction_amount": self.avg_transaction_amount,
            "age_20s_sales": self.age_20s_sales,
            "age_30s_sales": self.age_30s_sales,
            "age_40s_sales": self.age_40s_sales,
            "age_50s_sales": self.age_50s_sales,
            "age_60s_sales": self.age_60s_sales,
            "male_sales": self.male_sales,
            "female_sales": self.female_sales,
            "created_at": self.created_at.isoformat()
        }

class BusinessData(db.Model):
    """사업체 데이터 (창업/폐업 정보)"""
    id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey('commercial_area.id'), nullable=False)
    business_type = db.Column(db.String(50), nullable=False)
    business_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'active', 'closed', 'new'
    opened_date = db.Column(db.Date, nullable=True)
    closed_date = db.Column(db.Date, nullable=True)
    rent_cost = db.Column(db.Integer, nullable=True)  # 월 임대료
    floor_area = db.Column(db.Float, nullable=True)  # 면적 (제곱미터)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "area_id": self.area_id,
            "business_type": self.business_type,
            "business_name": self.business_name,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "status": self.status,
            "opened_date": self.opened_date.isoformat() if self.opened_date else None,
            "closed_date": self.closed_date.isoformat() if self.closed_date else None,
            "rent_cost": self.rent_cost,
            "floor_area": self.floor_area,
            "created_at": self.created_at.isoformat()
        }

class RiskAnalysis(db.Model):
    """리스크 분석 결과"""
    id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey('commercial_area.id'), nullable=False)
    business_type = db.Column(db.String(50), nullable=False)
    risk_type = db.Column(db.String(50), nullable=False)  # '유입저조형', '과포화경쟁형', '소비력약형', '성장잠재형'
    risk_score = db.Column(db.Float, nullable=False)  # 0-100 점수
    health_score = db.Column(db.Float, nullable=False)  # 상권 건강 점수
    analysis_data = db.Column(db.JSON, nullable=False)  # 분석 상세 데이터
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "area_id": self.area_id,
            "business_type": self.business_type,
            "risk_type": self.risk_type,
            "risk_score": self.risk_score,
            "health_score": self.health_score,
            "analysis_data": self.analysis_data,
            "created_at": self.created_at.isoformat()
        }

class StrategyCard(db.Model):
    """전략 카드"""
    id = db.Column(db.Integer, primary_key=True)
    risk_type = db.Column(db.String(50), nullable=False)
    business_type = db.Column(db.String(50), nullable=False)
    strategy_category = db.Column(db.String(50), nullable=False)  # '업종전략', '운영전략', '마케팅전략'
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    checklist = db.Column(db.JSON, nullable=True)  # 체크리스트 항목들
    tips = db.Column(db.JSON, nullable=True)  # 실행 팁들
    case_studies = db.Column(db.JSON, nullable=True)  # 성공 사례들
    priority = db.Column(db.Integer, default=1)  # 우선순위
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "risk_type": self.risk_type,
            "business_type": self.business_type,
            "strategy_category": self.strategy_category,
            "title": self.title,
            "description": self.description,
            "checklist": self.checklist,
            "tips": self.tips,
            "case_studies": self.case_studies,
            "priority": self.priority,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat()
        }

class PolicySupport(db.Model):
    """정책 지원 정보"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    target_business_types = db.Column(db.JSON, nullable=True)  # 대상 업종들
    target_areas = db.Column(db.JSON, nullable=True)  # 대상 지역들
    support_amount = db.Column(db.String(100), nullable=True)  # 지원 금액
    application_period = db.Column(db.String(100), nullable=True)  # 신청 기간
    contact_info = db.Column(db.String(200), nullable=True)  # 연락처
    website_url = db.Column(db.String(500), nullable=True)  # 관련 웹사이트
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "target_business_types": self.target_business_types,
            "target_areas": self.target_areas,
            "support_amount": self.support_amount,
            "application_period": self.application_period,
            "contact_info": self.contact_info,
            "website_url": self.website_url,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat()
        }

class ExpertConsultation(db.Model):
    """전문가 상담 예약"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('commercial_area.id'), nullable=False)
    business_type = db.Column(db.String(50), nullable=False)
    consultation_type = db.Column(db.String(50), nullable=False)  # '상권분석', '사업계획', '운영전략'
    preferred_date = db.Column(db.Date, nullable=False)
    preferred_time = db.Column(db.String(20), nullable=False)  # '오전', '오후', '저녁'
    contact_phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'confirmed', 'completed', 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "area_id": self.area_id,
            "business_type": self.business_type,
            "consultation_type": self.consultation_type,
            "preferred_date": self.preferred_date.isoformat(),
            "preferred_time": self.preferred_time,
            "contact_phone": self.contact_phone,
            "message": self.message,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }
