import requests

from ..exceptions import NoInternetConnection
from .file import File


class Download:
    """
    Simplification of the downloads.

    :param str url: The url to download.
    :param bool verify_certificate: Allows/Disallows the certificate verification.
    """

    def __init__(self, url, verify_certificate=True):
        if not isinstance(url, str):
            raise TypeError(f"<url> must be {str}, {type(url)} given.")

        if not isinstance(verify_certificate, bool):
            raise TypeError(
                f"<verify_certificate> must be {bool}, {type(verify_certificate)} given."
            )

        self.url = url
        self.certificate_verification = verify_certificate

    def text(self, destination=None):
        """
        Download the body of the given url.

        .. note::
            if :code:`destination` is set to :code:`None`,
            we only return the output.

            Otherwise, we save the output into the given
            destination, but we also return the output.

        :param str destination: The download destination.
        :rtype: str:
        :raise Exception: When the status code is not 200.
        :raise NoInternetConnection: When no connection could be made.
        """

        try:
            req = requests.get(self.url, verify=self.certificate_verification)

            if req.status_code == 200:
                response = req.text

                if destination and isinstance(destination, str):
                    File(destination).write(req.text, overwrite=True)

                return response

            raise Exception(
                f"Unable to download {req.url} (status code: {req.status_code})."
            )
        except requests.exceptions.ConnectionError:
            raise NoInternetConnection()
