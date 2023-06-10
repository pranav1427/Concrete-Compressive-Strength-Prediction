from concrete.logger import logging
from concrete.exception import ConcreteException
from concrete.utils import get_collection_as_dataframe
import os,sys
from concrete.entity.config_entity import DataIngestionConfig
from concrete.entity import config_entity
from concrete.components.data_ingestion import DataIngestion
from concrete.components.data_validation import DataValidation
from concrete.components.model_trainer import ModelTrainer
from concrete.components.data_transformation import DataTransformation


if __name__=="__main__" :
     try:
          training_pipeline_config=config_entity.TrainingPipelineConfig()
          data_ingestion_config=DataIngestionConfig(training_pipeline_config=training_pipeline_config)
          print(data_ingestion_config.to_dict())
          data_ingestion= DataIngestion(data_ingestion_config=data_ingestion_config)
          data_ingestion_artifact=data_ingestion.initiate_data_ingestion()

          data_validation_config=config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
          data_validation=DataValidation(data_validation_config=data_validation_config,
                         data_ingestion_artifact=data_ingestion_artifact)

          data_validation_artifact=data_validation.initiate_data_validation()

          data_transformation_config=config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
          data_transformation=DataTransformation(data_transformation_config=data_transformation_config,
          data_ingestion_artifact=data_ingestion_artifact)
          data_transformation_artifact=data_transformation.initiate_data_transformation()

          model_trainer_config=config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
          model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
          model_trainer_artifact=model_trainer.initiate_model_trainer()
         
     except Exception as e:
          print(e)