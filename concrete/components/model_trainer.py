from concrete import utils
from concrete.entity import config_entity
from concrete.entity import artifact_entity
from concrete.exception import ConcreteException
from concrete.logger import logging
import os,sys
from xgboost import XGBRegressor
from concrete import utils
from sklearn.metrics import r2_score

class ModelTrainer:
    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact
                ):
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact

        except Exception as e:
            raise ConcreteException(e, sys)

    
    def train_model(self,x,y):
        try:
            xgb_reg=XGBRegressor()
            xgb_reg.fit(x,y)
            return xgb_reg
        except Exception as e:
            raise ConcreteException(e, sys)

    def initiate_model_trainer(self,)->artifact_entity.ModelTrainerArtifact:
        try:
            logging.info(f"Loading train and test array.")
            train_arr=utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr=utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)

            logging.info(f"Splitting input and target feature from both train and test arr.")
            X_train,y_train=train_arr[:,:-1],train_arr[:,-1]
            X_test,y_test=test_arr[:,:-1],test_arr[:,-1]

            logging.info(f"Train the model")
            model=self.train_model(x=X_train,y=y_train)

            logging.info(f"Calculating r2 train score")
            yhat_train=model.predict(X_train)
            r2_train_score=r2_score(y_true=y_train,y_pred=yhat_train)

            logging.info(f"Calculating r2 test score")
            yhat_test=model.predict(X_test)
            r2_test_score=r2_score(y_true=yhat_test,y_pred=yhat_test)

            logging.info(f"train score:{r2_train_score} and tests score {r2_test_score}")
            #check for overfitting 0r underfitting or expected score
            logging.info(f"Checking if our model is underfitting or not")
            if r2_test_score<self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good as it is not able to give \
                expected accuracy:{self.model_trainer_config.expected_score}: model actual score:{r2_test_score}")

            logging.info(f"Checking if our model is overfiiting or not")
            diff= abs(r2_train_score-r2_test_score)

            if diff>self.model_trainer_config.overfitting_threshold:
                    raise Exception(f"Train and Test score diff: {diff} is more than Overfitting threshold {self.model_trainer_config.overfitting_threshold}")
            
            #save the trained model
            logging.info(f"Saving mode object")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

            #prepare artifact
            logging.info(f"Prepare the artifact")
            model_trainer_artifact=artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path,
            r2_train_score=r2_train_score, r2_test_score=r2_test_score)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise ConcreteException(e, sys)
