#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : datalayer.py                                                      #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# --------------------------------------------------------------------------- #
# Created       : Thursday, January 23rd 2020, 5:40:50 pm                     #
# Last Modified : Thursday, January 23rd 2020, 5:40:50 pm                     #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Module encapsulating all PostgreSQL data operations."""
from abc import ABC, abstractmethod
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from credentials import USERID, PASSWORD, HOST, PORT, SERVER
# --------------------------------------------------------------------------- #
#                                DATALAYER                                    #
# --------------------------------------------------------------------------- #
class DataLayer(ABC):
    """Abstract base layer for DataLayer objects."""

    def __init__(self, name):
        self._name = name
        self._userid = USERID
        self._pwd = PASSWORD
        self._host = HOST
        self._port = PORT
        self._server = SERVER

    @property
    def name(self):
        return self._name

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def get(self, name):
        pass    

    @abstractmethod
    def add(self, data_entity):
        pass

    @abstractmethod
    def delete(self, data_entity):
        pass

# --------------------------------------------------------------------------- #
#                                DATALAYER                                    #
# --------------------------------------------------------------------------- #
class Database(DataLayer):
    """Creates & manages PostgreSQL databases and contains DataTable objects.""" 

    def __init__(self, name):
        super(Database, self).__init__(name)
        self._server_connection = None
        self._db_connection = None
        self._cursor = None
        self._data_entities = {}

    def _connect(self, name):
        """Creates a connection to PostgreSQL server."""
        try:
            connection = psycopg2.connect(user = self._userid,
                                          password = self._pwd,
                                          host = self._host,
                                          port = self._port,
                                          database = name)            
        except (Exception, psycopg2.Error) as error: 
            print("Error while connecting to PostgreSQL. {error}".format(
                error=error))
            return None
        # Print PostgreSQL cursor properties
        print(connection.get_dsn_parameters(), "\n")            
        return connection

    def _get_server_connection(self):
        self._server_connection = self._connect(self._server)
        self._server_connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)        

    def _get_db_connection(self):
        self._db_connection = self._connect(self._name)


    def _close_connection(self, connection):
        """Closes connection."""
        if (connection):
            connection.close()
            print("PostgreSQL connection is closed.")

    def _close_cursor(self, cursor):
        if (cursor):
            cursor.close()
            print("PostgreSQL cursor is closed.")

    def create(self):
        """Creates a PostgreSQL database."""
        # Connect to PostgreSQL DBMS
        self._get_server_connection()
        self._cursor = self._server_connection.cursor()
        try:
            self._cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                        sql.Identifier(self._name)))
            # Print PostgreSQL Database version
            self._cursor.execute('SELECT version()')
            db_version = self._cursor.fetchone()
            print(db_version)                    
        except (Exception, psycopg2.Error) as error:
            print("Error creating databases {db}. {error}".format(
                        db=self._name, error = error))
        finally:
            self._close_connection(self._server_connection)            
            self._close_cursor(self._cursor)
            

    def drop_db(self):
        """Drops the PostgreSQL database."""
        self._get_server_connection()
        self._cursor = self._server_connection.cursor()
        try:
            self._cursor.execute(sql.SQL("drop database if exists {}").format(
                sql.Identifier(self._name)))
            print("Successfully dropped {name} database.".format(
                name=self._name))
        except (Exception, psycopg2.Error) as error:
            print("Error dropping the {name} database. {error}".format(
                name=self._name, error=error))
        finally:
            self._close_connection(self._server_connection)
            self._close_cursor(self._cursor)


    def get(self, name):
        """Retrieves a member Database or DataTable object.

        Parameters
        ----------
        name : str
            The name of the Database or DataTable object

        """
        return self._data_entities[name]
        

    def add(self, data_entity):
        """Adds a data_entity to the Database object.
        
        Parameters
        ----------
        data_entity : Database, DataTable
            Object to add to the Database object.
        
        """
        self._data_entities[data_entity.name] = data_entity
        return self

    def delete(self, name):
        """Deletes a data_entity from the Database object.

        Parameters
        ----------
        name : str
            The name of the Database or DataTable object

        """
        del self._data_entities[name]
        return self
    

        