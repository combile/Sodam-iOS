//
//  FindPWView.swift
//  SodamProject
//
//  Created by 강윤서 on 9/3/25.
//

import SwiftUI

struct FindPWView: View {
    @Environment(\.dismiss) private var dismiss
    
    @State private var email: String = ""
    @State private var isSending: Bool = false
    @State private var showSentAlert: Bool = false
    @State private var sent: Bool = false
    @State private var goToLogin: Bool = false
    
    var body: some View {
        VStack(spacing: 40) {
            HStack {
                Button {
                    dismiss()
                } label: {
                    Image(systemName: "chevron.left")
                        .font(.system(size: 20, weight: .semibold))
                        .foregroundColor(Color(hex: "#4A4A4A"))
                }
                Spacer()
                Text("아이디 찾기")
                    .font(.system(size: 20, weight: .semibold))
                    .foregroundColor(Color(hex: "#4A4A4A"))
                Spacer()
            }
            .padding(.horizontal, 20)
            .padding(.vertical, 12)
            
            ScrollView {
                VStack(spacing: 32) {
                    AppName()
                        .padding(.top, 20)
                    
                    VStack(alignment: .leading, spacing: 10) {
                        Text("이메일")
                            .font(.system(size: 14, weight: .medium))
                            .foregroundColor(Color(hex: "#4A4A4A"))
                        
                        InputField(
                            placeholder:"이메일을 입력해주세요",
                            text: $email,
                            isSecure: false,
                            keyboardType: .emailAddress
                        )
                    }
                    .padding(.horizontal, 20)
                    
                    VStack(alignment: .leading, spacing: 10) {
                        Text("아이디")
                            .font(.system(size: 14, weight: .medium))
                            .foregroundColor(Color(hex: "#4A4A4A"))
                        
                        InputField(
                            placeholder:"이메일을 입력해주세요",
                            text: $email,
                            isSecure: false,
                            keyboardType: .emailAddress
                        )
                    }
                    .padding(.horizontal, 20)
                    
                    Spacer(minLength: 0)
                    
                    VStack(alignment: .leading, spacing: 10) {
                        if sent {
                            DefaultButton(title: "로그인하러가기", action: {goToLogin = true}
                            )
                        } else {
                            DefaultButton(
                                title: isSending ? "전송 중..." : "인증하기",
                                action: sendRequest,
                                isEnabled: isValidEmail(email) && !isSending
                            )
                        }
                    }
                    .padding(.horizontal, 20)
                    .padding(.vertical, 16)
                }
                .frame(maxWidth: .infinity)
            }
        }
        
        .alert("전송 완료", isPresented: $showSentAlert) {
            Button("확인") {
                DispatchQueue.main.async { sent = true }
            }
        }
        message: {
            Text("이메일로 아이디를 전송하였습니다")
        }
        .fullScreenCover(isPresented: $goToLogin) {
            LoginView()
        }
    }
    
    private func sendRequest() {
        guard isValidEmail(email) else { return }
        isSending = true
        
        // TODO : 실제 API 호출로 교체
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) {
            isSending = false
            showSentAlert = true
        }
    }
    
    private func isValidEmail(_ text: String) -> Bool {
        let regex = #"^\S+@\S+\.\S+$"#
        return text.range(of: regex, options: .regularExpression) != nil
    }
    
}

#Preview {
    FindPWView()
}

