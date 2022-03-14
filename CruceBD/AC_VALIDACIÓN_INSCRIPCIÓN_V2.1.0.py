#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import glob


# # VARIABLES Y CONFIGURACIÓN

# In[2]:


# COLUMNAS IMPORTANTES
COLUMNA_DOCUMENTO_A = 'DOCUMENTO'
COLUMNA_DOCUMENTO_B = 'Número de Documento'
COLUMNA_EMAIL_A = 'EMAIL INSCRIPCION'
COLUMNA_EMAIL_B = 'Correo electrónico personal que usa'
COLUMNA_TELEFONO_A = 'TELEFONO MINTIC'
COLUMNA_TELEFONO_B = 'Teléfono Celular que usa'

# CONFIGURACIÓN
VALOR_MANTENER_DUPLICADO = 'last' # Puede ser "last", "first" o False. Last es para que deje el más reciente.


# # FASE DE LECTURA DE DATOS

# In[3]:


archivos = glob.glob('./INPUT/FORMULARIO/*.xlsx')
dfs = []
print ("Cargando archivos de FORMULARIO ENCUESTA de caracterización...")
for archivo in archivos:
    dfs.append(pd.read_excel(archivo, engine = 'openpyxl'))
est_form = pd.concat(dfs, ignore_index = True)


# In[4]:


print ("Cargando archivos de módulo de inscripción...")
est_inscritos = pd.read_csv('./INPUT/INS_UIS/inscripcion.csv', sep=';', encoding='latin-1')


# In[5]:


est_inscritos[COLUMNA_TELEFONO_A] = est_inscritos[COLUMNA_TELEFONO_A].str.replace(r'[^0-9]+', '')
est_inscritos[COLUMNA_TELEFONO_A] = pd.to_numeric(est_inscritos[COLUMNA_TELEFONO_A], errors='coerce')
est_inscritos[COLUMNA_TELEFONO_A] = est_inscritos[COLUMNA_TELEFONO_A].values.astype(np.int64)
if 'Unnamed: 9' in est_inscritos:
    est_inscritos.drop(axis = 1, labels='Unnamed: 9', inplace = True)



# # FASE DE ELIMINACIÓN DE DUPLICADOS

# In[8]:


# ELIMINACIÓN DE DUPLICADOS POR DOCUMENTO DE INDENTIDAD Y CORREO, PERMANECE EL MÁS RECIENTE
est_form.drop_duplicates(subset=[COLUMNA_DOCUMENTO_B, COLUMNA_EMAIL_B], keep=VALOR_MANTENER_DUPLICADO, inplace = True)
est_inscritos.drop_duplicates(subset=[COLUMNA_DOCUMENTO_A, COLUMNA_EMAIL_A], keep=VALOR_MANTENER_DUPLICADO, inplace = True)



# # FASE DE CRUCES

# ![INFORMACI%C3%93N_JOINS.jpeg](attachment:INFORMACI%C3%93N_JOINS.jpeg)

# In[11]:


def buscarEnDataframe(df, col1, col2, v1, v2):
    il = df.index[(df[col1] == v1) & (df[col2] == v2)].tolist()
    if len(il) != 1:
        return -1
    return il[0]


# In[12]:


print ("Procesando cruces...")
est_validados = pd.merge(est_inscritos,est_form,how='inner',left_on=[COLUMNA_DOCUMENTO_A, COLUMNA_EMAIL_A],right_on=[COLUMNA_DOCUMENTO_B, COLUMNA_EMAIL_B])


# In[13]:


# LEFT OUTER JOIN a estudiantes solo del conjunto de inscripción y
# RIGHT OUTER JOIN a estudiantes solo del conjunto de formulario de caracterización
est_solo_inscripcion = est_inscritos.copy()
est_solo_formulario = est_form.copy()
for index, row in est_validados.iterrows():
    documento = row[COLUMNA_DOCUMENTO_A]
    email = row[COLUMNA_EMAIL_A]
    i = buscarEnDataframe(est_inscritos, COLUMNA_DOCUMENTO_A, COLUMNA_EMAIL_A, documento, email)
    if i != -1:
        est_solo_inscripcion.drop(labels=i, inplace = True)
    i = buscarEnDataframe(est_form, COLUMNA_DOCUMENTO_B, COLUMNA_EMAIL_B, documento, email)
    if i != -1:
        est_solo_formulario.drop(labels=i, inplace = True)


# # RE-INPUT
# Para el reinput se usan los output de la tubería anterior, se quitan los repetidos que **COINCIDAN** en **CÉDULA** y **CELULAR**.
# La probabilidad que una persona se equivoque en ambos campos y justo coincida con otra es extremadamente baja como para tenerlo en cuenta.

# In[14]:


est_solo_formulario.drop_duplicates(subset=[COLUMNA_DOCUMENTO_B, COLUMNA_TELEFONO_B], keep=VALOR_MANTENER_DUPLICADO, inplace = True)
est_solo_inscripcion.drop_duplicates(subset=[COLUMNA_DOCUMENTO_A, COLUMNA_TELEFONO_A], keep=VALOR_MANTENER_DUPLICADO, inplace = True)


# In[15]:


# ESTE JOIN BUSCA POR CÉDULA
est_nuevos_validados = pd.merge(est_solo_inscripcion,est_solo_formulario,how='inner',left_on=[COLUMNA_DOCUMENTO_A],right_on=[COLUMNA_DOCUMENTO_B])
est_validados = pd.concat([est_validados, est_nuevos_validados])
est_validados.drop_duplicates(subset=[COLUMNA_DOCUMENTO_A], keep = VALOR_MANTENER_DUPLICADO, inplace = True)

# In[17]:


# LEFT OUTER JOIN a estudiantes solo del conjunto de inscripción y
# RIGHT OUTER JOIN a estudiantes solo del conjunto de formulario de caracterización
for index, row in est_validados.iterrows():
    documento = row[COLUMNA_DOCUMENTO_A]
    il = est_solo_inscripcion.index[est_solo_inscripcion[COLUMNA_DOCUMENTO_A] == documento].tolist()
    il2 = est_solo_formulario.index[est_solo_formulario[COLUMNA_DOCUMENTO_B] == documento].tolist()
    if len(il) == 1:
        est_solo_inscripcion.drop(labels=il, inplace = True)
    if len(il2) == 1:
        est_solo_formulario.drop(labels=il2, inplace = True)

# # GUARDADO DE DATOS

# In[20]:


print ("Guardando resultados...")
est_validados.to_excel('./OUTPUT/VALIDADOS.xlsx', index = False)
est_solo_inscripcion.to_excel('./OUTPUT/SOLO_INSCRIPCION_UIS.xlsx', index = False)
est_solo_formulario.to_excel('./OUTPUT/SOLO_FORMULARIO.xlsx', index = False)
print ("Finalizado")
input("Presione una tecla para cerrar.")
