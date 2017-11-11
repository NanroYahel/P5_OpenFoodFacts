#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This file contain classes representing the data base of this programm"""


class Categories():
    """Class representing the 'Categories' table of the database"""

    def __init__(self, data_from_off, index=None):
        """Init taking a dictionnary for argument"""
        #Use key when creating the database from OFF API
        try:
            self.id = data_from_off['id']
            self.name = data_from_off['name']
        #Use index when call the class from the programme
        except TypeError:
            self.id = data_from_off[0]
            self.name = data_from_off[1]
            self.index = index

class Food():
    """Class representing the 'Food' table of the database"""
    
    def __init__(self, data_from_off, index=None):    
        """Init taking a dictionnary for argument"""

        #Use key when creating the database from OFF API
        try:
            #No id attribute because of the auto-increment
            self.name = data_from_off['product_name']
            #Take the first 3 categories of the product
            try:
                self.category_1 = data_from_off['categories_tags'][0]
            except IndexError:
                pass
            try:
                self.category_2 = data_from_off['categories_tags'][1]
            except IndexError:
                self.category_2 = "None"
            try:
                self.category_3 = data_from_off['categories_tags'][2]
            except IndexError:
                self.category_3 = "None"
            try:
                self.category_4 = data_from_off['categories_tags'][3]
            except IndexError:
                self.category_4 = "None"
            try:
                self.category_5 = data_from_off['categories_tags'][4]
            except IndexError:
                self.category_5 = "None"
            try:
                self.nutri_score = data_from_off['nutriments']['nutrition-score-fr_100g']
            except KeyError:
                self.nutri_score = ""
            try:
                self.stores = data_from_off['stores']
            except KeyError:
                self.stores = ""
            try:
                self.url = data_from_off['url']
            except KeyError:
                self.url = "Url not available"
        except IndexError:
            pass

        #Use index when call the class from the programme
        except TypeError:
            self.id = data_from_off[0]
            self.name = data_from_off[1]
            self.category_1 = data_from_off[2]
            self.category_2 = data_from_off[3]
            self.category_3 = data_from_off[4]
            self.category_4 = data_from_off[5]
            self.category_5 = data_from_off[6]
            self.nutri_score = data_from_off[7]
            self.stores = ""
            try:
                self.stores = data_from_off[8]
            except IndexError:
                pass
            try:
                self.url = data_from_off[9]
            except IndexError:
                self.url = data_from_off[8]
            self.index = index
