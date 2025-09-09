//
//  DamsoView.swift
//  SodamProject
//
//  Created by 강윤서 on 8/27/25.
//

import SwiftUI

struct DamsoView: View {
    @State private var searchText: String = ""
    @State private var goToProfile: Bool = false
    
    // 더미 포스트 데이터
    private let posts: [Post] = [
        Post(
            profileImage: "profile1",
            username: "월매출1억꿈나무",
            // isVerified: true,
            message: "초기 비용이 궁금해요!",
            subtitle: "다들 가게 차리실 때 얼마정도 들어가셨어요?",
            timeAgo: "2시간 전",
            location: "덕명동",
            views: 34,
            likeCount: 2,
            commentCount: 9
        ),
        Post(
            profileImage: "profile2",
            username: "3호점가즈아아",
            // isVerified: false,
            message: "손님이 예약하고 안 옴",
            subtitle: "아.. 손님이 예약전화 해놓고 결국 안 옴",
            timeAgo: "8시간 전",
            location: "학하동",
            views: 63,
            likeCount: 8,
            commentCount: 29
        )
    ]
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                headerView
                
                Divider()
                    .background(Color.gray.opacity(0.3))
                
                announcementCard
                
                Divider()
                    .background(Color.gray.opacity(0.3))
                
                postsList
                
                Spacer()
            }
            .background(Color.white)
        }
        .navigationBarHidden(true)
    }
    
    private var headerView: some View {
        HStack {
            Text("유성구")
                .font(.system(size: 20, weight: .semibold))
                .foregroundColor(Color(hex: "#4A4A4A"))
            
            Spacer()
            
            HStack(spacing: 15) {
                NavigationLink(destination: DamsoProfileView(), label: {
                    Image(systemName: "person.circle")
                        .font(.system(size: 24))
                        .foregroundColor(Color(hex: "#4A4A4A"))
                })
                               
                               Button(action: {}) {
                    Image(systemName: "magnifyingglass")
                        .font(.system(size: 20))
                        .foregroundColor(Color(hex: "#4A4A4A"))
                }
            }
        }
        .padding(.horizontal, 20)
        .padding(.top, 10)
        .padding(.bottom, 15)
    }
    
    private var announcementCard: some View {
        VStack(spacing: 0) {
            HStack {
                HStack(spacing: 8) {
                    Image("Chat")
                        .resizable()
                        .scaledToFit()
                        .frame(width: 40, height: 40)
                }
                .padding(.horizontal, 20)
                .padding(.vertical, 8)
                
                Text("사장님에게 무엇이든 물어보세요!")
                    .font(.system(size: 16, weight: .medium))
                    .foregroundColor(Color(hex: "#4A4A4A"))
                
                Spacer()
            }
            .padding(.horizontal, 20)
            .padding(.vertical, 15)
            
            HStack {
                Spacer()
                
                Button(action: {}) {
                    HStack(spacing: 5) {
                        Text("질문하기")
                            .font(.system(size: 14, weight: .medium))
                            .foregroundColor(Color(hex: "#4A4A4A"))
                        
                        Image(systemName: "arrow.right")
                            .font(.system(size: 14))
                            .foregroundColor(Color(hex: "#4A4A4A"))
                    }
                }
                .padding(.trailing, 20)
            }
            .padding(.bottom, 15)
        }
        .background(Color.white)
    }
    
    private var postsList: some View {
        ScrollView {
            LazyVStack(spacing: 0) {
                ForEach(posts, id: \.id) { post in
                    PostView(
                        profileImage: post.profileImage,
                        username: post.username,
                        message: post.message,
                        subtitle: post.subtitle,
                        timeAgo: post.timeAgo,
                        location: post.location,
                        views: post.views,
                        likeCount: post.likeCount,
                        commentCount: post.commentCount
                    )
                    
                    if post.id != posts.last?.id {
                        Divider()
                            .background(Color.gray.opacity(0.1))
                            .padding(.horizontal, 20)
                    }
                }
            }
            .padding(.top, 10)
        }
    }
}

#Preview {
    DamsoView()
}
