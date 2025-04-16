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
    @Query() var devices: [AppUserDevice]
    
    let animation: Namespace.ID
    let name: Namespace.ID
    let logo: Namespace.ID
    
    @Binding public var screen: Screen

    let dimen: SplashDimensValues
    
    @State private var rotateDegree = 0.0
    @State private var offset = 0.0
    @State private var isSubTitleVisible = true
    @State private var isLoading = true

    @State private var canSignIn = false
    
    let appName = "Takbuff"
    let subTitle = "An Open Source Application"
    let subText = "Powered By"
    let companyName = "Aburv"
    
    let fullRotatingDegree = 360.0
    
    let fullOpacity = 1.0
    let zeroOpacity = 0.0
    
    let speed = 0.7
    
    let oneDelay = 1.0
    let twoDelay = 2.0
    let threeDelay = 3.0
    
    let rotate = Animation
        .linear(duration: 1.0)
        .speed(0.7)
        .repeatForever(autoreverses: false)
    
    var body: some View {
        VStack {
            
            Spacer()
            
            VStack {
                if(isLoading){
                    AppLogo()
                        .frame(width: dimen.appLogoSize, height: dimen.appLogoSize)
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
                        .frame(width: dimen.appLogoSize, height: dimen.appLogoSize)
                }
                
                Text(appName)
                    .font(.system(size: dimen.appTitleSize))
                    .foregroundColor(.white)
                    .matchedGeometryEffect(id: name, in: animation)
                
                Text(subTitle)
                    .font(.system(size: dimen.subTitleSize))
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
                    .font(.system(size: dimen.poweredByTextSize))
                    .foregroundColor(.white)
                Text(companyName).bold()
                    .font(.system(size: dimen.companyTextSize))
                    .foregroundColor(.white)
            }
        }
        .frame(maxWidth: .infinity)
        .onAppear{
            if (devices.isEmpty) {
                DeviceData().registerDevice() { dData, error in
                    if error != nil {
                        return
                    }
                    guard let dData = dData else {
                        return
                    }
                    let deviceData = AppUserDevice(appDeviceId: dData)
                    modelContext.insert(deviceData)
                    do {
                        try modelContext.save()
                    } catch {
                        print("Failed to save context:", error)
                    }
                }
            }
            UserData().getAppData { data, error in
                guard error == nil else {return}
                DispatchQueue.main.asyncAfter(deadline: .now() + threeDelay){
                    isLoading = false
                    withAnimation(.bouncy.speed(speed)){
                        offset = dimen.liftUpOffSet
                        canSignIn = true
                    }
                    DispatchQueue.main.asyncAfter(deadline: .now() + twoDelay){
                        withAnimation{
                            screen = .HOME
                        }
                    }
                }
            }
        }
    }
}

struct SplashDimensValues {
    let topSpace: CGFloat = 250.0
    
    let appLogoSize: CGFloat
    let liftUpOffSet: CGFloat
    
    let appTitleSize: CGFloat
    let subTitleSize: CGFloat
    
    let poweredByTextSize: CGFloat
    let companyTextSize: CGFloat
    
    init(screenDimenType: ScreenDimenType, height: CGFloat){
        switch(screenDimenType){
        case .MOBILE:
            appLogoSize = 100.0
            appTitleSize = 35.0
            subTitleSize = 25.0
            poweredByTextSize = 20.0
            companyTextSize = 30.0
        case .MIN_TABLET:
            appLogoSize = 150.0
            appTitleSize = 54.0
            subTitleSize = 44.0
            poweredByTextSize = 35.0
            companyTextSize = 45.0
        case .TABLET:
            appLogoSize = 180.0
            appTitleSize = 54.0
            subTitleSize = 44.0
            poweredByTextSize = 35.0
            companyTextSize = 45.0
        case .DESKTOP:
            appLogoSize = 200.0
            appTitleSize = 64.0
            subTitleSize = 54.0
            poweredByTextSize = 45.0
            companyTextSize = 55.0
        }
        liftUpOffSet = 0 - ((height/2) - topSpace)
    }
}
