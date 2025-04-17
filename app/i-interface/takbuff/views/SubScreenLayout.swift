//
//  SubScreenLayout.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 20/12/23.
//

import SwiftUI

struct SubScreenLayout: View {
    let animation: Namespace.ID
    
    @Binding var isLoading: Bool
    @Binding var screen: Screen
    @Binding var subScreen: SubScreen
    
    let layout: LayoutProperties

    
    var body: some View{
        switch subScreen {
        case .Dashboard: DashboardScreen(
            isLoading: $isLoading,
            screen: $screen,
            subScreen: $subScreen,
            dimen: layout.dashboardDimen
        )
        }
    }
}

enum SubScreen {
    case Dashboard
}
