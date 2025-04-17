//
//  GAuthServices.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 28/11/24.
//

import GoogleSignInSwift
import GoogleSignIn

class GAuthServices {
    
    func auth(completion:@escaping ([String: Any]?, Error?) -> ()) {
        guard let rootViewController = (UIApplication.shared.connectedScenes.first as? UIWindowScene)?.windows.first?.rootViewController else {return}
        
        GIDSignIn.sharedInstance.signIn(withPresenting: rootViewController) { signInResult, error in
            guard let signInResult = signInResult else {
                completion(nil, error)
                return
            }
            if error != nil {
                completion(nil, error)
            }
            
            let gUser = signInResult.user
            
            let emailAddress = gUser.profile?.email
            let fullName = gUser.profile?.name
            let profilePicUrl = gUser.profile?.imageURL(withDimension: 320)?.description
            
            let gUserData = [
                "name": fullName!,
                "picUrl": profilePicUrl!,
                "uId": [
                    "value": emailAddress!,
                    "type": "M",
                    "gId": gUser.userID!
                ]
            ]
            
            completion(gUserData, nil)
        }
    }
}
