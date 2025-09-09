//
//  Banner.swift
//  SodamProject
//
//  Created by 강윤서 on 9/5/25.
//

import SwiftUI

struct PolicyBanner: Identifiable, Hashable {
    let id = UUID()
    let title: String
    let subtitle: String
    let theme: BannerTheme
}

enum BannerTheme: Hashable {
    case blue, green, purple, orange

    var gradient: LinearGradient {
        // 배경색 제거 - 투명하게 설정
        return LinearGradient(
            colors: [Color.clear, Color.clear],
            startPoint: .topLeading, endPoint: .bottomTrailing
        )
    }

    var iconName: String {
        switch self {
        case .blue: return "lightbulb.fill"
        case .green: return "leaf.fill"
        case .purple: return "sparkles"
        case .orange: return "building.columns.fill"
        }
    }
}

struct PolicyBannerView: View {
    let banner: PolicyBanner

    var body: some View {
        HStack(alignment: .center, spacing: 16) {
            // Icon
            Image(systemName: banner.theme.iconName)
                .font(.system(size: 32, weight: .medium))
                .foregroundStyle(getIconColor())
                .frame(width: 48, height: 48)
                .background(getIconBackgroundColor())
                .clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))
                .shadow(color: Color.black.opacity(0.08), radius: 2, x: 0, y: 1)

            // Texts
            VStack(alignment: .leading, spacing: 6) {
                Text(banner.title)
                    .font(.system(size: 18, weight: .bold))
                    .foregroundStyle(getTextColor())
                    .lineLimit(1)

                Text(banner.subtitle)
                    .font(.system(size: 14, weight: .medium))
                    .foregroundStyle(getSubtitleColor())
                    .lineLimit(2)
            }

            Spacer(minLength: 0)
        }
        .padding(16)
        .frame(height: 172)
        .background(Color(hex: "#F5F5F5").opacity(0.3))
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(getBorderColor(), lineWidth: 0.5)
        )
        .cornerRadius(12)
        .shadow(color: Color.black.opacity(0.05), radius: 4, x: 0, y: 2)
        .padding(.horizontal, 0) // 외부에서 frame을 감쌀 때 간격 제어
    }
    
    // MARK: - Color Helpers
    private func getIconColor() -> Color {
        return Color(hex: "#6B7280") // 연한 회색
    }
    
    private func getIconBackgroundColor() -> Color {
        return Color(hex: "#F3F4F6") // 매우 연한 회색
    }
    
    private func getTextColor() -> Color {
        return Color(hex: "#374151") // 진한 회색
    }
    
    private func getSubtitleColor() -> Color {
        return Color(hex: "#6B7280") // 연한 회색
    }
    
    private func getBorderColor() -> Color {
        return Color(hex: "#D1D5DB") // 연한 회색 테두리
    }
}

struct BannerCarouselView: View {
    let banners: [PolicyBanner]
    @State private var current = 0

    var body: some View {
        TabView(selection: $current) {
            ForEach(Array(banners.enumerated()), id: \.offset) { index, item in
                PolicyBannerView(banner: item)
                    .padding(.horizontal, 0)
                    .tag(index)
            }
        }
        .tabViewStyle(.page(indexDisplayMode: .automatic))
        .frame(height: 172)
        .animation(.easeInOut, value: current)
        .accessibilityLabel("정책 배너 캐러셀")
    }
}

enum BannerData {
    static let samples: [PolicyBanner] = [
        PolicyBanner(
            title: "청년 창업 지원금",
            subtitle: "사업화 자금 최대 1,000만원 • 교육/멘토링 포함",
            theme: .blue
        ),
        PolicyBanner(
            title: "디지털 전환 지원",
            subtitle: "스마트상점·배달앱 연동 등 디지털화 비용 지원",
            theme: .purple
        ),
        PolicyBanner(
            title: "소상공인 저금리 대출",
            subtitle: "연 2%대 융자 프로그램 • 보증료 감면",
            theme: .green
        ),
        PolicyBanner(
            title: "점포 환경개선",
            subtitle: "간판/인테리어/위생설비 개선 비용 일부 지원",
            theme: .orange
        )
    ]
}


#Preview("Banner - Single") {
    PolicyBannerView(banner: BannerData.samples.first!)
        .padding()
        .background(Color(.systemGroupedBackground))
}

#Preview("Banner - Carousel") {
    BannerCarouselView(banners: BannerData.samples)
        .padding(.horizontal, 20)
        .background(Color(.systemGroupedBackground))
}
