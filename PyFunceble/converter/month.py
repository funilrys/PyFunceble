from PyFunceble.exceptions import WrongParameterType

from .base import ConverterBase


class Month(ConverterBase):
    """
    Converts a given month to a unified format.
    """

    # We map the different month and their possible representation.
    months = {
        "jan": [str(1), "01", "Jan", "January"],
        "feb": [str(2), "02", "Feb", "February"],
        "mar": [str(3), "03", "Mar", "March"],
        "apr": [str(4), "04", "Apr", "April"],
        "may": [str(5), "05", "May"],
        "jun": [str(6), "06", "Jun", "June"],
        "jul": [str(7), "07", "Jul", "July"],
        "aug": [str(8), "08", "Aug", "August"],
        "sep": [str(9), "09", "Sep", "September"],
        "oct": [str(10), "Oct", "October"],
        "nov": [str(11), "Nov", "November"],
        "dec": [str(12), "Dec", "December"],
    }

    def __init__(self, data_to_convert):
        if not isinstance(data_to_convert, str):
            raise WrongParameterType(
                f"<data_to_convert> should be {str}, {type(data_to_convert)} given."
            )

        super().__init__(data_to_convert)

        for to_return, possibilities in self.months.items():
            if self.data_to_convert in possibilities:
                self.converted_data = to_return
                break
