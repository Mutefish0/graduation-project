import bottle
from bottle import get, post, request, response, static_file, run
from processRecvData import process

bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024

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

run(host='0.0.0.0', port=6484, debug=False)
