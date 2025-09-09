//
//  MyAreaDiagnosisView.swift
//  SodamProject
//
//  Created by 강윤서 on 9/1/25.
//

import SwiftUI
import MapKit
import CoreLocation
import Foundation

struct MyAreaDiagnosisView: View {
    @EnvironmentObject var userManager: UserManager
    @StateObject private var locationManager = LocationManager()
    @State private var searchText = ""
    @State private var searchResults: [MKMapItem] = []
    @State private var selectedLocation: CLLocationCoordinate2D?
    @State private var showBottomSheet = false
    @State private var selectedCategory = ""
    @State private var navigateToAnalyze = false
    @State private var isSubmitting = false
    @State private var showAlert = false
    @State private var alertMessage = ""
    
    var body: some View {
        NavigationStack {
            ZStack {
            // 지도
            Map(position: $locationManager.cameraPosition) {
                // 사용자 위치 마커
                if let userLocation = locationManager.userLocation {
                    Marker("내 위치", coordinate: userLocation.coordinate)
                        .tint(.blue)
                }
                
                // 검색된 위치 마커와 반경 원
                if let selectedLocation = selectedLocation {
                    Marker("진단 위치", coordinate: selectedLocation)
                        .tint(.red)
                    
                    // 500m 반경 원
                    MapCircle(center: selectedLocation, radius: 500)
                        .foregroundStyle(.red.opacity(0.3))
                        .stroke(.red, lineWidth: 2)
                }
            }
            .mapStyle(.standard)
            .ignoresSafeArea(.all)
            .onAppear {
                locationManager.requestLocation()
            }
            
            // 검색바
            VStack {
                HStack {
                    Image(systemName: "magnifyingglass")
                        .foregroundColor(.gray)
                        .padding(.leading, 16)
                    
                    TextField("검색하거나 지도에서 위치를 선택해주세요", text: $searchText)
                        .padding(.vertical, 12)
                        .padding(.trailing, 16)
                        .onSubmit {
                            searchLocation()
                        }
                        .onTapGesture {
                            if !showBottomSheet && selectedLocation != nil {
                                withAnimation(.spring(response: 0.5, dampingFraction: 0.8)) {
                                    showBottomSheet = true
                                }
                            }
                        }
                        .textInputAutocapitalization(.never)
                        .autocorrectionDisabled()
                }
                .background(Color.white)
                .cornerRadius(25)
                .shadow(color: .black.opacity(0.1), radius: 4, x: 0, y: 2)
                .padding(.horizontal, 20)
                .padding(.top, 50)
                
                Spacer()
            }
            
            // Bottom Sheet
            if showBottomSheet {
                VStack {
                    Spacer()
                    
                    BottomSheetView(
                        selectedLocation: selectedLocation,
                        selectedCategory: $selectedCategory,
                        selectedSubCategory: .constant(""),
                        showSubCategories: .constant(false),
                        navigateToAnalyze: $navigateToAnalyze,
                        showBottomSheet: $showBottomSheet,
                        isSubmitting: $isSubmitting,
                        onAnalyze: { submitPreferencesAndNavigate() }
                    )
                    .transition(.move(edge: .bottom))
                    .animation(.spring(response: 0.5, dampingFraction: 0.8), value: showBottomSheet)
                }
            }
        }
        .navigationDestination(isPresented: $navigateToAnalyze) {
            AnalyzeView(
                region: searchText,
                category: selectedCategory
            )
            .environmentObject(userManager)
        }
        .alert("알림", isPresented: $showAlert) {
            Button("확인") { }
        } message: {
            Text(alertMessage)
        }
        }
    }
    
    private func searchLocation() {
        guard !searchText.isEmpty else { return }
        
        // 키보드 숨기기
        hideKeyboard()
        
        let request = MKLocalSearch.Request()
        request.naturalLanguageQuery = searchText
        request.region = MKCoordinateRegion(
            center: locationManager.userLocation?.coordinate ?? CLLocationCoordinate2D(latitude: 36.3504, longitude: 127.3845),
            span: MKCoordinateSpan(latitudeDelta: 0.1, longitudeDelta: 0.1)
        )

        let search = MKLocalSearch(request: request)
        search.start { response, error in
            if let error = error {
                DispatchQueue.main.async {
                    self.alertMessage = "검색 중 오류가 발생했습니다: \(error.localizedDescription)"
                    self.showAlert = true
                }
                return
            }

            guard let response = response, let firstResult = response.mapItems.first else {
                DispatchQueue.main.async {
                    self.alertMessage = "검색 결과를 찾을 수 없습니다."
                    self.showAlert = true
                }
                return
            }
            
            DispatchQueue.main.async {
                self.selectedLocation = firstResult.placemark.coordinate
                self.locationManager.cameraPosition = MapCameraPosition.region(
                    MKCoordinateRegion(
                        center: firstResult.placemark.coordinate,
                        span: MKCoordinateSpan(latitudeDelta: 0.01, longitudeDelta: 0.01)
                    )
                )
                withAnimation(.spring(response: 0.5, dampingFraction: 0.8)) {
                    self.showBottomSheet = true
                }
            }
        }
    }
    
    private func hideKeyboard() {
        UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)
    }
    
    private func submitPreferencesAndNavigate() {
        guard !isSubmitting else { return }
        
        guard let userId = userManager.currentUser?.id else {
            alertMessage = "로그인 사용자 정보를 찾을 수 없어요."
            showAlert = true
            return
        }
        
        guard selectedLocation != nil || !searchText.isEmpty else {
            alertMessage = "분석할 위치를 먼저 선택해주세요."
            showAlert = true
            return
        }
        
        isSubmitting = true
        let interests: [String] = selectedCategory.isEmpty ? [] : [selectedCategory]
        
        if !searchText.isEmpty {
            Task {
                do {
                    // 업종과 위치를 기반으로 고유한 marketCode 생성
                    let marketCode = generateMarketCode(
                        location: searchText,
                        category: selectedCategory
                    )
                    print("🔍 Generated marketCode: \(marketCode)")
                    print("🔍 Category: \(selectedCategory)")
                    
                    _ = try await APIService.shared.getComprehensiveDiagnosis(
                        marketCode: marketCode,
                        category: selectedCategory
                    )
                    
                    await MainActor.run {
                        self.isSubmitting = false
                        self.navigateToAnalyze = true
                    }
                } catch {
                    await MainActor.run {
                        self.isSubmitting = false
                        self.alertMessage = "상권 진단 중 오류가 발생했습니다: \(error.localizedDescription)"
                        self.showAlert = true
                    }
                }
            }
        } else if let coord = selectedLocation {
            reverseGeocodeAndSubmit(coord: coord, userId: userId, interests: interests)
        }
    }
    
    private func generateMarketCode(location: String, category: String) -> String {
        // 먼저 상권명을 숫자 코드로 변환 시도
        if let marketCode = convertLocationToMarketCode(location) {
            print("🔍 Using market code: \(marketCode) for location: \(location)")
            return marketCode
        }
        
        // 숫자 코드가 없으면 기존 방식 사용 (fallback)
        let locationCode = convertKoreanToEnglish(location)
        let categoryCode = convertCategoryToCode(category)
        
        let timestamp = Int(Date().timeIntervalSince1970)
        let marketCode = "\(locationCode)_\(categoryCode)_\(timestamp)"
        
        print("🔍 Using generated market code: \(marketCode) for location: \(location)")
        return marketCode
    }
    
    private func convertCategoryToCode(_ category: String) -> String {
        let conversions: [String: String] = [
            "전체": "all",
            "쇼핑업": "shopping",
            "숙박업": "accommodation",
            "식음료업": "food",
            "여가서비스업": "leisure",
            "여행업": "travel",
            "운송업": "transport"
        ]
        return conversions[category] ?? category.lowercased()
    }
    
    
    private func convertKoreanToEnglish(_ korean: String) -> String {
        let conversions: [String: String] = [
            "대전시청": "daejeon_city_hall",
            "대전 시청": "daejeon_city_hall",
            "강남구": "gangnam_gu",
            "서울시청": "seoul_city_hall",
            "부산시청": "busan_city_hall",
            "인천시청": "incheon_city_hall",
            "광주시청": "gwangju_city_hall",
            "대구시청": "daegu_city_hall",
            "울산시청": "ulsan_city_hall"
        ]
        
        return conversions[korean] ?? korean.lowercased().replacingOccurrences(of: " ", with: "_")
    }
    
    // 상권명을 숫자 코드로 변환하는 함수
    private func convertLocationToMarketCode(_ location: String) -> String? {
        let marketCodeMapping: [String: String] = [
            "대전느리울중학교": "10435",
            "유성고속터미널": "10436",
            "시청역6번 출구": "10437",
            "대전역1번 출구": "10438",
            "중앙로역7번 출구": "10439",
            "대전 중리전통시장": "10440",
            "대전시청": "10441",
            "대전 시청": "10441",
            "대전역": "10438",
            "시청역": "10437",
            "중앙로역": "10439",
            "유성고속": "10436",
            "느리울중학교": "10435",
            "중리전통시장": "10440"
        ]
        
        // 정확한 매칭 시도
        if let code = marketCodeMapping[location] {
            return code
        }
        
        // 부분 매칭 시도 (포함된 키워드로 검색)
        for (key, code) in marketCodeMapping {
            if location.contains(key) || key.contains(location) {
                return code
            }
        }
        
        return nil
    }
    
    private func reverseGeocodeAndSubmit(coord: CLLocationCoordinate2D, userId: Int, interests: [String]) {
        let geocoder = CLGeocoder()
        geocoder.reverseGeocodeLocation(CLLocation(latitude: coord.latitude, longitude: coord.longitude)) { placemarks, error in
            
            if let error = error {
                DispatchQueue.main.async {
                    self.isSubmitting = false
                    self.alertMessage = "위치 정보를 가져올 수 없습니다: \(error.localizedDescription)"
                    self.showAlert = true
                }
                return
            }
            
            // 실제 위치 정보 추출
            let locationName = placemarks?.first?.administrativeArea ??
                              placemarks?.first?.locality ??
                              placemarks?.first?.subLocality ?? "선택지역"
            
            print("🔍 Reverse geocoded location: \(locationName)")
            
            Task {
                do {
                    // 업종과 실제 위치를 기반으로 고유한 marketCode 생성
                    let marketCode = generateMarketCode(
                        location: locationName,
                        category: selectedCategory
                    )
                    print("🔍 Generated marketCode (map): \(marketCode)")
                    print("🔍 Location: \(locationName)")
                    print("🔍 Category: \(selectedCategory)")
                    
                    _ = try await APIService.shared.getComprehensiveDiagnosis(
                        marketCode: marketCode,
                        category: selectedCategory
                    )
                    
                    await MainActor.run {
                        self.isSubmitting = false
                        self.navigateToAnalyze = true
                    }
                } catch {
                    await MainActor.run {
                        self.isSubmitting = false
                        self.alertMessage = "상권 진단 중 오류가 발생했습니다: \(error.localizedDescription)"
                        self.showAlert = true
                    }
                }
            }
        }
    }
}

#Preview {
    MyAreaDiagnosisView()
        .environmentObject(UserManager())
}
