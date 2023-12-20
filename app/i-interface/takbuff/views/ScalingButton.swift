//
//  ScalingButton.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 20/12/23.
//

import SwiftUI

struct ScalingButton: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .padding()
            .background(.white)
            .foregroundStyle(.black)
            .clipShape(Capsule())
            .scaleEffect(configuration.isPressed ? 1.2 : 1)
            .animation(.easeOut(duration: 0.2), value: configuration.isPressed)
    }
}
