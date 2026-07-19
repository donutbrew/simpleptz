import http.server, socket, functools, webbrowser, argparse, configparser


def get_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


def get_browser():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config.get("app", "browser", fallback="edge").lower()


def open_browser(url, browser):
    try:
        if browser == "chrome":
            b = webbrowser.get("chrome")
        elif browser == "firefox":
            b = webbrowser.get("firefox")
        else:
            webbrowser.open(url)
            return
        b.open(url)
    except webbrowser.Error:
        print(f"Browser '{browser}' not found, falling back to system default.")
        webbrowser.open(url)


parser = argparse.ArgumentParser()
parser.add_argument("--server", action="store_true", help="Only start server.")
args = parser.parse_args()
url = f"http://{get_ip()}:8080"

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory="app")
with http.server.HTTPServer(("0.0.0.0", 8080), handler) as httpd:

    print(f"Open SimplePTZ by pointing your browser to \033[1m{url}\033[0m")
    print("Press Ctrl+C to stop.")
    if not args.server:
        browser = get_browser()
        print(f"opening window in {browser}")
        open_browser(url, browser)
    else:
        print("not opening")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nExiting.")
        

