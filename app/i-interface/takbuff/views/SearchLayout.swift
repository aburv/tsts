//
//  SearchLayout.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 20/12/23.
//

import SwiftUI

struct SearchLayout: View {
    let layout:LayoutProperties
    
    @Binding public var isSearching: Bool
    @Binding public var searchText: String
    
    let radius = 25.0
    let nonSearchingIconBgSize = 45.0
    
    var body: some View {
        ZStack (alignment: .trailing) {
            ZStack{
                RoundedRectangle(
                    cornerRadius: isSearching ? layout.homeDimen.searchingCornerRadius : radius,
                    style: .continuous
                )
                .foregroundColor(Color(isSearching ? "background" : "bright"))
                .frame(width: nil, height: nil)
            }
            .frame(
                width: isSearching ? layout.homeDimen.searchingBgWidth : nonSearchingIconBgSize,
                height: isSearching ? layout.homeDimen.searchingBgHeight : nonSearchingIconBgSize
            )
            .foregroundColor(Color("dark"))
            
            HStack{
                if(isSearching){
                    Button{
                        DispatchQueue.main.asyncAfter(deadline: .now() + 0.3){
                            withAnimation{
                                isSearching = false
                            }
                        }
                    } label : {
                        BackIcon()
                    }
                    
                    TextField("Search here", text: $searchText)
                        .foregroundColor(Color("dark"))
                        .padding(.horizontal)
                        .frame(maxWidth: isSearching ? layout.homeDimen.searchingBgWidth : .infinity)
                }
                
                SearchIcon(
                    isSearching: $isSearching,
                    searchText: $searchText
                )
            }
        }
        .frame(maxWidth: layout.homeDimen.searchingBgWidth, alignment: .trailing)
    }
    
}

struct SearchIcon: View {
    @Binding public var isSearching: Bool
    @Binding public var searchText: String
    
    let rotateAngle = 80.0
    let circleSize = 15.0
    let lineCornerRadius = 5.0
    let lineWidth = 5.0
    let searchHeight = 20.0
    let nonSearchheight = 10.0
    
    let iconSize = 25.0
    var body: some View {
        Button {
            if !isSearching {
                DispatchQueue.main.asyncAfter(deadline: .now() + 0.3){
                    withAnimation{
                        isSearching = true
                    }
                }
            }
            else{
                searchText.removeAll()
            }
        } label: {
            VStack(spacing: 0) {
                Circle()
                    .trim(from: 0.0, to: isSearching ? 0.0: 1.0)
                    .stroke(lineWidth: lineWidth - 2)
                    .rotationEffect(.degrees(rotateAngle))
                    .frame(width: circleSize, height: circleSize)
                    .padding()
                RoundedRectangle(cornerRadius: lineCornerRadius)
                    .frame(width: lineWidth, height: isSearching ? searchHeight : nonSearchheight)
                    .offset(y:-17)
                    .overlay{
                        RoundedRectangle(cornerRadius: lineCornerRadius)
                            .frame(width:lineWidth, height: isSearching ? searchHeight : nonSearchheight)
                            .rotationEffect(.degrees(isSearching ? rotateAngle: 0.0), anchor: .center)
                            .offset(y:-17)
                    }
            }
            .rotationEffect(.degrees( 0 - (rotateAngle / 2 )))
            .offset(x: isSearching ? -18 : -7, y: isSearching ? -7 : 2)
            .foregroundColor(Color("dark"))
            .frame(width: iconSize, height: iconSize)
        }
    }
}


struct BackIcon: View {
    let lineWidth = 5.0
    let lineHeight = 15.0
    let lineCornerRadius = 5.0
    let lineAngle = 45.0
    
    var body: some View {
        VStack(spacing: 0) {
            RoundedRectangle(cornerRadius: lineCornerRadius)
                .frame(width: lineWidth, height: lineHeight)
                .rotationEffect(.degrees(lineAngle), anchor: .center)
                .offset(y:-18)
            RoundedRectangle(cornerRadius: lineCornerRadius)
                .frame(width: lineWidth, height: lineHeight)
                .rotationEffect(.degrees(0 - lineAngle), anchor: .center)
                .offset(y:-25)
        }
        .foregroundColor(Color("dark"))
        .padding(
            EdgeInsets(
                top: 40.0,
                leading: 20.0,
                bottom: 0.0,
                trailing: 0.0
            )
        )
    }
}
