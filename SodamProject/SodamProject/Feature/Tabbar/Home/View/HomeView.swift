//
//  HomeView.swift
//  SodamProject
//
//  Created by 강윤서 on 9/3/25.
//

import SwiftUI

struct HomeView: View {
    @EnvironmentObject var userManager: UserManager
    @State private var selectedTab = "home"
    @State private var isKeyboardVisible = false
    
    let tabItems = [
        TabItem(id:"result", title: "결과", systemImage: "book.fill"),
        TabItem(id:"chat", title: "담소", systemImage: "message.fill"),
        TabItem(id:"home", title: "홈", systemImage: "house.fill"),
        TabItem(id:"notification", title: "알림", systemImage: "bell.fill"),
        TabItem(id:"my", title: "마이", systemImage: "person.fill")
    ]
    
    var body: some View {
        VStack(spacing: 0) {
            TabView(selection: $selectedTab) {
                MyAreaDiagnosisView()
                    .tag("result")
                
                DamsoView()
                    .tag("chat")
                
                homeContent
                    .tag("home")
                
                NotificationView()
                    .tag("notification")
                
                MyView()
                    .tag("my")
            }
            .tabViewStyle(PageTabViewStyle(indexDisplayMode: .never))
            
            if !isKeyboardVisible {
                Tabbar(selectedTab: $selectedTab, tabItems: tabItems)
            }
        }
        .navigationBarHidden(true)
        .ignoresSafeArea(.keyboard, edges: .bottom)
        .onReceive(NotificationCenter.default.publisher(for: UIResponder.keyboardWillShowNotification)) { _ in
            withAnimation(.easeInOut(duration: 0.3)) {
                isKeyboardVisible = true
            }
        }
        .onReceive(NotificationCenter.default.publisher(for: UIResponder.keyboardWillHideNotification)) { _ in
            withAnimation(.easeInOut(duration: 0.3)) {
                isKeyboardVisible = false
            }
        }
    }
    
    private var homeContent: some View {
        NavigationView {
            VStack(spacing: 0) {
                VStack(spacing: 0) {
                    Image("SODAM")
                        .resizable()
                        .scaledToFit()
                        .frame(width: 120, height: 120)
                }
                .padding(.top, 50)
                
                ZStack {
                    BannerCarouselView(banners: BannerData.samples)
                            .padding(.horizontal, 0)
                    }
                    .frame(height: 172)
                    .padding(.bottom, 25)
                
                VStack(spacing: 15) {
                    HStack(spacing: 15) {
                        NavigationLink(destination: MyAreaDiagnosisView()) {
                            MenuCardView(
                                title: "내 상권 진단",
                                subtitle: "'상권 건강 점수' 제공",
                                icon: "Map",
                                cardWidth: 200,
                                cardHeight: 259,
                                iconType: .large
                            )
                        }
                        
                        VStack(spacing: 15) {
                            // 오늘도 사장
                            NavigationLink(destination: TodayBossView()) {
                                MenuCardView(
                                    title: "오늘도 사장",
                                    subtitle: "나의 현재 상권은?",
                                    icon: "Shop",
                                    cardWidth: 155,
                                    cardHeight: 122,
                                    iconType: .medium
                                )
                            }
                            
                            // 내일은 사장
                            NavigationLink(destination: TomorrowBossView()) {
                                MenuCardView(
                                    title: "내일은 사장",
                                    subtitle: "창업 가이드북",
                                    icon: "Rocket",
                                    cardWidth: 155,
                                    cardHeight: 122,
                                    iconType: .medium
                                )
                            }
                        }
                    }
                    
                    HStack(spacing: 15) {
                        NavigationLink(destination: ApplySupportView()) {
                            MenuCardView(
                                title: "나를 위한 지원서",
                                subtitle: "딱 맞춤 정책!",
                                icon: "Apply",
                                cardWidth: 199,
                                cardHeight: 110,
                                iconType: .small
                            )
                        }
                        
                        NavigationLink(destination: DamsoView()) {
                            MenuCardView(
                                title: "질문하기",
                                subtitle: "무엇이든 물어봐",
                                icon: "Chat",
                                cardWidth: 156,
                                cardHeight: 110,
                                iconType: .small
                            )
                        }
                    }
                }
                .padding(.horizontal, 20)
                
                Spacer(minLength: 100)
            }
        }
        .navigationBarHidden(true)
    }
}

struct MenuCardView: View {
    let title: String
    let subtitle: String
    let icon: String
    var cardWidth: CGFloat = 150
    var cardHeight: CGFloat = 140
    var iconSize: CGFloat = 40
    var iconType: CardType = .medium
    var isHighlighted: Bool = false
    var isWide: Bool = false
    
    enum CardType {
        case large // 내 상권 진단
        case medium // 오늘도 사장, 내일은 사장
        case small // 나를 위한 지원서, 질문하기
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: getSpacing()) {
            VStack(alignment: .leading, spacing: 1) {
                Text(title)
                    .font(.system(size: getTitleFontSize(), weight: .bold))
                    .foregroundColor(Color(hex:"#4A4A4A"))
                
                if !subtitle.isEmpty {
                    Text(subtitle)
                        .font(.system(size: getSubtitleFontSize()))
                        .foregroundStyle(Color(hex: "#B0B0B0"))
                        .multilineTextAlignment(.leading)
                }
            }
            Spacer(minLength: 2)
            
            HStack {
                Spacer()
                Image(icon)
                    .resizable()
                    .scaledToFit()
                    .frame(width: getIconSize(), height: getIconSize())
                    .padding(.trailing, getIconTrailingPadding())
                    .padding(.bottom, getIconBottomPadding())
            }
        }
        .padding(.top, getPadding())
        .padding(.horizontal, 15)
        .frame(width: cardWidth, height: cardHeight)
        .background(Color.white)
        .cornerRadius(8)
        .shadow(color: Color.black.opacity(0.1), radius: 4, x:0, y:0)
        .overlay(
            RoundedRectangle(cornerRadius: 8)
                .stroke(isHighlighted ? Color.blue : Color.clear)
        )
    }
    
    private func getSpacing() -> CGFloat {
        switch iconType {
        case .large: return 15
        case .medium: return 0
        case .small: return 0
        }
    }
    
    private func getTitleFontSize() -> CGFloat {
        switch iconType {
        case .large: return 24
        case .medium: return 18
        case .small: return 18
        }
    }
    
    private func getSubtitleFontSize() -> CGFloat {
        switch iconType {
        case .large: return 15
        case .medium: return 12
        case .small: return 12
        }
    }
    
    private func getIconSize() -> CGFloat {
        switch iconType {
        case .large: return 160
        case .medium: return 70
        case .small: return 55
        }
    }
    
    private func getPadding() -> CGFloat {
        switch iconType {
        case .large: return 15
        case .medium: return 15
        case .small: return 15
        }
    }
    
    private func getIconTrailingPadding() -> CGFloat {
        return iconType == .large ? 5 : 2
    }
    
    private func getIconBottomPadding() -> CGFloat {
        switch iconType {
        case .large: return 5
        case .medium: return 12
        case .small: return 12
        }
    }
}


#Preview {
    HomeView()
        .environmentObject(UserManager())
}
