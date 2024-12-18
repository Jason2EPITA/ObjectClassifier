import AVFoundation
import UIKit
import Vision

struct BoundingBox: Identifiable {
    let id = UUID()
    let rect: CGRect
    let label: String
}

class CameraManager: NSObject, ObservableObject, AVCaptureVideoDataOutputSampleBufferDelegate {
    private let session = AVCaptureSession()
    @Published var boundingBoxes: [BoundingBox] = []
    @Published var detectedObject: String = "En attente..."
    
    var previewLayer: AVCaptureVideoPreviewLayer?
    private var visionModel: VNCoreMLModel?

    override init() {
        super.init()
        setupCamera()
        loadVisionModel()
    }

    // Méthodes pour démarrer et arrêter la session
    func startSession() {
        if !session.isRunning {
            session.startRunning()
        }
    }

    func stopSession() {
        if session.isRunning {
            session.stopRunning()
        }
    }

    // Configuration de la caméra
    private func setupCamera() {
        session.sessionPreset = .photo
        guard let captureDevice = AVCaptureDevice.default(for: .video),
              let input = try? AVCaptureDeviceInput(device: captureDevice) else { return }
        
        if session.canAddInput(input) { session.addInput(input) }
        
        let output = AVCaptureVideoDataOutput()
        output.setSampleBufferDelegate(self, queue: DispatchQueue(label: "videoQueue"))
        
        if session.canAddOutput(output) { session.addOutput(output) }
        
        previewLayer = AVCaptureVideoPreviewLayer(session: session)
        previewLayer?.videoGravity = .resizeAspectFill
    }

    // Chargement du modèle Vision Core ML
    private func loadVisionModel() {
        guard let model = try? myfirstmodel(configuration: MLModelConfiguration()) else { return }
        visionModel = try? VNCoreMLModel(for: model.model)
    }

    // Gestion des prédictions et extraction des boîtes englobantes
    func captureOutput(_ output: AVCaptureOutput, didOutput sampleBuffer: CMSampleBuffer, from connection: AVCaptureConnection) {
        guard let pixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer), let visionModel = visionModel else { return }
        
        let request = VNCoreMLRequest(model: visionModel) { [weak self] (finishedReq, error) in
            guard let results = finishedReq.results as? [VNRecognizedObjectObservation] else { return }
            
            DispatchQueue.main.async {
                // Mise à jour des boîtes englobantes
                self?.boundingBoxes = results.map { observation in
                    let boundingBox = observation.boundingBox
                    let rect = self?.convertBoundingBox(boundingBox: boundingBox) ?? .zero
                    let label = observation.labels.first?.identifier ?? "Unknown"
                    return BoundingBox(rect: rect, label: label)
                }
                
                // Mise à jour du texte "detectedObject"
                self?.detectedObject = results.first?.labels.first?.identifier ?? "Inconnu"
            }
        }
        
        try? VNImageRequestHandler(cvPixelBuffer: pixelBuffer, options: [:]).perform([request])
    }
    
    // Convertit les coordonnées normalisées de Core ML en coordonnées pour l'écran
    private func convertBoundingBox(boundingBox: CGRect) -> CGRect {
        guard let previewLayer = previewLayer else { return .zero }
        let previewRect = previewLayer.frame
        let x = boundingBox.minX * previewRect.width
        let y = (1 - boundingBox.maxY) * previewRect.height
        let width = boundingBox.width * previewRect.width
        let height = boundingBox.height * previewRect.height
        return CGRect(x: x, y: y, width: width, height: height)
    }
}
