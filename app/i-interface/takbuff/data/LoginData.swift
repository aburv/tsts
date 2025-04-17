//
//  LoginData.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 18/12/24.
//

import Foundation
import SwiftData

class LoginData {
    private let data: ApiRequest = ApiRequest()
    
    private static let namespace = "auth/"
    
    func auth(
        uData: [String: Any],
        lData: [String: Any],
        completion:@escaping (Dictionary<String, Any>?, Error?) -> ()
    ) {
 
        let reqData: [String: Any] = [
            "user": uData,
            "login": lData
        ]
        
        data.post(path: LoginData.namespace + "login", body: reqData) { tokenData, error in
            guard let tokenData = tokenData else {
                completion(nil, error)
                return
            }
            var tokens = try! JSONDecoder().decode(Dictionary<String, Dictionary<String, String>>.self, from: tokenData)
            var data: Dictionary<String, String> = tokens.removeValue(forKey: "data")!

            let idToken: String = data.removeValue(forKey: "idToken")!
            let accessToken: String = data.removeValue(forKey: "accessToken")!
            
            let idPayload = self.decodeJWTPayload(idToken)
            var userData = idPayload!["user"] as! [String: Any]
            
            if let accessPayload = self.decodeJWTPayload(accessToken) {
                userData["isNew"] = LoginData.isNewToApp(accessPayload: accessPayload)
            }
            
            userData["idToken"] = idToken
            userData["accessToken"] = accessToken
            
            DispatchQueue.main.async {
                completion(userData, nil)
            }
        }
    }
    
    func refresh(
        completion:@escaping (Dictionary<String, Any>?, Error?) -> ()
    ) {

        data.get(path: LoginData.namespace + "refresh_token") { tokenData, error in
            guard let tokenData = tokenData else {
                completion(nil, error)
                return
            }
            
            var tokens = try! JSONDecoder().decode(Dictionary<String, Dictionary<String, String>>.self, from: tokenData)
            
            var data: Dictionary<String, String> = tokens.removeValue(forKey: "data")!
            let idToken = data.removeValue(forKey: "idToken")!
            let accessToken = data.removeValue(forKey: "accessToken")!
            
            let idPayload = self.decodeJWTPayload(idToken)
            var userData = idPayload!["user"] as! [String: Any]
            
            userData["idToken"] = idToken
            userData["accessToken"] = accessToken
            
            DispatchQueue.main.async {
                completion(userData, nil)
            }
        }
    }
    
    func decodeJWTPayload(_ jwt: String) -> [String: Any]? {
        let parts = jwt.components(separatedBy: ".")
        guard parts.count == 3 else {
            print("Invalid JWT format")
            return nil
        }

        let payloadPart = parts[1]

        guard let payloadData = base64UrlDecode(payloadPart) else {
            print("Base64URL decoding failed")
            return nil
        }

        do {
            let jsonObject = try JSONSerialization.jsonObject(with: payloadData, options: [])
            return jsonObject as? [String: Any]
        } catch {
            print("JSON decoding error:", error)
            return nil
        }
    }
    
    private static func isNewToApp(accessPayload: [String: Any]) -> Bool {
        if let accesses = accessPayload["accesses"] as? [[String: String]] {
            for accessValue in accesses {
                for (key, value) in accessValue {
                    if (((key == "object_type") && (value == "U"))){
                        return false
                    }
                }
            }
        }
        return true
    }

    func base64UrlDecode(_ base64Url: String) -> Data? {
        var base64 = base64Url
            .replacingOccurrences(of: "-", with: "+")
            .replacingOccurrences(of: "_", with: "/")

        let padding = base64.count % 4
        if padding > 0 {
            base64 += String(repeating: "=", count: 4 - padding)
        }

        return Data(base64Encoded: base64)
    }

}
