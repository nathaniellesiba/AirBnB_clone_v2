#!/usr/bin/python3
"""the module defines a base class for all models"""
import uuid
from datetime import datetime


class BaseModel:
    """Defines common attributes and methods for other classes"""

    def __init__(self, *args, **kwargs):
        """Initialize instance attributes"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
        else:
            kwargs_date = strftime('%y-%m-%dT%H%M%S.%f')
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     kwargs_date)
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     kwargs_date)
            del kwargs['__class__']
            self.__dict__.update(kwargs)


    def __str__(self):
        """Return a string representation of the instance"""
        return "[{}] ({}) {}".format(cls,self.id, self.__dict__)

    def save(self):
        """Update public instance attr updated_at with current datetime"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save

    def to_dict(self):
        """Return dictionary containing all keys/values
        of __dict__ of the instance"""
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict
