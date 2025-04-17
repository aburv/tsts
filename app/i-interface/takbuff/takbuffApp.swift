//
//  takbuffApp.swift
//  takbuff
//
//  Created by Gurunathan on 23/08/23.
//

import SwiftUI

@main
struct takbuffApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) private var appDelegate
    
    @Namespace private var animation
    @Namespace private var logo
    @Namespace private var name
    @Namespace private var dp
    
    @State var user: User? = nil
    
    @State var screen: Screen = .SPLASH
    
    var body: some Scene {
        WindowGroup {
            ZStack {
                Color((screen == .HOME || screen == .SPLASH) ? "banner" : "background")
                    .edgesIgnoringSafeArea(.all)
                
                if(screen == .HOME) {
                    Color("background")
                        .edgesIgnoringSafeArea(.bottom)
                }
                
                VStack{
                    switch screen {
                    case .HOME:
                        ResponsiveView { properties in
                            HomeScreen(
                                animation: animation,
                                name: name,
                                logo: logo,
                                dp: dp,
                                user: $user,
                                screen: $screen,
                                layout: properties
                            )
                        }
                    case .USER:
                        ResponsiveView { properties in
                            UserScreen(
                                animation: animation,
                                logo: logo,
                                dp: dp,
                                user: $user,
                                screen: $screen,
                                dimen: properties.userDimen
                            )
                        }
                    case .NEWUSER:
                        ResponsiveView { properties in
                            NewUserScreen(
                                animation: animation,
                                logo: logo,
                                dp: dp,
                                user: $user,
                                screen: $screen,
                                dimen: properties.newUserDimen
                            )
                        }
                    case .SPLASH:
                        ResponsiveView { properties in
                            SplashScreen(
                                animation: animation,
                                name: name,
                                logo: logo,
                                screen: $screen,
                                user: $user,
                                dimen: properties.splashDimen
                            )
                        }
                    }
                }
                .padding([.horizontal], 1.0)
            }
        }
        .modelContainer(for: AppUserDevice.self)
    }
}

struct ResponsiveView<Content:View>: View {
    var content:(LayoutProperties) -> Content
    var body: some View {
        GeometryReader{ geo in
            let height = geo.size.height
            let width = geo.size.width
            let landScape = height > 500.0 && width > 900.0
            let screenDimenType: ScreenDimenType = getDimens(width: width)
            let homeDimen = HomeDimensValues(screenDimenType: screenDimenType)
            let splashDimen = SplashDimensValues(screenDimenType: screenDimenType, height: height)
            let newUserDimen = NewUserDimensValues(screenDimenType: screenDimenType)
            let userDimen = UserDimensValues(screenDimenType: screenDimenType)
            let dashboardDimen = DashboardDimensValues(screenDimenType: screenDimenType)
            let searchDimen = SearchDimensValues(screenDimenType: screenDimenType)
            
            content(
                LayoutProperties(
                    isLandscape: landScape,
                    homeDimen: homeDimen,
                    splashDimen: splashDimen,
                    newUserDimen: newUserDimen,
                    userDimen: userDimen,
                    dashboardDimen: dashboardDimen,
                    searchDimen:searchDimen,
                    height: height,
                    width: width
                )
            )
        }
    }
    
    func getDimens(width: CGFloat) -> ScreenDimenType {
        if (width<700.0) {
            .MOBILE
        }
        else if (width>=700.0 && width<1000.0) {
            .MIN_TABLET
        }
        else if (width>=1000.0 && width<1200.0) {
            .TABLET
        }
        else {
            .DESKTOP
        }
    }
}

enum ScreenDimenType {
    case MOBILE, MIN_TABLET, TABLET, DESKTOP
}

class AppDelegate: NSObject, UIApplicationDelegate {
    static var orientation: UIInterfaceOrientationMask = .portrait
    
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchingOptions: [UIApplication.LaunchOptionsKey: Any]? = nil) -> Bool{
        return true
    }
    
    func application(_ application: UIApplication, supportedInterfaceOrientationsFor window: UIWindow?) -> UIInterfaceOrientationMask {
        return Self.orientation
    }
}

extension View {
    func setOrientation(_ orientation: UIInterfaceOrientationMask) {
        if let windowScene = UIApplication.shared.connectedScenes.first as? UIWindowScene {
            AppDelegate.orientation = orientation
            windowScene.requestGeometryUpdate(.iOS(interfaceOrientations: orientation))
            windowScene.keyWindow?.rootViewController?.setNeedsUpdateOfSupportedInterfaceOrientations()
        }
    }
}

struct LayoutProperties {
    var isLandscape:Bool
    var homeDimen: HomeDimensValues
    var splashDimen: SplashDimensValues
    var newUserDimen: NewUserDimensValues
    var userDimen: UserDimensValues
    var dashboardDimen: DashboardDimensValues
    var searchDimen: SearchDimensValues
    var height:CGFloat
    var width:CGFloat
}
