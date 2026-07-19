import http.server, socket, functools, webbrowser, argparse, configparser, subprocess, sys, os, threading, shutil, tempfile


def get_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_browser():
    config = configparser.ConfigParser()
    config.read(os.path.join(SCRIPT_DIR, "config.ini"))
    return config.get("app", "browser", fallback="edge").lower()


def find_executable(browser):
    candidates = {
        "edge": [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        ],
        "chrome": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ],
        "firefox": [
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
        ],
    }
    for path in candidates.get(browser, []):
        if os.path.exists(path):
            return path
    names = {"edge": "msedge", "chrome": "chrome", "firefox": "firefox"}
    return shutil.which(names.get(browser, browser))


def open_browser(url, browser, httpd):
    exe = find_executable(browser)
    if not exe:
        print(f"Browser '{browser}' not found, falling back to system default.")
        webbrowser.open(url)
        return

    userdir = tempfile.mkdtemp(prefix="simpleptz_")
    try:
        if browser in ("edge", "chrome"):
            proc = subprocess.Popen([exe, f"--user-data-dir={userdir}", f"--app={url}"])
        else:  # firefox
            proc = subprocess.Popen([exe, "--new-window", url])
    except OSError as e:
        print(f"Failed to launch '{browser}': {e}. Falling back to system default.")
        webbrowser.open(url)
        shutil.rmtree(userdir, ignore_errors=True)
        return

    def watch():
        proc.wait()
        print("\nBrowser closed. Exiting.")
        httpd.shutdown()
        shutil.rmtree(userdir, ignore_errors=True)

    threading.Thread(target=watch, daemon=True).start()


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
        open_browser(url, browser, httpd)
    else:
        print("not opening")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nExiting.")
