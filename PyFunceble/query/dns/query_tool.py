"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides an interface for the query.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2021 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import copy
import functools
import ipaddress
import random
import socket
import time
from typing import Dict, List, Optional, Union

import dns.exception
import dns.message
import dns.name
import dns.query
import dns.rdataclass
import dns.rdatatype

import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.helpers.list import ListHelper
from PyFunceble.query.dns.nameserver import Nameservers
from PyFunceble.query.record.dns import DNSQueryToolRecord


class DNSQueryTool:
    """
    Provides our query tool.
    """

    # pylint: disable=too-many-public-methods

    STD_PROTOCOL: str = "UDP"
    STD_TIMEOUT: float = 5.0
    STD_FOLLOW_NAMESERVER_ORDER: bool = True
    STD_TRUST_SERVER: bool = False

    SUPPORTED_PROTOCOL: List[str] = ["TCP", "UDP", "HTTPS", "TLS"]
    BREAKOFF: float = 0.2

    value2rdata_type: Dict[int, str] = {
        x.value: x.name for x in dns.rdatatype.RdataType
    }
    rdata_type2value: Dict[str, int] = {
        x.name: x.value for x in dns.rdatatype.RdataType
    }

    nameservers: Nameservers = Nameservers()
    _query_record_type: int = dns.rdatatype.RdataType.ANY

    _subject: Optional[str] = None
    _follow_nameserver_order: bool = True
    _preferred_protocol: str = "UDP"
    _query_timeout: float = 5.0
    _trust_server: bool = False

    dns_name: Optional[str] = None

    query_message: Optional[dns.message.QueryMessage] = None
    lookup_record: Optional[DNSQueryToolRecord] = None

    def __init__(
        self,
        *,
        nameservers: Optional[List[str]] = None,
        follow_nameserver_order: Optional[bool] = None,
        preferred_protocol: Optional[str] = None,
        trust_server: Optional[bool] = None,
    ) -> None:
        if nameservers is not None:
            self.nameservers.set_nameservers(nameservers)
        else:  # pragma: no cover ## I'm not playing with system resolver.
            self.nameservers.guess_and_set_nameservers()

        if preferred_protocol is not None:
            self.preferred_protocol = preferred_protocol
        else:
            self.guess_and_set_preferred_protocol()

        if follow_nameserver_order is not None:
            self.follow_nameserver_order = follow_nameserver_order
        else:
            self.guess_and_set_follow_nameserver_order()

        if trust_server is not None:
            self.trust_server = trust_server
        else:
            self.guess_and_set_trust_server()

    def prepare_query(func):  # pylint: disable=no-self-argument
        """
        Prepare the query after running the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)  # pylint: disable=not-callable

            if self.subject and self.query_record_type:
                self.dns_name = self.get_dns_name_from_subject_and_query_type()

                if self.dns_name:
                    self.query_message = dns.message.make_query(
                        self.dns_name, self.query_record_type
                    )
                else:
                    self.query_message = None

            return result

        return wrapper

    def update_lookup_record(func):  # pylint: disable=no-self-argument
        """
        Ensures that a clean record is generated after the execution of
        the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)  # pylint: disable=not-callable

            if self.lookup_record is None or self.subject != self.lookup_record.subject:
                self.lookup_record = DNSQueryToolRecord()
                self.lookup_record.subject = self.subject

            if self.dns_name != self.lookup_record.dns_name:
                self.lookup_record.dns_name = self.dns_name

            if (
                self.get_human_query_record_type()
                != self.lookup_record.query_record_type
            ):
                self.lookup_record.query_record_type = (
                    self.get_human_query_record_type()
                )

            if (
                self.follow_nameserver_order
                != self.lookup_record.follow_nameserver_order
            ):
                self.lookup_record.follow_nameserver_order = (
                    self.follow_nameserver_order
                )

            if self.query_timeout != self.lookup_record.query_timeout:
                self.lookup_record.query_timeout = self.query_timeout

            if self.preferred_protocol != self.lookup_record.preferred_protocol:
                self.lookup_record.preferred_protocol = self.preferred_protocol

            return result

        return wrapper

    def ensure_subject_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the subject to work with is given before running the
        decorated method.

        :raise TypeError:
            If :code:`self.subject` is not a :py:class:`str`.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not isinstance(self.subject, str):
                raise TypeError(
                    f"<self.subject> should be {str}, {type(self.subject)} given."
                )

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def update_lookup_record_response(func):  # pylint: disable=no-self-argument
        """
        Ensures that the response of the decorated method is set as response
        in our record.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)  # pylint: disable=not-callable

            if result != self.lookup_record.response:
                self.lookup_record.response = result

            return result

        return wrapper

    def ignore_if_query_message_is_missing(func):  # pylint: disable=no-self-argument
        """
        Ignores the call to the decorated method if the query message is
        missing. Otherwise, return an empty list.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.query_message:
                return func(self, *args, **kwargs)  # pylint: disable=not-callable
            return []  # pragma: no cover ## Safety

        return wrapper

    @ensure_subject_is_given
    def get_dns_name_from_subject_and_query_type(self):
        """
        Provides the dns name based on the current subject and query type.
        """

        try:
            if self.get_human_query_record_type().lower() == "ptr":
                try:
                    return dns.name.from_text(
                        ipaddress.ip_address(self.subject).reverse_pointer
                    )
                except ValueError:
                    return dns.name.from_text(self.subject)
            return dns.name.from_text(self.subject)
        except (dns.name.LabelTooLong, dns.name.EmptyLabel):
            return None

    @property
    def subject(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_subject` attribute.
        """

        return self._subject

    @subject.setter
    @prepare_query
    @update_lookup_record
    def subject(self, value: str) -> None:
        """
        Sets the subject to work with.

        :param value:
            The subject to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._subject = value

    def set_subject(self, value: str) -> "DNSQueryTool":
        """
        Sets the subject to work with.

        :param value:
            The subject to set.
        """

        self.subject = value

        return self

    def set_nameservers(
        self, value: List[str]
    ) -> "DNSQueryTool":  # pragma: no cover ## Underlying already tested.
        """
        Sets the nameservers to work with.

        :raise TypeError:
            When the given :code:`value` is not a list of :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        self.nameservers.set_nameservers(value)

    @property
    def follow_nameserver_order(self) -> bool:
        """
        Provides the current state of the :code:`_follow_nameserver_order`
        attribute.
        """

        return self._follow_nameserver_order

    @follow_nameserver_order.setter
    @update_lookup_record
    def follow_nameserver_order(self, value: bool) -> None:
        """
        Updates the :code:`follow_nameserver_order` variable.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._follow_nameserver_order = value

    def set_follow_nameserver_order(self, value: bool) -> "DNSQueryTool":
        """
        Updates the :code:`follow_nameserver_order` variable.

        :param value:
            The value to set.
        """

        self.follow_nameserver_order = value

        return self

    @property
    def query_record_type(self) -> int:
        """
        Provides the current state of the :code:`_query_record_type` attribute.
        """

        return self._query_record_type

    @query_record_type.setter
    @prepare_query
    @update_lookup_record
    def query_record_type(self, value: Union[str, int]) -> None:
        """
        Sets the DNS record type to query.

        :param value:
            The value to set. It can be the human version (e.g AAAA) or an
            integer as registered in the :code:`value2rdata_type` attribute.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str` nor
            :py:class:`int`.
        :raise ValueError:
            When the given :code:`value` is unknown or unsupported.
        """

        if not isinstance(value, (str, int)):
            raise TypeError(f"<value> should be {int} or {str}, {type(value)} given.")

        if value in self.rdata_type2value:
            self._query_record_type = self.rdata_type2value[value]
        elif value in self.value2rdata_type:
            self._query_record_type = value
        else:
            raise ValueError(f"<value> ({value!r}) is unknown or unsupported.")

    def set_query_record_type(self, value: Union[str, int]) -> "DNSQueryTool":
        """
        Sets the DNS record type to query.

        :param value:
            The value to set. It can be the human version (e.g AAAA) or an
            integer as registered in the :code:`value2rdata_type` attribute.
        """

        self.query_record_type = value

        return self

    def get_human_query_record_type(self) -> str:
        """
        Provides the currently set record type.
        """

        return self.value2rdata_type[self.query_record_type]

    @property
    def query_timeout(self) -> float:
        """
        Provides the current state of the :code:`_query_timeout` attribute.
        """

        return self._query_timeout

    @query_timeout.setter
    @update_lookup_record
    def query_timeout(self, value: Union[int, float]) -> None:
        """
        Sets the timeout to apply.

        :param value:
            The timeout to apply.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`float`
            nor :py:class.`int`.
        """

        if not isinstance(value, (float, int)):
            raise TypeError(f"<value> should be {float} or {int}, {type(value)} given.")

        self._query_timeout = float(value)

    def set_timeout(self, value: Union[int, float]) -> "DNSQueryTool":
        """
        Sets the timeout to apply.

        :param value:
            The timeout to apply.
        """

        self.query_timeout = value

        return self

    @property
    def trust_server(self) -> Optional[bool]:
        """
        Provides the current state of the :code:`trust_server` attribute.
        """

        return self._trust_server

    @trust_server.setter
    def trust_server(self, value: bool) -> None:
        """
        Sets the value to apply.

        :param value:
            The value to apply.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._trust_server = value

    def set_trust_server(self, value: bool) -> "DNSQueryTool":
        """
        Sets the value to apply.

        :param value:
            The value to apply.
        """

        self.trust_server = value

        return self

    def guess_and_set_timeout(self) -> "DNSQueryTool":
        """
        Try to guess and set the timeout.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            if PyFunceble.storage.CONFIGURATION.lookup.timeout:
                self.query_timeout = PyFunceble.storage.CONFIGURATION.lookup.timeout
            else:
                self.query_timeout = self.STD_TIMEOUT
        else:
            self.query_timeout = self.STD_TIMEOUT

        return self

    @property
    def preferred_protocol(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_preferred_protocol` attribute.
        """

        return self._preferred_protocol

    @preferred_protocol.setter
    def preferred_protocol(self, value: str) -> None:
        """
        Sets the preferred protocol.

        :param value:
            The protocol to use.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is unknown or unsupported.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        value = value.upper()

        if value not in self.SUPPORTED_PROTOCOL:
            raise ValueError(
                f"<value> {value!r} is unknown or unsupported "
                f"(supported: {self.SUPPORTED_PROTOCOL!r})."
            )

        self._preferred_protocol = self.nameservers.protocol = value

    def set_preferred_protocol(self, value: str) -> "DNSQueryTool":
        """
        Sets the preferred protocol.

        :param value:
            The protocol to use.
        """

        self.preferred_protocol = value

        return self

    def guess_and_set_preferred_protocol(self) -> "DNSQueryTool":
        """
        Try to guess and set the preferred procol.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            if isinstance(PyFunceble.storage.CONFIGURATION.dns.protocol, str):
                self.preferred_protocol = PyFunceble.storage.CONFIGURATION.dns.protocol
            else:
                self.preferred_protocol = self.STD_PROTOCOL
        else:
            self.preferred_protocol = self.STD_PROTOCOL

        return self

    def guess_and_set_follow_nameserver_order(self) -> "DNSQueryTool":
        """
        Try to guess and authorize the mix of the nameserver before each
        query.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            if isinstance(
                PyFunceble.storage.CONFIGURATION.dns.follow_server_order, bool
            ):
                self.follow_nameserver_order = (
                    PyFunceble.storage.CONFIGURATION.dns.follow_server_order
                )
            else:
                self.follow_nameserver_order = self.STD_FOLLOW_NAMESERVER_ORDER
        else:
            self.follow_nameserver_order = self.STD_FOLLOW_NAMESERVER_ORDER

        return self

    def guess_and_set_trust_server(self) -> "DNSQueryTool":
        """
        Try to guess and set the trust flag.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            if isinstance(PyFunceble.storage.CONFIGURATION.dns.trust_server, bool):
                self.trust_server = PyFunceble.storage.CONFIGURATION.dns.trust_server
            else:
                self.trust_server = self.STD_TRUST_SERVER
        else:
            self.trust_server = self.STD_TRUST_SERVER

        return self

    def guess_all_settings(
        self,
    ) -> "DNSQueryTool":  # pragma: no cover ## Method themselves are more important
        """
        Try to guess all settings.
        """

        to_ignore = ["guess_all_settings"]

        for method in dir(self):
            if method in to_ignore or not method.startswith("guess_"):
                continue

            getattr(self, method)()

        return self

    def get_lookup_record(
        self,
    ) -> Optional[DNSQueryToolRecord]:
        """
        Provides the current query record.
        """

        return self.lookup_record

    def _get_result_from_response(
        self, response: dns.message.Message
    ) -> List[str]:  # pragma: no cover ## This just reads upstream result
        """
        Given a response, we return the best possible result.
        """

        result = []

        rrset = response.get_rrset(
            response.answer,
            self.dns_name,
            dns.rdataclass.RdataClass.IN,
            self.query_record_type,
        )

        if rrset:
            result.extend([x.to_text() for x in rrset])

        PyFunceble.facility.Logger.debug("Result from response:\r%r", result)

        return result

    def _mix_order(
        self, data: Union[dict, List[str]]
    ) -> Union[dict, List[str]]:  # pragma: no cover ## Just a shuffle :-)
        """
        Given a dataset, we mix its order.
        """

        dataset = copy.deepcopy(data)

        if not self.follow_nameserver_order:
            if isinstance(dataset, list):
                random.shuffle(dataset)

                return dataset

            if isinstance(dataset, dict):
                temp = list(dataset.items())
                random.shuffle(temp)

                return dict(temp)

        PyFunceble.facility.Logger.debug("Mixed data:\n%r", dataset)
        return dataset

    @ensure_subject_is_given
    @ignore_if_query_message_is_missing
    @update_lookup_record_response
    def tcp(
        self,
    ) -> Optional[List[str]]:
        """
        Request the chosen record through the TCP protocol.
        """

        self.lookup_record.used_protocol = "TCP"

        result = []

        for nameserver, port in self._mix_order(
            self.nameservers.get_nameserver_ports()
        ).items():
            PyFunceble.facility.Logger.debug(
                "Started to query information of %r from %r", self.subject, nameserver
            )

            try:
                response = dns.query.tcp(
                    self.query_message,
                    nameserver,
                    port=port,
                    timeout=self.query_timeout,
                )

                local_result = self._get_result_from_response(response)

                if local_result:
                    result.extend(local_result)

                    self.lookup_record.nameserver = nameserver
                    self.lookup_record.port = port

                    PyFunceble.facility.Logger.debug(
                        "Successfully queried information of %r from %r.",
                        self.subject,
                        nameserver,
                    )

                    if not self.trust_server:  # pragma: no cover: Per case.
                        break
                if self.trust_server:  # pragma: no cover: Per case.
                    break
            except (dns.exception.Timeout, socket.error):
                # Example: Resource temporarily unavailable.
                pass
            except dns.query.UnexpectedSource:
                # Example: got a response from XXX instead of XXX.
                pass
            except ValueError:
                # Example: Input is malformed.
                break

            PyFunceble.facility.Logger.debug(
                "Unsuccessfully queried information of %r from %r. Sleeping %fs.",
                self.subject,
                nameserver,
                self.BREAKOFF,
            )

            time.sleep(self.BREAKOFF)

        return ListHelper(result).remove_duplicates().subject

    @ensure_subject_is_given
    @ignore_if_query_message_is_missing
    @update_lookup_record_response
    def udp(
        self,
    ) -> Optional[List[str]]:
        """
        Request the chosen record through the UTP protocol.
        """

        self.lookup_record.used_protocol = "UDP"

        result = []

        for nameserver, port in self._mix_order(
            self.nameservers.get_nameserver_ports()
        ).items():
            PyFunceble.facility.Logger.debug(
                "Started to query information of %r from %r", self.subject, nameserver
            )

            try:
                response = dns.query.udp(
                    self.query_message,
                    nameserver,
                    port=port,
                    timeout=self.query_timeout,
                )

                local_result = self._get_result_from_response(response)

                if local_result:
                    result.extend(local_result)

                    self.lookup_record.nameserver = nameserver
                    self.lookup_record.port = port

                    PyFunceble.facility.Logger.debug(
                        "Successfully queried information of %r from %r.",
                        self.subject,
                        nameserver,
                    )

                    if not self.trust_server:  # pragma: no cover: Per case.
                        break
                if self.trust_server:  # pragma: no cover: Per case.
                    break
            except (dns.exception.Timeout, socket.error):
                # Example: Resource temporarily unavailable.
                pass
            except dns.query.UnexpectedSource:
                # Example: got a response from XXX instead of XXX.
                pass
            except ValueError:
                # Example: Input is malformed.
                break

            PyFunceble.facility.Logger.debug(
                "Unsuccessfully queried information of %r from %r. Sleeping %fs.",
                self.subject,
                nameserver,
                self.BREAKOFF,
            )

            time.sleep(self.BREAKOFF)

        return ListHelper(result).remove_duplicates().subject

    @ensure_subject_is_given
    @ignore_if_query_message_is_missing
    @update_lookup_record_response
    def https(
        self,
    ) -> Optional[List[str]]:
        """
        Request the chosen record through the https protocol.
        """

        self.lookup_record.used_protocol = "HTTPS"

        result = []

        for nameserver in self._mix_order(self.nameservers.get_nameservers()):
            PyFunceble.facility.Logger.debug(
                "Started to query information of %r from %r", self.subject, nameserver
            )

            try:
                response = dns.query.https(
                    self.query_message, nameserver, timeout=self.query_timeout
                )

                local_result = self._get_result_from_response(response)

                if local_result:
                    result.extend(local_result)

                    self.lookup_record.nameserver = nameserver

                    PyFunceble.facility.Logger.debug(
                        "Successfully queried information of %r from %r.",
                        self.subject,
                        nameserver,
                    )

                    if not self.trust_server:  # pragma: no cover: Per case.
                        break
                if self.trust_server:  # pragma: no cover: Per case.
                    break
            except (dns.exception.Timeout, socket.error):
                # Example: Resource temporarily unavailable.
                pass
            except dns.query.UnexpectedSource:
                # Example: got a response from XXX instead of XXX.
                pass
            except ValueError:
                # Example: Input is malformed.
                break

            PyFunceble.facility.Logger.debug(
                "Unsuccessfully queried information of %r from %r. Sleeping %fs.",
                self.subject,
                nameserver,
                self.BREAKOFF,
            )

            time.sleep(self.BREAKOFF)

        return ListHelper(result).remove_duplicates().subject

    @ensure_subject_is_given
    @ignore_if_query_message_is_missing
    @update_lookup_record_response
    def tls(
        self,
    ) -> Optional[List[str]]:
        """
        Request the chosen record through the TLS protocol.
        """

        self.lookup_record.used_protocol = "TLS"

        result = []

        for nameserver, port in self._mix_order(
            self.nameservers.get_nameserver_ports()
        ).items():
            PyFunceble.facility.Logger.debug(
                "Started to query information of %r from %r", self.subject, nameserver
            )

            if port == 53:
                # Default port for nameserver class is 53. So we ensure we
                # overwrite with our own default.
                port = 853

            try:
                response = dns.query.tls(
                    self.query_message,
                    nameserver,
                    port=port,
                    timeout=self.query_timeout,
                )

                local_result = self._get_result_from_response(response)

                if local_result:
                    result.extend(local_result)

                    self.lookup_record.nameserver = nameserver
                    self.lookup_record.port = port

                    PyFunceble.facility.Logger.debug(
                        "Successfully queried information of %r from %r.",
                        self.subject,
                        nameserver,
                    )

                    if not self.trust_server:  # pragma: no cover: Per case.
                        break
                if self.trust_server:  # pragma: no cover: Per case.
                    break
            except (dns.exception.Timeout, socket.error):
                # Example: Resource temporarily unavailable.
                pass
            except dns.query.UnexpectedSource:
                # Example: got a response from XXX instead of XXX.
                pass
            except ValueError:
                # Example: Input is malformed.
                break

            PyFunceble.facility.Logger.debug(
                "Unsuccessfully queried information of %r from %r. Sleeping %fs.",
                self.subject,
                nameserver,
                self.BREAKOFF,
            )

            time.sleep(self.BREAKOFF)

        return ListHelper(result).remove_duplicates().subject

    def query(
        self,
    ) -> Optional[List[str]]:
        """
        Process the query based on the preferred protocol.
        """

        return getattr(self, self.preferred_protocol.lower())()
