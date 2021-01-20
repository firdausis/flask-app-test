DROP DATABASE IF EXISTS data_manager;

CREATE DATABASE data_manager;

\c data_manager;

CREATE TABLE users (
    id            BIGSERIAL   PRIMARY KEY, 
    first_name    VARCHAR     NOT NULL,
    last_name     VARCHAR     NOT NULL,
    user_name     VARCHAR     NOT NULL,
    user_pwd      VARCHAR     NOT NULL,
    is_active     BOOLEAN     NOT NULL DEFAULT TRUE,
    created_time  TIMESTAMP   NOT NULL
);

CREATE TABLE user_data(
    id              BIGSERIAL    PRIMARY KEY,
    data_file_name  VARCHAR      NOT NULL,
    total_count     INT          NOT NULL,
    success_count   INT          NOT NULL,
    fail_count      INT          NOT NULL,
    user_id         INT          NOT NULL,
    created_time    TIMESTAMP    NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE user_data_details(
    id                              BIGSERIAL   PRIMARY KEY,
    data_year                       INT			NOT NULL,
    industry_aggregation_nzsioc     VARCHAR		NOT NULL,
    industry_code_nzsioc            VARCHAR		NOT NULL,
    industry_name_nzsioc            VARCHAR		NOT NULL,
    units                           VARCHAR		NOT NULL,
    variable_code                   VARCHAR		NOT NULL,
    variable_name                   VARCHAR		NOT NULL,
    variable_category               VARCHAR		NOT NULL,
    data_value                      INT			NOT NULL,
    industry_code_anzsic06          VARCHAR		NOT NULL,
    user_data_id                    INT			NOT NULL,
    created_time                    TIMESTAMP   NOT NULL,
    FOREIGN KEY (user_data_id) REFERENCES user_data(id)
);

INSERT INTO users(first_name, last_name, user_name, user_pwd, created_time) VALUES('John', 'Smith', 'johnsmith', '$2b$12$zHlI8ZpxyWYgdjxQadIU6ebDKioD5KmK1pYJumfRzVND10aGi9PVq', CURRENT_TIMESTAMP);
INSERT INTO users(first_name, last_name, user_name, user_pwd, created_time) VALUES('David', 'Johnson', 'davidjohnson', '$2b$12$zHlI8ZpxyWYgdjxQadIU6ebDKioD5KmK1pYJumfRzVND10aGi9PVq', CURRENT_TIMESTAMP);
INSERT INTO users(first_name, last_name, user_name, user_pwd, created_time) VALUES('Amir', 'Strum', 'amirstrum', '$2b$12$zHlI8ZpxyWYgdjxQadIU6ebDKioD5KmK1pYJumfRzVND10aGi9PVq', CURRENT_TIMESTAMP);
INSERT INTO users(first_name, last_name, user_name, user_pwd, created_time) VALUES('Avi', 'Galber', 'avigelber', '$2b$12$zHlI8ZpxyWYgdjxQadIU6ebDKioD5KmK1pYJumfRzVND10aGi9PVq', CURRENT_TIMESTAMP);