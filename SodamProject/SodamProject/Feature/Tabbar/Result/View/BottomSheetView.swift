//
//  BottomSheetView.swift
//  SodamProject
//
//  Created by 강윤서 on 9/1/25.
//

import SwiftUI
import MapKit

struct BottomSheetView: View {
    let selectedLocation: CLLocationCoordinate2D?
    @Binding var selectedCategory: String
    @Binding var selectedSubCategory: String
    @Binding var showSubCategories: Bool
    @Binding var navigateToAnalyze: Bool
    @Binding var showBottomSheet: Bool
    @Binding var isSubmitting: Bool
    @State private var dragOffset: CGFloat = 0
    let onAnalyze: () -> Void

    private let mainCategories = ["전체", "쇼핑업", "숙박업", "식음료업", "여가서비스업", "여행업", "운송업"]
    
    var body: some View {
        VStack(spacing: 0) {
            // 핸들바와 닫기 버튼
            HStack {
                RoundedRectangle(cornerRadius: 2)
                    .fill(Color.gray.opacity(0.3))
                    .frame(width: 40, height: 4)
                
                Spacer()
                
                Button(action: {
                    withAnimation(.spring(response: 0.5, dampingFraction: 0.8)) {
                        showBottomSheet = false
                    }
                }) {
                    Image(systemName: "xmark")
                        .font(.system(size: 16, weight: .medium))
                        .foregroundColor(.gray)
                        .frame(width: 30, height: 30)
                        .background(Color.gray.opacity(0.1))
                        .clipShape(Circle())
                }
            }
            .padding(.top, 8)
            .padding(.horizontal, 20)
            
            VStack(alignment: .leading, spacing: 16) {
                // 위치 정보
                HStack {
                    Image(systemName: "mappin.circle.fill")
                        .foregroundColor(.red)
                        .font(.title2)
                    
                    VStack(alignment: .leading) {
                        Text("진단 위치")
                            .font(.headline)
                        Text("500m 반경 분석")
                            .font(.caption)
                            .foregroundColor(.gray)
                    }
                    
                    Spacer()
                    
                    Image(systemName: "location.fill")
                        .foregroundColor(.blue)
                        .font(.title2)
                    
                    VStack(alignment: .trailing) {
                        Text("내 위치")
                            .font(.headline)
                        Text("현재 위치")
                            .font(.caption)
                            .foregroundColor(.gray)
                    }
                }
                .padding(.horizontal, 20)
                .padding(.top, 16)
                
                // 카테고리 선택
                VStack(alignment: .leading, spacing: 12) {
                    Text("업종 선택")
                        .font(.headline)
                        .padding(.horizontal, 20)
                    
                    LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 2), spacing: 8) {
                        ForEach(mainCategories, id: \.self) { category in
                            CategoryButton(
                                title: category,
                                isSelected: selectedCategory == category,
                                action: {
                                    selectedCategory = category
                                }
                            )
                        }
                    }
                    .padding(.horizontal, 20)
                }
                
                
                // 분석하기 버튼
                VStack(spacing: 0) {
                    Divider()
                        .padding(.horizontal, 20)
                    
                    DefaultButton(
                        title: isSubmitting ? "분석 준비중..." : "분석하기",
                        action: { onAnalyze() },
                        isEnabled: isAnalyzeButtonEnabled && !isSubmitting
                    )
                    .padding(.horizontal, 20)
                    .padding(.vertical, 16)
                }
            }
        }
        .background(Color.white)
        .cornerRadius(20, corners: [.topLeft, .topRight])
        .shadow(color: .black.opacity(0.1), radius: 10, x: 0, y: -5)
        .offset(y: dragOffset)
        .clipped()
        .gesture(
            DragGesture()
                .onChanged { value in
                    if value.translation.height > 0 && !isSubmitting {
                        let maxDrag = UIScreen.main.bounds.height * 0.5
                        dragOffset = min(value.translation.height, maxDrag)
                    }
                }
                .onEnded { value in
                    if !isSubmitting {
                        if value.translation.height > 150 {
                            withAnimation(.spring(response: 0.5, dampingFraction: 0.8)) {
                                showBottomSheet = false
                                dragOffset = 0
                            }
                        } else {
                            withAnimation(.spring(response: 0.5, dampingFraction: 0.8)) {
                                dragOffset = 0
                            }
                        }
                    }
                }
        )
    }
    
    
    private var isAnalyzeButtonEnabled: Bool {
        return !selectedCategory.isEmpty
    }
}

#Preview {
    BottomSheetView(
        selectedLocation: CLLocationCoordinate2D(latitude: 37.5665, longitude: 126.9780),
        selectedCategory: .constant("외식업"),
        selectedSubCategory: .constant("한식음식점"),
        showSubCategories: .constant(true),
        navigateToAnalyze: .constant(false),
        showBottomSheet: .constant(true),
        isSubmitting: .constant(false),
        onAnalyze: {}
    )
    .padding()
}
