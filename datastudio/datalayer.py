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
import logging
from logging.handlers import TimedRotatingFileHandler
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
import sys
import yaml

CREDENTIALS_FILENAME = 'credentials.yaml'
# --------------------------------------------------------------------------- #
#                                DATALAYER                                    #
# --------------------------------------------------------------------------- #
class DataLayer(ABC):
    """Abstract base layer for DataLayer objects."""

    def __init__(self, name):
        # Name for database to be created
        self._name = name                
        
        # Configure Logger
        self._log = logging.getLogger(__name__)    

        # Obtain PostgreSQL credentials.
        with open(CREDENTIALS_FILENAME) as f:
            vals = yaml.load(f, Loader=yaml.FullLoader)

        if ('USERID' not in vals.keys() or
            'PASSWORD' not in vals.keys() or
            'DBNAME' not in vals.keys() or
            'HOST' not in vals.keys() or
            'PORT' not in vals.keys()):
            raise ValueError('Bad credentials file: ' + CREDENTIALS_FILENAME)

        self._userid = vals['USERID']
        self._pwd = vals['PASSWORD']
        self._pg_dbname = vals['DBNAME']
        self._host = vals['HOST']
        self._port = vals['PORT']

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
#                                DATABASE                                     #
# --------------------------------------------------------------------------- #
class Database(DataLayer):
    """Creates & manages PostgreSQL databases and contains DataTable objects.""" 

    def __init__(self, name):
        super(Database, self).__init__(name)

    def _connect(self, name):
        try:
            engine = self._get_connection(name)
            self._log.info("Connected to {name} database!".format(name=name))
        except IOError:
            self._log.exception("Failed to connect to {name} database!".format(name=name))
            return None
        return engine

    def _get_connection(self, name):
        """Connects to named database."""
        
        url = "postgresql://{user}:{passwd}@{host}:{port}/{db}".format(
            user=self._userid, passwd=self._pwd, host=self._host, 
            port=self._port, db=name)
      
        engine = create_engine(url, pool_size=50)
        return engine
         
    def get_server_connection(self):
        return self._connect(self._pg_dbname).raw_connection()              

    def get_db_connection(self):
        return self._connect(self._name).raw_connection()        

    def _terminate_connections(self, name, cursor):
        """Terminates active connections to databases."""
        # Assumes connection and cursor to server. 
        self._log.info("Terminating active connections.")
        try:
            cursor.execute(\
                "SELECT pg_terminate_backend(pg_stat_activity.pid)\
                    FROM pg_stat_activity \
                        WHERE pg_stat_activity.datname = %s;", (name,))
            self._log.info("Active connections on {name} terminated.".format(
                name=name
            ))
        except (Exception, psycopg2.Error) as error:
            self._log.exception("Error terminating active connections. {error}"\
                .format(error=error))

    def create(self):
        """Creates a PostgreSQL database."""
        # Connect to PostgreSQL DBMS
        self._log.info("Creating {name} database.".format(name=self._name))
        connection = self.get_server_connection()
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  
        cursor = connection.cursor()
        try:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                        sql.Identifier(self._name)))
            # Print PostgreSQL Database version
            cursor.execute('SELECT version()')
            db_version = cursor.fetchone()
            self._log.info(db_version)                    
        except (Exception, psycopg2.Error) as error:
            self._log.info("Error creating databases {db}. {error}".format(
                        db=self._name, error = error))
        finally:
            connection.close()            
            cursor.close()
            

    def drop_db(self):
        """Drops the PostgreSQL database."""
        connection = self.get_server_connection()
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  
        cursor = connection.cursor()
        self._terminate_connections(self._name, cursor)
        try:
            cursor.execute(sql.SQL("drop database if exists {}").format(
                sql.Identifier(self._name)))
            self._log.info("Successfully dropped {name} database.".format(
                name=self._name))
        except (Exception, psycopg2.Error) as error:
            self._log.info("Error dropping the {name} database. {error}".format(
                name=self._name, error=error))
        finally:
            connection.close()
            cursor.close()

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
    
# --------------------------------------------------------------------------- #
#                                DATATABLE                                    #
# --------------------------------------------------------------------------- #
class DataTable(DataLayer):
    """Creates and manages PostgreSQL data tables."""

    def __init__(self, name):
        super(DataTable, self).__init__(name)        

    def create(self, df):
        """Creates a PostgreSQL data table from a pandas DataFrame object.
        
        Parameters
        ----------
        df : DataFrame
            The pandas DataFrame to be written to the table.
        """
