//
//  ValidationUtils.swift
//  SodamProject
//
//  Created by 강윤서 on 9/09/25.
//

import Foundation

struct ValidationUtils {
    static func isValidEmail(_ text: String) -> Bool {
        let regex = #"^\S+@\S+\.\S+$"#
        return text.range(of: regex, options: .regularExpression) != nil
    }
    
    static func isValidEmailFormat(_ email: String) -> Bool {
        let emailRegex = "[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"
        let emailPredicate = NSPredicate(format: "SELF MATCHES %@", emailRegex)
        return emailPredicate.evaluate(with: email)
    }
}
