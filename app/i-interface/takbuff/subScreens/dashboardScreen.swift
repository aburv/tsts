//
//  dashboardScreen.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 11/08/24.
//

import SwiftUI

struct DashboardScreen: View {
    
    @Binding var isLoading: Bool
    @Binding var screen: SubScreen

    var body: some View {
        Text("No tournaments to show")
            .font(.system(size: 16))
            .foregroundColor(Color("dark"))
    }
}
