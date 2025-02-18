//
//  ImageView.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 26/12/23.
//

import SwiftUI

struct ImageView: View {
    @ObservedObject private var imageData: ImageData
    
    init(imageId: String, size: String) {
        imageData = ImageData(imageId: imageId, size: size)
    }
    
    var body: some View {
        Image(uiImage: imageData.image ?? UIImage())
            .resizable()
    }
}
