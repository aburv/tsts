//
//  TabBarView.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 08/09/24.
//

import SwiftUI

struct TabBarView: View {
    let optionTitles: [String]
    
    @Binding var selectedTabIndex: Int
    
    let radius = 10.0
    
    let layoutMargin = 5.0
    let layoutPadding = 5.0
    
    var body: some View{
        HStack {
            ForEach(Array(zip(optionTitles.indices, optionTitles)), id: \.0) {index, name in
                TabBarItem(title: name, index: index, selectedTabIndex: $selectedTabIndex, radius: radius )
                    .padding(.all, layoutPadding)
            }
        }
        .background(Color("background")
            .clipShape(
                .rect(
                    topLeadingRadius: radius,
                    bottomLeadingRadius: radius,
                    bottomTrailingRadius: radius,
                    topTrailingRadius: radius
                )
            )
        )
        .padding(.horizontal, layoutMargin)
    }
}

struct TabBarItem: View {
    let title: String
    let index: Int
    
    @Binding var selectedTabIndex: Int
    
    let radius: CGFloat
    
    let itemHeight = 30.0
    let textSize = 14.0
    
    var body: some View{
        Button {
            withAnimation(.easeInOut.speed(10.0)) {
                selectedTabIndex = index
            }
        } label: {
            HStack {
                Spacer()
                
                Text(title)
                    .font(.system(size: textSize))
                    .fontWeight(selectedTabIndex == index ? .bold : .regular)
                    .foregroundColor(Color(selectedTabIndex == index ? "bright" : "dark"))
                    .frame(height: itemHeight)
                
                Spacer()
            }
            .background(Color(selectedTabIndex == index ? "primary" : "background")
                .clipShape(
                    .rect(
                        topLeadingRadius: radius,
                        bottomLeadingRadius: radius,
                        bottomTrailingRadius: radius,
                        topTrailingRadius: radius
                    )
                )
            )
        }
        .buttonStyle(.plain)
    }
}
