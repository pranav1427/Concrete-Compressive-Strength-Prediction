import pandas as pd 
from concrete.config import mongo_client
from concrete.logger import logging
from concrete.exception import ConcreteException
import os,sys
import yaml

def get_collection_as_dataframe(database_name,collection_name:str)->pd.DataFrame:
    try:
        logging.info(f"Reading data from database :{database_name} and collection name {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found columns: {df.columns}")
        if"_id" in df.columns:
            logging.info(f"Dropping column : _id")
            df=df.drop("_id",axis=1)
        logging.info(f"rows and col in df:{df.shape}")
        return df
    except Exception as e:
        raise ConcreteException(e, sys)

def write_yaml_file(file_path,data:dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path,"w") as file_writer:
            yaml.dump(data,file_writer)
    except Exception as e:
        raise ConcreteException(e, sys)