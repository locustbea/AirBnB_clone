#!/usr/bin/python3
"""BaseModel class module for AirBnB clone console"""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """HBnB BaseModel class for object hierarchy"""

    def __init__(self, *args, **kwargs):
        """Initialises a new BaseModel.

        Args:
            - *args (any): args list (unused)
            - **kwargs (dict): key-value arg pair attributes dict
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, time_format)
                else:
                    self.__dict__[k] = v
        else:
            models.storage.new(self)

    def save(self):
        """Using updated_at to update current datetime"""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Returns BaseModel dict key/ value pair"""
        mydict = self.__dict__.copy()
        mydict["created_at"] = self.created_at.isoformat()
        mydict["updated_at"] = self.updated_at.isoformat()
        mydict["__class__"] = self.__class__.__name__
        return mydict

    def __str__(self):
        """Returns BaseModel instance as string"""
        clname = self.__class__.__name__
        return f"[{clname}] ({self.id}) {self.__dict__}"
