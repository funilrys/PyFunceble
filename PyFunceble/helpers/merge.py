class Merge:
    """
    Simplify the merging of dict and list.

    :param main: The main data to work with.
    :type main: str, tuple, bool, int, dict, list, float
    """

    def __init__(self, main):
        self.main = main

    def __list(self, origin, strict=True):
        """
        Process the list merging.

        :param bool strict:
            Activates the strict mode.

        :rtype: list
        """

        result = []

        if strict:
            for index, element in enumerate(self.main):
                try:
                    if isinstance(element, dict) and isinstance(origin[index], dict):
                        result.append(Merge(element).into(origin[index], strict=strict))
                    elif isinstance(element, list) and isinstance(origin[index], list):
                        result.append(Merge(element).into(origin[index], strict=strict))
                    else:
                        result.append(element)
                except IndexError:  # pragma: no cover
                    result.append(element)
        else:
            result = origin

            for element in self.main:
                if element not in result:
                    result.append(element)

        return result

    def __dict(self, origin, strict=True):
        """
        Process the dict merging.

        :param bool strict:
            Activates the strict mode.

        :rtype: dict
        """

        result = {}

        for index, data in self.main.items():
            if index in origin:
                if isinstance(data, dict) and isinstance(origin[index], dict):
                    result[index] = Merge(data).into(origin[index], strict=strict)
                elif isinstance(data, list) and isinstance(origin[index], list):
                    result[index] = Merge(data).into(origin[index], strict=strict)
                else:
                    result[index] = data
            else:
                result[index] = data

        for index, data in origin.items():
            if index not in result:
                result[index] = data

        return result

    def into(self, origin, strict=True):
        """
        Process the mergin.

        :param origin: The original data.
        :param bool strict:
            Activates the strict mode.
        """

        try:
            origin = origin.copy()
        except AttributeError:
            pass

        if isinstance(self.main, list) and isinstance(origin, list):
            return self.__list(origin, strict=strict)

        if isinstance(self.main, dict) and isinstance(origin, dict):
            return self.__dict(origin, strict=strict)

        return self.main  # pragma: no cover
