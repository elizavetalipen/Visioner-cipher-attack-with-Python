# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 18:20:01 2021

@author: User
"""
import pandas as pd
import matplotlib.pyplot as plt


def hist_plot(data:dict):
    values = data.values()
    symbols = data.keys()
    # построение гистограммы
    plt.bar(symbols, values, color = 'green')
    plt.title("Частотный анализ")
    plt.ylabel("Частоты, %")
    
def table_data(data_dict:dict, filename='output.xlsx'):
    ''' Занесение данных в таблицу и сохранение в файл эксель'''
    
    table = pd.DataFrame.from_dict(data_dict, 
    orient='index').rename(columns={0:'Frequency,%'})
    
    writer = pd.ExcelWriter(filename) 
    table.to_excel(writer)
    writer.save() 
    print('DataFrame is written successfully to Excel File.')
