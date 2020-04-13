# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 13:39:03 2020

@author: Brendan Non-Admin
"""

import psycopg2
from connection_config import cc

class RedshiftSQLHelper:

    def __init__(self, fin):
        self.fin = fin
        self.sql = open(fin, 'r').read()
        self.conn = psycopg2.connect(**cc)
        self.cur = self.conn.cursor()
        self.commands = list()
        self.split_commands()

    def split_commands(self):
        sql = open(self.fin, 'r').read()
        for command in sql.split(';\n'):
            command = command.strip()
            if command != '':
                self.commands.append(command)

    def print_commands(self):
        for command in self.commands:
            print('\n' + '*' * 80 + '\n\n', command)

    def excecute_commands(self):
        for command in self.commands:
            print('\n' + '*' * 80 + '\n\n', 'Executing:', '\n', command)
            self.cur.execute(command)
        self.cur.close()
        print('\n' + '*' * 80 + '\n\n', 'Execution Complete')