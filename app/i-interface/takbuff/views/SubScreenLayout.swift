//
//  SubScreenLayout.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 20/12/23.
//

import SwiftUI

struct SubScreenLayout: View {
    let animation: Namespace.ID
    let layout: LayoutProperties
    
    @Binding var isLoading: Bool
    @Binding var screen: SubScreen
    
    var body: some View{
        switch screen {
            case .Dashboard: DashboardScreen(isLoading: $isLoading, screen: $screen)
        }
    }
}

enum SubScreen {
    case Dashboard
}
