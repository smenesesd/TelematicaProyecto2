import os
import constants
import re
from pathlib import Path
BASE_DIR = Path(__file__).parent.absolute()         #Tomamos el directorio base para obtener los recursos
import put

def delete_object(header):
    nombre = str(header[1])
    nombre = nombre[1:]
    direccion = put.get_direction(nombre)
    try:
        os.remove(direccion)
        header = constants.OK200+constants.Okdelete
    except:
        header = constants.Error400
    final_response = header.encode(constants.ENCONDING_FORMAT)
    return final_response


