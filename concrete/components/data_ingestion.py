from concrete import utils
from concrete.entity import config_entity
from concrete.entity import artifact_entity
from concrete.exception import ConcreteException
from concrete.logger import logging
import os,sys
import pandas as pd
import numpy as np 
from sklearn.model_selection import train_test_split


class DataIngestion:

    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise ConcreteException(e,sys)

    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            logging.info(f"exporting database name and collection name ")
            # exporting database name and collection name 
            df:pd.DataFrame=utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name,
                collection_name=self.data_ingestion_config.collection_name)

            logging.info(f"save dataset in feature store folder")
            #save dataset in feature store folder
            df.replace(to_replace="na",value=np.NAN, inplace=True)

            logging.info(f"create feature store folder")
            #create feature store folder
            feature_store_dir=os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)

            logging.info(f"save df to feature store")
            #save df to feature store
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)

            logging.info(f"split data into train test split")
            #split data into train test split
            train_df,test_df=train_test_split(df,test_size=self.data_ingestion_config.test_size)

            logging.info(f"create dataset dir")
            #create dataset dir
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)

            logging.info(f"save df to feature store folder")
            #save df to feature store folder
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)

            #Artifacts
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_Path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path)

            logging.info(f"Data ingestion artifact:{data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise ConcreteException(e,sys)

