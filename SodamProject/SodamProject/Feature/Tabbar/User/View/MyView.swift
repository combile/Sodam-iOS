//
//  MyPageView.swift
//  SodamProject
//
//  Created by 강윤서 on 9/3/25.
//

import SwiftUI

struct MyView: View {
    @EnvironmentObject var userManager: UserManager
    @State private var email: String = ""
    @State private var name: String = ""
    @State private var username: String = ""
    
    @State private var showSaveAlert = false
    @State private var showLogoutAlert = false
    @State private var showWidthdrawConfirm = false
    
    var body: some View {
        VStack(spacing: 0) {
            // Navigation Bar
            HStack {
                Spacer()
                Text("마이페이지")
                    .font(.system(size: 20, weight: .semibold))
                    .foregroundColor(.primary)
                Spacer()
            }
            .padding(.vertical, 20)
            .background(Color(.systemBackground))
            .shadow(color: .black.opacity(0.05), radius: 1, x: 0, y: 1)
            
            ScrollView {
                VStack(spacing: 0) {
                    // Profile Section
                    VStack(spacing: 16) {
                        ZStack {
                            Circle()
                                .fill(
                                    LinearGradient(
                                        gradient: Gradient(colors: [Color.blue.opacity(0.1), Color.purple.opacity(0.1)]),
                                        startPoint: .topLeading,
                                        endPoint: .bottomTrailing
                                    )
                                )
                                .frame(width: 80, height: 80)
                            
                            Image(systemName: "person.circle.fill")
                                .font(.system(size: 50))
                                .foregroundColor(.blue)
                        }
                        .shadow(color: .black.opacity(0.1), radius: 8, x: 0, y: 4)
                        
                        Text(userManager.currentUser?.name ?? "사용자")
                            .font(.system(size: 24, weight: .bold))
                            .foregroundColor(.primary)
                    }
                    .padding(.top, 16)
                    .padding(.bottom, 16)
                    
                    // Information Card
                    VStack(spacing: 0) {
                        VStack(spacing: 20) {
                            VStack(alignment: .leading, spacing: 10) {
                                Text("이메일")
                                    .font(.system(size: 15, weight: .semibold))
                                    .foregroundColor(.primary)
                                
                                InputField(
                                    placeholder: "이메일을 입력하세요",
                                    text: $email,
                                    keyboardType: .emailAddress
                                )
                            }
                            
                            VStack(alignment: .leading, spacing: 10) {
                                Text("이름")
                                    .font(.system(size: 15, weight: .semibold))
                                    .foregroundColor(.primary)
                                
                                InputField(
                                    placeholder: "이름을 입력하세요",
                                    text: $name
                                )
                            }
                            
                            VStack(alignment: .leading, spacing: 10) {
                                Text("아이디")
                                    .font(.system(size: 15, weight: .semibold))
                                    .foregroundColor(.primary)
                                
                                InputField(
                                    placeholder: "아이디를 입력하세요",
                                    text: $username
                                )
                            }
                        }
                        .padding(20)
                    }
                    .background(Color(.systemBackground))
                    .cornerRadius(16)
                    .shadow(color: .black.opacity(0.08), radius: 12, x: 0, y: 4)
                    .padding(.horizontal, 20)
                    
                    Spacer(minLength: 10)
                    
                    // Action Buttons
                    VStack(spacing: 16) {
                        DefaultButton(
                            title: "저장하기",
                            action: {
                                showSaveAlert = true
                            }
                        )
                        .padding(.horizontal, 20)
                        
                        HStack(spacing: 12) {
                            Button(action: {
                                showLogoutAlert = true
                            }) {
                                VStack(spacing: 3) {
                                    Image(systemName: "rectangle.portrait.and.arrow.right")
                                        .font(.system(size: 16, weight: .medium))
                                    Text("로그아웃")
                                        .font(.system(size: 12, weight: .medium))
                                }
                                .foregroundColor(.blue)
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 8)
                                .background(Color.blue.opacity(0.1))
                                .cornerRadius(8)
                            }
                            
                            Button(action: {
                                showWidthdrawConfirm = true
                            }) {
                                VStack(spacing: 3) {
                                    Image(systemName: "person.fill.xmark")
                                        .font(.system(size: 16, weight: .medium))
                                    Text("탈퇴하기")
                                        .font(.system(size: 12, weight: .medium))
                                }
                                .foregroundColor(.red)
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 8)
                                .background(Color.red.opacity(0.1))
                                .cornerRadius(8)
                            }
                        }
                        .padding(.horizontal, 20)
                        .padding(.bottom, 30)
                    }
                }
            }
            .background(Color(.systemGroupedBackground))
        }
        
        .alert("저장되었습니다", isPresented: $showSaveAlert) {
            Button("확인", role: .cancel) { }
        }
        
        .alert("로그아웃", isPresented: $showLogoutAlert) {
            Button("취소", role: .cancel) { }
            Button("로그아웃", role: .destructive) {
                userManager.logout()
            }
        } message: {
            Text("정말 로그아웃하시겠습니까?")
        }
        
        .alert("탈퇴하시겠습니다?", isPresented: $showWidthdrawConfirm) {
            Button("취소", role: .cancel) { }
            Button("탈퇴하기", role: .destructive) {
                userManager.logout()
            }
        }
        .onAppear {
            loadUserData()
        }
        .onChange(of: userManager.currentUser) { _, _ in
            loadUserData()
        }
    }
    
    private func loadUserData() {
        email = userManager.currentUser?.email ?? ""
        name = userManager.currentUser?.name ?? ""
        username = userManager.currentUser?.username ?? ""
    }
}

#Preview {
    MyView()
        .environmentObject(UserManager())
}

