#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import time

from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver


def get_pages(count=132, headless=False):
    """Récupère un nombre spécifié de pages de recherche sur le site internet Superimmo.com 
       sur des logements situés à Paris intramuros 

    Arguments : 
        count (int, optionnel): Nombre de résultats à chercher. 132 par défaut. 
        headless (bool, optionnel): Est-ce qu'on cache le moteur de recherche. False par défaut.'

    Returns:
        list: pages HTML encodées en utf-8 
    """

    pages = []

    driver = webdriver.Firefox() 

    for page_nb in range(1, count + 1):

        page_url = f"https://www.superimmo.com/location/ile-de-france/paris/paris/p/{page_nb}.html"   
        driver.get(page_url)
        if page_nb == 1:
            time.sleep(15)
        else:
            time.sleep(10)
        pages.append(driver.page_source.encode("utf-8"))
    return pages

def save_pages(pages):
    """Sauvegarde les pages HTML dans le fichier "data_final" 
    Args:
        pages (list): liste des pages 
    """
    os.makedirs("data_final", 
                exist_ok=True #si le dossier existe déjà, pas d'erreur créée 
                ) #Crée un objet data 
    for page_nb, page in enumerate(pages):
        with open(f"data_final/page_{page_nb}.html", "wb") as f_out: #on ouvre en écriture binaire 
            f_out.write(page)

def parse_pages():
    """ Analyse toutes les pages du fichier 'data_final' 
    Returns:
        pd.DataFrame: un Dataframe avec les différentes infos pertinentes pour l'analyse
        en fonction des différentes classes des pages HTML. En l'occurrence on a le titre, 
        le prix, et pour la localisation il n'y avait pas de classe, on a donc dû trouver à 
        la main en analysant tout le texte des pages HTML.
    """
    results = pd.DataFrame()
    
    for i in range(0,132) : 
        results = results.append(parse_page(i))
    return(results)

def convert(lst):
    """Convertit une liste en liste de mots""" 
    return (lst[0].split())


def parse_page(i):
    """
    Args:
        page (bytes): page html encodée en utf-8 
    Returns:
        pd.DataFrame: données analysées 
    """
    
    with open(f"data_final/page_{i}.html", "rb") as f_in: #on ouvre en écriture binaire 
        html = f_in.read().decode("utf-8")
        
    soup = BeautifulSoup(html, "html.parser") #On enregistre dans la variable soup le contenu de la page
  
    
    result = pd.DataFrame()
   

    result["loyer (€)"] = [tag.text for tag in soup.find_all(attrs={"class": "js-newtab"}) ] #le .text permet d'obtenir seulement le texte dans l'élément html
    #On crée la première colonne du DataFrame avec tous les éléments de la page html qui ont la classe "js-newtab", dans laquelle on trouve le loyer
   
    result["titre"] = [tag.text for tag in soup.find_all(attrs={"class": "titre"}) ]
    #On fait la même chose avec la classe "titre" qui contient plusieurs éléments à la fois comme la surface, le nombre de pièces, si c'est un appartement ou une maison...  
    
    ''''Pour le code postal c'est plus compliqué car les pages html n'ont pas de classe spécifique pour le code postal. Ils apparaissent derrière <b> 
    que l'on retrouve pour beaucoup d'autres éléments de la page. C'est pourquoi nous avons cherché le code postal de manière plus classique 
    comme si on analysait n'importe quel texte, en particulier ici le texte contenu dans la page html auquel on a accès avec soup.text'''
    
    txt = soup.text
    with open(f'yourfile{i}.txt', 'w') as f:
        f.write(txt)
   
    arr = ['(75001)','(75002)','(75003)','(75004)','(75005)','(75006)','(75007)','(75008)',
              '(75009)','(75010)','(75011)','(75012)','(75013)','(75014)','(75015)','(75016)',
              '(75017)', '(75018)','(75019)','(75020)', '(75116)']
    
    with open(f'yourfile{i}.txt', 'w') as f:
        f.write(txt)
    
    liste = []
    with open(f"yourfile{i}.txt", "r+") as f: 
        for line in f:
            #print(line)
            list = convert([line])
            for j in list:
                if j in arr : 
                    if len(list) < 6 :
                        liste.append(re.sub("[()]","", j)) #on enlève les parenthèses autour des codes postaux
   
    result["Code postal"] = liste
    return(result)
 

"""Ici on fait une série de fonctions qui permettent d'extraire des informations plus précises 
qui sont en puissance dans les trois colonnes du DataFrame : titre, loyer et code postal"""   
    
def clean_loyer(colonne) : 
    loyers = []
    chiffres = ['0','1','2','3','4','5','6','7','8','9']
    for i in colonne : 
        res = []
        for j in list(i.replace(" ", "")) : 
            #print(j)
            if j in chiffres :  
                #print(j)
                res.append(int(j))    
            if j == '€' : 
                break 
        if len(res) == 5 : 
            loyer = res[0]*10000 + res[1]*1000 + res[2]*100 + res[3]*10 + res[4] 
        if len(res) == 4 : 
            loyer = res[0]*1000 + res[1]*100 + res[2]*10 + res[3]         
        if len(res) == 3 : 
            loyer = res[0]*100 + res[1]*10 + res[2]
        if len(res) == 2 : 
            loyer = res[0]*10 + res[1]
        loyers.append(loyer)
    return(loyers)
    
    
def clean_surface(colonne) : 
    chiffres = ['0','1','2','3','4','5','6','7','8','9']
    surfaces = []
    for i in colonne : 
        b = ""
        a = i.find('m²')
        for j in list(i)[:a] : 
            if j in chiffres : 
                b = str(b + j)
            elif j == ',' : 
                b = str(b + ".")
        surfaces.append(b)
    return(surfaces)
  
def clean_style(colonne) : 
    type = []
    for i in colonne : 
        type.append(i.split()[0])
    return(type)

def arrondissement(colonne) : 
    arr = []
    for i in colonne : 
        if i == '75116' : 
            arr.append(16)
        else : 
            arr.append(i%1000)
    return(arr)

def clean_meuble(colonne) : 
    meublé = []
    for i in colonne : 
        a = i.find('Meublé') 
        if a == -1 : 
           meublé.append("Non meublé")
        else : 
            meublé.append("Meublé")
    return(meublé)


def clean_df(df) : 
    '''On utilise trois fonctions différentes sur la même colonne titre car elle 
    est de la forme : Appartement • 32 m² • 2 pièces
    argument : 
        pd.DataFrame
    returns : 
        pd.DataFrame '''
    
    df['Arrrondissement'] = arrondissement(df['Code postal'])
    df['Loyer (€)'] = clean_loyer(df['loyer (€)'])  
    df['Surface (m²)'] = clean_surface(df['titre'])
    df['Appartement ou maison'] = clean_style(df['titre'])
    df['Meublé ou non'] = clean_meuble(df['titre'])
    df = df.drop(["loyer (€)", "titre"], axis=1)
    
    return(df)


def main() :
    pages = get_pages()
    save_pages(pages)
    results = parse_pages()
    results.to_csv(r'loyers.csv', index=False)
    df = clean_df(pd.read_csv('loyers.csv'))   
    df.to_csv(r'loyers.csv', index=False)
    

if __name__ == "__main__":
    main()
 

