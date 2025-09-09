//
//  SearchView.swift
//  SodamProject
//
//  Created by 강윤서 on 8/15/25.
//

import SwiftUI

struct SearchView: View {
    @State private var searchText = ""
    @State private var selectedCategory = "전체"
    @State private var searchHistory: [String] = []
    
    private let categories = ["전체", "질문", "정보", "후기", "정책"]
    
    private let searchResults = [
        SearchResult(
            title: "초기 창업 비용이 얼마나 들어가나요?",
            category: "질문",
            author: "월매출1억꿈나무",
            timeAgo: "2시간 전",
            views: 34,
            likes: 2
        ),
        SearchResult(
            title: "청년창업지원금 신청 방법",
            category: "정책",
            author: "소상공인지원센터",
            timeAgo: "1일 전",
            views: 156,
            likes: 12
        ),
        SearchResult(
            title: "덕명동 상권 분석 결과",
            category: "정보",
            author: "상권분석가",
            timeAgo: "3일 전",
            views: 89,
            likes: 8
        ),
        SearchResult(
            title: "카페 창업 후기 - 첫 달 매출 공개",
            category: "후기",
            author: "카페사장님",
            timeAgo: "1주 전",
            views: 234,
            likes: 25
        )
    ]
    
    var filteredResults: [SearchResult] {
        var filtered = searchResults
        
        if selectedCategory != "전체" {
            filtered = filtered.filter { $0.category == selectedCategory }
        }
        
        if !searchText.isEmpty {
            filtered = filtered.filter { 
                $0.title.localizedCaseInsensitiveContains(searchText) ||
                $0.author.localizedCaseInsensitiveContains(searchText)
            }
        }
        
        return filtered
    }
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Header
                HStack {
                    Button(action: {}) {
                        Image(systemName: "chevron.left")
                            .font(.title2)
                            .foregroundColor(.primary)
                    }
                    
                    Text("검색")
                        .font(.title2)
                        .fontWeight(.bold)
                        .frame(maxWidth: .infinity)
                    
                    Spacer()
                }
                .padding(.horizontal, 20)
                .padding(.top, 10)
                
                // 검색바
                HStack {
                    Image(systemName: "magnifyingglass")
                        .foregroundColor(.gray)
                        .padding(.leading, 16)
                    
                    TextField("궁금한 것을 검색해보세요", text: $searchText)
                        .padding(.vertical, 12)
                        .padding(.trailing, 16)
                        .textInputAutocapitalization(.never)
                        .autocorrectionDisabled()
                        .onSubmit {
                            if !searchText.isEmpty && !searchHistory.contains(searchText) {
                                searchHistory.insert(searchText, at: 0)
                                if searchHistory.count > 10 {
                                    searchHistory.removeLast()
                                }
                            }
                        }
                }
                .background(Color.gray.opacity(0.1))
                .cornerRadius(25)
                .padding(.horizontal, 20)
                .padding(.top, 16)
                
                if searchText.isEmpty {
                    // 검색 기록
                    if !searchHistory.isEmpty {
                        VStack(alignment: .leading, spacing: 12) {
                            HStack {
                                Text("최근 검색어")
                                    .font(.headline)
                                Spacer()
                                Button("전체 삭제") {
                                    searchHistory.removeAll()
                                }
                                .font(.caption)
                                .foregroundColor(.gray)
                            }
                            .padding(.horizontal, 20)
                            .padding(.top, 20)
                            
                            ScrollView(.horizontal, showsIndicators: false) {
                                HStack(spacing: 8) {
                                    ForEach(searchHistory, id: \.self) { history in
                                        Button(action: {
                                            searchText = history
                                        }) {
                                            Text(history)
                                                .font(.system(size: 14))
                                                .foregroundColor(.primary)
                                                .padding(.horizontal, 12)
                                                .padding(.vertical, 6)
                                                .background(Color.gray.opacity(0.1))
                                                .cornerRadius(15)
                                        }
                                    }
                                }
                                .padding(.horizontal, 20)
                            }
                        }
                    }
                    
                    // 인기 검색어
                    VStack(alignment: .leading, spacing: 12) {
                        Text("인기 검색어")
                            .font(.headline)
                            .padding(.horizontal, 20)
                            .padding(.top, 20)
                        
                        VStack(spacing: 8) {
                            ForEach(["창업 비용", "사업자 등록", "상권 분석", "지원금", "창업 교육"], id: \.self) { keyword in
                                HStack {
                                    Text("\(Array(1...5).firstIndex(of: Array(1...5).randomElement() ?? 1) ?? 1)")
                                        .font(.system(size: 14, weight: .bold))
                                        .foregroundColor(.blue)
                                        .frame(width: 20)
                                    
                                    Text(keyword)
                                        .font(.system(size: 14))
                                        .foregroundColor(.primary)
                                    
                                    Spacer()
                                    
                                    Image(systemName: "arrow.up.left")
                                        .font(.system(size: 12))
                                        .foregroundColor(.gray)
                                }
                                .padding(.horizontal, 20)
                                .padding(.vertical, 8)
                                .background(Color.white)
                                .onTapGesture {
                                    searchText = keyword
                                }
                            }
                        }
                    }
                } else {
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
                    
                    // 검색 결과
                    ScrollView {
                        LazyVStack(spacing: 12) {
                            ForEach(filteredResults, id: \.title) { result in
                                SearchResultCard(result: result)
                            }
                        }
                        .padding(.horizontal, 20)
                        .padding(.top, 20)
                    }
                }
                
                Spacer()
            }
        }
        .navigationBarHidden(true)
    }
}

struct SearchResult {
    let title: String
    let category: String
    let author: String
    let timeAgo: String
    let views: Int
    let likes: Int
}


struct SearchResultCard: View {
    let result: SearchResult
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(result.category)
                    .font(.system(size: 12, weight: .medium))
                    .foregroundColor(.white)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 2)
                    .background(Color.blue)
                    .cornerRadius(4)
                
                Spacer()
                
                Text(result.timeAgo)
                    .font(.system(size: 12))
                    .foregroundColor(.gray)
            }
            
            Text(result.title)
                .font(.system(size: 16, weight: .medium))
                .foregroundColor(.primary)
                .lineLimit(2)
            
            HStack {
                Text(result.author)
                    .font(.system(size: 14))
                    .foregroundColor(.secondary)
                
                Spacer()
                
                HStack(spacing: 12) {
                    HStack(spacing: 4) {
                        Image(systemName: "eye")
                            .font(.system(size: 12))
                            .foregroundColor(.gray)
                        Text("\(result.views)")
                            .font(.system(size: 12))
                            .foregroundColor(.gray)
                    }
                    
                    HStack(spacing: 4) {
                        Image(systemName: "hand.thumbsup")
                            .font(.system(size: 12))
                            .foregroundColor(.gray)
                        Text("\(result.likes)")
                            .font(.system(size: 12))
                            .foregroundColor(.gray)
                    }
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
    SearchView()
}
