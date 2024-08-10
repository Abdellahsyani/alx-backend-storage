-- write SQL script that create a table users
-- it will execute with any database

CREATE TABLE users (
	id INT NOT NULL AUTO_INCREMENT,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(25),
	PRIMARY KEY (id)
	);
