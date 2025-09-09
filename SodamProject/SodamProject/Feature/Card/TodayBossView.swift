//
//  TodayBossView.swift
//  SodamProject
//
//  Created by 강윤서 on 8/12/25.
//

import SwiftUI

struct TodayBossView: View {
    @EnvironmentObject var userManager: UserManager
    @State private var selectedCategory = "전체"
    @State private var selectedSubCategory = ""
    @State private var showSubCategories = false
    
    private let mainCategories = ["전체", "쇼핑업", "숙박업", "식음료업", "여가서비스업", "여행업", "운송업"]
    private let shoppingSubCategories = ["관광기념품", "대형쇼핑몰", "레저용품쇼핑"]
    private let accommodationSubCategories = ["기타숙박", "캠핑장/펜션", "콘도", "호텔"]
    private let foodSubCategories = ["식음료"]
    private let leisureSubCategories = ["골프장", "관광유원시설", "기타레저", "문화서비스"]
    private let travelSubCategories = ["여행업"]
    private let transportSubCategories = ["렌터카", "수상운송", "육상운송"]
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Header
                HStack {
                    Text("오늘도 사장")
                        .font(.title2)
                        .fontWeight(.bold)
                    Spacer()
                }
                .padding(.horizontal, 20)
                .padding(.top, 20)
                
                ScrollView {
                    VStack(spacing: 20) {
                        // 상권 정보 카드
                        VStack(alignment: .leading, spacing: 16) {
                            HStack {
                                Image(systemName: "map.fill")
                                    .foregroundColor(.blue)
                                    .font(.title2)
                                
                                VStack(alignment: .leading) {
                                    Text("현재 상권 분석")
                                        .font(.headline)
                                    Text("실시간 상권 정보를 확인하세요")
                                        .font(.caption)
                                        .foregroundColor(.gray)
                                }
                                
                                Spacer()
                            }
                            
                            // 간단한 상권 정보 (더미 데이터)
                            HStack(spacing: 20) {
                                VStack {
                                    Text("유동인구")
                                        .font(.caption)
                                        .foregroundColor(.gray)
                                    Text("1,234명")
                                        .font(.title3)
                                        .fontWeight(.bold)
                                        .foregroundColor(.blue)
                                }
                                
                                VStack {
                                    Text("상권 점수")
                                        .font(.caption)
                                        .foregroundColor(.gray)
                                    Text("85점")
                                        .font(.title3)
                                        .fontWeight(.bold)
                                        .foregroundColor(.green)
                                }
                                
                                VStack {
                                    Text("경쟁업체")
                                        .font(.caption)
                                        .foregroundColor(.gray)
                                    Text("12개")
                                        .font(.title3)
                                        .fontWeight(.bold)
                                        .foregroundColor(.orange)
                                }
                                
                                Spacer()
                            }
                        }
                        .padding(20)
                        .background(Color.white)
                        .cornerRadius(12)
                        .shadow(color: .black.opacity(0.1), radius: 4, x: 0, y: 2)
                        .padding(.horizontal, 20)
                        
                        // 업종 선택
                        VStack(alignment: .leading, spacing: 16) {
                            Text("관심 업종 선택")
                                .font(.headline)
                                .padding(.horizontal, 20)
                            
                            LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 2), spacing: 12) {
                                ForEach(mainCategories, id: \.self) { category in
                                    CategoryButton(
                                        title: category,
                                        isSelected: selectedCategory == category,
                                        action: {
                                            selectedCategory = category
                                            selectedSubCategory = ""
                                            showSubCategories = category != "전체"
                                        }
                                    )
                                }
                            }
                            .padding(.horizontal, 20)
                            
                            // 하위 카테고리
                            if showSubCategories {
                                VStack(alignment: .leading, spacing: 12) {
                                    Text("세부 업종")
                                        .font(.subheadline)
                                        .fontWeight(.medium)
                                        .padding(.horizontal, 20)
                                    
                                    LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 2), spacing: 8) {
                                        ForEach(getSubCategories(), id: \.self) { subCategory in
                                            CategoryButton(
                                                title: subCategory,
                                                isSelected: selectedSubCategory == subCategory,
                                                action: {
                                                    selectedSubCategory = subCategory
                                                }
                                            )
                                        }
                                    }
                                    .padding(.horizontal, 20)
                                }
                            }
                        }
                        
                        // 분석하기 버튼
                        NavigationLink(destination: MyAreaDiagnosisView()) {
                            DefaultButton(
                                title: "상권 진단하기",
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
    
    private func getSubCategories() -> [String] {
        switch selectedCategory {
        case "쇼핑업":
            return shoppingSubCategories
        case "숙박업":
            return accommodationSubCategories
        case "식음료업":
            return foodSubCategories
        case "여가서비스업":
            return leisureSubCategories
        case "여행업":
            return travelSubCategories
        case "운송업":
            return transportSubCategories
        default:
            return []
        }
    }
}


#Preview {
    TodayBossView()
        .environmentObject(UserManager())
}
