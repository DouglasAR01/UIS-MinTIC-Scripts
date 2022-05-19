import pandas as pd
import glob
print ('Todos los archivos Excel (.xlsx) a unir deben de estar en el mismo directorio que este programa')
print ('y deben de tener una estructura similar. El formato de las celdas se perderá')
archivos = glob.glob('./*.xlsx')
dfs = []
for archivo in archivos:
	print ('Procesando a...', archivo)
    dfs.append(pd.read_excel(archivo, engine = 'openpyxl'))
print ('Uniendo...')
datos = pd.concat(dfs, ignore_index = True)
print ('Terminado')
input()
