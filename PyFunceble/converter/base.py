from PyFunceble.exceptions import NoConversionMade


class ConverterBase:  # pragma: no cover
    def __init__(self, data_to_convert):
        self.data_to_convert = data_to_convert

    def get_converted(self):
        """
        Provides the converted data.
        """

        if hasattr(self, "converted_data"):
            # pylint: disable=no-member
            return self.converted_data

        raise NoConversionMade(self.data_to_convert)
