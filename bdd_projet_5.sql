SET NAMES utf8;

DROP DATABASE IF EXISTS openfoodfacts;

CREATE DATABASE openfoodfacts;

USE openfoodfacts;

CREATE TABLE Food(
	id INT UNSIGNED AUTO_INCREMENT,
	name VARCHAR(250) NOT NULL,
	category_id_1 VARCHAR(300) NOT NULL,
	category_id_2 VARCHAR(300),
	category_id_3 VARCHAR(300),
	stores VARCHAR(150),
	PRIMARY KEY(id)
	)ENGINE=InnoDB;

CREATE TABLE Categories(
	id VARCHAR(300) NOT NULL,
	name VARCHAR(200),
	PRIMARY KEY(id)
	)ENGINE=InnoDB;

-- Not used for now
CREATE TABLE User(
	id INT UNSIGNED AUTO_INCREMENT,
	name VARCHAR(100) NOT NULL,
	favorite_id INT UNSIGNED,
	PRIMARY KEY(id)
	)ENGINE=InnoDB;

INSERT INTO Categories (id, name) VALUES ('None', "") -- Need an id for empty categories because of the foreign key

ALTER TABLE User ADD CONSTRAINT fk_favorite_id_food FOREIGN KEY (favorite_id) REFERENCES Food(id); -- Not used for now
ALTER TABLE Food ADD CONSTRAINT fk_categories_id_1_food FOREIGN KEY (category_id_1) REFERENCES Categories(id);
ALTER TABLE Food ADD CONSTRAINT fk_categories_id_2_food FOREIGN KEY (category_id_2) REFERENCES Categories(id);
ALTER TABLE Food ADD CONSTRAINT fk_categories_id_3_food FOREIGN KEY (category_id_3) REFERENCES Categories(id);

--ALTER TABLE Food ADD FULLTEXT ind_name_food (name);
--ALTER TABLE Categories ADD FULLTEXT ind_name_categories(name);



