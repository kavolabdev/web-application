
USE auth;

CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO user (email, password) VALUES ('admin@gmail.com', 'admin123');
