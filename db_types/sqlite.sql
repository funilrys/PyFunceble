
CREATE TABLE auto_continue (
    id INTEGER PRIMARY KEY,
    file_path TEXT NOT NULL,
    subject TEXT NOT NULL,
    status TEXT NOT NULL,
    created timestamp DEFAULT CURRENT_TIMESTAMP,
    modified timestamp DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(file_path, subject)
);

CREATE TRIGGER updateAutoContinueDates
    AFTER UPDATE
    ON auto_continue
    FOR EACH ROW
    WHEN NEW.modified <= old.modified
BEGIN
    UPDATE auto_continue SET modified=CURRENT_TIMESTAMP where id=OLD.id;
END;

CREATE TABLE inactive (
    id INTEGER PRIMARY KEY,
    file_path TEXT NOT NULL,
    subject TEXT NOT NULL,
    created timestamp DEFAULT CURRENT_TIMESTAMP,
    modified timestamp DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(file_path, subject)
);

CREATE TRIGGER updateInactiveDates
    AFTER UPDATE
    ON inactive
    FOR EACH ROW
    WHEN NEW.modified <= old.modified
BEGIN
    UPDATE inactive SET modified=CURRENT_TIMESTAMP where id=OLD.id;
END;

CREATE TABLE mining (
    id INTEGER PRIMARY KEY,
    file_path TEXT NOT NULL,
    subject TEXT NOT NULL,
    mined TEXT NOT NULL,
    created timestamp DEFAULT CURRENT_TIMESTAMP,
    modified timestamp DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(file_path, subject, mined)
);

CREATE TRIGGER updateMiningDates
    AFTER UPDATE
    ON mining
    FOR EACH ROW
    WHEN NEW.modified <= old.modified
BEGIN
    UPDATE mining SET modified=CURRENT_TIMESTAMP where id=OLD.id;
END;

CREATE TABLE whois (
    id INTEGER PRIMARY KEY,
    subject TEXT NOT NULL,
    expiration_date TEXT NOT NULL,
    expiration_date_epoch INTEGER NOT NULL,
    state TEXT NOT NULL,
    created timestamp DEFAULT CURRENT_TIMESTAMP,
    modified timestamp DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(subject)
);

CREATE TRIGGER updateWhoisDates
    AFTER UPDATE
    ON whois
    FOR EACH ROW
    WHEN NEW.modified <= old.modified
BEGIN
    UPDATE whois SET modified=CURRENT_TIMESTAMP where id=OLD.id;
END;