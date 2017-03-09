from bottle import get, post, request, response, static_file, run
from processRecvData import process

@get('/')
def index():
    return static_file('index.html', root='./public')

@get('/<filename>')
def static(filename):
    return static_file(filename, root='./public')

@post('/pd')
def postData():
    response.set_header('Content-Type','application/json')
    return process(request.json)

run(host='localhost', port=6484, debug=True)
