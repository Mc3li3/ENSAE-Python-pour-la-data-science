# 🕵️‍♂️ Reverse Engineering du Nutri-Score via OpenFoodFacts

## 📋 À propos du projet

Nous vivons une époque paradoxale : nous n'avons jamais eu accès à autant d'informations nutritionnelles, et pourtant, il n'a jamais été aussi difficile de savoir ce que l'on mange vraiment. Le **Nutri-Score** est apparu comme une solution miracle, mais pour un Data Scientist, cela reste souvent une "boîte noire".

Ce projet ne se contente pas d'analyser des données, il cherche à **"cracker" le code du Nutri-Score**.

🎯 **Problématique**
Notre projet cherche à répondre à une question centrale :

Les données déclaratives d'OpenFoodFacts sont-elles suffisamment fiables et structurées pour nous permettre de redécouvrir, par l'analyse statistique et le Machine Learning, les règles cachées du Nutri-Score ?

Pour y répondre, nous avons découpé notre approche en trois étapes logiques :

1. Exploration & Diagnostic (Data Viz) : Avant de vouloir prédire, nous devons comprendre. Les distributions de sucre ou de gras sont-elles cohérentes ? Y a-t-il des anomalies évidentes ou des tendances surprenantes (comme le poids réel du sel ou des fruits) qui contredisent l'intuition ?

2. Nettoyage & Préparation (Data Engineering) : Peut-on transformer une base de données collaborative "bruitée" (erreurs de saisie, valeurs manquantes) en un dataset propre, respectant les lois physico-chimiques, apte à entraîner une intelligence artificielle ?

3. Modélisation (Machine Learning) : Un algorithme comme le Random Forest peut-il apprendre tout seul la formule du Nutri-Score ? Avons-nous besoin de l'aider en lui fournissant des indices "métier" (Smart Features) pour qu'il atteigne une performance satisfaisante ?

> **Approche frugale :**
> Nous avons fait le choix conscient de travailler sur un échantillon représentatif et méticuleusement nettoyé plutôt que sur le Big Data brut. Nous privilégions la qualité de la méthodologie et la pertinence des variables (*Smart Features*) à la quantité massive de données, réduisant ainsi l'empreinte écologique de nos calculs.

## 🔄 Contexte et Pivot Technique

Ce projet est le fruit d'une adaptation. Initialement conçu pour l'analyse musicale via l'API Spotify, nous avons opéré un pivot stratégique suite à la découverte d'une dépréciation soudaine de l'endpoint `audio_features` par Spotify en novembre 2024.

Nous avons transformé cette contrainte en opportunité en nous tournant vers **OpenFoodFacts**, une source de données plus complexe, collaborative, et offrant de véritables défis en termes de nettoyage de données (*Data Cleaning*) et de modélisation.

## 🚀 Démarrage Rapide

Le cœur du projet et l'intégralité du code se trouvent dans le dossier `src`. Tout a été conçu pour être exécuté séquentiellement via un Notebook Jupyter unique.

### 1. Environnement
Il est conseillé d'éxécuter ce projet sur une instance du **SSP Cloud** (ou tout environnement JupyterLab standard avec Python 3.8+).

### 2. Exécution
Toute la logique (Récupération API → Nettoyage → Visualisation → Machine Learning) est centralisée dans un seul fichier :

👉 **`src/main.ipynb`**

**Procédure :**
1.  Ouvrez le dossier `src/` dans votre explorateur de fichiers.
2.  Ouvrez le fichier `main.ipynb`.
3.  **Exécutez la première cellule** : elle contient les commandes magiques (`%pip install ...`) pour installer automatiquement toutes les dépendances nécessaires (`pandas`, `scikit-learn`, `plotly`, etc.).
4.  Exécutez les cellules suivantes séquentiellement pour dérouler l'analyse.

## 🛠️ Stack Technique

Ce projet met en œuvre un pipeline de Data Science complet :

### 📥 Data Engineering & Cleaning
* **Requests :** Extraction de données via l'API OpenFoodFacts (gestion de JSON imbriqués).
* **Pandas :** Nettoyage drastique basés sur des règles physico-chimiques (règle des 100g, cohérence calorique).
* **Gestion des données manquants :** Refus de l'imputation par la moyenne pour garantir la pureté des données d'entraînement.

### 📊 Data Visualization
* **Plotly :** Graphiques interactifs pour l'exploration multidimensionnelle.
* **Matplotlib / Seaborn :** Visualisation des matrices de confusion et courbes d'importance.

### 🤖 Machine Learning & IA
* **Algorithmes :** Random Forest Classifier (pour gérer les effets de seuil et la non-linéarité).
* **Validation :** Stratified K-Fold Cross-Validation (pour assurer la robustesse statistique).
* **Optimisation :** GridSearchCV (Tuning des hyperparamètres).
* **Feature Engineering (Le cœur du projet) :** Création de "Smart Features" (Ratios énergétiques, simulation des points N/P) par Reverse Engineering pour injecter de la connaissance métier dans le modèle.

## 👥 Auteurs
Aaron HADDAD et Elie ATTALI