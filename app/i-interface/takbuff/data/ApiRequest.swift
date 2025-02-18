//
//  ApiRequest.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 17/01/24.
//

import Foundation
import SwiftUI

class ApiRequest{
    
    static let url = AppData.API_DOMAIN + "/api/"
    
    var accessToken: String
    
    init() {
        accessToken = ""
        if (decode(accessToken: accessToken)){
            self.get(path: "user/auth") { string, _ in
                
            }
        }
    }
    
    private func decode(accessToken: String) -> Bool {
        return true
    }
    
    func get(path: String, completion: @escaping @Sendable (Data?, Error?) -> Void) {
        guard let url = URL(string: ApiRequest.url + path ) else {return}
        
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue(AppData.API_KEY, forHTTPHeaderField: "x-api-key")
        request.setValue(accessToken, forHTTPHeaderField: "x-access-key")
        
        URLSession.shared.dataTask(with: request){ (data, response, error) in
            if (error as? URLError)?.code == .timedOut {
                DispatchQueue.main.async {
                    completion(nil, error)
                }
            }
            DispatchQueue.main.async {
                completion(data, nil)
            }
        }.resume()
    }
    
    func post(path: String, body: [String: Any], completion: @escaping @Sendable (Data?, Error?) -> Void){
        guard let url = URL(string: ApiRequest.url + path ) else {
            return
        }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let jsonEncodable = JSONEncodable(data: body.mapValues { AnyEncodable($0) })
        request.httpBody = try! JSONEncoder().encode(jsonEncodable)
        
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        request.setValue(AppData.API_KEY, forHTTPHeaderField: "x-api-key")
        request.setValue(accessToken, forHTTPHeaderField: "x-access-key")
        URLSession.shared.dataTask(with: request){ (data, response, error) in
            if (error as? URLError)?.code == .timedOut {
                DispatchQueue.main.async {
                    completion(nil, error)
                }
            }
            DispatchQueue.main.async {
                completion(data, error)
            }
        }.resume()
    }
    
    func put(path: String, body: Data, completion: @escaping @Sendable (Data?, Error?) -> Void){
        guard let url = URL(string: ApiRequest.url + path ) else {
            return
        }
        var request = URLRequest(url: url)
        request.httpMethod = "PUT"
        request.httpBody = body
        
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        request.setValue(AppData.API_KEY, forHTTPHeaderField: "x-api-key")
        request.setValue(accessToken, forHTTPHeaderField: "x-access-key")
        URLSession.shared.dataTask(with: request){ (data, response, error) in
            if (error as? URLError)?.code == .timedOut {
                DispatchQueue.main.async {
                    completion(nil, error)
                }
            }
            DispatchQueue.main.async {
                completion(data, error)
            }
        }.resume()
    }
}

struct JSONEncodable: Encodable {
    let data: [String: AnyEncodable]
}

struct AnyEncodable: Encodable {
    let value: Any

    init(_ value: Any) {
        self.value = value
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        
        // Encode based on the type of value
        switch value {
        case let v as String:
            try container.encode(v)
        case let v as Int:
            try container.encode(v)
        case let v as Double:
            try container.encode(v)
        case let v as Bool:
            try container.encode(v)
        case let v as [Any]:
            var arrayContainer = encoder.unkeyedContainer()
            for item in v {
                try arrayContainer.encode(AnyEncodable(item))
            }
        case let v as [String: Any]:
            let dictContainer = JSONEncodable(data: v.mapValues { AnyEncodable($0) })
            try container.encode(dictContainer)
        default:
            throw EncodingError.invalidValue(value, EncodingError.Context(codingPath: encoder.codingPath, debugDescription: "Unsupported type"))
        }
    }
}
