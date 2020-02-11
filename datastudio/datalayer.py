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
from io import StringIO
import logging
from logging.handlers import TimedRotatingFileHandler
import pandas as pd
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

    def _connect(self, name):
        """Returns a connection to the named database."""
        url = "postgresql://{user}:{passwd}@{host}:{port}/{db}".format(
            user=self._userid, passwd=self._pwd, host=self._host, 
            port=self._port, db=name)        
        try:
            engine = create_engine(url)
            self._log.info("Connected to {name} database!".format(name=name))
        except IOError:
            self._log.exception("Failed to connect to {name} database!".format(name=name))
            return None
        return engine
         
    def get_server_connection(self):
        """Returns a connection to the PostgreSQL Database server."""
        return self._connect(self._pg_dbname).raw_connection()              

    def get_db_connection(self):
        """Returns a connection to a named database."""
        return self._connect(self._name).raw_connection()  

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

    def delete(self):
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

        # Copy the DataFrame to CSV Format
        data = StringIO()
        df.to_csv(data, header=False, index=False)
        data.seek(0)
        
        # Obtain connection to the PostgreSQL database and cursor
        connection = self.get_server_connection()
        cursor = connection.cursor()

        # Drop the table if it already exists
        cursor.execute("DROP TABLE IF EXISTS " + self._name)

        # Create empty table
        empty_table = pd.io.sql.get_schema(df, self._name, con=connection)
        empty_table = empty_table.replace('"','')

        # Copy data to table and commit
        cursor.execute(empty_table)
        cursor.copy_from(data, self._name)
        cursor.connection.commit()

        # Close connection and cursor
        connection.close()
        cursor.close()

        
        # Write dataframe to table
        # df.to_sql(name=self._name, con=connection, if_exists = 'replace', 
        #           index=False)
        return self

    def get(self):
        """Retrieves all data from the data table."""

        # Obtain connection to the PostgreSQL database  
        connection = self.get_server_connection()

        # Reading PostgreSQL table into pandas DataFrame.
        try:
            df = pd.read_sql('SELECT * FROM {}', connection).format(self._name)
            rows = df.shape[0]
            cols = df.shape[1]
            msg = """Created {name} data table with a pandas DataFrame
            containing {rows} rows and {cols} columns.""".format(name=self._name,
            rows=rows, cols=cols)                
            self._log.info(msg)
        except (Exception, psycopg2.Error) as error:
            msg = """Attempt to create the {name} data table from a pandas
            DataFrame failed. {error}""".format(name=self._name,
            error=error)
            self._log.info(msg)

        return df

    def add(self, df):
        """Adds rows from pandas DataFrame to data table.
        
        Parameters
        ----------
        df : DataFrame
            The pandas DataFrame to be written to the table.        
        """
        # Obtain connection to the PostgreSQL database  
        connection = self.get_server_connection()
        
        # Append dataframe to table
        try:
            df.to_sql(name=self._name, con=connection, if_exists = 'append', 
                      index=False)
            rows = df.shape[0]
            cols = df.shape[1]
            msg = """Appended pandas DataFrame containing {rows} rows 
            and {cols} columns to {name} data table.""".format(
            rows=rows, cols=cols, name=self._name)                
            self._log.info(msg)
        except (Exception, psycopg2.Error) as error:
            msg = """Attempt to append a pandas DataFrame to the {name} data 
            table failed. {error}""".format(name=self._name,
            error=error)
            self._log.info(msg)

    def delete(self):
        """Drops the PostgreSQL data table."""
        connection = self.get_server_connection()
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  
        cursor = connection.cursor()
        #self._terminate_connections(self._name, cursor)
        try:
            cursor.execute(sql.SQL("drop table if exists {}").format(
                sql.Identifier(self._name)))
            self._log.info("Successfully deleted {name} table.".format(
                name=self._name))
        except (Exception, psycopg2.Error) as error:
            self._log.info("Error deleting the {name} table. {error}".format(
                name=self._name, error=error))
        finally:
            connection.close()
            cursor.close()            