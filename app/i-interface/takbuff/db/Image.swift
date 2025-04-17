//
//  Image.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 26/09/24.
//

import UIKit


class ImageCache: NSCache<NSString, UIImage> {
    static let shared = ImageCache()

    private static var keySet = Set<NSString>()

    override func setObject(_ obj: UIImage, forKey key: NSString) {
        super.setObject(obj, forKey: key)
        Self.keySet.insert(key)
    }

    override func removeObject(forKey key: NSString) {
        super.removeObject(forKey: key)
        Self.keySet.remove(key)
    }

    override func removeAllObjects() {
        super.removeAllObjects()
        Self.keySet.removeAll()
    }
}

class ImageStore {
    
    func set(image: UIImage, key: String) {
        ImageCache.shared.setObject(image as UIImage, forKey: key as NSString)
    }
    
    func get(from key: String) -> UIImage? {
        return ImageCache.shared.object(forKey: key as NSString) as UIImage?
    }
}
