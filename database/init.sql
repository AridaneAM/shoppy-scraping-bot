CREATE TABLE tel_user (
    id SERIAL NOT NULL PRIMARY KEY,
    tel_chat_id INT NOT NULL,
    product_ID TEXT[]
);