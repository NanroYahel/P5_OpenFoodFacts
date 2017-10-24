#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file is used to create the database,
 and fill it with the openfoodfacts API"""

#import standard module
import json

#import pip module
import MySQLdb
import requests as req

#import personnal module
import class_bdd as cl

#Constant of this script
CREATION_FILE = 'bdd_projet_5.sql'
CATEGORIES_URL = 'https://fr.openfoodfacts.org/categories.json'
FOOD_URL = 'https://world.openfoodfacts.org/country/france/'
NB_FOOD = 3000

#For now I use this code to connect to mysql but I have to change it to use an config file.
db = MySQLdb.connect(host='localhost', user='test', 
    passwd='123456', use_unicode=True, charset='utf8')
cursor = db.cursor()

def get_data_from_api(url):
    """Take an url and return data"""
    data = req.get(url)
    return data.json()


def fill_categories_table(url):
    """Function to fill categories tables, with the categories data of OFF"""
    data_from_api = get_data_from_api(url)

    for data in data_from_api['tags']:
        # if i < NB_CATEGORIES:
        try:
            category = cl.Categories(data)
            #Only take the french and english categories
            if 'fr:' in category.id or 'en:' in category.id:
                #Do not take the categories with 'fr' or 'en' in the name
                if 'en:' in category.name or 'fr:' in category.name:
                    pass
                else:
                    cursor.execute("INSERT INTO Categories (id, name)"
                        "VALUES (%s, %s)", (category.id, category.name))
                    db.commit()
            else:
                pass
        #Not take the non utf-8 data
        except db.OperationalError:
            pass

def fill_food_table(url):
    """Function to fill food tables, with the food data of OFF"""
    data_from_api = get_data_from_api(url)
    i = 0
    for data in data_from_api['products']:
        if i < NB_FOOD:
            try:
                food = cl.Food(data)
                food_properties = (food.name, food.categories_id, food.stores)
                cursor.execute("INSERT INTO Food "
                    "(name, categories_id, stores)"
                    "VALUES (%s, %r, %s)", food_properties)
                db.commit()
            #We don't take uncompleted lignes
            except KeyError:
                pass
            except db.OperationalError:
                pass
        i += 1

def main():
    """Main function, lauching the script"")"""
    #Call the sql script to create the database
    file_sql = open(CREATION_FILE, 'r')
    query = " ".join(file_sql.readlines())
    cursor.execute(query)

    try:
        cursor.execute('USE openfoodfacts;')
    except:
        print('On saut l\'étape on verra si ça change quelque chose')
    fill_categories_table(CATEGORIES_URL)
    for i in range(1, 10000):
        url_food = FOOD_URL+str(i)+'.json'
        fill_food_table(url_food)
    print('Ok normalement c\'est bon !')


if __name__ == "__main__":
    main()
