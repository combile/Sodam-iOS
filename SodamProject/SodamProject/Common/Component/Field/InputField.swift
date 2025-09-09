//
//  InputField.swift
//  SodamProject
//
//  Created by 강윤서 on 8/12/25.
//

import SwiftUI

struct InputField: View {
    let placeholder: String
    @Binding var text: String
    var isSecure: Bool = false
    var keyboardType: UIKeyboardType = .default
    var placeholderColor: Color = Color(red: 0.39, green: 0.45, blue: 0.55)
    var strokeColor: Color = Color(red: 0.39, green: 0.45, blue: 0.55).opacity(0.55)
    var textColor: Color = Color.black
       
    @FocusState private var isFocused: Bool
    
    var body: some View {
        ZStack(alignment: .leading) {
            if text.isEmpty {
                Text(placeholder)
                    .font(.custom("Inter", size: 13))
                    .foregroundColor(placeholderColor)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding(.vertical, 12)
                    .padding(.horizontal, 16)
            }
            Group {
                if isSecure {
                    SecureField("", text: $text)
                        .focused($isFocused)
                        .keyboardType(keyboardType)
                } else {
                    TextField("", text: $text)
                        .focused($isFocused)
                        .keyboardType(keyboardType)
                }
            }
            .padding(.vertical, 12)
            .padding(.horizontal, 16)
            .foregroundColor(textColor)
        }
        .background(Color.white)
        .overlay(
            RoundedRectangle(cornerRadius: 10)
                .stroke(isFocused ? Color.blue : strokeColor, lineWidth: 1)
        )
        .cornerRadius(10)
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}


