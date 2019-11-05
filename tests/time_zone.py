from datetime import timedelta, timezone


class TZ:
    """
    Provides a timezone

    :param int offset: The offset in seconds.
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
        """

        return timezone(self.sign * self.timedelda)
