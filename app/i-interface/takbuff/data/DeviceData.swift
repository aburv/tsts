//
//  userData.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 17/01/24.
//

import Foundation
import SwiftData
import UIKit

class DeviceData {
    
    private let dataAPI: ApiRequest = ApiRequest()
    let namespace = "device/"
    
    func registerDevice(modelContext: ModelContext) {
        let device = UIDevice.current
        
        let dtype = switch(UIDevice.current.userInterfaceIdiom) {
        case .pad :
            "T"
        case .phone:
            "P"
        case .tv:
            "D"
        case .carPlay:
            "D"
        case .mac:
            "D"
        case .vision:
            "D"
        case .unspecified:
            ""
        @unknown default:
            ""
        }
        
        let dData: [String: Any]  = [
            "deviceId": device.identifierForVendor!.uuidString,
            "os": device.systemName,
            "version": device.systemVersion,
            "other": [device.localizedModel, device.name, device.model].joined(separator:" "),
            "deviceType": dtype,
            "platform": "A"
        ]
        
        dataAPI.post(path: namespace + "register", body: dData) { data, error in
            guard let data = data else {
                return
            }
            
            var device = try! JSONDecoder().decode(Dictionary<String, String>.self, from: data)
            DispatchQueue.main.async {
                DeviceDb().save(modelContext: modelContext, deviceId: device.removeValue(forKey: "data")!)
            }
        }
    }
    
    func isRegistered(modelContext: ModelContext, device: [AppUserDevice]) {
        if (device.count == 0) {
            registerDevice(modelContext: modelContext)
        }
    }
}
