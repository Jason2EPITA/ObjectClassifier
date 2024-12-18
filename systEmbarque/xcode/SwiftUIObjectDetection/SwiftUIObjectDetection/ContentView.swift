import SwiftUI

struct ContentView: View {
    @StateObject private var cameraManager = CameraManager()
    @State private var isCameraActive = false

    var body: some View {
        ZStack {
            CameraView(cameraManager: cameraManager)
                .edgesIgnoringSafeArea(.all)

            ForEach(cameraManager.boundingBoxes) { box in
                Rectangle()
                    .stroke(Color.green, lineWidth: 3)
                    .frame(width: box.rect.width, height: box.rect.height)
                    .position(x: box.rect.midX, y: box.rect.midY)
                
                Text(box.label)
                    .foregroundColor(.white)
                    .background(Color.black.opacity(0.7))
                    .cornerRadius(5)
                    .position(x: box.rect.midX, y: box.rect.minY - 10)
            }
            
            VStack {
                Spacer()
                Button(action: {
                    isCameraActive.toggle()
                    if isCameraActive {
                        cameraManager.startSession()
                    } else {
                        cameraManager.stopSession()
                    }
                }) {
                    Text(isCameraActive ? "Arrêter la caméra" : "Activer la caméra")
                        .font(.title2)
                        .foregroundColor(.white)
                        .padding()
                        .background(isCameraActive ? Color.red : Color.green)
                        .cornerRadius(10)
                }
                .padding()
            }
        }
    }
}

#Preview {
    ContentView()
}
