//
//  DeviceLocationService.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 27/12/24.
//

import Foundation
import Combine
import CoreLocation

final class DeviceLocationService: NSObject, ObservableObject {
    static let shared = DeviceLocationService()
    
    let locationPublisher = PassthroughSubject<CLLocationCoordinate2D, Error>()
    let deniedLocationPublisher = PassthroughSubject<Void, Never>()
    

    private lazy var locationManager: CLLocationManager = {
        let manager = CLLocationManager()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyBest
        manager.distanceFilter = 10 // meters
        return manager
    }()
    
    private override init() {
        super.init()
    }
    
    func requestLocationUpdates() {
        switch locationManager.authorizationStatus {
        case .notDetermined:
            locationManager.requestWhenInUseAuthorization()
            
        case .authorizedWhenInUse, .authorizedAlways:
            locationManager.startUpdatingLocation()
            
        case .restricted, .denied:
            deniedLocationPublisher.send()
            
        @unknown default:
            deniedLocationPublisher.send()
        }
    }
}

extension DeviceLocationService: CLLocationManagerDelegate {
    
    func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        switch manager.authorizationStatus {
        case .authorizedWhenInUse, .authorizedAlways:
            manager.startUpdatingLocation()
        case .restricted, .denied:
            manager.stopUpdatingLocation()
            deniedLocationPublisher.send()
        default:
            break
        }
    }
    
    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        print("Location update failed with error: \(error.localizedDescription)")
        locationPublisher.send(completion: .failure(error))
    }
    
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard let location = locations.last else { return }
        print("DeviceLocationService: Got new location – \(location.coordinate)")
        locationPublisher.send(location.coordinate)
        manager.stopUpdatingLocation() // Optional: one-shot update
    }

}

final class LocationViewModel: ObservableObject {
    
    @Published var locationCoordinates: (latitude: Double, longitude: Double)?
    @Published var locationAccessDenied: Bool = false

    private var cancellables = Set<AnyCancellable>()
    private let deviceLocationService = DeviceLocationService.shared

    init() {
        print("ViewModel initialized")
        observeDeviceLocation()
        observeLocationAccessDenied()
        deviceLocationService.requestLocationUpdates()
    }

    private func observeDeviceLocation() {
        print("Setting up location observer")
        deviceLocationService.locationPublisher
            .receive(on: DispatchQueue.main)
            .sink { completion in
                if case .failure(let error) = completion {
                    print("ViewModel: Failed to get location – \(error.localizedDescription)")
                }
            } receiveValue: { coordinates in
                print("ViewModel: Received coordinates – \(coordinates)")
                self.locationCoordinates = (coordinates.latitude, coordinates.longitude)
            }
            .store(in: &cancellables)
    }

    private func observeLocationAccessDenied() {
        deviceLocationService.deniedLocationPublisher
            .receive(on: DispatchQueue.main)
            .sink {
                print("ViewModel: Location access denied.")
                self.locationAccessDenied = true
            }
            .store(in: &cancellables)
    }
}
