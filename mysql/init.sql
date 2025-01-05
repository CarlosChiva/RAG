CREATE DATABASE IF NOT EXISTS app_db;

USE app_db;

CREATE TABLE IF NOT EXISTS users (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL

);
CREATE TABLE IF NOT EXISTS collections (
    id_colleciton SERIAL PRIMARY KEY,
    id_user INT NOT NULL,
    collection_name VARCHAR(255) UNIQUE NOT NULL,
    FOREIGN KEY (id_user) REFERENCES users(id_user)
);
