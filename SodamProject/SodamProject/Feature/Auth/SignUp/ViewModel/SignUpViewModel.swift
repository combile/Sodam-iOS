//
//  SignUpViewModel.swift
//  SodamProject
//
//  Created by 강윤서 on 8/12/25.
//

import Foundation

@MainActor
class SignUpViewModel: ObservableObject {
    @Published var id: String = ""
    @Published var email: String = ""
    @Published var password: String = ""
    @Published var passwordConfirm: String = ""
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?
    @Published var showAlert: Bool = false
    
    private let apiService = APIService.shared
    
    var isValidEmail: Bool {
        email.isEmpty || isValidEmailFormat(email)
    }
    
    var isValidPassword: Bool {
        password.count >= 8
    }
    
    var passwordsMatch: Bool {
        passwordConfirm.isEmpty || password == passwordConfirm
    }
    
    var isNextEnabled: Bool {
        !id.isEmpty &&
        !email.isEmpty &&
        !password.isEmpty &&
        !passwordConfirm.isEmpty &&
        isValidEmail &&
        isValidPassword &&
        passwordsMatch
    }
    
    func performSignUp() async -> AuthResponse? {
        guard isNextEnabled else { return nil }
        
        isLoading = true
        errorMessage = nil
        
        do {
            let response = try await apiService.register(username: id, email: email, password: password, name: id)
            isLoading = false
            return response
        } catch {
            errorMessage = error.localizedDescription
            showAlert = true
            isLoading = false
            return nil
        }
    }
    
    func clearError() {
        errorMessage = nil
        showAlert = false
    }
    
    private func isValidEmailFormat(_ email: String) -> Bool {
        let emailRegex = "[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"
        let emailPredicate = NSPredicate(format: "SELF MATCHES %@", emailRegex)
        return emailPredicate.evaluate(with: email)
    }
}
