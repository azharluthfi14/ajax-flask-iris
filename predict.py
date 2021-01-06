import pandas as pd
import numpy as np
import joblib


def predict_iris(sl, sw, pl, pw):
    model_learning = joblib.load(
        r"F:\MyFlask\Project1\backend\model\svm_model_iris.pkl")
    result = model_learning.predict([[sl, sw, pl, pw]])
    classification = result[0]
    
    return classification
