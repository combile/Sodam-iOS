//
//  APIService.swift
//  SodamProject
//
//  Created by 강윤서 on 9/09/25.
//

import Foundation

class APIService: ObservableObject {
    static let shared = APIService()
    
    private init() {}
    
    // MARK: - Generic Request Method
    private func request<T: Codable>(
        endpoint: APIConfig.Endpoint,
        method: HTTPMethod = .GET,
        body: Data? = nil,
        responseType: T.Type
    ) async throws -> T {
        // URL 인코딩을 올바르게 처리
        guard let url = URL(string: endpoint.fullURL) else {
            print("❌ Invalid URL: \(endpoint.fullURL)")
            throw APIError.invalidURL
        }
        
        print("🌐 Making request to: \(endpoint.fullURL)")
        print("🌐 Method: \(method.rawValue)")
        print("🌐 URL object: \(url)")
        
        var request = URLRequest(url: url)
        request.httpMethod = method.rawValue
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        // User-Agent 추가
        request.setValue("SodamProject/1.0", forHTTPHeaderField: "User-Agent")
        
        if let body = body {
            request.httpBody = body
        }
        
        do {
            print("📤 Sending request...")
            let (data, response) = try await URLSession.shared.data(for: request)
            print("📥 Received response")
            
            guard let httpResponse = response as? HTTPURLResponse else {
                print("❌ Invalid response type")
                throw APIError.invalidResponse
            }
            
            print("📊 Status code: \(httpResponse.statusCode)")
            
            guard 200...299 ~= httpResponse.statusCode else {
                print("❌ HTTP error: \(httpResponse.statusCode)")
                
                // 401 Unauthorized의 경우 특별 처리
                if httpResponse.statusCode == 401 {
                    // 응답 본문에서 에러 메시지 확인
                    if let responseData = String(data: data, encoding: .utf8) {
                        print("❌ 401 Response body: \(responseData)")
                    }
                }
                
                throw APIError.httpError(httpResponse.statusCode)
            }
            
            let decoder = JSONDecoder()
            let result = try decoder.decode(responseType, from: data)
            print("✅ Successfully decoded response")
            return result
        } catch {
            print("❌ Network error: \(error.localizedDescription)")
            print("❌ Error type: \(type(of: error))")
            print("❌ Error details: \(error)")
            if error is APIError {
                throw error
            } else {
                throw APIError.networkError(error)
            }
        }
    }
    
    // MARK: - 인증 API
    
    func login(username: String, password: String) async throws -> AuthResponse {
        // 입력값 검증
        guard !username.isEmpty, !password.isEmpty else {
            throw APIError.invalidRequest("아이디와 비밀번호를 입력해주세요.")
        }
        
        let loginData = LoginRequest(username: username, password: password)
        let jsonData = try JSONEncoder().encode(loginData)
        
        let response = try await request(
            endpoint: .authLogin,
            method: .POST,
            body: jsonData,
            responseType: AuthResponse.self
        )
        
        // 응답 검증
        print("🔍 로그인 응답 검증:")
        print("  - access_token: \(response.access_token != nil ? "있음" : "없음")")
        print("  - user: \(response.user != nil ? "있음" : "없음")")
        print("  - message: \(response.message ?? "없음")")
        print("  - error: \(response.error ?? "없음")")
        print("  - success: \(response.success)")
        
        return response
    }
    
    func register(username: String, email: String, password: String, name: String) async throws -> AuthResponse {
        let registerData = RegisterRequest(username: username, email: email, password: password, name: name)
        let jsonData = try JSONEncoder().encode(registerData)
        return try await request(
            endpoint: .authRegister,
            method: .POST,
            body: jsonData,
            responseType: AuthResponse.self
        )
    }
    
    // MARK: - 상권 진단 API
    
    func getFootTraffic(marketCode: String) async throws -> FootTrafficResponse {
        return try await request(
            endpoint: .footTraffic(marketCode: marketCode),
            responseType: FootTrafficResponse.self
        )
    }
    
    func getCardSales(marketCode: String) async throws -> CardSalesResponse {
        return try await request(
            endpoint: .cardSales(marketCode: marketCode),
            responseType: CardSalesResponse.self
        )
    }
    
    func getSameIndustry(marketCode: String) async throws -> SameIndustryResponse {
        return try await request(
            endpoint: .sameIndustry(marketCode: marketCode),
            responseType: SameIndustryResponse.self
        )
    }
    
    func getBusinessRates(marketCode: String) async throws -> BusinessRatesResponse {
        return try await request(
            endpoint: .businessRates(marketCode: marketCode),
            responseType: BusinessRatesResponse.self
        )
    }
    
    func getDwellTime(marketCode: String) async throws -> DwellTimeResponse {
        return try await request(
            endpoint: .dwellTime(marketCode: marketCode),
            responseType: DwellTimeResponse.self
        )
    }
    
    func getHealthScore(marketCode: String, industry: String? = nil) async throws -> HealthScoreResponse {
        // POST 요청으로 변경하고 industry 파라미터 추가
        var requestBody: [String: Any] = [:]
        
        if let industry = industry, !industry.isEmpty {
            requestBody["industry"] = industry
        }
        
        let jsonData = try JSONSerialization.data(withJSONObject: requestBody)
        
        return try await request(
            endpoint: .healthScore(marketCode: marketCode),
            method: .POST,
            body: jsonData,
            responseType: HealthScoreResponse.self
        )
    }
    
    func getComprehensiveDiagnosis(marketCode: String, category: String? = nil) async throws -> ComprehensiveDiagnosisResponse {
        // POST 요청에 marketCode와 업종 정보 추가
        var requestBody: [String: Any] = ["market_code": marketCode]
        
        if let category = category, !category.isEmpty {
            requestBody["category"] = category
        }
        
        let jsonData = try JSONSerialization.data(withJSONObject: requestBody)
        
        print("🔍 API Request Body: \(requestBody)")
        
        return try await request(
            endpoint: .comprehensiveDiagnosis(marketCode: marketCode),
            method: .POST,
            body: jsonData,
            responseType: ComprehensiveDiagnosisResponse.self
        )
    }
    
    // MARK: - 리스크 분류 API
    
    func classifyRisk(marketCode: String) async throws -> RiskClassificationResponse {
        return try await request(
            endpoint: .riskClassify(marketCode: marketCode),
            responseType: RiskClassificationResponse.self
        )
    }
    
    func getRiskTypes() async throws -> RiskTypesResponse {
        return try await request(
            endpoint: .riskTypes,
            responseType: RiskTypesResponse.self
        )
    }
    
    // MARK: - 전략 카드 API
    
    func generateStrategyCards() async throws -> StrategyCardsResponse {
        return try await request(
            endpoint: .strategyCardsGenerate,
            responseType: StrategyCardsResponse.self
        )
    }
    
    func getSuccessCases() async throws -> SuccessCasesResponse {
        return try await request(
            endpoint: .strategyCardsSuccessCases,
            responseType: SuccessCasesResponse.self
        )
    }
    
    // MARK: - 지원 도구 API
    
    func getSupportCenters() async throws -> SupportCentersResponse {
        return try await request(
            endpoint: .supportCenters,
            responseType: SupportCentersResponse.self
        )
    }
    
    func getExpertConsultation() async throws -> ExpertConsultationResponse {
        return try await request(
            endpoint: .expertConsultation,
            responseType: ExpertConsultationResponse.self
        )
    }
    
    // MARK: - 지도 시각화 API
    
    func getMapHeatmap() async throws -> MapHeatmapResponse {
        return try await request(
            endpoint: .mapHeatmap,
            responseType: MapHeatmapResponse.self
        )
    }
    
    func getMapAnalysisTypes() async throws -> MapAnalysisTypesResponse {
        return try await request(
            endpoint: .mapAnalysisTypes,
            responseType: MapAnalysisTypesResponse.self
        )
    }
}

// MARK: - HTTP Methods
enum HTTPMethod: String {
    case GET = "GET"
    case POST = "POST"
    case PUT = "PUT"
    case DELETE = "DELETE"
}

// MARK: - API Errors
enum APIError: Error, LocalizedError {
    case invalidURL
    case invalidResponse
    case httpError(Int)
    case networkError(Error)
    case decodingError(Error)
    case invalidRequest(String)
    
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .invalidResponse:
            return "Invalid response"
        case .httpError(let code):
            return "HTTP Error: \(code)"
        case .networkError(let error):
            return "Network Error: \(error.localizedDescription)"
        case .decodingError(let error):
            return "Decoding Error: \(error.localizedDescription)"
        case .invalidRequest(let message):
            return message
        }
    }
}
