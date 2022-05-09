import os, sys
p = os.path.abspath('D:\TelematicaProyecto2')       #Para poder importar la clase  constatns
sys.path.insert(1, p)
import constants
import re
from pathlib import Path
BASE_DIR = Path(__file__).parent.absolute()         #Tomamos el directorio base para obtener los recursos