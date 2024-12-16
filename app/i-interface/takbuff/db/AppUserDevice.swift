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
    var id: String?
    var name: String?
    var email: String?
    var dp: String?
    
    init(appDeviceId: String) {
        self.appDeviceId = appDeviceId
        self.isActive = true
    }
    
    func setUser(id: String, name: String, email:String, dp: String, accessToken: String) {
        self.id = id
        self.name = name
        self.email = email
        self.dp = dp
    }
}
class DeviceDb{
    @MainActor
    func save (modelContext: ModelContext, deviceId: String) {
        let deviceData = AppUserDevice(appDeviceId: deviceId)
        modelContext.insert(deviceData)
        try! modelContext.save()
    }
}
