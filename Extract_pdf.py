# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 09:37:22 2017

@author: Felipe
"""
"""

"""

import PyPDF2
import glob

path = '~/Beneficiarios/*.pdf'   
files = glob.glob(path)
todo = []
for file in files:
    ruta = file.replace('\\','/')
    with open(ruta, 'rb') as f:
       cte = PyPDF2.PdfFileReader(f)
       if cte.isEncrypted:
           cte.decrypt('')
       pdf = []
       for i in range(0,cte.getNumPages()):
           pdf.append(cte.getPage(i).extractText())
       todo.append(pdf)    

import re

valores=[]
for i in range(0,len(todo)):
    f29=[]
    f22=[]
    for j in range(0,len(todo[i])):
        if len(re.findall('formulario 29',todo[i][j],re.I))>0:
            if len(re.findall('(?<=base imponible)(?:[A-Za-z\s]*)([\d\.]*)(?:\d{3})',todo[i][j],re.I)) >0:
                f29.append(int(re.findall('(?<=base imponible)(?:[A-Za-z\s]*)([\d\.]*)(?:\d{3})',todo[i][j],re.I)[0].replace(".","")))
            else:
                f29.append(0)
        else:
            f29.append(0)
        if len(re.findall('^Rut',todo[i][j],re.I))>0:
            if len(re.findall('(?<=baseimponible)(?:[A-Za-z\s\(\)]*)(\d*)(?:\d{2})',todo[i][j],re.I)) >0:
                f22.append(int(re.findall('(?<=baseimponible)(?:[A-Za-z\s\(\)]*)(\d*)(?:\d{2})',todo[i][j],re.I)[0]))
            else:
                f22.append(int(re.findall('(?:Ingresos del Giro Percibidos oDevengados)(\d*)(?:\d{3})', todo[i][j],re.I)[0]))
        elif len(re.findall('FORM. 22',todo[i][j],re.I))>0:
            if len(re.findall('(?<=base imponible)(?:[A-Za-z\s]*)(\d*)(?:\d{3})',todo[i][j],re.I)) > 0:
                f22.append(int(re.findall('(?<=base imponible)(?:[A-Za-z\s]*)(\d*)(?:\d{3})',todo[i][j],re.I)[0]))
            elif len(re.findall('(?:Ingresos del Giro Percibidos o Devengados )(\d*)(?:\d{3})', todo[i][j],re.I))>0:
                f22.append(int(re.findall('(?:Ingresos del Giro Percibidos o Devengados )(\d*)(?:\d{3})', todo[i][j],re.I)[0]))
            else:
                f22.append(0)
    if len(re.findall('(?=emisor:).*(?=RUT del emisor:)',todo[i][0]))>0:
        valores.append([re.findall('(?=emisor:).*(?=RUT del emisor:)',todo[i][0])[0], sum(f29),len(f29),f29,sum(f29[len(f29)-12:]), f22])
    elif len(re.findall('(?<=MAterno05Nombres)(?:\d*)(?:-\w)([\w\s]*)(?:06)',todo[i][0],re.I))>0:
        valores.append([re.findall('(?<=MAterno05Nombres)(?:\d*)(?:-\w)([\w\s]*)(?:06)',todo[i][0], re.I),sum(f29),len(f29),f29,sum(f29[len(f29)-12:]),f22])
    else:
        valores.append([i,sum(f29),len(f29),f29,sum(f29[len(f29)-12:]),f22])

       
import pandas as pd

tabla = pd.DataFrame(valores)
tabla.to_csv("cte.csv")
