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
    
    @State private var isSearching = false
    @State private var searchText = ""
    @State private var isLoading = false
    @State private var searchResultList: Array<Result> = []
    
    let appName = "Takbuff"
    
    let appLogoSize = 50.0
    let appTitleSize = 25.0
    
    let layoutCornerRadius = 20.0
        
    let searchPaddingTop = 10.0
    let searchPaddingSide = 20.0
    let searchPaddingBottom = 15.0
    
    var body: some View {
        ZStack{
            VStack {
                HStack {
                    if(!isSearching){
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
                        isSearching: $isSearching,
                        searchText: $searchText
                    )
                }
                .padding(
                    EdgeInsets(
                        top: isSearching ? 0.0 : searchPaddingTop,
                        leading: isSearching ? 0.0 : searchPaddingSide,
                        bottom: isSearching ? 0.0 : searchPaddingBottom,
                        trailing: isSearching ? 0.0 : searchPaddingSide
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
                
                if (isSearching) {
                    searchList(ResultList: $searchResultList)
                } else {
                    SubScreenLayout(isLoading: $isLoading)
                }
            }
            
            if(isLoading){
                Loader()
            }
        }
    }
}
