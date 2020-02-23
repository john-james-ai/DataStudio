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
# URL     : https://github.com/decisionscients/datastudio                     #
# --------------------------------------------------------------------------- #
# Created       : Saturday, February 15th 2020, 9:48:56 pm                    #
# Last Modified : Monday, February 17th 2020, 8:58:23 pm                      #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
""" Module defines the DataStudio data layer.

There are three main types of classes in this module.

    * DataSet : Wrapper for a single pandas DataFrame 
    * DataCollection : A collection of DataSet objects.
    * DataStore : Encapsulates behaviors and methods for physical storage.
    * DataSource : An immutable data source. Inherits from DataStore.
    
The DataSet object is the core object in the DataStudio package. It 
encapsulates tabular data stored as a Pandas DataFrame object. The class
also includes behaviors for reading and manipulating the data.

The DataCollection class contains DataSet objects which belong to a logical
group such as a project or experiment. It provides methods for adding,
changing, extracting, serializing and removing DataSet objects. The
DataCollection class also includes methods to create and manage relationships
between DataSet objects in the DataCollection.

The DataStore class encapsulates the data and behaviors responsible
for physical storage of DataSet objects. DataStore classes include:

    * DataStoreFile : Data stored in a file system.
    * DataStoreMySQL : Data and methods to access a MySQL Database. 
    * DataStorePostgreSQL : Data and methods to access a PostgreSQL Database.
    * DataStoreSQLite : Data and methods to access a SQLite Database.
    * DataStoreOracle : Data and methods to access an Oracle Database.

The DataSource class inherits from the DataStore class and represents 
immutable source objects for DataSet objects. There is a DataSource
subclasses corresponding to each DataStore subclass above.       

"""

from abc import ABC, abstractmethod
from collections import OrderedDict
import pandas as pd
from tabulate import tabulate

from datastudio.core.file import FileIO
from datastudio.core.metadata import MetadataRemoteFactory
from datastudio.core.metadata import MetadataRDBMSFactory
from datastudio.core.metadata import MetadataFileFactory
from datastudio.core.metadata import MetadataDataCollectionFactory
# =========================================================================== #
#                              DATASET CLASSES                                #
# =========================================================================== #
# --------------------------------------------------------------------------- #
#                              AbstractDataSet                                #
# --------------------------------------------------------------------------- #
class AbstractDataSet(ABC):
    """Abstract base class for all DataSet classes."""

    def __init__(self, name, **kwargs):
        super(AbstractDataSet, self).__init__(name)        
        self._locked = False
        self._is_collection = False
        self._data = pd.DataFrame

    @property
    def size(self):
        return self.metadata['tech'].get('size')

    @property
    def user(self):
        return self.metadata['admin'].get('user')

    @property
    def created(self):
        return self.metadata['admin'].get('created')

    @property
    def modified(self):
        return self.metadata['admin'].get('modified')    

    @property
    def is_locked(self):
        """ Returns the value of the locked parameter."""
        return self._locked

    def lock(self):
        """ Locks the object, making it immutable."""
        self._locked = True

    def unlock(self):
        """ Unlocks the object."""
        self._locked = False

    @abstractmethod
    def source(self):
        """Loads the data from the datasource object."""
        pass

    @abstractmethod
    def load(self):
        """Loads the data from the datastore object."""
        pass

    @abstractmethod    
    def save(self):
        """ Saves the data in the datastore object."""
        pass    


# --------------------------------------------------------------------------- #
#                                 DataSet                                     #
# --------------------------------------------------------------------------- #
class DataSet(AbstractDataSet):
    """ Encapsulates a single dataset in a pandas DataFrame object."""

    def __init__(self, name, datasource=None, datastore=None):
        super(DataSet, self).__init__(name, datasource=datasource, 
                                            datastore=datastore)
        self._datasource = datasource
        self._datastore = datastore


    @property
    def datasource(self):
        return self._datasource

    @datasource.setter
    def datasource(self, value):
        if isinstance(value, AbstractDataSource):
            self._datasource = value
        else:
            raise TypeError("Not a valid DataSource object.")

    @property
    def datastore(self):
        return self._datastore

    @datastore.setter
    def datastore(self, value):
        if isinstance(value, AbstractDataStore):
            self._datastore = value
        else:
            raise TypeError("Not a valid DataSource object.")


    @property
    def dataframe(self):
        """Returns pandas DataFrame object."""
        return self._data

    #TODO: Revisit the necessity of this exposure
    @dataframe.setter
    def dataframe(self, value):
        """Sets the pandas DataFrame object."""
        if isinstance(value, pd.DataFrame):
            self._data = value
        else:
            raise TypeError("Value must be a pandas DataFrame object.")        
        
    def source(self):
        """Reads the data from the DataSource object. """
        if self._datasource:
            self._data = self._datasource.read()
        else:
            raise Exception("Unable to source. A DataSource has not been designated")

    def load(self):
        """ Reads the data from the DataStore object."""
        if self._datastore:
            self._data = self._datastore.read()
        else:
            raise Exception("Unable to load. A DataStore has not been designated")

    def save(self):
        """ Saves data back to the datasource."""

        if self._datastore:
            self._datastore.write(self._data)
        else:
            raise Exception("Unable to save. A DataStore has not been designated")

# --------------------------------------------------------------------------- #
#                              DataCollection                                 #
# --------------------------------------------------------------------------- #
class DataCollection(AbstractDataSet):
    """ Encapsulates a single dataset in a pandas DataFrame object."""

    def __init__(self, name, entity=None, **kwargs):
        super(DataCollection, self).__init__(name, **kwargs)
        self._filter = None
        self._is_collection = True
        self._collection = OrderedDict()
        if entity:
            key = self._format_key(entity)
            self._collection[key] = entity

        self.metadata = self._build_metadata()

    def _build_metadata(self):
        factory = MetadataDataCollectionFactory(self, self._name)
        factory.create_admin() 
        factory.create_desc() 
        factory.create_tech() 
        factory.create_process() 
        return factory.metadata

    def _format_key(self, entity, name=None):
        if name:
            key = entity.__class__.__name__.lower() + "_" + name
        else:
            key = entity.__class__.__name__.lower() + "_" + entity.name
        return key

    def get_member(self, name):
        """Returns a DataSet or DataCollection object matching the given name."""
        try:
            entity = next( v for k,v in self._collection.items() if name == v.name)
        except KeyError as e:
            print(e)


    def add(self, entity, name=None):
        """Adds a DataSet or DataCollection to the DataCollection object.
        
        This method adds a DataSet or DataCollection to the DataCollection
        object if it doesn't already exist. DataSets and DataCollections
        are stored with keys containing the class and the name of
        the object. If it already exists, an exception is raised.

        Parameters
        ----------
        data : DataSet or DataCollection object.
            The data to be added to the DataCollection.
        name : str Optional
            A human readable name in snake case. 

        Raises
        ------
        Exception if the object already exists in the collection. 
        
        """
        key = self._format_key(entity, name)
        if key in self._collection.keys():
            raise KeyError("Unable to add {name}. The key already exists."\
                .format(name=entity.get('name', "Name is Null")))
        else:
            self._collection[key] = entity

    def change(self, key, entity):
        """Changes the DataSet or DataCollection for a given key.
        
        This method replaces the DataSet or DataCollection object
        for an existing key. If the key does not exist, an exception
        is thrown.

        Parameters
        ----------
        key : str
            The key to change.
        entity : DataSet or DataCollection object.
            The data to be associated with the key.

        Raises
        ------
        Exception if the object does not exists in the collection. 
        
        """
        
        if key not in self._collection.keys():
            raise KeyError("The designated key, '{key}', does not exist."\
                .format(key=key))
        else:
            self._collection[key] = entity
    
    def remove(self, key):
        """Removes the DataSet or DataCollection object at the designated key.
        
        No exception is thrown if the object does not exist. 

        Parameters
        ----------
        key : str
            The key associated with the object to remove.
        
        """
        del self._collection[key]

    def copy(self, entity, name=None):
        """Copies a member DataSet or DataCollection object.

        The new object is assigned a key containing the class and the name.
        If the name is not provided, a key will be created using the 
        class name and the generated UUID.

        Parameters
        ----------
        data : DataSet or DataCollection object
            The object to be copied.
        name : str
            The name to be assigned to the new object.

        """
        key = self._format_key(entity, name=name)
        clone = copy.deepcopy(entity)
        self._add(clone, name)


    #TODO: Create filter capability see https://github.com/swl10/pyslet/blob/b30e9a439f6c0f0e2d01f1ac80986944bed7427b/pyslet/odata2/core.py#L498

    def set_filter(self, filter):
        pass

    def check_filter(self, observation):
        pass

    def apply_filter(self, filter):
        pass

    def set_orderby(self, orderby):
        pass

    def sort_data(self, observations):
        pass

    def source(self, name):
        """Reads the data from the DataSource object. """
        self._data = self._datasource.load()

    def load(self):
        """ Reads the data from the DataStore object."""
        pass

    def save(self):
        """ Saves data back to the datasource."""
        pass

    def lock(self, name=None):
        """Lock all composite members or the member with the matching name.

        Parameters
        ----------
        name : str
            Names are lower case and have the format 'classname_name'.
        """   
        if name:
            entities = next( v for k,v in self._collection.items() if name == v.name)
            for k, v in entities.items():
                v.lock()
        else:
            for k, v in self._collection.items():
                v.lock()

    def unlock(self, name=None):
        """Unlock all composite members or the member with the matching name.

        Parameters
        ----------
        name : str
            Names are lower case and have the format 'classname_name'.
        """         
        if name:
            entities = next( v for k,v in self._collection.items() if name == v.name)
            for k, v in entities.items():
                v.lock()
        else:
            for k, v in self._collection.items():
                v.lock()

    def print_members(self):
        classes = []
        names = []
        locked = []        
        sizes = []
        created = []
        modified = []
        updates = []
        user = []
        for k, v in self._collection.items():
            classes.append(v.__class__.__name__)
            names.append(v.name)
            locked.append(v.is_locked)
            sizes.append(v.metadata.get('technical').get('object_size'))
            created.append(v.metadata.get('administrative').get('created'))
            modified.append(v.metadata.get('administrative').get('modified'))
            updates.append(v.metadata.get('administrative').get('updates'))
            user.append(v.metadata.get('administrative').get('creator'))

        d = {"Class": classes, "Name": names, "Is Locked?": locked, "Size": sizes,
             "Created": created, "Modified": modified, "Updates": updates, 
             "User": user}
        print(tabulate(d, headers="keys"))

# =========================================================================== #
#                            DATA STORE CLASSES                               #
# =========================================================================== #
# --------------------------------------------------------------------------- #
#                           AbstractDataStore                                 #
# --------------------------------------------------------------------------- #
class AbstractDataStore(ABC):
    """Defines the interface for DataStore subclasses.

    Parameters
    ----------
    name : str
        The name of the DataSource object.
    **kwargs : str
        Designates an arbitrary set of parameters required to  access the 
        source.
    
    """

    def __init__(self, name, path):        
        self._name = name        
        self._path = path        
        self._locked = False
        self._is_collection = False

    @property
    def name(self):
        """Returns the name of the DataSet."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        admin = next( v for k,v in self._metadata.items() if k.startswith('admin'))
        admin.change('name', value)

    @abstractmethod
    def load(self):
        """Loads a DataFrame from the DataStore."""
        pass

    @abstractmethod
    def save(self):
        """Saves a DataFrame object to a given DataStore."""
        pass

# --------------------------------------------------------------------------- #
#                             DataStoreFile                                   #
# --------------------------------------------------------------------------- #
class DataStoreFile(AbstractDataStore):
    """ Loads and saves DataFrame objects in various file formats.
    
    The class provides input and output behavior for various tabular file
    formats such as .csv, .csv.gz, and Excel.

    Parameters
    ----------
    path : str
        The relative path for the file
    """

    def __init__(self, name, path):
        super(DataStoreFile, self).__init__(name, path)                
        self._io = FileIO()
        self._path = path
        self.metadata = self._build_metadata()

    def _build_metadata(self):
        factory = MetadataFileFactory(self, self._name, path=self._path)
        factory.create_admin() 
        factory.create_desc() 
        factory.create_tech() 
        factory.create_process() 
        return factory.metadata        

    def load(self):
        """ Loads data from designated path and returns as DataFrame."""
        return self._io.read(self._path)
    
    def save(self, data):
        """ Saves data to the designated path.

        Parameters
        ----------
        data : pd.DataFrame
            Contains the data to saved.

        """
        self._io.write(data)


# =========================================================================== #
#                            DATA SOURCE CLASSES                              #
# =========================================================================== #
# --------------------------------------------------------------------------- #
#                           AbstractDataSource                                #
# --------------------------------------------------------------------------- #
class AbstractDataSource(ABC):
    """Defines the interface for DataSource subclasses.

    Parameters
    ----------
    name : str
        The name of the DataSource object.
    **kwargs : str
        Designates an arbitrary set of parameters required to  access the 
        source.
    
    """

    def __init__(self, name, **kwargs):        
        self._name = name        
        self._locked = False
        self._is_collection = False

    @property
    def name(self):
        """Returns the name of the DataSet."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        admin = next( v for k,v in self._metadata.items() if k.startswith('admin'))
        admin.change('name', value)

    @abstractmethod
    def load(self):
        """Loads a DataFrame from the DataSource."""
        pass

# --------------------------------------------------------------------------- #
#                             DataSourceFile                                  #
# --------------------------------------------------------------------------- #
class DataSourceFile(AbstractDataSource):
    """ Loads and saves DataFrame objects in various file formats.
    
    The class provides input and output behavior for various tabular file
    formats such as .csv, .csv.gz, and Excel.

    Parameters
    ----------
    path : str
        The relative path for the file
    """

    def __init__(self, name, **kwargs):
        super(DataSourceFile, self).__init__(name, **kwargs)                
        self._io = FileIO()
        self._path = next(v for (k,v) in kwargs.items() if 'path' in k)
        self.metadata = self._build_metadata()

    def _build_metadata(self):
        factory = MetadataFileFactory(self, self._name, path=self._path)
        factory.create_admin() 
        factory.create_desc() 
        factory.create_tech() 
        factory.create_process() 
        return factory.metadata          

    def load(self):
        """ Loads data from designated path and returns as DataFrame."""
        return self._io.read(self._path)
    

    
