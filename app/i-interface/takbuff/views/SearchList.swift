//
//  SearchList.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 20/12/23.
//

import SwiftUI

struct searchList: View {
    
    @Binding public var ResultList: Array<Result>
    
    let dimen: SearchDimensValues
    
    var body: some View{
        if(ResultList.count == 0){
            Text("Nothing to show")
                .font(.system(size: dimen.warningTextSize))
                .foregroundColor(Color("dark"))
        }
        else{
            List {}
                .listStyle(.plain)
        }
    }
}

struct Result{}

struct SearchDimensValues {
    let warningTextSize: CGFloat
    
    init(screenDimenType: ScreenDimenType){
        switch(screenDimenType){
        case .MOBILE:
            warningTextSize = 20.0
        case .MIN_TABLET:
            warningTextSize = 24.0
        case .TABLET:
            warningTextSize = 26.0
        case .DESKTOP:
            warningTextSize = 30.0
        }
    }
}
