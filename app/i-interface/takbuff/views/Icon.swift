//
//  Icon.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 15/08/24.
//

import SwiftUI

struct Icon: View {
    @State public var logo: String;
    @State public var iconColor = "dark";
    @State public var bgColor = "bright";
    
    let size: CGFloat
    
    var body: some View {
        ZStack{
            RoundedRectangle(
                cornerRadius: size/2,
                style: .continuous
            )
            .foregroundColor(Color(bgColor))
            .frame(width: size, height: size)
            
            Image(logo)
                .resizable()
                .frame(width: size - (size/2), height: size - (size/2))
                .foregroundColor(Color(iconColor))
        }
    }
}
