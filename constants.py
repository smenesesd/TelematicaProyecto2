# Constants....

PORT = 9090
ENCONDING_FORMAT = "utf-8"
RECV_BUFFER_SIZE = 518144
IP_SERVER = '127.0.0.1'
HELO = 'HELO'
DATA = 'DATA'
QUIT = 'QUIT'
GET = 'GET'
PUT = 'PUT'
HEAD = 'HEAD'
DELETE = 'DELETE'

OK200 = "HTTP/1.1 200 OK\n"
Okdelete = "\n<html><body><h3>Contenido eliminado con exito</h3></body></html>"
Error400 = 'HTTP/1.1 400 Bad Request\nContent-Type: text/html\n\n<html><body>Error 400: Bad Request</body></html>'
Error404 = 'HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n<html><body>Error 404: File not found</body></html>'
OK201 = 'HTTP/1.1 201 Created\n\nContent-Location: '
Error409 = 'HTTP/1.1 409 Conflict\nContent-Type: text/html\n\n<html><body>Error 409: Conflit</body></html>'