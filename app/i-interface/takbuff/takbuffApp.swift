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
                        ResponsiveView {properties in
                            HomeScreen(animation: animation, name: name, logo: logo, layout: properties)
                        }
                    }
                    else {
                        SplashScreen(animation: animation, name: name, logo: logo, proceed: $proceed)
                    }
                } .padding([.horizontal], 1.0)
            }
        }
    }
}

struct ResponsiveView<Content:View>: View {
    var content:(LayoutProperties) -> Content
    var body: some View {
        GeometryReader{geo in
            let height = geo.size.height
            let width = geo.size.width
            let landScape = height > 500 && width > 900
            let dimen = CustomDimensValues(height:height, width:width)
            content(
                LayoutProperties(
                    isLandscape: landScape,
                    dimen: dimen,
                    height: height,
                    width: width
                )
            )
        }
    }
}

struct CustomDimensValues {
    let keepBanner: Bool 
    let keepSideLayouts: Bool
    let bannerLayoutWidth: CGFloat?
    
    let mainLayoutWidth: CGFloat?
    
    let searchlayoutPaddingTop: CGFloat
    let searchlayoutPaddingBottom: CGFloat
    let searchlayoutPaddingTrailing: CGFloat
    let searchlayoutPaddingLeading: CGFloat
    
    let searchingBgHeight: CGFloat
    let searchingBgWidth: CGFloat?
    let searchingCornerRadius: CGFloat
    
    init(height:CGFloat, width:CGFloat){
        switch width{
        case _ where width<700.0:
            keepBanner = false
            keepSideLayouts = false
            bannerLayoutWidth = nil
            mainLayoutWidth = nil
            
            searchlayoutPaddingTop = 0.0
            searchlayoutPaddingBottom = 0.0
            searchlayoutPaddingLeading = 0.0
            searchlayoutPaddingTrailing = 0.0
            
            searchingBgHeight = 70.0
            searchingBgWidth = nil
            searchingCornerRadius = 0.0
        case _ where width>=700.0 && width<1000.0:
            keepBanner = true
            keepSideLayouts = false
            bannerLayoutWidth = 800.0
            mainLayoutWidth = 700.0
            
            searchlayoutPaddingTop = 0.0
            searchlayoutPaddingBottom = 5.0
            searchlayoutPaddingLeading = 20.0
            searchlayoutPaddingTrailing = 10.0
            
            searchingBgHeight = 45.0
            searchingBgWidth = 350.0
            searchingCornerRadius = 25.0
        case _ where width>=1000.0 && width<1200.0:
            keepBanner = true
            keepSideLayouts = false
            bannerLayoutWidth = 900.0
            mainLayoutWidth =  700.0
            
            searchlayoutPaddingTop = 0.0
            searchlayoutPaddingBottom = 5.0
            searchlayoutPaddingLeading = 20.0
            searchlayoutPaddingTrailing = 10.0
            
            searchingBgHeight = 45.0
            searchingBgWidth = 400.0
            searchingCornerRadius = 25.0
        case _ where width>=1200.0:
            keepBanner = true
            keepSideLayouts = true
            bannerLayoutWidth = 1100.0
            mainLayoutWidth = 700.0
            
            searchlayoutPaddingTop = 0.0
            searchlayoutPaddingBottom = 5.0
            searchlayoutPaddingLeading = 20.0
            searchlayoutPaddingTrailing = 10.0
            
            searchingBgHeight = 45.0
            searchingBgWidth = 400.0
            searchingCornerRadius = 25.0
        default:
            keepBanner = true
            keepSideLayouts = true
            bannerLayoutWidth = 1200.0
            mainLayoutWidth = 700.0
            
            searchlayoutPaddingTop = 0.0
            searchlayoutPaddingBottom = 5.0
            searchlayoutPaddingLeading = 20.0
            searchlayoutPaddingTrailing = 10.0
            
            searchingBgHeight = 45.0
            searchingBgWidth = 400.0
            searchingCornerRadius = 25.0
        }
    }
}

struct LayoutProperties {
    var isLandscape:Bool
    var dimen:CustomDimensValues
    var height:CGFloat
    var width:CGFloat
}
