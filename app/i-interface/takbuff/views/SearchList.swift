//
//  SearchList.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 20/12/23.
//

import SwiftUI

struct searchList: View {
    
    var body: some View{
        List {}
        .listStyle(.plain)
        .background(
            Color("background")
                .edgesIgnoringSafeArea(/*@START_MENU_TOKEN@*/.all/*@END_MENU_TOKEN@*/)
        )
    }
}

#Preview {
    searchList()
}
