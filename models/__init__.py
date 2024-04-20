#!/usr/bin/python3
"""module to satisfy object of class storage"""
from models.engine.file_storage import FileStorage
"""Import the FileStorage class
from the filestorage module"""

storage = FileStorage()
storage.reload()
