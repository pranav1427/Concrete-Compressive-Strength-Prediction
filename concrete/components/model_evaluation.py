from concrete.predictor import ModelResolver
from concrete.entity import config_entity,artifact_entity
from concrete.exception import ConcreteException
from concrete.logger import logging
from concrete.utils import load_object
from sklearn.metrics import r2_score
import pandas as pd
import os, sys
from concrete.config import TARGET_COLUMN
import numpy as np 




class ModelEvaluation:
    def __init__(self,
        model_eval_config:config_entity.ModelEvaluationConfig,
        data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
        data_transformation_artifact:artifact_entity.DataTransformationArtifact,
        model_trainer_artifact:artifact_entity.ModelTrainerArtifact
        ):
        try:
            logging.info(f"{'>>'*20} Model Evaluation {'<<'*20}")
            self.model_eval_config=model_eval_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver=ModelResolver()
        except Exception as e:
            raise ConcreteException(e,sys)

    def initiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:
            # if saved model  folder  has model then we will compare which is best
            logging.info(f"if saved model  folder  has model then we will compare which is best")
            latest_dir_path=self.model_resolver.get_latest_dir_path()
            if latest_dir_path==None:
                model_eval_artifact=artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, improved_accuracy=None)
                logging.info(f"model evaluation artifact:{model_eval_artifact}")
                return model_eval_artifact

            #finding location of transformer , model and target scaler
            logging.info(f"finding location of transformer , model and target scaler")
            transformer_path=self.model_resolver.get_latest_transformer_path()
            model_path=self.model_resolver.get_latest_model_path()
            
            

            logging.info(f"previously trained objects of transformer , model and target scaler")
            #previously trained objects
            transformer=load_object(file_path=transformer_path)
            model= load_object(file_path=model_path)
            

            logging.info(f"currently trained objects of transformer , model and target scaler")
            #currently trained model objects
            current_transformer=load_object(file_path=self.data_transformation_artifact.transform_object_path)
            current_model=load_object(file_path=self.model_trainer_artifact.model_path)
            

            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)
            target_df= test_df[TARGET_COLUMN]
            y_true=(target_df)
            #accuracy using previous trained model
            logging.info(f"accuracy using previous trained model")

            input_feature_name=list(transformer.feature_names_in_)
            input_arr=transformer.transform(test_df[input_feature_name])
            y_pred=model.predict(input_arr)
            
            print(f"prediction using previous model: {(y_pred[:5])}")
            previous_model_score=r2_score(y_true=y_true,y_pred=y_pred)
            logging.info(f"accuracy using previous trained model:{previous_model_score}")
            
            #accuracy using currrent trained model
            input_feature_name=list(current_transformer.feature_names_in_)
            input_arr=current_transformer.transform(test_df[input_feature_name])
            y_pred=current_model.predict(input_arr)
            y_true=(target_df)
            
            print(f"prediction using trained model: {(y_pred[:5])}")
            current_model_score=r2_score(y_true=y_true,y_pred=y_pred)
            logging.info(f"accuracy using current trained model:{current_model_score}")

            if current_model_score<=previous_model_score:
                logging.info(f"current trained model is not better than previous trained model")
                raise Exception("current trained model is not better than previous trained model")

            model_eval_artifact=artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
            improved_accuracy=current_model_score-previous_model_score)


            logging.info(f"Model eval artifact:{model_eval_artifact}")
            return model_eval_artifact
    
        except Exception as e:
            raise ConcreteException(e, sys)

        

