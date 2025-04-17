//
//  User.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 15/08/24.
//

import Foundation

class User{
    var id: String;
    var name: String;
    var dp: String;
    var email: String;
    
    init(id: String, name: String, dp: String, email: String) {
        self.id = id
        self.name = name
        self.dp = dp
        self.email = email
    }
}
