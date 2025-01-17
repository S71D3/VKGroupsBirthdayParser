# -*- coding: utf-8 -*-
"""
Created on Mon May 11 19:15:52 2020

@author: S11De
"""

import pandas as pd #работаем с датафреймами
import os #для пути загрузки сета
import matplotlib.pyplot as plt #работа с визуализацией графиками
from numpy import datetime64 as datetime #работа с ячейками с датой

CSVNAME = 'walmart.csv' #название исходника с датасетом
PERCENTDELETION = 0.6 #сколько процентов пропуска допустимо для переменной

def DownloadDS():
    df = pd.read_csv(os.getcwd()+'/'+CSVNAME) #загрузка по пути запуска исходника
    return df #загружаем дс в датафрейм

def PreWork(df):
    print('Общая информация:')
    print ('Первые 5 записей:\n' + str(df.head()) + '\n') #первые 5, можно было как и последние 5 через илокейт
    print ('Последние 5 записей:\n' + str(df.iloc[len(df)-5:len(df)]) + '\n') #последние 5
    print ('Кол-во наблюдений:\n' + str(len(df))) #кол-во наблюдений
    
    print('Названия и типы переменных:\n')
    print(df.dtypes) #выводим название и тип
    print('\n')
    
def DateToDate(df):
    print('Изменяем тип переменной даты:')
    df['Date'] = pd.to_datetime(df['Date']) #меняем тип через apply с помощью лямбда-функции
    #print('Получившийся тип первой ячейки - ' + str(type(df['Date'][0]))) #смотрим тип первого
    #print('Получившийся тип последней ячейки - ' + str(type(df['Date'][len(df)-1]))) #и тип последнего элемента в столбце даты
    print('Получившийся тип столбца - ' + str(df.Date.dtypes))
    print('\n')
    return df #получаем датафрейм со столбцом даты, имеющий тип datatime.date
    
def MissingFields(df):
    print('Информация о пустых полях:')
    
    for column in df: #цикл по столбцам вроде можно
        emptyFCount = df[column].isnull().sum()
        print('У переменной ' + column + ' ' + str(emptyFCount) + ' пустых полей') #выводим информацию о пропусках
        if (emptyFCount/len(df) > PERCENTDELETION): #если кол-во пустых строк больше PERCENTDELETION процентов, то удаляем столбец
            del df[column]
    
    print('\n')
    return df

def Sampling(df):
    print('Информация о выборке:')
    
    print('Магазинов в датасете ' + str(df.Store.value_counts().size)) #кол-во магазинов
    print('Отделов в датасете ' + str(df.Dept.value_counts().size)) #кол-во отделов
    print('Охватывается промежуток в ' + str((df.Date.max()-df.Date.min()).days) + ' дней') #разница между максимальной и минимальной датами

    print('\n')


def Dynamics(df):
    df = df[['Date', 'Weekly_Sales']] #убираем ненужные столбцы
    df = df.groupby('Date', as_index=False).aggregate(sum) #группируем строки по дате, т.к. выручка по отдельности не важна
    df.plot(x='Date', y='Weekly_Sales')
    
def Corr(df):
    plt.matshow(df.corr()) #выводим матрицу корреляции
    plt.show()
    
def TopSupp(df, mainfield, topcount):
    dfSel = df[[mainfield, "Weekly_Sales"]] #убираем ненужные столбцы
    dfSel = dfSel.groupby(mainfield, as_index=False).aggregate(sum) #группируем строки элементов типа mainfield
    dfSel.sort_values(by=['Weekly_Sales'], inplace=True, ignore_index=True) #сортируем по убыванию
    df = df.loc[df[mainfield].isin(dfSel[mainfield].head(topcount))] #оставляем в чистовом ДФ только topcount самых прибыльных элементов типа mainfield

    l = [] #список для хранения отдельных экземпляров датафреймов для каждого элемента типа mainfield
    for i in range(topcount):
        l.append(df[df[mainfield] == dfSel[mainfield][i]]) #отбираем только подходящие элементы базового датафрейма
        l[i] = l[i][['Date', "Weekly_Sales"]] #убираем все ненужные строки в каждом отдельном датафрейме
        l[i] = l[i].groupby('Date', as_index=False).aggregate(sum) #группируем строки элементам типа mainfield
        l[i] = [l[i], dfSel[mainfield][i]] #добавляем каждому датафрейму название для вывода легенды
        
    for frame in l:
        plt.plot(frame[0]['Date'], frame[0]['Weekly_Sales'], label = frame[1]) #добавляем график каждого дочернего датафрейма в визуализацию
    plt.legend() #виз легенды
    plt.show() #виз картинки
    
def Top5(df):
    TopSupp(df, 'Store', 5)

def Top10(df):
    df = df[df.Type == 'A']
    df = df[['Weekly_Sales', 'Date', 'Dept']]
    df = df[df.Date >= datetime('2011')]
    df = df[df.Date < datetime('2012')] #отсеяли ненужные отделы
    
    TopSupp(df, 'Dept', 10)

    
def main():
    df = DownloadDS() #Загружаем датасет в датафрейм
    PreWork(df) #Первые\последние 5 наблюдений, сколько наблюдений, какой формат переменных
    df = DateToDate(df) #привести Date к формату даты
    df = MissingFields(df) #удаляем переменные, имеющие более 60% пропущенных полей
    Sampling(df) #работа с выборкой. сколько магазинов и отделов, за какой период времени
    Dynamics(df) #динамика продаж, график - по оси Х - дата, по оси Y - продажи всей сети
    Corr(df) #матрица корреляции числовых показателей
    Top5(df) #топ5 самых больших магазинов по сумм. за все время + динамика продаж на одном графике
    Top10(df) #топ10 самых больших ОТДЕЛОВ по сумм. за 2011(!) год среди магазинов типа А (!) + столбчатая диаграмма для них

main()