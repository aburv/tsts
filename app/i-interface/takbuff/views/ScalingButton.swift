//
//  ScalingButton.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 20/12/23.
//

import SwiftUI

struct ScalingButton: ButtonStyle {
    @State var backgroundColor: Color;
    @State var color: Color;
    @State var border: Color;
    @State var cornerRadius: CGFloat;
    
    let lineWidth: CGFloat = 2;
    
    let animateDuration = 0.2;
    
    let extentedSize: CGFloat = 1.3;
    let normalSize: CGFloat = 1.0;
    
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .padding()
            .background(backgroundColor)
            .foregroundStyle(color)
            .clipShape(Capsule())
            .overlay(
                RoundedRectangle(cornerRadius: cornerRadius)
                    .stroke(border, lineWidth: lineWidth)
            )
            .animation(
                .easeOut(duration: animateDuration),
                value: configuration.isPressed
            )
            .scaleEffect(configuration.isPressed ? extentedSize : normalSize)
    }
}
