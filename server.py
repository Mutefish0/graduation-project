import bottle
from bottle import get, post, request, response, static_file, run
from processRecvData import process, process_from_img

bottle.BaseRequest.MEMFILE_MAX = 8 * 1024 * 1024

@get('/')
def index():
    return static_file('index.html', root='./public')

@get('/pic')
def pic():
    return static_file('pic.html', root='./public')

@get('/<filename>')
def static(filename):
    return static_file(filename, root='./public')

@post('/pd')
def post_data():
    response.set_header('Content-Type','application/json')
    return process(request.json)

@post('/pd_pic')
def post_data_pic():
    response.set_header('Content-Type','application/json')
    return process_from_img(request.json['data'])

run(host='0.0.0.0', port=6484, debug=False)
