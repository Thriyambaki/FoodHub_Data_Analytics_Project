create database foodhub;
use foodhub;
show tables;
SELECT COUNT(*) AS Total_Orders
FROM order_raw_cleaned;
SELECT
    order_id,
    COUNT(*) AS Duplicate_Count
FROM order_raw_cleaned
GROUP BY order_id
HAVING COUNT(*) > 1;

describe order_raw_cleaned;

USE FoodHub;

ALTER TABLE order_raw_cleaned
RENAME COLUMN `ï»¿order_id` TO order_id;



SELECT COUNT(*) AS Missing_Cities
FROM order_raw_cleaned
WHERE city IS NULL OR TRIM(city) = '';


SELECT COUNT(*) AS Missing_Delivery_Times
FROM order_raw_cleaned
WHERE delivery_time_min IS NULL;


SELECT
    order_status,
    COUNT(*) AS Total_Orders
FROM order_raw_cleaned
GROUP BY order_status;  # gives the total delivered,cancelled,returned orders





# exercises on food data

select * from order_raw_cleaned;

SELECT order_id, city, order_amount FROM order_raw_cleaned;


SELECT * FROM order_raw_cleaned LIMIT 20;

SELECT * FROM order_raw_cleaned WHERE order_status = 'Delivered';

SELECT * FROM order_raw_cleaned WHERE city = 'Bengaluru';

SELECT * FROM order_raw_cleaned WHERE order_amount > 500;

SELECT * FROM order_raw_cleaned WHERE order_status = 'Delivered'AND city = 'Bengaluru';

select * from order_raw_cleaned where city= 'Bengaluru' or 'Chennai';

SELECT * FROM order_raw_cleaned WHERE order_amount BETWEEN 300 AND 800;

SELECT order_id, order_amount FROM order_raw_cleaned 
ORDER BY order_amount DESC LIMIT 10;

SELECT DISTINCT city FROM order_raw_cleaned;


SELECT COUNT(*) AS Total_Orders FROM order_raw_cleaned;

SELECT SUM(order_amount) AS Total_Delivered_Sales FROM order_raw_cleaned
WHERE order_status = 'Delivered';


SELECT AVG(delivery_time_min) AS Average_Delivery_Time FROM order_raw_cleaned
WHERE order_status = 'Delivered';

SELECT
    MAX(order_amount) AS Highest_Order,
    MIN(order_amount) AS Lowest_Order
FROM order_raw_cleaned;

SELECT city, COUNT(*) AS Total_Orders FROM order_raw_cleaned GROUP BY city;


SELECT city, SUM(order_amount) AS Total_Sales FROM order_raw_cleaned 
WHERE order_status = 'Delivered'
GROUP BY city ORDER BY Total_Sales DESC;


SELECT order_status, COUNT(*) AS Order_Count FROM order_raw_cleaned GROUP BY order_status;


SELECT city, COUNT(*) AS Total_Orders FROM order_raw_cleaned 
GROUP BY city HAVING COUNT(*) > 400;

SELECT
    o.order_id,
    o.customer_id,
    c.customer_name,
    o.city,
    o.order_amount
FROM order_raw_cleaned o
INNER JOIN customers c
ON o.customer_id = c.customer_id;

describe customers;

ALTER TABLE customers
RENAME COLUMN `ï»¿customer_id` TO customer_id;

describe restaurants;

ALTER TABLE restaurants
RENAME COLUMN `ï»¿restaurant_id` TO restaurant_id;

SELECT
    o.order_id,
    r.restaurant_name,
    o.order_amount,
    o.order_status
FROM order_raw_cleaned o
INNER JOIN restaurants r
ON o.restaurant_id = r.restaurant_id;



SELECT
    r.restaurant_id,
    r.restaurant_name
FROM restaurants r
LEFT JOIN order_raw_cleaned o
ON r.restaurant_id = o.restaurant_id
WHERE o.restaurant_id IS NULL;


SELECT
    COUNT(*) AS Total_Orders,
    SUM(CASE
        WHEN order_status = 'Cancelled' THEN 1
        ELSE 0
    END) AS Cancelled_Orders,
    ROUND(
        100.0 * SUM(CASE
            WHEN order_status = 'Cancelled' THEN 1
            ELSE 0
        END) / COUNT(*),
        2
    ) AS Cancellation_Percentage
FROM order_raw_cleaned;



SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS Order_Month,
    SUM(order_amount) AS Monthly_Sales
FROM order_raw_cleaned
WHERE order_status = 'Delivered'
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY Order_Month;


SELECT
    ROUND(AVG(order_amount), 2) AS Average_Order_Value
FROM order_raw_cleaned
WHERE order_status = 'Delivered';









