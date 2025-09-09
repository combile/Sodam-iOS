//
//  RoleSelectionModal.swift
//  SodamProject
//
//  Created by 강윤서 on 9/3/25.
//

import SwiftUI

struct RoleSelectionModal: View {
    @Binding var isPresented: Bool
    let name: String
    //let onRoleSelected: (UserRole) -> Void
    
    var body: some View {
        ZStack {
            Color.black.opacity(0.4)
                .ignoresSafeArea()
            
            VStack(spacing: 20) {
                VStack(spacing: 8) {
                    Text("\(name)님 반가워요!")
                        .font(.title2)
                        .fontWeight(.bold)
                        .foregroundColor(Color(hex: "#4A4A4A"))
                    
                    Text("당신은 어떤 분인가요?")
                        .font(.body)
                        .foregroundColor(.secondary)
                }
                .padding(.top, 10)
                
                HStack {
                    RoleButton(
                        title: "오늘도 사장",
                        subtitle: "매장을 운영 중이에요",
                        icon: "person.crop.circle.fill.badge.checkmark",
                        action: {
                          //  onRoleSelected(.existing)
                        }
                    )
                    
                    RoleButton(
                        title: "내일은 사장",
                        subtitle: "창업을 준비하고 있어요",
                        icon: "person.circle",
                        action: {
                       //     onRoleSelected(.prospective)
                        }
                    )
                }
                .padding(.bottom, 20)
            }
            .padding(30)
            .background(Color.white)
            .cornerRadius(20)
            .shadow(radius: 10)
            .padding(.horizontal, 40)
        }
    }
}

struct RoleButton: View {
    let title: String
    let subtitle: String
    let icon: String
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            VStack(spacing: 8) {
                Image(systemName: icon)
                    .font(.system(size: 30))
                    .foregroundColor(.primary)
                    .frame(width: 50, height: 50)
                    .background(Color.white)
                    .clipShape(Circle())
                    .shadow(color: .gray.opacity(0.3), radius: 3, x: 0, y: 2)
                
                VStack(spacing: 4) {
                    Text(title)
                        .font(.system(size: 16, weight: .semibold))
                        .foregroundColor(.primary)
                    
                    Text(subtitle)
                        .font(.system(size: 12))
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.center)
                }
            }
            .frame(maxWidth: .infinity)
            .padding(.vertical, 20)
            .background(Color.gray.opacity(0.05))
            .cornerRadius(15)
            .overlay(
                RoundedRectangle(cornerRadius: 15)
                    .stroke(Color.gray.opacity(0.2), lineWidth: 1)
            )
        }
        .buttonStyle(PlainButtonStyle())
    }
}


//#Preview {
//    RoleSelectionModal()
// }
