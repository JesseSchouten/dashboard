#dashboard database
CREATE DATABASE dashboard;
drop table dashboard.users;
CREATE TABLE dashboard.users(
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100),
email VARCHAR(100),
username BLOB not null,
password VARCHAR(100),
permissions VARCHAR(30) DEFAULT 'user',
register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
UNIQUE KEY `u_k_1`(username(30))
 );
 
 SELECT * FROM dashboard.users;

CREATE TABLE dashboard.articles (
id INT AUTO_INCREMENT PRIMARY KEY,
title VARCHAR(255),
author VARCHAR(100),
body TEXT,
create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
