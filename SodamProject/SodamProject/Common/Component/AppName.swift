//
//  AppName.swift
//  SodamProject
//
//  Created by 강윤서 on 8/12/25.
//

import SwiftUI

extension Color {
    init(hex: String) {
        let s = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var v: UInt64 = 0
        Scanner(string: s).scanHexInt64(&v)
        let r, g, b: Double
        switch s.count {
        case 6:
            (r, g, b) = (
                Double((v >> 16) & 0xFF) / 255,
                Double((v >> 8) & 0xFF) / 255,
                Double(v & 0xFF) / 255
            )
        default:
            (r, g, b) = (1, 1, 1) // 기본값: 흰색
        }
        self.init(red: r, green: g, blue: b)
    }
}

struct AppName: View {
    var body: some View {
        VStack(spacing: 5) {
            Text("소담")
                .font(.system(size: 34, weight: .bold))
                .foregroundStyle(Self.titleGradient)

            Text("소상공인을 담다,")
                .font(.system(size: 28, weight: .medium))
                .foregroundStyle(Self.titleGradient)
        }
    }

    // Figma 비율 반영: 20% 지점에서 #579DB7 → 100%에서 #7DDB69
    private static let titleGradient = LinearGradient(
        gradient: Gradient(stops: [
            .init(color: Color(hex: "#579DB7"), location: 0.20),
            .init(color: Color(hex: "#7DDB69"), location: 1.00)
        ]),
        startPoint: .leading,
        endPoint: .trailing
    )
}

#Preview {
    AppName()
}

