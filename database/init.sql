-- many to many
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    product TEXT,
    last_stock INT,
    title TEXT
);

CREATE TABLE telegram_users (
    id SERIAL PRIMARY KEY,
    tel_chat_id INT NOT NULL
);

CREATE TABLE notifications (
    product_id BIGINT NOT NULL,
    telegram_user_id BIGINT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (telegram_user_id) REFERENCES telegram_users(id)
);