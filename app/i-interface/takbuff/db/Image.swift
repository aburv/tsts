//
//  Image.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 26/09/24.
//

import SwiftUI

class ImageCache {
    private var imageCache: NSCache<NSString, UIImage>?
    
    func set(image: UIImage, key: String) {
        imageCache?.setObject(image, forKey: key as NSString)
    }
    
    func get(from key: String) -> UIImage? {
        return imageCache?.object(forKey: key as NSString) as? UIImage
    }
}
