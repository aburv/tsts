//
//  SearchList.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 20/12/23.
//

import SwiftUI

struct searchList: View {
    
    @Binding public var ResultList: Array<Result>
    
    var body: some View{
        if(ResultList.count == 0){
            Text("Nothing to show")
                .font(.system(size: 20))
                .foregroundColor(Color("dark"))
        }
        else{
            List {}
                .listStyle(.plain)
        }
    }
}

struct Result{}
