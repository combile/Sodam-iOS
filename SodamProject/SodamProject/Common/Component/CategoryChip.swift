//
//  CategoryChip.swift
//  SodamProject
//
//  Created by 강윤서 on 8/12/25.
//

import SwiftUI

struct CategoryChip: View {
    let title: String
    let isSelected: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.system(size: 14, weight: .medium))
                .foregroundColor(isSelected ? .white : .gray)
                .padding(.horizontal, 16)
                .padding(.vertical, 8)
                .background(isSelected ? Color.blue : Color.gray.opacity(0.1))
                .cornerRadius(20)
        }
    }
}

#Preview {
    HStack {
        CategoryChip(title: "전체", isSelected: true) {}
        CategoryChip(title: "카테고리", isSelected: false) {}
    }
    .padding()
}
