//
//  ContentView.swift
//  takbuff
//
//  Created by Gurunathan on 23/08/23.
//

import SwiftUI
import SwiftData


struct SplashScreen: View {
    @Environment(\.modelContext) var modelContext
    @Query() var device: [AppUserDevice]
    
    let animation: Namespace.ID
    let name: Namespace.ID
    let logo: Namespace.ID
    
    @Binding public var proceed: Bool
    
    @State private var rotateDegree = 0.0
    @State private var offset = 0.0
    @State private var isSubTitleVisible = true
    @State private var isLoading = true

    @State private var canSignIn = false
    
    let appName = "Takbuff"
    let subTitle = "An Open Source Application"
    let subText = "Powered By"
    let companyName = "Aburv"
    
    let appLogoSize = 150.0
    let liftUpOffSet = -100.0
    let fullRotatingDegree = 360.0
    
    let appTitleSize = 35.0
    let subTitleSize = 25.0
    
    let fullOpacity = 1.0
    let zeroOpacity = 0.0
    
    let speed = 0.7
    
    let oneDelay = 1.0
    let twoDelay = 2.0
    let threeDelay = 3.0
    
    let rotate = Animation.linear(duration: 1.0).speed(0.7).repeatForever(autoreverses: false)
    
    var body: some View {
        return VStack {
            
            Spacer()
            
            VStack {
                if(isLoading){
                    AppLogo()
                        .frame(width: appLogoSize, height: appLogoSize)
                        .rotationEffect(.degrees(rotateDegree))
                        .onAppear {
                            withAnimation(rotate) {
                                rotateDegree = fullRotatingDegree
                            }
                        }
                }
                else{
                    AppLogo()
                        .matchedGeometryEffect(id: logo, in: animation)
                        .frame(width: appLogoSize, height: appLogoSize)
                }
                Text(appName)
                    .font(.system(size: appTitleSize))
                    .foregroundColor(.white)
                    .matchedGeometryEffect(id: name, in: animation)
                
                Text(subTitle)
                    .font(.system(size: subTitleSize))
                    .foregroundColor(.white)
                    .opacity(isSubTitleVisible ? fullOpacity : zeroOpacity)
                    .onAppear {
                        withAnimation(
                            .spring()
                            .delay(oneDelay)
                            .speed(speed)
                        ) {
                            isSubTitleVisible = false
                        }
                    }
            }
            .offset(y: offset)
            
            Spacer()
            
            VStack(){
                Text(subText)
                    .font(.system(size: 20))
                    .foregroundColor(.white)
                Text(companyName).bold()
                    .font(.system(size: 30))
                    .foregroundColor(.white)
            }
        }
        .onAppear{
            DeviceData().isRegistered(modelContext: modelContext, device: device)
            UserData().getAppData { data, error in
                guard error == nil else {return}
                DispatchQueue.main.asyncAfter(deadline: .now() + threeDelay){
                    isLoading = false
                    withAnimation(.bouncy.speed(speed)){
                        offset = liftUpOffSet
                        canSignIn = true
                    }
                    DispatchQueue.main.asyncAfter(deadline: .now() + twoDelay){
                        withAnimation{
                            proceed = true
                        }
                    }
                }
            }
        }
    }
}
