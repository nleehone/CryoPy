class Driver(object):
    """Base class for all instrument drivers"""
    def __init__(self, resource):
        self.resource = resource

    def multi_query(self, query_string):
        """
        Custom query. Can be used to query multiple parameters in one go
        """
        self.resource.write(query_string)
        return [self.resource.read() for i in range(len(query_string.split(";")))]

    def query(self, command):
        return self.resource.query(command)

    def write(self, command):
        return self.resource.write(command)

    """
    Common commands are defined below. Note that not all common commands will be defined by every instrument.
    If you want to make sure the user cannot use a common command on a particular instrument driver
    you must override the method as follows:

    def <command to disable>():
        raise AttributeError("The <command to disable> is not available on this instrument.")
    """

    def identify(self):
        """
        *IDN?
        Queries the device's identification string.

        The string will have the following format:
        manufacturer, model number, serial number, firmware revision level
        """
        return self.query("*IDN?")

    def clear_status(self):
        """
        *CLS
        Clears all event registers and error queue.
        """
        self.write("*CLS")

    def reset(self):
        """
        *RST
        Reset command. Returns the instrument to its default configuration.
        """
        self.write("*RST")

