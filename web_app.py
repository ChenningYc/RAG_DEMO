from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from rag_demo import generate_answer, load_knowledge_base, retrieve


HOST = "127.0.0.1"
PORT = 8000
STATIC_DIR = Path("static")


class RAGWebHandler(BaseHTTPRequestHandler):
    chunks = load_knowledge_base()

    def do_GET(self) -> None:
        parsed_path = urlparse(self.path)
        request_path = parsed_path.path

        if request_path == "/":
            self.send_static_file(STATIC_DIR / "index.html", "text/html")
            return

        if request_path.startswith("/static/"):
            relative_path = request_path.removeprefix("/static/")
            file_path = STATIC_DIR / relative_path
            self.send_static_file(file_path, self.get_content_type(file_path))
            return

        self.send_error(404, "Page not found")

    def do_POST(self) -> None:
        if self.path != "/api/ask":
            self.send_error(404, "API endpoint not found")
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length)

        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            self.send_json({"error": "Invalid JSON body"}, status=400)
            return

        question = str(payload.get("question", "")).strip()

        if not question:
            self.send_json({"error": "Question is required"}, status=400)
            return

        retrieved_chunks = retrieve(question, self.chunks)
        answer = generate_answer(question, retrieved_chunks)
        sources = [
            {
                "source": chunk.source,
                "score": round(score, 2),
                "text": chunk.text,
            }
            for score, chunk in retrieved_chunks
        ]

        self.send_json(
            {
                "question": question,
                "answer": answer,
                "sources": sources,
                "chunk_count": len(self.chunks),
            }
        )

    def send_static_file(self, file_path: Path, content_type: str) -> None:
        if not file_path.exists() or not file_path.is_file():
            self.send_error(404, "File not found")
            return

        content = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def send_json(self, data: dict, status: int = 200) -> None:
        content = json.dumps(data, ensure_ascii=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    @staticmethod
    def get_content_type(file_path: Path) -> str:
        suffix = file_path.suffix.lower()
        if suffix == ".css":
            return "text/css"
        if suffix == ".js":
            return "application/javascript"
        if suffix == ".html":
            return "text/html"
        return "text/plain"

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), RAGWebHandler)
    print(f"RAG web demo running at http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop the server.")
    server.serve_forever()


if __name__ == "__main__":
    main()
