import http.server, socket, functools

def get_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory="app")
with http.server.HTTPServer(("0.0.0.0", 8080), handler) as httpd:
    print(f"Open SimplePTZ by pointing your browser to \033[1mhttp://{get_ip()}:8080\033[0m")
    print("Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nExiting.")