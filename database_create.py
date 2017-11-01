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
            if 'en:' in category.id:
                #Do not take the categories with 'fr' or 'en' in the name
                if 'en:' in category.name or 'fr:' in category.name:
                    pass
                else:
                    cursor.execute("INSERT INTO Categories (id, name)"\
                        "VALUES (%s, %s)", (category.id, category.name))
                    db.commit()
            else:
                pass
        #Don't take the non utf-8 data
        except db.OperationalError:
            pass

def fill_food_table(url):
    """Function to fill food tables, with the food data of OFF"""
    data_from_api = get_data_from_api(url)
    for data in data_from_api['products']:
        try:
            food = cl.Food(data)
            food_properties = (food.name, food.category_1, food.category_2, \
             food.category_3, food.stores)
            cursor.execute("INSERT INTO Food "\
                "(name, category_id_1, category_id_2, category_id_3, stores)"\
                "VALUES (%s, %s, %s, %s, %s)", food_properties)
            db.commit()
        except KeyError: #Don't take lignes without 'product_name'
            pass
        except AttributeError: #Don't take products with 0 categories
            pass
        except db.OperationalError: #Don't take the products with encoding error
            pass
        except db.IntegrityError: #Don't take the products with an category unknow in the database
            pass
        except db.DataError: #Pass when product name is too long
            pass

def main():
    """Main function, lauching the script"""
    #Call the sql script to create the database
    file_sql = open(CREATION_FILE, 'r')
    query = " ".join(file_sql.readlines())
    cursor.execute(query)

    try:
        cursor.execute('USE openfoodfacts;')
    except:
        print('On saut l\'étape on verra si ça change quelque chose')
    fill_categories_table(CATEGORIES_URL)
    for i in range(1, 10000): #Take 10000 pages of french data
        url_food = FOOD_URL+str(i)+'.json'
        fill_food_table(url_food)
    print('Ok normalement c\'est bon !')


if __name__ == "__main__":
    main()
