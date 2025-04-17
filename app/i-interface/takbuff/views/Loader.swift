//
//  Loader.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 20/12/23.
//

import SwiftUI
 
struct Loader: View {
    @State private var rotationAngle = 0.0
    private let ringSize: CGFloat = 80

    var colors: [Color] = [Color.red, Color.red.opacity(0.3)]

    var body: some View {
        ZStack {
            Rectangle()
                .fill(.gray.opacity(0.7))
                .ignoresSafeArea()
            
            ZStack {
                AppLogo()
                    .frame(width: 50.0, height: 50.0)

            }
            .rotationEffect(.degrees(rotationAngle))
            .padding(.horizontal, 80)
            .padding(.vertical, 50)
            .onAppear {
                withAnimation(.linear(duration: 1.5)
                            .repeatForever(autoreverses: false)) {
                        rotationAngle = 360.0
                    }
            }
            .onDisappear{
                rotationAngle = 0.0
            }
        }

        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .center)
    }
}
