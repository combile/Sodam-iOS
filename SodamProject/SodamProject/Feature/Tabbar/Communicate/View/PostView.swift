//
//  PostView.swift
//  SodamProject
//
//  Created by 강윤서 on 8/27/25.
//

import SwiftUI

struct PostView: View {
    let profileImage: String
    let username: String
    let message: String
    let subtitle: String
    let timeAgo: String
    let location: String
    let views: Int
    let likeCount: Int
    let commentCount: Int
    
    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Circle()
                .fill(Color.gray.opacity(0.3))
                .frame(width: 50, height: 50)
                .overlay(
                    Image(systemName: "person.fill")
                        .foregroundColor(.gray)
                        .font(.system(size: 20))
                )
            VStack(alignment: .leading, spacing: 4) {
                HStack(spacing: 4) {
                    Text(username)
                        .font(.system(size: 12, weight: .medium))
                        .foregroundColor(Color(hex: "#4A4A4A"))
                    
                    Spacer()
                    
                    HStack(spacing: 4) {
                        Text(timeAgo)
                            .font(.system(size: 12))
                            .foregroundStyle(Color(hex: "#A0A0A0"))
                        
                        Text("·")
                            .font(.system(size: 12))
                            .foregroundColor(Color(hex: "#A0A0A0"))
                        
                        Text(location)
                            .font(.system(size: 12))
                            .foregroundColor(Color(hex: "#A0A0A0"))
                        
                        Text("·")
                            .font(.system(size: 12))
                            .foregroundColor(Color(hex: "#A0A0A0"))
                        
                        Text("\(views)")
                            .font(.system(size: 12))
                            .foregroundColor(Color(hex: "#A0A0A0"))
                    }
                }
                
                Text(message)
                    .font(.system(size: 15, weight: .medium))
                    .foregroundColor(Color(hex: "#4A4A4A"))
                    .lineLimit(1)
                
                Text(subtitle)
                    .font(.system(size: 12, weight: .medium))
                    .foregroundColor(Color(hex: "#A0A0A0"))
                    .lineLimit(2)
                    .padding(.bottom, 8)
                
                HStack(spacing: 8) {
                    HStack(spacing: 4) {
                        Image(systemName: "hand.thumbsup.fill")
                            .font(.system(size: 14))
                            .foregroundColor(Color(hex: "#A0A0A0"))
                        
                        Text("\(likeCount)")
                            .font(.system(size: 14))
                            .foregroundColor(Color(hex: "#A0A0A0"))
                    }
                    
                    HStack(spacing: 4) {
                        Image(systemName: "message.fill")
                            .font(.system(size: 14))
                            .foregroundColor(Color(hex: "#A0A0A0"))
                        
                        Text("\(commentCount)")
                            .font(.system(size: 14))
                            .foregroundColor(Color(hex: "#A0A0A0"))
                    }
                    Spacer()
                }
            }
            Spacer()
        }
        .padding(.horizontal, 20)
        .padding(.vertical, 12)
    }
}

struct Post {
    let id = UUID()
    let profileImage: String
    let username: String
    let message: String
    let subtitle: String
    let timeAgo: String
    let location: String
    let views: Int
    let likeCount: Int
    let commentCount: Int
}

#Preview {
    VStack {
        PostView(
            profileImage: "profile1",
            username: "월매출1억꿈나무",
            message: "초기 비용이 궁금해요!",
            subtitle: "다들 가게 차리실 때 얼마정도 들어가셨어요?",
            timeAgo: "2시간 전",
            location: "덕명동",
            views: 34,
            likeCount: 2,
            commentCount: 9
        )
        
        Divider()
        
        PostView(
            profileImage: "profile2",
            username: "3호점가즈아아",
            message: "손님이 예약하고 안 옴",
            subtitle: "아.. 손님이 예약전화 해놓고 결국 안 옴",
            timeAgo: "8시간 전",
            location: "학하동",
            views: 63,
            likeCount: 8,
            commentCount: 29
        )
    }
}
