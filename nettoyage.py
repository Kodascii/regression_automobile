from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.svm import SVR
from sklearn.linear_model import ElasticNet
import pandas as pd
import numpy as np


from res.csv_cleaner_ import clean_mileage_engine_power_
from pipeline import pipeline_create

model  = SVR()
# model = ElasticNet()

dataset = pd.read_csv('res/train.csv')

dataset = clean_mileage_engine_power_(dataset)

print(dataset.head())

dataset = dataset.drop('New_Price', axis=1)

X = dataset.drop('Price', axis=1)
y = dataset['Price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


param_grid = {
    'C': [0.1, 1, 10, 100], 
    'gamma': ['scale','auto'], 
    'kernel': ['rbf', 'linear']
    }

# param_grid = {
#     'alpha': [0.1, 1, 10],
#     'l1_ratio': [0.1, 0.5, 0.9],
#     'max_iter': [1000, 5000, 10000]
# }

model = GridSearchCV(model, param_grid, cv=5, verbose=1)


full_pipeline = pipeline_create(dataset, X_train, model)

full_pipeline.fit(X_train, y_train)

y_pred = full_pipeline.predict(X_test)
y = y.reset_index(drop=True)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)


# kf = KFold(n_splits=10, shuffle=True, random_state=42)

mse_scores = []
rmse_scores = []
r2_scores = []

"""for train_index, test_index in kf.split(X):
    X_train_kf, X_test_kf = X.iloc[train_index], X.iloc[test_index]
    y_train_kf, y_test_kf = y.iloc[train_index], y.iloc[test_index]  # Use iloc here as well
    
    # Fit the pipeline to the training data
    full_pipeline.fit(X_train_kf, y_train_kf)
    
    # Predict on the testing set
    y_pred_kf = full_pipeline.predict(X_test_kf)
    
    # Calculate metrics
    mse = mean_squared_error(y_test_kf, y_pred_kf)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test_kf, y_pred_kf)
    
    # Append to lists
    mse_scores.append(mse)
    rmse_scores.append(rmse)
    r2_scores.append(r2)
"""

mse_scores.append(mse)
rmse_scores.append(rmse)
r2_scores.append(r2)


print(f"Average R2 score across folds: {np.mean(r2_scores)}")
print(f"Average Root Mean Squared Error across folds: {np.mean(rmse_scores)}")
print(f"Average Mean Squared Error across folds: {np.mean(mse_scores)}")