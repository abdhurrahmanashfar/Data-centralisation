-- Milestone 4
-- Task 1

SELECT country_code AS country, COUNT(*) AS total_no_stores
FROM dim_store_details
GROUP BY country_code
ORDER BY total_no_stores DESC;

-- Task 2

SELECT locality, COUNT(*) AS total_no_stores
FROM dim_store_details
GROUP BY locality
ORDER BY total_no_stores DESC
LIMIT 7;

-- Task 3

SELECT SUM(orders_table.product_quantity * dim_products.product_price) as total_sales, dim_date_times.month 
FROM dim_date_times 
JOIN orders_table ON dim_date_times.date_uuid = orders_table.date_uuid 
JOIN dim_products ON orders_table.product_code = dim_products.product_code 
GROUP BY dim_date_times.month 
ORDER BY total_sales DESC
LIMIT 6;

-- TASK 4

SELECT COUNT(*) as number_of_sales, SUM(product_quantity) as product_quantity_count,
CASE 
    WHEN store_code LIKE 'WEB%' THEN 'Web'
    ELSE 'Offline'
END AS location    
FROM orders_table
GROUP BY location;

-- TASK 5

SELECT
	store_type,
	SUM(product_quantity * product_price) AS total_sales,
	ROUND((SUM(product_quantity * product_price)::numeric / SUM(SUM(product_quantity * product_price)::numeric) OVER ()) * 100.0, 2) AS percentage_total
FROM
	orders_table
	JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code
	JOIN dim_products ON orders_table.product_code = dim_products.product_code
GROUP BY store_type
ORDER BY total_sales DESC;

-- Task 6

SELECT
    SUM(product_quantity * product_price) AS total_sales,
    year, month 
FROM orders_table
    JOIN dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid
	JOIN dim_products ON orders_table.product_code = dim_products.product_code
GROUP BY year, month
ORDER BY total_sales DESC
LIMIT 10;

-- Task 7

SELECT 
	SUM(staff_numbers) as total_staff_numbers, country_code
FROM dim_store_details
GROUP BY country_code
ORDER BY total_staff_numbers DESC;

-- Task 8

SELECT 
SUM(product_quantity * product_price) AS total_sales, 
store_type, 
country_code 
FROM orders_table
JOIN dim_products on orders_table.product_code = dim_products.product_code 
JOIN dim_store_details on orders_table.store_code = dim_store_details.store_code AND dim_store_details.country_code = 'DE' 
GROUP BY store_type, country_code
ORDER BY total_sales;

-- Task 9

WITH cte AS(
SELECT TO_TIMESTAMP(CONCAT(year, '-', month, '-', day, ' ', timestamp), 'YYYY-MM-DD HH24:MI:SS') as datetimes, year FROM dim_date_times
ORDER BY datetimes DESC), 
cte2 AS(
SELECT
year, 
datetimes, 
LEAD(datetimes, 1) OVER (ORDER BY datetimes DESC) as time_difference 
FROM cte) 
SELECT year, AVG((datetimes - time_difference)) as actual_time_taken FROM cte2
GROUP BY year
ORDER BY actual_time_taken DESC
LIMIT 5;













