from concrete.predictor import ModelResolver
from concrete.entity.config_entity import ModelPusherConfig
from concrete.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact,ModelPusherArtifact
from concrete.exception import ConcreteException
import os,sys
from concrete.logger import logging
from concrete.utils import  load_object , save_object
class ModelPusher:

    def __init__(self,model_pusher_config:ModelPusherConfig,
    data_transformation_artifact:DataTransformationArtifact,
    model_trainer_artifact:ModelTrainerArtifact):
        try:
            logging.info(f"{'>>'*20} Model Pusher {'<<'*20}")
            self.model_pusher_config=model_pusher_config
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver=ModelResolver(model_registry=self.model_pusher_config.saved_model_dir)
        except Exception as e:
            raise ConcreteException(e, sys)

    def initiate_model_pusher(self,)->ModelPusherArtifact:
        try:
            
            #load object
            logging.info(f"loading transformer , model and target scaler path")
            transformer=load_object(file_path=self.data_transformation_artifact.transform_object_path)
            model= load_object(file_path=self.model_trainer_artifact.model_path)
            target_scaler=load_object(file_path=self.data_transformation_artifact.target_scaler_path)


            #model pusher dir
            logging.info(f"saving model into model pusher dir")
            save_object(file_path=self.model_pusher_config.pusher_transformer_path, obj=transformer)
            save_object(file_path=self.model_pusher_config.pusher_model_path, obj=model)
            save_object(file_path=self.model_pusher_config.pusher_target_scaler_path, obj=target_scaler)


            #saved model dir
            logging.info(f"saving model into saved model  dir")
            transformer_path=self.model_resolver.get_latest_save_transformer_path()
            model_path=self.model_resolver.get_latest_save_model_path()
            target_scaler_path=self.model_resolver.get_latest_save_target_scaler_path()



            save_object(file_path=transformer_path, obj=transformer)
            save_object(file_path=model_path, obj=model)
            save_object(file_path=target_scaler_path, obj=target_scaler)


            model_pusher_artifact=ModelPusherArtifact(push_model_dir=self.model_pusher_config.pusher_model_dir,
            saved_model_dir=self.model_pusher_config.saved_model_dir)
            logging.info(f"model pusher artifact:{model_pusher_artifact}")
            return model_pusher_artifact

        except Exception as e:
            raise ConcreteException(e, sys)


