import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier


class NutriModel:
    def __init__(self, df):
        self.df = df.copy()
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.features_names = []
        self.target_col = 'Nutriscore'
        
        # Features de base
        self.basic_features = ['Energie', 'Sucre', 'Gras', 'Saturés', 'Sel', 'Fibres', 'Protéines', 'Fruits et Légumes']
        # Features intelligentes
        self.smart_features_list = ['Ratio_Sucre_Energie', 'Ratio_Gras_Energie', 'Est_Points_Negatifs', 'Est_Points_Positifs', 'Est_Score_Final']

    def add_smart_features(self):
        """ [ETAPE 4] Ajoute les calculs 'maison' au DataFrame """
        print("🧠 Injection des connaissances humaines (Smart Features)...")
        df = self.df
        epsilon = 0.0001
        
        # Ratios et Estimations
        df['Ratio_Sucre_Energie'] = (df['Sucre'] * 4) / (df['Energie'] + epsilon)
        df['Ratio_Gras_Energie'] = (df['Gras'] * 9) / (df['Energie'] + epsilon)
        df['Est_Points_Negatifs'] = (df['Energie']/335) + (df['Saturés']/1) + (df['Sucre']/4.5) + (df['Sel']/0.09)
        df['Est_Points_Positifs'] = (df['Fibres']/0.9) + (df['Protéines']/1.6) + (df['Fruits et Légumes']/20)
        df['Est_Score_Final'] = df['Est_Points_Negatifs'] - df['Est_Points_Positifs']
        
        print("✅ Colonnes calculées ajoutées !")

    def prepare_data(self, include_categorical=False):
        """ Prépare X et y dynamiquement selon ce qui est dispo """
        # Détection des colonnes
        features_to_use = self.basic_features.copy()
        if 'Est_Score_Final' in self.df.columns:
            print(f"😎 Mode EXPERT : {len(self.smart_features_list)} smart features détectées.")
            features_to_use += self.smart_features_list
        else:
            print("👶 Mode BASIC : Utilisation des nutriments bruts.")

        # Nettoyage
        clean_df = self.df.dropna(subset=features_to_use + [self.target_col]).copy()
        
        # Encodage One-Hot (Catégories)
        if include_categorical and 'Category_Label' in clean_df.columns:
            X = pd.get_dummies(clean_df[features_to_use + ['Category_Label']], columns=['Category_Label'])
        else:
            X = clean_df[features_to_use]

        y = clean_df[self.target_col]
        self.features_names = X.columns.tolist()
        
        # Split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        print(f"✅ Dataset prêt : {X.shape[1]} variables en entrée.")

    def train(self):
        """ Entraîne un modèle par défaut """
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(self.X_train, self.y_train)

    def evaluate(self, method="simple"):
        """ Retourne le score (Simple ou Cross-Val) """
        if self.model is None: self.train()
        
        if method == "cross_val":
            cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
            # On recolle tout pour la CV
            X_full = pd.concat([self.X_train, self.X_test])
            y_full = pd.concat([self.y_train, self.y_test])
            scores = cross_val_score(self.model, X_full, y_full, cv=cv, scoring='accuracy', n_jobs=-1)
            print(f"📊 CV Score : {scores.mean():.2%} (+/- {scores.std():.2%})")
            return scores.mean()
        else:
            score = self.model.score(self.X_test, self.y_test)
            print(f"🎯 Test Score : {score:.2%}")
            return score

    def optimize_hyperparameters(self):
        """ [ETAPE 3 & 5] GridSearch """
        print("🔧 Optimisation en cours (Patience...)...")
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [None, 15, 30],
            'min_samples_split': [2, 10],
            'min_samples_leaf': [1, 4]
        }
        rf = RandomForestClassifier(random_state=42)
        grid = GridSearchCV(rf, param_grid, cv=3, n_jobs=-1, verbose=1)
        grid.fit(self.X_train, self.y_train)
        
        print(f"🎉 Meilleurs params : {grid.best_params_}")
        self.model = grid.best_estimator_ # On garde le meilleur

    def plot_feature_importance(self, top_n=15, custom_title=None):
        """ Affiche les features les plus importantes avec un titre personnalisable """
        if self.model is None: return
        
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        # Gestion du nombre de barres
        actual_n = min(top_n, len(importances))
        
        plt.figure(figsize=(10, 5))
        
        # Titre dynamique
        if custom_title:
            plt.title(custom_title)
        else:
            plt.title(f"Top {actual_n} Features Importantes")
            
        plt.bar(range(actual_n), importances[indices][:actual_n], color="skyblue")
        
        names = [self.features_names[i] for i in indices][:actual_n]
        plt.xticks(range(actual_n), names, rotation=45, ha='right')
        
        plt.tight_layout()
        plt.show()