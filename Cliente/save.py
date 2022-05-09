encabezado = encabezado.split()
#[HTTP/1.1, 200, OK, Content-type:, image/png]

contido = [pedazo1, pedazo2]
cotenido_unido=b""
if len(contido)>1:
    for i in range(len(contido)):
        cotenido_unido += contido[i]+b'\n\n'
else:
    cotenido_unido = contido[0]
