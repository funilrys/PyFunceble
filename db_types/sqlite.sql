
CREATE TABLE IF NOT EXISTS auto_continue (
    id INTEGER PRIMARY KEY,
    file_path TEXT NOT NULL,
    subject TEXT NOT NULL,
    status TEXT NOT NULL,
    is_complement INTEGER NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(file_path, subject)
);

CREATE TRIGGER IF NOT EXISTS updateAutoContinueDates
    AFTER UPDATE
    ON auto_continue
    FOR EACH ROW
    WHEN NEW.modified <= old.modified
BEGIN
    UPDATE auto_continue SET modified=CURRENT_TIMESTAMP WHERE id=OLD.id;
END;

CREATE TABLE IF NOT EXISTS inactive (
    id INTEGER PRIMARY KEY,
    file_path TEXT NOT NULL,
    subject TEXT NOT NULL,
    status INTEGER NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(file_path, subject)
);

CREATE TRIGGER IF NOT EXISTS updateInactiveDates
    AFTER UPDATE
    ON inactive
    FOR EACH ROW
    WHEN NEW.modified <= old.modified
BEGIN
    UPDATE inactive SET modified=CURRENT_TIMESTAMP WHERE id=OLD.id;
END;

CREATE TABLE IF NOT EXISTS mining (
    id INTEGER PRIMARY KEY,
    file_path TEXT NOT NULL,
    subject TEXT NOT NULL,
    mined TEXT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(file_path, subject, mined)
);

CREATE TRIGGER IF NOT EXISTS updateMiningDates
    AFTER UPDATE
    ON mining
    FOR EACH ROW
    WHEN NEW.modified <= old.modified
BEGIN
    UPDATE mining SET modified=CURRENT_TIMESTAMP WHERE id=OLD.id;
END;

CREATE TABLE IF NOT EXISTS whois (
    id INTEGER PRIMARY KEY,
    subject TEXT NOT NULL,
    expiration_date TEXT NOT NULL,
    expiration_date_epoch INTEGER NOT NULL,
    state TEXT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(subject)
);

CREATE TRIGGER IF NOT EXISTS updateWhoisDates
    AFTER UPDATE
    ON whois
    FOR EACH ROW
    WHEN NEW.modified <= old.modified
BEGIN
    UPDATE whois SET modified=CURRENT_TIMESTAMP WHERE id=OLD.id;
END;