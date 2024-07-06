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
    
    var body: some View {
        VStack {
            HStack {
                if(!isSearching){
                    AppLogo()
                        .matchedGeometryEffect(id: logo, in: animation)
                        .frame(width: 50.0, height: 50.0)
                    
                    VStack(alignment: .leading) {
                        Text("Takbuff")
                            .font(.system(size: 25))
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
                    top: isSearching ? 0.0: 10.0,
                    leading: isSearching ? 0.0: 20.0,
                    bottom: isSearching ? 0.0: 20.0,
                    trailing: isSearching ? 0.0: 20.0
                )
            )
            .background(
                Color("banner")
                    .clipShape(
                        .rect(
                            topLeadingRadius: 0,
                            bottomLeadingRadius: 20,
                            bottomTrailingRadius:20,
                            topTrailingRadius: 0
                        )
                    )
            )
            
            if (isSearching) {
                searchList()
            } else {
                SubScreenLayout()
            }
        }
    }
}
