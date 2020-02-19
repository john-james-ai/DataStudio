#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : file.py                                                           #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# --------------------------------------------------------------------------- #
# Created       : Monday, January 20th 2020, 12:52:03 pm                      #
# Last Modified : Tuesday, January 21st 2020, 7:14:39 pm                      #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""File module includes classes for reading, writing and manipulating files.

There types of classes are included in this module.

    * File : Concrete class that encapsulates a single file on disk.
    * FileIO : Abstract base class for file input and output.
    * FileIOCSV : File handler for CSV files    
    * FileIOCSVGZ : File handler for .GZ compressed files    
    * FileIOStrategy : Returns a file hander based upon file extension.
    
File types which support tabular data have been prioritized. Support for
additional file formats will be added to future releases if and
when needed.
"""
from abc import ABC, abstractmethod
import os
import shutil
import pandas as pd

# ---------------------------------------------------------------------------- #
#                                     FILE                                     #   
# ---------------------------------------------------------------------------- #
class File:
    """ Encapsulates information and behaviors of files. 

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
        self._name = name or os.path.splitext(os.path.basename(path))[0]
        self._path = path
        self._directory = os.path.dirname(path)
        self._locked = False
        self._exists = os.path.exists(path)    
        self._filename =  os.path.basename(path)
        self._fileext = os.path.splitext(path)[1]
        self._io = FileIO()

    @property
    def name(self):
        """Returns the name of the FileObject."""
        return self._name

    @property
    def path(self):
        """Returns the path to the file."""
        return self._path

    @property
    def filename(self):
        """Returns the file name."""
        return self._filename

    @property
    def directory(self):
        """Returns the directory for the file."""
        return self._directory

    @property
    def file_ext(self):
        """Returns the file extension."""
        return self._fileext

    @property
    def exists(self):
        """Returns True if the file exists, returns False otherwise."""
        return self._exists

    @property
    def is_locked(self):
        """Returns True if the file is locked, returns False otherwise."""
        return self._locked

    def lock(self):
        """Locks the file, preventing any updates or writes to the file."""
        self._locked = True        

    def _update_filename_data(self, path):
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
            The path to the new file if the file is unlocked. Returns None
            if file is locked.

        """
        if self._is_unlocked(self._path, 'move'):
            new_path = shutil.move(self._path, path)
            self._update_filename_data(new_path)
            return new_path
        return None


    def rename(self, name):
        """ Renames a file.

        This method renames the file basename, but not the file extension. 

        Parameters
        ----------
        name : str
            The name and file to which the file should be renamed.

        Returns
        ------
        str
            The path to the new file if the file is unlocked. Returns None
            if file is locked.

        """
        if self._is_unlocked(self._path, 'rename'):
            new_path = os.path.splitext(\
                os.path.join(self._directory, name))[0].replace("\\", "/")\
                + self._fileext
            os.rename(self._path, new_path)
            self._update_filename_data(new_path)
            return new_path
        return None

    def read(self, filter=None):
        """Reads and returns the file contents.

        Parameters
        ----------
        filter : array like (Optional)
            Specifies specific columns to read.

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
        return self._io.read(self._path, filter)

    def write(self, content):
        """Writes content to file.

        The format of the content must correspond with the file type. The 
        formats and their corresponding file types are:

        Format              File Type
        ------              ---------
        string              .txt
        DataFrame           .csv
        DataFrame           .csv.gz
        Numpy Array         .npy
        JSON                .json

        """
        if self._is_unlocked(self._path, 'write'):            
            self._io.write(self._path, content)


# ---------------------------------------------------------------------------- #
#                            FileIOStrategy                                    #  
# ---------------------------------------------------------------------------- #
class FileIOStrategy(ABC):
    """Abstract base class for FileIO subclasses."""

    @abstractmethod
    def read(self, path, filter=None):
        pass

    @abstractmethod
    def write(self, path, content):
        pass

    
    def _check_dir(self, path):
        """Checks existence of a files directory and creates if not exists."""

        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.mkdir(directory)    
            print("Directory did not exist. \
                Created {dirname}.".format(dirname=directory))

    def _check_file_ext(self, path, ext):
        """Ensures file extension is correct."""
        if not os.path.splitext(path)[1] == ext:
            new_path = path + ext
            print("File extension incompatible with file type.\
                Saving {oldname} as {newname}.".format(
                    oldname=path, newname=new_path
                ))
            return new_path
        return path
        
#         
# ---------------------------------------------------------------------------- #
#                               FilEIOCSVgz                                    #  
# ---------------------------------------------------------------------------- #
class FileIOCSVgz(FileIOStrategy):
    """Read and write .gz compressed CSV files into and from DataFrame objects."""

    def read(self, path, filter=None):
        """Reads a .gz file, designated by 'path' into a DataFrame.
        
        Parameters
        ----------
        path : str
            The relative or fully qualified file path
        filter : list
            A list of the column names to include in the result. 

        Returns
        -------
        DataFrame : The file contents in DataFrame format. Returns None if 
                    unable to read the file.
        
        """
        
        try:
            result = pd.read_csv(path, compression='gzip', error_bad_lines=False,
                        low_memory=False, usecols=filter)
        except IOError:
            print("The file, {fname}, does not exist. None returned.".format(fname=path))
            result = None
        except Exception as e:
            print(e)
            result = None
        return result

    def write(self, path, content):
        """Accepts a path and a DataFrame and writes it to a .csv.gz file.
        
        Parameters
        ----------
        path : str
            The relative or fully qualified file path
        content : DataFrame
            The content to be written to file.

        Returns
        -------
        str
            If successful, the method returns the path to which the file was
            written.  If unsuccessful, None is returned.
        
        """
        
        self._check_dir(path)
        path = self._check_file_ext(path, '.gz')
        try:
            content.to_csv(path, compression='gzip', index=False)
        except Exception as e:
            print(e)
            path = None

        return path
        
# ---------------------------------------------------------------------------- #
#                               FileIOCSV                                      #  
# ---------------------------------------------------------------------------- #
class FileIOCSV(FileIOStrategy):
    """Read and write CSV files and returning DataFrames."""

    def read(self, path, filter=None):
        """Reads a .csv file, designated by 'path' into a DataFrame.
        
        Parameters
        ----------
        path : str
            The relative or fully qualified file path
        filter : list
            A list of column names to return in the result

        Returns
        -------
        DataFrame : The file contents in DataFrame format. Returns None if 
                    unable to read the file.
        
        """
        try:
            result = pd.read_csv(path, usecols=filter, low_memory=False)
        except IOError:
            print("The file, {fname}, does not exist. None returned.".format(fname=path))
            result = None
        except Exception as e:
            print(e)
            result = None
        return result

    def write(self, path, content):
        """Accepts a filename and a DataFrame and writes it to a .csv file.
        
        Parameters
        ----------
        path : str
            The relative or fully qualified file path
        content : DataFrame
            The DataFrame object to be written to file.

        Returns
        -------
        str
            If successful, the method returns the path to which the file was
            written.  If unsuccessful, None is returned.

        """

        self._check_dir(path)
        path = self._check_file_ext(path, '.csv')
        try:
            content.to_csv(path, index=False)
        except Exception as e:
            print(e)
            path = None
        return path
        

# ---------------------------------------------------------------------------- #
#                               FileIOTXT                                      #  
# ---------------------------------------------------------------------------- #
class FileIOTXT(FileIOStrategy):
    """Read and write TXT files, returning strings."""

    def read(self, path, filter=None):
        """Reads a .txt file, designated by 'path' into a DataFrame.
        
        Parameters
        ----------
        path : str
            The relative or fully qualified file path
        filter : list
            The number of bytes to read

        Returns
        -------
        string : The file contents in string format. Returns None if 
                    unable to read the file.
        
        """
        try:
            f = open(path, 'r')
            result = f.read(filter)
        except IOError:
            print("The file, {fname}, does not exist. None returned.".format(fname=path))
            result = None
        except Exception as e:
            print(e)
            result = None
        return result

    def write(self, path, content):
        """Accepts a filename and a DataFrame and writes it to a .csv file.
        
        Parameters
        ----------
        path : str
            The relative or fully qualified file path
        content : string or list of strings
            For string content, write will places the string on a single line
            in the text file. For a list of strings, writelines is used to
            place each string on a separate line. Note: When writing a
            list of strings, they are not saved as a list, but as strings
            of text separated by '\n'. Therefore, the read method will not
            return a list but a continuous string with '\n' separating each
            list element. 

        Returns
        -------
        str
            If successful, the method returns the path to which the file was
            written.  If unsuccessful, None is returned.

        """

        self._check_dir(path)
        path = self._check_file_ext(path, '.txt')
        try:
            f = open(path, 'w')
            if isinstance(content, str):                
                f.write(content)
            else:
                for string in content:
                    f.writelines(string)
        except Exception as e:
            print(e)
            path = None
        return path


# ---------------------------------------------------------------------------- #
#                                  FILEIO                                      #     
# ---------------------------------------------------------------------------- #
class FileIO:
    """Context class sets IO strategy and performs IO operations ."""
    _FILE_HANDLERS = {'.gz': FileIOCSVgz(), '.csv': FileIOCSV()}

    def __init__(self):
        pass
        
    def _get_file_handler(self, path):
        file_ext = os.path.splitext(path)[1]
        file_handler = self._FILE_HANDLERS.get(file_ext)
        if file_handler is None:
            raise Exception("{ext} files are not supported.".format(ext=file_ext))        
        else:
            return file_handler

    def read(self, path, filter=None):
        """Obtains a file handler based upon the file extension, then reads.""" 
        file_handler = self._get_file_handler(path)
        return file_handler.read(path, filter)

    def write(self, path, df):
        """Obtains a file handler based upon the file extension, then reads.""" 
        file_handler = self._get_file_handler(path)
        return file_handler.write(path, df)