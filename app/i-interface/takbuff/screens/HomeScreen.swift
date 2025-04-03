//
//  HomeScreen.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 02/12/23.
//

import SwiftUI

struct HomeScreen: View {
    let animation: Namespace.ID
    let name: Namespace.ID
    let logo: Namespace.ID
    
    @Binding var screen: Screen
    
    let layout: LayoutProperties
    
    @State private var subScreen: SubScreen = .Dashboard
    
    @State private var isSearching = false
    @State private var searchText = ""
    @State private var isLoading = false
    @State private var searchResultList: Array<Result> = []
    
    let appName = "Takbuff"
    
    let appLogoSize = 50.0
    let appTitleSize = 25.0
    
    let layoutCornerRadius = 20.0
    
    let sideLayoutSize = 200.0
    
    let searchPaddingTop = 5.0
    let searchPaddingSide = 20.0
    let searchPaddingBottom = 10.0
    
    var body: some View {
        ZStack{
            VStack {
                HStack {
                    if(!isSearching || layout.homeDimen.keepBanner){
                        AppLogo()
                            .matchedGeometryEffect(id: logo, in: animation)
                            .frame(width: appLogoSize, height: appLogoSize)
                        
                        VStack(alignment: .leading) {
                            Text(appName)
                                .font(.system(size: appTitleSize))
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
                }
                .padding(
                    EdgeInsets(
                        top: isSearching ? layout.homeDimen.searchlayoutPaddingTop : searchPaddingTop,
                        leading: isSearching ? layout.homeDimen.searchlayoutPaddingLeading : searchPaddingSide,
                        bottom: isSearching ?layout.homeDimen.searchlayoutPaddingBottom : searchPaddingBottom,
                        trailing: isSearching ? layout.homeDimen.searchlayoutPaddingTrailing : searchPaddingSide
                    )
                )
                .background(
                    Color("banner")
                        .clipShape(
                            .rect(
                                bottomLeadingRadius: layoutCornerRadius,
                                bottomTrailingRadius:layoutCornerRadius
                            )
                        )
                )
                .frame(width: layout.homeDimen.bannerLayoutWidth)
                
                HStack(alignment: .top) {
                    if (layout.homeDimen.keepSideLayouts){
                        ZStack {
                            RoundedRectangle(
                                cornerRadius: layoutCornerRadius,
                                style: .continuous
                            )
                            .foregroundColor(Color("mildBackground"))
                            .frame(width: nil, height: nil)
                        }
                        .frame(width: sideLayoutSize, height: sideLayoutSize)
                        
                    }
                    
                    ZStack {
                        Color("mildBackground")
                            .edgesIgnoringSafeArea(.bottom)
                        
                        if (isSearching) {
                            searchList(ResultList: $searchResultList)
                        } else {
                            SubScreenLayout(
                                animation: animation,
                                layout: layout,
                                isLoading: $isLoading,
                                screen: $subScreen
                            )
                        }
                    }
                    .frame(width: layout.homeDimen.mainLayoutWidth)
                    
                    if (layout.homeDimen.keepSideLayouts){
                        ZStack {
                            RoundedRectangle(
                                cornerRadius: layoutCornerRadius,
                                style: .continuous
                            )
                            .foregroundColor(Color("mildBackground"))
                            .frame(width: nil, height: nil)
                        }
                        .frame(width: sideLayoutSize, height: sideLayoutSize)
                    }
                }
                .frame(maxWidth: .infinity)
            }
            
            if(isLoading){
                Loader()
            }
        }
    }
}

struct HomeDimensValues {
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
    
    init(screenDimenType: ScreenDimenType){
        switch screenDimenType{
        case .MOBILE:
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
