from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_selection import RFECV

# Pour Utiliser cette function mettre 'from pipeline import pipeline_create'

def pipeline_create(X_train, estimator): 

    
    def separate_column_types():

        numerical_cols = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_cols = X_train.select_dtypes(include=['object']).columns.tolist()

        return numerical_cols, categorical_cols

    numerical_cols, categorical_cols = separate_column_types()

    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler()),
    ])

    # Categorical pipeline
    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore')),
    ])

    # Full preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_pipeline, numerical_cols),
            ('cat', cat_pipeline, categorical_cols),
        ])
    
    rfecv = RFECV(estimator=estimator, step=1, cv=5, scoring='neg_mean_squared_error', min_features_to_select=1)

    # Création du pipeline final avec un nom pour l'étape ElasticNet
    full_pipeline_elasticnet = Pipeline([
        ('preprocessor', preprocessor),
        ('rfecv', rfecv)
    ])

    return full_pipeline_elasticnet