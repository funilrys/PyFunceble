class List:
    """
    Simplify the list manipulation.

    :param list main: The main list to work with.
    :param bool remove_empty: Process the deletion of empty strings.
    """

    def __init__(self, main, remove_empty=False):
        if remove_empty:
            self.main = [x for x in main if x is None or x]
        else:
            self.main = main

    def format(self):
        """
        Return a well formatted list. Basicaly, it's sort a list and remove duplicate.

        :return: A sorted, without duplicate, list.
        :rtype: list
        """

        try:
            return sorted(list(set(self.main)), key=str.lower)

        except TypeError:  # pragma: no cover
            return self.main

    def custom_format(self, key_method, reverse=False):
        """
        Return a well formatted list. With the key_method as a function/method to format
        the elements before sorting.

        :param key_method:
            A function or method to use to format the
            readed element before sorting.
        :type key_method: function|method

        :param bool reverse: Tell us if we have to reverse the list.

        :return: A sorted list.
        :rtype: list
        """

        try:
            return sorted(list(set(self.main)), key=key_method, reverse=reverse)
        except TypeError:  # pragma: no cover
            return self.main
