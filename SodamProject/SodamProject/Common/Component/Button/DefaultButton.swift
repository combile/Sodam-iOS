//
//  DefaultButton.swift
//  SodamProject
//
//  Created by 강윤서 on 8/12/25.
//

import SwiftUI

struct DefaultButton: View {
    let title: String
    let action: () -> Void
    
    var backgroundColor: Color = Color(hex: "7DDB69")
    var textColor: Color = .white
    var font: Font = .headline
    var cornerRadius: CGFloat = 12
    var height: CGFloat = 50
    var shadowRadius: CGFloat = 2
    var shadowOffset: CGSize = CGSize(width: 0, height: 2)
    var shadowColor: Color = Color.black.opacity(0.1)
    var isEnabled: Bool = true
    
    @State private var isPressed: Bool = false
    
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(font)
                .fontWeight(.semibold)
                .foregroundColor(textColor)
                .frame(maxWidth: .infinity)
                .frame(height: height)
                .background(
                    RoundedRectangle(cornerRadius: cornerRadius)
                        .fill(isEnabled ? backgroundColor : Color.gray)
                        .scaleEffect(isPressed ? 0.98 : 1.0)
                )
                .shadow(
                    color: shadowColor,
                    radius: shadowRadius,
                    x: shadowOffset.width,
                    y: shadowOffset.height
                )
        }
        .disabled(!isEnabled)
        .scaleEffect(isPressed ? 0.98 : 1.0)
        .onLongPressGesture(minimumDuration: 0, maximumDistance: .infinity, pressing: { pressing in
            withAnimation(.easeInOut(duration: 0.1)) {
                isPressed = pressing
            }
        }, perform: {})
    }
}
