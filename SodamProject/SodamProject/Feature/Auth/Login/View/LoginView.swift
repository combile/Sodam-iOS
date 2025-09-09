//
//  LoginView.swift
//  SodamProject
//
//  Created by 강윤서 on 8/12/25.
//

import SwiftUI

struct LoginView: View {
    @EnvironmentObject var userManager: UserManager
    @StateObject private var viewModel = LoginViewModel()
    @State private var navigateToSignUp = false
    
    init() {
        // UserManager를 ViewModel에 전달하기 위해 init에서 설정
    }
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                Spacer()
                AppName()
                    .padding(.bottom, 20)
                VStack(spacing: 24) {
                    InputField(placeholder: "아이디를 입력해주세요", text: $viewModel.username)
                    InputField(placeholder: "비밀번호를 입력해주세요", text: $viewModel.password, isSecure: true)
                }
                .padding(.horizontal, 20)
                .padding(.top, 20)
                
                DefaultButton(title: viewModel.isLoading ? "로그인 중..." : "로그인") {
                    Task {
                        await viewModel.performLogin()
                    }
                }
                .disabled(viewModel.isLoading)
                .padding(.horizontal, 20)
                .padding(.top, 32)
                
            
                HStack(spacing: 10) {
                    Button("회원가입") {
                        navigateToSignUp = true
                    }
                    .foregroundColor(Color(hex: "7DDB69"))
                    
                    Text("|")
                        .foregroundColor(Color(hex: "999999"))
                    
                    Button("아이디 찾기") {
                        // 아이디 찾기 페이지로 이동
                    }
                    .foregroundColor(Color(hex: "999999"))
                    
                    Text("|")
                        .foregroundColor(Color(hex: "999999"))
                    
                    Button("비밀번호 찾기") {
                        // 비밀번호 찾기 페이지로 이동
                    }
                    .foregroundColor(Color(hex: "999999"))
                }
                .font(.system(size: 15))
                .padding(.top, 32)
                
                Spacer()
                    }
        .onAppear {
            viewModel.userManager = userManager
        }
        .navigationDestination(isPresented: $navigateToSignUp) {
            SignUpInfoView()
        }
        .alert("오류", isPresented: $viewModel.showAlert) {
            Button("확인") {
                viewModel.clearError()
            }
        } message: {
            Text(viewModel.errorMessage ?? "")
        }
        }
    }
    
}

#Preview {
    LoginView()
        .environmentObject(UserManager())
}

