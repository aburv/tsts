//
//  NewUserScreen.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 15/08/24.
//

import SwiftUI
import PhotosUI


struct NewUserScreen: View {
    let animation: Namespace.ID
    let logo: Namespace.ID
    let dp: Namespace.ID
    
    @Binding public var user: User?
    @Binding public var screen: Screen
    
    let dimen: NewUserDimensValues
    
    @State var showCropper = false
    
    @State var selectedImage: UIImage?
    @State var photopickerItem: PhotosPickerItem?
    
    @State var currentStep: Float = 0.0
    
    let views: [AnyView] = [
        AnyView(Text(""))
    ]
    
    var body: some View {
        VStack {
            AppLogo()
                .frame(width: dimen.appLogoSize, height: dimen.appLogoSize)
                .matchedGeometryEffect(id: logo, in: animation)
            
            if currentStep == 0 {
                Spacer()
                
                if user!.dp == "" {
                    Icon(logo: "icPerson", size: currentStep >= 1 ? dimen.profileIconSize - 70 : dimen.profileIconSize)
                        .foregroundStyle(Color.black)
                        .offset(y: currentStep >= 1 ? -5 : 0)
                        .offset(x: currentStep >= 1 ? -140 : 0)
                        .animation(.easeOut(duration: 0.5), value: currentStep >= 1)
                }
                else {
                    ImageView(imageId: user!.dp, size: "80")
                        .frame(width: dimen.profileLogoSize, height: dimen.profileLogoSize)
                        .cornerRadius(dimen.profileLogoSize/4)
                        .matchedGeometryEffect(id: dp, in: animation)
                }
                
                Text(user!.name)
                    .font(.system(size: user!.name.count > 10 ? dimen.nameFontSize  : dimen.nameFontSize + 10.0))
                    .bold()
                    .foregroundColor(Color("dark"))
                
                Text(user!.email)
                    .font(.system(size: user!.name.count > 30 ? dimen.emailFontSize : dimen.emailFontSize + 6.0))
                    .foregroundColor(Color("dark"))
                
                Spacer()
            }
            else {
                VStack {
                    if currentStep < 1 {
                        Spacer()
                    }
                    if user!.dp == "" {
                        Icon(logo: "icPerson", size: currentStep >= 1 ? dimen.profileIconSize - 70 : dimen.profileIconSize)
                            .foregroundStyle(Color.black)
                            .offset(y: currentStep >= 1 ? -5 : 0)
                            .offset(x: currentStep >= 1 ? -140 : 0)
                            .animation(.easeOut(duration: 0.5), value: currentStep >= 1)
                    }
                    else {
                        ImageView(imageId: user!.dp, size: "160")
                            .frame(
                                width: currentStep >= 1 ? dimen.profileLogoSize - 70 : dimen.profileLogoSize,
                                height: currentStep >= 1 ? dimen.profileLogoSize - 70 : dimen.profileLogoSize
                            )
                            .cornerRadius((currentStep >= 1 ? dimen.profileLogoSize - 70 : dimen.profileLogoSize)/4)
                            .offset(y: currentStep >= 1 ? -5 : 0)
                            .offset(x: currentStep >= 1 ? -140 : 0)
                            .animation(.easeOut(duration: 0.5), value: currentStep >= 1)
                            .matchedGeometryEffect(id: dp, in: animation)
                    }
                    
                    Text(user!.name)
                        .font(
                            .system(
                                size:currentStep >= 1 ?
                                ((user!.name.count > 10) ? dimen.nameFontSize - 5 : dimen.nameFontSize + 6.0 - 5) :
                                    ((user!.name.count) > 10 ? dimen.nameFontSize : dimen.nameFontSize + 10.0))
                        )
                        .bold()
                        .foregroundColor(Color("dark"))
                        .offset(y: currentStep >= 1 ? -75 : 0)
                        .offset(x: currentStep >= 1 ? 40 : 0)
                        .animation(.easeOut(duration: 0.5), value: currentStep >= 1)
                    
                    Text(user!.email)
                        .font(.system(size: currentStep >= 1 ?
                                      ((user!.email.count > 30) ? dimen.emailFontSize - 6 : dimen.emailFontSize + 6.0 - 6.0)  :
                                        ((user!.email.count > 30) ? dimen.emailFontSize : dimen.emailFontSize + 6.0)
                                     )
                        )
                        .foregroundColor(Color("dark"))
                        .offset(y: currentStep >= 1 ? -75 : 0)
                        .offset(x: currentStep >= 1 ? 20 : 0)
                        .animation(.easeOut(duration: 0.5), value: currentStep >= 1)
                    
                    if currentStep < 1 {
                        Spacer()
                    }
                }
                
                if currentStep >= 1 {
                    VStack{

                    }
                    .frame(maxHeight: .infinity)
                }
            }
            
            Button() {
                if Int(currentStep) != views.count {
                    
                    withAnimation {
                        if self.currentStep == 0.0 {
                            self.currentStep = 0.5
                            DispatchQueue.main.asyncAfter(deadline: .now() + 0.5){
                                self.currentStep = 1.0
                            }
                        }
                        else {
                            self.currentStep += 1.0
                        }
                    }
                    
                }
                else {
                    UserData().setOnBoardingDone() { (isDone, error) in
                        guard let _ = isDone else { return }
                        
                        withAnimation {
                            self.screen = .HOME
                        }
                    }
                }
            }
            label: {
                Image(systemName: Int(currentStep) != views.count ? "chevron.right" : "checkmark")
                    .foregroundColor(Color("bright"))
                    .font(.system(size: (dimen.buttonSize / 2), weight: .bold))
                    .frame(width: dimen.buttonSize, height: dimen.buttonSize)
                    .background(
                        Color("primary")
                            .clipShape(
                                .rect(
                                    topLeadingRadius: (dimen.buttonSize / 2),
                                    bottomLeadingRadius: (dimen.buttonSize / 2),
                                    bottomTrailingRadius:(dimen.buttonSize / 2),
                                    topTrailingRadius: (dimen.buttonSize / 2)
                                )
                            )
                    )
                    .padding(.vertical, 50.0)
            }
            
        }
        .frame(maxWidth: .infinity)
    }
}

struct NewUserDimensValues {
    let warningTextSize: CGFloat
    let appLogoSize: CGFloat
    
    let profileIconSize: CGFloat
    let profileLogoSize: CGFloat
    
    let nameFontSize: CGFloat
    let emailFontSize: CGFloat
    
    let buttonSize: CGFloat
    
    init(screenDimenType: ScreenDimenType){
        switch(screenDimenType){
        case .MOBILE:
            warningTextSize = 16.0
            appLogoSize = 50.0
            
            profileIconSize = 150.0
            profileLogoSize = 130.0
            
            nameFontSize = 26.0
            emailFontSize = 18.0
            
            buttonSize = 65.0
        case .MIN_TABLET:
            warningTextSize = 16.0
            appLogoSize = 60.0
            
            profileIconSize = 160.0
            profileLogoSize = 140.0
            
            nameFontSize = 26.0
            emailFontSize = 18.0
            
            buttonSize = 65.0
        case .TABLET:
            warningTextSize = 16.0
            appLogoSize = 70.0
            
            profileIconSize = 170.0
            profileLogoSize = 150.0
            
            nameFontSize = 26.0
            emailFontSize = 18.0
            
            buttonSize = 65.0
        case .DESKTOP:
            warningTextSize = 16.0
            appLogoSize = 80.0
            
            profileIconSize = 200.0
            profileLogoSize = 175.0
            
            nameFontSize = 26.0
            emailFontSize = 18.0
            
            buttonSize = 65.0
        }
    }
}
