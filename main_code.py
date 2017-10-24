#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main script of the P5 programm"""

#import standard module
from random import randrange as rd

#import pip module
import MySQLdb

#import personnal module
import class_bdd as cl


#Connect to the bdd
DB = MySQLdb.connect(host='localhost', user='test', \
    passwd='123456', use_unicode=True, charset='utf8')
CURSOR = DB.cursor()


def display_categories():
    """Show 10 categories"""
    #Create and dict with the Categories instances
    dict_categories = {}
    #Take a random limit for the SQL request
    limit = rd(0, 1000)
    #SQL request for categories
    CURSOR.execute('USE openfoodfacts;')
    CURSOR.execute("""SELECT id, name \
        FROM Categories \
        LIMIT 10 OFFSET %s""", (limit,))
    categories = CURSOR.fetchall()
    #Fill dict_categories with the result of the request
    index = 1
    for i in categories:
        categories_display = cl.Categories(i, index)
        dict_categories[categories_display.index] = categories_display.name
        print(index, " : ", categories_display.name)
        index += 1
    return dict_categories

def display_products(category):
    """Select 10 products in the database \
    containing the category chosed by the user"""
    dict_product = {}
    category = '%' + category + '%'
    CURSOR.execute('USE openfoodfacts;')
    CURSOR.execute("""SELECT name, categories_id, stores \
        FROM Food \
        WHERE categories_id LIKE (%s)""", (category,))
    products = CURSOR.fetchall()
    print(products)
    # index = 1
    # for i in products:
    #     products_display = cl.Food(i, index)
    #     dict_product[products_display.index] = products_display.name
    #     print(index, " : ", products_display.name)
    #     index += 1
    # return dict_product


def try_user_input():
    """Test the entry of the use"""
    test_input = True
    while test_input is True:
        input_user = input('Choose a category : ')
        try:
            int(input_user)
            test_input = False
            return int(input_user)
        except ValueError:
            print('This is not a valid answer, you need to choose a number...')

def main():
    """Main function of the program"""
    dict_categories = display_categories()
    choice = try_user_input()
    print(dict_categories[choice], type(dict_categories[choice]))
    # dict_product = display_products(dict_categories[choice])
    # choice = try_user_input()
    # print(dict_product[choice])

if __name__ == "__main__":
    main()
