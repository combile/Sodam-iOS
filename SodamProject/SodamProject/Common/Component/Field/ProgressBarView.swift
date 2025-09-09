//
//  ProgressBarView.swift
//  SodamProject
//
//  Created by 강윤서 on 8/14/25.
//

import SwiftUI

struct ProgressBarView: View {
    let currentStep: Int
    let totalSteps: Int
    
    var body: some View {
        HStack {
            ForEach(1...totalSteps, id: \.self) { step in
                RoundedRectangle(cornerRadius: 2)
                    .fill(step <= currentStep ? Color(hex: "7DDB69") : Color(hex: "D9D9D9"))
                    .frame(height: 5)
            }
        }
    }
}

