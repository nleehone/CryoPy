class Driver(object):
    """Base class for all instrument drivers"""
    def __init__(self, resource):
        self.resource = resource

    def query(self, command):
        return self.resource.query(command)

    def write(self, command):
        return self.resource.query(command)
