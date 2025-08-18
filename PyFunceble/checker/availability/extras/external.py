"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the extra rules handler based on some DNS records.

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


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024, 2025 Nissar Chababy

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

# pylint: disable=line-too-long

from typing import Optional

from PyFunceble.checker.availability.extras.base import ExtraRuleHandlerBase
from PyFunceble.checker.availability.status import AvailabilityCheckerStatus


class ExternalRulesHandler(ExtraRuleHandlerBase):
    """
    Provides the external rules handler that is used to handle the external
    provided rules.

    Through this handler, end-user can provide their own rules to handle
    the availability status of a subject.

    :param status:
        The previously gathered status.
    :type status:
        :class:`~PyFunceble.checker.availability.status.AvailabilityCheckerStatus`
    """

    rulesets: list = []
    """
    The rulesets to process.

    If you want to switch from the status code, you should provide a dict
    with the following structure:

        {
            "subject_pattern": ".*", // The pattern the subject should match.
            "validation_type": "status_code", // Type of validation (status_code, headers, body, etc.)
            "state_transition": "up", // "up" -> ACTIVE, "down" -> INACTIVE
            "required_status_code": [404], // Status code to match.
        }

    If you want to switch from the headers, you should provide a dict

        {
            "subject_pattern": ".*", // The pattern the subject should match.
            "validation_type": "headers", // Type of validation (status_code, headers, body, etc.)
            "state_transition": "up", // "up" -> ACTIVE, "down" -> INACTIVE
            "required_headers_patterns": { // Required, the headers to match.
                "header_name": ["possible", "values"]
            },
        }

    If you want to switch from the body, you should provide a dict

        {
            "subject_pattern": ".*", // The pattern the subject should match.
            "validation_type": "body", // Type of validation (status_code, headers, body, etc.)
            "state_transition": "up", // "up" -> ACTIVE, "down" -> INACTIVE
            "required_body_patterns": ["regex1", "regex2"] // Required, the body patterns to match.
        }

    If you want to switch from a combination of headers and body, you should provide a dict

        {
            "subject_pattern": ".*", // The pattern the subject should match.
            "validation_type": "headers+body", // Type of validation (status_code, headers, body, etc.)
            "state_transition": "up", // "up" -> ACTIVE, "down" -> INACTIVE
            "required_headers_patterns": { // Required, the headers to match.
                "header_name": ["possible", "values"]
            },
            "required_body_patterns": ["regex1", "regex2"] // Required, the body patterns to match.
        }

    If you want to switch from a combination of all, you should provide a dict

        {
            "subject_pattern": ".*", // The pattern the subject should match.
            "validation_type": "all", // Type of validation (status_code, headers, body, etc.)
            "state_transition": "up", // "up" -> ACTIVE, "down" -> INACTIVE
            "required_status_code": [404], // Optional, Status code to match.
            "required_headers_patterns": { // Optional, the headers to match.
                "header_name": ["possible", "values"]
            },
            "required_body_patterns": ["regex1", "regex2"] // Optional, the body patterns to match.
        }

    """

    def __init__(
        self,
        status: Optional[AvailabilityCheckerStatus] = None,
        *,
        rulesets: list = None
    ) -> None:
        if rulesets is not None:
            self.rulesets = rulesets

        super().__init__(status)

    def switch_from_status_code_rule(self, rule: dict) -> "ExternalRulesHandler":
        """
        Switch from the status code rule.

        :param rule:
            The rule to switch from.
        :type rule: dict
        """

        required_keys = ["validation_type", "required_status_code"]

        if any(x not in rule for x in required_keys):
            return self

        if rule["validation_type"] != "status_code":
            return self

        if all(
            self.status.http_status_code != int(x) for x in rule["required_status_code"]
        ):
            return self

        if rule["state_transition"] == "up":
            return self.switch_to_up()

        if rule["state_transition"] == "down":
            return self.switch_to_down()

        return self

    def switch_from_headers_rule(self, rule: dict) -> "ExternalRulesHandler":
        """
        Switch from the headers rule.

        :param rule:
            The rule to switch from.
        :type rule: dict
        """

        required_keys = ["validation_type", "required_headers_patterns"]

        if any(x not in rule for x in required_keys):
            return self

        if rule["validation_type"] != "headers":
            return self

        if rule["state_transition"] == "up":
            switch_method = self.switch_to_up

        if rule["state_transition"] == "down":
            switch_method = self.switch_to_down

        if "required_headers_patterns" in rule and rule["required_headers_patterns"]:
            # pylint: disable=possibly-used-before-assignment
            self.do_on_header_match(
                self.req_url,
                rule["required_headers_patterns"],
                method=switch_method,
                strict=False,
                allow_redirects=False,
            )

        return self

    def switch_from_body_rule(self, rule: dict) -> "ExternalRulesHandler":
        """
        Switch from the body rule.

        :param rule:
            The rule to switch from.
        :type rule: dict
        """

        required_keys = ["validation_type", "required_body_patterns"]

        if any(x not in rule for x in required_keys):
            return self

        if rule["validation_type"] != "body":
            return self

        if rule["state_transition"] == "up":
            switch_method = self.switch_to_up

        if rule["state_transition"] == "down":
            switch_method = self.switch_to_down

        if "required_body_patterns" in rule and rule["required_body_patterns"]:
            # pylint: disable=possibly-used-before-assignment
            self.do_on_body_match(
                self.req_url,
                rule["required_body_patterns"],
                method=switch_method,
                strict=False,
                allow_redirects=False,
            )

        return self

    def switch_from_all_rule(self, rule: dict) -> "ExternalRulesHandler":
        """
        Switch from the all rule.

        :param rule:
            The rule to switch from.
        :type rule: dict
        """

        required_keys = [
            "validation_type",
        ]

        if any(x not in rule for x in required_keys):
            return self

        if rule["validation_type"] != "all":
            return self

        if rule["state_transition"] == "up":
            switch_method = self.switch_to_up

        if rule["state_transition"] == "down":
            switch_method = self.switch_to_down

        if (
            "required_status_code" in rule
            and rule["required_status_code"]
            and any(
                self.status.http_status_code == int(x)
                for x in rule["required_status_code"]
            )
        ):
            # pylint: disable=possibly-used-before-assignment
            switch_method()

        if "required_headers_patterns" in rule and rule["required_headers_patterns"]:
            self.do_on_header_match(
                self.req_url,
                rule["required_headers_patterns"],
                method=switch_method,
                strict=False,
                allow_redirects=False,
            )

        if "required_body_patterns" in rule and rule["required_body_patterns"]:
            self.do_on_body_match(
                self.req_url,
                rule["required_body_patterns"],
                method=switch_method,
                strict=False,
                allow_redirects=False,
            )

        return self

    @ExtraRuleHandlerBase.ensure_status_is_given
    @ExtraRuleHandlerBase.setup_status_before
    @ExtraRuleHandlerBase.setup_status_after
    def start(self) -> "ExternalRulesHandler":
        """
        Process the check and handling of the external rules for the given subject.
        """

        required_keys = ["subject_pattern", "validation_type", "state_transition"]

        for rule in self.rulesets:
            if any(x not in rule for x in required_keys):
                continue

            if not self.regex_helper.set_regex(rule["subject_pattern"]).match(
                self.status.netloc, return_match=False
            ):
                continue

            if rule["state_transition"] not in ["up", "down"]:
                continue

            if self.status.status_after_extra_rules:
                # We already switched the status.
                break

            if rule["validation_type"] == "status_code":
                self.switch_from_status_code_rule(rule)
            elif rule["validation_type"] == "headers":
                self.switch_from_headers_rule(rule)
            elif rule["validation_type"] == "body":
                self.switch_from_body_rule(rule)
            elif rule["validation_type"] == "headers+body":
                self.switch_from_headers_rule(rule)
                self.switch_from_body_rule(rule)
            elif rule["validation_type"] == "all":
                self.switch_from_all_rule(rule)

        return self
