//
//  Tabbar.swift
//  SodamProject
//
//  Created by 강윤서 on 8/26/25.
//

import SwiftUI

struct TabItem {
    let id: String
    let title: String
    let systemImage: String
    let selectedColor: Color
    let unselectedColor: Color
    
    init(id: String, title: String, systemImage: String, selectedColor: Color = Color(hex:"#7DDB69"), unselectedColor: Color = Color(hex:"#B0B0B0")) {
        self.id = id
        self.title = title
        self.systemImage = systemImage
        self.selectedColor = selectedColor
        self.unselectedColor = unselectedColor
    }
}

struct Tabbar: View {
    @Binding var selectedTab: String
    let tabItems: [TabItem]
    
    var body: some View {
        HStack {
            ForEach(tabItems, id: \.id) { item in
                TabBarItemView(
                    item: item,
                    isSelected: selectedTab == item.id
                )
                .contentShape(Rectangle())
                .onTapGesture{
                    selectedTab = item.id
                }
                if item.id != tabItems.last?.id {
                    Spacer()
                }
            }
        }
        .padding(.horizontal, 20)
        .padding(.vertical, 12)
        .background(Color.white)
        .overlay(
            Rectangle()
                .frame(height: 0.5)
                .foregroundColor(Color.gray.opacity(0.15)),
            alignment: .top
        )
    }
}

struct TabBarItemView: View {
    let item: TabItem
    let isSelected: Bool

    var body: some View {
        VStack(spacing: 4) {
            Image(systemName: item.systemImage)
                .font(.system(size: 24, weight: .medium))
                .foregroundColor(isSelected ? item.selectedColor : item.unselectedColor)
            Text(item.title)
                .font(.system(size: 12, weight: .medium))
                .foregroundColor(isSelected ? item.selectedColor : item.unselectedColor)
        }
        .frame(maxWidth: .infinity)
        .animation(.easeInOut(duration: 0.2), value: isSelected)
    }
}

