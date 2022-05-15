from bs4 import BeautifulSoup

links = [] #arreglo para guardar los links 
with open("fotos.html") as fp:#se abre el archivo html
    soup = BeautifulSoup(fp, "html.parser") #le envia al contrusctor el archivo html y una salida 
    images = soup.findAll('img') #encuentre todas los tags en este caso img
    for img in images:  #recorre el arreglo y guarda todos los tags que tengan src
        print(img['src'])
        links.append(img['src'])

print(links)