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
import config as cfg

#Constant of this script
CREATION_FILE = 'bdd_projet_5.sql'
CATEGORIES_URL = 'https://fr.openfoodfacts.org/categories.json'
FOOD_URL = 'https://world.openfoodfacts.org/country/france/'

#For now I use this code to connect to mysql but I have to change it to use an config file.
DB = MySQLdb.connect(host=cfg.mysql['host'], user=cfg.mysql['user'], \
    passwd=cfg.mysql['passwd'], use_unicode=True, charset='utf8')
CURSOR = DB.cursor()

def get_data_from_api(url):
    """Take an url and return data"""
    data = req.get(url)
    return data.json()


def fill_categories_table(url):
    """Function to fill categories tables, with the categories data of OFF"""
    data_from_api = get_data_from_api(url)

    for data in data_from_api['tags']:
        # if i < NB_CATEGORIES:
        if data['products'] > 300 and 'en:' in data['id']: #Don't take the categories with to few products and
            try:
                category = cl.Categories(data)
                if 'en:' in category.name or 'fr:' in category.name:
                    pass
                else:
                    CURSOR.execute("INSERT INTO Categories (id, name)"\
                        "VALUES (%s, %s)", (category.id, category.name))
                    DB.commit()
            #Don't take the non utf-8 data
            except DB.OperationalError:
                pass

def fill_food_table(url):
    """Function to fill food tables, with the food data of OFF"""
    data_from_api = get_data_from_api(url)
    for data in data_from_api['products']:
        try:
            food = cl.Food(data)
            food_properties = (food.name, food.category_1, food.category_2, \
             food.category_3, food.stores, food.url)
            CURSOR.execute("INSERT INTO Food "\
                "(name, category_id_1, category_id_2, category_id_3, stores, url)"\
                "VALUES (%s, %s, %s, %s, %s, %s)", food_properties)
            DB.commit()
        except KeyError: #Don't take lignes without 'product_name'
            pass
        except AttributeError: #Don't take products with 0 categories
            pass
        except DB.OperationalError: #Don't take the products with encoding error
            pass
        except DB.IntegrityError: #Don't take the products with an category unknow in the database
            pass
        except DB.DataError: #Pass when product name is too long
            pass

def main():
    """Main function, lauching the script"""
    #Call the sql script to create the database
    file_sql = open(CREATION_FILE, 'r')
    query = " ".join(file_sql.readlines())
    CURSOR.execute(query)

    try:
        CURSOR.execute('USE openfoodfacts;')
    except:
        print('On saut l\'étape on verra si ça change quelque chose')

    fill_categories_table(CATEGORIES_URL)
    for i in range(1, 7200): #7200 is approximatively the number of pages in french
        url_food = FOOD_URL+str(i)+'.json'
        fill_food_table(url_food)
    print("Database 'openfoodfacts' successfully created !")


if __name__ == "__main__":
    main()
