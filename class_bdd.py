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
            self.categories_id = data_from_off['categories_tags']
            self.stores = data_from_off['stores']
        #Use index when call the class from the programme
        except TypeError:
            self.name = data_from_off[0]
            self.categories_id = data_from_off[1].replace("'", "").replace(")", "")\
            .replace("(", "").split(',')
            self.stores = ""
            try:
                self.stores = data_from_off[2]
            except IndexError: 
                pass
            self.index = index
