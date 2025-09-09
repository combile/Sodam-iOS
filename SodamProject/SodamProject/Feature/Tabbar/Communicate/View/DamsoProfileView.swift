//
//  DamsoProfileView.swift
//  SodamProject
//
//  Created by 강윤서 on 8/27/25.
//

import SwiftUI

struct DamsoProfileView: View {
    @State private var selectedTab = 0
    @Environment(\.dismiss) private var dismiss
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                HStack {
                    Button(action: {
                        dismiss()
                    }) {
                        Image(systemName: "chevron.left")
                            .font(.title2)
                            .foregroundColor(Color(hex: "#4A4A4A"))
                    }
                    
                    Spacer()
                    
                    Text("담소 프로필")
                        .font(.title2)
                        .fontWeight(.bold)
                    
                    Spacer()
                }
                .padding(.horizontal, 20)
                .padding(.top, 10)
                
                VStack(spacing: 16) {
                    HStack(spacing: 16) {
                        AsyncImage(url: URL(string: "https://i.pinimg.com/originals/ac/7e/b0/ac7eb0bb4515a5fb6aca6e6993b47676.jpg")) { image in
                            image
                                .resizable()
                                .aspectRatio(contentMode: .fill)
                        } placeholder: {
                            Circle()
                                .fill(Color.gray.opacity(0.3))
                                .overlay(
                                    Image(systemName: "pawprint.fill")
                                        .foregroundColor(.gray)
                                        .font(.title2)
                                )
                        }
                        .frame(width: 80, height: 80)
                        .clipShape(Circle())
                        
                        VStack(alignment: .leading, spacing: 8) {
                            HStack {
                                Text("월매출1억꿈나무")
                                    .font(.title2)
                                    .fontWeight(.bold)
                            }
                            
                            HStack {
                                Text("덕명동")
                                    .font(.caption)
                                    .foregroundColor(.gray)
                                Text("·")
                                    .font(.caption)
                                    .foregroundColor(.gray)
                                Text("예비 창업자")
                                    .font(.caption)
                                    .foregroundColor(.gray)
                            }
                        }
                        
                        Spacer()
                        
                        Text("Lv.8")
                            .font(.caption)
                            .fontWeight(.medium)
                            .padding(.horizontal, 12)
                            .padding(.vertical, 4)
                            .background(Color.cyan.opacity(0.2))
                            .foregroundColor(.cyan)
                            .cornerRadius(12)
                    }
                    .padding(.horizontal, 20)
                    
                    HStack {
                        Text("Lv.8")
                            .font(.caption)
                            .foregroundColor(.gray)
                        
                        GeometryReader { geometry in
                            ZStack(alignment: .leading) {
                                Rectangle()
                                    .fill(Color.gray.opacity(0.2))
                                    .frame(height: 6)
                                
                                Rectangle()
                                    .fill(LinearGradient(
                                        gradient: Gradient(colors: [.cyan, .green]),
                                        startPoint: .leading,
                                        endPoint: .trailing
                                    ))
                                    .frame(width: geometry.size.width * 0.7, height: 6)
                            }
                            .cornerRadius(3)
                        }
                        .frame(height: 6)
                        
                        Text("Lv.9")
                            .font(.caption)
                            .foregroundColor(.gray)
                    }
                    .padding(.horizontal, 20)
                    
                    Button(action: {
                    }) {
                        Text("프로필 편집")
                            .font(.system(size: 16, weight: .medium))
                            .foregroundColor(.black)
                            .frame(maxWidth: .infinity)
                            .frame(height: 44)
                            .background(Color.gray.opacity(0.1))
                            .cornerRadius(8)
                    }
                    .padding(.horizontal, 20)
                }
                .padding(.top, 20)
                
                Divider()
                    .padding(.top, 20)
                
                HStack {
                    Button(action: { selectedTab = 0 }) {
                        VStack(spacing: 8) {
                            Text("작성한 글")
                                .font(.system(size: 16, weight: selectedTab == 0 ? .semibold : .regular))
                                .foregroundColor(selectedTab == 0 ? .black : .gray)
                            
                            Rectangle()
                                .fill(selectedTab == 0 ? Color.black : Color.clear)
                                .frame(height: 2)
                        }
                    }
                    
                    Button(action: { selectedTab = 1 }) {
                        VStack(spacing: 8) {
                            Text("질문한 글")
                                .font(.system(size: 16, weight: selectedTab == 1 ? .semibold : .regular))
                                .foregroundColor(selectedTab == 1 ? .black : .gray)
                            
                            Rectangle()
                                .fill(selectedTab == 1 ? Color.black : Color.clear)
                                .frame(height: 2)
                        }
                    }
                }
                .padding(.horizontal, 20)
                .padding(.top, 16)
                
                if selectedTab == 0 {
                    ScrollView {
                        VStack(spacing: 16) {
                            PostItemView()
                        }
                        .padding(.top, 20)
                    }
                } else {

                    VStack {
                        Spacer()
                        
                        Text("동네 사장님들에게 질문해보세요.")
                            .font(.system(size: 16))
                            .foregroundColor(.gray)
                            .padding(.bottom, 20)
                        
                        NavigationLink(destination: DamsoView()) {
                            Text("질문하러 가기")
                                .font(.system(size: 16, weight: .medium))
                                .foregroundColor(.black)
                                .padding(.horizontal, 24)
                                .padding(.vertical, 12)
                                .background(Color.gray.opacity(0.1))
                                .cornerRadius(20)
                        }
                        
                        Spacer()
                    }
                }
                
                Spacer()
            }
        }
        .navigationBarHidden(true)
        .gesture(
            DragGesture()
                .onEnded { value in
                    if value.translation.width > 100 {
                        dismiss()
                    }
                }
        )
    }
}

struct PostItemView: View {
    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            AsyncImage(url: URL(string: "https://i.pinimg.com/originals/ac/7e/b0/ac7eb0bb4515a5fb6aca6e6993b47676.jpg")) { image in
                image
                    .resizable()
                    .aspectRatio(contentMode: .fill)
            } placeholder: {
                Circle()
                    .fill(Color.gray.opacity(0.3))
                    .overlay(
                        Image(systemName: "pawprint.fill")
                            .foregroundColor(.gray)
                            .font(.caption)
                    )
            }
            .frame(width: 40, height: 40)
            .clipShape(Circle())
            
            VStack(alignment: .leading, spacing: 8) {
                HStack {
                    Text("월매출1억꿈나무")
                        .font(.system(size: 14, weight: .semibold))
                    
                    Image(systemName: "leaf.fill")
                        .foregroundColor(.green)
                        .font(.caption2)
                    
                    Spacer()
                    
                    Text("덕명동")
                        .font(.caption2)
                        .foregroundColor(.gray)
                    
                    Text("·")
                        .font(.caption2)
                        .foregroundColor(.gray)
                    
                    Text("2시간 전")
                        .font(.caption2)
                        .foregroundColor(.gray)
                    
                    Text("조회 34")
                        .font(.caption2)
                        .foregroundColor(.gray)
                }
                
                Text("초기 비용이 궁금해요")
                    .font(.system(size: 16, weight: .medium))
                    .foregroundColor(.black)
                    .multilineTextAlignment(.leading)
                
                Text("다들 가게 차리실 때 얼마정도 들어가셨어요?")
                    .font(.system(size: 14))
                    .foregroundColor(.gray)
                    .multilineTextAlignment(.leading)
                
                HStack {
                    HStack(spacing: 4) {
                        Image(systemName: "hand.thumbsup")
                            .font(.caption)
                            .foregroundColor(.gray)
                        Text("2")
                            .font(.caption)
                            .foregroundColor(.gray)
                    }
                    
                    HStack(spacing: 4) {
                        Image(systemName: "message")
                            .font(.caption)
                            .foregroundColor(.gray)
                        Text("9")
                            .font(.caption)
                            .foregroundColor(.gray)
                    }
                    
                    Spacer()
                }
                .padding(.top, 4)
            }
        }
        .padding(.horizontal, 20)
    }
}

#Preview {
    DamsoProfileView()
}
