class Parser:

    """
    Parser Class
    See main Parser.parse(str, Any) method
    See Parser.clean(str, Any) method
    """
    def parse(self, filename:str, data):
        """
        Interface which serves as a unifier to extracting data from the datafiles to the relevant object
        It is overridden by the implementing class
        The method adds the requirement of a filename, which must be in a list returned by the Filenames Class.
        It also accepts data, which SHOULD be a (or collection of) elements from the filename
        This serves as an "indicator" for what parsing policy to apply on the data, and is useful in types which parse data from more then one file
        This method is normally overridden by Atomic classes (not composed of other Atomic classes), but it is not necessary
        :param: filename: The filename from which the class implements from
        :param: data: The data in the filename which is parsed
        """
        pass

    @staticmethod
    def clean(result:str):
        """
        Convenience method to "clean" the inputted string
        The result, a data cell in the datafile, should either be empty or a number
        This cleans it, returning 0 if empty, or the most specific type it possesses
        :param result: The string containing the cell value
        :return: The cleaned result
        """
        if result == '':
            return 0
        # assert isinstance(result, int) or isinstance(result, float)
        temporary_float = float(result) # Must be either float or integer
        temporary_int = int(temporary_float) # Integer version
        if temporary_int == temporary_float:
            return temporary_int # Integer, can return it
        return temporary_float # Otherwise must be a float
