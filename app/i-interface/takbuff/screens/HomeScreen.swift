//
//  HomeScreen.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 02/12/23.
//

import Combine
import SwiftUI
import SwiftData
import GoogleSignInSwift
import GoogleSignIn

struct HomeScreen: View {
    @Environment(\.modelContext) var modelContext
    @Query() var devices: [AppUserDevice]
    
    let animation: Namespace.ID
    let name: Namespace.ID
    let logo: Namespace.ID
    let dp: Namespace.ID
    
    @Binding public var user: User?
    
    @Binding public var screen: Screen
    
    let layout: LayoutProperties
    
    @State public var subScreen: SubScreen = .Dashboard
    
    @State private var isSearching = false
    @State private var searchText = ""
    @State private var isLoading = false
    @State private var searchResultList: Array<Result> = []
    
    @StateObject private var viewModel = LocationViewModel()
    
    @State private var errorMessage = ""

    let appName = "Takbuff"

    var body: some View {
        ZStack{
            VStack {
                HStack {
                    if(!isSearching || layout.homeDimen.keepBanner){
                        AppLogo()
                            .matchedGeometryEffect(id: logo, in: animation)
                            .frame(width: layout.homeDimen.appLogoSize, height: layout.homeDimen.appLogoSize)
                        
                        VStack(alignment: .leading) {
                            Text(appName)
                                .font(.system(size: layout.homeDimen.appTitleSize))
                                .foregroundColor(.white)
                                .matchedGeometryEffect(id: name, in: animation)
                        }
                        
                        Spacer()
                    }
                    
                    SearchLayout(
                        layout: layout,
                        isSearching: $isSearching,
                        searchText: $searchText
                    )
                    
                    if(!isSearching || layout.homeDimen.keepBanner){
                        Button {
                            if (user == nil){
                               authenticate()
                            }
                            else{
                                navigateUser()
                            }
                        } label: {
                            if (user == nil){
                                Icon(logo: "icGoogle", size: layout.homeDimen.appLogoSize)
                            }
                            else{
                                if(user!.dp == ""){
                                    Icon(logo: "icPerson", size: layout.homeDimen.appLogoSize)
                                        .matchedGeometryEffect(id: dp, in: animation)
                                }
                                else {
                                    ImageView(imageId: user!.dp, size: "80")
                                        .frame(width: layout.homeDimen.appLogoSize, height: layout.homeDimen.appLogoSize)
                                        .cornerRadius(layout.homeDimen.appLogoSize/3)
                                        .matchedGeometryEffect(id: dp, in: animation)
                                }
                            }
                        }
                    }
                }
                .padding(
                    EdgeInsets(
                        top: isSearching ? layout.homeDimen.searchlayoutPaddingTop : layout.homeDimen.searchPaddingTop,
                        leading: isSearching ? layout.homeDimen.searchlayoutPaddingLeading : layout.homeDimen.searchPaddingSide,
                        bottom: isSearching ? layout.homeDimen.searchlayoutPaddingBottom : layout.homeDimen.searchPaddingBottom,
                        trailing: isSearching ? layout.homeDimen.searchlayoutPaddingTrailing : layout.homeDimen.searchPaddingSide
                    )
                )
                .background(
                    Color("banner")
                        .clipShape(
                            .rect(
                                bottomLeadingRadius: layout.homeDimen.layoutCornerRadius,
                                bottomTrailingRadius:layout.homeDimen.layoutCornerRadius
                            )
                        )
                )
                .frame(width: layout.homeDimen.bannerLayoutWidth)
                
                HStack(alignment: .top) {
                    if (layout.homeDimen.keepSideLayouts){
                        ZStack {
                            RoundedRectangle(
                                cornerRadius: layout.homeDimen.layoutCornerRadius,
                                style: .continuous
                            )
                            .foregroundColor(Color("mildBackground"))
                            .frame(width: nil, height: nil)
                        }
                        .frame(width: layout.homeDimen.sideLayoutSize, height: layout.homeDimen.sideLayoutSize)
                        
                    }
                    
                    ZStack {
                        Color("mildBackground")
                            .edgesIgnoringSafeArea(.bottom)
                        
                        if (isSearching) {
                            searchList(
                                ResultList: $searchResultList,
                                dimen: layout.searchDimen
                            )
                        } else {
                            SubScreenLayout(
                                animation: animation,
                                isLoading: $isLoading,
                                screen: $screen,
                                subScreen: $subScreen,
                                layout: layout
                            )
                        }
                    }
                    .frame(width: layout.homeDimen.mainLayoutWidth)
                    
                    if (layout.homeDimen.keepSideLayouts){
                        ZStack {
                            RoundedRectangle(
                                cornerRadius: layout.homeDimen.layoutCornerRadius,
                                style: .continuous
                            )
                            .foregroundColor(Color("mildBackground"))
                            .frame(width: nil, height: nil)
                        }
                        .frame(width: layout.homeDimen.sideLayoutSize, height: layout.homeDimen.sideLayoutSize)
                    }
                }
                .frame(maxWidth: .infinity)
            }
            
            if(isLoading){
                Loader()
            }
        }
    }
    
    private func authenticate() {
        GAuthServices().auth { data, error in
            guard let data = data else {
                errorMessage = "Unexpected Error on Google Login"
                return
            }
            
            var lData: [String: Any] = [
                "deviceId": devices[0].appDeviceId,
                
            ]
            if let location = viewModel.locationCoordinates {
                lData["location"] = [
                    "lat": location.latitude.description,
                    "long": location.longitude.description
                ]
            }
            
            LoginData().auth(uData: data, lData: lData) { userData, error in
                    guard let userData = userData else {
                        errorMessage = "Unable to connect Server"
                        return
                    }
                    
                    let idToken = userData["idToken"]! as! String
                    let accessToken = userData["accessToken"]! as! String
                    devices[0].idToken = idToken
                    devices[0].accessToken = accessToken
                    
                    AuthVar.setAccessToken(idToken: idToken, accessToken: accessToken)
                    
                    let userId: [String : String] = userData["user_id"] as! [String : String]
                    
                    self.user = User(
                        id: userData["id"]! as! String,
                        name: userData["name"]! as! String,
                        dp: userData["dp"]! as! String,
                        email: userId["val"]!
                    )
                    
                    if ((userData["isNew"]! as! Bool)){
                        withAnimation {
                            screen = .NEWUSER
                        }
                    }
                }
        }
    }
    
    func navigateUser() {
        withAnimation{
            screen = .USER
        }
    }
}

struct HomeDimensValues {
    let appLogoSize: CGFloat
    let appTitleSize: CGFloat
    
    let layoutCornerRadius = 20.0
    
    let sideLayoutSize = 200.0
    
    let searchPaddingTop = 5.0
    let searchPaddingSide = 20.0
    let searchPaddingBottom = 10.0
    
    let keepBanner: Bool
    let keepSideLayouts: Bool
    let bannerLayoutWidth: CGFloat?
    
    let mainLayoutWidth: CGFloat?
    
    let searchlayoutPaddingTop: CGFloat
    let searchlayoutPaddingBottom: CGFloat
    let searchlayoutPaddingTrailing: CGFloat
    let searchlayoutPaddingLeading: CGFloat
    
    let searchingBgHeight: CGFloat
    let searchingBgWidth: CGFloat?
    let searchingCornerRadius: CGFloat
    
    init(screenDimenType: ScreenDimenType) {
        switch screenDimenType{
        case .MOBILE:
            appLogoSize = 45.0
            appTitleSize = 18.0
            keepBanner = false
            keepSideLayouts = false
            bannerLayoutWidth = nil
            mainLayoutWidth = nil
            
            searchlayoutPaddingTop = 0.0
            searchlayoutPaddingBottom = 0.0
            searchlayoutPaddingLeading = 0.0
            searchlayoutPaddingTrailing = 0.0
            
            searchingBgHeight = 70.0
            searchingBgWidth = nil
            searchingCornerRadius = 0.0
        case .MIN_TABLET:
            appLogoSize = 60.0
            appTitleSize = 34.0
            
            keepBanner = true
            keepSideLayouts = false
            bannerLayoutWidth = 800.0
            mainLayoutWidth = 700.0
            
            searchlayoutPaddingTop = 0.0
            searchlayoutPaddingBottom = 5.0
            searchlayoutPaddingLeading = 20.0
            searchlayoutPaddingTrailing = 10.0
            
            searchingBgHeight = 45.0
            searchingBgWidth = 350.0
            searchingCornerRadius = 25.0
        case .TABLET:
            appLogoSize = 70.0
            appTitleSize = 40.0
            
            keepBanner = true
            keepSideLayouts = false
            bannerLayoutWidth = 900.0
            mainLayoutWidth =  700.0
            
            searchlayoutPaddingTop = 0.0
            searchlayoutPaddingBottom = 5.0
            searchlayoutPaddingLeading = 20.0
            searchlayoutPaddingTrailing = 10.0
            
            searchingBgHeight = 45.0
            searchingBgWidth = 400.0
            searchingCornerRadius = 25.0
        case .DESKTOP:
            appLogoSize = 60.0
            appTitleSize = 30.0
            
            keepBanner = true
            keepSideLayouts = true
            bannerLayoutWidth = 1100.0
            mainLayoutWidth = 700.0
            
            searchlayoutPaddingTop = 0.0
            searchlayoutPaddingBottom = 5.0
            searchlayoutPaddingLeading = 20.0
            searchlayoutPaddingTrailing = 10.0
            
            searchingBgHeight = 45.0
            searchingBgWidth = 400.0
            searchingCornerRadius = 25.0
        }
    }
}
