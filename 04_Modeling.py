
# Import Library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
import lightgbm as lgb
import xgboost as xgb
import catboost as ctb


# Load Data
target = pd.read_csv('train_target.csv', header=None)
submission = pd.read_csv('sample_submission.csv')


# Define Functions
def RMSLE(real, pred):
    r = [np.log(x+1) for x in real]
    p = [np.log(x+1) for x in pred]
    
    rmsle = (np.sum(np.subtract(p, r) ** 2) / len(pred)) ** 0.5
    return rmsle


def check_important_features(feature_importances_, features):
    important_features = pd.Series(feature_importances_, index=features)
    important_features = important_features.loc[important_features > 0].nlargest(100)        
    return important_features


def lgbm(X_train, X_val, y_train, y_val, test_data):
    params = {
            'objective': 'regression',
            'metric': 'rmse',
            'num_leaves': 40,
            'learning_rate': 0.005,
            'bagging_fraction': 0.6,
            'featrue_fraction': 0.6,
            'bagging_frequency': 6,
            'bagging_seed': 0,
            'verbosity': -1,
            'seed':0
            }
    
    train = lgb.Dataset(X_train, label=y_train)
    valid = lgb.Dataset(X_val, label=y_val)
    
    evals_result = {}
    
    model = lgb.train(params, train, 5000,
                      valid_sets=[train,valid],
                      early_stopping_rounds=100,
                      verbose_eval=200,
                      evals_result=evals_result)
    
    real = np.exp(y_train) - 1
    pred = model.predict(X_train, num_iteration=model.best_iteration)
    pred = np.exp(pred) - 1
    
    rmsle = RMSLE(real, pred)
    print('RMSLE of Train data : ', rmsle)
    
    real = np.exp(y_val) - 1
    pred = model.predict(X_val, num_iteration=model.best_iteration)
    pred = np.exp(pred) - 1
    
    rmsle = RMSLE(real, pred)
    print('RMSLE of Test data : ', rmsle) 
    
    pred = model.predict(test_data, num_iteration=model.best_iteration)
    pred = np.exp(pred) - 1
    
    return pred, evals_result, model


# ----------------------------------------------------------------------------------------------
# Load Data
train = pd.read_csv('train_remove_constant.csv')
test = pd.read_csv('test_remove_constant.csv')


# Divid Data
X_train, X_val, y_train, y_val = train_test_split(train, target[0], test_size=0.2, random_state=0)
print('X_train size : ', X_train.shape)
print('X_val size : ', X_val.shape)
print('y_train size : ', y_train.shape)
print('y_val size : ', y_val.shape)


# Train the Model
lgb_pred, result, boost = lgbm(X_train, X_val, y_train, y_val, test)


# ----------------------------------------------------------------------------------------------
# Load Data
train = pd.read_csv('train_use_feat_90.csv')
test = pd.read_csv('test_use_feat_90.csv')



# Divid Data
X_train, X_val, y_train, y_val = train_test_split(train, target[0], test_size=0.2, random_state=0)
print('X_train size : ', X_train.shape)
print('X_val size : ', X_val.shape)
print('y_train size : ', y_train.shape)
print('y_val size : ', y_val.shape)


# Train the Model
lgb_pred, result, boost = lgbm(X_train, X_val, y_train, y_val, test)
submission['target'] = lgb_pred
submission.to_csv('lgb_90_pred.csv', index=False)


# ----------------------------------------------------------------------------------------------
# Load Data
train = pd.read_csv('train_use_feat_80.csv')
test = pd.read_csv('test_use_feat_80.csv')



# Divid Data
X_train, X_val, y_train, y_val = train_test_split(train, target[0], test_size=0.2, random_state=0)
print('X_train size : ', X_train.shape)
print('X_val size : ', X_val.shape)
print('y_train size : ', y_train.shape)
print('y_val size : ', y_val.shape)


# Train the Model
lgb_pred, result, boost = lgbm(X_train, X_val, y_train, y_val, test)
submission['target'] = lgb_pred
submission.to_csv('lgb_80_pred.csv', index=False)


# ----------------------------------------------------------------------------------------------
# Load Data
train = pd.read_csv('train_use_feat_70.csv')
test = pd.read_csv('test_use_feat_70.csv')



# Divid Data
X_train, X_val, y_train, y_val = train_test_split(train, target[0], test_size=0.2, random_state=0)
print('X_train size : ', X_train.shape)
print('X_val size : ', X_val.shape)
print('y_train size : ', y_train.shape)
print('y_val size : ', y_val.shape)


# Train the Model
lgb_pred, result, boost = lgbm(X_train, X_val, y_train, y_val, test)
submission['target'] = lgb_pred
submission.to_csv('lgb_70_pred.csv', index=False)



