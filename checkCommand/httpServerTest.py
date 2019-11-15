import urllib
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

data = {'result': 'this is a test'}


class Resquest(BaseHTTPRequestHandler):

    def do_GET(self):
        if '?' in self.path:  # 如果带有参数
            self.queryString = urllib.parse.unquote(self.path.split('?', 1)[1])
            # name=str(bytes(params['name'][0],'GBK'),'utf-8')
            params = urllib.parse.parse_qs(self.queryString)
            print(params)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_POST(self):
        s = str(self.rfile.readline(), 'UTF-8')  # 先解码
        print(urllib.parse.parse_qs(urllib.parse.unquote(s)))  # 解释参数
        self.send_response(301)  # URL跳转
        self.send_header("Location", "/?" + s)
        self.end_headers()

def strat(hostNumber=8888):
    host=('0.0.0.0',hostNumber)
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()

if __name__ == '__main__':
    hostNumber = 22222
    strat(hostNumber=hostNumber)
