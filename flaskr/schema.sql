DROP TABLE IF EXISTS payment;
DROP TABLE IF EXISTS sale_order_line;
DROP TABLE IF EXISTS sale_order;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS product_category;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  type TEXT NOT NULL
);
INSERT INTO USER(name, username, password, type)
VALUES('Administrador', 'admin', 'pbkdf2:sha256:150000$quqc7hq5$51bf3b35c9161e849f9b364dda2daaf562564c3d19e59ac10dda0664e9338b93', 'internal');

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE product_category (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);
INSERT INTO product_category(id, name) values(1, 'Ninguno');
INSERT INTO product_category(id, name) values(2, 'Ninguno2');

CREATE TABLE product (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  price_unit REAL NOT NULL,
  image_base64 TEXT NULL,
  category_id INTEGER NOT NULL,
  FOREIGN KEY (category_id) REFERENCES product_category (id)
);
INSERT INTO product (code, name, price_unit, category_id) VALUES('PRO1', 'Producto prueba 1 ', 12.99, 1);
INSERT INTO product (code, name, price_unit, category_id) VALUES('PRO2', 'Producto prueba 2', 1.99, 2);


CREATE TABLE sale_order (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  customer_id INTEGER NOT NULL,
  state TEXT NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES user (id)
);

CREATE TABLE sale_order_line (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id INTEGER NOT NULL,
  quantity REAL NOT NULL,
  price_unit REAL NOT NULL,
  order_id INTEGER NOT NULL,
  FOREIGN KEY (product_id) REFERENCES product (id),
  FOREIGN KEY (order_id) REFERENCES sale_order (id)
);

CREATE TABLE payment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  amount REAL NOT NULL,
  order_id INTEGER NOT NULL,
  FOREIGN KEY (order_id) REFERENCES sale_order (id)
);