class Driver(object):
    """Base class for all instrument drivers"""
    def __init__(self, resource):
        self.resource = resource

