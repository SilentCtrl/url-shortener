USE URLs

CREATE TABLE IF NOT EXISTS links (
	id INT not NULL AUTO_INCREMENT,
	link VARCHAR(2000) NOT NULL
	PRIMARY KEY (id), KEY(link)
);
