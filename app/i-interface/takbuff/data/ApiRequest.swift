//
//  ApiRequest.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 17/01/24.
//

import Foundation
import SwiftUI

class ApiRequest {
    static let url = AppData.API_DOMAIN + "/api/"
    
    func get(path: String, completion: @escaping @Sendable (Data?, Error?) -> Void) {
        guard let url = URL(string: ApiRequest.url + path ) else {return}

        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue(AppData.API_KEY, forHTTPHeaderField: "x-api-key")
        request.setValue(AuthVar.getAccessToken(), forHTTPHeaderField: "x-access-key")

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
    
    func post(path: String, body: [String: Any], completion: @escaping @Sendable (Data?, Error?) -> Void) {
        guard let url = URL(string: ApiRequest.url + path ) else {
            return
        }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let reqbody = ["data": body ]
        let jsonEncodable = reqbody.mapValues { AnyCodable($0) }

        request.httpBody = try! JSONEncoder().encode(jsonEncodable)
        
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        request.setValue(AppData.API_KEY, forHTTPHeaderField: "x-api-key")
        request.setValue(AuthVar.getAccessToken(), forHTTPHeaderField: "x-access-key")
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
    
    func put(path: String, body: Data, completion: @escaping @Sendable (Data?, Error?) -> Void) {
        guard let url = URL(string: ApiRequest.url + path ) else {
            return
        }
        var request = URLRequest(url: url)
        request.httpMethod = "PUT"
        
        let reqbody = ["data": body ]
        let jsonEncodable = reqbody.mapValues { AnyCodable($0) }

        request.httpBody = try! JSONEncoder().encode(jsonEncodable)
        
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        request.setValue(AppData.API_KEY, forHTTPHeaderField: "x-api-key")
        request.setValue(AuthVar.getAccessToken(), forHTTPHeaderField: "x-access-key")
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
    
    private func isTokenValid() -> Bool {
        return true
    }
}

struct AnyCodable: Codable {
    let value: Any

    init(_ value: Any) {
        self.value = value
    }
    
    init(from decoder: Decoder) throws {
            let container = try decoder.singleValueContainer()
            
            if let value = try? container.decode(Bool.self) {
                self.value = value
            } else if let value = try? container.decode(Int.self) {
                self.value = value
            } else if let value = try? container.decode(Double.self) {
                self.value = value
            } else if let value = try? container.decode(String.self) {
                self.value = value
            } else if let value = try? container.decode([String: AnyCodable].self) {
                self.value = value.mapValues { $0.value }
            } else if let value = try? container.decode([AnyCodable].self) {
                self.value = value.map { $0.value }
            } else {
                throw DecodingError.dataCorruptedError(in: container, debugDescription: "Unsupported value")
            }
        }

    func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        
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
                try arrayContainer.encode(AnyCodable(item))
            }
        case let v as [String: Any]:
            let dictContainer = v.mapValues { AnyCodable($0) }
            try container.encode(dictContainer)
        default:
            throw EncodingError.invalidValue(value, EncodingError.Context(codingPath: encoder.codingPath, debugDescription: "Unsupported type"))
        }
    }
}
