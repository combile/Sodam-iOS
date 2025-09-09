//
//  SignUpAgreeView.swift
//  SodamProject
//
//  Created by 강윤서 on 8/15/25.
//

import SwiftUI

struct SignUpAgreeView: View {
    @Environment(\.dismiss) private var dismiss
    @State private var agreeAll = false
    @State private var agreeService = false
    @State private var agreePersonalInfo = false
    @State private var agreeLocationService = false
    @State private var agreeAge = false
    @State private var agreeMarketing = false
    @State private var navigateToHome = false
    
    private var isNextEnabled: Bool {
        agreeService && agreePersonalInfo && agreeLocationService && agreeAge
    }
    
    var body: some View {
        NavigationStack {
            ZStack {
                VStack(spacing: 35) {
                    VStack(spacing: 10) {
                        HStack(spacing: 24) {
                            NavigationLink(destination: SignUpUserView()) {
                                Image(systemName: "chevron.left")
                                    .font(.title3.weight(.semibold))
                                    .foregroundColor(Color(red: 0.29, green: 0.29, blue: 0.29))
                            }
                            Spacer()
                        }
                        .padding(.horizontal, 20)
                        .padding(.top, 12)
                        
                        ProgressBarView(currentStep: 3, totalSteps: 4)
                            .padding(.horizontal, 130)
                    }

                    VStack(alignment: .leading, spacing: 8) {
                        Text("원활한 서비스 이용을 위해")
                            .font(.system(size: 24, weight: .bold))
                        Text("필수 약관 동의가 필요해요")
                            .font(.system(size: 24, weight: .bold))
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding(.horizontal, 20)

                    VStack(spacing: 20) {
                        // 모두 동의
                        HStack(spacing: 12) {
                            Button {
                                agreeAll.toggle()
                                if agreeAll {
                                    agreeService = true
                                    agreePersonalInfo = true
                                    agreeLocationService = true
                                    agreeAge = true
                                    agreeMarketing = true
                                } else {
                                    agreeService = false
                                    agreePersonalInfo = false
                                    agreeLocationService = false
                                    agreeAge = false
                                    agreeMarketing = false
                                }
                            } label: {
                                Circle()
                                    .fill(agreeAll ? Color(hex: "7DDB69") : Color.gray.opacity(0.3))
                                    .frame(width: 24, height: 24)
                                    .overlay(
                                        Image(systemName: "checkmark")
                                            .font(.system(size: 12, weight: .bold))
                                            .foregroundColor(agreeAll ? .white : .gray.opacity(0.6))
                                    )
                            }
                            
                            Text("모두 동의합니다.")
                                .font(.system(size: 16, weight: .medium))
                                .foregroundColor(.black)
                                .frame(maxWidth: .infinity, alignment: .leading)
                        }
                        .contentShape(Rectangle())
                        .onTapGesture {
                            agreeAll.toggle()
                            if agreeAll {
                                agreeService = true
                                agreePersonalInfo = true
                                agreeLocationService = true
                                agreeAge = true
                                agreeMarketing = true
                            } else {
                                agreeService = false
                                agreePersonalInfo = false
                                agreeLocationService = false
                                agreeAge = false
                                agreeMarketing = false
                            }
                        }
                        
                        // 개별 약관들
                        VStack(spacing: 16) {
                            agreementRow(
                                title: "(필수) 서비스 이용약관에 동의합니다.",
                                isSelected: $agreeService,
                                isRequired: true
                            )
                            
                            agreementRow(
                                title: "(필수) 개인정보 처리방침에 동의합니다.",
                                isSelected: $agreePersonalInfo,
                                isRequired: true
                            )
                            
                            agreementRow(
                                title: "(필수) 위치기반 서비스 이용약관에 동의합니다.",
                                isSelected: $agreeLocationService,
                                isRequired: true
                            )
                            
                            agreementRow(
                                title: "(필수) 만 14세 이상입니다.",
                                isSelected: $agreeAge,
                                isRequired: true
                            )
                            
                            agreementRow(
                                title: "(선택) 마케팅 정보 수신에 동의합니다.",
                                isSelected: $agreeMarketing,
                                isRequired: false
                            )
                        }
                    }
                    .padding(.horizontal, 20)
                    
                    Spacer()
                }

                VStack {
                    Spacer()
                    DefaultButton(
                        title: "가입 완료",
                        action: onTapComplete,
                        isEnabled: isNextEnabled
                    )
                    .padding(.horizontal, 20)
                    .padding(.bottom, 24)
                }
            }
            .navigationBarHidden(true)
            .navigationDestination(isPresented: $navigateToHome) {
                SignUpView()
            }
        }
        .onChange(of: agreeService) {
            updateAgreeAll()
        }
        .onChange(of: agreePersonalInfo) {
            updateAgreeAll()
        }
        .onChange(of: agreeLocationService) {
            updateAgreeAll()
        }
        .onChange(of: agreeAge) {
            updateAgreeAll()
        }
        .onChange(of: agreeMarketing) {
            updateAgreeAll()
        }
    }
    
    // MARK: - Agreement Row
    private func agreementRow(
        title: String,
        isSelected: Binding<Bool>,
        isRequired: Bool,
        showArrow: Bool = true
    ) -> some View {
        HStack(spacing: 12) {
            Button {
                isSelected.wrappedValue.toggle()
            } label: {
                Circle()
                    .fill(isSelected.wrappedValue ? Color(hex: "7DDB69") : Color.gray.opacity(0.3))
                    .frame(width: 24, height: 24)
                    .overlay(
                        Image(systemName: "checkmark")
                            .font(.system(size: 12, weight: .bold))
                            .foregroundColor(isSelected.wrappedValue ? .white : .gray.opacity(0.6))
                    )
            }
            
            Text(title)
                .font(.system(size: 16))
                .foregroundColor(.black)
                .frame(maxWidth: .infinity, alignment: .leading)
            
            if showArrow {
                Image(systemName: "chevron.right")
                    .font(.system(size: 14))
                    .foregroundColor(.gray)
            }
        }
        .contentShape(Rectangle())
        .onTapGesture {
            if showArrow {
                // 약관 상세보기 액션
            } else {
                isSelected.wrappedValue.toggle()
            }
        }
    }
    
    // MARK: - Actions
    private func updateAgreeAll() {
        agreeAll = agreeService && agreePersonalInfo && agreeLocationService && agreeAge && agreeMarketing
    }
    
    private func onTapComplete() {
        guard isNextEnabled else { return }
        navigateToHome = true
    }
}

#Preview {
    SignUpAgreeView()
}
