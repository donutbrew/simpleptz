import argparse
import functools
import http.server
import socket
import subprocess
import threading
import webbrowser


def get_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


def launch_edge_app(url: str):
    """
    Launch Microsoft Edge in app mode and return the Popen object.
    Returns None if Edge couldn't be launched this way.
    """
    candidates = [
        "msedge",  # if on PATH
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]

    for exe in candidates:
        try:
            # --app launches a dedicated app-style window/process
            return subprocess.Popen([exe, f"--app={url}"])
        except FileNotFoundError:
            continue
        except Exception as e:
            print(f"Failed launching Edge via {exe}: {e}")
            continue

    return None


parser = argparse.ArgumentParser()
parser.add_argument("--server", action="store_true", help="Only start server.")
args = parser.parse_args()

url = f"http://{get_ip()}:8080"
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory="app")
httpd = http.server.HTTPServer(("0.0.0.0", 8080), handler)

print(f"Open SimplePTZ by pointing your browser to \033[1m{url}\033[0m")
print("Press Ctrl+C to stop.")

if args.server:
    # Server-only mode: existing behavior
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nExiting.")
    finally:
        httpd.server_close()
else:
    # App mode: run server in background, open Edge app, stop server when app exits
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    edge_proc = launch_edge_app(url)

    if edge_proc is None:
        print("Could not launch Edge app mode. Falling back to default browser.")
        webbrowser.open(url)
        print("Press Ctrl+C to stop.")
        try:
            while True:
                # Keep process alive while server runs
                server_thread.join(timeout=1)
        except KeyboardInterrupt:
            print("\nExiting.")
        finally:
            httpd.shutdown()
            httpd.server_close()
    else:
        print("Opened Edge app window. Server will stop when app window exits.")
        try:
            edge_proc.wait()
        except KeyboardInterrupt:
            print("\nInterrupted; closing.")
            try:
                edge_proc.terminate()
            except Exception:
                pass
        finally:
            httpd.shutdown()
            httpd.server_close()
            print("Edge app exited. Server stopped.")
