from data_extraction import DataExtractor
from database_utils import DatabaseConnector
from data_cleaning import DataCleaning

db_ex = DataExtractor()
db_con = DatabaseConnector()
db_clean = DataCleaning()

import pandas as pd

users_df = db_ex.read_rds_table(db_con, "legacy_users")
users_df.to_csv("legacy_users.csv")
clean_users_df = db_clean.clean_user_data(users_df)
clean_users_df.to_csv("clean_users_data.csv")
db_con.upload_to_db(clean_users_df, "dim_users")

pdf_data = db_ex.retrieve_pdf_data("https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf")
print(pdf_data)
pdf_data.to_csv("card_details.csv")
clean_pdf_data = db_clean.clean_card_data(pdf_data)
print(clean_pdf_data)
db_con.upload_to_db(clean_pdf_data, "dim_card_details")

store_df = db_ex.list_number_of_stores("https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores", 
"https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}")
print(store_df)

store_df_1 = db_ex.retrieve_stores_data("https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}", {"x-api-key" : "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"})
print(store_df_1)
store_df_1.to_csv("store_details.csv")
df = pd.read_csv("store_details.csv")
clean_store_df = db_clean.clean_store_data(df) 
print(clean_store_df)
db_con.upload_to_db(clean_store_df, "dim_store_details")

products = db_ex.extract_from_s3("s3://data-handling-public/products.csv")
print(products)
# products.to_csv("product_details.csv")
clean_products_df = db_clean.clean_products_data(products)
print(clean_products_df)
# clean_products_df.to_csv("cleaned_product_df.csv")
db_con.upload_to_db(clean_products_df, "dim_products")

db_con.list_db_tables()
orders_df = db_ex.read_rds_table(db_con, "orders_table")
print(orders_df)
orders_df.to_csv("orders_df.csv")
clean_orders_df = db_clean.clean_orders_data(orders_df)
print(clean_orders_df)
db_con.upload_to_db(clean_orders_df, "orders_table")

json_df = db_ex.extract_json("https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json")
print(json_df)
json_df.to_csv("date_times.csv")
cleaned_json_df = db_clean.clean_date_times(json_df)
print(cleaned_json_df)
db_con.upload_to_db(cleaned_json_df, "dim_date_times")


