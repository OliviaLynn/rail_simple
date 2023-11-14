"""An example module containing simplistic functions."""
from rail.creation.engine import Modeler, Creator


class SimpleModeler(Modeler):
    name = "SimpleModeler"

    def __init__(self, args, comm=None):
        """Initialize Modeler"""
        super().__init__(self, args, comm=None)


class SimpleCreator(Creator):
    name = "SimpleCreator"

    def __init__(self, args, comm=None):
        """Initialize Simple Creator"""
        super().__init__(self, args, comm=None)