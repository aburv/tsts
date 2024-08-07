//
//  SearchLayout.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 20/12/23.
//

import SwiftUI

struct SearchLayout: View {
    @Binding public var isSearching: Bool
    @Binding public var searchText: String

    var body: some View {
        ZStack (alignment: .trailing) {
            ZStack{
                RoundedRectangle(
                    cornerRadius: isSearching ? 0.0 : 25.0,
                    style: .continuous
                )
                .foregroundColor(Color(isSearching ? "background" : "bright"))
            }
            .frame(width: isSearching ? 400.0 : 45.0, height: isSearching ? 70.0 : 45.0)
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
                        .frame(width: isSearching ? 340 : 0)
                }
                
                SearchIcon(
                    isSearching: $isSearching,
                    searchText: $searchText
                )
            }

        }
        .frame(maxWidth: .infinity, alignment: .trailing)
    }
    
}

struct SearchIcon: View {
    @Binding public var isSearching: Bool
    @Binding public var searchText: String

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
                    .stroke(lineWidth: 3)
                    .rotationEffect(.degrees(80))
                    .frame(width: 15, height: 15)
                    .padding()
                RoundedRectangle(cornerRadius: 5.0)
                    .frame(width: 5.0, height: isSearching ? 20.0 : 10.0)
                    .offset(y:-17)
                    .overlay{
                        RoundedRectangle(cornerRadius: 5.0)
                            .frame(width: 5.0, height: isSearching ? 20.0 : 10.0)
                            .rotationEffect(.degrees(isSearching ? 80.0: 0.0), anchor: .center)
                            .offset(y:-17)
                    }
            }
            .rotationEffect(.degrees(-40))
            .offset(x: isSearching ? -18 : -7, y: isSearching ? -7 : 2)
            .foregroundColor(Color("dark"))
            .frame(width: 25.0, height: 25.0)
        }
    }
}


struct BackIcon: View {
    var body: some View {
        VStack(spacing: 0) {
            RoundedRectangle(cornerRadius: 5.0)
                .frame(width: 5.0, height: 15.0)
                .rotationEffect(.degrees(45.0), anchor: .center)
                .offset(y:-18)
            RoundedRectangle(cornerRadius: 5.0)
                .frame(width: 5.0, height: 15.0)
                .rotationEffect(.degrees(-45.0), anchor: .center)
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
