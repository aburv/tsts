//
//  Data.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 26/09/24.
//

import Foundation

class AppData {
    static let API_DOMAIN = ProcessInfo.processInfo.environment["API_DOMAIN"] ?? ""
    static let API_KEY = ProcessInfo.processInfo.environment["API_KEY"] ?? ""
    static let SEPARATOR = ProcessInfo.processInfo.environment["SEPARATOR"] ?? ""
}
