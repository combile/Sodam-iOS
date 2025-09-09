//
//  ApplySupportView.swift
//  SodamProject
//
//  Created by 강윤서 on 8/12/25.
//

import SwiftUI

struct ApplySupportView: View {
    @EnvironmentObject var userManager: UserManager
    @State private var selectedCategory = "전체"
    @State private var searchText = ""
    
    private let categories = ["전체", "창업지원", "자금지원", "교육지원", "기술지원", "마케팅지원"]
    
    private let supportPolicies = [
        SupportPolicy(
            title: "청년창업지원금",
            category: "자금지원",
            amount: "최대 1,000만원",
            deadline: "2025.12.31",
            description: "만 18~39세 청년 창업자 대상",
            isRecommended: true
        ),
        SupportPolicy(
            title: "소상공인 디지털 전환 지원",
            category: "기술지원",
            amount: "최대 500만원",
            deadline: "2025.11.30",
            description: "스마트상점 구축 및 배달앱 연동 지원",
            isRecommended: false
        ),
        SupportPolicy(
            title: "창업교육 프로그램",
            category: "교육지원",
            amount: "무료",
            deadline: "상시",
            description: "창업 기초부터 실무까지 단계별 교육",
            isRecommended: true
        ),
        SupportPolicy(
            title: "소상공인 저금리 대출",
            category: "자금지원",
            amount: "연 2%대",
            deadline: "상시",
            description: "보증료 감면 및 신속 심사",
            isRecommended: false
        ),
        SupportPolicy(
            title: "점포 환경개선 지원",
            category: "기술지원",
            amount: "최대 300만원",
            deadline: "2025.10.31",
            description: "간판, 인테리어, 위생설비 개선 지원",
            isRecommended: false
        ),
        SupportPolicy(
            title: "온라인 마케팅 지원",
            category: "마케팅지원",
            amount: "최대 200만원",
            deadline: "2025.09.30",
            description: "SNS 홍보 및 온라인 광고비 지원",
            isRecommended: true
        )
    ]
    
    var filteredPolicies: [SupportPolicy] {
        var filtered = supportPolicies
        
        if selectedCategory != "전체" {
            filtered = filtered.filter { $0.category == selectedCategory }
        }
        
        if !searchText.isEmpty {
            filtered = filtered.filter { 
                $0.title.localizedCaseInsensitiveContains(searchText) ||
                $0.description.localizedCaseInsensitiveContains(searchText)
            }
        }
        
        return filtered
    }
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Header
                HStack {
                    Text("나를 위한 지원서")
                        .font(.title2)
                        .fontWeight(.bold)
                    Spacer()
                }
                .padding(.horizontal, 20)
                .padding(.top, 20)
                
                // 검색바
                HStack {
                    Image(systemName: "magnifyingglass")
                        .foregroundColor(.gray)
                        .padding(.leading, 16)
                    
                    TextField("지원사업을 검색하세요", text: $searchText)
                        .padding(.vertical, 12)
                        .padding(.trailing, 16)
                        .textInputAutocapitalization(.never)
                        .autocorrectionDisabled()
                }
                .background(Color.white)
                .cornerRadius(25)
                .shadow(color: .black.opacity(0.1), radius: 4, x: 0, y: 2)
                .padding(.horizontal, 20)
                .padding(.top, 16)
                
                // 카테고리 필터
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 12) {
                        ForEach(categories, id: \.self) { category in
                            CategoryChip(
                                title: category,
                                isSelected: selectedCategory == category
                            ) {
                                selectedCategory = category
                            }
                        }
                    }
                    .padding(.horizontal, 20)
                }
                .padding(.top, 16)
                
                // 지원사업 리스트
                ScrollView {
                    LazyVStack(spacing: 12) {
                        ForEach(filteredPolicies, id: \.title) { policy in
                            SupportPolicyCard(policy: policy)
                        }
                    }
                    .padding(.horizontal, 20)
                    .padding(.top, 20)
                }
            }
        }
        .navigationBarHidden(true)
    }
}

struct SupportPolicy {
    let title: String
    let category: String
    let amount: String
    let deadline: String
    let description: String
    let isRecommended: Bool
}


struct SupportPolicyCard: View {
    let policy: SupportPolicy
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    HStack {
                        Text(policy.title)
                            .font(.system(size: 16, weight: .bold))
                            .foregroundColor(.primary)
                        
                        if policy.isRecommended {
                            Text("추천")
                                .font(.system(size: 10, weight: .bold))
                                .foregroundColor(.white)
                                .padding(.horizontal, 6)
                                .padding(.vertical, 2)
                                .background(Color.red)
                                .cornerRadius(4)
                        }
                    }
                    
                    Text(policy.description)
                        .font(.system(size: 14))
                        .foregroundColor(.secondary)
                        .lineLimit(2)
                }
                
                Spacer()
                
                VStack(alignment: .trailing, spacing: 4) {
                    Text(policy.amount)
                        .font(.system(size: 14, weight: .bold))
                        .foregroundColor(.blue)
                    
                    Text(policy.category)
                        .font(.system(size: 12))
                        .foregroundColor(.gray)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 2)
                        .background(Color.gray.opacity(0.1))
                        .cornerRadius(8)
                }
            }
            
            HStack {
                HStack(spacing: 4) {
                    Image(systemName: "calendar")
                        .font(.system(size: 12))
                        .foregroundColor(.gray)
                    
                    Text("마감: \(policy.deadline)")
                        .font(.system(size: 12))
                        .foregroundColor(.gray)
                }
                
                Spacer()
                
                Button(action: {}) {
                    Text("신청하기")
                        .font(.system(size: 14, weight: .medium))
                        .foregroundColor(.white)
                        .padding(.horizontal, 16)
                        .padding(.vertical, 8)
                        .background(Color.blue)
                        .cornerRadius(6)
                }
            }
        }
        .padding(16)
        .background(Color.white)
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.05), radius: 4, x: 0, y: 2)
    }
}

#Preview {
    ApplySupportView()
        .environmentObject(UserManager())
}
