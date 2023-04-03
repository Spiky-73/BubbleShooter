# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 08:57:34 2023

@author: friboulet
"""
import csv

with open('init_jeu_f.csv','r',encoding='utf-8') as fich:
    # Mise en place d'un lecteur CSV
    csvReader = csv.reader(fich, delimiter=',')

    a = []

    i = 0
    for row in csvReader:
        a.append(row)
        print(row)    