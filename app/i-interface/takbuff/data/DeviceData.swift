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
    private static let namespace = "device/"
    
    func registerDevice(
        completion:@escaping (String?, Error?) -> ()
    ) {
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
        dataAPI.post(path: DeviceData.namespace + "register", body: dData) { data, error in
            guard let data = data else {
                completion(nil, error)
                return
            }
            
            var regResponse = try! JSONDecoder().decode(Dictionary<String, String>.self, from: data)
            DispatchQueue.main.async {
                let deviceData = regResponse.removeValue(forKey: "data")!
                completion(deviceData, nil)
            }
        }
    }
}
