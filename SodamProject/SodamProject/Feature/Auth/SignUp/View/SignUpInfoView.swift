//
//  SignUpInfoView.swift
//  SodamProject
//
//  Created by 강윤서 on 8/13/25.
//

import SwiftUI
import Foundation

// TODO : 아이디, 이메일 중복 체크
struct SignUpInfoView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject var userManager: UserManager
    @StateObject private var viewModel = SignUpViewModel()
    @State private var goNext = false
    @FocusState private var isFocused: Bool   // 키보드 포커스 제어

    var body: some View {
        NavigationStack {
            ZStack {
                VStack(spacing: 35) {
                    VStack(spacing: 10) {
                        HStack(spacing: 24) {
                            Button { dismiss() } label: {
                                Image(systemName: "chevron.left")
                                    .font(.title3.weight(.semibold))
                            }
                            .foregroundColor(Color(red: 0.29, green: 0.29, blue: 0.29))
                            Spacer()
                        }
                        .padding(.horizontal, 20)
                        .padding(.top, 12)
                        
                        ProgressBarView(currentStep: 1, totalSteps: 4)
                            .padding(.horizontal, 130)
                    }

                    Text("계정 정보를 입력해주세요")
                        .font(.system(size: 24, weight: .bold))
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .padding(.horizontal, 20)
                        .padding(.top, 8)

                    ScrollView {
                        VStack(alignment: .leading, spacing: 16) {
                            groupField(title: "아이디") {
                                InputField(
                                    placeholder: "아이디를 입력해 주세요",
                                    text: $viewModel.id,
                                    keyboardType: .default
                                )
                                .textInputAutocapitalization(.never)
                                .autocorrectionDisabled()
                                .focused($isFocused)
                                .onChange(of: viewModel.id) { _, newValue in
                                    // 한국어 입력 필터링 (ASCII만 허용)
                                    let filtered = newValue.filter { char in
                                        guard let unicode = char.unicodeScalars.first else { return false }
                                        return (unicode.value >= 0x0020 && unicode.value <= 0x007F)
                                    }
                                    if filtered != newValue {
                                        viewModel.id = filtered
                                    }
                                }
                            }
                            
                            groupField(title: "이메일") {
                                InputField(
                                    placeholder: "이메일을 입력해 주세요",
                                    text: $viewModel.email,
                                    keyboardType: .emailAddress
                                )
                                .textInputAutocapitalization(.never)
                                .autocorrectionDisabled()
                                .focused($isFocused)
                                
                                if !viewModel.email.isEmpty && !viewModel.isValidEmail {
                                    Text("올바른 이메일 형식을 입력해주세요")
                                        .font(.footnote)
                                        .foregroundStyle(.red)
                                        .padding(.top, 1)
                                }
                            }
                            
                            groupField(title: "비밀번호") {
                                InputField(
                                    placeholder: "비밀번호를 입력해 주세요",
                                    text: $viewModel.password,
                                    isSecure: true
                                )
                                .focused($isFocused)
                            }
                            
                            groupField(title: "비밀번호 확인") {
                                InputField(
                                    placeholder: "비밀번호를 다시 입력해 주세요",
                                    text: $viewModel.passwordConfirm,
                                    isSecure: true
                                )
                                .focused($isFocused)
                                
                                if !viewModel.passwordConfirm.isEmpty {
                                    if viewModel.passwordsMatch {
                                        Text("비밀번호가 일치합니다")
                                            .font(.footnote)
                                            .foregroundStyle(.green)
                                            .padding(.top, 1)
                                    } else {
                                        Text("비밀번호가 일치하지 않습니다")
                                            .font(.footnote)
                                            .foregroundStyle(.red)
                                            .padding(.top, 1)
                                    }
                                }
                            }

                            Spacer(minLength: 40)
                        }
                        .padding(.horizontal, 20)
                        .padding(.top, 16)
                        .padding(.bottom, 120)
                    }
                }

                VStack {
                    Spacer()
                    DefaultButton(
                        title: viewModel.isLoading ? "처리 중..." : "다음",
                        action: onTapNext,
                        isEnabled: viewModel.isNextEnabled && !viewModel.isLoading
                    )
                    .padding(.horizontal, 20)
                    .padding(.bottom, 24)
                }
            }
            .contentShape(Rectangle())
            .onTapGesture {            // 빈 곳 탭 시 키보드 내림
                isFocused = false
            }
            .ignoresSafeArea(.keyboard, edges: .bottom)
            .navigationBarHidden(true)   // 이전 버전과 호환
            .navigationDestination(isPresented: $goNext) {
                SignUpUserView()
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

    private func groupField<Content: View>(title: String, @ViewBuilder content: () -> Content) -> some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(title).font(.subheadline.weight(.semibold))
            content()
        }
    }

    private func onTapNext() {
        guard viewModel.isNextEnabled else { return }
        
        // 입력된 정보를 UserManager에 임시 저장 (아직 회원가입은 하지 않음)
        let tempUser = User(
            id: 0,
            username: viewModel.id,
            email: viewModel.email,
            created_at: nil,
            name: nil, // 이름은 SignUpUserView에서 입력받음
            interests: [],
            regions: []
        )
        userManager.currentUser = tempUser
        userManager.tempPassword = viewModel.password
        
        print("User info saved temporarily: \(viewModel.email)")
        
        goNext = true
    }
}

#Preview {
    SignUpInfoView()
}

