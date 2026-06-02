CREATE TABLE sales (
    order_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    product VARCHAR(100),
    quantity INT,
    price NUMERIC(10,2),
    total_amount NUMERIC(10,2),
    order_date DATE
);

CREATE TABLE sales_staging (
    order_id INT,
    customer_name VARCHAR(100),
    product VARCHAR(100),
    quantity INT,
    price NUMERIC(10,2),
    total_amount NUMERIC(10,2),
    order_date DATE
);