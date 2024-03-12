from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

""" Pour Utiliser cette function mettre 'from pipeline import pipeline_create'
"""
def pipeline_create(dataset, X_train, model):  

    
    def separate_column_types():

        numerical_cols = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_cols = X_train.select_dtypes(include=['object']).columns.tolist()

        return numerical_cols, categorical_cols

    numerical_cols, categorical_cols = separate_column_types( )

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

    full_pipeline = make_pipeline(preprocessor, model)
    return full_pipeline