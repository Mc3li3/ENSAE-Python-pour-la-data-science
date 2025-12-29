# 🕵️‍♂️ Reverse Engineering du Nutri-Score via OpenFoodFacts

## 📋 À propos du projet

Nous vivons une époque paradoxale : nous n'avons jamais eu accès à autant d'informations nutritionnelles, et pourtant, il n'a jamais été aussi difficile de savoir ce que l'on mange vraiment. Le **Nutri-Score** est apparu comme une solution miracle, mais pour un Data Scientist, cela reste souvent une "boîte noire".

Ce projet ne se contente pas d'analyser des données, il cherche à **"cracker" le code du Nutri-Score**.

🎯 **Problématique**

Notre projet s'articule autour d'une question centrale :

> **Au-delà de la note finale (A, B, C...), quels sont les nutriments qui pèsent réellement le plus lourd dans la balance du Nutri-Score ?**

L'algorithme officiel est complexe, mais notre objectif est de vérifier si, à partir des données réelles d'OpenFoodFacts, nous pouvons établir une **hiérarchie claire des facteurs d'influence**.

---

### Notre démarche en 3 étapes

Pour y parvenir, nous avons structuré notre analyse de la manière suivante :

#### 1. Exploration & Qualité de la donnée (Data Viz)
**Avant tout, les données déclaratives sont-elles fiables ?**
Nous chercherons à observer des corrélations évidentes (ex: Gras vs Nutri-Score) ou à détecter des anomalies de distribution qui pourraient fausser notre analyse.

#### 2. Nettoyage (Data Cleaning)
**Comment isoler un échantillon représentatif et sain ?**
L'enjeu est d'éliminer les erreurs de saisie (valeurs aberrantes, incohérences physico-chimiques) pour garantir que le modèle ne soit pas biaisé par du bruit numérique.

#### 3. Modélisation & Interprétabilité (Machine Learning)
En entraînant un modèle (**Random Forest**), nous ne cherchons pas seulement à prédire la note, mais à **interroger le modèle** pour comprendre sa logique interne :

* Le sucre est-il plus pénalisant que le gras ?
* Le sel joue-t-il un rôle marginal ou décisif ?
* L'ajout de connaissances métier (**Smart Features**) change-t-il la perception du modèle sur l'importance des variables ?

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


### ⚙️ Méthodologie : Collaboration et Reproductibilité (CI/CD)

Pour garantir la robustesse technique de notre projet, nous avons adopté un flux de travail inspiré des standards de l'industrie. Le développement s'est articulé autour de **Pull Requests**, imposant une relecture (parfois croisée) du code avant fusion dans la branche principale.

En parallèle, nous avons mis en place un pipeline d'intégration continue (CI) via **GitHub Actions**. Ce système automatise l'installation des dépendances et l'exécution du notebook à chaque modification, nous assurant que l'environnement est stable et que nos résultats sont parfaitement **reproductibles**, indépendamment de nos machines locales.


## 🛠️ Stack Technique

Ce projet met en œuvre un pipeline de Data Science complet :

### 📥 Data Engineering & Cleaning
* **Requests :** Extraction de données via l'API OpenFoodFacts (gestion de JSON imbriqués).
* **Pandas :** Nettoyage drastique basés sur des règles physico-chimiques (règle des 100g, cohérence calorique).
* **Gestion des données manquants :** Refus de l'imputation par la moyenne pour garantir la pureté des données d'entraînement.

### 📊 Data Visualization
* **Plotly :** Graphiques interactifs pour l'exploration multidimensionnelle.
* **Matplotlib / Seaborn :** Visualisation des matrices de confusion et courbes d'importance.

### 🤖 Machine Learning
* **Algorithmes :** Random Forest Classifier (pour gérer les effets de seuil et la non-linéarité).
* **Validation :** Stratified K-Fold Cross-Validation (pour assurer la robustesse statistique).
* **Optimisation :** GridSearchCV (Tuning des hyperparamètres).
* **Feature Engineering (Le cœur du projet) :** Création de "Smart Features" (Ratios énergétiques, simulation des points N/P) par Reverse Engineering pour injecter de la connaissance métier dans le modèle.

## 👥 Auteurs
Aaron HADDAD et Elie ATTALI