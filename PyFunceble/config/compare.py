"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the configuration comparision interface.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://docs.pyfunceble.com

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import copy
from typing import List, Optional

import PyFunceble.storage
from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.merge import Merge


class ConfigComparison:
    """
    Provides an interface for comparing 2 configuration.
    """

    DELETED_LINKS: List[str] = [
        "config",
        "dir_structure",
        "iana",
        "ipv4_reputation",
        "mariadb",
        "mysql",
        "psl",
        "repo",
        "requirements",
        "user_agents",
        "api_date_format",
        "api_no_referrer",
    ]
    DELETED_CORE: List[str] = [
        "dns_lookup_over_tcp",
        "generate_json",
        "header_printed",
        "iana_whois_server",
        "idna_conversion",
        "logs",
        "maximal_processes",
        "multiprocess_merging_mode",
        "multiprocess",
        "no_http_codes",
        "outputs",
        "shadow_file",
        "status",
        "store_whois_record",
        "unified",
    ]

    OLD_TO_NEW: dict = {
        "adblock": "cli_decoding.adblock",
        "aggressive": "cli_decoding.adblock_aggressive",
        "auto_continue": "cli_testing.autocontinue",
        "command": "cli_testing.ci.command",
        "command_before_end": "cli_testing.ci.end_command",
        "cooldown_time": "cli_testing.cooldown_time",
        "custom_ip": "cli_testing.hosts_ip",
        "days_between_inactive_db_clean": "cli_testing.days_between.db_clean",
        "days_between_db_retest": "cli_testing.days_between.db_retest",
        "db_type": "cli_testing.db_type",
        "debug": "debug.active",
        "dns_server": "dns.server",
        "filter": "cli_testing.file_filter",
        "generate_complements": "cli_testing.complements",
        "generate_hosts": "cli_testing.file_generation.hosts",
        "hierarchical_sorting": "cli_testing.sorting_mode.hierarchical",
        "inactive_database": "cli_testing.inactive_db",
        "less": "cli_testing.display_mode.less",
        "local": "cli_testing.local_network",
        "mining": "cli_testing.mining",
        "no_files": "cli_testing.file_generation.no_file",
        "plain_list_domain": "cli_testing.file_generation.plain",
        "print_dots": "cli_testing.display_mode.dots",
        "quiet": "cli_testing.display_mode.dots",
        "use_reputation_data": "lookup.reputation",
        "reputation": "lookup.reputation",
        "rpz": "cli_decoding.rpz",
        "show_execution_time": "cli_testing.display_mode.execution_time",
        "show_percentage": "cli_testing.display_mode.percentage",
        "simple": "cli_testing.display_mode.simple",
        "syntax": "cli_testing.testing_mode.syntax",
        "timeout": "lookup.timeout",
        "ci": "cli_testing.ci.active",
        "ci_autosave_commit": "cli_testing.ci.commit_message",
        "ci_autosave_final_commit": "cli_testing.ci.end_commit_message",
        "ci_autosave_minutes": "cli_testing.ci.max_exec_minutes",
        "ci_branch": "cli_testing.ci.branch",
        "ci_distribution_branch": "cli_testing.ci.distribution_branch",
        "whois_database": "cli_testing.whois_db",
        "wildcard": "cli_decoding.wildcard",
        "cli_decoding.adblock_aggressive": "cli_decoding.aggressive",
        "lookup.collection": "lookup.platform",
        "collection.push": "platform.push",
        "collection.preferred_status_origin": "platform.preferred_status_origin",
    }

    OLD_TO_NEW_NEGATE: dict = {
        "no_special": "lookup.special",
        "no_whois": "lookup.whois",
        "split": "cli_testing.file_generation.unified_results",
    }

    DELETE_FLATTEN: List[str] = [
        "platform.url_base",
    ]

    NEW_STATUS_CODES: dict = {
        "up": [102, 207, 208, 226, 429],
        "potentially_down": [451],
        "potentially_up": [
            308,
            403,
            418,
            421,
            422,
            423,
            424,
            426,
            428,
            431,
            506,
            507,
            508,
            510,
            511,
        ],
    }

    _local_config: dict = {}
    _upsteam_config: dict = {}

    dict_helper: DictHelper = DictHelper()

    def __init__(
        self,
        *,
        local_config: Optional[dict] = None,
        upstream_config: Optional[dict] = None,
    ) -> None:
        if local_config:
            self.local_config = local_config

        if upstream_config:
            self.upstream_config = upstream_config

    @property
    def local_config(self) -> dict:
        """
        Provides the current state of the :code:`_local_config`.
        """

        return self._local_config

    @local_config.setter
    def local_config(self, value: dict) -> None:
        """
        Sets the local configuration to work with.

        :raise TypeError:
            When :code:`value` is not a :py:class:`dict`.
        """

        if not isinstance(value, dict):
            raise TypeError(f"<value> should be {dict}, {type(value)} given.")

        self._local_config = copy.deepcopy(value)

    def set_local_config(self, value: dict) -> "ConfigComparison":
        """
        Sets the local configuration to work with.
        """

        self.local_config = value

        return self

    @property
    def upstream_config(self) -> dict:
        """
        Provides the current state of the :code:`_upstream_config`.
        """

        return self._upsteam_config

    @upstream_config.setter
    def upstream_config(self, value: dict) -> None:
        """
        Sets the upstram configuration to work with.

        :raise TypeError:
            When :code:`value` is not a :py:class:`dict`
        """

        if not isinstance(value, dict):
            raise TypeError(f"<value> should be {dict}, {type(value)} given.")

        self._upsteam_config = copy.deepcopy(value)

    def set_upstream_config(self, value: dict) -> "ConfigComparison":
        """
        Sets the upstram configuration to work with.
        """

        self.upstream_config = value

        return self

    def is_local_identical(self) -> bool:
        """
        Checks if the local configuration is identical to the upstream one.
        """

        # pylint: disable=too-many-boolean-expressions,too-many-return-statements
        if (
            not self.dict_helper.set_subject(self.local_config).has_same_keys_as(
                self.upstream_config
            )
            or "user_agent" not in self.local_config
            or not isinstance(self.local_config["user_agent"], dict)
            or "active" in self.local_config["http_codes"]
            or "not_found_default" in self.local_config["http_codes"]
            or "self_managed" not in self.local_config["http_codes"]
            or "dns" not in self.local_config
            or "proxy" not in self.local_config
            or "follow_server_order" not in self.local_config["dns"]
            or "trust_server" not in self.local_config["dns"]
            or "platform" not in self.local_config
            or "platform" not in self.local_config["lookup"]
        ):
            return False

        for index in self.local_config:
            if index in self.DELETED_CORE:
                return False

        for index in self.local_config["links"]:
            if index in self.DELETED_LINKS:
                return False

        if "self_managed" in self.local_config["http_codes"] and not bool(
            self.local_config["http_codes"]["self_managed"]
        ):
            if "http_codes" not in self.upstream_config:
                return False

            for index, values in self.local_config["http_codes"]["list"].items():
                if set(self.upstream_config["http_codes"]["list"][index]) != set(
                    values
                ):
                    return False

        if (
            "platform" in self.local_config
            and "url_base" in self.local_config["platform"]
        ):
            return False

        return True

    def get_merged(self) -> dict:
        """
        Provides the merged configuration.
        """

        # pylint: disable=too-many-branches

        if self.is_local_identical():
            return self.local_config

        if not self.local_config:
            return self.upstream_config

        original_local = copy.deepcopy(self.local_config)
        original_upstream = copy.deepcopy(self.upstream_config)

        flatten_original = self.dict_helper.set_subject(original_local).flatten()
        flatten_upstream = self.dict_helper.set_subject(original_upstream).flatten()

        for key, value in self.OLD_TO_NEW.items():
            if key not in flatten_original:
                continue

            if value not in flatten_upstream:  # pragma: no cover ## Safety.
                raise RuntimeError(f"<value> ({value!r}) not found.")

            if "." not in key:
                flatten_original[value] = original_local[key]
            else:
                flatten_original[value] = flatten_original[key]

            del flatten_original[key]

        for key, value in self.OLD_TO_NEW_NEGATE.items():
            if key not in flatten_original:
                continue

            if value not in flatten_upstream:  # pragma: no cover ## Safety.0
                raise RuntimeError(f"<value> ({value!r}) not found.")

            if "." not in key:
                flatten_original[value] = not original_local[key]
            else:
                flatten_original[value] = not flatten_original[key]

            del flatten_original[key]

        for key in self.DELETE_FLATTEN:
            if key in flatten_original:
                del flatten_original[key]

        original_local = self.dict_helper.set_subject(flatten_original).unflatten()
        del flatten_original

        merged = Merge(original_local).into(original_upstream)

        if "dns_lookup_over_tcp" in merged and merged["dns_lookup_over_tcp"]:
            merged["dns"]["protocol"] = "TCP"

        for index in self.DELETED_CORE:
            if index in merged:
                del merged[index]

        for index in self.DELETED_LINKS:
            if index in merged["links"]:
                del merged["links"][index]

        if not bool(merged["http_codes"]["self_managed"]):
            for index, values in PyFunceble.storage.STD_HTTP_CODES.list.items():
                merged["http_codes"]["list"][index] = list(values)

        if merged["cli_testing"]["db_type"] == "json":
            merged["cli_testing"]["db_type"] = "csv"

        if merged["cli_testing"]["cooldown_time"] is None:
            merged["cli_testing"]["cooldown_time"] = self.upstream_config[
                "cli_testing"
            ]["cooldown_time"]

        if "user_agent" not in self.local_config or not isinstance(
            self.local_config["user_agent"], dict
        ):
            merged["user_agent"] = self.upstream_config["user_agent"]

        if "active" in merged["http_codes"]:
            del merged["http_codes"]["active"]

        if "not_found_default" in merged["http_codes"]:
            del merged["http_codes"]["not_found_default"]

        return merged
