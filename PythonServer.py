from http.server import HTTPServer
from HubRequstHandler import HubRequestHandler
from PythonHub import PythonHub

class PythonServer:
    __defhost = 'localhost'
    __defport =  8080

    def __init__(self, host=__defhost, port=__defport):
        self.host = host
        self.port = port
        self.webServer = HTTPServer((self.host, self.port), HubRequestHandler)
        self.webServer.gateway = PythonHub()
    
    def run(self):
        print(f'My web server started at http://{self.host}:{self.port}')
        self.webServer.serve_forever()

    
        