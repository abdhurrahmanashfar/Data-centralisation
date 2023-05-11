import yaml
from sqlalchemy import create_engine
from sqlalchemy import inspect

class DatabaseConnector:

    def read_rds_credentials(self, db_creds_file):
        with open(db_creds_file, "r") as db_creds:
            creds_dict = yaml.safe_load(db_creds)
            return creds_dict

    def init_db_engine(self):
        creds_dict = self.read_rds_credentials("db_creds.yaml")
        database_type = "postgresql"
        dbapi = "psycopg2"
        host = creds_dict['RDS_HOST']
        user = creds_dict['RDS_USER']
        password = creds_dict['RDS_PASSWORD']
        database = creds_dict['RDS_DATABASE']
        port = creds_dict['RDS_PORT']
        engine = create_engine(f'{database_type}+{dbapi}://{user}:{password}@{host}:{port}/{database}')
        engine.connect()
        return engine

    def upload_to_db(self, df, table_name):
        creds_dict = self.read_rds_credentials("local_db_creds.yaml")
        database_type = "postgresql"
        dbapi = "psycopg2"
        host = creds_dict['HOST']
        user = creds_dict['USER']
        password = creds_dict['PASSWORD']
        database = creds_dict['DATABASE']
        port = 5432
        engine = create_engine(f'{database_type}+{dbapi}://{user}:{password}@{host}:{port}/{database}')
        engine.connect()
        df.to_sql(name = table_name, con = engine, if_exists = "replace")

    def list_db_tables(self):
        engine = self.init_db_engine()
        inspector = inspect(engine)

        return inspector.get_table_names()

        


