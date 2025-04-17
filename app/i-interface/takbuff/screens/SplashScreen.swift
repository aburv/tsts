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
    @Binding public var user: User?
    
    let dimen: SplashDimensValues
    
    @State private var rotateDegree = 0.0
    @State private var offset = 0.0
    @State private var isSubTitleVisible = true
    @State private var isLoading = false
    
    @State private var needsSignIn = false
    
    @State private var errorMessage = ""
    
    @StateObject private var viewModel = LocationViewModel()

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
            
            if(user == nil && needsSignIn) {
                Spacer()
                
                Button {
                    doGoogleAuth()
                } label: {
                    HStack {
                        Image("icGoogle")
                            .resizable()
                            .frame(width: dimen.buttonIconSize, height: dimen.buttonIconSize)
                        
                        Text("Sign In")
                            .font(.system(size: dimen.buttonTextSize))
                    }
                }
                .buttonStyle(
                    ScalingButton(
                        backgroundColor: Color(.white),
                        color: Color(.black),
                        border: Color(.white),
                        cornerRadius: dimen.buttonIconSize
                    )
                )
                
                Button {
                    withAnimation(.spring()) {
                        self.screen = .HOME
                    }
                } label: {
                    Text("Skip")
                        .font(.system(size: dimen.buttonTextSize))
                        .foregroundStyle(Color(.white))
                }
            }
            
            if(errorMessage != "") {
                Text("Unable to connect Server")
                    .font(.system(size: dimen.warningTextSize))
                    .foregroundColor(Color(.white))
                
                Button() {
                    doInitialSetup()
                } label: {
                    Text("Try Again")
                        .font(.system(size: dimen.buttonTextSize))
                }
                .buttonStyle(
                    ScalingButton(
                        backgroundColor: Color(.white),
                        color: Color(.black),
                        border: Color(.white),
                        cornerRadius: dimen.buttonIconSize
                    )
                )
            }
            
            if (errorMessage == "" || needsSignIn) {
                Spacer()
            }
            
            VStack {
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
            doInitialSetup()
        }
    }
    
    func doGoogleAuth() {
        GAuthServices().auth { data, error in
            guard let data = data else {
                needsSignIn = false
                errorMessage = "Unexpected Error on Google Login"
                return
            }
            
            var lData: [String: Any] = [
                "deviceId": devices[0].appDeviceId,
                
            ]
            if let location = viewModel.locationCoordinates {
                lData["location"] = [
                    "lat": location.latitude.description,
                    "long": location.longitude.description
                ]
            }
            LoginData().auth( uData: data,lData: lData) { userData, error in
                
                guard let userData = userData else {
                    errorMessage = "Unable to connect Server"
                    return
                }
                
                let idToken = userData["idToken"]! as! String
                let accessToken = userData["accessToken"]! as! String
                devices[0].idToken = idToken
                devices[0].accessToken = accessToken
                
                AuthVar.setAccessToken(idToken: idToken, accessToken: accessToken)
                
                let userId: [String : String] = userData["user_id"] as! [String : String]
                self.user = User(
                    id: userData["id"]! as! String,
                    name: userData["name"]! as! String,
                    dp: userData["dp"]! as! String,
                    email: userId["val"]!
                )
                
                withAnimation {
                    screen = .NEWUSER
                }
            }
            
        }
    }
    
    func doInitialSetup() {
        rotateDegree = 0.0
        offset = 0.0
        isSubTitleVisible = true
        isLoading = true
        errorMessage = ""
        
        DispatchQueue.main.asyncAfter(deadline: .now() + oneDelay) {
            withAnimation(
                .spring()
                .speed(speed)
            ) {
                isSubTitleVisible = false
            }
        }
        
        if (devices.isEmpty){
            DeviceData().registerDevice() { dData, error in
                if error != nil {
                    errorMessage = "Unable to connect Server"
                    return
                }
                guard let dData = dData else {
                    errorMessage = "Unable to connect Server"
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
        
        if !devices.isEmpty && devices[0].idToken != nil && devices[0].accessToken != nil {
            needsSignIn = false
            AuthVar.setAccessToken(
                idToken: devices[0].idToken!,
                accessToken: devices[0].accessToken!
            )
            LoginData().refresh() { userData, error in
                guard let userData = userData else {
                    needsSignIn = false
                    errorMessage = "Unable to connect Server"
                    return
                }
                
                let idToken = userData["idToken"]! as! String
                let accessToken = userData["accessToken"]! as! String
                devices[0].idToken = idToken
                devices[0].accessToken = accessToken
                
                AuthVar.setAccessToken(idToken: idToken, accessToken: accessToken)
                
                let userId: [String : String] = userData["user_id"] as! [String : String]
                self.user = User(
                    id: userData["id"]! as! String,
                    name: userData["name"]! as! String,
                    dp: userData["dp"]! as! String,
                    email: userId["val"]!
                )
                UserData().getAppData { data, error in                    
                    proceedAfterLoading()
                }
            }
        }
        else {
            proceedAfterLoading()
        }
    }
    
    func proceedAfterLoading() {
        DispatchQueue.main.asyncAfter(deadline: .now() + threeDelay){
            isLoading = false
            withAnimation(.bouncy.speed(speed)){
                offset = dimen.liftUpOffSet
                
                if (user == nil){
                    needsSignIn = true
                }
            }
            if user != nil {
                DispatchQueue.main.asyncAfter(deadline: .now() + twoDelay){
                    withAnimation {
                        screen = .HOME
                    }
                }
            }
        }
    }
}

struct SplashDimensValues {
    let topSpace: CGFloat
    
    let appLogoSize: CGFloat
    let liftUpOffSet: CGFloat
    
    let buttonTextSize: CGFloat
    let buttonIconSize: CGFloat
    
    let warningTextSize: CGFloat
    
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
            topSpace = 300.0
            buttonTextSize = 18.0
            buttonIconSize = 30.0
            warningTextSize = 20.0
        case .MIN_TABLET:
            appLogoSize = 150.0
            appTitleSize = 54.0
            subTitleSize = 44.0
            poweredByTextSize = 35.0
            companyTextSize = 45.0
            topSpace = 500.0
            buttonTextSize = 28.0
            buttonIconSize = 50.0
            warningTextSize = 24.0
        case .TABLET:
            appLogoSize = 180.0
            appTitleSize = 54.0
            subTitleSize = 44.0
            poweredByTextSize = 35.0
            companyTextSize = 45.0
            topSpace = 500.0
            buttonTextSize = 30.0
            buttonIconSize = 55.0
            warningTextSize = 26.0
        case .DESKTOP:
            appLogoSize = 200.0
            appTitleSize = 64.0
            subTitleSize = 54.0
            poweredByTextSize = 45.0
            companyTextSize = 55.0
            topSpace = 600.0
            buttonTextSize = 34.0
            buttonIconSize = 70.0
            warningTextSize = 30.0
        }
        liftUpOffSet = 0 - ((height/2) - topSpace)
    }
}
