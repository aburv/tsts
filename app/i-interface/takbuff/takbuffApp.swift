//
//  takbuffApp.swift
//  takbuff
//
//  Created by Gurunathan on 23/08/23.
//

import SwiftUI
import SwiftData

@main
struct takbuffApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) private var appDelegate
    
    @Namespace private var animation
    @Namespace private var logo
    @Namespace private var name
    
    @State var screen: Screen = .SPLASH

    var body: some Scene {
        WindowGroup {
            ZStack {
                Color("banner")
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
                                screen: $screen,
                                layout: properties
                            )
                        }
                    case .SPLASH:
                        ResponsiveView { properties in
                            SplashScreen(
                                animation: animation,
                                name: name,
                                logo: logo,
                                screen: $screen,
                                dimen: properties.splashDimen
                            )
                        }
                    }
                } .padding([.horizontal], 1.0)
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
            
            content(
                LayoutProperties(
                    isLandscape: landScape,
                    homeDimen: homeDimen,
                    splashDimen: splashDimen,
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
    var height:CGFloat
    var width:CGFloat
}
