//
//  AnalyzeView.swift
//  SodamProject
//
//  Created by 강윤서 on 9/1/25.
//

import SwiftUI
import Foundation

struct AnalyzeView: View {
    @EnvironmentObject var userManager: UserManager
    let initialRegion: String?
    let initialCategory: String?
    @State private var region: String = "강남구"
    @State private var score: Double = 0.0
    @State private var recommendations: [String] = []
    @State private var strengths: [String] = []
    @State private var weaknesses: [String] = []
    @State private var details: [String: Double] = [:]
    @State private var isLoading: Bool = false
    @State private var errorMessage: String? = nil 
    
    init(region: String? = nil, category: String? = nil) {
        self.initialRegion = region
        self.initialCategory = category
    }
    
    var scorePercentage: Int {
        Int(score * 100)
    }
    
    var scoreColor: Color {
        switch score {
        case 0.8...1.0:
            return Color(red: 0.2, green: 0.7, blue: 0.3) // 진한 초록
        case 0.6..<0.8:
            return Color(red: 1.0, green: 0.6, blue: 0.0) // 주황
        case 0.4..<0.6:
            return Color(red: 1.0, green: 0.4, blue: 0.0) // 빨간 주황
        default:
            return Color(red: 0.9, green: 0.2, blue: 0.2) // 빨강
        }
    }
    
    
    var scoreDescription: String {
        switch score {
        case 0.8...1.0:
            return "매우 우수한 상권입니다"
        case 0.6..<0.8:
            return "양호한 상권입니다"
        case 0.4..<0.6:
            return "보통 수준의 상권입니다"
        default:
            return "신중한 검토가 필요한 상권입니다"
        }
    }
    
    private func getKoreanLabel(for key: String) -> String {
        switch key.lowercased() {
        case "foot_traffic":
            return "유동인구 변화량"
        case "card_sales":
            return "카드매출 변화량"
        case "business_rates":
            return "창업·폐업 비율"
        case "dwell_time":
            return "체류시간"
        case "competition":
            return "경쟁도"
        case "population_density":
            return "인구 밀도"
        case "competition_level":
            return "경쟁 수준"
        case "accessibility":
            return "접근성"
        case "rent_cost":
            return "임대료"
        case "survival_rate":
            return "생존율"
        case "growth_potential":
            return "성장 잠재력"
        case "risk_level":
            return "리스크 수준"
        case "competition_intensity":
            return "경쟁 강도"
        case "economic_indicators":
            return "경제 지표"
        case "demographics":
            return "인구 통계"
        case "infrastructure":
            return "인프라"
        default:
            return key
        }
    }
    
    private func getDescription(for key: String) -> String {
        switch key.lowercased() {
        case "foot_traffic":
            return "월평균 유동인구 변화율"
        case "card_sales":
            return "월평균 카드매출 변화율"
        case "business_rates":
            return "창업·폐업 비율과 상권 활력도"
        case "dwell_time":
            return "고객 평균 체류시간"
        case "competition":
            return "동일업종 경쟁 수준"
        case "population_density":
            return "지역 인구 밀도"
        case "competition_level":
            return "상권 내 경쟁 수준"
        case "accessibility":
            return "교통편 및 접근성"
        case "rent_cost":
            return "임대료 수준"
        case "survival_rate":
            return "업종별 생존율"
        case "growth_potential":
            return "업종 성장 잠재력"
        case "risk_level":
            return "업종 리스크 수준"
        case "competition_intensity":
            return "업종 내 경쟁 강도"
        case "economic_indicators":
            return "지역 경제 지표"
        case "demographics":
            return "지역 인구 통계"
        case "infrastructure":
            return "지역 인프라 수준"
        default:
            return "상세 분석 결과"
        }
    }
    
    private func getUnit(for key: String) -> String {
        switch key.lowercased() {
        case "foot_traffic":
            return "%"
        case "card_sales":
            return "%"
        case "business_rates":
            return "점"
        case "dwell_time":
            return "분"
        case "competition":
            return "점"
        case "population_density":
            return "명/km²"
        case "competition_level":
            return "점"
        case "accessibility":
            return "점"
        case "rent_cost":
            return "원"
        case "survival_rate":
            return "%"
        case "growth_potential":
            return "점"
        case "risk_level":
            return "점"
        case "competition_intensity":
            return "점"
        case "economic_indicators":
            return "점"
        case "demographics":
            return "점"
        case "infrastructure":
            return "점"
        default:
            return "점"
        }
    }
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    // 헤더 정보
                    VStack(alignment: .leading, spacing: 8) {
                        HStack {
                            Image(systemName: "location.circle.fill")
                                .foregroundColor(.blue)
                                .font(.title2)
                            Text("분석 지역")
                                .font(.headline)
                                .foregroundColor(.secondary)
                        }
                        
                        Text(region)
                            .font(.title2)
                            .fontWeight(.bold)
                            .foregroundColor(.primary)
                    }
                    .padding(.horizontal, 20)
                    .padding(.top, 10)
                
                    if isLoading {
                        VStack(spacing: 16) {
                            ProgressView()
                                .scaleEffect(1.2)
                            Text("분석 데이터를 불러오는 중...")
                                .font(.body)
                                .foregroundColor(.gray)
                        }
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                        .padding(.vertical, 60)
                    } else if let errorMessage = errorMessage {
                        VStack(spacing: 12) {
                            Image(systemName: "exclamationmark.triangle.fill")
                                .font(.largeTitle)
                                .foregroundColor(.red)
                            Text("오류 발생")
                                .font(.headline)
                                .foregroundColor(.red)
                            Text(errorMessage)
                                .font(.body)
                                .foregroundColor(.gray)
                                .multilineTextAlignment(.center)
                        }
                        .padding(.horizontal, 20)
                        .padding(.vertical, 40)
                    } else {
                        // 메인 점수 카드
                        VStack(spacing: 20) {
                            // 점수 원형 차트
                            VStack(spacing: 16) {
                                ZStack {
                                    // 배경 원
                                    Circle()
                                        .stroke(Color.gray.opacity(0.2), lineWidth: 12)
                                        .frame(width: 160, height: 160)
                                    
                                    // 점수 원
                                    Circle()
                                        .trim(from: 0, to: score)
                                        .stroke(
                                            LinearGradient(
                                                gradient: Gradient(colors: [scoreColor.opacity(0.7), scoreColor]),
                                                startPoint: .topLeading,
                                                endPoint: .bottomTrailing
                                            ),
                                            style: StrokeStyle(lineWidth: 12, lineCap: .round)
                                        )
                                        .frame(width: 160, height: 160)
                                        .rotationEffect(.degrees(-90))
                                        .animation(.easeInOut(duration: 1.5), value: score)
                                    
                                    // 점수 텍스트
                                    VStack(spacing: 4) {
                                        Text("\(scorePercentage)")
                                            .font(.system(size: 36, weight: .bold, design: .rounded))
                                            .foregroundColor(scoreColor)
                                        Text("점")
                                            .font(.system(size: 16, weight: .medium))
                                            .foregroundColor(.secondary)
                                    }
                                }
                                
                                // 점수 설명
                                VStack(spacing: 8) {
                                    Text(scoreDescription)
                                        .font(.headline)
                                        .foregroundColor(.primary)
                                        .multilineTextAlignment(.center)
                                    
                                    Text("상권의 전반적인 건강도를 0-100점으로 나타낸 결과입니다")
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                        .multilineTextAlignment(.center)
                                }
                            }
                            
                            // 추천사항
                            if !recommendations.isEmpty {
                                VStack(alignment: .leading, spacing: 12) {
                                    HStack {
                                        Image(systemName: "lightbulb.fill")
                                            .foregroundColor(.yellow)
                                        Text("추천사항")
                                            .font(.headline)
                                            .fontWeight(.semibold)
                                    }
                                    
                                    ForEach(Array(recommendations.enumerated()), id: \.offset) { index, rec in
                                        HStack(alignment: .top, spacing: 12) {
                                            Text("\(index + 1)")
                                                .font(.caption)
                                                .fontWeight(.bold)
                                                .foregroundColor(.white)
                                                .frame(width: 20, height: 20)
                                                .background(scoreColor)
                                                .clipShape(Circle())
                                            
                                            Text(rec)
                                                .font(.body)
                                                .foregroundColor(.primary)
                                                .fixedSize(horizontal: false, vertical: true)
                                            
                                            Spacer()
                                        }
                                        .padding(.vertical, 8)
                                    }
                                }
                                .padding(16)
                                .background(Color(.systemGray6))
                                .cornerRadius(12)
                            }
                        }
                        .padding(20)
                        .background(
                            RoundedRectangle(cornerRadius: 20)
                                .fill(Color(.systemBackground))
                                .shadow(color: Color.black.opacity(0.1), radius: 10, x: 0, y: 5)
                        )
                        
                        // 상세 정보 섹션
                        VStack(alignment: .leading, spacing: 20) {
                            // 지표별 점수
                            if !details.isEmpty {
                                VStack(alignment: .leading, spacing: 16) {
                                    HStack {
                                        Image(systemName: "chart.bar.fill")
                                            .foregroundColor(.blue)
                                        Text("지표별 분석")
                                            .font(.headline)
                                            .fontWeight(.bold)
                                    }
                                    
                                    VStack(spacing: 12) {
                                        ForEach(Array(details.keys.sorted()), id: \.self) { key in
                                            HStack {
                                                VStack(alignment: .leading, spacing: 4) {
                                                    Text(getKoreanLabel(for: key))
                                                        .font(.body)
                                                        .fontWeight(.medium)
                                                    Text(getDescription(for: key))
                                                        .font(.caption)
                                                        .foregroundColor(.secondary)
                                                }
                                                
                                                Spacer()
                                                
                                                VStack(alignment: .trailing, spacing: 4) {
                                                    Text("\(Int(details[key]!))")
                                                        .font(.title2)
                                                        .fontWeight(.bold)
                                                        .foregroundColor(scoreColor)
                                                    Text(getUnit(for: key))
                                                        .font(.caption)
                                                        .foregroundColor(.secondary)
                                                }
                                            }
                                            .padding(16)
                                            .background(
                                                RoundedRectangle(cornerRadius: 12)
                                                    .fill(Color(.systemGray6))
                                            )
                                        }
                                    }
                                }
                                .padding(.horizontal, 20)
                            }
                            
                            // 강점
                            if !strengths.isEmpty {
                                VStack(alignment: .leading, spacing: 16) {
                                    HStack {
                                        Image(systemName: "checkmark.circle.fill")
                                            .foregroundColor(.green)
                                        Text("강점")
                                            .font(.headline)
                                            .fontWeight(.bold)
                                            .foregroundColor(.green)
                                    }
                                    
                                    VStack(spacing: 12) {
                                        ForEach(Array(strengths.enumerated()), id: \.offset) { index, strength in
                                            HStack(alignment: .top, spacing: 12) {
                                                Image(systemName: "checkmark.circle.fill")
                                                    .foregroundColor(.green)
                                                    .font(.title3)
                                                
                                                Text(strength)
                                                    .font(.body)
                                                    .foregroundColor(.primary)
                                                    .fixedSize(horizontal: false, vertical: true)
                                                
                                                Spacer()
                                            }
                                            .padding(16)
                                            .background(
                                                RoundedRectangle(cornerRadius: 12)
                                                    .fill(Color.green.opacity(0.1))
                                            )
                                        }
                                    }
                                }
                                .padding(.horizontal, 20)
                            }
                            
                            // 약점
                            if !weaknesses.isEmpty {
                                VStack(alignment: .leading, spacing: 16) {
                                    HStack {
                                        Image(systemName: "exclamationmark.triangle.fill")
                                            .foregroundColor(.orange)
                                        Text("개선점")
                                            .font(.headline)
                                            .fontWeight(.bold)
                                            .foregroundColor(.orange)
                                    }
                                    
                                    VStack(spacing: 12) {
                                        ForEach(Array(weaknesses.enumerated()), id: \.offset) { index, weakness in
                                            HStack(alignment: .top, spacing: 12) {
                                                Image(systemName: "exclamationmark.triangle.fill")
                                                    .foregroundColor(.orange)
                                                    .font(.title3)
                                                
                                                Text(weakness)
                                                    .font(.body)
                                                    .foregroundColor(.primary)
                                                    .fixedSize(horizontal: false, vertical: true)
                                                
                                                Spacer()
                                            }
                                            .padding(16)
                                            .background(
                                                RoundedRectangle(cornerRadius: 12)
                                                    .fill(Color.orange.opacity(0.1))
                                            )
                                        }
                                    }
                                }
                                .padding(.horizontal, 20)
                            }
                        }
                    }
                }
            }
            .navigationTitle("분석 결과")
            .navigationBarTitleDisplayMode(.inline)
            .onAppear {
                if let r = initialRegion, !r.isEmpty { 
                    region = r 
                }
                initializeAndFetch()
            }
        }
    }
    
    private func initializeAndFetch() {
        Task { await fetchScore() }
    }
    
    // 상권명을 숫자 코드로 변환하는 함수
    private func convertLocationToMarketCode(_ location: String) -> String? {
        let marketCodeMapping: [String: String] = [
            "대전느리울중학교": "10435",
            "유성고속터미널": "10436",
            "시청역6번 출구": "10437",
            "대전역1번 출구": "10438",
            "중앙로역7번 출구": "10439",
            "대전 중리전통시장": "10440",
            "대전시청": "10441",
            "대전 시청": "10441",
            "대전역": "10438",
            "시청역": "10437",
            "중앙로역": "10439",
            "유성고속": "10436",
            "느리울중학교": "10435",
            "중리전통시장": "10440"
        ]
        
        // 정확한 매칭 시도
        if let code = marketCodeMapping[location] {
            return code
        }
        
        // 부분 매칭 시도 (포함된 키워드로 검색)
        for (key, code) in marketCodeMapping {
            if location.contains(key) || key.contains(location) {
                return code
            }
        }
        
        return nil
    }
    
    private func fetchScore() async {
        isLoading = true
        errorMessage = nil
        
        print("🔍 AnalyzeView - Region: \(region)")
        print("🔍 AnalyzeView - InitialRegion: \(initialRegion ?? "nil")")
        
        do {
            // 상권명을 숫자 코드로 변환
            let marketCode = convertLocationToMarketCode(region) ?? region
            print("🔍 Using marketCode: \(marketCode)")
            
            // category만 사용
            let category = initialCategory ?? "전체"
            
            let diagnosisResponse = try await APIService.shared.getComprehensiveDiagnosis(
                marketCode: marketCode,
                category: category
            )
            
            print("🔍 Raw response: \(diagnosisResponse)")
            print("🔍 Score received: \(diagnosisResponse.overall_score)")
            
            await MainActor.run {
                print("📊 Score received: \(diagnosisResponse.overall_score)")
                // 점수가 100을 초과하는 경우 100으로 제한, 0 미만인 경우 0으로 제한
                let rawScore = diagnosisResponse.overall_score
                let normalizedScore = max(0.0, min(rawScore, 100.0))
                self.score = normalizedScore / 100.0 // 백분율을 소수로 변환 (0.0 ~ 1.0)
                self.recommendations = diagnosisResponse.recommendations
                self.strengths = diagnosisResponse.strengths
                self.weaknesses = diagnosisResponse.weaknesses
                // 지표별 점수 그대로 사용 (이미 0-100 범위)
                self.details = diagnosisResponse.indicators
                
                print("📊 Score converted: \(self.score)")
                print("📊 Score percentage: \(self.scorePercentage)")
                print("📊 Recommendations: \(self.recommendations)")
                print("📊 Strengths: \(self.strengths)")
                print("📊 Weaknesses: \(self.weaknesses)")
            }
        } catch {
            await MainActor.run {
                self.errorMessage = error.localizedDescription
            }
        }
        
        await MainActor.run {
            self.isLoading = false
        }
    }
}


#Preview {
    AnalyzeView()
        .environmentObject(UserManager())
}
