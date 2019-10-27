from PyFunceble.exceptions import WrongParameterType

from .base import ConverterBase


class Digit2Digits(ConverterBase):
    """
    Converts a given digit to a 2 digits string.
    """

    def __init__(self, data_to_convert):
        if not isinstance(data_to_convert, str):
            raise WrongParameterType(
                f"<data_to_convert> should be {str}, {type(data_to_convert)} given."
            )

        super().__init__(data_to_convert)

        self.converted_data = str(self.data_to_convert).zfill(2)
