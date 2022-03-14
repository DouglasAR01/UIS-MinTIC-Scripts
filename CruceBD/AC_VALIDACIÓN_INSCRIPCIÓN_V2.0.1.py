#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
# import glob Para futuras versiones


# # FASE DE LECTURA DE DATOS

# In[2]:


est_inscritos = pd.read_csv('./INPUT/INS_UIS/inscripcion.csv', sep=';', encoding='latin-1')
est_form = pd.read_excel('./INPUT/FORMULARIO/formulario.xlsx', engine='openpyxl')


# In[3]:


est_inscritos['TELEFONO MINTIC'] = est_inscritos['TELEFONO MINTIC'].str.replace(r'[^0-9]+', '')
est_inscritos['TELEFONO MINTIC'] = pd.to_numeric(est_inscritos['TELEFONO MINTIC'], errors='coerce')
est_inscritos['TELEFONO MINTIC'] = est_inscritos['TELEFONO MINTIC'].values.astype(np.int64)
est_inscritos.drop(axis = 1, labels='Unnamed: 9', inplace = True)

# # FASE DE ELIMINACIÓN DE DUPLICADOS

# In[6]:


# ELIMINACIÓN DE DUPLICADOS POR DOCUMENTO DE INDENTIDAD Y CORREO, PERMANECE EL MÁS RECIENTE
est_form.drop_duplicates(subset=['Número de Documento', 'Correo electrónico personal que usa'], keep='last', inplace = True)
est_inscritos.drop_duplicates(subset=['DOCUMENTO', 'EMAIL INSCRIPCION'], keep='last', inplace = True)

# # FASE DE CRUCES

# ![INFORMACI%C3%93N_JOINS.jpeg](attachment:INFORMACI%C3%93N_JOINS.jpeg)

# In[9]:


def buscarEnDataframe(df, col1, col2, v1, v2):
    il = df.index[(df[col1] == v1) & (df[col2] == v2)].tolist()
    if len(il) != 1:
        return -1
    return il[0]


# In[10]:


est_validados = pd.merge(est_inscritos,est_form,how='inner',left_on=['DOCUMENTO','EMAIL INSCRIPCION'],right_on=['Número de Documento', 'Correo electrónico personal que usa'])


# In[11]:


# LEFT OUTER JOIN a estudiantes solo del conjunto de inscripción y
# RIGHT OUTER JOIN a estudiantes solo del conjunto de formulario de caracterización
est_solo_inscripcion = est_inscritos.copy()
est_solo_formulario = est_form.copy()
for index, row in est_validados.iterrows():
    documento = row['DOCUMENTO']
    email = row['EMAIL INSCRIPCION']
    i = buscarEnDataframe(est_inscritos, 'DOCUMENTO', 'EMAIL INSCRIPCION', documento, email)
    if i != -1:
        est_solo_inscripcion.drop(labels=i, inplace = True)
    i = buscarEnDataframe(est_form, 'Número de Documento', 'Correo electrónico personal que usa', documento, email)
    if i != -1:
        est_solo_formulario.drop(labels=i, inplace = True)


# # RE-INPUT
# Para el reinput se usan los output de la tubería anterior, se quitan los repetidos que **COINCIDAN** en **CÉDULA** y **CELULAR**.
# La probabilidad que una persona se equivoque en ambos campos y justo coincida con otra es extremadamente baja como para tenerlo en cuenta.

# In[12]:


est_solo_formulario.drop_duplicates(subset=['Número de Documento', 'Teléfono Celular que usa'], keep='last', inplace = True)
est_solo_inscripcion.drop_duplicates(subset=['DOCUMENTO', 'TELEFONO MINTIC'], keep='last', inplace = True)


# In[13]:


# ESTE JOIN BUSCA POR CÉDULA
est_nuevos_validados = pd.merge(est_solo_inscripcion,est_solo_formulario,how='inner',left_on=['DOCUMENTO'],right_on=['Número de Documento'])
est_validados = pd.concat([est_validados, est_nuevos_validados])
est_validados.drop_duplicates(subset=['DOCUMENTO'], keep = 'last', inplace = True)





# LEFT OUTER JOIN a estudiantes solo del conjunto de inscripción y
# RIGHT OUTER JOIN a estudiantes solo del conjunto de formulario de caracterización
for index, row in est_validados.iterrows():
    documento = row['DOCUMENTO']
    il = est_solo_inscripcion.index[est_solo_inscripcion['DOCUMENTO'] == documento].tolist()
    il2 = est_solo_formulario.index[est_solo_formulario['Número de Documento'] == documento].tolist()
    if len(il) == 1:
        est_solo_inscripcion.drop(labels=il, inplace = True)
    if len(il2) == 1:
        est_solo_formulario.drop(labels=il2, inplace = True)




# # GUARDADO DE DATOS

# In[18]:


est_validados.to_excel('./OUTPUT/VALIDADOS.xlsx', index = False)
est_solo_inscripcion.to_excel('./OUTPUT/SOLO_INSCRIPCION_UIS.xlsx', index = False)
est_solo_formulario.to_excel('./OUTPUT/SOLO_FORMULARIO.xlsx', index = False)

