from PyFunceble.exceptions import NoExtractionMade, WrongParameterType


class ExtractorBase:  # pragma: no cover
    def __init__(self, data):
        if not isinstance(data, str):
            raise WrongParameterType(
                f"<data> ({data}) should be {str}, {type(data)} given."
            )

        self.data = data

    def get_extracted(self):
        """
        Provides the converted data.
        """

        if hasattr(self, "extracted_data"):
            # pylint: disable=no-member
            return self.extracted_data

        raise NoExtractionMade()
