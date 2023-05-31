ALTER TABLE orders_table
ALTER COLUMN date_uuid TYPE uuid USING date_uuid::uuid,
ALTER COLUMN user_uuid TYPE uuid USING user_uuid::uuid,
ALTER COLUMN card_number TYPE varchar(255),
ALTER COLUMN store_code TYPE varchar(255),
ALTER COLUMN product_code TYPE varchar(255),
ALTER COLUMN product_quantity TYPE smallint;


ALTER TABLE dim_users
ALTER COLUMN first_name TYPE varchar(255),
ALTER COLUMN last_name TYPE varchar(255),
ALTER COLUMN date_of_birth TYPE date,
ALTER COLUMN country_code TYPE varchar(255),
ALTER COLUMN user_uuid TYPE uuid USING user_uuid::uuid,
ALTER COLUMN join_date TYPE date;


UPDATE dim_store_details
SET staff_numbers = CAST(REGEXP_REPLACE(staff_numbers, '[A-Za-z]', '') AS INTEGER);

ALTER TABLE dim_store_details
ALTER COLUMN longitude TYPE float USING longitude::double precision,
ALTER COLUMN locality TYPE varchar(255),
ALTER COLUMN store_code TYPE varchar(255),
ALTER COLUMN staff_numbers TYPE smallint USING staff_numbers::smallint,
ALTER COLUMN opening_date TYPE date,
ALTER COLUMN store_type TYPE varchar(255),
ALTER COLUMN latitude TYPE float USING latitude::double precision,
ALTER COLUMN country_code TYPE varchar(255),
ALTER COLUMN continent TYPE varchar(255);


-- UPDATE dim_store_details
-- SET location = 'N/A'
-- WHERE location IS NULL;

-- UPDATE dim_products
-- SET product_price = REPLACE(product_price, '£', '');


ALTER TABLE dim_products ADD COLUMN weight_class VARCHAR(14);
UPDATE dim_products
SET weight_class = CASE
    WHEN weight < 2 THEN 'Light'
    WHEN weight BETWEEN 3 AND 40 THEN 'Mid_Sized'
    WHEN weight BETWEEN 41 AND 140 THEN 'Heavy'
    ELSE 'Truck_required'
END;


ALTER TABLE dim_products RENAME COLUMN removed TO still_available;


ALTER TABLE dim_products
ALTER COLUMN product_price TYPE FLOAT USING product_price::double precision,
ALTER COLUMN weight TYPE FLOAT,
ALTER COLUMN "EAN" TYPE VARCHAR(50),
ALTER COLUMN product_code TYPE VARCHAR(50),
ALTER COLUMN date_added TYPE DATE,
ALTER COLUMN uuid TYPE UUID USING uuid::uuid,
ALTER COLUMN still_available TYPE BOOL USING 
	CASE 
		WHEN still_available LIKE 'Still_available' THEN true
		ELSE false
	END;



ALTER TABLE dim_date_times
ALTER COLUMN month TYPE CHAR(50),
ALTER COLUMN year TYPE CHAR(50),
ALTER COLUMN day TYPE CHAR(50),
ALTER COLUMN time_period TYPE VARCHAR(100),
ALTER COLUMN date_uuid TYPE UUID USING date_uuid::uuid;


ALTER TABLE dim_card_details
ALTER COLUMN card_number TYPE VARCHAR(50),
ALTER COLUMN expiry_date TYPE VARCHAR(50),
ALTER COLUMN date_payment_confirmed TYPE DATE;


-- Primary keys
ALTER TABLE dim_card_details
ADD CONSTRAINT PK_dim_card_details PRIMARY KEY (card_number);


ALTER TABLE dim_date_times
ADD CONSTRAINT PK_dim_date_times PRIMARY KEY (date_uuid);

ALTER TABLE dim_store_details
ADD CONSTRAINT PK_dim_store_details PRIMARY KEY (store_code);

ALTER TABLE dim_products
ADD CONSTRAINT PK_dim_products PRIMARY KEY (product_code);

ALTER TABLE dim_users
ADD CONSTRAINT PK_dim_users PRIMARY KEY (user_uuid);


-- Foreign keys
ALTER TABLE orders_table
ADD CONSTRAINT FK_orders_table
FOREIGN KEY (card_number)
REFERENCES dim_card_details(card_number);

ALTER TABLE orders_table
ADD CONSTRAINT FK_orders_table
FOREIGN KEY (date_uuid)
REFERENCES dim_date_times(date_uuid);

ALTER TABLE orders_table
ADD CONSTRAINT FK_orders_table
FOREIGN KEY (store_code)
REFERENCES dim_store_details(store_code);

ALTER TABLE orders_table
ADD CONSTRAINT FK_orders_table
FOREIGN KEY (product_code)
REFERENCES dim_products(product_code);

ALTER TABLE orders_table
ADD CONSTRAINT FK_orders_table
FOREIGN KEY (user_uuid)
REFERENCES dim_users(user_uuid);





