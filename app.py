import http.server, socket, functools, webbrowser, argparse
 

def get_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

parser = argparse.ArgumentParser()
parser.add_argument( "--server", action="store_true", help="Only start server.")
args = parser.parse_args()
url = f"http://{get_ip()}:8080"

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory="app")
with http.server.HTTPServer(("0.0.0.0", 8080), handler) as httpd:
    
    print(f"Open SimplePTZ by pointing your browser to \033[1m{url}\033[0m")
    print("Press Ctrl+C to stop.")
    if not args.server:
        print("opening window")
        webbrowser.open(url)
    else:
        print("not opening")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nExiting.")
        

