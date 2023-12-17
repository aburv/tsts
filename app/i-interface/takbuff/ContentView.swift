//
//  ContentView.swift
//  takbuff
//
//  Created by Gurunathan on 23/08/23.
//

import SwiftUI

struct ContentView: View {
    @State private var isRotating = 0.0
    @State private var isShowing = true

    var body: some View {
        
        return ZStack{
            Color("banner")
                .edgesIgnoringSafeArea(.all)
            
            VStack(){
                Spacer()
                
                VStack(){
                    Image("AppLogo").resizable().frame(width: 150, height: 150)
                        .rotationEffect(.degrees(isRotating))
                        .onAppear {
                            withAnimation(.linear(duration: 1)
                            .speed(0.5)) {
                                isRotating = 360.0
                            }
                        }
                    Text("Takbuff")
                        .font(.system(size: 35))
                        .foregroundColor(.white)
                    Text("An Open Source Application")
                        .font(.system(size: 25))
                        .foregroundColor(.white)
                        .opacity(isShowing ? 1.0 : 0.0)
                        .onAppear {
                            withAnimation(Animation.spring().speed(0.2)) {
                                isShowing.toggle()
                            }
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
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
