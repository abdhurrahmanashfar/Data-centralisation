import pandas as pd
import tabula
import requests
import boto3


class DataExtractor:
    def read_rds_table(self, db_connector, table_name):
        engine = db_connector.init_db_engine()
        users_df = pd.read_sql_table(table_name, con=engine, index_col="index")
        return users_df

    def retrieve_pdf_data(self, link):
        df = pd.concat(tabula.read_pdf(link, pages="all"), ignore_index = True)
        df = pd.DataFrame(df)
        return df

    def list_number_of_stores(self, num_of_stores, header_dict):
        header_dict = {"x-api-key" : "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"}
        response = requests.get(num_of_stores, headers = header_dict)
        data = response.json()
        # {'statusCode': 200, 'number_stores': 451}
        return data
       
    def retrieve_stores_data(self, Retrieve_store, header_dict):
        dict_list = []
        header_dict = {"x-api-key" : "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"}
        for stores in range(451):
            response = requests.get(Retrieve_store.format(store_number = stores), headers = header_dict)
            dict_list.append(response.json())

        df = pd.DataFrame(dict_list)
        # df.to_csv("store_details.csv")
                
        return df
        
    def extract_from_s3(self, address):
        s3 = boto3.client('s3')
        # df = s3.download_file(address)
        df = pd.read_csv(address)

        return df

    def extract_json(self, link):
        response = requests.get(link)
        data = response.json()
        df = pd.DataFrame(data)
        
        return df
        






