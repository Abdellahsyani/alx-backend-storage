-- write SQL script that create a table users
-- it will execute with any database

CREATE TABLE users (
	id INT NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255),
	PRIMARY KEY (id)
	);
