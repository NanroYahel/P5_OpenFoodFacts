SET NAMES utf8;

CREATE DATABASE openfoodfacts;

USE openfoodfacts;

CREATE TABLE Food(
	id INT UNSIGNED AUTO_INCREMENT,
	name VARCHAR(150) NOT NULL,
	categories_id VARCHAR(400) NOT NULL,
	stores VARCHAR(150),
	PRIMARY KEY(id)
	)ENGINE=InnoDB;

CREATE TABLE Categories(
	id VARCHAR(400) NOT NULL,
	name VARCHAR(100) NOT NULL,
	PRIMARY KEY(id)
	)ENGINE=InnoDB;

-- Not used for now
CREATE TABLE User(
	id INT UNSIGNED AUTO_INCREMENT,
	name VARCHAR(100) NOT NULL,
	favorite_id INT UNSIGNED,
	PRIMARY KEY(id)
	)ENGINE=InnoDB;

ALTER TABLE Food ADD CONSTRAINT fk_food_categories FOREIGN KEY (categories_id) REFERENCES Categories(id);
ALTER TABLE User ADD CONSTRAINT fk_favorite_id_food FOREIGN KEY (favorite_id) REFERENCES Food(id); -- Not used for now

ALTER TABLE Food ADD FULLTEXT ind_name_food (name);
ALTER TABLE Categories ADD FULLTEXT ind_name_categories(name);



