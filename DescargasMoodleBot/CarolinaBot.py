import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
from os import getcwd

RUTA_BASE = getcwd()
RUTA_DRIVER = RUTA_BASE + '/conf/chromedriver.exe'
RUTA_DESCARGAS = RUTA_BASE + '\\downloads'
RUTA_CREDENCIALES = RUTA_BASE + '/conf/CREDENCIALES.json'
RUTA_CONFIGURACION = RUTA_BASE + '/conf/CURSOS.xlsx'

f = open(RUTA_CREDENCIALES)
CREDENCIALES = json.load(f)
f.close()

# LECTURA DE DATOS DE CONFIGURACIÓN DE GRUPOS
CONFIGURACION_GRUPOS = pd.read_excel(RUTA_CONFIGURACION, engine = 'openpyxl')

# CONFIGURACIÓN DEL DRIVER
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("prefs", {
  "download.default_directory": RUTA_DESCARGAS
  })
DRIVER = webdriver.Chrome(executable_path = RUTA_DRIVER, options=options)
DRIVER.implicitly_wait(0.5)
DRIVER.maximize_window()


# INICIO DE NAVEGACIÓN Y DESCARGAS
# Login
DRIVER.get('https://lms.uis.edu.co/mintic2022/my/')
usuario=DRIVER.find_element(By.ID,"username")
contrasena=DRIVER.find_element(By.ID,"password")
login = DRIVER.find_element(By.ID,"loginbtn")

usuario.send_keys(CREDENCIALES['USUARIO'])
contrasena.send_keys(CREDENCIALES['PASS'])
login.click()

# Descarga de notas
for index, row in CONFIGURACION_GRUPOS.iterrows():
    DRIVER.get('https://lms.uis.edu.co/mintic2022/report/progress/index.php?course=' + str(row['ID']))
    DRIVER.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div/div/div/div[1]/div/div[2]/div[2]/ul/li[2]/a').click()
    DRIVER.get('https://lms.uis.edu.co/mintic2022/mod/attendance/export.php?id=' + str(row['ID_ASIST']))
    DRIVER.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[5]/div[3]/div[2]/div/div/div/div/div[2]/form/div[2]/div[2]/input').click()
    
