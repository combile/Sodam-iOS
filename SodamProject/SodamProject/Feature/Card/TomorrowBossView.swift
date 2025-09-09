//
//  TomorrowBossView.swift
//  SodamProject
//
//  Created by 강윤서 on 8/12/25.
//

import SwiftUI

struct TomorrowBossView: View {
    @EnvironmentObject var userManager: UserManager
    @State private var selectedGuide = 0
    
    private let guides = [
        GuideItem(
            title: "사업자 등록하기",
            description: "개인사업자 vs 법인사업자 선택 가이드",
            icon: "doc.text.fill",
            color: .blue
        ),
        GuideItem(
            title: "창업 자금 마련하기",
            description: "정부 지원금, 대출, 투자 유치 방법",
            icon: "banknote.fill",
            color: .green
        ),
        GuideItem(
            title: "상권 분석하기",
            description: "입지 선정과 경쟁업체 분석 방법",
            icon: "map.fill",
            color: .orange
        ),
        GuideItem(
            title: "사업계획서 작성하기",
            description: "투자자와 은행을 위한 사업계획서",
            icon: "doc.plaintext.fill",
            color: .purple
        ),
        GuideItem(
            title: "마케팅 전략 수립하기",
            description: "디지털 마케팅과 오프라인 홍보",
            icon: "megaphone.fill",
            color: .red
        ),
        GuideItem(
            title: "인력 채용하기",
            description: "직원 채용과 관리 노하우",
            icon: "person.2.fill",
            color: .cyan
        )
    ]
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Header
                HStack {
                    Text("내일은 사장")
                        .font(.title2)
                        .fontWeight(.bold)
                    Spacer()
                }
                .padding(.horizontal, 20)
                .padding(.top, 20)
                
                ScrollView {
                    VStack(spacing: 20) {
                        // 인사말 카드
                        VStack(alignment: .leading, spacing: 16) {
                            HStack {
                                Image(systemName: "rocket.fill")
                                    .foregroundColor(.blue)
                                    .font(.title2)
                                
                                VStack(alignment: .leading) {
                                    Text("창업 가이드북")
                                        .font(.headline)
                                    Text("사장님이 되기 위한 모든 과정을 단계별로 안내해드려요")
                                        .font(.caption)
                                        .foregroundColor(.gray)
                                }
                                
                                Spacer()
                            }
                        }
                        .padding(20)
                        .background(Color.white)
                        .cornerRadius(12)
                        .shadow(color: .black.opacity(0.1), radius: 4, x: 0, y: 2)
                        .padding(.horizontal, 20)
                        
                        // 가이드 리스트
                        LazyVStack(spacing: 12) {
                            ForEach(Array(guides.enumerated()), id: \.offset) { index, guide in
                                GuideCardView(
                                    guide: guide,
                                    stepNumber: index + 1,
                                    isSelected: selectedGuide == index
                                ) {
                                    selectedGuide = index
                                }
                            }
                        }
                        .padding(.horizontal, 20)
                        
                        // 시작하기 버튼
                        NavigationLink(destination: MyAreaDiagnosisView()) {
                            DefaultButton(
                                title: "상권 진단 시작하기",
                                action: {}
                            )
                        }
                        .padding(.horizontal, 20)
                        .padding(.top, 20)
                    }
                }
            }
        }
        .navigationBarHidden(true)
    }
}

struct GuideItem {
    let title: String
    let description: String
    let icon: String
    let color: Color
}

struct GuideCardView: View {
    let guide: GuideItem
    let stepNumber: Int
    let isSelected: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            HStack(spacing: 16) {
                // 단계 번호
                ZStack {
                    Circle()
                        .fill(isSelected ? guide.color : Color.gray.opacity(0.2))
                        .frame(width: 40, height: 40)
                    
                    Text("\(stepNumber)")
                        .font(.system(size: 16, weight: .bold))
                        .foregroundColor(isSelected ? .white : .gray)
                }
                
                // 아이콘
                Image(systemName: guide.icon)
                    .font(.title2)
                    .foregroundColor(guide.color)
                    .frame(width: 30)
                
                // 내용
                VStack(alignment: .leading, spacing: 4) {
                    Text(guide.title)
                        .font(.system(size: 16, weight: .semibold))
                        .foregroundColor(.primary)
                        .multilineTextAlignment(.leading)
                    
                    Text(guide.description)
                        .font(.system(size: 14))
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.leading)
                }
                
                Spacer()
                
                // 화살표
                Image(systemName: "chevron.right")
                    .font(.system(size: 14, weight: .medium))
                    .foregroundColor(.gray)
            }
            .padding(16)
            .background(isSelected ? guide.color.opacity(0.1) : Color.white)
            .cornerRadius(12)
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(isSelected ? guide.color : Color.clear, lineWidth: 2)
            )
            .shadow(color: .black.opacity(0.05), radius: 2, x: 0, y: 1)
        }
    }
}

#Preview {
    TomorrowBossView()
        .environmentObject(UserManager())
}
