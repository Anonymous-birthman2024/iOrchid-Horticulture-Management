import SwiftUI
import WebKit

// 1. Create the Web View wrapper
struct EmbeddedWebView: UIViewRepresentable {
    let urlString: String

    func makeUIView(context: Context) -> WKWebView {
        let webView = WKWebView()
        webView.backgroundColor = .clear
        webView.isOpaque = false
        return webView
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {
        if let url = URL(string: urlString) {
            let request = URLRequest(url: url)
            uiView.load(request)
        }
    }
}

// 2. Display it on a blank page
struct BlankEmbedPage: View {
    var body: some View {
        ZEdgeStack {
            Color.white.ignoresSafeArea() // Keeps the background blank
            
            EmbeddedWebView(urlString: "https://localhost:5002") // placeholder for future standalone server.
                .ignoresSafeArea(edges: .bottom) // Embed fills the screen
        }
    }
}
