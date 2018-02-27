#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import argparse
import random

parser = argparse.ArgumentParser(description='Server that returns a random sentence.')
parser.add_argument('port', metavar='p', nargs='?', const=1, type=int, default=8080, help='A valid port number')
args = parser.parse_args()

print("ARGS", args.port)

SENTENCES = None

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
	self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(getRandomSentence())
        #self.wfile.write("<html><body><h1>hi!</h1></body></html>")

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")

def readSentenceFile():
    with open('harvard_sentence.txt', 'r') as f:
	content = f.readlines()
	global SENTENCES  
	SENTENCES = [x.strip() for x in content]  
	print(len(SENTENCES))
        
def getRandomSentence():
    global SENTENCES
    return SENTENCES[random.randint(0, len(SENTENCES)-1)]

def run(server_class=HTTPServer, handler_class=S, port=args.port):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    readSentenceFile()
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
