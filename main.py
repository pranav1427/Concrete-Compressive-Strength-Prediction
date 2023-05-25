from concrete.logger import logging
from concrete.exception import ConcreteException
from concrete.utils import get_collection_as_dataframe
import os,sys
from concrete.entity.config_entity import DataIngestionConfig
from concrete.entity import config_entity


if __name__=="__main__" :
     try:
          training_pipeline_config=config_entity.TrainingPipelineConfig()
          data_ingestion_config=DataIngestionConfig(training_pipeline_config=training_pipeline_config)
          print(data_ingestion_config.to_dict())
         
     except Exception as e:
          print(e)