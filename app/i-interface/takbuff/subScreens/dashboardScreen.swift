//
//  dashboardScreen.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 11/08/24.
//

import SwiftUI

struct DashboardScreen: View {
    
    @Binding var isLoading: Bool
    @Binding var screen: Screen
    @Binding var subScreen: SubScreen
    
    let dimen: DashboardDimensValues

    var body: some View {
        Text("No tournaments to show")
            .font(.system(size: dimen.warningTextSize))
            .foregroundColor(Color("dark"))
    }
}

struct DashboardDimensValues {
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
