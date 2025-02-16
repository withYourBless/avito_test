CREATE TABLE Users (
    id text primary key,
    username text NOT NULL,
    password text NOT NULL,
    coins INT DEFAULT 0
);


CREATE TABLE Inventory (
    id text primary key,
    user_id text NOT NULL,
    item_name text NOT NULL,
    quantity INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TYPE transaction_type AS ENUM ('received', 'sent');

CREATE TABLE CoinTransactions (
    id text primary key,
    user_id text NOT NULL,
    from_user_id text NOT NULL,
    to_user_id text NOT NULL,
    amount INT,
    transaction_type transaction_type,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (from_user_id) REFERENCES Users(id),
    FOREIGN KEY (to_user_id) REFERENCES Users(id)
);


CREATE TABLE Items (
    id text primary key,
    name text NOT NULL,
    price INT NOT NULL
);

INSERT INTO Items (id, name, price) VALUES
('1', 't-shirt', 80),
('2', 'cup', 20),
('3', 'book', 50),
('4', 'pen', 10),
('5', 'powerbank', 200),
('6', 'hoody', 300),
('7', 'umbrella', 200),
('8', 'socks', 10),
('9', 'wallet', 50),
('10', 'pink-hoody', 500);


