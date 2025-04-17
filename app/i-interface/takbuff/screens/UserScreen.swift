//
//  UserScreen.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 15/08/24.
//

import SwiftUI
import SwiftData


struct UserScreen: View {
    @Environment(\.modelContext) var modelContext
    @Query() var devices: [AppUserDevice]
    
    let animation: Namespace.ID
    let logo: Namespace.ID
    let dp: Namespace.ID

    @Binding public var user: User?
    @Binding public var screen: Screen
    
    let dimen: UserDimensValues
    
    let appName = "Takbuff"
    let version = "1.0.0"
    let subTitle = "An Open Source Application"
    let subText = "Powered By"
    let companyName = "Aburv"
        
    var body: some View {
        return VStack {
            ZStack{
                HStack {
                    Button() {
                        withAnimation(.spring()) {
                            self.screen = .HOME
                        }
                    }
                    label: {
                        BackIcon()
                    }
                    Spacer()
                }
                
                HStack{
                    Spacer()
                    
                    AppLogo()
                        .matchedGeometryEffect(id: logo, in: animation)
                        .frame(width: dimen.appLogoSize, height: dimen.appLogoSize)
                    Spacer()
                }
            }
            
            if user != nil {
                VStack {
                    if user!.dp == "" {
                        Icon(logo: "icPerson", size: dimen.profileIconSize)
                            .matchedGeometryEffect(id: dp, in: animation)
                    }
                    else {
                        ImageView(imageId: user!.dp, size: "160")
                            .frame(width: dimen.profileLogoSize, height: dimen.profileLogoSize)
                            .matchedGeometryEffect(id: dp, in: animation)
                            .cornerRadius(dimen.profileLogoSize/4)
                    }
                }
                
                Text(user!.name)
                    .font(.system(size: dimen.nameFontSize))
                    .foregroundColor(Color("dark"))

                Text(user!.email)
                    .font(.system(size: dimen.emailFontSize))
                    .foregroundColor(Color("dark"))
                
            }
            Spacer()
            
            Button() {
                signOut()
            } label: {
                Text("Sign Out")
                    .font(.system(size: dimen.buttonTextSize))
            }
            .buttonStyle(
                ScalingButton(
                    backgroundColor: Color("primary"),
                    color: Color("bright"),
                    border: Color("primary"),
                    cornerRadius: dimen.buttonIconSize
                )
            )
            
            Spacer()
            
            VStack {
                Text(subText)
                    .font(.system(size: 18))
                    .foregroundColor(Color("dark"))
                Text(companyName)
                    .bold()
                    .font(.system(size: 20))
                    .foregroundColor(Color("dark"))
                Text(appName + " © " + self.getThisYear())
                    .bold()
                    .font(.system(size: 14))
                    .foregroundColor(Color("dark"))
                Text("Version " + version)
                    .font(.system(size: 14))
                    .foregroundColor(Color("dark"))
            }
        }
        .frame(maxWidth: .infinity)
        .onAppear{
        }
    }
    
    private func getThisYear() -> String {
        return Calendar.current.component(.year, from: Date()).description
    }
    
    private func signOut() {
        devices[0].idToken = nil
        devices[0].accessToken = nil
        user = nil
        screen = .HOME
    }
}

struct UserDimensValues {
    let warningTextSize: CGFloat
    let appLogoSize: CGFloat
    
    let profileIconSize: CGFloat
    let profileLogoSize: CGFloat
    
    let nameFontSize: CGFloat
    let emailFontSize: CGFloat
    
    let buttonTextSize: CGFloat
    let buttonIconSize: CGFloat
    
    init(screenDimenType: ScreenDimenType){
        switch(screenDimenType){
        case .MOBILE:
            warningTextSize = 16.0
            appLogoSize = 50.0
            
            profileIconSize = 150.0
            profileLogoSize = 130.0
            
            nameFontSize = 26.0
            emailFontSize = 18.0
                        
            buttonTextSize = 18.0
            buttonIconSize = 30.0
        case .MIN_TABLET:
            warningTextSize = 16.0
            appLogoSize = 60.0
            
            profileIconSize = 160.0
            profileLogoSize = 140.0
            
            nameFontSize = 26.0
            emailFontSize = 18.0
            
            buttonTextSize = 28.0
            buttonIconSize = 50.0
        case .TABLET:
            warningTextSize = 16.0
            appLogoSize = 70.0
            
            profileIconSize = 175.0
            profileLogoSize = 150.0

            nameFontSize = 26.0
            emailFontSize = 18.0
            
            buttonTextSize = 30.0
            buttonIconSize = 55.0
        case .DESKTOP:
            warningTextSize = 16.0
            appLogoSize = 80.0
            
            profileIconSize = 200.0
            profileLogoSize = 175.0
            
            nameFontSize = 26.0
            emailFontSize = 18.0
            
            buttonTextSize = 34.0
            buttonIconSize = 70.0
        }
    }
}
