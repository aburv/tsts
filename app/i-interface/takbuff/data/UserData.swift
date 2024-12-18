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
    
    func auth(completion:@escaping ([String], Error?) -> ()) {
        data.get(path: UserData.namespace + "auth") { data, error in
            guard let data = data else{
                completion([], error)
                return
            }
            let posts = try! JSONDecoder().decode([String].self, from: data)
            DispatchQueue.main.async {
                completion(posts, error)
            }
        }
    }
}
