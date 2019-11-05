from datetime import timedelta, timezone


class TZ:
    """
    Provides a timezone.

    :param str sign:
        The sign to apply. Should be :code:`+` or :code:`-`.
    :param int days:
        The number of days from UTC.
    :param int seconds:
        The number of seconds from UTC.
    :param int microseconds:
        The number of microseconds from UTC.
    :param int milliseconds:
        The number of days from UTC.
    :param int minutes:
        The number of minutes from UTC.
    :param int hours:
        The number of hours from UTC.
    :param int weeks:
        The number of weeks from UTC.
    """

    def __init__(
        self,
        sign="+",
        days=0,
        seconds=0,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0,
    ):
        if sign == "+":
            self.sign = 1
        else:  # pragma: no cover
            self.sign = -1

        self.timedelda = timedelta(
            days=days,
            seconds=seconds,
            microseconds=microseconds,
            milliseconds=milliseconds,
            minutes=minutes,
            hours=hours,
            weeks=weeks,
        )

    def get(self):
        """
        Provides the timezone itself.

        :rtype: timezone
        """

        return timezone(self.sign * self.timedelda)
