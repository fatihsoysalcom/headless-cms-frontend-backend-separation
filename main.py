import http.server
import socketserver
import json

PORT = 8000

# --- Backend: Content Data (simulating a Headless CMS) ---
# This data would typically come from a database or a real CMS API.
# It is purely content, without any presentation logic.
CMS_CONTENT = {
    "title": "Headless CMS Mimarisi: Frontend ve Backend Ayrımını Anlamak",
    "sections": [
        {
            "heading": "Giriş",
            "body": "Geleneksel CMS'lerin sınırlamalarıyla boğuşuyor, daha esnek, ölçeklenebilir ve geleceğe dönük bir çözüm mü arıyorsunuz? İşte Headless CMS mimarisi devreye giriyor."
        },
        {
            "heading": "Neden Headless CMS?",
            "body": "Günümüzün dijital ekosistemi çok daha karmaşık. Sadece bir web sitesi değiliz; mobil uygulamalarımız, akıllı saatlerimiz ve dijital tabelalarımız var. Geleneksel CMS'ler bu çoklu kanal ihtiyacını karşılamakta yetersiz kalıyor."
        },
        {
            "heading": "Frontend ve Backend Ayrımı",
            "body": "Headless CMS, içerik yönetimini (backend) sunum katmanından (frontend) ayırır. İçerik bir API aracılığıyla sunulur ve farklı frontend uygulamaları bu API'yi kullanarak içeriği kendi ihtiyaçlarına göre işler."
        }
    ],
    "author": "Dev.to Blog Post",
    "date": "2023-10-27"
}

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/content':
            # --- Backend: API Endpoint for Content ---
            # This endpoint serves the raw content data as JSON.
            # It doesn't care how the content will be displayed.
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(CMS_CONTENT, ensure_ascii=False).encode('utf-8'))
        elif self.path == '/':
            # --- Frontend: HTML Page ---
            # This serves the HTML and JavaScript that will consume the API.
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html_content = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Headless CMS Demo</title>
    <style>
        body {{ font-family: sans-serif; margin: 2em; line-height: 1.6; color: #333; background-color: #f4f7f6; }}
        h1 {{ color: #0056b3; text-align: center; margin-bottom: 1.5em; }}
        h2 {{ color: #007bff; border-bottom: 1px solid #eee; padding-bottom: 0.3em; margin-top: 1.5em; }}
        h3 {{ color: #007bff; margin-top: 1.2em; }}
        .article-meta {{ font-size: 0.9em; color: #666; margin-bottom: 1em; text-align: right; }}
        #content-container {{ max-width: 800px; margin: 0 auto; background: #ffffff; padding: 2em; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .loading {{ color: #888; text-align: center; font-style: italic; }}
        p {{ margin-bottom: 1em; }}
    </style>
</head>
<body>
    <h1>Headless CMS Mimarisi: Frontend ve Backend Ayrımını Anlamak</h1>
    <div id="content-container">
        <p class="loading">İçerik yükleniyor...</p>
    </div>

    <script>
        // --- Frontend: Consuming Content from API ---
        document.addEventListener('DOMContentLoaded', () => {
            fetch('/api/content') // Frontend makes an API call to the backend for content
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    const container = document.getElementById('content-container');
                    container.innerHTML = ''; // Clear loading message

                    // Display article title (from CMS_CONTENT)
                    const articleTitleElem = document.createElement('h2');
                    articleTitleElem.textContent = data.title;
                    container.appendChild(articleTitleElem);

                    // Display meta info (from CMS_CONTENT)
                    const metaElem = document.createElement('div');
                    metaElem.className = 'article-meta';
                    metaElem.textContent = `Yazar: ${data.author} | Tarih: ${data.date}`;
                    container.appendChild(metaElem);

                    // Display sections (from CMS_CONTENT)
                    data.sections.forEach(section => {
                        const sectionHeading = document.createElement('h3');
                        sectionHeading.textContent = section.heading;
                        container.appendChild(sectionHeading);

                        const sectionBody = document.createElement('p');
                        sectionBody.textContent = section.body;
                        container.appendChild(sectionBody);
                    });

                    // This JavaScript code is the 'frontend' application.
                    // It is responsible only for presentation and fetching content.
                    // It does not manage content, only displays what the API provides.
                })
                .catch(error => {
                    console.error('İçerik yüklenirken bir hata oluştu:', error);
                    document.getElementById('content-container').innerHTML = '<p style="color: red; text-align: center;">İçerik yüklenemedi. Lütfen konsolu kontrol edin.</p>';
                });
        });
    </script>
</body>
</html>
            """
            self.wfile.write(html_content.encode('utf-8'))
        else:
            # For any other path, return 404
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("404 Not Found".encode('utf-8'))

# --- Server Setup ---
if __name__ == "__main__":
    Handler = MyHandler
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        print("Open your browser to http://localhost:8000 to see the frontend.")
        print("You can also access the raw API content at http://localhost:8000/api/content")
        httpd.serve_forever()
