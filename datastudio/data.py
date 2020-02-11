#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : data.py                                                           #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# --------------------------------------------------------------------------- #
# Created       : Saturday, January 18th 2020, 4:04:31 pm                     #
# Last Modified : Tuesday, February 11th 2020, 4:42:25 pm                     #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Module defines the DataObject classes core to the DataStudio Environment.

Three classes define the DataStudio core DataObject model:

    * DataObject : Abstract base class for DataObjects.
    * DataSet : A single identifiable set of data. 
    * DataGroup : Collection of DataSet or DataGroup objects. 

"""
#%%
from abc import ABC, abstractmethod
from collections import OrderedDict
import pandas as pd

from src.data.file_classes import File
# --------------------------------------------------------------------------- #
#                                DataObject                                   #
# --------------------------------------------------------------------------- #
"""Abstract class that defines the interface for DataObject subclasses.

Parameters
----------
name : str
       The name to assign to the DataObject object

"""
class DataObject(ABC):

    def __init__(self, name):
        self._df = pd.DataFrame()
        self._metadata = pd.DataFrame()
        self._summary = pd.DataFrame()

    def metadata(self):
        """Prints object metadata."""
        print("\n#","="*30,  "Author Information",  "="*30,"#")
        print(f"Id: {self._id}")
        print(f"Creator: {self._creator}")
        print(f"Created: {self._created}")
        print(f"Modifier: {self._modifier}")
        print(f"Modified: {self._modified}")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        return self

    @abstractmethod
    def summarize(self):
        pass

    @abstractmethod
    def get_data(self, name):
        """Returns the Data object designated by the name."""
        pass

    @abstractmethod
    def add(self, data):
        pass

    @abstractmethod
    def remove(self, name):
        pass

# --------------------------------------------------------------------------- #
#                              DataCollection                                 #
# --------------------------------------------------------------------------- #
class DataCollection(DataObject):
    """The Composite of the Data Object Model."""

    def __init__(self, name):
        super(DataCollection, self).__init__(name)
        self._data_collection = OrderedDict()

    def merge_data(self):
        """Merges all DataSets and DataCollections into a single DataFrame."""
        merged = pd.DataFrame()
        for _, data_object in self._data_collection.items():
            df = data_object.get_data()
            merged = pd.concat([merged,df], axis=0)
        return merged


    def metadata(self):
        """Prints DataCollection metadata."""
        super(DataCollection, self).metadata(verbose)
        print("="*30, "DataType Summary", "="*30)
        merged = self._merge_data()
        metadata = pd.DataFrame()
        metadata[self._name] = merged.dtypes.value_counts()
        print(metadata)
        return metadata


    def summarize(self):
        """Descriptive summaries for DataCollection and DataSet objects.
        
        Parameters
        ----------
        verbose : Bool
            True if the summary should be printed.

        Returns
        -------
        Dict : Cointaining quantitative and qualitative descriptive 
               statistics.
        
        """
        describe = Describe()
        df = self.merge_data()
        describe.fit(df)            
        summary = describe.get_analysis()        
    
        print("#","=*35  Quantitative Analysis  35*=","#")
        print(summary['quant'])
        print("#","=*35  Quantitative Analysis  35*=","#")
        print(summary['qual'])            
        return summary

    def get_data(self, name=None):
        """Return all data or the named dataset or collection.
        
        Parameters
        ----------
        name : str
            The name of the DataSet or DataCollection object.
        """
        if name:
            return self._data_collection[name]            
        else:
            return self._data_collection

    def add(self, data):
        """Adds a DataSet or DataCollection object to the collection.
        
        Parameters
        ----------
        dataset : DataSet or DataCollection object.
        """
        name = data.name
        self._data_collection[name] = data
        return self

    def remove(self, name):
        """Removes a DataSet or DataCollection object from the collection."""
        del self._data_collection[name]        
        return self

    def replace_string(self, pattern, replace, columns=None, regex=True):
        """Regex capable, string replace method for DataSet objects.
        
        Parameters
        ----------
        pattern : str
            A (regex) pattern to find in the DataSet or designated columns.
        replace : str
            A string sequence to replace the pattern
        columns : array-like (Optional)
            List of columns to which the replacement should be applied.
        regex : Bool
            Indicates whether the pattern and replacement are valid regex.

        """
        for _, data_object in self._data_collection.items():
            if columns:
                data_object.replace_string(pattern, replace, columns, regex)
            else:
                data_object.replace_string(pattern, replace, regex)
            self._add(data_object)


    def cast_types(self, data_types):
        """Cast objects of the dataframe to designated types."""
        for _, data_object in self._data_collection.items():
            data_object.cast_types(data_types)
            self._add(data_object)


    def import_data(self, directory, columns=None):
        """Creates DataSet objects, imports the data and adds the DataSets.

        Parameters
        ----------
        directory : str
            The directory containing the files to import.
        columns : list
            List of column names to return.
        """

        filenames = os.listdir(directory)
        for filename in filenames:
            name = filename.split(".")[0]
            dataset = DataSet(name=name)            
            path = os.path.join(directory, filename)
            dataset.import_data(filename=path, columns=columns)
            self.add(data=dataset)
        return self

    def export_data(self, directory, file_format='csv'):
        """Exports the data from contained DataSets to the directory in format.

        Parameters
        ----------
        directory : str
            The directory to which the data will be exported.
        file_format : str
            The format in which the data will be saved.
        """
        for name, dataset in self._data_collection.items():
            filename = name + "." + file_format
            path = os.path.join(directory, filename)
            dataset.export_data(filename=path)
        return self

# --------------------------------------------------------------------------- #
#                              DataSet                                        #
# --------------------------------------------------------------------------- #
class DataSet(DataObject):
    """Base class for all DataSet subclasses.
    
    Parameters
    ----------
    name : str
        The name of the dataset.
    df : DataFrame (Optional)
        The content in DataFrame format.
    """
    def __init__(self, name):
        super(DataSet, self).__init__(name)           

    def metadata(self):
        """Prints DataSet metadata."""
        super(DataSet, self).metadata()
        print("#","="*30, "DataType Summary", "="*30,"#")
        metadata = pd.DataFrame()
        metadata[self._name] = self._df.dtypes.value_counts()
        print(metadata)
        print("#","="*30, "DataType Detail", "="*30,"#")                
        metadata = pd.DataFrame()
        metadata[self._name] = self._df.dtypes.T        
        print(metadata)        
        return metadata
    
    def summarize(self, verbose=True):
        """Prints DataSet descriptive statistics."""
        describe = Describe()
        describe.fit(self)
        summary = describe.get_analysis()
        if verbose:
            print("\n#=*35  Quantitative Analysis  35*=#")
            print(summary['quant'])
            print("#=*35  Qualitative Analysis  35*=#")
            print(summary['qual'])            
        return summary        

    def add(self, data):
        pass

    def remove(self, name):
        pass

    def replace_string(self, pattern, replace, columns=None, regex=True):
        """Regex capable, string replace method for DataSet objects.
        
        Parameters
        ----------
        pattern : str
            A (regex) pattern to find in the DataSet or designated columns.
        replace : str
            A string sequence to replace the pattern
        columns : array-like (Optional)
            List of columns to which the replacement should be applied.
        regex : Bool
            Indicates whether the pattern and replacement are valid regex.

        """
        if columns:
            self._df[columns] = self._df[columns].replace({pattern:replace}, regex=regex)
        else:
            self._df = self._df.replace({pattern:replace}, regex=regex)


    def import_data(self, filename, columns=None):
        """Reads the data from filename and appends it to the dataframe member."""
        f = File()
        df = f.read(filename, columns=columns)        
        self._df = pd.concat([self._df, df], axis=0, sort=False)                
        return self

    def export_data(self, filename):
        """Writes the data to the location designated by the filename."""        
        f = File()
        f.write(filename, self._df)
        return self

    def get_data(self, attribute=None):
        """Method to return all data or one, or more attributes.

        Parameters
        ----------
        attribute : str or list (Optional)
            The attribute or attributes to retrieve

        Returns
        -------
        DataFrame or Series
        
        """
        if attribute is not None:
            return self._df[attribute]
        return self._df

from .constants import DTYPES