import pandas as pd
import re

class DataCleaning:
    def clean_user_data(self, users_df):
        users_df.drop(index = [752, 1047, 2997, 3539, 5309, 6426, 8398, 9026, 10224, 10373, 11381, 12197, 13135, 14124, 14523], inplace = True)
        users_df = users_df.drop(users_df[users_df['user_uuid'].str.contains('NULL')].index)
        users_df["date_of_birth"] = pd.to_datetime(users_df["date_of_birth"])
        users_df["join_date"] = pd.to_datetime(users_df["join_date"])

        return users_df
    
    def clean_card_data(self, pdf_data):
        pdf_data.drop(index = [377, 827, 847, 884, 1443, 2418, 2489, 2830, 3694, 4208, 4196, 4916, 5686, 6024, 6653, 7332, 7493, 7818, 10457, 11345, 11465, 11499, 12876, 13708, 14884], inplace = True)
        pdf_data["date_payment_confirmed"] = pd.to_datetime(pdf_data["date_payment_confirmed"])

        return pdf_data    

    def clean_store_data(self, store_df):
        store_df.drop("lat", axis = 1, inplace = True)
        store_df.drop(index = [0, 63, 172, 231, 333, 381, 414, 447], inplace = True)
        store_df['opening_date'] = pd.to_datetime(store_df['opening_date'])
        store_df['continent'] = store_df['continent'].str.replace('ee', '')

        return store_df

    def convert_product_weights(self, weight):
        weight = str(weight)
        if re.search(r'kg\b', weight):
            x = re.sub("[\s,'kg']", "", weight)
            return float(x)
        elif re.search ('x', weight):
            weight = re.sub("x", "*", weight)
            y = re.sub("[\s,'g']", "", weight)
            z = eval(y)
            return float(z)/1000
        elif re.search (r'ml\b',weight):
            x = re.sub("[\s,'ml']", "", weight)
            return float(x)/1000
        elif re.search(r'g\b', weight):
            x = re.sub("[\s,'g']", "", weight)
            return float(x)/1000
        elif re.search(r'oz\b', weight):
            x = re.sub("[\s,'oz']", "", weight)
            return float(x)*0.0283495
        
        return weight

       
# product_df['weight'] = product_df['weight'].apply(self.convert_product_weights)
        
    def clean_products_data(self, product_df):
        product_df.drop(index = [751, 1133, 1400], inplace = True)
        product_df['date_added'] = pd.to_datetime(product_df['date_added'])
        product_df['product_price'] = product_df['product_price'].str.replace('£', '')
        product_df['product_price'] = product_df['product_price'].str.replace('Â', '')
        product_df['weight'] = product_df['weight'].apply(self.convert_product_weights)
        product_df['weight'] = product_df['weight'].astype('float')
        product_df.drop('Unnamed: 0', axis=1, inplace=True)
        
        return product_df
        
    def clean_orders_data(self, order_df):
        order_df.drop(["first_name", "last_name", "1"], axis = 1, inplace = True)

        return order_df


    def clean_date_times(self, date_times_df):
        date_times_df.dropna(inplace = True)
        # date_times_df["timestamp"] = pd.to_datetime(date_times_df["timestamp"])

        return date_times_df

