#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main script of the P5 programm"""

#import standard module
# from random import randrange as rd

#import pip module
import MySQLdb

#import personnal module
import class_bdd as cl
import config as cfg

#Connect to the bdd
DB = MySQLdb.connect(host=cfg.mysql['host'], user=cfg.mysql['user'], \
    passwd=cfg.mysql['passwd'], use_unicode=True, charset='utf8')
CURSOR = DB.cursor()


def select_categories(dict_categories):
    """Show 10 categories"""
    #Ask the user for enter a category
    user_search = ""
    while user_search == "":
        user_search = input('Please enter a category you want to find : ')
        if user_search == "":
            print("You didn't write anything...")
        else:
            format_user_search = "%" +user_search+ "%"
    #SQL request for categories
    CURSOR.execute('USE openfoodfacts;')
    CURSOR.execute("""SELECT id, name \
        FROM Categories \
        WHERE name LIKE %s
        LIMIT 10""", (format_user_search,))
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
    CURSOR.execute("""SELECT id, name, category_id_1, category_id_2, category_id_3, stores, url \
        FROM Food \
        WHERE category_id_1 LIKE %s OR category_id_2 LIKE %s OR category_id_3 LIKE %s
        LIMIT 10""", (category, category, category))
    products = CURSOR.fetchall()
    return products

def add_favorite(product, substitute):
    """Add the chosen product and his substitute to the TABLE User in the database"""
    print('\n Do you want to save this match as favorite ?')
    print('1. Yes')
    print('2. No')
    choice = try_user_input(2)
    if choice == 1:
        CURSOR.execute('USE openfoodfacts;')
        CURSOR.execute("""INSERT INTO Favorites (product_id, substitute_id) \
            VALUES (%s,%s)""", (product.id, substitute.id))
        DB.commit()
        print('Favorite saved')
    elif choice == 2:
        print('Ok, this is not saved')

def search_substitute(product):
    """Seach a correct substitute of the product in the database"""
    CURSOR.execute('USE openfoodfacts;')
    # #Catch the id of the category of the product
    product_categories_name = (product.category_1, product.category_2, product.category_3)
    CURSOR.execute(""" SELECT id FROM Categories WHERE name IN %s""", (product_categories_name,))
    id_category = CURSOR.fetchall()
    #Make a string with the category, used in the query
    search = (id_category[0][0], id_category[1][0], id_category[2][0])
    #Query
    product_name = product.name
    CURSOR.execute("""SELECT Food.id, Food.name, C1.name as category_1, C2.name as category_2, \
        C3.name as category_3, stores, url \
    FROM Food \
    INNER JOIN Categories C1 ON C1.id = Food.category_id_1 \
    INNER JOIN Categories C2 ON C2.id = Food.category_id_2 \
    INNER JOIN Categories C3 ON C3.id = Food.category_id_3 \
    WHERE (C1.id IN %s OR C2.id IN %s OR C3.id IN %s) \
    AND Food.name NOT LIKE %s""", (search, search, search, product_name))
    substitute = CURSOR.fetchone()
    try:
        return cl.Food(substitute)
    except TypeError:
        pass

def display_products_list(products):
    """Use the result of the products selection function and display it"""
    print('\n Select a product : ')
    dict_product = {}
    index = 1
    for i in products:
        products_display = cl.Food(i, index)
        dict_product[products_display.index] = products_display.name
        print(index, " : ", products_display.name)
        index += 1
    return dict_product

def try_user_input(number_of_choice):
    """Test the entry of the use"""
    test_input = True
    while test_input is True:
        input_user = input('Make your choice : ')
        try:
            int(input_user)
            if int(input_user) <= 0 or int(input_user) > number_of_choice:
                print('Please select a number in the list.')
            else:
                test_input = False
                return int(input_user)
        except ValueError:
            print('This is not a valid answer, you need to choose a number...')


def find_substitute():
    """Part of the programme where the user chose a product in a list
    and return a substitute for this product"""
    #Create and dict with the Categories instances
    dict_categories = {}
    dict_product = {}
    #Display a list of 10 categories in which the user has to chose one
    while len(dict_product) == 0:
        while dict_categories == {}:
            select_categories(dict_categories)
            if dict_categories == {}:
                print('Sorry, there is no category for this search...')
                print('Try another.')
        choice = try_user_input(len(dict_categories))
        #Display a list of 10 (maximum) products contained in the chosen category
        #Use has to chose one product
        dict_product = display_products_list(select_products(dict_categories[choice][1]))
        if len(dict_product) == 0:
            print('\n There is no product for this category... \n')
            dict_categories = {}
    #Search product until one product is ok with the chosen category
    choice = try_user_input(len(dict_product))
    print(dict_product[choice])
    product_chosen = extract_product(dict_product[choice])
    #Display the description of the chosen product
    print('\n You chosed this product : \n')
    print_product(product_chosen)

    #Search a substitute and display it
    substitute = search_substitute(product_chosen)
    print('\n You can substitute this product by : \n')
    print_product(substitute)
    add_favorite(product_chosen, substitute)

def display_favorites():
    """Display all the favorites of the user"""
    #List of favorites used for the function "select_favorite"
    favorites_dict = {}
    # for products in Count(requete nb product in the database)
    CURSOR.execute('USE openfoodfacts;')
    # CURSOR.execute('SELECT COUNT(*) FROM Favorites;')
    # nb_favorites = CURSOR.fetchone()
    CURSOR.execute("""SELECT F1.name as Product, F2.name as Substitute \
        FROM Favorites \
        INNER JOIN Food F1 ON Favorites.product_id = F1.id
        INNER JOIN Food F2 ON Favorites.substitute_id = F2.id""")
    favorites = CURSOR.fetchall()
    index = 1
    for i in favorites:
        favorite_tuple = (i[0], i[1])
        print("\n {}. {}, can be substitute by {}.".format(index, \
            favorite_tuple[0], favorite_tuple[1]))
        favorites_dict[index] = favorite_tuple
    print('Select a number for more details.')
    select_favorite(favorites_dict)

def select_favorite(favorites_dict):
    """Display the information of the product and the substitute"""
    choice = try_user_input(len(favorites_dict))
    product = extract_product(favorites_dict[choice][0])
    substitute = extract_product(favorites_dict[choice][1])
    print_product(product)
    print('\n You can substitute this product by : \n')
    print_product(substitute)


def extract_product(product):
    """Take the name of a product and return an object
    containing the specifications of this product"""
    CURSOR.execute("USE openfoodfacts;")
    CURSOR.execute("""SELECT Food.id, Food.name, C1.name as Category_1, C2.name as Category_2, \
        C3.name as Category_3, stores, url
        FROM Food
        INNER JOIN Categories C1 ON C1.id = Food.category_id_1 
        INNER JOIN Categories C2 ON C2.id = Food.category_id_2
        INNER JOIN Categories C3 ON C3.id = Food.category_id_3
        WHERE Food.name LIKE %s;""", (product,))
    product = CURSOR.fetchone()
    product_class = cl.Food(product)
    return product_class


def print_product(product):
    """Take a product (object) and print his specifications"""
    print('\n \
Name : {}, \n \
Categories : {}, {}, {} \n \
Store : {} \n \
URL : {}'.format(product.name, product.category_1, product.category_2, \
    product.category_3, product.stores, product.url))

def main():
    """Main function of the program"""
    print('Welcome to OpenFoodFind !')
    running = True
    while running is True:
        print('\n''-------------MAIN MENU-------------')
        print('1. Find a substitute.')
        print('2. Show favorites.')
        print('3. Exit.')
        choice = try_user_input(3)
        if choice == 1:
            find_substitute()
        elif choice == 2:
            display_favorites()
        elif choice == 3:
            running = False

if __name__ == "__main__":
    main()
