from concrete.entity import artifact_entity , config_entity
from concrete.exception import ConcreteException
from concrete.logger import logging 
from typing import Optional
import os, sys
from sklearn.pipeline import Pipeline
import pandas as pd 
from concrete import utils
import numpy as np 
from concrete.config import TARGET_COLUMN
from scipy.stats import zscore
from sklearn.preprocessing import StandardScaler


class DataTransformation:

    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        
        try:
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise ConcreteException(e, sys)

    
    @classmethod
    def get_data_transfer_object(cls)->Pipeline:
        try:
            std_scaler=StandardScaler()
            
            pipeline=Pipeline(steps=[
                    ("stdscaler",std_scaler)
                ])
            return pipeline
        except Exception as e:
            raise ConcreteException(e,sys)

    

    def initiate_data_transformation(self,)->artifact_entity.DataTransformationArtifact:
        try:
            #reading train and test file
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_Path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)

            #selecting input feature for train and test dataframe
            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)

            #selecting target feature for train and test dataframe
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_test_df=test_df[TARGET_COLUMN]

            transformation_pipeline=DataTransformation.get_data_transfer_object()
            transformation_pipeline.fit(input_feature_train_df)

            #transforming input feature
            input_feature_train_arr=transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr=transformation_pipeline.transform(input_feature_test_df)

            
            
            #transformation on target columns
            target_feature_train_arr = (target_feature_train_df).values.reshape(-1, 1)
            target_feature_test_arr = (target_feature_test_df).values.reshape(-1, 1)

            train_arr=np.c_[input_feature_train_arr,target_feature_train_arr]
            test_arr=np.c_[input_feature_test_arr,target_feature_test_arr]

            #save numpy array
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path, array=train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path, array=test_arr)
        
            utils.save_object(file_path=self.data_transformation_config.transform_object_path, obj=transformation_pipeline)
            utils.save_object(file_path=self.data_transformation_config.target_scaler_path, obj=None)

            data_transformation_artifact=artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_train_path=self.data_transformation_config.transformed_train_path,
                transformed_test_path=self.data_transformation_config.transformed_test_path,
                target_scaler_path=self.data_transformation_config.target_scaler_path


            )

            logging.info(f" Data Transformation object{data_transformation_artifact}")
            return data_transformation_artifact
        
        
        except Exception as e:
            raise ConcreteException(e, sys)