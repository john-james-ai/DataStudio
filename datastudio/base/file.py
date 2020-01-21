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

import numpy as np
import pandas as pd

class FileObject(ABC):
    """Abstract base class for FileObject subclasses."""

    def __init__(self, path, name=None):
        self._name = name or os.path.basename(path)
        self._path = path
        self._directory = os.path.dirname(path)
        self._locked = False
        self._exists = os.path.exists(path)

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

    def read(self, columns=None):
        """Reads and returns the file contents.

        Parameters
        ----------
        subset : array like (Optional)
            Used when reading .csv or .csv.gz files. Specifies specific 
            columns to read.

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
        return io.read(self._path, columns)

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
#                                   FILE GROUP                                 #   
# ---------------------------------------------------------------------------- #
class FileGroup(FileObject):
    """Collection of File and FileGroup objects.
    
    Note
    ----
    File and FileGroup objects are stored as dictionaries. No two 
    objects may have the same name. 
    """

    def __init__(self, path, name=None):
        super(File, self).__init__(path=path, name=name)
        self._file_objects = {}

    def get(name):
        """Gets the FileObject designated by 'name'.
        
        Parameters
        ----------
        name : str
            The name of the FileObject to obtain
        """
        try:
            result = self._file_objects[name]
        except KeyError:
            print("No object of the name {name} exists in the FileGroup.\
                ".format(name=name))

    def add(file_object):
        """Adds a File or FileGroup

        Parameters
        ----------
        file_object : File or FileGroup
            The object to be added to the FileGroup object.
        
        """

        name = file_object.name
        try:
            self._file_objects[name] = file_object
        except KeyError:
            print("An object with the same name, {name}, already exists in the \
                FileGroup.".format(name=name))

    def remove(name):
        """Removes a FileObject designated by 'name' from the FileGroup."""
        try:
            del self._file_objects[name]
        except KeyError:
            print("No object of the name {name} exists in the FileGroup.\
                ".format(name=name))

    def print():
        """Prints a list of the FileObjects contained herein."""
        if self._file_objects:
            d = {}
            classnames = []
            names = []
            paths = []
            created = []
            updated = []
            sizes = []

            for name, file_object in self._file_objects.items():
                classnames.append(file_object.__class__.__name__)
                names.append(file_object.name)
                paths.append(file_object.path)
                created.append(file_object.created)
                updated.append(file_object.updated)
                sizes.append(file_object.size)
            d = {
                'Class' : classnames,
                'Name' : names,
                'Path' : paths,
                'Created' : created,
                'Last Updated' : updated,
                'Size' : sizes
            }
            df = pd.DataFrame(d)
            print(tabulate(df))
        else:
            print("This FileGroup contains no FileObjects.")
    

    



# ---------------------------------------------------------------------------- #
#                                FILEIO FACTORY                                #   
# ---------------------------------------------------------------------------- #
class FileIOFactory:
    """Encapsulates an individual file on disk."""
    _FILE_HANDLERS = {'.gz': FileCSVgz(), '.csv': FileCSV(), '.npy': FileNumpy()}

    def __init__(self):
        pass
        
    def _get_file_handler(self, path):
        file_ext = os.path.splitext(path)[1]
        file_handler = self._FILE_HANDLERS.get(file_ext)
        if file_handler is None:
            raise Exception("{ext} files are not supported.".format(ext=file_ext))        
        else:
            return file_handler

    def read(self, path, columns=None):
        """Obtains a file handler based upon the file extension, then reads.""" 
        file_handler = self._get_file_handler(path)
        return file_handler.read(path, columns)

    def write(self, path, df):
        """Obtains a file handler based upon the file extension, then reads.""" 
        file_handler = self._get_file_handler(path)
        return file_handler.write(path, df)

# ---------------------------------------------------------------------------- #
#                                 FILEIO                                       #  
# ---------------------------------------------------------------------------- #
class FileIO:
    """Abstract base class for FileIO subclasses."""

    def __init__(self):
        pass

    def _check_dir(path):
        """Checks existence of a files directory and creates if not exists."""

        directory = os.path.dirname(path)
        if not os.path.exists(path):
            os.mkdir(directory)    
            print("Directory did not exist. \
                Created {dirname}.".format(dirname=directory))

    def _check_file_ext(path, ext):
        """Ensures file extension is correct."""
        if not os.path.splitext(path)[1] == ext:
            new_path = os.path.splitext(path)[0] + ext
            print("File extension incompatible with file type.\
                Saving {oldname} as {newname}.".format(
                    oldname=path, newname=new_path
                ))
            return new_path
        return path
        
#         
# ---------------------------------------------------------------------------- #
#                               FilECSVGZ                                      #  
# ---------------------------------------------------------------------------- #
class FileCSVgz:
    """Read and write .gz compressed CSV files into and from DataFrame objects."""

    def __init__(self):
        pass

    def read(self, path, columns=None):
        """Reads a .gz file, designated by 'path' into a DataFrame.
        
        Parameters
        ----------
        path : str
            The relative or fully qualified file path
        columns : list
            A list of column names to return

        Returns
        -------
        DataFrame : The file contents in DataFrame format. Returns None if 
                    unable to read the file.
        
        """
        
        try:
            result = pd.read_csv(path, compression='gzip', error_bad_lines=False,
                        low_memory=False, usecols=columns)
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
            content.to_csv(path, compression='gzip')
        except Exception as e:
            print(e)
            path = None

        return path
        
# ---------------------------------------------------------------------------- #
#                               FileCSV                                        #  
# ---------------------------------------------------------------------------- #
class FileCSV:
    """Read and write CSV files and returning DataFrames."""

    def __init__(self):
        pass

    def read(self, path, columns=None):
        """Reads a .csv file, designated by 'path' into a DataFrame.
        
        Parameters
        ----------
        path : str
            The relative or fully qualified file path
        columns : list
            A list of column names to return

        Returns
        -------
        DataFrame : The file contents in DataFrame format. Returns None if 
                    unable to read the file.
        
        """
        try:
            result = pd.read_csv(path, usecols=columns)
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
            content.to_csv(path)
        except Exception as e:
            print(e)
            path = None
        return path
        

# ---------------------------------------------------------------------------- #
#                               FileNumpy                                      #  
# ---------------------------------------------------------------------------- #
class FileNumpy:
    """Read and write numpy files (.npy, .npz)"""

    def __init__(self):
        pass

    def read(self, path, columns=None):
        """Reads a .npy or .npz file, designated by 'path' into a numpy object.

        For .npy files, a numpy array is returned. For .npz files, a dictionary
        is returned containing the filename as key and a numpy array as 
        the value, for each file in the archive.
        
        Parameters
        ----------
        path : str
            The relative or fully qualified file path
        columns : array-like
            Not used

        Returns
        -------
        numpy array / dict
            Numpy array for .npy files. Dictionary for .npz files. Returns 
                None if unable to read the file.
        
        """
        try:
            result = np.load(path)
        except IOError:
            print("The file, {fname}, does not exist. None returned.".format(fname=path))
            result = None
        except Exception as e:
            print(e)
            result = None
        return result

    def write(self, path, content):
        """Writes a numpy array, or a dictionary containing, to path.
        
        Parameters
        ----------
        path : str
            The relative or fully qualified file path
        content : numpy array or array like thereof
            A numpy array or a dictionary containing numpy arrays.

        Returns
        -------
        str
            If successful, the method returns the path to which the file was
            written.  If unsuccessful, None is returned.
        
        """
        
        self._check_dir(path)        
        if isinstance(content, (np.ndarray, np.generic)):
            path = self._check_file_ext(path, '.npy')
            try:                
                np.save(path, content)
            except Exception as e:
                print(e)
                path = None
        else:
            path = self._check_file_ext(path, '.npz')
            try:
                np.savez(path, content)
            except Exception as e:
                print(e)
                path = None        
        return path
