//
//  LoginViewModel.swift
//  SodamProject
//
//  Created by 강윤서 on 8/12/25.
//

import Foundation

@MainActor
class LoginViewModel: ObservableObject {
    @Published var username: String = ""
    @Published var password: String = ""
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?
    @Published var showAlert: Bool = false
    
    private let apiService = APIService.shared
    weak var userManager: UserManager?
    
    func performLogin() async {
        guard !username.isEmpty else {
            errorMessage = "아이디를 입력해주세요."
            showAlert = true
            return
        }
        
        guard !password.isEmpty else {
            errorMessage = "비밀번호를 입력해주세요."
            showAlert = true
            return
        }
        
        isLoading = true
        errorMessage = nil
        
        do {
            let response = try await apiService.login(username: username, password: password)
            print("로그인 응답: \(response)")
            
            if response.success, let user = response.user {
                print("로그인 성공: 사용자 정보 - \(user)")
                userManager?.currentUser = user
                userManager?.isLoggedIn = true
            } else {
                // 더 구체적인 에러 메시지 제공
                let errorMsg = response.error ?? response.message ?? "로그인에 실패했습니다."
                print("로그인 실패: \(errorMsg)")
                errorMessage = errorMsg
                showAlert = true
            }
        } catch {
            print("로그인 오류: \(error)")
            
            // APIError 타입에 따라 구체적인 메시지 표시
            if let apiError = error as? APIError {
                switch apiError {
                case .httpError(let code):
                    if code == 401 {
                        errorMessage = "가입되지 않은 계정이거나 아이디/비밀번호가 올바르지 않습니다."
                    } else if code == 400 {
                        errorMessage = "아이디와 비밀번호를 올바르게 입력해주세요."
                    } else {
                        errorMessage = "서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
                    }
                case .networkError:
                    errorMessage = "네트워크 연결을 확인해주세요."
                case .invalidRequest(let message):
                    errorMessage = message
                case .invalidURL, .invalidResponse, .decodingError:
                    errorMessage = "서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
                }
            } else {
                // 기타 오류 (네트워크 연결 문제 등)
                errorMessage = "네트워크 연결을 확인해주세요."
            }
            
            showAlert = true
        }
        
        isLoading = false
    }
    
    func clearError() {
        errorMessage = nil
        showAlert = false
    }
}
