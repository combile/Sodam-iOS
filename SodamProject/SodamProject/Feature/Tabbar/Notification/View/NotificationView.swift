//
//  NotificationView.swift
//  SodamProject
//
//  Created by 강윤서 on 8/26/25.
//

import SwiftUI

struct NotificationView: View {
    @State private var selectedTab: NotificationTab = .myNews
    
    @State private var hasMyNews: Bool = false
    @State private var hasAnnouncements: Bool = false
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                HStack {
                    Text("알림")
                        .font(.title2)
                        .fontWeight(.semibold)
                        .frame(maxWidth: .infinity)
                    Spacer()
                }
                .padding(.top, 20)
                
                HStack(spacing: 10) {
                    TabButton(
                        title: "내 소식",
                        isSelected: selectedTab == .myNews,
                        hasContent: hasMyNews
                    ) {
                        selectedTab = .myNews
                    }
                    
                    TabButton(
                        title: "공지",
                        isSelected: selectedTab == .announcements,
                        hasContent: hasAnnouncements
                    ) {
                        selectedTab = .announcements
                    }
                }
                .padding(.top, 20)
                
                TabView(selection: $selectedTab) {
                    VStack {
                        if hasMyNews {
                            MyNewsContentView()
                        } else {
                            EmptyStateView(
                                message: "내 소식이 없습니다."
                            )
                        }
                    }
                    .tag(NotificationTab.myNews)
                    
                    VStack {
                        if hasAnnouncements {
                            AnnouncementContentView()
                        } else {
                            EmptyStateView(
                                message: "공지가 없습니다."
                            )
                        }
                    }
                    .tag(NotificationTab.announcements)
                }
                .tabViewStyle(.page(indexDisplayMode: .never))
                
                Spacer()
            }
        }
        .toolbar(.hidden, for: .navigationBar)
        .onAppear {
            setupTestData()
        }
    }
    
    private func setupTestData() {
        // 테스트를 위해 데이터 상태 변경
        hasMyNews = true
        hasAnnouncements = true
    }
}

struct TabButton: View {
    let title: String
    let isSelected: Bool
    let hasContent: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            VStack(spacing: 20) {
                Text(title)
                    .font(.system(size: 16, weight: isSelected ? .semibold : .medium))
                    .foregroundStyle(isSelected ? Color(hex: "#7DDB69") : Color(hex: "#C0C0C0"))
                
                Rectangle()
                    .fill(isSelected ? Color(hex: "#7DDB69") : Color.clear)
                    .frame(height: 2)
            }
        }
        .frame(maxWidth: .infinity)
    }
}

struct EmptyStateView: View {
    let message: String
    
    var body: some View {
        VStack(spacing: 20) {
            Spacer()
            
            Text(message)
                .font(.system(size: 16))
                .foregroundColor(Color(hex: "#C0C0C0"))
            
            Spacer()
        }
        .frame(maxWidth: .infinity)
    }
}

struct MyNewsContentView: View {
    let newsItems = [
        NewsItem(
            category: "[나를 위한 지원서]",
            title: "나에게 딱 맞는 창업 지원 정책이 새로 추가됐어요!",
            date: "2025.07.15"
        ),
        NewsItem(
            category: "[내일은 사장]",
            title: "사장님이 되기 위한 다음 단계 : '사업자 등록 준비하기'",
            date: "2025.06.13"
        ),
        NewsItem(
            category: "[내 상권 진단]",
            title: "사장님의 상권, 점심시간 유동인구가 상승 중입니다.",
            date: "2025.05.18"
        ),
        NewsItem(
            category: "[나를 위한 지원서]",
            title: "오늘 마감되는 정책이 있어요 - 3분 만에 신청하기!",
            date: "2025.02.11"
        )
    ]
    
    var body: some View {
        ScrollView {
            LazyVStack(spacing: 0) {
                ForEach(newsItems, id: \.id) { item in
                    NewsItemRow(item: item)
                    Divider()
                }
            }
            .padding(.top, 5)
        }
    }
}

struct AnnouncementContentView: View {
    let announcements = [
        AnnouncementItem(
            category: "[서비스 점검 안내]",
            title: "2025-07-29 02:00~04:00 서비스점검 예정입니다.",
            date: "2025.07.15"
        ),
        AnnouncementItem(
            category: "[업데이트 소식]",
            title: "업무 편의 기능 가이드 더 특별해졌어요!",
            date: "2025.07.14"
        )
    ]
    
    var body: some View {
        ScrollView {
            LazyVStack(spacing: 0) {
                ForEach(announcements, id: \.id) { item in
                    AnnouncementItemRow(item: item)
                    Divider()
                }
            }
            .padding(.top, 20)
        }
    }
}

struct NewsItemRow: View {
    let item: NewsItem
    
    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Circle()
                .fill(Color(hex: "#D0D0D0").opacity(0.2))
                .frame(width: 40, height: 40)
                .overlay(
                    Image(systemName: "bell")
                        .foregroundColor(Color(hex: "#D0D0D0"))
                        .font(.system(size: 20))
                )
            VStack(alignment: .leading, spacing: 4) {
                Text(item.category)
                    .font(.system(size: 15, weight: .medium))
                    .foregroundColor(Color(hex: "#4A4A4A"))
                
                Text(item.title)
                    .font(.system(size: 13))
                    .foregroundColor(.primary)
                    .lineLimit(2)
                
                Text(item.date)
                    .font(.system(size: 12))
                    .foregroundColor(.gray.opacity(0.6))
            }
            
            Spacer()
        }
        .padding(.horizontal, 20)
        .padding(.vertical, 16)
    }
}

struct AnnouncementItemRow: View {
    let item: AnnouncementItem
    
    var body: some View {
        HStack(alignment: .top, spacing: 10) {
            Circle()
                .fill(Color(hex: "#D0D0D0").opacity(0.2))
                .frame(width: 40, height: 40)
                .overlay(
                    Image(systemName: "megaphone")
                        .foregroundColor(Color(hex: "#D0D0D0"))
                        .font(.system(size: 18))
                )
            
            VStack(alignment: .leading, spacing: 4) {
                Text(item.category)
                    .font(.system(size: 15, weight: .medium))
                    .foregroundColor(Color(hex: "#4A4A4A"))
                
                Text(item.title)
                    .font(.system(size: 13))
                    .foregroundColor(.primary)
                    .lineLimit(1)
                
                Text(item.date)
                    .font(.system(size: 12))
                    .foregroundColor(.gray.opacity(0.6))
            }
            Spacer()
        }
        .padding(.horizontal, 20)
        .padding(.vertical, 16)
    }
}

enum NotificationTab: CaseIterable {
    case myNews
    case announcements
}

struct NewsItem {
    let id = UUID()
    let category: String
    let title: String
    let date: String
}

struct AnnouncementItem {
    let id = UUID()
    let category: String
    let title: String
    let date: String
}

#Preview {
    NotificationView()
}
