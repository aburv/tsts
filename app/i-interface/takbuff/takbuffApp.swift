//
//  takbuffApp.swift
//  takbuff
//
//  Created by Gurunathan on 23/08/23.
//

import SwiftUI

@main
struct takbuffApp: App {
    @Namespace private var animation
    @Namespace private var logo
    @Namespace private var name
    
    @State var proceed = false

    var body: some Scene {
        WindowGroup {
            ZStack {
                Color("banner")
                    .edgesIgnoringSafeArea(.all)
                
                if(proceed) {
                    Color("background")
                        .edgesIgnoringSafeArea(.bottom)
                }
                
                VStack{
                    if(proceed){
                        HomeScreen(animation: animation, name: name, logo: logo)
                    }
                    else {
                        SplashScreen(animation: animation, name: name, logo: logo, proceed: $proceed)
                    }
                } .padding([.horizontal], 1.0)
            }
            .onAppear{
                DispatchQueue.main.asyncAfter(deadline: .now() + 5.0){
                    withAnimation{
                        proceed = true
                    }
                }
            }
        }
    }
}
