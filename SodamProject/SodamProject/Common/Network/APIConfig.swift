//
//  APIConfig.swift
//  SodamProject
//
//  Created by 강윤서 on 9/09/25.
//

import Foundation

struct APIConfig {
    static let baseURL = "http://192.168.219.101:5001"
    
    enum Endpoint {
        // 인증 API
        case authLogin
        case authRegister
        
        // 상권 진단 핵심 지표 API
        case footTraffic(marketCode: String)
        case cardSales(marketCode: String)
        case sameIndustry(marketCode: String)
        case businessRates(marketCode: String)
        case dwellTime(marketCode: String)
        case healthScore(marketCode: String)
        case comprehensiveDiagnosis(marketCode: String)
        
        // 리스크 분류 시스템 API
        case riskClassify(marketCode: String)
        case riskDetailedAnalysis(marketCode: String)
        case riskTypes
        case mitigationStrategies
        
        // 전략 카드 시스템 API
        case strategyCardsGenerate
        case strategyCardsChecklist(strategyId: String)
        case strategyCardsSuccessCases
        case strategyCardsTemplates
        case strategyCardsCategories
        
        // 실행 지원 도구 API
        case supportCenters
        case expertConsultation
        case policyRecommendations
        case successCases
        case consultationBooking
        case policyApplication
        
        // 지도 기반 시각화 API
        case mapHeatmap
        case mapRadiusAnalysis
        case mapClusterAnalysis
        case mapTrafficFlow(marketCode: String)
        case mapAccessibility(marketCode: String)
        case mapAnalysisTypes
        
        var path: String {
            switch self {
            // 인증 API
            case .authLogin:
                return "/api/v1/sodam/auth/login"
            case .authRegister:
                return "/api/v1/sodam/auth/register"
                
            // 상권 진단 핵심 지표 API
            case .footTraffic(let marketCode):
                return "/api/v1/sodam/core-diagnosis/foot-traffic/\(marketCode)"
            case .cardSales(let marketCode):
                return "/api/v1/sodam/core-diagnosis/card-sales/\(marketCode)"
            case .sameIndustry(let marketCode):
                return "/api/v1/sodam/core-diagnosis/same-industry/\(marketCode)"
            case .businessRates(let marketCode):
                return "/api/v1/sodam/core-diagnosis/business-rates/\(marketCode)"
            case .dwellTime(let marketCode):
                return "/api/v1/sodam/core-diagnosis/dwell-time/\(marketCode)"
            case .healthScore(let marketCode):
                return "/api/v1/sodam/core-diagnosis/health-score/\(marketCode)"
            case .comprehensiveDiagnosis(let marketCode):
                return "/api/v1/sodam/core-diagnosis/comprehensive/\(marketCode)"
                
            // 리스크 분류 시스템 API
            case .riskClassify(let marketCode):
                return "/api/v1/sodam/risk-classification/classify/\(marketCode)"
            case .riskDetailedAnalysis(let marketCode):
                return "/api/v1/sodam/risk-classification/detailed-analysis/\(marketCode)"
            case .riskTypes:
                return "/api/v1/sodam/risk-classification/risk-types"
            case .mitigationStrategies:
                return "/api/v1/sodam/risk-classification/mitigation-strategies"
                
            // 전략 카드 시스템 API
            case .strategyCardsGenerate:
                return "/api/v1/sodam/strategy-cards/generate"
            case .strategyCardsChecklist(let strategyId):
                return "/api/v1/sodam/strategy-cards/checklist/\(strategyId)"
            case .strategyCardsSuccessCases:
                return "/api/v1/sodam/strategy-cards/success-cases"
            case .strategyCardsTemplates:
                return "/api/v1/sodam/strategy-cards/templates"
            case .strategyCardsCategories:
                return "/api/v1/sodam/strategy-cards/categories"
                
            // 실행 지원 도구 API
            case .supportCenters:
                return "/api/v1/sodam/support-tools/support-centers"
            case .expertConsultation:
                return "/api/v1/sodam/support-tools/expert-consultation"
            case .policyRecommendations:
                return "/api/v1/sodam/support-tools/policy-recommendations"
            case .successCases:
                return "/api/v1/sodam/support-tools/success-cases"
            case .consultationBooking:
                return "/api/v1/sodam/support-tools/consultation-booking"
            case .policyApplication:
                return "/api/v1/sodam/support-tools/policy-application"
                
            // 지도 기반 시각화 API
            case .mapHeatmap:
                return "/api/v1/sodam/map-visualization/heatmap"
            case .mapRadiusAnalysis:
                return "/api/v1/sodam/map-visualization/radius-analysis"
            case .mapClusterAnalysis:
                return "/api/v1/sodam/map-visualization/cluster-analysis"
            case .mapTrafficFlow(let marketCode):
                return "/api/v1/sodam/map-visualization/traffic-flow/\(marketCode)"
            case .mapAccessibility(let marketCode):
                return "/api/v1/sodam/map-visualization/accessibility/\(marketCode)"
            case .mapAnalysisTypes:
                return "/api/v1/sodam/map-visualization/analysis-types"
            }
        }
        
        var fullURL: String {
            return APIConfig.baseURL + path
        }
    }
}
