//
//  userData.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 17/01/24.
//

import Foundation


class UserData {
    private let data: ApiRequest = ApiRequest()
    
    private static let namespace = "user/"
    
    func getAppData(completion:@escaping (Dictionary<String, String>, Error?) -> ()) {
        data.get(path: UserData.namespace + "app") { data, error in
            guard let data = data else {
                completion([:], error)
                return
            }
            
            var userData = try! JSONDecoder().decode(Dictionary<String, Dictionary<String, String>>.self, from: data)
            let dd = userData.removeValue(forKey: "data")!
            completion(dd, nil)
        }
    }
    
    func setOnBoardingDone(completion:@escaping (String?, Error?) -> ()) {
        data.post(path: UserData.namespace + "done_onboarding", body: [:]) { data, error in
            guard let data = data else {
                completion(nil, error)
                return
            }
            
            var userData = try! JSONDecoder().decode(Dictionary<String, String>.self, from: data)
            let dd = userData.removeValue(forKey: "data")!
            completion(dd, nil)
        }
    }
}
