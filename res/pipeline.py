from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np
import matplotlib.pyplot as plt


""" Pour utiliser ces méthodes, importer le fichier : 'from pipeline import pipeline_create'

    Ensuite, créer un objet ML_pipeline : model = ML_pipeline(SVR(), X, y)
    
    Méthodes :
        data_conversion :
         
            Retourne un pipeline de transformations pour le modèle et les X, 
            y spécifié lors la création de notre objet ML_pipeline. A utiliser dans
            GridSearchCV en tant qu'estimateur :
            
            Exemple : 
            sbr_cv = GridSearchCV(svr.full_pipeline, param_grid = param_grid, cv=5, scoring="neg_mean_squared_error")
        
        model_train_and_eval : 
        
            Prends en argument un Based estimator de GridSearchCV.
            
                - entraîne et évalue le modèle avec kfold
                - mesure le score mse, rmse et r2
                
        ML_pipeline.make_graph([model_1, model_2, model_3]) : Pour créer le graphique comparant        
        les scores de chaque modèle
                
    Attributs utiles :
    
        self.mean_mse_score : Score MSE du modèle
        self.mean_rmse_score : Score RMSE du modèle
        self.mean_r2_score : Score R2 du modèle
        self.best_params : Listes des paramètres optimaux choisis par GridSearchCV  
        
"""

class ML_pipeline:
    
    def __init__(self, estimator, X_array, y_array):
        self.estimator = estimator
        self.X_array = X_array
        self.y_array = y_array
        self.preprocessor = None
        self.full_pipeline = None
        self.estimator_cv = None
        self.mean_mse_score = None
        self.mean_rmse_score = None
        self.mean_r2_score = None
        self.best_params = None
        self.print_model_stats
        return self.full_pipeline
    
    def data_conversion(self):
        
        numerical_cols = self.X_array.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_cols = self.X_array.select_dtypes(include=['object']).columns.tolist()
        
        # Numerical pipeline
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
        self.preprocessor = preprocessor
        
        full_pipeline = make_pipeline(self.preprocessor, self.estimator)
        self.full_pipeline = full_pipeline
        
        return self.full_pipeline
        
        
      
    
    def model_train_and_eval(self, estimator_cv, nb_of_splits=5):
        
        self.estimator_cv = estimator_cv
        
        kf = KFold(n_splits=nb_of_splits, shuffle=True, random_state=42)
        # Initialiser des listes pour enregistrer les scores pour chaque pli
        mse_scores = []
        rmse_scores = []
        r2_scores = []

        # Boucler sur chaque pli défini par KFold
        for train_index, test_index in kf.split(self.X_array):

            # On redéfini les données d'apprentissage et de test pour chaque pli
            X_train, X_test = self.X_array.iloc[train_index], self.X_array.iloc[test_index]
            y_train, y_test = self.y_array.iloc[train_index], self.y_array.iloc[test_index]
    

            self.estimator_cv.fit(X_train, y_train)
            y_pred = self.estimator_cv.predict(X_test)

            # Calcul du MSE
            mse = mean_squared_error(y_test, y_pred)
            mse_scores.append(mse)
    
            # Calcul du RMSE
            rmse = np.sqrt(mse)
            rmse_scores.append(rmse)
    
            # Calcul du R2
            r2 = r2_score(y_test, y_pred)
            r2_scores.append(r2)
            
        self.mean_mse_score = np.mean(mse_scores)
        self.mean_rmse_score = np.mean(rmse_scores)
        self.mean_r2_score = np.mean(r2_scores)
        self.best_params = estimator_cv.best_params_
        
    def print_model_stats(self):
        print(str(self.estimator))
        print(f"Mean MSE Score : {self.mean_mse_score}")
        print(f"Mean RMSE Score : {self.mean_rmse_score}")
        print(f"Mean R2 Score : {self.mean_r2_score}")
        print(f"Best GridSearch parameters : {self.best_params}")
    
    
    
    # Prend en entrée un tableau des objets ML_pipeline
    def make_graph(models : list):
        
        # Instanciation des listes pour récupérer les scores de chaque modèles
        rmse_scores =  [] 
        mse_scores = [] 
        r2_scores =  []
        model_stats = []

        
        for model in models : 
            rmse_scores.append(model.mean_rmse_score)
            mse_scores.append(model.mean_mse_score)
            r2_scores.append(model.mean_r2_score)
            model_stats.append(model.print_model_stats())
            
            
      # X-axis positions
        x = np.arange(len(models))

    #   Largeur des barres
        width = 0.2

        # Mise en graph des barres
        plt.bar(x + width*2, r2_scores, width=width, label='R²')
        plt.bar(x, rmse_scores, width=width, label='RMSE')
        plt.bar(x + width, mse_scores, width=width, label='MSE')
        

        # Ajout labels et titre
        plt.xlabel('Modèles')
        plt.ylabel('Scores')
        plt.title('Comparaison des modèles')

        # Ajout des labels pour l'axe X en fonction du nom de l'estimateur
        plt.xticks(x + width, [i.estimator for i in models])
    
        plt.legend()
        
        
        
        return (plt.show(), [i for i in model_stats])

    



        