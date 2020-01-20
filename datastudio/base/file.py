#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : MetaData Studio                                                   #
# Version : 0.1.0                                                             #
# File    : file_object.py                                                    #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# --------------------------------------------------------------------------- #
# Created       : Monday, January 20th 2020, 12:52:03 pm                      #
# Last Modified : Monday, January 20th 2020, 12:52:03 pm                      #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""File module includes classes for reading, writing and manipulating files.

Two categories of classes encapsulate file capabilities.

    * FileObject : Object representations of files and groups of files.
    * FileIO : Factory and handlers for file i/o.

The FileObject classes include:
    
    * FileObject: The abstract base class for all FileObject subclasses.
    * File : Concrete class that encapsulates a single file on disk.
    * FileGroup : A collection of FileGroup or File objects.

The FileIO family of classes include:

    * FileCSV : File handler for CSV files
    * FileJSON : Flle handler for JSON files
    * FileCSVGZ : File handler for .GZ compressed files
    * FileIOFactory : Returns a file hander based upon file extension.
    
    * other FileIO classes to be added as needed.
"""
from abc import ABC, abstractmethod
import os
import shutil
import pandas as pd

class FileObject(ABC):
    """Abstract base class for FileObject subclasses."""

    def __init__(self, path, name=None):
        self._name = name or os.path.basename(path)
        self._path = path
        self._directory = os.path.dirname(path)
        self._locked = False
        self._exists = True

    @property
    def name(self):
        """Returns the name of the FileObject."""
        return self._name

    @property
    def path(self):
        """Returns the path to the file."""
        return self._path

    @property
    def directory(self):
        """Returns the directory for the file."""
        return self._directory

    @property
    def locked(self):
        """Returns True if the file is locked, returns False otherwise."""
        return self._locked

    @property
    def exists(self):
        """Returns True if the file exists, returns False otherwise."""
        return self._exists

    def lock(self):
        """Locks the file, preventing any updates or writes to the file."""
        self._locked = True
    
    def unlock(self):
        """Unlocks the file."""
        self._locked = False

# ---------------------------------------------------------------------------- #
#                                     FILE                                     #   
# ---------------------------------------------------------------------------- #
class File(FileObject):
    """Encapsulates content and behaviors of individual files on disk.

    File class includes the location and obtains appropriate file I/O handlers
    for reading and writing the files. Methods are exposed to move, copy
    and rename the file represented by the File object.
    
    Parameters
    ----------
    path : str
        The absolute or relative path (from current working directory).
    name : str
        The name for the File object, not the name of the file. The filename
        should be included in the path variable.   
    
    """

    def __init__(self, path, name=None):
        super(File, self).__init__(path=path, name=name)
        self._filename = os.path.basename(path)
        self._fileext = os.path.splitext(path)[1]

    @property
    def filename(self):
        """Returns the file name."""
        return self._filename

    @property
    def file_ext(self):
        """Returns the file extension."""
        return self._fileext

    def _update_filename_data(path):
        """Updates the directory, filename, and extension based upon 'path'."""
        self._path = path
        self._directory = os.path.dirname(path)
        self._filename = os.path.basename(path)
        self._fileext = os.path.splitext(path)[1]

    def copy(self, path):
        """ Copies a file from current location to 'path'.
        
        Parameters
        ----------
        path : str
            The absolute or relative path to which the file should be copied.
            
        Returns
        ------
        str
            The path to the new file.

        """
        return shutil.copy2(self._path, path)

    def move(self, path):        
        """ Moves a file from current location to 'path'.

        Moves the file to the destination indicated by 'path' and updates file location
        data.
        
        Parameters
        ----------
        path : str
            The absolute or relative path to which the file should be moved.
            
        Returns
        ------
        str
            The path to the new file.

        """
        new_path = shutil.move(self._path, path)
        self._update_filename_data(new_path)
        return new_path

    def rename(self, name):
        """ Renames a file.

        Parameters
        ----------
        name : str
            The name and file extension to which the file should be renamed.

        """
        new_path = os.path.join(self._directory, name)
        os.rename(self._path, new_path)
        self._update_filename_data(new_path)
        return new_path

    def read(self):
        """Reads and returns the file contents.

        Returns
        -------
            The format of the data returned is based upon the file format 
            as follows:

                File Format             Return Format
                -----------             -------------
                .txt                    string
                .csv                    Pandas DataFrame
                .csv.gz                 Pandas DataFrame
                .json                   JSON
                .npy                    Numpy Array
        
            Support for additional formats will be added as needed.

        """
        io = FileIOFactory()
        return io.read(self._path)

    def write(self, content):
        """Writes content to file.

        The format of the content must correspond with the file type. The 
        formats and their corresponding file types are:

        Format              File Type
        ------              ---------
        string              .txt
        DataFrame           .csv
        Numpy Array         .npy
        JSON                .json

        """

        io = FileIOFactory()
        io.write(self._path, content)


# ---------------------------------------------------------------------------- #
#                                FILEIO FACTORY                                #   
# ---------------------------------------------------------------------------- #
class FileIOFactory:
    """Encapsulates an individual file on disk."""
    _FILE_HANDLERS = {'gz': FileGZ(), 'csv': FileCSV()}

    def __init__(self):
        pass
        
    def _get_file_handler(self, filename):
        file_ext = filename.split(".")[-1]
        file_handler = self._FILE_HANDLERS.get(file_ext)
        if file_handler is None:
            raise Exception("{ext} files are not supported.".format(ext=file_ext))        
        else:
            return file_handler

    def read(self, filename, columns=None):
        """Obtains a file handler based upon the file extension, then reads.""" 
        file_handler = self._get_file_handler(filename)
        return file_handler.read(filename, columns)

    def write(self, filename, df):
        """Obtains a file handler based upon the file extension, then reads.""" 
        file_handler = self._get_file_handler(filename)
        return file_handler.write(filename, df)
# ---------------------------------------------------------------------------- #
#                               FileGZ                                         #  
# ---------------------------------------------------------------------------- #
class FileGZ(BaseFile):
    """Read and write compressed GZ files and returning DataFrames."""

    def __init__(self):
        pass

    def read(self, filename, columns=None):
        """Reads a .gz file, designated by 'filename' into a DataFrame.
        
        Parameters
        ----------
        filename : str
            The relative or fully qualified file path
        columns : list
            A list of column names to return

        Returns
        -------
        DataFrame : The file contents in DataFrame format.
        
        """

        self._filename = filename
        df = pd.read_csv(filename, compression='gzip', error_bad_lines=False,
                        low_memory=False, usecols=columns)
        return df

    def write(self, filename, df):
        """Accepts a filename and a DataFrame and writes it to a .gz file.
        
        Parameters
        ----------
        filename : str
            The relative or fully qualified file path
        df : DataFrame
            The DataFrame object to be written to file.

        Returns
        -------
        self
        
        """

        self._filename = filename
        self._df = df
        check_dir(filename)
        df.to_csv(filename, compression='gzip')
        return self
        
# ---------------------------------------------------------------------------- #
#                               FileCSV                                        #  
# ---------------------------------------------------------------------------- #
class FileCSV(BaseFile):
    """Read and write CSV files and returning DataFrames."""

    def __init__(self):
        pass

    def read(self, filename, columns=None):
        """Reads a .csv file, designated by 'filename' into a DataFrame.
        
        Parameters
        ----------
        filename : str
            The relative or fully qualified file path
        columns : list
            A list of column names to return

        Returns
        -------
        DataFrame : The file contents in DataFrame format.
        
        """

        self._filename = filename
        df = pd.read_csv(filename, usecols=columns)
        return df

    def write(self, filename, df):
        """Accepts a filename and a DataFrame and writes it to a .csv file.
        
        Parameters
        ----------
        filename : str
            The relative or fully qualified file path
        df : DataFrame
            The DataFrame object to be written to file.

        Returns
        -------
        self
        
        """

        self._filename = filename
        self._df = df
        check_dir(filename)
        df.to_csv(filename)
        return self
        


# ---------------------------------------------------------------------------- #
#                                    HELPERS                                   #   
# ---------------------------------------------------------------------------- #        
def check_dir(filename):
    directory = os.path.dirname(filename)
    if os.path.exists(directory):
        pass
    else:
        os.mkdir(directory)