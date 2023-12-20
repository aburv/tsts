//
//  ContentView.swift
//  takbuff
//
//  Created by Gurunathan on 23/08/23.
//

import SwiftUI


struct SplashScreen: View {
    
    let animation: Namespace.ID
    let name: Namespace.ID
    let logo: Namespace.ID
    
    
    @Binding public var proceed: Bool
    
    @State private var isRotating = 0.0
    @State private var isShowing = true
    @State private var offset = 0.0
    @State private var loading = 3.0
    
    @State private var canSignIn = false
            
    var body: some View {
        return VStack {
            
            Spacer()
            
            VStack {
                AppLogo()
                    .matchedGeometryEffect(id: logo, in: animation)
                    .frame(width: 150.0, height: 150.0)
                    .rotationEffect(.degrees(isRotating))
                    .onAppear {
                        withAnimation(
                            .linear(duration: loading)
                            .speed(1)
                        ) {
                            isRotating = 360.0
                        }
                    }
                
                Text("Takbuff")
                    .font(.system(size: 35))
                    .foregroundColor(.white)
                    .matchedGeometryEffect(id: name, in: animation)
                
                Text("An Open Source Application")
                    .font(.system(size: 25))
                    .foregroundColor(.white)
                    .opacity(isShowing ? 1.0 : 0.0)
                    .onAppear {
                        withAnimation(
                            .spring()
                            .speed(0.5)
                        ) {
                            isShowing = false
                        }
                    }
            }
            .offset(y: offset)
            .onAppear() {
                withAnimation(
                    .bouncy
                        .delay(loading)
                ){
                    offset = -100.0
                    canSignIn = true
                }
            }
            
            Spacer()
            
            VStack(){
                Text("Powered By")
                    .font(.system(size: 25))
                    .foregroundColor(.white)
                Text("Aburv").bold()
                    .font(.system(size: 35))
                    .foregroundColor(.white)
            }
        }
    }
}
