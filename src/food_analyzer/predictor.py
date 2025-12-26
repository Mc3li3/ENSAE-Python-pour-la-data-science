from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd


class NutriModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.encoder = LabelEncoder()
        # L'ordre est CRUCIAL pour la prédiction future
        self.features = ['Energie', 'Sucre', 'Gras', 'Saturés', 'Sel', 'Fibres', 'Protéines']

    def train(self, df):
        """Entraîne le modèle sur le DataFrame donné"""
        X = df[self.features]
        y = self.encoder.fit_transform(df['Nutriscore'])
        self.model.fit(X, y)
        accuracy = self.model.score(X, y)
        return accuracy

    def predict(self, values_dict):
        """Prédit le score pour un produit imaginaire"""
        # On s'assure que les données sont dans le bon ordre
        data = pd.DataFrame([values_dict], columns=self.features)
        prediction_code = self.model.predict(data)[0]
        return self.encoder.inverse_transform([prediction_code])[0]
