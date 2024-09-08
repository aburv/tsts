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
    let layout:LayoutProperties
    
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
                    if(!isSearching || layout.dimen.keepBanner){
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
                        top: isSearching ? layout.dimen.searchlayoutPaddingTop : searchPaddingTop,
                        leading: isSearching ? layout.dimen.searchlayoutPaddingLeading : searchPaddingSide,
                        bottom: isSearching ? layout.dimen.searchlayoutPaddingBottom : searchPaddingBottom,
                        trailing: isSearching ? layout.dimen.searchlayoutPaddingTrailing : searchPaddingSide
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
                .frame(width: layout.dimen.bannerLayoutWidth)
                
                HStack(alignment: .top) {
                    if (layout.dimen.keepSideLayouts){
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
                            SubScreenLayout(isLoading: $isLoading)
                        }
                    }
                    .frame(width: layout.dimen.mainLayoutWidth)
                    
                    if (layout.dimen.keepSideLayouts){
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
