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


def select_categories():
    """Show 10 categories"""
    #Create and dict with the Categories instances
    dict_categories = {}
    #Take a random limit for the SQL request
    limit = rd(0, 2000)
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
        dict_categories[categories_display.index] = (categories_display.name, categories_display.id)
        print(index, " : ", categories_display.name)
        index += 1
    return dict_categories

def select_products(category):
    """Select 10 products in the database \
    containing the category chosed by the user"""
    category = '%' + category + '%'
    CURSOR.execute('USE openfoodfacts;')
    CURSOR.execute("""SELECT name, category_id_1, category_id_2, category_id_3 \
        FROM Food \
        WHERE category_id_1 LIKE %s OR category_id_2 LIKE %s OR category_id_3 LIKE %s
        LIMIT 10""", (category, category, category))
    products = CURSOR.fetchall()
    return products


def add_favorite(product, substitute):
    """Add the chosen product and his substitute to the TABLE User in the database"""
    CURSOR.execute('USE openfoodfacts;')
    CURSOR.execute("""INSERT INTO User (product_id, substitute_id) \
        VALUES (%s,%s)""", (product.id, substitute.id))
    DB.commit()
    print('Favorite saved')

def display_favorite():
    """Display all the favorites of the user"""
    # for products in Count(requete nb product in the database)
    CURSOR.execute('USE openfoodfacts;')
    CURSOR.execute("""SELECT product_id \
        FROM User \
        INNER JOIN Food ON User.product_id = Food.name""")
    favorites = CURSOR.fetchall()
    return favorites

def display_substitute(favorite):
    """Show the substitute associated to the favorite"""
    CURSOR.execute('USE openfoodfacts;')
    CURSOR.execute("""SELECT product_id, substitute_id
        FROM User \
        INNER JOIN Food ON User.product_id = Food.name
        INNER JOIN Food ON User.substitute_id = Food.name
        WHERE User.product_id = %s""", favorite.name)
    substitute = CURSOR.fetchall()
    substitute_display = cl.Food(substitute)
    return substitute_display

def try_user_input():
    """Test the entry of the use"""
    test_input = True
    while test_input is True:
        input_user = input('Make your choice : ')
        try:
            int(input_user)
            test_input = False
            return int(input_user)
        except ValueError:
            print('This is not a valid answer, you need to choose a number...')


def search_substitute(product):
    """Seach a correct substitute of the product in the database"""
    CURSOR.execute('USE openfoodfacts;')
    #Catch the id of the first category of the product
    CURSOR.execute(""" SELECT id FROM Categories WHERE name = %s""", (product.category_1,))
    id_category = CURSOR.fetchone()
    #Make a string with the category, used in the query
    search = '%' + id_category[0] + '%'
    product_name = product.name
    CURSOR.execute("""SELECT name, category_id_1, category_id_2, category_id_3 \
    FROM Food \
    WHERE category_id_1 LIKE %s OR category_id_2 LIKE %s OR category_id_3 LIKE %s \
    AND name NOT LIKE %s""", (search, search, search, product_name))

    substitute = CURSOR.fetchone()
    return cl.Food(substitute)

def display_products(products):
    """Use the result of the products selection function and display it"""
    dict_product = {}
    index = 1
    for i in products:
        products_display = cl.Food(i, index)
        dict_product[products_display.index] = products_display.name
        print(index, " : ", products_display.name)
        index += 1
    return dict_product

def main():
    """Main function of the program"""
    dict_categories = select_categories()
    choice = try_user_input()

    dict_product = display_products(select_products(dict_categories[choice][1]))
    choice = try_user_input()
    print(dict_product[choice])
    # #Show all the datas of the choisen product
    CURSOR.execute("USE openfoodfacts;")
    CURSOR.execute("""SELECT Food.name, C1.name as Category_1, C2.name as Category_2, C3.name as Category_3, Stores
        FROM Food
        INNER JOIN Categories C1 ON C1.id = Food.category_id_1 
        INNER JOIN Categories C2 ON C2.id = Food.category_id_2
        INNER JOIN Categories C3 ON C3.id = Food.category_id_3
        WHERE Food.name LIKE %s
        LIMIT 10;""", (dict_product[choice],))
    product = CURSOR.fetchone()
    product_class = cl.Food(product)
    print('\n \
Name : {}, \n \
Categories : {}, {}, {} \n \
Store : {}'.format(product_class.name, product_class.category_1, product_class.category_2, product_class.category_3, product_class.stores))
    try:
        substitute = search_substitute(product_class)
        print(substitute.name)
    except:
        print('Sorry, there is no substitute...')
        exit()
    choice = input('Do you want to add this match to favorites ? (y/n)')
    add_favorite(product_class, substitute)


if __name__ == "__main__":
    main()
