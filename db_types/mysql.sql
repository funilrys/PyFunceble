
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

