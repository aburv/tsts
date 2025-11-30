//
//  InputText.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 26/12/23.
//

import SwiftUI

struct InputText: View {
    @State public var placeholder: String
    @Binding public var value: String
    @State public var width: CGFloat
    
    
    var body: some View {
        
        TextField(placeholder, text: $value)
            .frame(width: width)
            .foregroundStyle(Color("dark"))
            .padding(
                EdgeInsets(
                    top: 10.0,
                    leading: 20.0,
                    bottom: 10.0,
                    trailing: 20.0
                )
            )
            .overlay(
                RoundedRectangle(cornerRadius: 30)
                    .stroke(Color("primary"), lineWidth: 2)
                
            )
            .background(
                RoundedRectangle(cornerRadius: 30)
                    .fill(Color("bright"))
            )
    }
}
