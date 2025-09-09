//
//  Models.swift
//  SodamProject
//
//  Created by 강윤서 on 9/07/25.
//

import Foundation

// MARK: - Request Models
struct RegisterRequest: Codable {
    let username: String
    let email: String
    let password: String
    let name: String
}

struct LoginRequest: Codable {
    let username: String
    let password: String
}

struct RecsScoreRequest: Codable {
    let features: Features
}

struct Features: Codable {
    let foot_traffic: Double
    let competition: Double?
    let rent_cost: Double?
    let accessibility: Double?
    let demographics: Double?
}

// MARK: - Response Models
struct HealthResponse: Codable {
    let status: String
    let timestamp: String?
}

struct AuthResponse: Codable {
    let access_token: String?
    let message: String?
    let user: User?
    let email: String?
    let error: String?
    
    // success는 더 엄격한 조건으로 판단
    var success: Bool {
        // 에러가 있으면 실패
        if let error = error, !error.isEmpty {
            return false
        }
        
        // 로그인 성공: access_token과 user 정보가 모두 있어야 함
        if access_token != nil && user != nil {
            return true
        }
        
        // 회원가입 성공: 특정 메시지와 함께 user 정보가 있어야 함
        if let message = message, 
           (message == "registered" || message == "User registered successfully"),
           user != nil {
            return true
        }
        
        return false
    }
}

struct RecsScoreResponse: Codable {
    let score: Double
    let recommendation: String?
    let details: [String: Double]?
}

struct RecsSampleResponse: Codable {
    let samples: [SampleData]
}

struct SampleData: Codable {
    let id: String
    let features: Features
    let score: Double
    let location: String?
}

// MARK: - User Model
struct User: Codable, Identifiable, Equatable {
    let id: Int
    let username: String
    let email: String
    let created_at: String?
    var name: String?
    
    // Local-only profile fields (not persisted to backend for now)
    var interests: [String] = []
    var regions: [String] = []
    var phone: String? = nil
    var birth_date: String? = nil
    
    // General initializer for creating User objects
    init(id: Int, username: String, email: String, created_at: String? = nil, name: String? = nil, interests: [String] = [], regions: [String] = [], phone: String? = nil, birth_date: String? = nil) {
        self.id = id
        self.username = username
        self.email = email
        self.created_at = created_at
        self.name = name
        self.interests = interests
        self.regions = regions
        self.phone = phone
        self.birth_date = birth_date
    }
    
    // Custom initializer to handle optional fields
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        id = try container.decode(Int.self, forKey: .id)
        username = try container.decode(String.self, forKey: .username)
        email = try container.decode(String.self, forKey: .email)
        created_at = try container.decodeIfPresent(String.self, forKey: .created_at)
        name = try container.decodeIfPresent(String.self, forKey: .name)
        phone = try container.decodeIfPresent(String.self, forKey: .phone)
        
        // Initialize local fields with default values
        interests = []
        regions = []
        birth_date = nil
    }
    
    // CodingKeys for JSON decoding
    private enum CodingKeys: String, CodingKey {
        case id, username, email, created_at, name, phone
    }
}

// MARK: - 스웨거 API Response Models

// 상권 진단 API 응답 모델들
struct FootTrafficResponse: Codable {
    let data: FootTrafficData?
    let message: String?
}

struct FootTrafficData: Codable {
    let market_code: String
    let foot_traffic_change: Double
    let trend: String
    let period: String
}

struct CardSalesResponse: Codable {
    let data: CardSalesData?
    let message: String?
}

struct CardSalesData: Codable {
    let market_code: String
    let sales_trend: Double
    let growth_rate: Double
    let period: String
}

struct SameIndustryResponse: Codable {
    let data: SameIndustryData?
    let message: String?
}

struct SameIndustryData: Codable {
    let market_code: String
    let same_industry_count: Int
    let density: Double
    let competition_level: String
}

struct BusinessRatesResponse: Codable {
    let data: BusinessRatesData?
    let message: String?
}

struct BusinessRatesData: Codable {
    let market_code: String
    let startup_rate: Double
    let closure_rate: Double
    let net_growth: Double
}

struct DwellTimeResponse: Codable {
    let data: DwellTimeData?
    let message: String?
}

struct DwellTimeData: Codable {
    let market_code: String
    let average_dwell_time: Double
    let trend: String
    let period: String
}

struct HealthScoreResponse: Codable {
    let data: HealthScoreData?
    let message: String?
}

struct HealthScoreData: Codable {
    let market_code: String
    let health_score: Double
    let factors: [String: Double]
    let recommendation: String
}

struct ComprehensiveDiagnosisResponse: Codable {
    let market_code: String
    let overall_score: Double
    let indicators: [String: Double]
    let strengths: [String]
    let weaknesses: [String]
    let recommendations: [String]
}

struct ComprehensiveDiagnosisData: Codable {
    let market_code: String
    let overall_score: Double
    let indicators: [String: Double]
    let strengths: [String]
    let weaknesses: [String]
    let recommendations: [String]
}

// 리스크 분류 API 응답 모델들
struct RiskClassificationResponse: Codable {
    let data: RiskClassificationData?
    let message: String?
}

struct RiskClassificationData: Codable {
    let market_code: String
    let risk_type: String
    let risk_level: String
    let confidence: Double
    let factors: [String: Double]
}

struct RiskTypesResponse: Codable {
    let data: [RiskType]?
    let message: String?
}

struct RiskType: Codable {
    let id: String
    let name: String
    let description: String
    let mitigation_strategies: [String]
}

// 전략 카드 API 응답 모델들
struct StrategyCardsResponse: Codable {
    let data: [StrategyCard]?
    let message: String?
}

struct StrategyCard: Codable {
    let id: String
    let title: String
    let description: String
    let category: String
    let priority: String
    let estimated_impact: String
    let implementation_steps: [String]
}

struct SuccessCasesResponse: Codable {
    let data: [SuccessCase]?
    let message: String?
}

struct SuccessCase: Codable {
    let id: String
    let title: String
    let description: String
    let location: String
    let industry: String
    let results: [String: Double]
    let lessons_learned: [String]
}

// 지원 도구 API 응답 모델들
struct SupportCentersResponse: Codable {
    let data: [SupportCenter]?
    let message: String?
}

struct SupportCenter: Codable {
    let id: String
    let name: String
    let address: String
    let phone: String
    let services: [String]
    let operating_hours: String
}

struct ExpertConsultationResponse: Codable {
    let data: [Expert]?
    let message: String?
}

struct Expert: Codable {
    let id: String
    let name: String
    let specialization: String
    let experience: String
    let availability: String
    let contact: String
}

// 지도 시각화 API 응답 모델들
struct MapHeatmapResponse: Codable {
    let data: MapHeatmapData?
    let message: String?
}

struct MapHeatmapData: Codable {
    let coordinates: [MapCoordinate]
    let intensity_values: [Double]
    let color_scale: [String: String]
}

struct MapCoordinate: Codable {
    let latitude: Double
    let longitude: Double
}

struct MapAnalysisTypesResponse: Codable {
    let data: [String]?
    let message: String?
}

// MARK: - App State Models
@MainActor
class UserManager: ObservableObject {
    @Published var currentUser: User?
    @Published var isLoggedIn: Bool = false
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?
    
    // 임시 회원가입 데이터 저장
    var tempPassword: String = ""
    
    let apiService = APIService.shared
    
    func register(username: String, email: String, password: String, name: String) async {
        isLoading = true
        errorMessage = nil
        
        do {
            let response = try await apiService.register(username: username, email: email, password: password, name: name)
            if response.success, let user = response.user {
                currentUser = user
                isLoggedIn = true
            } else {
                errorMessage = response.message
            }
        } catch {
            errorMessage = error.localizedDescription
        }
        
        isLoading = false
    }
    
    func login(username: String, password: String) async {
        isLoading = true
        errorMessage = nil
        
        do {
            let response = try await apiService.login(username: username, password: password)
            if response.success, let user = response.user {
                currentUser = user
                isLoggedIn = true
            } else {
                errorMessage = response.message
            }
        } catch {
            errorMessage = error.localizedDescription
        }
        
        isLoading = false
    }
    
    func logout() {
        currentUser = nil
        isLoggedIn = false
        errorMessage = nil
    }
}
