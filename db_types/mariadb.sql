-- -- The tool to check the availability or syntax of domain, IP or URL.
-- --
-- ::
--
--
--     ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
--     ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
--     ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
--     ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
--     ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
--     ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝
--
-- This file is part of the PyFunceble project. It provide the MariaDB database structure.
--
-- Author:
--     Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom
--
-- Special thanks:
--     https://pyfunceble.github.io/special-thanks.html
--
-- Contributors:
--     https://pyfunceble.github.io/contributors.html
--
-- Project link:
--     https://github.com/funilrys/PyFunceble
--
-- Project documentation:
--     https://pyfunceble.readthedocs.io/en/master/
--
-- Project homepage:
--     https://pyfunceble.github.io/
--
-- License:
-- ::
--
--
--     Copyright 2017, 2018, 2019, 2020 Nissar Chababy
--
--     Licensed under the Apache License, Version 2.0 (the "License");
--     you may not use this file except in compliance with the License.
--     You may obtain a copy of the License at
--
--         http://www.apache.org/licenses/LICENSE-2.0
--
--     Unless required by applicable law or agreed to in writing, software
--     distributed under the License is distributed on an "AS IS" BASIS,
--     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
--     See the License for the specific language governing permissions and
--     limitations under the License.

CREATE TABLE IF NOT EXISTS pyfunceble_auto_continue (
    id BIGINT(20) PRIMARY KEY AUTO_INCREMENT,
    file_path LONGTEXT NOT NULL,
    subject LONGTEXT NOT NULL,
    status VARCHAR(12) NOT NULL,
    is_complement TINYINT(1) NOT NULL,
    digest VARCHAR(64) NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(digest)
);

DELIMITER ///
CREATE TRIGGER IF NOT EXISTS updatePyFuncebleAutoContinueDates
    BEFORE UPDATE ON pyfunceble_auto_continue FOR EACH ROW
BEGIN
    IF NEW.modified <= OLD.modified THEN
        SET NEW.modified = CURRENT_TIMESTAMP;
    END IF;
END ///
DELIMITER ;

CREATE TABLE IF NOT EXISTS pyfunceble_inactive (
    id BIGINT(20) PRIMARY KEY AUTO_INCREMENT,
    file_path LONGTEXT NOT NULL,
    subject LONGTEXT NOT NULL,
    status VARCHAR(12) NOT NULL,
    digest VARCHAR(64) NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(digest)
);

DELIMITER ///
CREATE TRIGGER IF NOT EXISTS updatePyFuncebleInactiveDates
    BEFORE UPDATE ON pyfunceble_inactive FOR EACH ROW
BEGIN
    IF NEW.modified <= OLD.modified THEN
        SET NEW.modified = CURRENT_TIMESTAMP;
    END IF;
END ///
DELIMITER ;

CREATE TABLE IF NOT EXISTS pyfunceble_mining (
    id BIGINT(20) PRIMARY KEY AUTO_INCREMENT,
    file_path LONGTEXT NOT NULL,
    subject LONGTEXT NOT NULL,
    mined LONGTEXT NOT NULL,
    digest VARCHAR(64) NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(digest)
);

DELIMITER ///
CREATE TRIGGER IF NOT EXISTS updatePyFuncebleMiningDates
    BEFORE UPDATE ON pyfunceble_mining FOR EACH ROW
BEGIN
    IF NEW.modified <= OLD.modified THEN
        SET NEW.modified = CURRENT_TIMESTAMP;
    END IF;
END ///
DELIMITER ;

CREATE TABLE IF NOT EXISTS pyfunceble_whois (
    id BIGINT(20) PRIMARY KEY AUTO_INCREMENT,
    subject LONGTEXT NOT NULL,
    expiration_date VARCHAR(12) NOT NULL,
    expiration_date_epoch INTEGER(11) NOT NULL,
    state VARCHAR(12) NOT NULL,
    record LONGTEXT NOT NULL,
    digest VARCHAR(64) NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(digest)
);

DELIMITER ///
CREATE TRIGGER IF NOT EXISTS updatePyFuncebleWhoisDates
    BEFORE UPDATE ON pyfunceble_whois FOR EACH ROW
BEGIN
    IF NEW.modified <= OLD.modified THEN
        SET NEW.modified = CURRENT_TIMESTAMP;
    END IF;
END ///
DELIMITER ;

CREATE TABLE IF NOT EXISTS pyfunceble_tested (
    id BIGINT(20) PRIMARY KEY AUTO_INCREMENT,
    digest VARCHAR(64) NOT NULL,
    tested LONGTEXT NOT NULL,
    file_path LONGTEXT DEFAULT NULL,
    _status LONGTEXT DEFAULT NULL,
    status LONGTEXT DEFAULT NULL,
    _status_source LONGTEXT DEFAULT NULL,
    status_source LONGTEXT DEFAULT NULL,
    domain_syntax_validation TINYINT(1) DEFAULT NULL,
    expiration_date VARCHAR(12) DEFAULT NULL,
    http_status_code INT(4) DEFAULT NULL,
    ipv4_range_syntax_validation TINYINT(1) DEFAULT NULL,
    ipv4_syntax_validation TINYINT(1) DEFAULT NULL,
    subdomain_syntax_validation TINYINT(1) DEFAULT NULL,
    url_syntax_validation TINYINT(1) DEFAULT NULL,
    whois_server LONGTEXT DEFAULT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(digest)
);

DELIMITER ///
CREATE TRIGGER IF NOT EXISTS updatePyFuncebleTestedDates
    BEFORE UPDATE ON pyfunceble_tested FOR EACH ROW
BEGIN
    IF NEW.modified <= OLD.modified THEN
        SET NEW.modified = CURRENT_TIMESTAMP;
    END IF;
END ///
DELIMITER ;


---------- PATCHES -------------

ALTER TABLE pyfunceble_tested ADD COLUMN IF NOT EXISTS ipv6_syntax_validation TINYINT(1) NULL AFTER ipv4_syntax_validation;
ALTER TABLE pyfunceble_tested ADD COLUMN IF NOT EXISTS ipv6_range_syntax_validation TINYINT(1) NULL AFTER ipv6_syntax_validation;