#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This file contain classes representing the data base of this programm"""


class Categories():
    """Class representing the 'Categories' table of the database"""

    def __init__(self, data_from_off):
        """Init taking a dictionnary for argument"""
        self.id = data_from_off['id']
        self.name = data_from_off['name']

class Food():
    """Class representing the 'Food' table of the database"""
    
    def __init__(self, data_from_off):    
        """Init taking a dictionnary for argument"""
        #No id attribute because of the auto-increment
        self.name = data_from_off['product_name']
        self.categories_id = data_from_off['categories_tags']
        self.stores = data_from_off['stores']