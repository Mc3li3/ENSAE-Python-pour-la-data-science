# 🍎 Analyse de la Fiabilité du Nutriscore via OpenFoodFacts

## 📋 Description du Projet
Ce projet de Data Science explore la relation entre le **Nutriscore** (A à E) et la composition nutritionnelle réelle des produits alimentaires (sucre, gras, calories).

En utilisant l'API publique d'**OpenFoodFacts**, nous avons extrait, nettoyé et analysé des données sur plusieurs catégories de produits (biscuits, céréales, snacks) pour répondre à la question suivante :
> *"Le Nutriscore sanctionne-t-il efficacement les produits trop sucrés ou trop gras, ou existe-t-il des anomalies dans la distribution ?"*

## 🔄 Contexte et Pivot Technique
Initialement orienté vers l'analyse musicale via l'API Spotify, ce projet a dû être réorienté suite à la dépréciation majeure de l'endpoint `audio_features` par Spotify en novembre 2024. Ce pivot a permis de se concentrer sur une source de données plus riche et permettant une analyse statistique plus poussée (OpenFoodFacts).

## 🛠️ Stack Technique
Ce projet met en œuvre les compétences clés du traitement de données avec Python :
* **Récupération de données (API) :** `requests` (traitement de JSON imbriqués).
* **Manipulation de données :** `pandas` (Nettoyage, filtrage, gestion des `NaN`).
* **Visualisation :** `seaborn` et `matplotlib` (Boxplots, Scatterplots multidimensionnels).
* **Versionning :** Git & GitHub.

## 🚀 Installation et Utilisation

### 1. Prérequis
Assurez-vous d'avoir Python installé (version 3.8+ recommandée).

### 2. Installation des dépendances
Clonez le dépôt et installez les librairies nécessaires via le fichier `requirements.txt` :

```bash
pip install -r requirements.txt