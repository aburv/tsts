//
//  AppUserDevice.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 24/09/24.
//

import SwiftData

@Model
final class AppUserDevice {
    @Attribute(.unique) var appDeviceId: String
    var isActive: Bool
    var accessToken: String?
    var idToken: String?

    init(appDeviceId: String) {
        self.appDeviceId = appDeviceId
        self.isActive = true
    }
    
    func updateTokens( accessToken: String, idToken: String) {
        self.accessToken = accessToken
        self.idToken = idToken
    }
}

struct AuthVar {
    private static var accessToken: String = ""
    
    static func setAccessToken(idToken: String, accessToken: String) {
        AuthVar.accessToken = idToken + AppData.SEPARATOR + accessToken
    }
    
    static func getAccessToken() -> String{
        return AuthVar.accessToken
    }
}
