import http.server
import socketserver
import subprocess
import signal
import sys

result = subprocess.call(["pipenv", "run", "coverage", "html"])
if result:
    print("There was an error generating the HTML coverage report. Exiting.")
    exit()


def stop_coverage(sig, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, stop_coverage)

# the approach below is from: https://2ality.com/2014/06/simple-http-server.html
PORT = 8001
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving coverage details at http://localhost:{PORT}/htmlcov/")
    print("(Use Ctrl-C to stop the server)")
    httpd.serve_forever()
