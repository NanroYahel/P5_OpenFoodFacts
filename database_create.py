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

#Constant of this program
CREATION_FILE = 'bdd_projet_5.sql'
CATEGORIES_URL = 'https://fr.openfoodfacts.org/categories.json'
FOOD_URL = 'https://world.openfoodfacts.org/language/french.json'
NB_CATEGORIES = 2000
NB_FOOD = 3000

#For now I use this code to connect to mysql but I have to change it to use an config file.
conn = MySQLdb.connect(host='localhost', user='test',passwd='123456', use_unicode=True, charset="utf8")


def get_data_from_api(url):
    """Take an url and return data"""
    data = req.get(url)
    return data.json()


def fill_categories_table(url):
    """Function to fill categories tables, with the categories data of OFF"""
    data_from_api = get_data_from_api(CATEGORIES_URL)
    i = 0
    for data in data_from_api['tags']:
        if i < NB_CATEGORIES:
            category = cl.Categories(data)
            data_for_sql = (category.id, category.name)
            cursor.execute("""INSERT INTO Categories (id, name) VALUES (%s, %s)""", data_for_sql)
            conn.commit()
            i += 1


def main():
    """Main function, lauching the script"""    

    cursor = conn.cursor()
    
    #Call the sql script to create the database
    cursor.execute("""SOURCE %s""", CREATION_FILE)

    #fill_categories_table(CATEGORIES_URL)

    print('Ok normalement c\'est bon !')


if __name__ == "__main__":
    main()